import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import random

st.set_page_config(page_title="GC Stats do Vintorez", layout="centered")

# Fundo no estilo Discord
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2c2f33;
        color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Estatísticas GamersClub - Zueira Edition")
st.markdown("Insira o ID do perfil da GamersClub abaixo (ex: `2399445`)")

# Entrada do ID do jogador
player_id = st.text_input("ID do Jogador", value="2399445")

# Emojis para zoação
emojis = ["♿", "👍", "😂", "💀", "🧠"]

# Carregando reações armazenadas na sessão
if "reactions" not in st.session_state:
    st.session_state.reactions = {emoji: 0 for emoji in emojis}

def pegar_estatisticas_gc(player_id):
    try:
        url = f"https://gamersclub.com.br/player/{player_id}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        stats = {}

        # Nome do jogador
        nome_tag = soup.find("h1")
        stats["Nome"] = nome_tag.text.strip() if nome_tag else "Desconhecido"

        # Nível
        nivel_tag = soup.find("div", {"class": "level"})
        stats["Nível"] = nivel_tag.text.strip() if nivel_tag else "?"

        # K/D
        kd_match = re.search(r"K/D</span>\s*<strong[^>]*>([\d.]+)</strong>", res.text)
        stats["K/D"] = kd_match.group(1) if kd_match else "?"

        # Headshot %
        hs_match = re.search(r"HS</span>\s*<strong[^>]*>([\d.]+)%</strong>", res.text)
        stats["HS %"] = hs_match.group(1) + "%" if hs_match else "?"

        # Total de partidas
        partidas_match = re.search(r"Partidas</span>\s*<strong[^>]*>([\d.]+)</strong>", res.text)
        stats["Partidas"] = partidas_match.group(1) if partidas_match else "?"

        return stats

    except Exception as e:
        st.error("❌ Erro ao buscar os dados. Verifique o ID ou tente novamente mais tarde.")
        st.exception(e)
        return None

# Quando clicar no botão
if st.button("🔍 Buscar estatísticas"):
    with st.spinner("Buscando dados..."):
        stats = pegar_estatisticas_gc(player_id)

    if stats:
        st.markdown(f"## 👤 {stats['Nome']}")
        st.markdown(f"**Nível:** {stats['Nível']}")
        st.markdown(f"**K/D:** {stats['K/D']}")
        st.markdown(f"**HS %:** {stats['HS %']}")
        st.markdown(f"**Partidas:** {stats['Partidas']}")

        st.divider()

        # Reações (Zoação)
        st.markdown("### Clique em uma reação para zoar 👇")
        cols = st.columns(len(emojis))
        for i, emoji in enumerate(emojis):
            if cols[i].button(emoji):
                st.session_state.reactions[emoji] += 1

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

        # Mostrar emojis acumulando
        for emoji in emojis:
            st.markdown(f"**{emoji}** " + (emoji + " ") * st.session_state.reactions[emoji])
            
