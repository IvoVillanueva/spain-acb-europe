# spain-acb-europe

Proyecto personal para extraer y consolidar datos de jugadores españoles de la ACB que participan en competiciones europeas entre semana.

## Objetivo
Recolectar, normalizar y almacenar información (player_id, nombre, nacionalidad, equipo, posición, fecha del partido, competición, minutos, puntos, rebotes, asistencias, valoración, fuente_url, fecha_scrape) de jugadores españoles de la ACB que juegan en competiciones europeas (EuroLeague, EuroCup, Basketball Champions League, etc.).

## Fuentes de datos (ejemplos)
- Sitios oficiales de competiciones (EuroLeague, EuroCup)
- Webs oficiales de equipos y de la ACB
- APIs deportivas (si están disponibles)
- Scraping de páginas de estadísticas (respetando ToS y robots.txt)

## Estructura sugerida
- /src : código (scrapers, parsers, normalizadores)
- /data : dumps CSV/JSON/SQLite (no versionar grandes dumps)
- /notebooks : análisis exploratorio (Jupyter)
- /docs : documentación y notas
- README.md, LICENSE, .gitignore

## Tecnologías sugeridas
- Python: requests, BeautifulSoup / Playwright (si necesitas render JS)
- Pandas para limpieza/transformación
- SQLite o PostgreSQL para almacenamiento
- GitHub Actions para automatizar scrapes (cron) si lo necesitas

## Buenas prácticas
- Respetar rate limits y robots.txt; usar backoff y caches.
- Guardar credenciales fuera del repo (usar .env y secrets en GitHub).
- Normalizar identificadores (player_id, team_id) para evitar duplicados.
- Versionar el esquema de salida si cambias campos.

## Uso (local)
1. Clonar el repo:
   git clone https://github.com/IvoVillanueva/spain-acb-europe.git
2. Crear y activar entorno virtual e instalar dependencias:
   python -m venv venv
   source venv/bin/activate   # mac/linux
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   pip install -r requirements.txt
3. Ejecutar el scraper principal:
   python src/main.py

## Licencia
MIT (ver LICENSE)
