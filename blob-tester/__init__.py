import os
from azure.storage.blob import BlobServiceClient
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Retrieve the connection string from environment variables
        connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        if not connection_string:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set")

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

        return func.HttpResponse(f"Blobs in container '{container_name}': {', '.join(blob_names)}")
    except Exception as e:
        return func.HttpResponse(f"Failed to connect to blob storage: {e}", status_code=500)