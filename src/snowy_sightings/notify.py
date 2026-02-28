"""Email notifications via Resend."""

import os

import resend


def send_email(to: str, subject: str, body_html: str) -> dict:
    """Send an email via Resend."""
    resend.api_key = os.environ["RESEND_API_KEY"]
    from_addr = os.environ.get("RESEND_FROM", "snowy@resend.dev")
    return resend.Emails.send(
        {"from": from_addr, "to": to, "subject": subject, "html": body_html}
    )
