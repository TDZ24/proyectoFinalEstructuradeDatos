import networkx as nx
from openai import OpenAI

# ----------------------------
# CONFIGURACIÓN
# ----------------------------
client = OpenAI(api_key="")  # Reemplaza con tu API KEY si es necesario

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
# IA: GENERAR PELÍCULAS DEL GÉNERO
# ----------------------------
def recomendar_peliculas_ia(genero):
    prompt = f"Recomiendame una lista de 10 peliculas populares del genero {genero}. Solo dame los titulos, en forma de lista."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ----------------------------
# PROGRAMA PRINCIPAL
# ----------------------------
if __name__ == "__main__":
    genero_favorito = hacer_preguntas()
    print(f"\n🎯 Segun tus respuestas, tu genero favorito es: **{genero_favorito.upper()}**\n")

    print("🤖 Buscando recomendaciones con inteligencia artificial...\n")
    peliculas_recomendadas = recomendar_peliculas_ia(genero_favorito)
    print("🎥 Peliculas recomendadas:")
    print(peliculas_recomendadas)
