import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from PIL import Image
from pathlib import Path

st.set_page_config(page_title="GC Stats do Vintorez", layout="centered")

# Fundo estilo Discord
st.markdown(
    """
    <style>
    body {
        background-color: #2c2f33;
        color: #ffffff;
    }
    .stApp {
        background-color: #2c2f33;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Estatísticas GamersClub - Zueira Edition")
st.markdown("Insira o ID do perfil da GamersClub abaixo (ex: `2399445`)")

player_id = st.text_input("ID do Jogador", value="2399445")

# Emojis para zoação
emojis = ["♿", "👍", "😂", "💀", "🧠"]

# Reações da zoeira por estatística
if "reactions_por_stat" not in st.session_state:
    st.session_state.reactions_por_stat = {
        "K/D": 0,
        "HS %": 0,
        "Partidas": 0
    }

# Caminho seguro da imagem
image_path = Path(__file__).parent / "image.png"
zoeira_img = Image.open(image_path)

def pegar_estatisticas_gc_com_selenium(player_id):
    stats = {
        "Nome": "Desconhecido",
        "Nível": "?",
        "K/D": "?",
        "HS %": "?",
        "Partidas": "?"
    }

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")

    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        url = f"https://gamersclub.com.br/player/{player_id}"
        driver.get(url)
        time.sleep(3)  # tempo para carregar

        # Nome
        try:
            nome = driver.find_element(By.TAG_NAME, "h1").text.strip()
            stats["Nome"] = nome
        except:
            pass

        # Nível
        try:
            nivel = driver.find_element(By.CLASS_NAME, "level").text.strip()
            stats["Nível"] = nivel
        except:
            pass

        # Estatísticas
        try:
            cards = driver.find_elements(By.CLASS_NAME, "statistics-card__value")
            if len(cards) >= 3:
                stats["K/D"] = cards[0].text.strip()
                stats["HS %"] = cards[1].text.strip()
                stats["Partidas"] = cards[2].text.strip()
        except:
            pass

        driver.quit()
    except Exception as e:
        st.error(f"Erro ao carregar perfil: {e}")

    return stats

if st.button("🔍 Buscar estatísticas"):
    stats = pegar_estatisticas_gc_com_selenium(player_id)

    st.markdown(f"## 👤 {stats['Nome']}")
    st.markdown(f"**Nível:** {stats['Nível']}")
    st.divider()

    # Mostrar stats com botão de zoeira do lado
    for stat in ["K/D", "HS %", "Partidas"]:
        cols = st.columns([3, 1])
        with cols[0]:
            st.markdown(f"**{stat}:** {stats[stat]}")
        with cols[1]:
            if st.button(f"Zoeira {stat}", key=stat):
                st.session_state.reactions_por_stat[stat] += 1
            st.image(zoeira_img, use_container_width=True)

    st.divider()

    titulos_zoeira = [
        "Medidor de vergonha alheia",
        "Galera tá reagindo assim 👇",
        "Termômetro da humilhação",
        "Quantas vezes ele foi ♿ hoje?",
        "Análise técnica dos crimes cometidos nas partidas",
        "As estatísticas não mentem… mas doem",
        "hoje ele ta level guanta?",
        "ele ta bem fisicamente?"
    ]

    titulo_aleatorio = random.choice(titulos_zoeira)
    st.markdown(f"### {titulo_aleatorio}")

    for stat, count in st.session_state.reactions_por_stat.items():
        st.markdown(f"**{stat}**: {count} zoeiras")
