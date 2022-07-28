import smtplib, ssl
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "manoj.cis114@gmail.com"
receiver_email = "manoj.cis@gmail.com"
password = "xsijsknfwvukhgnw"

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""
html = """\
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Host</th>
      <th>HasWarnings</th>
      <th>Grade</th>
      <th>Cert Expiry</th>
      <th>Chain Status</th>
      <th>Forward Secrecy</th>
      <th>Heartbeat ext</th>
      <th>Support RC4</th>
      <th>RC4 Only</th>
      <th>RC4 with modern protocols</th>
      <th>Vuln Drown</th>
      <th>Vuln FREAK</th>
      <th>Vuln Beast</th>
      <th>Vuln Heartbleed</th>
      <th>Vuln POODLE</th>
      <th>Vuln POODLE TLS</th>
      <th>Vuln openSsl Ccs</th>
      <th>Vuln openSSL LuckyMinus20</th>
      <th>SSL 2.0 INSECURE</th>
      <th>SSL 3.0 INSECURE</th>
      <th>TLS 1.0</th>
      <th>TLS 1.1</th>
      <th>TLS 1.2</th>
      <th>TLS 1.3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>google.com</td>
      <td>False</td>
      <td>B</td>
      <td>12/11/24</td>
      <td>none</td>
      <td>FS is achieved with modern clients</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>No</td>
      <td>No</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>
"""

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
