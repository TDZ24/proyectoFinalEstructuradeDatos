import networkx as nx
import time
import random
from tqdm import tqdm
import ollama

# Grafo para los generos de peliculas
G = nx.Graph()
generos = {
    "accion": [], "comedia": [], "drama": [], "terror": [],
    "ciencia ficcion": [], "romance": [], "aventura": [], "fantasia": []
}
for genero in generos:
    G.add_node(genero, tipo="genero")

# Funcion para hacer las preguntas 
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


# Configuracion del promp

MODELO = "llama3"  
PROMPT = """Responde EN ESPAÑOL. Recomienda 3 películas {aleatoriedad} del género {genero} que no sean las típicas. Para cada una:
1. **Título** (Año)
- *Sinopsis:* 1 línea máxima
- *Dato curioso:* Algo interesante
- *Similar a:* Otra película parecida

Ejemplo:
1. **Coherence** (2013)
- *Sinopsis:* Una cena se transforma por un fenómeno cuántico.
- *Dato curioso:* Filmada en 5 noches con guión improvisado.
- *Similar a:* The Invitation"""


# Funcion para que actue el prompt
def recomendar_peliculas(genero):
    try:
        # Añade aleatoriedad al prompt
        aleatoriedades = [
            "poco convencionales",
            "que rara vez te recomiendan",
            "con giros inesperados"
        ]
        prompt_aleatorio = PROMPT.format(
            genero=genero,
            aleatoriedad=random.choice(aleatoriedades)
        )
        
        # Configuración para mayor creatividad
        response = ollama.chat(
            model=MODELO,
            messages=[{
                "role": "user",
                "content": prompt_aleatorio
            }],
            options={
                'temperature': 0.8,  # Más alto = más aleatorio (rango 0-1)
                'num_predict': 400,  # Más espacio para respuestas largas
                'seed': random.randint(1, 1000)  # Semilla aleatoria
            }
        )
        return response['message']['content']
    
    except Exception as e:
        return f"Error: {str(e)}"


# main
if __name__ == "__main__":
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