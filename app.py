import streamlit as st
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import webbrowser

st.set_page_config(page_title="GC Stats do Vintorez", layout="wide", page_icon="🎯")

# Estilo escuro com vibe Discord
st.markdown(
    """
    <style>
    body {
        background-color: #2c2f33;
        color: white;
    }
    .emoji {
        font-size: 1.5rem;
        margin-right: 5px;
    }
    .stApp {
        background-color: #2c2f33;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎯 GC Stats do Vintorez")

url = st.text_input("Cole o link do perfil da GamersClub (ex: https://gamersclub.gg/player/123456)", "")

REACTIONS = ["♿", "👍", "😂", "💀", "🧠"]
reaction_counts = {emoji: 0 for emoji in REACTIONS}

def buscar_perfil(url):
    if not url.startswith("https://"):
        raise ValueError("URL inválida. Certifique-se de colar o link completo com https://")

    try:
        st.info("⏳ Carregando perfil...")

        options = uc.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        driver = uc.Chrome(options=options)
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nickname"))
        )

        html = driver.page_source
        driver.quit()

        # Salvar HTML localmente
        debug_path = os.path.abspath("perfil_debug.html")
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(html)

        # Exibir caminho no Streamlit
        st.info(f"📄 HTML salvo em: `{debug_path}`")

        # Abrir automaticamente no navegador padrão
        webbrowser.open(f"file://{debug_path}")

        return html

    except Exception as e:
        st.error("❌ Não foi possível carregar o perfil: elemento não encontrado após 20 segundos.")
        raise e

def extrair_stats(html):
    soup = BeautifulSoup(html, "html.parser")

    nickname = soup.find("h1", class_="nickname")
    nome = nickname.text.strip() if nickname else "Desconhecido"

    stats = soup.find_all("div", class_="player-stats__value")
    valores = [s.text.strip() for s in stats]

    return nome, valores

if url:
    try:
        html = buscar_perfil(url)
        nome, stats = extrair_stats(html)

        st.success(f"✅ Estatísticas de {nome}")

        col1, col2, col3 = st.columns(3)
        for i, stat in enumerate(stats[:9]):
            with [col1, col2, col3][i % 3]:
                st.metric(label=f"Stat {i+1}", value=stat)

        st.markdown("---")
        st.subheader("Reações dos amigos (anônimas)")
        cols = st.columns(len(REACTIONS))
        for i, emoji in enumerate(REACTIONS):
            if cols[i].button(f"{emoji}"):
                reaction_counts[emoji] += 1

        st.markdown(
            " ".join(f"<span class='emoji'>{emoji} x{reaction_counts[emoji]}</span>" for emoji in REACTIONS),
            unsafe_allow_html=True,
        )

    except Exception as e:
        st.error(f"Erro inesperado: {e}")
