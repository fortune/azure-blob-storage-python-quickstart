import sys
from azure.storage.blob import BlockBlobService

#
# Blob 情報を取得するサンプル。
#
# Blob 情報は、azure.storage.blob.models.Blob 、および、その中の properties フィールドにセットされる
# azure.storage.blob.models.BlobProperties オブジェクトで表現される。
#
# アカウント名、アカウントキー、コンテナ名、Blob 名を指定して実行すると、その Blob の情報（名前、タイプ、サイズ、最終更新日時、
# メタデータ）を表示する。
#

def run_sample(account_name, account_key, container_name, blob_name):
    blob_service = BlockBlobService(
        account_name=account_name,
        account_key=account_key)

    blob = blob_service.get_blob_properties(container_name, blob_name)

    print('\t Name: ' + blob.name)
    print('\t Blob type: ' + blob.properties.blob_type)
    print('\t Content length: ' + str(blob.properties.content_length))
    print('\t Last modified: ' + str(blob.properties.last_modified))
    print('\t Metadata: ' + str(blob.metadata))

# Main method.
if __name__ == '__main__':
    account_name = sys.argv[1]
    account_key = sys.argv[2]
    container_name = sys.argv[3]
    blob_name = sys.argv[4]

    run_sample(account_name, account_key, container_name, blob_name)