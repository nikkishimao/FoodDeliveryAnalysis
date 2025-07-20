CREATE DATABASE food_delivery_dw;
USE food_delivery_dw;

-- Drop existing tables if any
DROP TABLE IF EXISTS fact_orders;

DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_restaurant;
DROP TABLE IF EXISTS dim_driver;
DROP TABLE IF EXISTS dim_date;

DROP TABLE IF EXISTS staging_orders;

-- Step 2: Drop and Create Staging Table
DROP TABLE IF EXISTS staging_orders;
CREATE TABLE staging_orders (
    Customer_placed_order_datetime VARCHAR(50),
    Placed_order_with_restaurant_datetime VARCHAR(50),
    Driver_at_restaurant_datetime VARCHAR(50),
    Delivered_to_consumer_datetime VARCHAR(50),
    Driver_ID INT,
    Restaurant_ID INT,
    Consumer_ID INT,
    Is_New BOOLEAN,
    Delivery_Region VARCHAR(100),
    Is_ASAP BOOLEAN,
    Order_total FLOAT,
    Amount_of_discount FLOAT,
    Amount_of_tip FLOAT,
    Refunded_amount FLOAT
);

-- Step 3: Drop and Create Dimension Tables

-- Customer Dimension
DROP TABLE IF EXISTS dim_customer;
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    is_new BOOLEAN,
    delivery_region VARCHAR(100)
);

-- Restaurant Dimension
DROP TABLE IF EXISTS dim_restaurant;
CREATE TABLE dim_restaurant (
    restaurant_id INT PRIMARY KEY
);

-- Driver Dimension
DROP TABLE IF EXISTS dim_driver;
CREATE TABLE dim_driver (
    driver_id INT PRIMARY KEY
);

-- Date Dimension
DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    weekday VARCHAR(20)
);

-- Step 4: Drop and Create Fact Table
DROP TABLE IF EXISTS fact_orders;
CREATE TABLE fact_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    restaurant_id INT,
    driver_id INT,
    date_id DATE,
    order_total FLOAT,
    discount FLOAT,
    tip FLOAT,
    refunded FLOAT,
    is_asap BOOLEAN,
    delivery_time INT,

    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES dim_restaurant(restaurant_id),
    FOREIGN KEY (driver_id) REFERENCES dim_driver(driver_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- Check how many rows got inserted
SELECT COUNT(*) FROM staging_orders;

-- Preview some data
SELECT * FROM staging_orders LIMIT 10;

-- Star Schema
-- Drop fact table to handle foreign key constraints
DROP TABLE IF EXISTS fact_orders;

-- Drop dimension tables
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_driver;
DROP TABLE IF EXISTS dim_restaurant;
DROP TABLE IF EXISTS dim_time;

-- Dimension: Customer
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY
);

-- Dimension: Driver
CREATE TABLE dim_driver (
    driver_id INT PRIMARY KEY
);

-- Dimension: Restaurant
CREATE TABLE dim_restaurant (
    restaurant_id INT PRIMARY KEY
);

-- Dimension: Time
CREATE TABLE dim_time (
    time_id INT AUTO_INCREMENT PRIMARY KEY,
    order_datetime DATETIME,
    placed_datetime DATETIME,
    driver_arrival_datetime DATETIME,
    delivery_datetime DATETIME
);

-- Fact Table
CREATE TABLE fact_orders (
    fact_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    driver_id INT,
    restaurant_id INT,
    time_id INT,
    is_new BOOLEAN,
    delivery_region VARCHAR(100),
    is_asap BOOLEAN,
    order_total FLOAT,
    discount FLOAT,
    tip FLOAT,
    refund FLOAT,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (driver_id) REFERENCES dim_driver(driver_id),
    FOREIGN KEY (restaurant_id) REFERENCES dim_restaurant(restaurant_id),
    FOREIGN KEY (time_id) REFERENCES dim_time(time_id)
);

SELECT COUNT(*) FROM dim_customer;
SELECT COUNT(*) FROM dim_driver;
SELECT COUNT(*) FROM dim_restaurant;
SELECT COUNT(*) FROM dim_time;
SELECT COUNT(*) FROM fact_orders;
SHOW TABLES;
SHOW ERRORS;
SELECT * FROM dim_customer;
SELECT * FROM dim_driver;
SELECT * FROM dim_restaurant;
SELECT * FROM dim_time;
SELECT * FROM fact_orders;
