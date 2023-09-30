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

    # Initialize PySpark session with BigQuery connector
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

    # # Transformation and create trend_analysis table 
    trend_analysis = transformation_trendAnalysis(df_items, df_orders)

    # # Transformation and create sales_performance table
    sales_performance = transformation_salesPerformance(df_items, df_products, df_sellers)

    # Write to sink
    writeToBucket(trend_analysis, "overwrite")
    writeToBigQuery(trend_analysis, "e_commerce", "trend_analysis")

    writeToBucket(sales_performance, "overwrite")
    writeToBigQuery(sales_performance, "e_commerce", "sales_performance")



if __name__ == "__main__":
    etl_pipeline()

    