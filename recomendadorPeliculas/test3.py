import networkx as nx
import time
from tqdm import tqdm
import ollama

# ----------------------------
# GRAFO DE GÉNEROS Y PELÍCULAS
# ----------------------------
G = nx.Graph()
generos = {
    "accion": [], "comedia": [], "drama": [], "terror": [],
    "ciencia ficcion": [], "romance": [], "aventura": [], "fantasia": []
}
for genero in generos:
    G.add_node(genero, tipo="genero")

# ----------------------------
# PREGUNTAS MEJORADAS
# ----------------------------
def hacer_preguntas():
    print("\n🎬 Bienvenido al recomendador de películas\n")
    puntos = {g: 0 for g in generos}
    
    preguntas = [
        ("¿Te gustan escenas de acción intensas como 'John Wick'?", "accion", 2),
        ("¿Prefieres comedias inteligentes tipo 'Los Bridgerton'?", "comedia", 1),
        ("¿Disfrutas dramas profundos como 'El Padrino'?", "drama", 1.5),
        ("¿Buscas sustos como en 'El Conjuro'?", "terror", 1),
        ("¿Te interesa ciencia ficción como 'Interstellar'?", "ciencia ficcion", 1.5),
        ("¿Prefieres romances realistas?", "romance", 1),
        ("¿Te gustan aventuras como 'Indiana Jones'?", "aventura", 1),
        ("¿Adoras fantasía como 'El Señor de los Anillos'?", "fantasia", 2)
    ]

    for pregunta, genero, peso in preguntas:
        while True:
            respuesta = input(f"{pregunta} (si/no): ").lower().strip()
            if respuesta in ["si", "no"]:
                if respuesta == "si":
                    puntos[genero] += peso
                break
            print("⚠️ Responde solo 'si' o 'no'")

    max_puntos = max(puntos.values())
    generos_favoritos = [g for g, p in puntos.items() if p == max_puntos]
    
    if len(generos_favoritos) > 1:
        print(f"\n🔥 Empate entre {', '.join(generos_favoritos)}")
        genero_favorito = input("Elige tu género preferido: ").lower()
    else:
        genero_favorito = generos_favoritos[0]
    
    return genero_favorito

# ----------------------------
# CONFIGURACIÓN RÁPIDA
# ----------------------------
MODELO = "llama3"  # Modelo por defecto (usa :8b para versión ligera)
PROMPT = """Responde EN ESPAÑOL. Recomienda 3 películas de {genero} con:
1. **Título** (Año)
- *Sinopsis:* Breve descripción
- *Por qué verla:* Razón personalizada"""

# ----------------------------
# FUNCIÓN OPTIMIZADA
# ----------------------------
def recomendar_peliculas(genero):
    try:
        # Barra de progreso visual
        for _ in tqdm(range(15), desc="Buscando recomendaciones"):
            time.sleep(0.01)
        
        response = ollama.chat(
            model=MODELO,
            messages=[{
                "role": "user",
                "content": PROMPT.format(genero=genero)
            }],
            options={
                'temperature': 0.5,
                'num_predict': 250
            }
        )
        return response['message']['content']
    
    except Exception as e:
        return f"Error: {str(e)}\n⚠️ ¿Tienes Ollama instalado y el modelo descargado?"

# ----------------------------
# PROGRAMA PRINCIPAL
# ----------------------------
if __name__ == "__main__":
    # Verificación inicial
    try:
        ollama.list()
    except:
        print("❌ Ollama no está corriendo. Ejecuta primero 'ollama serve'")
        exit()

    genero = hacer_preguntas()
    print(f"\n🎯 Tu género favorito: {genero.upper()}")
    
    start_time = time.time()
    recomendaciones = recomendar_peliculas(genero)
    
    print("\n🍿 RECOMENDACIONES:")
    print(recomendaciones)
    print(f"\n⏱ Tiempo: {time.time() - start_time:.1f} segundos")