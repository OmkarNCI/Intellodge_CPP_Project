import boto3
from django.conf import settings

AWS_REGION = "us-east-1"
sns_client = boto3.client("sns", region_name=AWS_REGION)
# booking confirmation topic arn
TOPIC_ARN = "arn:aws:sns:us-east-1:414333503877:booking_confirmation_topic"

# this function will check guest email is already subscribed in list of subscriptions or not.
def is_email_subscribed(guest_email):
    response = sns_client.list_subscriptions_by_topic(TopicArn=TOPIC_ARN)
    
    for sub in response.get("Subscriptions", []):
        if sub["Endpoint"] == guest_email:
            return True  # Already subscribed
    return False

# subscribe the guest email 
def subscribe_guest_email(guest_email):
    if not is_email_subscribed(guest_email):
        sns_client.subscribe(
            TopicArn=TOPIC_ARN,
            Protocol="email",
            Endpoint=guest_email
        )
        print(f"Subscription request sent to {guest_email}")
    else:
        print(f" {guest_email} is already subscribed.")

# this function will send the message to the subscribers
def publish_booking_confirmation(booking):
    # below of the format for subscription in well format to read the other subscriber.

    guest_email = booking.get("guest_email")
    guest_name = booking.get("guest_name")
    room_number = booking.get("room_number")
    check_in = booking.get("check_in_date")
    check_out = booking.get("check_out_date")

    message_text = (
        f"Hello {guest_name},\n\n"
        f"Your booking has been confirmed at Intellodge.\n\n"
        f"Room Number: {room_number}\n"
        f"Check-In Date: {check_in}\n"
        f"Check-Out Date: {check_out}\n\n"
        f"We look forward to welcoming you!\n"
        f"Warm regards,\n"
        f"Intellodge Team"
    )

    try:
        response = sns_client.publish(
            TopicArn=TOPIC_ARN,
            Subject="Booking Confirmation - Intellodge",
            Message=message_text,
        )
        print("SNS Email Sent. Message ID:", response.get("MessageId"))
        return True
    except Exception as e:
        print("Error sending SNS Email:", e)
        return False
