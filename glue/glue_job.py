import sys
import io
import uuid

from decimal import Decimal, ROUND_HALF_UP
from urllib.parse import urlparse

import boto3
import pandas as pd

from awsglue.utils import getResolvedOptions


# Read arguments passed by Lambda / Glue job configuration
args = getResolvedOptions(
    sys.argv,
    [
        "INPUT_PATH",
        "OUTPUT_PATH"
    ]
)

input_path = args["INPUT_PATH"]
output_path = args["OUTPUT_PATH"]


# Python shell jobs have no Spark context, so S3 is read and written with boto3
s3 = boto3.client("s3")


def split_s3_uri(uri):
    # Split an s3://bucket/key URI into its bucket and key parts
    parsed = urlparse(uri)

    return parsed.netloc, parsed.path.lstrip("/")


def list_input_keys(bucket, key):
    # Spark accepted either a single file or a folder and read every CSV it
    # found underneath, so both cases are resolved here.
    if key and not key.endswith("/"):
        return [key]

    keys = []
    paginator = s3.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=bucket, Prefix=key):
        for obj in page.get("Contents", []):

            # Skip folder placeholder objects
            if obj["Key"].endswith("/"):
                continue

            keys.append(obj["Key"])

    return keys


def read_csv(bucket, key):
    # Read one CSV object from S3 into a DataFrame.
    # A header row and inferred column types match the Spark reader options.
    body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()

    return pd.read_csv(io.BytesIO(body))


def round_half_up(value):
    # Round to 2 decimals the way Spark's round() does.
    # pandas rounds halves to even, so 0.045 would become 0.04 here instead
    # of the 0.05 the Spark job produced.
    if pd.isna(value):
        return value

    return float(
        Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
    )


# Resolve the input into the list of CSV objects to process
input_bucket, input_key = split_s3_uri(input_path)

input_keys = list_input_keys(input_bucket, input_key)

if not input_keys:
    raise Exception(f"No input files found at {input_path}")


# Read the CSV file(s) from S3.
# Spark unioned everything under the path into a single DataFrame.
df = pd.concat(
    [read_csv(input_bucket, key) for key in input_keys],
    ignore_index=True
)


# Remove completely empty rows
df = df.dropna(how="all")


# Convert customer names to uppercase.
# The string cast mirrors Spark's upper(), which casts non-string columns
# and leaves nulls untouched.
df["customer_name"] = df["customer_name"].astype("string").str.upper()


# Add a new column with a 10% discount
df["discounted_amount"] = (df["amount"] * 0.90).map(round_half_up)


# Write transformed data back to S3.
# One new object per run keeps previous output files instead of replacing
# them, which is what the Spark append mode did.
output_bucket, output_prefix = split_s3_uri(output_path)

if output_prefix and not output_prefix.endswith("/"):
    output_prefix += "/"

output_key = f"{output_prefix}part-{uuid.uuid4().hex}.csv"

buffer = io.StringIO()

df.to_csv(buffer, index=False, header=True)

s3.put_object(
    Bucket=output_bucket,
    Key=output_key,
    Body=buffer.getvalue().encode("utf-8")
)

print(f"Read {len(input_keys)} input file(s) from {input_path}")
print(f"Wrote {len(df)} rows to s3://{output_bucket}/{output_key}")
