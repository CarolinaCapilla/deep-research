import types
import sys
from pathlib import Path
import importlib.util as _import_util

# Load the email_agent module directly from file to avoid import issues with top-level app.py
_ROOT = Path(__file__).resolve().parents[1]
_EMAIL_AGENT_PATH = _ROOT / "app" / "email_agent.py"
_spec = _import_util.spec_from_file_location("email_agent", str(_EMAIL_AGENT_PATH))
if _spec and _spec.loader:
    email_agent = _import_util.module_from_spec(_spec)  # type: ignore[assignment]
    _spec.loader.exec_module(email_agent)  # type: ignore[attr-defined]
else:
    raise ImportError(f"Failed to load email_agent.py from {_EMAIL_AGENT_PATH}")


def test_send_email_smtp_success_and_error(monkeypatch):
    # Arrange SMTP env (no SendGrid)
    monkeypatch.setenv("SMTP_SERVER", "smtp.test")
    monkeypatch.setenv("SMTP_PORT", "1025")
    monkeypatch.setenv("FROM_EMAIL", "from@example.com")
    monkeypatch.setenv("TO_EMAIL", "to@example.com")
    monkeypatch.delenv("SENDGRID_API_KEY", raising=False)

    # Fake SMTP client that succeeds
    class FakeSMTPSuccess:
        def __init__(self, host, port, timeout=None):
            assert host == "smtp.test"
            assert int(port) == 1025

        def ehlo(self):
            pass

        def starttls(self):
            pass

        def login(self, u, p):
            pass

        def sendmail(self, a, b, c):
            # success
            return {}

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    # Patch smtplib.SMTP to success
    monkeypatch.setattr(
        email_agent, "smtplib", types.SimpleNamespace(SMTP=FakeSMTPSuccess)
    )

    # Act (success)
    out = email_agent._send_email_impl("Subject", "<b>Hi</b>")

    # Assert (success)
    assert out["status"] == "success"
    assert out["via"] == "smtp"
    assert out["server"] == "smtp.test"
    assert out["port"] == "1025"

    # Now simulate an SMTP error
    class FakeSMTPError(FakeSMTPSuccess):
        def sendmail(self, a, b, c):
            raise RuntimeError("boom")

    monkeypatch.setattr(
        email_agent, "smtplib", types.SimpleNamespace(SMTP=FakeSMTPError)
    )

    out_err = email_agent._send_email_impl("Subject", "<b>Hi</b>")
    assert out_err["status"] == "error"
    assert "SMTP send failed" in out_err.get("reason", "")


def test_send_email_sendgrid_success(monkeypatch):
    # Arrange SendGrid env
    monkeypatch.setenv("SENDGRID_API_KEY", "sg_test_key")
    monkeypatch.delenv("SMTP_SERVER", raising=False)
    monkeypatch.setenv("FROM_EMAIL", "from@example.com")
    monkeypatch.setenv("TO_EMAIL", "to@example.com")

    # Create a fake sendgrid module with expected shapes
    class FakeResponse:
        status_code = 202

    class FakeClient:
        def __init__(self, api_key):
            assert api_key == "sg_test_key"

        def send(self, mail):
            return FakeResponse()

    # Fake helpers.mail submodule
    helpers_mail = types.SimpleNamespace()

    class Email:
        def __init__(self, addr):
            self.addr = addr

    class To:
        def __init__(self, addr):
            self.addr = addr

    class Content:
        def __init__(self, typ, body):
            self.typ = typ
            self.body = body

    class Mail:
        def __init__(self, email_from, email_to, subject, content):
            self.email_from = email_from
            self.email_to = email_to
            self.subject = subject
            self.content = content

    helpers_mail.Email = Email
    helpers_mail.To = To
    helpers_mail.Content = Content
    helpers_mail.Mail = Mail

    fake_sendgrid = types.SimpleNamespace(SendGridAPIClient=FakeClient)

    # Inject into sys.modules so imports succeed
    monkeypatch.setitem(sys.modules, "sendgrid", fake_sendgrid)
    monkeypatch.setitem(sys.modules, "sendgrid.helpers", types.SimpleNamespace())
    monkeypatch.setitem(sys.modules, "sendgrid.helpers.mail", helpers_mail)

    # Act
    out = email_agent._send_email_impl("Subject", "<b>Hi</b>")

    # Assert
    assert out["status"] == "success"
    assert out["via"] == "sendgrid"
    assert out["code"] == "202"


def test_send_email_no_config_skipped(monkeypatch):
    # Ensure neither SendGrid nor SMTP is configured
    monkeypatch.delenv("SENDGRID_API_KEY", raising=False)
    monkeypatch.delenv("SMTP_SERVER", raising=False)
    monkeypatch.delenv("SMTP_PORT", raising=False)

    out = email_agent._send_email_impl("S", "<i>x</i>")
    assert out["status"] == "skipped"
    assert "No SENDGRID_API_KEY or SMTP_SERVER" in out.get("reason", "")
