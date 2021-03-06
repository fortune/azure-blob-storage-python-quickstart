# Azure Blob ストレージの Quickstart for Python

[クイック スタート: Python を使用して BLOB をアップロード、ダウンロード、および一覧表示する](https://docs.microsoft.com/ja-jp/azure/storage/blobs/storage-quickstart-blobs-python) 中の https://github.com/Azure-Samples/storage-blobs-python-quickstart にあるサンプルプログラムを修正し、いくつか追加した。

- upload_blob.py

    使用方法: `python3 upload_blob.py <account name> <account key> <max_connections> <container name> <blob name> <local file path>`

    指定したローカルファイルを指定した Blob 名でアップロードする。サイズの大きいファイルは並列アップロードできるので、
    `max_connections` を大きくしてやると、アップロードが速くなる。インターネット越しに 879 MB をデフォルトの
    max_connections=2 でアップロードすると、2 分ちょっとかかったが、20 を指定すると 26 秒で完了した。

- download_blob.py

    使用方法: `python3 download_blob.py <account name> <account key> <max_connections> <container name> <blob name> <local file path>`

    指定した Blob を指定したローカルファイルにダウンロードする。サイズの大きいファイルは並列ダウンロードできるので、
    `max_connections` を大きくしてやると、ダウンロードが速くなる。インターネット越しに 3.73 GB の Blob をデフォルトの
    max_connections=2 でダウンロードすると、33 分かかったが、50 を指定すると、3 分 40 秒程度で完了した。

- example.py

    使用方法: `python3 example.py <account name> <account key> <container name>`
    
    カレントディレクトリにファイルを作成し、それを引数で指定した Blob ストレージのコンテナにアップロードし、ダウンロードする。
    その際、メタ情報も一緒にアップロード、取得できるように修正した。最後のクリーンアップで、ローカルのファイルとアップロードした
    Blob は削除するが、コンテナは削除しない。既存のコンテナを指定した場合、そのコンテナのアクセス権限が変更され、
    匿名の読み取り、書き込み権限が与えられるので気をつけること。

- blob_properties.py

    使用方法: `python3 blob_properties.py <account name> <account key> <container name> <blob name>`

    引数で指定した Blob のプロパティ情報をいくつか取得する。すなわち、Blob 名、Blob のタイプ、サイズ、最終更新日、およびメタデータを取得する。

- blob_copy.py

    使用方法: `python3 blob_copy.py <account name> <account key> <copy 元 container name> <copy 元 blob name> <copy 先 container name> <copy 先 blob name>`

    やってみるとわかるが、同一コンテナ内でコピーすると、数 GB の Blob でも一瞬でコピーできる。その Blob を別のプロセスでダウンロード中であっても同じ。
    `copy_blob` メソッドが一瞬でコピーできるのは、非同期で best effort でやっているからなので、コピーが完了したことを当てにしてはならない。


## Shared Access Signatures(SAS) を利用した Blob のダウンロードとアップロード

[Shared Access Signatures (SAS) の使用](https://docs.microsoft.com/ja-jp/azure/storage/common/storage-dotnet-shared-access-signature-part-1)

Python SDK を使って SAS を生成する場合、`BaseBlobService` クラスの `generate_account_shared_access_signature`,
`generate_container_shared_access_signature`, `generate_blob_shared_access_signature` メソッドを使う。
それぞれ、Storage アカウント、コンテナ、（コンテナ内の）Blob に対する sas token を生成する。これらの sas token から
特定の Blob に対する sas url を生成するには `make_blob_url` メソッドを使う。

Blob に対する SAS トークンは、特定の Blob の読み出しや書き込み、削除、作成、追加の権限を与える。
各々の権限は、`BlobPermissions` で表す。

コンテナに対する SAS トークンは、特定のコンテナ内にある Blob のリスト、任意の Blob の削除、任意の Blob の読み出し、
任意の Blob の作成や書き込みの権限を与える。各々の権限は、`ContainerPermissions` で表す。ちなみに削除の権限を与えなくても
作成（書き込み）の権限を与えれば上書きすることは可能。

Storage アカウントに対する SAS トークンは、特定の Storage アカウント内での権限を与える。Storage アカウント内には
Blob 以外にも File 共有や Queue、Table 等のサービスがあるので、ある権限がどういう意味をもつかはサービスにより異なる。
各々の権限は、`AccountPermissions` で表す。ちなみに Blob サービスにおいて、コンテナを作成したり削除するためには
このレベルの SAS が必要になる。



[BaseBlobService class](https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.baseblobservice.baseblobservice?view=azure-python)

[BlockBlobService class](https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blockblobservice.blockblobservice?view=azure-python)

[BlobPermissions class](https://docs.microsoft.com/ja-jp/python/api/azure-storage-blob/azure.storage.blob.models.BlobPermissions?view=azure-python)

[ContainerPermissions class](https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.models.containerpermissions?view=azure-python)

[AccountPermissions class](https://docs.microsoft.com/en-us/python/api/azure-storage-common/azure.storage.common.models.accountpermissions?view=azure-python)


ダウンロードであれば、ブラウザや `curl` コマンド、Python の標準ライブラリから sas url にアクセスし、
Blob をダウンロードできる。sas token を使い、Azure SDK for Python を利用してダウンロードすることもできる。

アップロードの場合、Azure SDK for Python から sas token を使ってアップロードできる。sas url を使っても
ブラウザ上でマルチパートでアップロードすることはできないので、sas url を利用するなら REST API を使って
HTTP PUT メソッドでアップロードする。しかし、この場合、大きいファイルは分割アップロードしなければならない。
したがって、Python からアップロードするなら、REST API ではなく、SDK を使う方がいい。

[Put Blob](https://docs.microsoft.com/ja-jp/rest/api/storageservices/put-blob)


JavaScript を使うなら、REST API を叩くしかないが、その場合でもライブラリが提供されているので、手動で
分割アップロードするようなことはしなくて済む。ただ、ブラウザ上の Ajax で通信するときはクロスドメイン対応が必要になる。
Azure ではストレージサービスでの Cross Origin Resource Sharing(CORS) をサポートしているので、それを使う。
具体的には、Azure ポータル上のストレージアカウントで、CORS の設定をすればいい。

[Azure ストレージ サービスでのクロス オリジン リソース共有 (CORS) のサポート](https://docs.microsoft.com/ja-jp/azure/storage/common/storage-cors-support)

以下、Python を使った Blob アップロードと SAS 取得のサンプル

- gen_blob_sas.py

    使用方法: `python3 gen_blob_sas.py <account name> <account key> <container name> <blob name> <permission> <minutes>`

    指定した Blob に対して、minutes 分後まで有効な、権限が permission である sas token と sas url を取得する。
    permission は、'r' or 'c' or 'w' or 's' である。それぞれ、`BlobPermissions.READ`, `BlobPermissions.CREATE`,
    `BlobPermissions.WRITE`, `BlobPermissions(read=True, create=True)` に対応させた。

    ソース中のコメントに書いたが、大きいサイズの Blob をアップロードするとき、`BlobPermissions.CREATE` だと
    うまくいかない。

    https://github.com/Azure/azure-storage-python/blob/master/samples/blob/sas_usage.py

- upload_blob_with_sas_token.py

    使用方法: `python3 upload_blob_with_sas_token.py <account name> <sas_token> <container name> <blob name> <local file path>`

    `gen_blob_sas.py` で取得した sas token を使えばいい。local file path で指定したファイルを Blob として
    アップロードする。当然、sas token は正しく書き込み権限をもち、ここで指定する account name, container name,
    blob name を使って生成されていなくてはならない。

- put_blob_with_sas_url.py

    使用方法: `python3 put_blob_with_sas_url.py <sas url> <local file path>`

    `gen_blob_sas.py` で取得した sas url を使えばいい。ここでは SDK ではなく、REST API を叩いて
    ファイルをアップロードする。前述したとおり、サイズが大きいファイルは分割アップロードしなければならないが、
    ここでは対応していないので、local file path に指定するファイルのサイズは、256MB 以下でないといけない。

    https://github.com/rahulbagal/upload-file-azure-sas-url/blob/master/azure_sas_upload.py


