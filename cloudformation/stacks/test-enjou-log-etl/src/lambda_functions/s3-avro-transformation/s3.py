import os
import uuid
from typing import Any, Dict, List

from base import Base


class S3(Base):
    def __init__(self):
        super().__init__("s3")
        self.bucket = os.getenv("S3_BUCKET")

    def download_file(
        self,
        bucket: str,
        key: str,
        download_path: str = None,
    ) -> None:
        """Download file from S3
        Args:
            download_path (str): ダウンロード先のパス（例えば，Lambda だと /tmp 配下にファイルをダウンロードした）
            bucket (str): bucket name
            key ([type]): file object name
        """

        if not download_path:  # for Lambda
            download_path = "/tmp/{}-{}".format(uuid.uuid4(), key)

        self.client.download_file(bucket, key, download_path)

    def upload_file(self, upload_path: str, bucket: str, key) -> None:
        """Upload file to S3
        Args:
            upload_path (str): ローカルに存在する，S3 へアップロードするファイルのパス（例えば，Lambda だと /tmp 配下にダウンロードしたファイルを加工して /tmp 配下のファイルをパスに指定する）
            bucket (str): bucket name
            key ([type]): file object name
        """

        self.client.upload_file(upload_path, bucket, key)
