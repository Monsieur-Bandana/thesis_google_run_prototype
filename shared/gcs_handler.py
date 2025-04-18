"""
provides helper function for communicating with google cloud storage
"""

from google.cloud import storage
import os

# from classifier import exec_file
from google.cloud import storage

print("Current working directory:", os.getcwd())


def list_directories_in_bucket(bucket_name, prefix=None):
    """
    List directories in a Google Cloud Storage bucket.

    Args:
        bucket_name (str): Name of the GCS bucket.
        prefix (str): (Optional) Prefix to filter objects by directory.

    Returns:
        List[str]: A list of directory names.
    """

    client = storage.Client()

    bucket = client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix)

    directories = []

    for blob in blobs:

        path_parts = blob.name.split("/")
        if path_parts[1] not in directories and not path_parts[1] == "":
            directories.append(path_parts[1])

    dir: list[str] = directories
    return dir


def list_files_in_bucket(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()  # List all files in the bucket
    return [blob.name for blob in blobs]


def list_files_in_folder(bucket_name, folder_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    if not folder_name.endswith("/"):
        folder_name += "/"

    blobs = bucket.list_blobs(prefix=folder_name)
    return [blob.name for blob in blobs if not blob.name.endswith("/")]


def upload_file(bucket_name, source_file_name, destination_blob_name, folder_name=None):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    if folder_name:
        if not folder_name.endswith("/"):
            folder_name += "/"
        destination_blob_name = folder_name + destination_blob_name

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def download_file_from_bucket(
    bucket_name, source_blob_name, destination_file_name, folder_name: str = None
):
    """
    checks if file is already downloaded, if not loads from google cloud strorage
    """
    if os.path.isfile(destination_file_name):
        print(f"{destination_file_name} found in temp folder")
        return
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    try:
        if folder_name:
            if not folder_name.endswith("/"):
                folder_name += "/"
            source_blob_name = folder_name + source_blob_name

        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print(f"Downloaded {source_blob_name} to {destination_file_name}")
    except:
        print("no file in bucket, going on")


def create_temp_folder(parentf):
    folder_path = f"{parentf}/temp"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")
