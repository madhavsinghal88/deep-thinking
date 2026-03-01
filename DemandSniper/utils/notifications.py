import json
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
import httpx
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template

from config.loader import load_scoring_config
from config.settings import settings


class NotificationManager:
    """Manages notifications via webhooks and email."""
    
    def __init__(self):
        self.config = load_scoring_config()
        self.notification_config = self.config.get("notifications", {})
    
    async def notify(self, event_type: str, data: Dict[str, Any]) -> bool:
        """Send notification based on event type and configuration."""
        if not self.notification_config.get("enabled", False):
            return False
        
        success = True
        
        # Check webhook
        webhook_config = self.notification_config.get("webhook", {})
        if webhook_config.get("url"):
            webhook_success = await self._send_webhook(event_type, data, webhook_config)
            success = success and webhook_success
        
        # Check email
        email_config = self.notification_config.get("email", {})
        if email_config.get("enabled", False):
            email_success = await self._send_email(event_type, data, email_config)
            success = success and email_success
        
        return success
    
    async def _send_webhook(
        self, 
        event_type: str, 
        data: Dict[str, Any],
        webhook_config: Dict[str, Any]
    ) -> bool:
        """Send webhook notification."""
        url = webhook_config.get("url")
        headers = webhook_config.get("headers", {})
        
        if not url:
            return False
        
        payload = self._format_webhook_payload(event_type, data)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )
                return response.status_code in [200, 201, 204]
        except Exception as e:
            print(f"Webhook notification failed: {e}")
            return False
    
    def _format_webhook_payload(
        self, 
        event_type: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format webhook payload based on event type."""
        company_name = data.get("company_name", "Unknown")
        demand_score = data.get("demand_score", 0)
        priority = data.get("priority_tag", "Low")
        
        if event_type == "demand_threshold_crossed":
            return {
                "text": f"🎯 High Priority Alert: {company_name}",
                "attachments": [{
                    "color": "danger",
                    "fields": [
                        {"title": "Company", "value": company_name, "short": True},
                        {"title": "Demand Score", "value": str(demand_score), "short": True},
                        {"title": "Priority", "value": priority, "short": True},
                        {"title": "Total Openings", "value": str(data.get("total_openings", "N/A")), "short": True}
                    ]
                }]
            }
        elif event_type == "new_high_priority_company":
            return {
                "text": f"🆕 New High Priority Company: {company_name}",
                "attachments": [{
                    "color": "warning",
                    "fields": [
                        {"title": "Company", "value": company_name, "short": True},
                        {"title": "Demand Score", "value": str(demand_score), "short": True},
                        {"title": "First Seen", "value": str(data.get("first_seen_date", "N/A")), "short": True}
                    ]
                }]
            }
        elif event_type == "significant_demand_spike":
            return {
                "text": f"📈 Demand Spike: {company_name}",
                "attachments": [{
                    "color": "good",
                    "fields": [
                        {"title": "Company", "value": company_name, "short": True},
                        {"title": "Previous Score", "value": str(data.get("previous_score", "N/A")), "short": True},
                        {"title": "Current Score", "value": str(demand_score), "short": True},
                        {"title": "Increase", "value": f"+{data.get('score_increase', 0)}", "short": True}
                    ]
                }]
            }
        else:
            return {
                "text": f"DemandSniper Alert: {event_type}",
                "data": data
            }
    
    async def _send_email(
        self, 
        event_type: str, 
        data: Dict[str, Any],
        email_config: Dict[str, Any]
    ) -> bool:
        """Send email notification."""
        if not settings.SMTP_HOST:
            print("SMTP not configured")
            return False
        
        recipients = email_config.get("recipients", [])
        if not recipients:
            return False
        
        subject_template = email_config.get(
            "subject_template", 
            "[DemandSniper] Alert: {company_name}"
        )
        
        subject = subject_template.format(
            priority=data.get("priority_tag", "Low"),
            company_name=data.get("company_name", "Unknown")
        )
        
        body = self._format_email_body(event_type, data)
        
        try:
            msg = MIMEMultipart()
            msg["From"] = settings.SMTP_FROM_EMAIL
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))
            
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                use_tls=True
            )
            return True
        except Exception as e:
            print(f"Email notification failed: {e}")
            return False
    
    def _format_email_body(self, event_type: str, data: Dict[str, Any]) -> str:
        """Format email HTML body."""
        template = Template("""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>DemandSniper Alert</h2>
            <p><strong>Event:</strong> {{ event_type }}</p>
            <hr>
            <h3>Company: {{ data.company_name }}</h3>
            <table style="border-collapse: collapse; width: 100%;">
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Demand Score</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{{ data.demand_score }}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Priority</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{{ data.priority_tag }}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Total Openings</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{{ data.total_openings }}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>First Seen</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{{ data.first_seen_date }}</td>
                </tr>
            </table>
            <hr>
            <p style="color: #666; font-size: 12px;">
                Generated by DemandSniper on {{ timestamp }}
            </p>
        </body>
        </html>
        """)
        
        return template.render(
            event_type=event_type,
            data=data,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )


# Global notification manager instance
notification_manager = NotificationManager()


async def send_notification(event_type: str, data: Dict[str, Any]) -> bool:
    """Convenience function to send notifications."""
    return await notification_manager.notify(event_type, data)


async def check_and_notify_triggers(
    job_data: Dict[str, Any],
    previous_score: Optional[float] = None
) -> None:
    """Check notification triggers and send alerts if conditions met."""
    config = load_scoring_config()
    triggers = config.get("notifications", {}).get("triggers", [])
    
    demand_score = job_data.get("demand_score", 0)
    priority_tag = job_data.get("priority_tag", "Low")
    
    for trigger in triggers:
        if not trigger.get("enabled", False):
            continue
        
        trigger_name = trigger.get("name", "")
        threshold = trigger.get("threshold", 0)
        
        if trigger_name == "demand_threshold_crossed":
            if demand_score >= threshold:
                await send_notification("demand_threshold_crossed", job_data)
        
        elif trigger_name == "new_high_priority_company":
            if priority_tag == "High" and previous_score is None:
                await send_notification("new_high_priority_company", job_data)
        
        elif trigger_name == "significant_demand_spike":
            if previous_score is not None:
                score_increase = demand_score - previous_score
                if score_increase >= threshold:
                    job_data["previous_score"] = previous_score
                    job_data["score_increase"] = score_increase
                    await send_notification("significant_demand_spike", job_data)
