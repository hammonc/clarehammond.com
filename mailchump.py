from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
import re
import smtplib
import sys

import AddressBook as ab
import html2text
import premailer

if len(sys.argv) != 3 or sys.argv[1] not in ['--test', '--real']:
    print 'Usage: ./mailchump.py --[test|real] <newsletter-datestamp>'
    exit(1)

is_test = (sys.argv[1] == '--test')
newsletter_datestamp = sys.argv[2]

with open('_site/newsletter-{}.html'.format(newsletter_datestamp)) as f:
    raw_html = f.read()

host = 'email-smtp.eu-west-1.amazonaws.com'
port = 587

with open('credentials.json') as f:
    credentials = json.load(f)

smtp_username = credentials['SES_SMTP_USERNAME']
smtp_password = credentials['SES_SMTP_PASSWORD']
test_email_address = credentials['TEST_EMAIL_ADDRESS']

subject = re.search(r'<title>(.*?)<\/title>', raw_html).group(1)

text_maker = html2text.HTML2Text()
text_maker.ignore_images = True
text_maker.ignore_emphasis = True
text_maker.body_width = 0
raw_text = text_maker.handle(raw_html)
text = re.sub(r'\[(?P<text>.*?)\]\((?P<url>.*?)\)', r'\g<text> <\g<url>>', raw_text)

html = premailer.transform(raw_html)

smtp = smtplib.SMTP(host, port)
smtp.ehlo() 
smtp.starttls()
smtp.ehlo()
smtp.login(smtp_username, smtp_password)

if is_test:
    addrs = [test_email_address]
else:
    address_book = ab.ABAddressBook.sharedAddressBook()
    for group in address_book.groups():
        if group.name() == '*A Newsletter':
            break
    else:
        print 'Could not load address book group!'
        exit(2)

    addrs = []

    for member in group.members():
        first = member.valueForProperty_('First')
        last = member.valueForProperty_('Last')
        name = u'{} {}'.format(first, last).strip()

        email = member.valueForProperty_('Email')

        if email is None or email.count() == 0:
            print u'No address found for {}'.format(name)
            continue
        elif email.count() > 1:
            print u'Multiple addresses found for {}'.format(name)

        addrs.append(email.valueAtIndex_(0))


print 'About to send to {} addresses'.format(len(addrs))
print 'Are you sure? (y/n)'

answer = raw_input()
if answer != 'y':
    print 'Aborting!'
    exit()

for addr in addrs:
    msg = MIMEMultipart('alternative')

    msg['Subject'] = subject
    msg['From'] = 'Clare Hammond <info@clarehammond.com>'
    msg['To'] = addr

    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    print('sending to {}'.format(addr))
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
