
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

mail = Mail(app)

def send_async(user, confirm_email):
	msg = Message(
		"Locale-Please Confirm Your Email",
		sender="donotreply@demo.com",
		recipients=[user.email],
		html=confirm_email,
		body = f"Welcome to Locale. Your account with username {user.username} has been successfully created.\n"
			"Please confirm your email address by clicking the link below."
			f"<a href={confirm_email}>Confirm Email</a>"
			"<br>"
			"<p>Thank you for using Locale.</p>"
	)
	
def send_reset_email(email, reset_token):
	msg = Message(
		"Locale-Password Reset Request",
		sender="donotreply@demo.com",
		recipients=[email],
		html=f"Please click the link below to reset your password.\n"
    )

	with app.app_context():
		mail.send(msg)