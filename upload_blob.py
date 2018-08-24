import sys
from azure.storage.blob import BlockBlobService



"""
ファイルをアップロードし、Blob を作成するサンプル。

使い方：

    python3 upload_blob.py {アカウント名} {アカウントキー} {最大コネクション数} {コンテナ名} {Blob 名} {ファイルパス}

    最大コネクション数を指定することで、サイズの大きいファイルのアップロードが速くなる。
"""


def upload_blob(account_name, account_key, max_connections, container_name, blob_name, file_path):
    blob_service = BlockBlobService(account_name=account_name, account_key=account_key)
    blob_service.create_blob_from_path(container_name, blob_name, file_path, max_connections=max_connections)



# Main method.
if __name__ == '__main__':
    account_name = sys.argv[1]
    account_key = sys.argv[2]
    max_connections = int(sys.argv[3])
    container_name = sys.argv[4]
    blob_name = sys.argv[5]
    file_path = sys.argv[6]

    upload_blob(
        account_name,
        account_key,
        max_connections,
        container_name,
        blob_name,
        file_path,
    )
