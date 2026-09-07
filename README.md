# AWS S3 → Lambda → Glue Workflow Data Pipeline

## Overview

This activity demonstrates an event-driven AWS data pipeline using
Amazon S3, AWS Lambda, AWS Glue Crawler, AWS Glue Data Catalog, AWS Glue
Python Shell, and Amazon S3.

The implementation is documented using two separate approaches:

1.  **Manual Approach** -- AWS resources are created and configured
    manually through the AWS Management Console.
2.  **CloudFormation Approach** -- AWS infrastructure is provisioned
    through AWS CloudFormation and deployed using GitHub Actions with
    GitHub OIDC.

The screenshots are separated into two folders:

-   `images/MNL/` -- screenshots used for the Manual Approach.
-   `images/CFN/` -- screenshots used for the CloudFormation
    Approach.

------------------------------------------------------------------------

# 1. Manual Approach

## 1.1 Overview

In the Manual Approach, the AWS resources are created and configured
directly through the AWS Management Console.

The pipeline follows this flow:

``` text
Upload CSV
   ↓
Source S3 Bucket
   ↓
S3 ObjectCreated Event
   ↓
Lambda Function
   ↓
Glue Workflow
   ↓
Glue Crawler
   ↓
Glue Data Catalog
   ↓
Glue Python Shell Job
   ↓
Destination S3 Bucket
   ↓
Processed CSV
```

## 1.2 S3 Buckets

The source and destination S3 buckets are configured manually for the
pipeline.

![S3 Buckets](images/MNL/S3-Buckets.png)

The source bucket contains the input folder used by the Glue crawler.

![S3 Source Folders](images/MNL/S3_Source_Folders.png)

The Python transformation script is stored in S3 for the Glue Python
Shell job.

![S3 Source Script](images/MNL/S3_Source_Script.png)


## 1.3 IAM Roles

The IAM roles required for the AWS services are created and configured
manually.

![Roles for AWS Activity](images/MNL/Roles_for_AWS_Activity.png)

The Lambda execution role provides the required permissions for the
Lambda function.

![Lambda Role](images/MNL/Lambda_Role.png)

![Lambda CloudWatch Role](images/MNL/Lambda_Cloudwatch_Role.png)

![Lambda Role Success](images/MNL/Lambda_Role_Success.png)

## 1.4 Lambda Function

The Lambda function is created to respond to the S3 object-created event
and start the Glue workflow.

![Lambda Function Creation](images/MNL/Lambda_Function_Creation.png)

![Lambda Function Code](images/MNL/Lambda_Function_Code.png)

The Lambda function is deployed and configured with the required
trigger.

![Lambda Function Deployment](images/MNL/Lambda_Function_Deploy.png)

![Lambda Trigger](images/MNL/Lambda_Trigger.png)

![S3 Trigger](images/MNL/S3_Trigger.png)

![Trigger Configuration](images/MNL/Trigger.png)

## 1.5 Glue Crawler and Data Catalog

The Glue crawler is configured to scan the source S3 location and
populate the Glue Data Catalog.

![Glue Source Crawler](images/MNL/S3_SRC_Crawler.png)

The Glue Data Catalog database is created for the crawled data.

![Glue Data Catalog](images/MNL/DB_Glue_Catalog.png)

## 1.6 Glue Python Shell Job

A Glue Python Shell job is configured to perform the transformation.

![Python Shell Job](images/MNL/Python_Shell.png)

The job parameters define the input and output locations.

![Job Parameters](images/MNL/Job_parameters.png)

The location of the ETL script is configured in S3.

![ETL Script Location](images/MNL/ETL_Script_Loc.png)

The transformation source script is documented below.

![Source Script](images/MNL/Source_Script.png)

## 1.7 Glue Workflow

The Glue Workflow orchestrates the crawler and Python Shell job.

![Glue Workflow 1](images/MNL/Glue_Workflow_1.png)

![Glue Workflow 2](images/MNL/Glue_Workflow_2.png)

![Glue Workflow 3](images/MNL/Glue_Workflow_3.png)

![Glue Workflow 4](images/MNL/Glue_Workflow_4.png)

![Glue Workflow 5](images/MNL/Glue_Workflow_5.png)

![Glue Workflow 6](images/MNL/Glue_Workflow_6.png)

![Glue Workflow 7](images/MNL/Glue_Workflow_7.png)

The workflow status and execution details are verified after execution.

![Glue Workflow Status](images/MNL/Glue_Workflow_Status.png)

## 1.8 Input CSV Upload

In the Manual Approach, the input CSV is uploaded manually to the source
S3 bucket. The S3 object-created event then invokes the Lambda function.

![Upload CSV to S3](images/MNL/Upload_CSV_to_S3_Bucket.png)

![Uploaded CSV File](images/MNL/Uploaded_CSV_File.png)

## 1.9 Execution and Validation

CloudWatch logs are used to verify the S3 event and Lambda execution.

![CloudWatch Logs](images/MNL/Cloudwatch_logs.png)

The successful workflow execution is verified.

![Workflow History](images/MNL/Workflow_History.png)

![Workflow Success](images/MNL/Successful_Workflow.png)

The processed output is generated in the destination S3 bucket.

![Output Transformed Files](images/MNL/Output_Transformed_Files.png)

------------------------------------------------------------------------

# 2. CloudFormation Approach

## 2.1 Overview

The CloudFormation Approach automates the provisioning and deployment of
the AWS infrastructure.

The implementation uses:

-   **AWS CloudFormation** for infrastructure as code.
-   **GitHub Actions** for CI/CD.
-   **GitHub OIDC** for AWS authentication without long-lived AWS access
    keys.
-   **Amazon S3** for the source and destination data.
-   **AWS Lambda** for the S3 event-driven workflow start.
-   **AWS Glue** for crawling, cataloging, orchestration, and
    transformation.

The automated flow is:

``` text
GitHub Repository
      ↓
GitHub Actions
      ↓
GitHub OIDC Authentication
      ↓
CloudFormation Deployment
      ↓
Upload input/sample.csv to Source S3
      ↓
S3 ObjectCreated Event
      ↓
Lambda
      ↓
Glue Workflow
      ↓
Crawler
      ↓
Conditional Trigger
      ↓
Glue Python Shell
      ↓
Destination S3
      ↓
Processed CSV
```

# 2. CloudFormation Approach

## 2.1 Overview

The CloudFormation Approach automates the deployment and execution of
the AWS data pipeline using **AWS CloudFormation** and **GitHub
Actions**.

The complete pipeline follows this sequence:

``` text
GitHub Repository
        ↓
GitHub Actions
        ↓
GitHub OIDC Authentication
        ↓
CloudFormation Deployment
        ↓
Upload input/sample.csv to Source S3
        ↓
S3 ObjectCreated Event
        ↓
Lambda Function
        ↓
Glue Workflow
        ↓
Glue Crawler
        ↓
Conditional Trigger
        ↓
Glue Python Shell Job
        ↓
Destination S3
        ↓
Processed CSV
```

## 2.2 GitHub Repository

The project source code, CloudFormation template, Glue script, Lambda
code, and input CSV are maintained in the GitHub repository.

The input file used for the pipeline is:

``` text
input/sample.csv
```

### GitHub Repository
![GitHub Repository](images/CFN/GitHub_Repo.png)


GitHub Actions uses the repository as the source for the deployment
files and input data.

![GitHub Workflow](images/CFN/Workflow_Success.png)

Deatailed view of Jobs
![GitHub Workflow Detailed View](images/CFN/Workflow_deailed_view.png)


## 2.3 GitHub Actions and OIDC Authentication

GitHub Actions is used to automate the deployment process.

Before interacting with AWS, GitHub Actions authenticates using the
GitHub OIDC identity provider.

![GitHub Identity Provider](images/CFN/Identity_Provider_for_Github.png)

An IAM deployment role is configured to allow GitHub Actions to assume
the role through OIDC.

![GitHub IAM Role](images/CFN/IAM_Role_Github.png)

This eliminates the need to store long-lived AWS access keys in GitHub.

## 2.4 CloudFormation Deployment

After authentication, GitHub Actions validates and deploys the
CloudFormation template.

The CloudFormation template provisions the AWS infrastructure required
for the pipeline.

![CloudFormation Resources](images/CFN/Resources_created_by_Cloudform.png)

The CloudFormation stack creates the source S3 bucket used for input
data.

![CloudFormation Source S3 Bucket](images/CFN/CFN_Source_S3_Bucket.png)

The S3 bucket to store the uploaded Transformation logic.

![S3 Location for Python Script](images/CFN/S3_to_store_python_Script.png)

The stack also provisions the required IAM roles, Lambda function, Glue
database, Glue crawler, Glue Python Shell job, Glue workflow, triggers,
and Lambda permission.

## 2.5 Glue Script Deployment

GitHub Actions uploads the Glue Python Shell script to the deployment S3
bucket.

The CloudFormation-managed Glue job references this script during
execution.

![S3 Location for Glue Python
Script](images/CFN/S3_to_store_python_Script.png)

## 2.6 Automated Input CSV Upload

After the CloudFormation deployment is completed, GitHub Actions uploads
the input CSV from the repository to the source S3 bucket.

``` text
GitHub Repository
       ↓
input/sample.csv
       ↓
GitHub Actions
       ↓
Source S3 Bucket
       ↓
input/sample.csv
```

This eliminates the need to manually upload the input CSV to the source
S3 bucket.

## 2.7 S3 Event and Lambda Trigger

When the CSV is uploaded to the source S3 bucket, an **S3 ObjectCreated
event** is generated.

The event invokes the CloudFormation-managed Lambda function.

The Lambda function starts the Glue Workflow.

``` text
CSV uploaded to S3
        ↓
S3 ObjectCreated Event
        ↓
Lambda Function
        ↓
Start Glue Workflow
```

## 2.8 Glue Workflow Execution

The Lambda function starts the CloudFormation-managed Glue Workflow.

The workflow executes the pipeline in the following sequence:

``` text
Start Trigger
      ↓
Glue Crawler
      ↓
Crawler Success Conditional Trigger
      ↓
Glue Python Shell Job
```

The Glue components provisioned by CloudFormation are shown below.

![Glue Jobs](images/CFN/Glue_jobs_MNL_CFN.png)

The workflow is configured to run the crawler first and start the Python
Shell job after the crawler completes successfully.

## 2.9 Glue Crawler

The Glue Crawler scans the input data in the source S3 bucket and
updates the Glue Data Catalog.

Once the crawler completes successfully, the conditional trigger starts
the Python Shell job.

``` text
Source S3
    ↓
Glue Crawler
    ↓
Crawler SUCCEEDED
    ↓
Conditional Trigger
    ↓
Glue Python Shell
```

## 2.10 Glue Python Shell Transformation

The conditional trigger starts the Glue Python Shell job after
successful crawler execution.

The Python Shell job performs the required data transformation and
generates the processed CSV.

The transformation includes:

-   Removing completely empty rows.
-   Converting `customer_name` values to uppercase.
-   Calculating `discounted_amount` as 90% of `amount`.
-   Writing the transformed data to the destination S3 bucket.

## 2.11 Destination S3 Output

After the Python Shell job completes, the transformed CSV is written to
the CloudFormation-managed destination S3 bucket.

CloudFormation stack also creates the destination S3 bucket where the processed data is
stored.

![CloudFormation Destination S3
Bucket](images/CFN/CFN_Destination_S3_Bucket.png)

``` text
Glue Python Shell
        ↓
Transformation
        ↓
Destination S3
        ↓
output/
        ↓
Processed CSV
```

The CloudFormation workflow execution is shown below.

![Running Glue Workflow](images/CFN/CFN_Running_Glue_Workflow.png)

![CloudFormation Workflow Result](images/CFN/CFN_Workflow_Result.png)

## 2.12 End-to-End CloudFormation Pipeline

The complete automated execution can be summarized as:

``` text
GitHub Repository
        ↓
GitHub Actions
        ↓
GitHub OIDC
        ↓
CloudFormation
        ↓
AWS Infrastructure
        ↓
Upload input/sample.csv
        ↓
Source S3 Bucket
        ↓
S3 ObjectCreated Event
        ↓
Lambda
        ↓
Glue Workflow
        ↓
Glue Crawler
        ↓
Conditional Trigger
        ↓
Glue Python Shell
        ↓
Transformation
        ↓
Destination S3
        ↓
Processed CSV
```

The CloudFormation workflow completes successfully after the CSV is
processed.

![CloudFormation Workflow Result](images/CFN/CFN_Workflow_Result.png)

------------------------------------------------------------------------

## 3. Manual vs CloudFormation Approach

| Aspect | Manual Approach | CloudFormation Approach |
|---|---|---|
| Infrastructure | Created through AWS Console | Defined using CloudFormation |
| Deployment | Manual | GitHub Actions |
| AWS authentication | AWS Console/IAM | GitHub OIDC |
| Input CSV | Manually uploaded to S3 | Uploaded by GitHub Actions |
| Event trigger | S3 → Lambda | S3 → Lambda |
| Orchestration | AWS Glue Workflow | AWS Glue Workflow |
| Transformation | Glue Python Shell | Glue Python Shell |
| Output | Destination S3 | Destination S3 |
| Reproducibility | Lower | Higher |
| CI/CD | Not used | Implemented |

## 4. Architecture Diagram of AWS Activity

![Architecture Diagram](images/AWS_Architecture.drawio.png)



## 5. Challenges Faced

### 1. Manual Approach

1. **Glue Python Shell Script File Error**  
   The Glue Python Shell job initially failed because the configured script file was not available at the specified S3 location.

2. **S3 Permissions for Glue Job**  
   The Glue job required appropriate S3 permissions to access the script stored in the AWS Glue assets bucket.

3. **Glue Workflow Execution Issues**  
   Configuring the crawler, trigger, and Python Shell job to execute in the correct sequence required troubleshooting the workflow dependencies.

4. **S3 Event → Lambda Integration**  
   Configuring the S3 event to invoke Lambda and ensuring Lambda could successfully start the Glue Workflow required troubleshooting across S3, Lambda, and IAM.

---

### 2. CloudFormation Approach

1. **CloudFormation Resource Dependency Issue**  
   The Glue Crawler initially failed because the source S3 bucket was not available when the crawler was created. This was resolved by adding a `DependsOn` dependency.

2. **Glue Crawler IAM Permission Issue**  
   The crawler initially failed with a `glue:GetDatabase` authorization error. Additional AWS Glue Data Catalog permissions were added to the crawler IAM role.

3. **Conditional Trigger Activation Issue**  
   The crawler completed successfully, but the Python Shell job did not start because the conditional trigger remained in the `CREATED` state instead of `ACTIVATED`. The trigger was manually activated to allow the workflow to proceed.

4. **GitHub Actions Authentication Issue**  
   GitHub Actions initially encountered an invalid AWS credentials action reference. This was resolved by updating the `aws-actions/configure-aws-credentials` action to a valid version.


## Conclusion

The **Manual Approach** demonstrates the complete AWS data pipeline when
the infrastructure and input file are managed manually.

The **CloudFormation Approach** converts the infrastructure into code
and integrates it with GitHub Actions and GitHub OIDC. The input CSV is
stored in the GitHub repository and automatically uploaded to the source
S3 bucket as part of the CI/CD workflow. The S3 event then triggers
Lambda, which starts the Glue Workflow and processes the data through
the crawler and Python Shell job.

The two approaches are documented independently, with **Manual
screenshots referenced only from `images/MNL/` and CloudFormation
screenshots referenced only from `images/CFN/`**.
