import os
from os.path import dirname
from typing import List
import pathlib
from azure.storage.blob import BlobClient
from azure.core.exceptions import ResourceExistsError


connect_str = os.getenv('AzureWebJobsStorage')

def main(rootDirectory: str) -> str:
    # Create the BlobServiceClient object which will be used to create a container client
    blob = BlobClient.from_connection_string(conn_str= connect_str, container_name="backups",blob_name=rootDirectory)
    with open("./"+ rootDirectory, "wb") as my_blob:
        stream =  blob.download_blob()
        data =  stream.readall()
        my_blob.write(data)
    return blob.blob_name.upper()
