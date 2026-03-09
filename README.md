# shelby-s3-sync

> Sync local directories to Shelby Protocol via the S3-compatible gateway.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Shelby](https://img.shields.io/badge/Shelby-Protocol-c6ff00?style=flat-square&labelColor=0a0a0f)

## Requirements

- Python 3.8+
- Shelby S3 Gateway: `npx @shelby-protocol/s3-gateway`

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python -m shelby_s3_sync ./my-files 0xYourAddress --prefix backups
python -m shelby_s3_sync ./my-files 0xYourAddress --dry-run
```

## Python API
```python
from shelby_s3_sync.sync import create_s3_client, sync_directory

client = create_s3_client(endpoint_url="http://localhost:9000")
results = sync_directory("./datasets", "0xYourAddress", prefix="ml/training")
```

## License
MIT
