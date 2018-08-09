import sys
from azure.storage.blob import BlockBlobService

#
# Blob をクラウド上でコピーするサンプル。
#
# アカウント名、アカウントキー、コピー元のコンテナ名、コピー元 Blob、コピー先のコンテナ名、コピー先の Blob を引数で指定する。
#

def run_sample(account_name, account_key, from_container_name, from_blob, to_container_name, to_blob):
    blob_service = BlockBlobService(
        account_name=account_name,
        account_key=account_key)

    if not blob_service.exists(from_container_name, from_blob):
        sys.exit('Not exist: ' + from_blob + ' in ' + from_container_name)
    
    if blob_service.exists(to_container_name, to_blob):
        sys.exit('Exist: ' + to_blob + ' in ' + to_container_name)

    blob_url = blob_service.make_blob_url(from_container_name, from_blob)

    blob_service.copy_blob(to_container_name, to_blob, blob_url)



# Main method.
if __name__ == '__main__':
    account_name = sys.argv[1]
    account_key = sys.argv[2]
    from_container_name = sys.argv[3]
    from_blob = sys.argv[4]
    to_container_name = sys.argv[5]
    to_blob = sys.argv[6]

    run_sample(account_name, account_key, from_container_name, from_blob, to_container_name, to_blob)
