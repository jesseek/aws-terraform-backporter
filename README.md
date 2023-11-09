# Sample scripts for 'backporting' existing AWS infrastructure into Terraform
Collection of scripts for backporting existing AWS infrastructure into Terraform
using AWS SDK for Python (`boto3`)


## Requirements

These scripts depend on `boto3` and requirePython. You can install `boto3` using pip:

    pip install boto3

## Basic Configuration

You need to set up your AWS security credentials before the sample code is able
to connect to AWS. You can do this by creating a file named "credentials" at ~/.aws/ 
(`C:\Users\USER_NAME\.aws\` for Windows users) and saving the following lines in the file:

    [profile_name]
    aws_access_key_id = <your access key id>
    aws_secret_access_key = <your secret key>

## Running the CGW (Customer Gateway) Example

This sample application connects to Amazon's [Simple Storage Service (S3)](http://aws.amazon.com/s3),
creates a bucket, and uploads a file to that bucket. The script will generate a
bucket name and file for you. All you need to do is run the code:

This example script generates the terraform import statement and terraform code for managing an existing
AWS Customer Gateway with terraform. Usage:
    update the `my_profile` and `my_region` variable in the script to match the profile_name in your 
    AWS configuration file.

    python cgw_example.py

## License

This sample application is distributed under the
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).