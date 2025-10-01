import os
from typing import Dict

from agents import Agent, function_tool

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send an email with the given subject and HTML body. Lazily imports SendGrid and skips when missing. """
    api_key = os.environ.get('SENDGRID_API_KEY')
    if not api_key:
        return {"status": "skipped", "reason": "SENDGRID_API_KEY not set"}

    try:
        import sendgrid  # type: ignore
        from sendgrid.helpers.mail import Email, Mail, Content, To  # type: ignore
    except Exception as e:
        return {"status": "skipped", "reason": f"SendGrid not available: {e}"}

    from_email = Email(os.environ.get("FROM_EMAIL", "noreply@example.com"))
    to_email = To(os.environ.get("TO_EMAIL", "recipient@example.com"))
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content)
    sg = sendgrid.SendGridAPIClient(api_key=api_key)
    response = sg.send(mail)
    return {"status": "success", "code": str(response.status_code)}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
