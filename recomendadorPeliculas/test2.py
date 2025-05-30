import networkx as nx
import requests  # Importamos requests para las llamadas a la API

# ----------------------------
# CONFIGURACIÓN DE DEEPSEEK API
# ----------------------------
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = ""  # Reemplaza con tu API key real

# ----------------------------
# GRAFO DE GÉNEROS Y PELÍCULAS
# ----------------------------
G = nx.Graph()

generos = {
    "accion": [],
    "comedia": [],
    "drama": [],
    "terror": [],
    "ciencia ficcion": [],
    "romance": [],
    "aventura": [],
    "fantasia": []
}

for genero in generos:
    G.add_node(genero, tipo="genero")

# ----------------------------
# PREGUNTAS PARA EL PERFIL
# ----------------------------
def hacer_preguntas():
    print("\n👋 Bienvenido al recomendador de peliculas 🎬\n")
    print("Responde con 'si' o 'no' a las siguientes preguntas:\n")

    puntos = {g: 0 for g in generos}

    preguntas = [
        ("¿Te gustan las emociones fuertes y las peleas?", "accion"),
        ("¿Prefieres peliculas que te hagan reir?", "comedia"),
        ("¿Te interesan las historias profundas o tristes?", "drama"),
        ("¿Te gustan las peliculas que dan miedo?", "terror"),
        ("¿Te fascinan los futuros, robots o el espacio?", "ciencia ficcion"),
        ("¿Disfrutas las historias de amor?", "romance"),
        ("¿Te gustan las aventuras y viajes emocionantes?", "aventura"),
        ("¿Te atraen mundos magicos o criaturas fantasticas?", "fantasia"),
        ("¿Te emocionan las persecuciones y disparos?", "accion"),
        ("¿Te gusta ver personajes en situaciones absurdas o graciosas?", "comedia"),
    ]

    for pregunta, genero in preguntas:
        respuesta = input(f"{pregunta} (si/no): ").strip().lower()
        if respuesta == "si":
            puntos[genero] += 1

    genero_favorito = max(puntos, key=puntos.get)
    return genero_favorito

# ----------------------------
# IA: GENERAR PELÍCULAS DEL GÉNERO (USANDO DEEPSEEK)
# ----------------------------
def recomendar_peliculas_ia(genero):
    prompt = f"Recomiéndame 10 películas populares del género {genero}. Solo devuelve los títulos en formato de lista, sin números ni comentarios."
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Verifica errores HTTP
        
        respuesta_json = response.json()
        return respuesta_json["choices"][0]["message"]["content"]
    
    except Exception as e:
        return f"❌ Error al conectar con DeepSeek: {e}"

# ----------------------------
# PROGRAMA PRINCIPAL
# ----------------------------
if __name__ == "__main__":
    genero_favorito = hacer_preguntas()
    print(f"\n🎯 Segun tus respuestas, tu genero favorito es: **{genero_favorito.upper()}**\n")

    print("🤖 Buscando recomendaciones con inteligencia artificial (DeepSeek)...\n")
    peliculas_recomendadas = recomendar_peliculas_ia(genero_favorito)
    print("🎥 Peliculas recomendadas:")
    print(peliculas_recomendadas)