import os
import json
import textwrap

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

DOWNLOAD_FILE_NAME = 'articles.json'
GENERATE_FILE_NAME = 'README.md'
FIREBASE_ACCESS_TOKEN_FILE = 'wr6yghttcx9.json'


def download_blob(bucket_name, source_blob_name, destination_file_name):
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )

    
def main():
    
    STORAGE_BUCKET_URL = os.environ.get("STORAGE_BUCKET_URL")
    
    cred = credentials.Certificate(FIREBASE_ACCESS_TOKEN_FILE)
    firebase_admin.initialize_app(cred, {
        'storageBucket': storage
    })

    download_blob(STORAGE_BUCKET_URL, DOWNLOAD_FILE_NAME, DOWNLOAD_FILE_NAME)

    f = open(DOWNLOAD_FILE_NAME, 'r')
    d = json.load(f)
    docs_str = textwrap.dedent("""\
    # tokizo

    [![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=tokizuoh&layout=compact)](https://github.com/anuraghazra/github-readme-stats)

    ## Recent Posts

    - [{a1}]({u1})
    - [{a2}]({u2})
    - [{a3}]({u3})
    - [{a4}]({u4})
    - [{a5}]({u5})""").format(
        a1=d[0]['title'],
        u1=d[0]['url'],
        a2=d[1]['title'],
        u2=d[1]['url'],
        a3=d[2]['title'],
        u3=d[2]['url'],
        a4=d[3]['title'],
        u4=d[3]['url'],
        a5=d[4]['title'],
        u5=d[4]['url'],
    )

    with open(GENERATE_FILE_NAME, 'w') as f:
        f.write(docs_str)


if __name__ == '__main__':
    main()
