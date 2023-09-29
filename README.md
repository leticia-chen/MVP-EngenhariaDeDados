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



