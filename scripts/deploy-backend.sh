# package code and upload artifact to S3
sam package --template-file template.yml --s3-bucket serverless-signup-packages --output-template-file template-packaged.yml --region eu-west-1

# deploy artifact
sam deploy --template-file template-packaged.yml --stack-name serverless-signup-python --capabilities CAPABILITY_IAM --region eu-west-1

ENDPOINT=$(aws cloudformation describe-stacks --stack-name serverless-signup-python --query 'Stacks[0].Outputs[?OutputKey==`Endpoint`].OutputValue' --output text)

echo $ENDPOINT