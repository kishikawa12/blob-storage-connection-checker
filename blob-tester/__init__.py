import os
from azure.storage.blob import BlobServiceClient
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    try:
        # Retrieve the connection string from environment variables
        connection_string = os.getenv('STORAGE_ACCOUNT_CONNECTION')
        if not connection_string:
            raise ValueError("STORAGE_ACCOUNT_CONNECTION environment variable is not set")

        # Create a BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Retrieve the container name
        container_name = os.getenv('BLOB_STORAGE_PATH')
        if not container_name:
            raise ValueError("BLOB_STORAGE_PATH environment variable is not set")

        # Create a ContainerClient
        container_client = blob_service_client.get_container_client(container_name)

        # List blobs in the container
        blobs_list = container_client.list_blobs()
        blob_names = [blob.name for blob in blobs_list]

        # Log the blob names
        logging.info(f"Blobs in container '{container_name}': {', '.join(blob_names)}")
    except Exception as e:
        logging.error(f"Failed to connect to blob storage: {e}")