## Dataset
<a href="https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce">Brazilian E-Commerce Public Dataset by Olist</a>

## Introduction
This project was conceived as part of my postgraduate course in Data Engineering at PUC-Rio, focusing on three main pillars: databases, data warehouses and data lakes, and data management and governance. It represents a unique opportunity to apply the theoretical concepts learned in a practical setting, using real data from the Brazilian e-commerce market. I chose to focus on the e-commerce sector not only due to its relevance and explosive growth in recent years, but also because the data is readily available and does not present confidentiality issues. In addition to providing a platform to enhance my skills in data manipulation and analysis, this project also allows me to explore some of the emerging trends in data science and big data, including automation, cloud computing, and specific tools from GCP (Google Cloud Platform).
## Goal
The main objective of this project is to use data from Brazil's largest e-commerce platform, Olist, which were obtained through the Kaggle platform, to perform trend and sales performance analyses. Due to resource limitations (using the trial version of GCP), our scope of analysis will focus on:

1. Sales trend analysis, including sales volume, revenue, and shipping costs.
2. Sales performance analysis, including seller ratings and product category performance.
3. Customer reactions to delivery time.

**Problem Statement**
This project will answer the following business questions:

1. What is the sales performance for the year 2018?
2. Which product categories are performing the best in terms of order volume and revenue?
3. How do customers react to delivery time? Is this related to customer satisfaction?
   
Due to the resource limitations of GCP and limited time, the current analysis is primarily based on questions that can be answered with the available resources. The results of the analysis will be stored in the GCP Bucket (Data Lake) and BigQuery (Data Warehouse).
## Data Modeling for E-commerce Analysis
In this e-commerce analysis project, we opted to use the Star Schema as the structure for our data modeling.

**Fact Table**
Order Items Fact Table:

This fact table is based on the olist_order_items_dataset.csv file, which contains multiple attributes of order items, such as Order ID, Product ID, price, and quantity, etc.

**Dimension Tables**
* Order Dimension: Contains data from the olist_orders_dataset.csv file, such as order date, order status, etc.
* Product Dimension: Contains data from the olist_products_dataset.csv and product_category_name_translation.csv files, such as product name, category, etc.
* Customer Dimension: Contains data from the olist_customers_dataset.csv file, such as customer name, address, etc.
* Seller Dimension: Contains data from the olist_sellers_dataset.csv file, such as seller name, address, etc.
* Review Dimension: Contains data from the olist_order_reviews_dataset.csv file, such as review score, review text, etc.
* Payment Dimension: Contains data from the olist_order_payments_dataset.csv file, such as payment type, payment value, etc.
* Geolocation Dimension: Contains data from the olist_geolocation_dataset.csv file, such as postal code, latitude, and longitude, etc.
  
These dimension tables are connected to our single fact table through foreign keys, forming a star schema.

Following is a structured model built using the Star Schema; this type of model is used for Business Intelligence applications. It consists of a central fact table (Fact Table -> List order_items) and one or more dimension tables (Dimension Tables). Through this model, it will be easier to quickly understand the relationships between each table.

<img src="Images/eCommerce_diagram.jpeg">

### Development and Testing on GCP's Dataproc via Jupyter Notebook
Prior to the final deployment of the ETL pipeline and execution of SQL queries, all developmental stages and tests were carried out within the Jupyter Notebook environment facilitated by Google Cloud Platform (GCP), utilizing PySpark. This initial phase ensures both the practicality and efficacy of the data transformation procedures, query operations, and other integral components of the data pipeline.

<a href="Dvelopment Stage/mvp_etl_query_develop.ipynb">Pre-Implementation: Development and Testing in Jupyter Notebook via GCP Dataproc</a>
## Data Loading
Firstly, I imported all the CSV data files into a Bucket on the GCP (Google Cloud Platform), serving as our Data Lake.
### How to upload dataset files via local computer terminal
Step by step:

>**1st, Create a 'key' in GCP IAM & Admin:**
>
>Please refer to the <a href="MVP_SprintIII_project_presentation_portuques.ipynb"> MVP_SprintIII_project_presentation_portuques.ipynb</a> file for more detailed steps.

>**2nd, Prepare Python script: upload_files.py**
>
>For your reference:<a href="upload_files.py"> upload_files.py</a>

>**3rd, Upload Python script in the terminal**
>```
>pip3 install google-cloud-storage
>export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
>python3 upload_files.py
>```
>**4th, Insert the created "Service Account" into the 'Principal' of the bucket**
>```
>Acesse bucket
>Click PERMISSIONS->GRANT ACCESS ->
>Add 'service account' para Principals->
>Assign roles: select Cloud storage->storage object creator
>```
```
(base) leticia@ChendeMacBook-Air Desktop % python3 upload_files.py
/Users/leticia/Downloads/Brasilian_ecommerce_dataset/olist_sellers_dataset.csvhasbeenuploadedtoe_commerce/olist_sellers_dataset.csv.
/Users/leticia/Downloads/Brasilian_ecommerce_dataset/olist_orders_dataset.csvhasbeenuploadedtoe_commerce/olist_orders_dataset.csv.
/Users/leticia/Downloads/Brasilian_ecommerce_dataset/olist_order_items_dataset.csvhas been uploaded to e_commerce/list_order_items_dataset.csv.
/Users/leticia/Downloads/Brasilian_ecommerce_dataset/olist_products_dataset.csvhasbeenuploadedtoe_commerce/olist_products_dataset.csv.
(base) leticia@ChendeMacBook-Air Desktop %
```
<img src="Images/dataset_in_bucket.png">

## Create Cluster in GCP Dataproc
Please refer to the <a href="MVP_SprintIII_project_presentation_portuques.ipynb"> MVP_SprintIII_project_presentation_portuques.ipynb -> 'Criar Cluster no GCP Dataproc'</a> file for more detailed steps.

## Data Analysis
Before extracting data from the Data Lake (GCS) and importing it into our data warehouse (BigQuery), a series of cleaning and pre-processing tasks need to be performed to ensure data consistency and accuracy. 

In a PySpark environment, use df.printSchema() to check if the data types are correct. Below is the result of checking one of the datasets.
```
# Schema do olist_order_items_dataset.csv
root
 |-- order_id: string (nullable = false)
 |-- order_item_id: string (nullable = false)
 |-- product_id: string (nullable = false)
 |-- seller_id: string (nullable = false)
 |-- shipping_limit_date: string (nullable = false)
 |-- price: string (nullable = false)
 |-- freight_value: string (nullable = false)
```
<img src="Images/order_item_dataset.png">
Based on the schema information, it is observed that some data types of the columns are incorrect after reading, so it is necessary to address this during the transformation stage. In addition, missing data parts will be filled with 'null'. Additionally, since the project does not involve machine learning at this stage, 'one-hot encoding' will not be applied.

Due to the fact that each data file may contain more than 112,650 rows, it was decided to keep only the necessary attributes (columns) when creating new tables for query analysis.

>**In response to the first question - Create the trend_analysis table**
   
>The purpose of creating the trend_analysis table is to understand the dynamics of the business over time. This table is the result of a join operation between
>
>* olist_order_items_dataset.csv and
>* olist_orders_dataset.csv
>  
>Through this table, we can perform various time-series analyses, including but not limited to, quarterly sales reports and annual revenue growth.
>
>The columns included in this table, such as sales_quantity, revenue, freight_cost, and order_approved_at, have been carefully selected. Specifically, the order_approved_at timestamp allows us to deepen our understanding of how to improve sales strategies within specific time periods.

>**In response to the second question - Create the sales_performance table**
>
>The purpose of creating the sales_performance table is to provide a comprehensive view for assessing the sales performance of different product categories and sellers. This table is the result of a join operation between
>* olist_order_items_dataset.csv,
>* olist_products_dataset.csv, and
>* olist_sellers_dataset.csv.
>Through this table, we can perform multi-dimensional sales analyses, such as which product categories are most popular, which sellers have the best sales performance, or in which regions there are more orders.

>The selected columns like order_id, product_id, seller_id, product_category_name, price, shipping_limit_date, and seller_state have specific purposes. For example, seller_state is used for geographical location analyses, which is very useful for understanding which regions have more active sellers or buyers.

>**In response to the third question - Create the Average Delivery Time Analysis by State table**
>
>The purpose of creating this table is to understand the impact of delivery time on customer satisfaction. The table is generated from a join between
>* olist_orders_dataset.csv and
>* olist_order_reviews_dataset.csv
>This table allows us to analyze how different delivery times affect customer reviews, which is crucial for optimizing logistics and increasing customer satisfaction.

>The columns retained after the join include order_id, order_purchase_date, order_delivered_customer_date, and review_score. These fields are essential for calculating the average delivery time and correlating it with the customer review score. Through this table, we can perform queries that help us better understand how to optimize our delivery time to improve customer experience.

## ETL Pipeline Development and Submitting it as a Dataproc Job
In the implementation of the ETL, two approaches were adopted. The first involves writing the ETL as a Python script, submitting it as a job, and then creating a workflow and cloud scheduler for automatic execution (creating the first and second table). The second approach uses Dataprep to create the ETL in a visual environment (generating the third table).
### Method 1: Write the ETL pipeline in a Python script and then submit it as a job, followed by combining the use of workflow and Cloud Scheduler to achieve automation.
Below is the ETL pipeline developed in Python script:
```
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, FloatType, TimestampType
from pyspark.sql.functions import col, year, month
from pyspark.sql import functions as F


BUCKET_PATH = "gs://mvp-pyspark/Brasilian_ecommerce_dataset/"


# Transform to create trend_analysis table
def transformation_trendAnalysis(df_items, df_orders):

    # Remove duplicate order_ids
    df_items = df_items.dropDuplicates(['order_id'])
    df_orders = df_orders.dropDuplicates(['order_id'])
    
    transform_join = df_items.join(df_orders, df_items.order_id == df_orders.order_id, "inner") \
                            .select(
                            [
                                df_items.order_id.alias("sales_quantity"),
                                df_items.price.alias("revenue"),
                                df_items.freight_value.alias("freight_cost"),
                                df_orders.order_approved_at
                            ]
    )

    # Casting columns to their appropriate data types
    transformWithColumn = (transform_join
                      .withColumn("revenue", col("revenue").cast(FloatType()))
                      .withColumn("freight_cost", col("freight_cost").cast(FloatType()))
                      .withColumn("order_approved_at", col("order_approved_at").cast(TimestampType()))
                     )

    # Adding 'month_year' for monthly analysis  
    trend_analysis_pre = (transformWithColumn
                      .withColumn("month_year", F.trunc("order_approved_at", "MM"))
                     )

    return trend_analysis_pre


# Transfom to create sales_performance table
def transformation_salesPerformance(df_items, df_products, df_sellers):

    df1 = df_items.join(df_products, df_items.product_id == df_products.product_id, "inner") \
            .select(
            [
                df_items.order_id,
                df_items.product_id,
                df_items.seller_id,
                df_products.product_category_name,
                df_items.price,
                df_items.shipping_limit_date
            ]
    )

    df2 = df1.join(df_sellers, df1.seller_id == df_sellers.seller_id, "inner") \
                    .select(
                    [
                        df1.order_id,
                        df1.product_id,
                        df1.seller_id,
                        df1.product_category_name,
                        df1.price,
                        df1.shipping_limit_date,
                        df_sellers.seller_state
                    ]
    )

  # Casting columns to their appropriate data types
    sales_performance_pre = (df2
                  .withColumn("price", col("price").cast("Float"))
                  .withColumn("shipping_limit_date", col("shipping_limit_date").cast(TimestampType()))

                 )

    return sales_performance_pre


# Write to sink (Data Lake)
def writeToBucket(df, mode):
    df.write.mode(mode).parquet("gs://mvp-pyspark/e_commerce/")


# Write to sink (Data Warehouse)
def writeToBigQuery(df, schema, file_name):
    df.write.format('bigquery').mode("overwrite") \
        .option('table', f"{schema}.{file_name}") \
        .option('temporaryGcsBucket', f"mvp-pyspark/tmp_staging") \
        .save()


def etl_pipeline():

    spark = SparkSession.builder.appName("pyspark-mvp") \
            .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar") \
            .getOrCreate()

    # Extract datas
    df_items = spark.read.csv("gs://mvp-pyspark/Brasilian_ecommerce_dataset/olist_order_items_dataset.csv", header=True)
    df_orders = spark.read.csv("gs://mvp-pyspark/Brasilian_ecommerce_dataset/olist_orders_dataset.csv", header=True)
    df_sellers = spark.read.csv("gs://mvp-pyspark/Brasilian_ecommerce_dataset/olist_sellers_dataset.csv", header=True)
    df_products = spark.read.csv("gs://mvp-pyspark/Brasilian_ecommerce_dataset/olist_products_dataset.csv", header=True)

    # Transformation, fill missing values
    df_items = df_items.fillna('null')
    df_orders = df_orders.fillna('null')
    df_sellers = df_sellers.fillna('null')
    df_products = df_products.fillna('null')

    # Transformation and create trend_analysis table
    trend_analysis = transformation_trendAnalysis(df_items, df_orders)

    # Transformation and create sales_performance table
    sales_performance = transformation_salesPerformance(df_items, df_products, df_sellers)

    # Write to sink
    writeToBucket(trend_analysis, "overwrite")
    writeToBigQuery(trend_analysis, "e_commerce", "trend_analysis")

    writeToBucket(sales_performance, "overwrite")
    writeToBigQuery(sales_performance, "e_commerce", "sales_performance")



if __name__ == "__main__":
    etl_pipeline()
```










