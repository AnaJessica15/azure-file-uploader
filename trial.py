# https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-copy?tabs=python



from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__,BlobLeaseClient
import os, uuid

# Create a BlobClient from a connection string
# retrieved from an environment variable named
# AZURE_STORAGE_CONNECTION_STRING.

load_dotenv()


source_blob = BlobServiceClient.from_connection_string(os.environ.get('AZURE_STORAGE_CONNECTION_STRING') , container_name, blob_name)

try:
    # Lease the source blob for the copy operation
    # to prevent another client from modifying it.
    lease = BlobLeaseClient(source_blob)
    lease.acquire()

    # Get the source blob's properties and display the lease state.
    source_props = source_blob.get_blob_properties()
    print("Lease state: " + source_props.lease.state)

    # Create a BlobServiceClient representing the
    # destination blob with a unique name.
    dest_blob = BlobServiceClient.from_connection_string(
       os.environ.get('AZURE_STORAGE_CONNECTION_STRING') , container_name, blob_name)

    # Start the copy operation.
    dest_blob.start_copy_from_url(source_blob.url)

    # Get the destination blob's properties to check the copy status.
    properties = dest_blob.get_blob_properties()
    copy_props = properties.copy

    # Display the copy status.
    print("Copy status: " + copy_props["status"])
    print("Copy progress: " + copy_props["progress"])
    print("Completion time: " + str(copy_props["completion_time"]))
    print("Total bytes: " + str(properties.size))

    if (source_props.lease.state == "leased"):
        # Break the lease on the source blob.
        lease.break_lease()

        # Update the destination blob's properties to check the lease state.
        source_props = source_blob.get_blob_properties()
        print("Lease state: " + source_props.lease.state)

except ResourceNotFoundError as ex:
    print("ResourceNotFoundError: ", ex.message)

except ServiceRequestError as ex:
    print("ServiceRequestError: ", ex.message)
