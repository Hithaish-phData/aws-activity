import boto3
import os
import urllib.parse

from botocore.exceptions import ClientError


# Create the Glue client once outside the Lambda handler
glue = boto3.client("glue")


# Glue job name is provided through the Lambda environment variable
GLUE_JOB_NAME = os.environ["GLUE_JOB_NAME"]


def lambda_handler(event, context):
    # Log the complete incoming S3 event for debugging
    print(f"Received event: {event}")

    # Read the first S3 event record
    record = event["Records"][0]

    # Get the S3 bucket name
    bucket_name = record["s3"]["bucket"]["name"]

    # Get the uploaded object's size
    object_size = record["s3"]["object"].get("size", 0)

    # S3 object keys can be URL encoded, so decode the key
    object_key = urllib.parse.unquote_plus(
        record["s3"]["object"]["key"]
    )

    print(f"Bucket: {bucket_name}")
    print(f"Object key: {object_key}")
    print(f"Object size: {object_size} bytes")


    # Ignore anything uploaded outside input/
    if not object_key.startswith("input/"):
        print("Ignored: object is outside input/")

        return {
            "statusCode": 200,
            "message": "Ignored object outside input/"
        }


    # Ignore anything that is not a CSV file
    if not object_key.lower().endswith(".csv"):
        print("Ignored: object is not a CSV file")

        return {
            "statusCode": 200,
            "message": "Ignored non-CSV file"
        }


    # Ignore empty files
    # This prevents a 0-byte CSV from unnecessarily starting Glue
    if object_size == 0:
        print("Ignored: CSV file is empty")

        return {
            "statusCode": 200,
            "message": "Ignored empty CSV file"
        }


    # Build the exact input S3 path
    input_path = f"s3://{bucket_name}/{object_key}"


    # Get only the filename
    file_name = object_key.split("/")[-1]


    # Remove the .csv extension
    base_name = file_name.rsplit(".", 1)[0]


    # Create a separate output folder for this input file
    output_path = f"s3://{bucket_name}/output/{base_name}/"


    print(f"Input path: {input_path}")
    print(f"Output path: {output_path}")
    print(f"Starting Glue job: {GLUE_JOB_NAME}")


    try:
        # Start the Glue ETL job
        response = glue.start_job_run(
            JobName=GLUE_JOB_NAME,
            Arguments={
                "--INPUT_PATH": input_path,
                "--OUTPUT_PATH": output_path
            }
        )

        print("Glue job started successfully")
        print(f"Glue JobRunId: {response['JobRunId']}")

        return {
            "statusCode": 200,
            "message": "Glue job started successfully",
            "jobRunId": response["JobRunId"],
            "inputPath": input_path,
            "outputPath": output_path
        }


    except ClientError as error:
        error_code = error.response["Error"]["Code"]


        # Glue is already processing another file
        if error_code == "ConcurrentRunsExceededException":
            print(
                "Glue job is already running. "
                "This file was not started to avoid concurrent Glue runs."
            )

            return {
                "statusCode": 200,
                "message": "Glue job already running",
                "inputPath": input_path
            }


        # Log and re-raise any unexpected AWS error
        print(f"Unexpected AWS error: {error}")
        raise