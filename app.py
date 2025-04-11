import streamlit as st
import requests
from bs4 import BeautifulSoup

# Emojis disponíveis para reações
emojis = ["♿", "😂", "💀", "👍", "🧠"]
reactions = {emoji: 0 for emoji in emojis}  # contador de reações

# Aplica o estilo visual do Discord
st.markdown("""
    <style>
    .stApp {
        background-color: #2C2F33;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("📊 Estatísticas GC - Zoação Mode 😎")

# Perfil de exemplo (do seu amigo)
player_url = "https://gamersclub.com.br/player/2399445"

# Função para extrair nome e stats
def pegar_estatisticas_gc(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    nome = soup.find("h1").text.strip() if soup.find("h1") else "Desconhecido"
    stats = soup.find_all("div", class_="general-stats__value")

    try:
        kd = stats[0].text.strip()
        hs = stats[1].text.strip()
        win_rate = stats[2].text.strip()
    except:
        kd = hs = win_rate = "?"

    return nome, kd, hs, win_rate

# Pegando dados reais do site
nome, kd, hs, win_rate = pegar_estatisticas_gc(player_url)

st.subheader(f"👤 Jogador: {nome}")

# Mostrando estatísticas
st.write(f"**K/D:** {kd}")
st.write(f"**Headshot %:** {hs}")
st.write(f"**Winrate:** {win_rate}")

st.divider()
st.markdown("### Reações da galera (anônimas):")

# Mostrar botões de reação
cols = st.columns(len(emojis))
for i, emoji in enumerate(emojis):
    if cols[i].button(emoji):
        reactions[emoji] += 1

# Mostrar emojis acumulando (zoação)
st.markdown("### Reações acumuladas:")
for emoji in emojis:
    st.markdown(f"**{emoji}** " + (emoji + " ") * reactions[emoji])
