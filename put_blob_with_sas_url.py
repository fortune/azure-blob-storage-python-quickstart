
import sys
import requests

"""
SAS URL に対して REST API を使ってファイルをアップロードする。

使い方：

    python3 put_blob_with_sas_url.py {sas_url} {file_path}

    ファイルサイズが 256MB より大きい場合、HTTP 413 Payload too large で失敗する。
    その場合、ファイルを分割してアップロードしなければならない。したがって、Python で
    アップロードするならば、REST API ではなく、SDK を用いてアップロードした方がいい。
"""

def put_blob_with_sas_url(sas_url, file_path):
    with open(file_path, 'rb') as fh:
        response = requests.put(
            sas_url,
            data=fh,
            headers={
                'x-ms-blob-type': 'BlockBlob'
            },
        )
    return response



# Main method.
if __name__ == '__main__':
    sas_url = sys.argv[1]
    file_path = sys.argv[2]

    response = put_blob_with_sas_url(
        sas_url,
        file_path,
    )

    print(response)
