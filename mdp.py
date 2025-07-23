import os

Site = os.getenv("KIWIX_SITE")
Username = os.getenv("KIWIX_USERNAME")
Password = os.getenv("KIWIX_PASSWORD")
Email_from = os.getenv("KIWIX_EMAIL_FROM")
Email_password = os.getenv("KIWIX_EMAIL_PASSWORD")
Email_to_list = os.getenv("KIWIX_EMAIL_TO_LIST", "").split(",")
Offres = os.getenv("KIWIX_OFFRES")