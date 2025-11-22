import boto3

sns = boto3.client("sns", region_name="us-east-1")

LOW_OCC_TOPIC_ARN = "arn:aws:sns:us-east-1:414333503877:low-occupancy-alert"
REV_DROP_TOPIC_ARN = "arn:aws:sns:us-east-1:414333503877:revenue-drop-alert"

email = "omkarjakkulwar78@gmail.com"

def setup_subscriptions():
    sns.subscribe(TopicArn=LOW_OCC_TOPIC_ARN, Protocol="email", Endpoint=email)
    sns.subscribe(TopicArn=REV_DROP_TOPIC_ARN, Protocol="email", Endpoint=email)
    print("Confirmation emails sent. Check your inbox.")

if __name__ == "__main__":
    setup_subscriptions()