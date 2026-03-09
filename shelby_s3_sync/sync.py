import boto3
import hashlib
from pathlib import Path
from botocore.client import Config


def create_s3_client(endpoint_url="http://localhost:9000",
                     access_key="AKIAIOSFODNN7EXAMPLE",
                     secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                     region="shelbyland"):
    return boto3.client("s3", endpoint_url=endpoint_url,
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key,
                        region_name=region,
                        config=Config(signature_version="s3v4"))


def compute_file_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def sync_directory(local_dir, bucket, prefix="", client=None, dry_run=False):
    if client is None:
        client = create_s3_client()
    results = {"uploaded": 0, "skipped": 0, "failed": 0}
    for file_path in Path(local_dir).rglob("*"):
        if not file_path.is_file():
            continue
        relative = file_path.relative_to(local_dir)
        blob_name = f"{prefix}/{relative}".lstrip("/") if prefix else str(relative)
        file_hash = compute_file_hash(str(file_path))
        if dry_run:
            print(f"[DRY RUN] {file_path} → {bucket}/{blob_name}")
            results["skipped"] += 1
            continue
        try:
            client.upload_file(str(file_path), bucket, blob_name,
                               ExtraArgs={"Metadata": {"sha256": file_hash}})
            print(f"✅ {blob_name} (sha256: {file_hash[:8]}...)")
            results["uploaded"] += 1
        except Exception as e:
            print(f"❌ {blob_name} — {e}")
            results["failed"] += 1
    return results
