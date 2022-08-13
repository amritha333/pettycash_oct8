
# import requests
# response = requests.get(f'https://ipapi.co/1.39.78.40/json/').json()
# location_data = {
#         "ip": '103.70.199.235',
#         "city": response.get("city"),
#         "region": response.get("region"),
#         "country": response.get("country_name")
# }

# print("location data:::::")
# print(response)


# import smtplib as smtp

# connection = smtp.SMTP_SSL('smtp.gmail.com', 465)
    
# email_addr = 'amrithakumar34@gmail.com'
# email_passwd = 'uehxynftlsmrvuly'
# connection.login(email_addr, email_passwd)

# connection.sendmail(from_addr=email_addr, to_addrs='amarnathnambiar79@gmail.com', msg="Your Otp is 9555555")
# connection.close()




import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content('your otp is 88888')

msg['Subject'] = 'Subject'
msg['From'] = "amrithakumar34@gmail.com"
msg['To'] = "anilkumart3333@gmail.com"

# Send the message via our own SMTP server.
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("amrithakumar34@gmail.com", "uehxynftlsmrvuly")
server.send_message(msg)
server.quit()
# print(location_data)