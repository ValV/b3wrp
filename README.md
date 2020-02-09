# AWS Boto3 Wrapper

## Prerequisites

- setup AWS credentials
- `pip install boto3`

# Methods

B3W class has only 3 methods:
- `get`
- `upload`
- `list_objects`

```python
def get(self, s3_path: str, output_path: str = None) -> None:
    ...

def upload(self, file_path, s3_path, timestamp=False, force=False):
    ...

def list_objects(self, prefix=None) -> List[str]:
    ...
```

# Usage example

```python
from b3w import B3W

s3 = B3W('bucket-name', default_path='./weights')
...

s3.list_objects(prefix='weights/project/')  # List all objects under 'weights/project/'
s3.get('path-to-file-in-this-bucket.h5')  # Get some model/weight
s3.get('path-to-file-in-this-bucket.zip')  # Get some dataset
s3.upload('./weights/best.pth', 'path/to/file/in/bucket/best.pth')  # Upload resulted weight
```

