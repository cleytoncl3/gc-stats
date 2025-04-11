import streamlit as st
import zipfile
import os
import requests
import shutil
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def install_chromedriver():
    try:
        # Descobre a versão do Chromium instalada
        version_output = subprocess.check_output(["chromium", "--version"]).decode("utf-8")
        version_number = version_output.strip().split(" ")[1].split(".")[0]

        # Monta URL do ChromeDriver correspondente
        response = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version_number}")
        driver_version = response.text.strip()
        zip_url = f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_linux64.zip"

        # Faz o download
        zip_path = "chromedriver.zip"
        with requests.get(zip_url, stream=True) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)

        # Verifica se é um ZIP válido antes de extrair
        if not zipfile.is_zipfile(zip_path):
            raise Exception("Erro ao baixar o ChromeDriver. Arquivo não é um ZIP válido.")

        # Extrai
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall()

        os.remove(zip_path)
        os.chmod("chromedriver", 0o755)

    except Exception as e:
        raise RuntimeError(f"Erro ao baixar o ChromeDriver: {e}")

def carregar_perfil(perfil_id):
    try:
        install_chromedriver()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = "/usr/bin/chromium"

        service = Service("./chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        url = f"https://gamersclub.gg/player/{perfil_id}"
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        nome = soup.select_one("h1")
        driver.quit()

        if not nome:
            return None

        return nome.text.strip()

    except Exception as e:
        raise RuntimeError(f"Erro ao carregar perfil: {e}")

# --- Interface Streamlit ---
st.set_page_config(page_title="GC Stats do Vintorez", layout="centered")
st.markdown("<h1 style='color:#f04;'>🎯 GC Stats do Vintorez</h1>", unsafe_allow_html=True)
st.write("Cole o link do perfil da **GamersClub**:")

input_url = st.text_input("URL do perfil", placeholder="Ex: 2399445")
if input_url:
    try:
        resultado = carregar_perfil(input_url)
        if resultado:
            st.success(f"Nome do jogador: {resultado}")
        else:
            st.error("Perfil não encontrado.")
    except Exception as erro:
        st.error(f"Erro ao carregar perfil: {erro}")
