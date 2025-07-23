from dotenv import load_dotenv
load_dotenv()

import mdp
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, locale, sys, re


sys.stdout.reconfigure(encoding='utf-8')
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
today = time.strftime("%d %B %Y", time.localtime()).replace(time.strftime("%B"), time.strftime("%B").capitalize())
yesterday = (time.datetime.now() - time.datetime(days=1)).strftime("%d %B %Y").replace((time.datetime.now() - time.datetime(days=1)).strftime("%B"), (time.datetime.now() - time.datetime(days=1)).strftime("%B").capitalize())


def main():
    driver = Driver(uc=True, headless=False)

    try:
        url_login = mdp.Site
        driver.uc_open_with_reconnect(url_login, reconnect_time=6)
        driver.uc_gui_click_captcha()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(mdp.Username)
        driver.find_element(By.ID, "password").send_keys(mdp.Password)
        bouton_connexion = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "kc-login")))
        bouton_connexion.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
        url_offres = mdp.Offres
        driver.get(url_offres)

        try:
            bouton_accepter = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accepter')]")))
            bouton_accepter.click()
            time.sleep(1)

        except:
            pass

        offres_brutes = driver.find_elements(By.CSS_SELECTOR, "div.MuiPaper-root.MuiCard-root.MuiPaper-elevation1")
        offres = [o for o in offres_brutes if "VOIR L'OFFRE" in o.text]
        nos_competences = ["Ingénierie", "Informatique & Web", "Stratégie", "Autre", "Finance"]
        offres_détails = []

        for idx, offre in enumerate(offres, start=1):

            try:
                bouton_voir = offre.find_element(By.XPATH, ".//button[contains(text(), concat('Voir l', \"'\", 'offre'))]")
                bouton_voir.click()
                time.sleep(1)
                titre = driver.find_element(By.CSS_SELECTOR, "h4.MuiTypography-root.MuiTypography-h4.css-jvake7").text.strip()
                description = driver.find_element(By.CSS_SELECTOR, "div.MuiDialogContent-root.css-1ty026z > div > div > div > div > div:nth-child(2)").text.strip()[len("Description\n"):].strip()
                secteurs = [el.strip() for el in driver.find_element(By.CSS_SELECTOR, "div.MuiDialogContent-root.css-1ty026z > div > div > div > div:nth-child(2) > div").text.strip().split("\n") if el.strip()]
                entreprise = driver.find_element(By.CSS_SELECTOR, "div.MuiDialogContent-root.css-1ty026z > div > div > div > div:nth-child(2) > :nth-child(3)").text.strip()
                contact = driver.find_element(By.CSS_SELECTOR, "div.MuiDialogContent-root.css-1ty026z > div > div > div > div:nth-child(2) > :nth-child(6)").text.strip()
                email = driver.find_element(By.CSS_SELECTOR, "div.MuiDialogContent-root.css-1ty026z > div > div > div > div:nth-child(2) > :nth-child(7)").text.strip()
                telephone = driver.find_element(By.CSS_SELECTOR, "div.MuiDialogContent-root.css-1ty026z > div > div > div > div:nth-child(2) > :nth-child(8)").text.strip()
                deadline = driver.find_element(By.CSS_SELECTOR, "div.MuiDialogContent-root.css-1ty026z > div > div > div > div > div > :nth-child(3)").text.strip()
                remuneration = driver.find_elements(By.CSS_SELECTOR, "div.MuiDialogContent-root.css-1ty026z > div > div > div > div > div")[-2].text.strip().rstrip('\n').strip()
                jour = re.search(r"Déposé le (.+)", driver.find_element(By.CSS_SELECTOR, "div.MuiDialogContent-root.css-1ty026z > div > div > div > div > div").text).group(1).strip()

                if jour != today:
                    break

                offre_dict = {"titre": titre, "secteurs": secteurs, "description": description, "entreprise": entreprise, "remuneration": remuneration, "contact": contact, "email": email, "telephone": telephone, "deadline": deadline}

                if [x for x in offre_dict['secteurs'] if x in nos_competences]:
                    offres_détails.append(offre_dict)

                ActionChains(driver).move_by_offset(1, 1).click().perform()
                time.sleep(1)

            except Exception as e:
                print(f"Erreur avec l'offre #{idx} : {e}")

        return offres_détails
    
    finally:
        driver.quit()