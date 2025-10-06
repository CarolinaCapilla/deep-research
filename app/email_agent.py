import os
import smtplib
from typing import Dict
from email.mime.text import MIMEText

from agents import Agent, function_tool


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Send an email with the given subject and HTML body.

    Priority:
    1) SendGrid if SENDGRID_API_KEY is set
    2) SMTP if SMTP_SERVER is set (works with MailHog/Mailtrap or real SMTP)
    Otherwise: skip.
    """
    from_email = os.environ.get("FROM_EMAIL", "noreply@example.com")
    to_email = os.environ.get("TO_EMAIL", "recipient@example.com")

    # Path 1: SendGrid
    sg_api_key = os.environ.get("SENDGRID_API_KEY")
    if sg_api_key:
        try:
            import sendgrid  # type: ignore
            from sendgrid.helpers.mail import Email, Mail, Content, To  # type: ignore
        except Exception as e:
            return {"status": "skipped", "reason": f"SendGrid not available: {e}"}

        mail = Mail(
            Email(from_email), To(to_email), subject, Content("text/html", html_body)
        )
        sg = sendgrid.SendGridAPIClient(api_key=sg_api_key)
        response = sg.send(mail)
        return {
            "status": "success",
            "code": str(response.status_code),
            "via": "sendgrid",
        }

    # Path 2: SMTP (MailHog/Mailtrap/real SMTP)
    smtp_server = os.environ.get("SMTP_SERVER")
    if smtp_server:
        smtp_port = int(os.environ.get("SMTP_PORT", "1025"))  # MailHog default: 1025
        smtp_user = os.environ.get("SMTP_USERNAME")
        smtp_pass = os.environ.get("SMTP_PASSWORD")
        use_starttls = os.environ.get("SMTP_STARTTLS", "0") not in (
            "",
            "0",
            "false",
            "False",
        )

        msg = MIMEText(html_body, "html")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        try:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
                server.ehlo()
                if use_starttls:
                    try:
                        server.starttls()
                        server.ehlo()
                    except Exception:
                        # Continue without TLS if not supported
                        pass
                if smtp_user and smtp_pass:
                    server.login(smtp_user, smtp_pass)
                server.sendmail(from_email, [to_email], msg.as_string())
            return {
                "status": "success",
                "via": "smtp",
                "server": smtp_server,
                "port": str(smtp_port),
            }
        except Exception as e:
            return {"status": "error", "reason": f"SMTP send failed: {e}"}

    # Neither SendGrid nor SMTP configured
    return {
        "status": "skipped",
        "reason": "No SENDGRID_API_KEY or SMTP_SERVER configured",
    }


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
