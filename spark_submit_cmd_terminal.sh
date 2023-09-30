
gcloud auth login
gcloud config set project [your porject ID]

gcloud dataproc jobs \
submit pyspark /path/to/file/ETL_file_name.py \
--cluster=seu-cluster-name \
--region southamerica-east1 \
--jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.26.0.jar






