import os
import smtplib
from flask import Flask, render_template, url_for, request, redirect
from email.message import EmailMessage
from string import Template
from pathlib import Path

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(f'{page_name}.html')


def send_email(data):
    html = Template(Path('./templates/emailIndex.html').read_text())
    email = EmailMessage()
    email['from'] = data['email']
    email['to'] = os.environ['TO_GMAIL']
    email['subject'] = data['subject']
    email.set_content(html.substitute(
        {'message': data['message'], 'from': data['email']}), 'html')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(os.environ['GMAIL'], os.environ['GMAIL_PASSWORD'])
        smtp.send_message(email)
        print('Email Sent')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            send_email(data)
            return redirect('/thankyou')
        except Exception as e:
            print(e)
            return redirect('/sorry')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
