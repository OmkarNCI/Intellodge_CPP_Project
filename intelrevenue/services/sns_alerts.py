#Here we are sending the low occupancy & revenue drop alerts email to the admin users.

import boto3
from intellodge_core.logger import get_logger
from revenue_services import RevenueService 

logger = get_logger(__name__)
sns = boto3.client("sns", region_name="us-east-1")

LOW_OCC_TOPIC_ARN = "arn:aws:sns:us-east-1:414333503877:low-occupancy-alert"
REV_DROP_TOPIC_ARN = "arn:aws:sns:us-east-1:414333503877:revenue-drop-alert"


# this will publish the email to the subscriber
def publish_email(topic_arn: str, subject: str, message: str):
    try:
        resp = sns.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
        logger.info(f"SNS Email Published → {topic_arn}")
        return resp
    except Exception as e:
        logger.error(f"Failed to send SNS email: {e}")
        raise

# Below is the alert service class which contains main alert logic
class AlertService:
    def __init__(self, revenue_service):
        self.rev = revenue_service

    # Low Occupancy Alert
    def send_low_occupancy_alert(self, threshold=30):
        occupancy = self.rev.occupancy_rate()

        if occupancy < threshold:
            subject = "Intellodge Alert: Low Occupancy Warning"
            message = (
            f"LOW OCCUPANCY ALERT\n"
            f"\n\n"
            f"Dear Intellodge Administrator,\n\n"
            f"Our monitoring system has detected 'low occupancy levels' "
            f"at our Intellodge Hotel.\n\n"

            f"- Current Status of this month \n"
            f"- Current Occupancy: {occupancy}% \n"
            f"- Alert Threshold: {threshold}% \n\n"
            f" Please take some actions as soon as posible to improve our occupancy rate...!! \n\n"
    
            f"Regards,\n"
            f"Intellodge Automated Alert System"
            )
            
            
            publish_email(
                LOW_OCC_TOPIC_ARN,
                subject,
                message,
            )
            return {"success": True, "occupancy": occupancy}
            
        return {"success": False, "occupancy": occupancy}

    # Revenue Drop Alert
    def send_revenue_drop_alert(self, drop_threshold=20):
        monthly = self.rev.revenue_by_month()
        
        if len(monthly) < 2:
            return {"success": False, "reason": "Not enough revenue data"}

        prev = monthly[-2]
        current = monthly[-1]
        
        if prev <= 0:
            return {"success": False, "reason": "Invalid previous revenue"}

        drop = ((prev - current) / prev) * 100

        if drop >= drop_threshold:
            subject = "Intellodge Alert: Revenue Drop Detected"
            message = (
                f" REVENUE DROP ALERT\n "
                f"\n\n"
                f"Dear Intellodge Administrator,\n\n"
                f"Our analytics system has identified a significant revenue decline this month. "
                f"\n\n"
    
                f" Revenue Summary \n"
                f"- Previous Month Revenue: ${prev} \n"
                f"- Current Month Revenue: ${current} \n"
                f"- Total Drop: {drop:.2f}% \n"
                f"- Alert Threshold: **{drop_threshold}%**\n\n"
                f" Please take some actions as soon as posible....!! \n"

                f"Regards,\n"
                f"Intellodge Automated Alert System"
            )

            publish_email(REV_DROP_TOPIC_ARN, subject, message)

            return {
                "success": True,
                "drop_percentage": round(drop, 2),
                "prev": prev,
                "current": current,
            }
        return {"success": False, "drop_percentage": round(drop, 2)}


if __name__ == "__main__":
    rev = RevenueService()
    alerts = AlertService(rev)

    alerts.send_low_occupancy_alert()
    alerts.send_revenue_drop_alert()
