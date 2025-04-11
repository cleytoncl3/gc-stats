import os
import zipfile
import requests
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Instala chromedriver da versão compatível com Chromium do ambiente
def install_chromedriver():
    url = "https://storage.googleapis.com/chrome-for-testing-public/120.0.6099.224/linux64/chromedriver-linux64.zip"
    response = requests.get(url)
    with open("chromedriver.zip", "wb") as f:
        f.write(response.content)
    
    with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
        zip_ref.extractall(".")
    
    os.chmod("chromedriver-linux64/chromedriver", 0o755)
    os.environ["PATH"] += os.pathsep + os.path.abspath("chromedriver-linux64")

# Função para criar o driver com Chromium
def create_driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        executable_path="./chromedriver-linux64/chromedriver",
        options=options
    )
    return driver

# Função para buscar dados do perfil
def buscar_perfil_gc(link_perfil):
    driver = create_driver()
    try:
        driver.get(link_perfil)
        time.sleep(5)  # Espera a página carregar

        # Exemplo: pegando o nome do jogador e KD
        nome = driver.find_element(By.CSS_SELECTOR, ".name").text
        kd = driver.find_element(By.XPATH, "//div[contains(text(),'K/D')]/following-sibling::div").text

        return {
            "nome": nome,
            "kd": kd
        }
    except Exception as e:
        return f"Erro ao carregar perfil: {e}"
    finally:
        driver.quit()

# Inicializa chromedriver no boot do app
install_chromedriver()

# Streamlit UI
st.set_page_config(page_title="GC Stats do Vintorez", page_icon="🎮", layout="centered", initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center;'>GC Stats do Vintorez</h1>", unsafe_allow_html=True)

link = st.text_input("Link do perfil da GamersClub:")

if link:
    with st.spinner("Buscando perfil..."):
        resultado = buscar_perfil_gc(link)
        if isinstance(resultado, dict):
            st.success("Perfil carregado com sucesso!")
            st.markdown(f"**Nome:** {resultado['nome']}")
            st.markdown(f"**K/D:** {resultado['kd']}")
        else:
            st.error(resultado)
