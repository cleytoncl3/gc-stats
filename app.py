import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
import time
import random
import os

# Corrigir path no Streamlit Cloud
os.environ["PATH"] += os.pathsep + "/usr/lib/chromium-browser/"
 
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

# Carregar imagem do botão zoeira
zoeira_img = Image.open("image.png")

def pegar_estatisticas_gc(player_id):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = "/usr/lib/chromium-browser/chromium-browser"

        driver = webdriver.Chrome(options=options)
        url = f"https://gamersclub.com.br/player/{player_id}"
        driver.get(url)
        time.sleep(3)

        stats = {}

        try:
            stats["Nome"] = driver.find_element(By.TAG_NAME, "h1").text.strip()
        except:
            stats["Nome"] = "Desconhecido"

        try:
            stats["Nível"] = driver.find_element(By.CLASS_NAME, "level").text.strip()
        except:
            stats["Nível"] = "?"

        try:
            stats["K/D"] = driver.find_element(By.XPATH, "//span[contains(text(),'K/D')]/following-sibling::strong").text.strip()
        except:
            stats["K/D"] = "?"

        try:
            stats["HS %"] = driver.find_element(By.XPATH, "//span[contains(text(),'HS')]/following-sibling::strong").text.strip()
        except:
            stats["HS %"] = "?"

        try:
            stats["Partidas"] = driver.find_element(By.XPATH, "//span[contains(text(),'Partidas')]/following-sibling::strong").text.strip()
        except:
            stats["Partidas"] = "?"

        driver.quit()
        return stats
    except Exception as e:
        return f"Erro ao carregar perfil: {e}"

if st.button("🔍 Buscar estatísticas"):
    stats = pegar_estatisticas_gc(player_id)

    if isinstance(stats, str):
        st.error(stats)
    else:
        st.markdown(f"## 👤 {stats['Nome']}")
        st.markdown(f"**Nível:** {stats['Nível']}")
        st.divider()

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
