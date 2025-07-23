from email.mime.text import MIMEText
import captcha, smtplib, mdp
from dotenv import load_dotenv
load_dotenv()

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_FROM = mdp.Email_from
EMAIL_PASSWORD = mdp.Email_password

EMAIL_TO_LIST = mdp.Email_to_list

subject = 'Nouvelles missions'
missions = captcha.main()
body = ""

if len(missions) > 0:
    for mission in missions:
        for key in mission.keys():
            if key == "secteurs":
                body += f"<b>{key.upper()}</b>: {', '.join(mission.get('secteurs', []))}<hr style='border:1px solid #000; margin:10px 0;'>"
            else:
                body += f"<b>{key.upper()}</b>: {str(mission[key])}<hr style='border:1px solid #000; margin:10px 0;'>"
        body += f"<hr style='border:5px solid red; margin:60px 0; opacity: 0.7;'>"


else:
    body = "Pas de nouvelles missions aujourd'hui"

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)

        for email_to in EMAIL_TO_LIST:
            msg = MIMEText(body, 'html')
            msg['Subject'] = subject
            msg['From'] = EMAIL_FROM
            msg['To'] = email_to

            server.sendmail(EMAIL_FROM, email_to, msg.as_string())
except Exception as e:
    print("Erreur lors de l'envoi :", e)