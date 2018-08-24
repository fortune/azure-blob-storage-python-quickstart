import sys
from azure.storage.blob import BlockBlobService



"""
Blob をダウンロードし、ローカルファイルを作成するサンプル。

使い方：

    python3 download_blob.py {アカウント名} {アカウントキー} {最大コネクション数} {コンテナ名} {Blob 名} {ローカルファイルパス}

    最大コネクション数を指定することで、サイズの大きいファイルのダウンロードが速くなる。
"""


def download_blob(account_name, account_key, max_connections, container_name, blob_name, file_path):
    blob_service = BlockBlobService(account_name=account_name, account_key=account_key)
    blob_service.get_blob_to_path(container_name, blob_name, file_path, max_connections=max_connections)



# Main method.
if __name__ == '__main__':
    account_name = sys.argv[1]
    account_key = sys.argv[2]
    max_connections = int(sys.argv[3])
    container_name = sys.argv[4]
    blob_name = sys.argv[5]
    file_path = sys.argv[6]

    download_blob(
        account_name,
        account_key,
        max_connections,
        container_name,
        blob_name,
        file_path,
    )
