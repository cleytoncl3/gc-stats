import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time
import random

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
try:
    zoeira_img = Image.open("image.png")
except FileNotFoundError:
    st.warning("Imagem image.png não encontrada. Coloque no mesmo diretório do app.")

def pegar_estatisticas_gc(player_id):
    # Configura o Selenium em modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = f"https://gamersclub.com.br/player/{player_id}"
        driver.get(url)
        time.sleep(3)

        stats = {}

        try:
            stats["Nome"] = driver.find_element(By.TAG_NAME, "h1").text
        except:
            stats["Nome"] = "Desconhecido"

        try:
            stats["Nível"] = driver.find_element(By.CLASS_NAME, "level").text
        except:
            stats["Nível"] = "?"

        def extrair_stat(titulo):
            try:
                elemento = driver.find_element(By.XPATH, f"//span[text()='{titulo}']/following-sibling::strong")
                return elemento.text
            except:
                return "?"

        stats["K/D"] = extrair_stat("K/D")
        stats["HS %"] = extrair_stat("HS") + "%"
        stats["Partidas"] = extrair_stat("Partidas")

        return stats

    finally:
        driver.quit()

if st.button("🔍 Buscar estatísticas"):
    try:
        stats = pegar_estatisticas_gc(player_id)

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
                if 'zoeira_img' in locals():
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

    except Exception as e:
        st.error(f"Erro ao carregar perfil: {e}")
