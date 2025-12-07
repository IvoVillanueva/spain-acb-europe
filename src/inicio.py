import requests
from bs4 import BeautifulSoup
import polars as pl
from urllib.parse import urljoin
import re
import os

BASE_URL = "https://www.proballers.com"
EQUIPOS_ACB_URL = f"{BASE_URL}/es/baloncesto/liga/30/spain-liga-endesa/equipos"
EQUIPOS_EUROPEOS = ["Real Madrid", "Barcelona", "Valencia", "Baskonia", 
                    "Unicaja", "Joventut", "Gran Canaria", "Manresa", 
                    "Tenerife", "Bilbao", "Zaragoza"]
OUTPUT_DIR = "data"
OUTPUT_FILE = "plantillas.csv"

def get_proballers_soup(url):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": BASE_URL,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9"
    }
    session.get(BASE_URL, headers=headers)
    res = session.get(url, headers=headers)
    return BeautifulSoup(res.text, "html.parser")

def get_plantillas(team_url):
    soup_team = get_proballers_soup(team_url)
    jugadores = soup_team.select(".select-tab-average-30 a")
    return pl.DataFrame({
        "nombres": [a.get_text(strip=True) for a in jugadores],
        "jugador_link": [urljoin(team_url, a.get('href')) for a in jugadores],
        "player_id": [re.search(r'\d+', a.get('href')).group() for a in jugadores]
    })

if __name__ == "__main__":
    soup = get_proballers_soup(EQUIPOS_ACB_URL)
    equipos = soup.select("a.home-league__team-list__content__entry-team__presentation")
    
    df_equipos = pl.DataFrame({
        "nombres": [a.find('h3').get_text(strip=True) for a in equipos],
        "enlaces_equipo": [urljoin(EQUIPOS_ACB_URL, a.get('href')) for a in equipos],
        "team_id": [re.search(r'\d+', a.get('href')).group() for a in equipos]
    }).filter(pl.col("nombres").str.contains("|".join(EQUIPOS_EUROPEOS)))
    
    team_urls = df_equipos['enlaces_equipo'].to_list()
    df_todas_plantillas = pl.concat([get_plantillas(url) for url in team_urls])
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df_todas_plantillas.write_csv(f"{OUTPUT_DIR}/{OUTPUT_FILE}")
    print(f"✓ {len(df_todas_plantillas)} jugadores guardados en {OUTPUT_DIR}/{OUTPUT_FILE}")