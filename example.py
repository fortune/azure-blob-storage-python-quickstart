import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
from azure.storage.blob.models import Include

# ---------------------------------------------------------------------------------------------------------
# Method that creates a test file in the current folder.
# This sample application creates a test file, uploads the test file to the Blob storage,
# lists the blobs in the container, and downloads the file with a new name.
# ---------------------------------------------------------------------------------------------------------
# Documentation References:
# Associated Article - https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
# What is a Storage Account - http://azure.microsoft.com/en-us/documentation/articles/storage-whatis-account/
# Getting Started with Blobs-https://docs.microsoft.com/en-us/azure/storage/blobs/storage-python-how-to-use-blob-storage
# Blob Service Concepts - http://msdn.microsoft.com/en-us/library/dd179376.aspx
# Blob Service REST API - http://msdn.microsoft.com/en-us/library/dd135733.aspx
# ----------------------------------------------------------------------------------------------------------

#
# アカウント名、アカウントキー、作業対象となるコンテナ名を引数に指定する。
#


def run_sample(account_name, account_key, container_name):
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(
            account_name=account_name,
            account_key=account_key)

        # Create a container
        # すでに存在していた場合は何も起こらない。
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

        # Create a file in the current folder to test the upload and download.
        #local_path=os.path.expanduser("~/Documents")
        local_path=os.getcwd()
        local_file_name ="QuickStart_" + str(uuid.uuid4()) + ".txt"
        full_path_to_file =os.path.join(local_path, local_file_name)

        # Write text to the file.
        file = open(full_path_to_file,  'w')
        file.write("Hello, World!")
        file.close()

        print("Temp file = " + full_path_to_file)
        print("\nUploading to Blob storage as blob " + local_file_name)

        # アップロードする Blob に付随させるメタデータ
        # value に空白文字を含めることはできるが、key に空白文字を含めると、アップロード用メソッドを実行したときエラーになる。
        # ポータル上で Blob のメタ情報を編集する場合も同じ。
        metadata = {'one': 'first first', 'two': 'second', 'three': 'third'}

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file, metadata=metadata)

        # List the blobs in the container
        # Blob のメタ情報は、デフォルトでは取得されないので、include キーワード引数で指定してやる必要がある。
        print("\nList blobs in the container")
        generator = block_blob_service.list_blobs(container_name, include=Include.METADATA)
        for blob in generator:
            # blob は、azure.storage.blob.models.Blob オブジェクトである。
            # blob.properties は、azure.storage.blob.models.BlobProperties オブジェクトである。
            print("\t Blob name: " + blob.name)
            print("\t Blob type: " + blob.properties.blob_type)
            print("\t Blob content length: " + str(blob.properties.content_length))
            print("\t Last modified: " + str(blob.properties.last_modified))

            # list_blobs メソッドの include キーワード引数を指定しなかったなら、メタ情報を取得するのに改めて
            # get_blob_metadata メソッドを呼び出す必要がある。
            # metadata = block_blob_service.get_blob_metadata(container_name, blob.name)
            metadata = blob.metadata
            if metadata:
                print("\t Metadata:")
                for key, value in metadata.items():
                    print("\t\t key = " + key + ", value = " + value)
            print()

        # Download the blob(s).
        # Add '_DOWNLOADED' as prefix to '.txt' so you can see both files in the current folder.
        full_path_to_file2 = os.path.join(local_path, str.replace(local_file_name ,'.txt', '_DOWNLOADED.txt'))
        print("\nDownloading blob to " + full_path_to_file2)
        block_blob_service.get_blob_to_path(container_name, local_file_name, full_path_to_file2)

        sys.stdout.write("Sample finished running. When you hit <any key>, the sample will be deleted and the sample "
                         "application will exit.")
        sys.stdout.flush()
        input()

        # Clean up resources. This includes the uploaded blob and the temp files but not the container for safety.
        #block_blob_service.delete_container(container_name)
        block_blob_service.delete_blob(container_name, local_file_name)
        os.remove(full_path_to_file)
        os.remove(full_path_to_file2)
    except Exception as e:
        print(e)


# Main method.
if __name__ == '__main__':
    account_name = sys.argv[1]
    account_key = sys.argv[2]
    container_name = sys.argv[3]

    run_sample(account_name, account_key, container_name)
