import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import zipfile
import requests
import re

CHROMEDRIVER_VERSION = "120.0.6099.71"
CHROMEDRIVER_URL = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip"
CHROMEDRIVER_ZIP_PATH = "chromedriver.zip"
CHROMEDRIVER_EXTRACTED_FOLDER = "chromedriver-linux64"
CHROMEDRIVER_BINARY = os.path.join(CHROMEDRIVER_EXTRACTED_FOLDER, "chromedriver")

def install_chromedriver():
    if os.path.exists(CHROMEDRIVER_BINARY):
        return
    try:
        r = requests.get(CHROMEDRIVER_URL)
        r.raise_for_status()
        with open(CHROMEDRIVER_ZIP_PATH, "wb") as f:
            f.write(r.content)
        with zipfile.ZipFile(CHROMEDRIVER_ZIP_PATH, "r") as zip_ref:
            zip_ref.extractall(".")
        os.remove(CHROMEDRIVER_ZIP_PATH)
    except Exception as e:
        raise RuntimeError(f"Erro ao baixar o ChromeDriver: {e}")

def start_browser():
    install_chromedriver()
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.binary_location = "/usr/bin/chromium"

    service = Service(CHROMEDRIVER_BINARY)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def extrair_stats(url):
    try:
        driver = start_browser()
        profile_url = f"https://gamersclub.gg/player/{url}"
        driver.get(profile_url)
        time.sleep(5)

        html = driver.page_source
        stats = {}
        padrao = r'{"label":"(.*?)","value":"(.*?)"}'
        matches = re.findall(padrao, html)
        for label, value in matches:
            stats[label] = value
        driver.quit()
        return stats
    except Exception as e:
        return {"erro": str(e)}

# Interface Streamlit
st.set_page_config(page_title="GC Stats do Vintorez", layout="centered", page_icon="🎯")

st.markdown("<h1 style='text-align: center;'>🎯 GC Stats do Vintorez</h1>", unsafe_allow_html=True)
st.markdown("Cole o link do perfil da **GamersClub**:")

url_input = st.text_input("URL do perfil", placeholder="Ex: 2399445")
if url_input:
    with st.spinner("Buscando stats..."):
        stats = extrair_stats(url_input)
    if "erro" in stats:
        st.error(f"Erro ao carregar perfil: {stats['erro']}")
    else:
        st.success("Stats encontrados!")
        for k, v in stats.items():
            st.markdown(f"**{k}:** {v}")
