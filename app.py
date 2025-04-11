import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import random
from PIL import Image

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
    url = f"https://gamersclub.com.br/player/{player_id}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    stats = {}
    nome_tag = soup.find("h1")
    stats["Nome"] = nome_tag.text.strip() if nome_tag else "Desconhecido"

    nivel_tag = soup.find("div", {"class": "level"})
    stats["Nível"] = nivel_tag.text.strip() if nivel_tag else "?"

    kd_match = re.search(r"K/D</span>\s*<strong[^>]*>([\d.]+)</strong>", res.text)
    stats["K/D"] = kd_match.group(1) if kd_match else "?"

    hs_match = re.search(r"HS</span>\s*<strong[^>]*>([\d.]+)%</strong>", res.text)
    stats["HS %"] = hs_match.group(1) + "%" if hs_match else "?"

    partidas_match = re.search(r"Partidas</span>\s*<strong[^>]*>([\d.]+)</strong>", res.text)
    stats["Partidas"] = partidas_match.group(1) if partidas_match else "?"

    return stats

if st.button("🔍 Buscar estatísticas"):
    stats = pegar_estatisticas_gc(player_id)

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

    # Título aleatório zoeiro
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

    # Mostrar contagem de zoeiras por stat
    for stat, count in st.session_state.reactions_por_stat.items():
        st.markdown(f"**{stat}**: {count} zoeiras")
