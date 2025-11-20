import boto3
from botocore.exceptions import ClientError

AWS_REGION = "us-east-1"
TOPIC_NAME = "booking_confirmation_topic"

def create_sns_topic(topic_name=TOPIC_NAME, region=AWS_REGION):
    """
    Create an SNS topic and return its ARN.
    """
    sns_client = boto3.client("sns", region_name=region)
    try:
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response["TopicArn"]
        print(f"Topic '{topic_name}' created successfully. ARN: {topic_arn}")
        return topic_arn
    except ClientError as e:
        print(f"Error creating topic '{topic_name}': {e}")
        return None

if __name__ == "__main__":
    result = create_sns_topic()
    print(result)
