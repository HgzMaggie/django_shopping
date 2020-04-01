import hashlib

from AXF01.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT
from django.core.mail import send_mail
from django.template import loader


def hash_str(source):
    hashlib.new("sha512", source.encode('utf-8')).hexdigest()


def send_email_activate(username, receive, u_token):
    subject = "%s 生鲜商城-注册激活" % username
    from_email = EMAIL_HOST_USER
    recipient_list = [receive, ]

    data = {
        "username": username,
        "activate_url": "http://{}:{}/axf/activate/?u_token={}".format(SERVER_HOST, SERVER_PORT, u_token),
    }
    html_msg = loader.get_template("user/activate.html").render(data)

    send_mail(subject=subject, message='', html_message=html_msg, from_email=from_email, recipient_list=recipient_list)

