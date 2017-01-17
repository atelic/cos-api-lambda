# Lambda functions for osf.io API tasks.

## Setup

```bash
$ pip install -r requirements.txt -t .
```

## Deploy to Lambda
* Zip function and required libraries
```bash
$  zip -r9 $function_name.zip $function_name.py requests whatever_library
$ aws s3 cp $function_name.zip s3://cos-api/$function_name.zip
```
* Point the Lambda function to the uploaded zip file

  * **Lambda** > **Functions** > **$function_name** > **Upload file from Amazon S3**
  * Copy the https://s3-us-west-2.amazonaws.com/cos-api/$function_name.zip into the input.
