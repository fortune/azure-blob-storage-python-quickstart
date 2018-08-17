import sys
from datetime import datetime, timedelta
from azure.storage.blob import BlockBlobService, BlobPermissions


"""
Azure Blob Storage 内の特定の Blob への Shared Access Signature を生成、取得するサンプル

使い方：

    python3 gen_blob_sas.py {アカウント名} {アカウントキー} {コンテナ名} {Blob 名} {permission} {minutes}

    指定した permission で minutes 分後まで有効な sas token と sas url を生成する。
    permission は r or w or c or s でなければならず、r は BlobPermission.READ、w は BlobPermissions.WRITE,
    c は BlobPermissions.CREATE, s は BlobPermissions(read=True, create=True) に対応する。

    CREATE と WRITE の違いは、新規書き込みのみか、上書きを許可するかの違い。奇妙なことに、サイズの小さいファイルなら
    CREATE で新規書き込みできるが、大きいファイル（ 1 GB で試したが駄目だった）だと失敗する。WRITE であれば、
    大きいファイルでも成功する。

    https://github.com/Microsoft/AzureStorageExplorer/issues/305

    で似たような問題が報告されていたので、そこでの解決策を参考に BlobPermissions(read=True, create=True) でも
    やってみたが、やはりサイズが大きいと失敗した。

    {アカウント名}, {アカウントキー}, {コンテナ名}, {Blob 名} は、正しくなかったり、存在していなくても SAS の生成では
    エラーにならないが、後で、その SAS を使用することはできないだろう。また、{アカウントキー} の形式（文字数とか）は
    正しくないと SAS 生成でエラーになる。

    SAS を使ってダウンロードしている最中に SAS が期限切れになっても途中でエラーにはならずに処理は
    そのまま続いていく。ただし、新たに、もしくは再度、その SAS を使って処理を開始することはできない。

    アップロードの場合、途中で期限切れになると、そこでアップロード処理そのものも失敗して終わる。
"""



def generate_blob_sas(account_name, account_key, container_name, blob_name, permission, minutes):
    """
    Azure Blob の SAS トークンと SAS URL を生成し、この順でタプルにして返す。
    """
    block_blob_service = BlockBlobService(
            account_name=account_name,
            account_key=account_key)

    sas_token = block_blob_service.generate_blob_shared_access_signature(
        container_name,
        blob_name,
        permission,
        datetime.utcnow() + timedelta(minutes=minutes)
    )

    return sas_token, block_blob_service.make_blob_url(container_name, blob_name, sas_token=sas_token)


# Main method.
if __name__ == '__main__':
    account_name = sys.argv[1]
    account_key = sys.argv[2]
    container_name = sys.argv[3]
    blob_name = sys.argv[4]
    if sys.argv[5] == 'r':
        permission = BlobPermissions.READ
    elif sys.argv[5] == 'c':
        permission = BlobPermissions.CREATE
    elif sys.argv[5] == 'w':
        permission = BlobPermissions.WRITE
    elif sys.argv[5] == 's':
        permission = BlobPermissions(read=True, create=True)
    else:
        raise Exception('Illegal argument: ' + sys.argv[5])

    minutes = int(sys.argv[6])

    sas_token, sas_url = generate_blob_sas(
        account_name,
        account_key,
        container_name,
        blob_name,
        permission,
        minutes,
    )

    print('sas token =', sas_token)
    print('sas url =', sas_url)


