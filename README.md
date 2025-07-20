<h1>Data Warehouse: A Food Delivery Analysis</h1>

<h2>Introduction</h2>

<p>This project focuses on analyzing and modeling food delivery operations using
transactional and behavioral data from a restaurant delivery platform. The dataset includes
detailed timestamps, customer information, restaurant interactions, delivery regions, and
payment transactions. By organizing this data into a dimensional model, we aim to support
efficient business intelligence reporting, performance monitoring, and operational decision-
making.
  
Our goal is to design a comprehensive data warehouse that enables deeper insights into
the customer journey—from placing an order to final delivery—as well as restaurant
performance and driver efficiency across regions.</p>

<h2>Objectives</h2>

<ul>
  <li>To develop a robust dimensional data model using the Kimball methodology that
supports multiple business processes.
  </li>
</ul>

<ul>
  <li>To design a Bus Matrix that clearly defines fact and dimension tables supporting use
cases such as:
    <ul>
      <li>Order placement and payment tracking</li>
      <li>Delivery efficiency and driver logistics</li>
      <li>Customer engagement and loyalty behavior</li>
      <li>Restaurant operational performance</li>
      <li>Regional analysis of delivery demand and timing</li>
    </ul>
  </li>
</ul>

<h2>Business Value</h2>

<p>This project empowers stakeholders with:</p>

<ul>
  <li><strong>Customer Insights:</strong>Understand ordering behavior, identify loyal customers, and measure retention efforts.</li>
  <li><strong>Operational Optimization:</strong>Analyze delivery performance and time splits to reduce delivery delays and improve customer satisfaction.</li>
  <li><strong>Restaurant Management:</strong>Track restaurant throughput, cancellation rates, and peak order times to optimize staffing and inventory.</li>
  <li><strong>Driver Efficieny:</strong>Monitor delivery times by driver and region to improve routing and resource allocation.</li>
  <li><strong>Strategic Planning:</strong>Support marketing and operations teams with data-driven decisions for promotions, discounts, and geographic expansion.</li>
</ul>

<h2>Data Overview</h2>
<h3>Source Data Description</h3>
<p>The dataset consists of transactional and operational data related to a food delivery platform, including:</p>
<ul>
  <li><strong>Orders:</strong>Order IDs, timestamps, order totals, discounts, tips, refund amounts, and ASAP vs. scheduled flags.</li>
  <li><strong>Customers:</strong>Customer IDs, demographics, loyalty status, total orders, and total spend.</li>
  <li><strong>Restaurants:</strong>Restaurant IDs, performance metrics such as order volume, delivery times, and cancellations.</li>
  <li><strong>Payments:</strong>Payment amounts, discounts, tips, and refund details.</li>
  <li><strong>Deliveries:</strong>Delivery IDs, timestamps for key delivery events, driver assignment, and total delivery duration.</li>
  <li><strong>Drivers:</strong>Driver IDs, associated delivery records, and delivery performance.</li>
  <li><strong>Regions/Locations:</strong>Delivery regions associated with orders, allowing geographic performance analysis.</li>
  <li><strong>Order Types:</strong>Classification of orders as ASAP or Scheduled for fulfillment timing analysis.</li>
</ul>

<h3>Data Profiling Insights</h3>
<ul>
  <li>Missing values were identified in specific columns (e.g., some refund amounts and
timestamps).</li>
  <li>The is_asap column was reviewed to distinguish between scheduled and ASAP orders.</li>
  <li>Date and time fields were converted into standard formats for consistency across datasets.</li>
  <li>Duplicates were minimal and handled during the ETL stage.</li>
  <li>Key dimensions (such as customer, restaurant, and driver) were checked for unique
identifiers to ensure referential integrity in fact table joins.</li>
  <li>Categorical fields (e.g., loyalty status, order type) were standardized for analysis and
visualization.</li>
</ul>

<h3>Challenges and Assumptions</h3>
<ul>
  <li><strong>Incomplete or inconsistent data:</strong> Some columns (like delivery times, refunded amounts, or driver timestamps) may have missing or inconsistent values, impacting accuracy in analytics.</li>
  <li><strong>Ambiguity in certain fields:</strong> Fields like is_ASAP required assumptions due to a lack of a clear order_type column.</li>
  <li><strong>Data normalization needs:</strong> Fields like locations and time formats required
transformation or standardization before modeling.</li>
  <li><strong>ETL Complexity:</strong> Ensuring consistent keys and grain across multiple fact tables and aligning with dimensional tables added complexity.</li>
  <li><strong>Performance optimization:</strong> As data volume grows, query speed and dashboard
performance may require further tuning.</li>
  <li><strong>Surrogate key generation:</strong> Needed for all dimension tables and fact relationships, requiring consistent ETL logic.</li>
</ul>

<h2>Dimensional Modeling</h2>
<h3>Bus Matrix</h3>

<h3>Tables used for Detailed Star Schema</h3>

<h3>Star Schema Example</h3>

<h3>Naming Conventions and Standards</h3>
<ul>
  <li>Table naming:
    <ul>
      <li>Prefix all fact tables with fact_ (e.g., fact_orders)</li>
      <li>Prefix all dimension tables with dim_ (e.g., dim_customer)</li>
    </ul>
  </li>
</ul>

<ul>
  <li>Column naming:
    <ul>
      <li>Use camelCase for all column names (e.g., orderId, customerKey)</li>
      <li>Surrogate keys end with Key (e.g., customerKey, regionKey)</li>
      <li>Business keys match source naming or follow logical descriptions (e.g.,
customerId, orderTotal)</li>
    </ul>
  </li>
</ul>

<ul>
  <li>Key and Relationships:
    <ul>
      <li>Surrogate keys used as primary keys in dimension tables</li>
      <li>Foreign keys in fact tables always reference the surrogate keys from dimension
tables</li>
      <li>All foreign keys are named consistently as dimensionNameKey (e.g.,
paymentKey, driverKey)</li>
    </ul>
  </li>
</ul>

<h2>Data Warehouse Implementation</h2>
<h3>Technical Architectire</h3>
<ul>
  <li>Data Source: A CSV file named data.csv, which contains order-related data.</li>
  <li>ETL Script: A Python script that extracts data from the CSV, transforms it (cleans,
parses datetime, checks for missing data), and loads it into a MySQL-based data
warehouse.</li>
  <li>Target Data Warehouse: MySQL database (food_delivery_dw) containing dimension
and fact tables (dim_customer, dim_driver, dim_restaurant, dim_time, fact_orders).</li>
  <li>Libraries Used: pandas for data handling, numpy for NaN handling, datetime for
timestamp conversion, mysql.connector for DB interaction, tqdm for progress bars, and
logging for structured log output.</li>
</ul>

<h3>Data Pipeline Design (ETL/ELT)</h3>
<ul>
  <li><strong>Extract:</strong>
    <ul>
      <li>The script reads in data from data.csv.</li>
      <li>Required columns are validated to ensure schema integrity.</li>
      <li>Missing values are replaced with None.</li>
    </ul>
  </li>
</ul>

<ul>
  <li><strong>Transform:</strong>
    <ul>
      <li>Datetime fields are parsed from custom 'DD HH:MM:SS' format to full datetime
objects</li>
      <li>Rows with critical missing datetime values are dropped.</li>
      <li>Data is type-cast (e.g., converting ID fields to integers, floats for monetary
amounts).</li>
      <li>Duplicates are avoided in dimensions by checking which IDs already exist in the
database.</li>
    </ul>
  </li>
</ul>

<ul>
  <li><strong>Load:</strong>
    <ul>
      <li>Connects to MySQL and inserts unique values into dim_customer, dim_driver,
and dim_restaurant.</li>
      <li>Inserts detailed datetime breakdowns into dim_time.</li>
      <li>Inserts transactional data (e.g., order total, tip, refund) into fact_orders, linking to all relevant dimension tables.</li>
    </ul>
  </li>
</ul>

<h2>Code</h2>


<h2>Business Intelligence Implementation</h2>
<h3>Dashboard Overview</h3>
<p>The BI dashboard was created using Power BI. The primary purpose of the dashboard is to
provide interactive and intuitive visualizations that allow stakeholders to monitor and analyze
various aspects of the food delivery operations, including order trends, delivery efficiency,
customer behavior, and restaurant performance.</p>

<p align="center">
  <img src="https://github.com/nikkishimao/FoodDeliveryAnalysis/blob/ca240f9495549bffe0f7bb05a934319b2c071a53/images/PowerBIDash.png" width="850" />
</p>

<h3>Star Schema (from PowerBI)</h3>
<p align="center">
  <img src="https://github.com/nikkishimao/FoodDeliveryAnalysis/blob/ca240f9495549bffe0f7bb05a934319b2c071a53/images/PowerBIStar.png" width="850" />
</p>

<h3>Key Features</h3>
<ul>
  <li><strong>Order Trends:</strong>
    <ul>
      <li>Visualizing metrics like order totals, total revenue, average tip, refund rate, orders
over time, tip analysis, and other comparisons like ASAP vs Scheduled orders.</li>
      <li>Ability to drill down into different regions or specific time periods.</li>
    </ul>
  </li>
</ul>

<ul>
  <li><strong>Customer Engagement:</strong>
    <ul>
      <li>Analyzing customer loyalty and spending behavior, highlighting frequent
customers, total orders, and lifetime value.</li>
      <li>Filters for viewing engagement patterns across different order types.</li>
    </ul>
  </li>
</ul>

<ul>
  <li><strong>Delivery Efficieny:</strong>
    <ul>
      <li>Visualization of delivery performance across different regions and drivers.</li>
    </ul>
  </li>
</ul>

<ul>
  <li><strong>Restaurant Performance:</strong>
    <ul>
      <li>Metrics to track restaurant performance, including tip analysis, average tip, and
refund rate.</li>
    </ul>
  </li>
</ul>

<h2>Challenges and Solutions</h2>
<h2>Challenges</h2>
<ul>
  <li><strong>Data Quality Issues:</strong>
    <ul>
      <li>Missing or inconsistent values in the dataset, especially in key columns like
delivery times or payment amounts.</li>
      <li>Ambiguous fields that required assumptions, such as is_ASAP due to missing
order type definitions.</li>
    </ul>
  </li>
</ul>

<ul>
  <li><strong>ETL Complexity:</strong>
    <ul>
      <li>Ensuring that the extraction, transformation, and loading (ETL) processes are
smooth, particularly when dealing with large data volumes and multiple fact
tables.</li>
      <li>Handling the generation of surrogate keys and foreign key relationships across
various fact tables and dimension tables.</li>
    </ul>
  </li>
</ul>

<ul>
  <li><strong>Modeling Complexity:</strong>
    <ul>
      <li>Designing the star schemas to ensure clarity, flexibility, and scalability while
avoiding overly complex relationships between fact and dimension tables.</li>
      <li>Deciding on the granularity of each fact table to balance performance and data
completeness.</li>
    </ul>
  </li>
</ul>

<h2>Solutions</h2>
<ul>
  <li><strong>Data Quality Solutions:</strong>
    <ul>
      <li>Implemented data profiling and data cleaning steps in the ETL pipeline to handle
missing values and outliers.</li>
      <li>Assumptions were documented for fields that lacked clear definitions (e.g.,
handling the is_ASAP field by using order timestamps).</li>
    </ul>
  </li>
</ul>

<ul>
  <li><strong>ETl Optimization Solutions:</strong>
    <ul>
      <li>Used Python and SQL to automate the ETL pipeline and ensure consistent data
transformations across fact and dimension tables.</li>
      <li>Designed the ETL process to handle incremental data loads, ensuring that only
new or changed data was loaded into the data warehouse.</li>
    </ul>
  </li>
</ul>

<ul>
  <li><strong>Modeling Complexity Solutions:</strong>
    <ul>
      <li>Focused on clearly defining the business processes and ensuring that fact tables
were designed around them with appropriate measures.</li>
      <li>Utilized conformed dimensions across fact tables to ensure consistency and
flexibility when querying data.</li>
      <li>Applied the Kimball methodology to maintain simplicity and reduce unnecessary
complexity in the star schema</li>
    </ul>
  </li>
</ul>

<h2>Next Steps</h2>
<ul>
  <li><strong>Enhanced Data Collection:</strong>
    <ul>
      <li>The future version of this system could include more granular data about the
customer experience, such as customer ratings or feedback on deliveries, to gain
further insights into customer satisfaction.</li>
      <li>Incorporating additional data sources like weather conditions or special events
could improve delivery time predictions and demand forecasting.</li>
    </ul>
  </li>
</ul>

<ul>
  <li><strong>Predictive Analytics:</strong>
    <ul>
      <li>Implementing machine learning models to predict delivery times, customer
behavior, and restaurant performance would provide even more valuable insights.</li>
    </ul>
  </li>
</ul>

<ul>
  <li><strong>Expanded Business Intelligence Capabilities:</strong>
    <ul>
      <li>Additional dashboards could be created to support other business functions, such
as marketing (e.g., promotions, discounts, campaigns) or financial analysis (e.g.,
profitability, cost per delivery).</li>
    </ul>
  </li>
</ul>

<ul>
  <li><strong>Mobile Dashboard Access:</strong>
    <ul>
      <li>As part of future development, making the dashboard mobile-friendly would
allow restaurant managers, delivery drivers, and business analysts to access key
insights on the go.</li>
      <li>Mobile access would be particularly useful for drivers and restaurant managers to
track real-time delivery performance and customer trends.</li>
    </ul>
  </li>
</ul>
