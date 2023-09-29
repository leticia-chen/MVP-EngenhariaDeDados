from google.cloud import storage
import os

def upload_files(request):
    storage_client = storage.Client()
    bucket = storage_client.bucket('your_bucket_name')

    local_directory_path = '/tmp/local_folder'

    for filename in os.listdir(local_directory_path):
        if filename.endswith('.csv'):
            local_file_path = os.path.join(local_directory_path, filename)
            blob_name = os.path.join('gcp_folder', filename)
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(local_file_path)

    return 'Files uploaded', 200