# Azure Blob ストレージの Quickstart for Python

[クイック スタート: Python を使用して BLOB をアップロード、ダウンロード、および一覧表示する](https://docs.microsoft.com/ja-jp/azure/storage/blobs/storage-quickstart-blobs-python) 中の https://github.com/Azure-Samples/storage-blobs-python-quickstart にあるサンプルプログラムを修正し、いくつか追加した。

- example.py

    使用方法: `python3 example.py <account name> <account key> <container name>`
    
    カレントディレクトリにファイルを作成し、それを引数で指定した Blob ストレージのコンテナにアップロードし、ダウンロードする。
    その際、メタ情報も一緒にアップロード、取得できるように修正した。最後のクリーンアップで、ローカルのファイルとアップロードした
    Blob は削除するが、コンテナは削除しない。

- blob_properties.py

    使用方法: `python3 blob_properties.py <account name> <account key> <container name> <blob name>`

    引数で指定した Blob のプロパティ情報をいくつか取得する。すなわち、Blob 名、Blob のタイプ、サイズ、最終更新日、およびメタデータを取得する。

- blob_copy.py

    使用方法: `python3 blob_copy.py <account name> <account key> <copy 元 container name> <copy 元 blob name> <copy 先 container name> <copy 先 blob name>`

    やってみるとわかるが、同一コンテナ内でコピーすると、数 GB の Blob でも一瞬でコピーできる。その Blob を
    別のプロセスでダウンロード中であっても同じ。