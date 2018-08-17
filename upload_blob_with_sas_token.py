
import sys
from azure.storage.blob import BlockBlobService



"""
sas token を使用して、ファイルをアップロードし、Blob を作成するサンプル。

使い方：

    python3 upload_blob_with_sas_token.py {アカウント名} {sas_token} {コンテナ名} {Blob 名} {ファイルパス}

    sas_token と、それを生成したときに指定したアカウント名、コンテナ名、Blob 名と、アップロードするローカルなファイルのパスを
    指定する。
"""


def upload_blob_with_sas_token(account_name, sas_token, container_name, blob_name, file_path):
    blob_service = BlockBlobService(account_name=account_name, sas_token=sas_token)
    blob_service.create_blob_from_path(container_name, blob_name, file_path)



# Main method.
if __name__ == '__main__':
    account_name = sys.argv[1]
    sas_token = sys.argv[2]
    container_name = sys.argv[3]
    blob_name = sys.argv[4]
    file_path = sys.argv[5]

    upload_blob_with_sas_token(
        account_name,
        sas_token,
        container_name,
        blob_name,
        file_path,
    )
