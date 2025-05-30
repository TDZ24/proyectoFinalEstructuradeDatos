import networkx as nx
import random
import ollama  # Importamos la librería Ollama

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
# PREGUNTAS PARA EL PERFIL (VERSIÓN MEJORADA)
# ----------------------------
def hacer_preguntas():
    print("\n🎬 Bienvenido al recomendador de películas 2.0\n")
    print("Responde con 'si' o 'no' a las siguientes preguntas:\n")

    # Puntos base + preguntas ponderadas (algunas valen más)
    puntos = {genero: 0 for genero in generos}
    
    preguntas_ponderadas = [
        # (Pregunta, Género, Peso)
        ("¿Te gustan las películas con intensas escenas de acción como 'John Wick' o 'Mad Max'?", "accion", 2),
        ("¿Prefieres comedias inteligentes tipo 'Los Bridgerton' sobre comedias slapstick?", "comedia", 1),
        ("¿Disfrutas dramas emocionales profundos como 'El Padrino' o 'Forrest Gump'?", "drama", 1.5),
        ("¿Buscas sustos intensos como en 'El Conjuro' más que terror psicológico?", "terror", 1),
        ("¿Te interesa la ciencia ficción dura como 'Interstellar' o 'Blade Runner'?", "ciencia ficcion", 1.5),
        ("¿Prefieres historias de amor realistas tipo 'Antes del Amanecer' sobre romances fantásticos?", "romance", 1),
        ("¿Te entusiasman las aventuras épicas como 'Indiana Jones' o 'Jurassic Park'?", "aventura", 1),
        ("¿Adoras mundos de fantasía complejos como 'El Señor de los Anillos'?", "fantasia", 2),
        ("¿Eres fan de las películas de artes marciales o peleas coreografiadas?", "accion", 1.5),
        ("¿Ries fácilmente con comedias absurdas como 'Superbad' o 'The Hangover'?", "comedia", 1),
    ]

    for pregunta, genero, peso in preguntas_ponderadas:
        while True:
            respuesta = input(f"{pregunta} (si/no): ").strip().lower()
            if respuesta in ["si", "no"]:
                break
            print("⚠️ Por favor, responde solo 'si' o 'no'")
        
        if respuesta == "si":
            puntos[genero] += peso  # Suma puntos ponderados

    # Detección de empates
    max_puntos = max(puntos.values())
    generos_favoritos = [g for g, p in puntos.items() if p == max_puntos]
    
    if len(generos_favoritos) > 1:
        print(f"\n🔥 ¡Hay empate entre {', '.join(generos_favoritos)}!")
        genero_favorito = input("¿Cuál prefieres? (escribe el género): ").lower()
    else:
        genero_favorito = generos_favoritos[0]
    
    return genero_favorito

# ----------------------------
# FUNCIÓN DE RECOMENDACIÓN EN ESPAÑOL
# ----------------------------
def recomendar_peliculas_ia(genero):
    try:
        prompt = f"""Recomienda EXACTAMENTE 5 películas del género {genero} en español. 
        Para cada una, incluye SOLO:
        1. **Título** (Año)
        - *Sinopsis:* Breve descripción (1 línea)
        - *Por qué te gustará:* Razón personalizada
        
        Evita películas demasiado obvias. Ejemplo:
        
        **El Secreto de sus Ojos** (2009)
        - *Sinopsis:* Un thriller judicial sobre un crimen no resuelto.
        - *Por qué te gustará:* Perfecta si disfrutas dramas con giros inesperados.
        """
        
        response = ollama.chat(
            model="llama3",  # Asegúrate de usar un modelo en español
            messages=[{"role": "user", "content": prompt}],
            options={
                'temperature': 0.8,  # Creatividad balanceada
                'num_predict': 300,     # Contexto amplio para respuestas detalladas
                'seed': 42           # Semilla fija para consistencia
            }
        )
        return response['message']['content']
    
    except Exception as e:
        return f"Error: {str(e)}"

# ----------------------------
# PROGRAMA PRINCIPAL
# ----------------------------
if __name__ == "__main__":
    genero_favorito = hacer_preguntas()  # Tu función existente
    
    print(f"\n🎬 Generando 5 recomendaciones de {genero_favorito.upper()}...")
    print("⏳ Esto puede tomar unos segundos...\n")
    
    recomendaciones = recomendar_peliculas_ia(genero_favorito)
    print("🔥 RECOMENDACIONES PERSONALIZADAS:")
    print(recomendaciones)