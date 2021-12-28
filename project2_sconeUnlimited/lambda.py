{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "import boto3\n",
    "import base64\n",
    "\n",
    "s3 = boto3.client('s3')\n",
    "\n",
    "def lambda_handler(event, context):\n",
    "    \"\"\"A function to serialize target data from S3\"\"\"\n",
    "\n",
    "    # Get the s3 address from the Step Function event input\n",
    "    key = event[s3_key]\n",
    "    bucket = event[s3_bucket]\n",
    "\n",
    "    # Download the data from s3 to /tmp/image.png\n",
    "    ## TODO: fill in\n",
    "    s3.download_file(bucket,key,\"/tmp/image.png\")\n",
    "    # We read the data from a file\n",
    "    with open(\"/tmp/image.png\", \"rb\") as f:\n",
    "        image_data = base64.b64encode(f.read())\n",
    "\n",
    "    # Pass the data back to the Step Function\n",
    "    print(\"Event:\", event.keys())\n",
    "    return {\n",
    "        'statusCode': 200,\n",
    "        'body': {\n",
    "            \"image_data\": image_data,\n",
    "            \"s3_bucket\": bucket,\n",
    "            \"s3_key\": key,\n",
    "            \"inferences\": []\n",
    "        }\n",
    "    }"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "import boto3\n",
    "import base64\n",
    "import os\n",
    "import io\n",
    "# Fill this in with the name of your deployed model\n",
    "ENDPOINT = \"image-classification-2021-12-26-11-51-07-610\"\n",
    "runtime = boto3.client('runtime.sagemaker')\n",
    "def lambda_handler(event, context):\n",
    "    # Decode the image data\n",
    "    image = base64.b64decode(event[\"body\"][\"image_data\"])\n",
    "    # Instantiate a Predictor\n",
    "    response = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType=\"image/png\", Body = image)\n",
    "    # For this model the IdentitySerializer needs to be \"image/png\"\n",
    "    # Make a prediction:\n",
    "    inferences = response[\"Body\"].read()\n",
    "    # We return the data back to the Step Function\n",
    "    event[\"inferences\"] = inferences.decode('utf-8')\n",
    "    return {\n",
    "        'statusCode': 200,\n",
    "        'body': json.dumps(event)\n",
    "    }"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "THRESHOLD = .93\n",
    "def lambda_handler(event, context):\n",
    "    # Grab the inferences from the event\n",
    "    inferences = event[\"inferences\"]\n",
    "    # Check if any values in our inferences are above THRESHOLD\n",
    "    for i in range(len(inferences)):\n",
    "        meets_threshold = i > THRESHOLD\n",
    "    # If our threshold is met, pass our data back out of the\n",
    "    # Step Function, else, end the Step Function with an error\n",
    "    if meets_threshold:\n",
    "        pass\n",
    "    else:\n",
    "        raise(\"THRESHOLD_CONFIDENCE_NOT_MET\")\n",
    "    return {\n",
    "        'statusCode': 200,\n",
    "        'body': json.dumps(event)\n",
    "    }"
   ]
  }
 ],
 "metadata": {
  "instance_type": "ml.t3.medium",
  "kernelspec": {
   "display_name": "Python 3 (Data Science)",
   "language": "python",
   "name": "python3__SAGEMAKER_INTERNAL__arn:aws:sagemaker:us-east-1:081325390199:image/datascience-1.0"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
