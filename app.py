import streamlit as st
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re

st.set_page_config(page_title="GC Stats do Vintorez", layout="centered")

st.markdown(
    """
    <style>
    body {
        background-color: #2f3136;
        color: white;
    }
    .emoji {
        font-size: 24px;
        margin-right: 5px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("GC Stats do Vintorez 😎")
st.write("Cole o link do perfil da **GamersClub** de um amigo para ver as estatísticas dele e reagir com zoeira.")

REACTIONS = ["♿", "👍", "😂", "💀", "🧠"]

reaction_state = {r: 0 for r in REACTIONS}

def iniciar_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=pt-BR")

    driver = uc.Chrome(options=options, headless=True)
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
        time.sleep(2)

        html = driver.page_source
        return html

    except Exception as e:
        html_debug = driver.page_source[:1000]
        st.error("❌ Não foi possível carregar o perfil: elemento não encontrado após 20 segundos.")
        st.write("⛔ Parte do HTML carregado (para debug):")
        st.code(html_debug)
        raise Exception(f"Erro inesperado: {str(e)}")

    finally:
        driver.quit()

def extrair_estatisticas(html):
    soup = BeautifulSoup(html, "html.parser")
    info = soup.find("div", class_="player-general-info")

    if not info:
        raise ValueError("Não foi possível encontrar as informações do jogador.")

    nome = info.find("h1").text.strip()
    detalhes = info.find_all("p")

    estatisticas = {
        "Nome": nome,
        "Rank": detalhes[0].text.strip() if len(detalhes) > 0 else "N/A",
        "Level": detalhes[1].text.strip() if len(detalhes) > 1 else "N/A",
        "Pontos": detalhes[2].text.strip() if len(detalhes) > 2 else "N/A",
    }

    return estatisticas

link = st.text_input("🔗 Cole o link do perfil GC aqui:")

if link:
    if st.button("🔍 Buscar"):
        with st.spinner("Carregando perfil..."):
            try:
                html = buscar_perfil(link)
                stats = extrair_estatisticas(html)

                st.subheader(f"📊 Estatísticas de {stats['Nome']}")
                st.markdown(f"**Rank:** {stats['Rank']}")
                st.markdown(f"**Level:** {stats['Level']}")
                st.markdown(f"**Pontos:** {stats['Pontos']}")

                st.markdown("---")
                st.subheader("Reaja com zoeira 👇")

                cols = st.columns(len(REACTIONS))
                for i, emoji in enumerate(REACTIONS):
                    if cols[i].button(emoji):
                        reaction_state[emoji] += 1

                st.markdown("### Reações:")
                for emoji in REACTIONS:
                    st.markdown(f"{emoji} × {reaction_state[emoji]}", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Erro ao carregar perfil.\n\n{str(e)}")
