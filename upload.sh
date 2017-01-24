#!/bin/sh
set -eu
# Pass the first arg as the function name without file extension
func=$1
# All other args are the names of libraries to include
shift
zip -r9 "$func".zip "$func".py "$@"
aws s3 cp "$func".zip s3://cos-api/"$func.zip"
