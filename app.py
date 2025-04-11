import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
import zipfile
import requests

def install_chromedriver():
    url = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.224/linux64/chromedriver-linux64.zip"
    
    response = requests.get(url)
    if response.status_code != 200 or not response.content.startswith(b'PK'):
        raise Exception("Erro ao baixar o ChromeDriver. Arquivo não é um ZIP válido.")
    
    with open("chromedriver.zip", "wb") as f:
        f.write(response.content)
    
    with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
        zip_ref.extractall(".")
    
    os.chmod("chromedriver-linux64/chromedriver", 0o755)
    os.environ["PATH"] += os.pathsep + os.path.abspath("chromedriver-linux64")

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = "/usr/bin/chromium"

    driver_path = os.path.abspath("chromedriver-linux64/chromedriver")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_player_stats(profile_url):
    driver = setup_driver()
    try:
        driver.get(profile_url)
        time.sleep(5)

        stats = {
            "Nome": driver.find_element(By.CLASS_NAME, "name").text,
            "Level": driver.find_element(By.CLASS_NAME, "level").text,
            "Elo": driver.find_element(By.CLASS_NAME, "elo").text
        }

        return stats
    finally:
        driver.quit()

# ========== Streamlit UI ==========
st.set_page_config(page_title="GC Stats do Vintorez", layout="wide", page_icon="🎯")

st.markdown("""
    <style>
    body {
        background-color: #2c2f33;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 GC Stats do Vintorez")
st.markdown("Cole o link do perfil da **GamersClub**:")

url = st.text_input("URL do perfil")

if url:
    try:
        install_chromedriver()
        stats = get_player_stats(url)
        st.success("Estatísticas carregadas com sucesso!")
        st.json(stats)
    except Exception as e:
        st.error(f"Erro ao carregar perfil: {e}")
