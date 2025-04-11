import os
import zipfile
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import streamlit as st
from colorama import Fore, Style

CHROMEDRIVER_PATH = "chromedriver"

def install_chromedriver():
    try:
        # Detecta a versão atual do Chromium
        version_output = os.popen("/usr/bin/chromium --version").read()
        version_number = version_output.split("Chromium")[1].strip().split('.')[0]

        # Monta URL correta do ChromeDriver
        url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version_number}"
        response = requests.get(url)
        if response.status_code != 200:
            st.error("Erro ao baixar o ChromeDriver: Versão do ChromeDriver compatível não encontrada")
            return

        latest_version = response.text.strip()
        download_url = f"https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_linux64.zip"
        zip_response = requests.get(download_url)
        zip_path = "chromedriver.zip"

        with open(zip_path, "wb") as f:
            f.write(zip_response.content)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall()

        os.remove(zip_path)
        os.chmod(CHROMEDRIVER_PATH, 0o755)

    except Exception as e:
        st.error(f"Erro ao baixar o ChromeDriver: {e}")

def start_browser():
    install_chromedriver()
    options = Options()
    # Flags seguras para headless em servidores
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    options.binary_location = "/usr/bin/chromium"

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def buscar_perfil_gc(url):
    try:
        driver = start_browser()
        driver.get(url)

        st.info("Carregando perfil...")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        nickname = soup.find("h1").text.strip()

        estatisticas = {}
        for div in soup.find_all("div", class_="player-stats__number"):
            label = div.find_previous_sibling("div").text.strip()
            valor = div.text.strip()
            estatisticas[label] = valor

        driver.quit()
        return nickname, estatisticas

    except WebDriverException as e:
        st.error(f"Erro ao carregar perfil: {e}")
    except Exception as e:
        st.error(f"Erro inesperado: {e}")

# --- INTERFACE ---
st.set_page_config(page_title="GC Stats do Vintorez", page_icon="🎯", layout="centered", initial_sidebar_state="auto")
st.markdown("""
    <style>
        body { background-color: #2c2f33; color: white; }
        .stApp { background-color: #2c2f33; }
        .emoji-bar { font-size: 24px; }
        .stat-card { background-color: #23272a; padding: 16px; border-radius: 12px; margin: 8px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 GC Stats do Vintorez")
st.caption("Zoando os amigos com estatísticas da GamersClub 😎")

url = st.text_input("Cole o link do perfil da GC:")

if url:
    resultado = buscar_perfil_gc(url)
    if resultado:
        nickname, stats = resultado
        st.subheader(f"🔍 Estatísticas de {nickname}")
        for k, v in stats.items():
            st.markdown(f"<div class='stat-card'><strong>{k}:</strong> {v}</div>", unsafe_allow_html=True)

        st.markdown("### Reações anônimas:")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: st.button("♿", key="r1")
        with col2: st.button("👍", key="r2")
        with col3: st.button("😂", key="r3")
        with col4: st.button("💀", key="r4")
        with col5: st.button("🧠", key="r5")
