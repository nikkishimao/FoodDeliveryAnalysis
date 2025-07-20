import pandas as pd
import mysql.connector
import numpy as np
from datetime import datetime
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_datetime(date_str):
    """Parse datetime from 'DD HH:MM:SS' format with robust error handling"""
    if pd.isna(date_str) or str(date_str).strip() == '':
        return None
    try:
        parts = str(date_str).split()
        if len(parts) != 2:
            return None
        day_part, time_part = parts
        day = int(day_part)
        now = datetime.now()
        return datetime.strptime(f"{now.year}-{now.month}-{day} {time_part}", "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.warning(f"Error parsing datetime {date_str}: {e}")
        return None

def validate_column_names(df, required_columns):
    """Ensure all required columns exist in the DataFrame"""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in CSV: {missing_columns}")

def main():
    try:
        # 1. Load and prepare data
        logger.info("Loading CSV data...")
        required_columns = [
            'Consumer_ID', 'Driver_ID', 'Restaurant_ID',
            'Customer_placed_order_datetime', 'Placed_order_with_restaurant_datetime',
            'Driver_at_restaurant_datetime', 'Delivered_to_consumer_datetime',
            'Is_New', 'Delivery_Region', 'Is_ASAP',
            'Order_total', 'Amount_of_discount', 'Amount_of_tip', 'Refunded_amount'
        ]
        df = pd.read_csv("data.csv").replace({np.nan: None})
        validate_column_names(df, required_columns)

        # Convert datetime fields
        logger.info("Processing datetime fields...")
        datetime_cols = [
            'Customer_placed_order_datetime',
            'Placed_order_with_restaurant_datetime',
            'Driver_at_restaurant_datetime',
            'Delivered_to_consumer_datetime'
        ]
        for col in datetime_cols:
            df[col] = df[col].apply(parse_datetime)

        # Filter required rows
        df = df.dropna(subset=['Customer_placed_order_datetime', 'Delivered_to_consumer_datetime'])
        logger.info(f"Rows to process: {len(df)}")

        # 2. Connect to MySQL
        logger.info("Connecting to MySQL...")
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="**********",
                database="food_delivery_dw",
                autocommit=False
            )
            cursor = conn.cursor(dictionary=True)
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return

        # 3. Improved dimension table handling
        def process_dimension_table(table_name, id_col, values):
            """Batch process dimension records with verification"""
            try:
                placeholders = ', '.join(['%s'] * len(values))
                cursor.execute(
                    f"SELECT {id_col} FROM {table_name} WHERE {id_col} IN ({placeholders})",
                    tuple(values)
                )
                existing_ids = {row[id_col] for row in cursor.fetchall()}

                # Insert new records
                new_records = [v for v in values if v not in existing_ids]
                if new_records:
                    values_str = ', '.join(['(%s)'] * len(new_records))
                    insert_query = f"INSERT INTO {table_name} ({id_col}) VALUES {values_str}"
                    cursor.execute(insert_query, tuple(new_records))
                    conn.commit()

                return len(new_records)

            except Exception as e:
                conn.rollback()
                logger.error(f"Error processing {table_name}: {e}")
                raise

        # 4. Process dimension tables
        logger.info("Processing dimension tables...")
        try:
            dim_stats = {}

            customer_ids = [int(x) for x in df['Consumer_ID'].unique() if pd.notna(x)]
            dim_stats['customers'] = process_dimension_table("dim_customer", "customer_id", customer_ids)

            driver_ids = [int(x) for x in df['Driver_ID'].unique() if pd.notna(x)]
            dim_stats['drivers'] = process_dimension_table("dim_driver", "driver_id", driver_ids)

            restaurant_ids = [int(x) for x in df['Restaurant_ID'].unique() if pd.notna(x)]
            dim_stats['restaurants'] = process_dimension_table("dim_restaurant", "restaurant_id", restaurant_ids)

            logger.info(f"Dimension records processed: {dim_stats}")

            # 5. Process fact and time records
            logger.info("Processing fact records...")
            conn.start_transaction()

            time_records = []
            fact_records = []

            for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
                try:
                    customer_id = int(row['Consumer_ID'])
                    driver_id = int(row['Driver_ID'])
                    restaurant_id = int(row['Restaurant_ID'])

                    # Prepare time record
                    time_records.append((
                        row['Customer_placed_order_datetime'],
                        row['Placed_order_with_restaurant_datetime'],
                        row['Driver_at_restaurant_datetime'],
                        row['Delivered_to_consumer_datetime']
                    ))

                    # Temporary time_id = len(time_records), will update later
                    fact_records.append((
                        customer_id,
                        driver_id,
                        restaurant_id,
                        len(time_records),
                        bool(row['Is_New']),
                        row['Delivery_Region'],
                        bool(row['Is_ASAP']),
                        float(row['Order_total']),
                        float(row['Amount_of_discount']) if pd.notna(row['Amount_of_discount']) else 0.0,
                        float(row['Amount_of_tip']) if pd.notna(row['Amount_of_tip']) else 0.0,
                        float(row['Refunded_amount']) if pd.notna(row['Refunded_amount']) else 0.0
                    ))

                except Exception as e:
                    logger.warning(f"Skipping row due to error: {e}")
                    continue

            # Insert time records
            time_ids = []
            if time_records:
                cursor.executemany("""
                    INSERT INTO dim_time (
                        order_datetime, placed_datetime,
                        driver_arrival_datetime, delivery_datetime
                    ) VALUES (%s, %s, %s, %s)
                """, time_records)
                cursor.execute("SELECT LAST_INSERT_ID() as first_id")
                first_id = cursor.fetchone()['first_id']
                time_ids = list(range(first_id, first_id + len(time_records)))

            # Assign actual time_id to fact records
            for i, fact in enumerate(fact_records):
                fact_records[i] = fact[:3] + (time_ids[i],) + fact[4:]

            # Insert fact records
            if fact_records:
                cursor.executemany("""
                    INSERT INTO fact_orders (
                        customer_id, driver_id, restaurant_id, time_id,
                        is_new, delivery_region, is_asap,
                        order_total, discount, tip, refund
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, fact_records)

            conn.commit()
            logger.info(f"Data loading complete! Success: {len(fact_records)} records")

        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction failed: {e}")
            raise
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        logger.error(f"ETL process failed: {e}")
        raise

if __name__ == "__main__":
    main()
