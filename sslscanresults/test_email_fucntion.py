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
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SSL Labs Analysis Summary Report</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<h1>SSL Labs Analysis Summary Report</h1>
<table class="tftable" border="1">
  <tr>
	<th>#Host</th>
	<th>Grade</th>
	<th>HasWarnings</th>
	<th>Cert Expiry</th>
	<th>Chain Status</th>
	<th>Forward Secrecy</th>
	<th>Heartbeat ext</th>
	<th>Vuln Beast</th>
	<th>Vuln Drown</th>
	<th>Vuln Heartbleed</th>
	<th>Vuln FREAK</th>
	<th>Vuln openSsl Ccs</th>
	<th>Vuln openSSL LuckyMinus20</th>
	<th>Vuln POODLE</th>
	<th>Vuln POODLE TLS</th>
	<th>Support RC4</th>
	<th>RC4 with modern protocols</th>
	<th>RC4 Only</th>
	<th>TLS 1.3</th>
	<th>TLS 1.2</th>
	<th>TLS 1.1</th>
	<th>TLS 1.0</th>
	<th>SSL 3.0 INSECURE</th>
	<th>SSL 2.0 INSECURE</th>
  </tr>
  <tr class="A">
	<td>duckduckgo.com</td>
	<td>A+</td>
	<td>False</td>
	<td>2022-11-26</td>
	<td>none</td>
	<td>Yes (with most browsers) ROBUST</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>Yes</td>
	<td>Yes</td>
	<td>No</td>
	<td>No</td>
	<td>No</td>
	<td>No</td>
  </tr>
  <tr class="B">
	<td>google.com</td>
	<td>B</td>
	<td>False</td>
	<td>2022-05-02</td>
	<td>none</td>
	<td>With modern browsers</td>
	<td>False</td>
	<td>True</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>False</td>
	<td>Yes</td>
	<td>Yes</td>
	<td>Yes</td>
	<td>Yes</td>
	<td>No</td>
	<td>No</td>
  </tr>
</table>
</body>
</html>
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
