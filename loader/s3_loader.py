import os
from dotenv import load_dotenv
from boto3.session import Session
from pathlib import Path
from tqdm import tqdm

load_dotenv()
OUT_PATH = Path(__file__).parent
PARQ_FOLDER = "fin_dataset.parquet"


def download_data_from_s3():
    """Load files from s3 parquert folder"""
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACESS_KEY")
    endpoint_url = os.environ.get("ENDPOINT_URL")

    s3 = Session()
    s3_client = s3.client(
        service_name="s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
    )

    # create output dir
    outpath = OUT_PATH / PARQ_FOLDER
    Path(outpath).mkdir(parents=True, exist_ok=True)

    # take all files in Prefix folder. Prefix must contain only files.
    parts = s3_client.list_objects_v2(Bucket="recsys", Prefix="fin_dataset.parquet")[
        "Contents"
    ]

    # iterate over all files in s3 folder
    for obj in tqdm(parts):
        key = obj["Key"]
        _, name = key.split("/")
        outfile = str(outpath / name)
        s3_client.download_file("recsys", key, outfile)


if __name__ == "__main__":
    download_data_from_s3()
