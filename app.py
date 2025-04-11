import streamlit as st
import time
import zipfile
import requests
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

CHROMEDRIVER_VERSION = "120.0.6099.71"
CHROMEDRIVER_URL = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip"

def install_chromedriver():
    if not os.path.exists("chromedriver"):
        try:
            r = requests.get(CHROMEDRIVER_URL)
            r.raise_for_status()
            with open("chromedriver.zip", "wb") as f:
                f.write(r.content)
            with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
                zip_ref.extractall()
            os.rename("chromedriver-linux64/chromedriver", "chromedriver")
            os.chmod("chromedriver", 0o755)
        except Exception as e:
            st.error(f"Erro ao baixar o ChromeDriver: {e}")
            raise

def iniciar_driver():
    install_chromedriver()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--remote-debugging-pipe")
    driver = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)
    return driver

def buscar_perfil(link):
    if not link.startswith("https://"):
        raise ValueError("URL inválida. Certifique-se de colar o link completo com https://")
    driver = iniciar_driver()
    try:
        driver.get(link)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "player-general-info"))
        )
        html = driver.page_source
        driver.quit()
        return html
    except TimeoutException:
        st.error("❌ Não foi possível carregar o perfil: elemento não encontrado após 20 segundos.")
        html = driver.page_source
        driver.quit()
        st.text("⛔ Parte do HTML carregado (para debug):")
        st.code(html[:1000])
        raise
    except Exception as e:
        driver.quit()
        raise e

def extrair_stats(html):
    soup = BeautifulSoup(html, "html.parser")
    stats = {}
    geral = soup.select_one(".player-general-info")
    if geral:
        stats["nome"] = geral.select_one(".player-info__name").text.strip()
        stats["elo"] = geral.select_one(".player-info__level").text.strip()
    return stats

def main():
    st.set_page_config(page_title="GC Stats do Vintorez", page_icon="🧠", layout="wide")
    st.markdown(
        """
        <h1 style='color: #7289da;'>GC Stats do Vintorez</h1>
        <p style='color: white;'>Cole o link do perfil da GamersClub para ver as estatísticas e reagir zoando com os amigos.</p>
        """,
        unsafe_allow_html=True
    )

    link = st.text_input("Link do perfil (cole aqui):")

    if st.button("Buscar perfil"):
        try:
            html = buscar_perfil(link)
            stats = extrair_stats(html)
            st.subheader(f"📊 Estatísticas de {stats.get('nome', 'Desconhecido')}")
            st.markdown(f"**Elo:** {stats.get('elo', 'N/A')}")

            st.markdown("---")
            st.markdown("### 😆 Reações")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1: st.button("♿", key="r1")
            with col2: st.button("👍", key="r2")
            with col3: st.button("😂", key="r3")
            with col4: st.button("💀", key="r4")
            with col5: st.button("🧠", key="r5")

        except ValueError as ve:
            st.error(f"Erro ao carregar perfil: {ve}")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
