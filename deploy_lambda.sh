#!/bin/bash

# Define variables
LAMBDA_FUNCTION_NAME="PolitiMeldingerBot"  # Replace with your actual Lambda function name
PACKAGE_DIR="package"
ZIP_FILE="lambda_function.zip"
REQUIREMENTS_FILE="requirements.txt"

# Step 1: Clean up old package and zip file
echo "Cleaning up old package and zip file..."
rm -rf $PACKAGE_DIR $ZIP_FILE

# Step 2: Install dependencies
echo "Installing dependencies..."
mkdir -p $PACKAGE_DIR
pip install -r $REQUIREMENTS_FILE -t ./$PACKAGE_DIR

# Step 3: Create the deployment package
echo "Creating deployment package..."
cd $PACKAGE_DIR
zip -r ../$ZIP_FILE .
cd ..
zip -g $ZIP_FILE PolitiMeldingerBot.py PolitiloggAPI.py Storage.py XAPI.py police_tweet_map.json

# Step 4: Update the Lambda function
echo "Updating Lambda function..."
aws lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME --zip-file fileb://$ZIP_FILE

# Step 5: Clean up
echo "Cleaning up..."
rm -rf $PACKAGE_DIR $ZIP_FILE

echo "Deployment complete!"