# AWS Boto3 Wrapper

## Description

100% Python

## Prerequisites

- setup AWS credentials
- `pip install boto3`

# Methods

B3W class has only 3 methods:
- `ls`
- `get`
- `put`

> `smbclient` Easter egg

Signatures:
```python
def ls(self, prefix=None) -> List[str]:
    ...

def get(self, remote_path: str, local_path: str = None) -> None:
    ...

def put(self, local_path, remote_path, timestamp=False, force=False):
    ...
```

# Usage example

```python
from b3w import B3W

s3 = B3W('bucket-name', default_path='./weights')
...

# List all objects under 'weights/project/'
s3.ls(prefix='weights/project/')

# Get some model/weight
s3.get('path-to-file-in-the-bucket.h5')

# Get some dataset
s3.get('path-to-file-in-the-bucket.zip')

# Upload resulted weight
s3.put('./weights/best.pth', 'path/to/file/in/bucket/best.pth')
```

