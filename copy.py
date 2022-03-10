# https://stackoverflow.com/questions/32500935/python-how-to-move-or-copy-azure-blob-from-one-container-to-another

from azure.storage.blob import BlobServiceClient

from dotenv import load_dotenv

load_dotenv()
connection_string   = os.environ.get('AZURE_STORAGE_CONNECTION_STRING') 
account_name   = os.environ.get('account_name') 


# Azure
# Get this from Settings/Access keys in your Storage account on Azure portal
# account_name = "YOUR_AZURE_ACCOUNT_NAME"
# connection_string = "YOUR_AZURE_CONNECTION_STRING"

# Source
source_container_name = "b0aa423d-222e-4f65-86b8-dad29ea19960"
source_file_path = "dac89330-6b87-45e8-b1c3-fd35866dd68e.txt"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
source_blob = (f"https://{account_name}.blob.core.windows.net/{source_container_name}/{source_file_path}")

# Target
target_container_name = "dest-container"
target_file_path = "target.txt"
copied_blob = blob_service_client.get_blob_client(target_container_name, target_file_path)
copied_blob.start_copy_from_url(source_blob)

# If you would like to delete the source file
# remove_blob = blob_service_client.get_blob_client(source_container_name, source_file_path)
# remove_blob.delete_blob()