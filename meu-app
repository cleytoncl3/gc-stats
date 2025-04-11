import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Zoeira GC", layout="centered")

st.title("📊 Estatísticas de Jogador - Gamers Club")
st.caption("Cole o link do jogador e veja os dados dele pra zoar no grupo 😎")

url_input = st.text_input("🔗 Link do perfil da Gamers Club:", "")

def get_gc_stats(player_id):
    url = f"https://gamersclub.com.br/player/{player_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        nome = soup.select_one(".player-profile .name").text.strip()
        nivel = soup.select_one(".level span").text.strip()
        rating = soup.find("span", string="Rating").find_next("strong").text.strip()
        kd = soup.find("span", string="K/D").find_next("strong").text.strip()
        hs = soup.find("span", string="HS%").find_next("strong").text.strip()
        partidas = soup.find("span", string="Partidas").find_next("strong").text.strip()
        mapa_fav = soup.select_one(".favorite-map .map-name").text.strip()

        stats = {
            "Nome": nome,
            "Nível": nivel,
            "Rating": rating,
            "K/D": kd,
            "HS%": hs,
            "Partidas": partidas,
            "Mapa favorito": mapa_fav
        }

        return stats
    
    except Exception as e:
        return None

if url_input:
    try:
        player_id = url_input.strip("/").split("/")[-1]
        stats = get_gc_stats(player_id)
        if stats:
            st.success(f"🎯 Estatísticas de {stats['Nome']}")
            for chave, valor in stats.items():
                st.write(f"**{chave}**: {valor}")
        else:
            st.error("⚠️ Não foi possível pegar os dados. Confere o link.")
    except:
        st.error("⚠️ Link inválido.")
