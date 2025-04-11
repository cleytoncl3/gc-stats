import os
import zipfile
import requests
import re
import streamlit as st
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROMEDRIVER_VERSION = "120.0.6099.71"
CHROMEDRIVER_URL = f"https://storage.googleapis.com/chrome-for-testing-public/{CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip"

def install_chromedriver():
    try:
        response = requests.get(CHROMEDRIVER_URL)
        response.raise_for_status()
        with open("chromedriver.zip", "wb") as f:
            f.write(response.content)

        with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
            zip_ref.extractall()

        os.rename("chromedriver-linux64/chromedriver", "chromedriver")
        os.chmod("chromedriver", 0o755)
        print(Fore.GREEN + "[✓] ChromeDriver instalado com sucesso." + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"[x] Erro ao baixar o ChromeDriver: {e}" + Style.RESET_ALL)
        raise e

def get_driver():
    if not os.path.exists("chromedriver"):
        install_chromedriver()

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = "/usr/bin/chromium"

    service = Service("./chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def buscar_perfil(link):
    try:
        driver = get_driver()
        driver.get(link)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "player-general-info"))
        )
        nome = driver.find_element(By.CLASS_NAME, "player-general-info").text
        driver.quit()
        return nome
    except Exception as e:
        print(Fore.RED + f"[x] Erro ao carregar perfil: {e}" + Style.RESET_ALL)
        st.exception(e)  # Exibe o erro no Streamlit também
        return None

st.set_page_config(page_title="GC Stats do Vintorez", layout="centered")
st.title("🔥 GC Stats do Vintorez")

link = st.text_input("Cole o link do perfil da GamersClub:")

if link:
    nome = buscar_perfil(link)
    if nome:
        st.success(f"Perfil encontrado: {nome}")
    else:
        st.error("Erro ao carregar perfil.")
