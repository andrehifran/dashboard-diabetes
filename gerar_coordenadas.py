import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Carregar CSV com cidades
df = pd.read_csv("dados_diabetes.csv")

# Pegar cidades únicas
cidades = df['Cidade'].dropna().unique()

# Configurar geolocator com User-Agent (obrigatório)
geolocator = Nominatim(user_agent="meu_app_streamlit")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Listas para armazenar resultados
lista_cidades = []
latitudes = []
longitudes = []

for cidade in cidades:
    location = geocode(f"{cidade}, Rondônia, Brazil")
    if location:
        lista_cidades.append(cidade)
        latitudes.append(location.latitude)
        longitudes.append(location.longitude)
        print(f"Encontrado: {cidade} -> {location.latitude}, {location.longitude}")
    else:
        print(f"Não encontrado: {cidade}")

# Criar DataFrame com as coordenadas
df_coords = pd.DataFrame({
    "Cidade": lista_cidades,
    "Latitude": latitudes,
    "Longitude": longitudes
})

# Salvar em CSV
df_coords.to_csv("coordenadas_cidades.csv", index=False)
print("Arquivo 'coordenadas_cidades.csv' salvo com sucesso.")
