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
        # Pega a versão completa do Chromium instalado
        version_output = subprocess.check_output(["chromium", "--version"]).decode("utf-8")
        full_version = version_output.strip().split(" ")[1]  # Ex: 120.0.6099.224

        # Busca a versão compatível exata do ChromeDriver
        response = requests.get(f"https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json")
        data = response.json()

        if full_version.split('.')[0] not in data['channels']['Stable']['version']:
            raise Exception("Versão do ChromeDriver compatível não encontrada")

        stable_data = data['channels']['Stable']
        driver_version = stable_data["version"]
        download_info = next(
            (item for item in stable_data["downloads"]["chromedriver"] if item["platform"] == "linux64"),
            None
        )

        if not download_info:
            raise Exception("Download para Linux não encontrado.")

        zip_url = download_info["url"]

        # Baixa o ZIP
        zip_path = "chromedriver.zip"
        with requests.get(zip_url, stream=True) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)

        if not zipfile.is_zipfile(zip_path):
            raise Exception("Erro ao baixar o ChromeDriver. Arquivo não é um ZIP válido.")

        # Extrai e renomeia o binário
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall()
        os.remove(zip_path)

        # Mover o chromedriver certo
        for root, dirs, files in os.walk("."):
            for file in files:
                if file == "chromedriver":
                    src = os.path.join(root, file)
                    shutil.move(src, "./chromedriver")
                    os.chmod("./chromedriver", 0o755)
                    return

        raise Exception("ChromeDriver não encontrado após extração.")

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
