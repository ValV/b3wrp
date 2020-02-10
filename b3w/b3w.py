import pathlib
import time
from typing import List

import boto3
import botocore

class B3W(object):
    def __init__(self, bucket_name: str,
                 aws_access_key_id: str = None,
                 aws_secret_access_key: str = None,
                 local_path: str = '.', prefix: str = ''):
        self.__bucket_name = bucket_name
        self.__s3r = boto3.resource('s3', aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key)
        self.__s3c = boto3.client('s3')
        self.__local_path = local_path
        self.__prefix = prefix

    @property
    def bucket_name(self) -> str:
        return self.__bucket_name

    @bucket_name.setter
    def bucket_name(self, value: str):
        self.__bucket_name = value

    @property
    def local_path(self) -> str:
        return self.__local_path

    @local_path.setter
    def local_path(self, value: str):
        self.__local_path = value

    @property
    def prefix(self) -> str:
        return self.__prefix

    @prefix.setter
    def prefix(self, value: str):
        self.__prefix = value

    def ls(self, prefix=None) -> List[str]:
        """
        List over objects in the bucket.
        :param prefix: Optional param to set `base directory`
        :return: List
        """
        if prefix and not prefix in ('.', './', './*', '*'):
            return [x.key for x in self.__s3r.Bucket(self.bucket_name).objects.filter(Prefix=prefix)]
        else:
            return [x.key for x in self.__s3r.Bucket(self.bucket_name).objects.all()]

    def get(self, remote_path: str, local_path: str = None) -> None:
        """
        Get a file from s3 bucket.
        :param remote_path:  key in S3 bucket
        :param local_path:
        :return: None
        """
        try:
            if not local_path:
                local_path = f"{self.local_path}/{pathlib.Path(remote_path).name}"
            self.__s3r.Bucket(self.bucket_name).download_file(
                remote_path, local_path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
        return None

    def put(self, local_path, remote_path, timestamp=False, force=False) -> None:
        """
        Load a file into s3 bucket.
        :param remote_path:  key in S3 bucket
        :param local_path:
        "param timestamp:
        :param force:
        :return: None
        """
        p = pathlib.Path(remote_path)
        if not timestamp and not force:
            if remote_path in self.ls(p.parent.as_posix()):
                raise Exception(f"Object <{remote_path}> already exists.")
        elif timestamp:
            """Add timestamp"""
            remote_path = f"{p.parent if p.parent.as_posix() != '.' else ''}{p.stem}_{time.strftime('%Y-%m-%d-%H-%M-%S')}{p.suffix}"
        self.__s3r.Bucket(self.bucket_name).upload_file(local_path, remote_path)
        return None
