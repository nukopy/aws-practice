import os
from typing import Any, Dict, List

from app.aws.base import Base


class S3(Base):
    def __init__(self):
        super().__init__("s3")
        self.bucket = os.getenv("S3_BUCKET")

    def upload(self):
        pass
