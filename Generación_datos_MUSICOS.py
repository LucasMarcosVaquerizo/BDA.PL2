import csv
import random
import os
from datetime import date, timedelta

# ==========================================
# CONFIGURACIÓN DE REPRODUCIBILIDAD
# ==========================================
# Al fijar la semilla, garantizamos que el compañero obtenga los mismos CSVs
random.seed(42)

# ==========================================
# CONSTANTES DE VOLUMEN (Según enunciado)
# ==========================================
NUM_MUSICOS = 1_000_000
NUM_GRUPOS = 200_000
NUM_CONCIERTOS = 100_000
NUM_DISCOS = 1_000_000
NUM_ENTRADAS = 24_000_000
CANCIONES_POR_DISCO = 12

# ==========================================
# DICCIONARIOS DE DATOS PARA DIVERSIDAD
# ==========================================
INSTRUMENTOS = ['Guitarra', 'Bajo', 'Batería', 'Teclado', 'Voz', 'Saxo', 'Trompeta', 'Violín']
GENEROS = ['Rock', 'Pop', 'Jazz', 'Metal', 'Techno', 'Indie', 'Clásica', 'Salsa', 'Punk']
PAISES = ['España', 'Francia', 'Italia', 'Alemania', 'Reino Unido', 'Portugal', 'EEUU', 'Japón']
CIUDADES = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao', 'Zaragoza', 'Málaga', 'Murcia']
PROVINCIAS = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Vizcaya', 'Zaragoza', 'Málaga', 'Murcia']

OUT_DIR = "."

# ==========================================
# FUNCIONES DE APOYO
# ==========================================

def random_date_2025():
    """Genera fechas solo dentro del año 2025."""
    return (date(2025, 1, 1) + timedelta(days=random.randint(0, 364))).isoformat()

def random_time():
    """Genera duración de canciones entre 2 y 7 minutos."""
    mins = random.randint(2, 6)
    secs = random.randint(0, 59)
    return f"00:{mins:02d}:{secs:02d}"

# ==========================================
# GENERADORES DE ARCHIVOS CSV
# ==========================================

def generar_musicos():
    print("1/7 Generando Musicos.csv...")
    with open(os.path.join(OUT_DIR, 'musicos.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["codigo_musico", "DNI", "Nombre", "Direccion", "Codigo_Postal", "Ciudad", "Provincia", "telefono", "Instrumentos"])
        for i in range(1, NUM_MUSICOS + 1):
            # Usamos el índice i para asegurar DNI y nombres únicos
            writer.writerow([
                i, 
                f"{i:08d}{'TRWAGMYFPDXBNJZSQVHLCKE'[i%23]}", # Letra de DNI real
                f"Musico_{i}", 
                f"Calle Falsa {i}", 
                random.randint(10000, 52000), 
                random.choice(CIUDADES), 
                random.choice(PROVINCIAS), 
                random.randint(600000000, 799999999), 
                random.choice(INSTRUMENTOS)
            ])

def generar_grupos():
    print("2/7 Generando Grupos.csv...")
    with open(os.path.join(OUT_DIR, 'grupos.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Codigo_grupo", "Nombre", "Genero_musical", "Pais", "Sitio_web"])
        for i in range(1, NUM_GRUPOS + 1):
            writer.writerow([i, f"Grupo_{i}", random.choice(GENEROS), random.choice(PAISES), f"www.grupo{i}.es"])

def generar_conciertos():
    print("3/7 Generando Conciertos.csv...")
    with open(os.path.join(OUT_DIR, 'conciertos.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Codigo_concierto", "Fecha_realizacion", "Pais", "Ciudad", "Recinto"])
        for i in range(1, NUM_CONCIERTOS + 1):
            writer.writerow([i, random_date_2025(), random.choice(PAISES), random.choice(CIUDADES), f"Recinto_{i}"])

def generar_relacion_grupo_musico():
    print("4/7 Generando Grupo_Musico.csv (N:M)...")
    with open(os.path.join(OUT_DIR, 'grupo_musico.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Codigo_grupo", "codigo_musico"])
        # Asignamos 5 músicos fijos a cada grupo para cumplir el ratio 1M/200k
        musico_ptr = 1
        for g_id in range(1, NUM_GRUPOS + 1):
            for _ in range(5):
                writer.writerow([g_id, musico_ptr])
                musico_ptr += 1

def generar_relacion_grupo_conciertos():
    print("5/7 Generando Grupo_Concierto.csv (N:M)...")
    with open(os.path.join(OUT_DIR, 'grupo_concierto.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Codigo_grupo", "Codigo_concierto"])
        # Cada grupo toca en 10 conciertos (cumple el mínimo del enunciado)
        # 200.000 grupos * 10 = 2.000.000 de actuaciones en 100.000 eventos
        for g_id in range(1, NUM_GRUPOS + 1):
            start_c = (g_id * 7) % NUM_CONCIERTOS # Salto pseudoaleatorio estable
            for j in range(10):
                c_id = ((start_c + j) % NUM_CONCIERTOS) + 1
                writer.writerow([g_id, c_id])

def generar_discos_y_canciones():
    print("6/7 Generando Discos.csv y Canciones.csv...")
    with open(os.path.join(OUT_DIR, 'discos.csv'), 'w', newline='', encoding='utf-8') as fd, \
         open(os.path.join(OUT_DIR, 'canciones.csv'), 'w', newline='', encoding='utf-8') as fc:
        w_d = csv.writer(fd)
        w_c = csv.writer(fc)
        w_d.writerow(["Codigo_disco", "Titulo", "Fecha_edicion", "Genero", "Formato", "Codigo_grupo"])
        w_c.writerow(["Codigo_cancion", "Nombre", "Compositor", "Fecha_grabacion", "Duracion", "Codigo_disco"])
        
        c_id = 1
        for d_id in range(1, NUM_DISCOS + 1):
            g_id = random.randint(1, NUM_GRUPOS)
            w_d.writerow([d_id, f"Disco_{d_id}", random_date_2025(), random.choice(GENEROS), "Digital", g_id])
            for _ in range(CANCIONES_POR_DISCO):
                w_c.writerow([c_id, f"Cancion_{c_id}", f"Autor_{g_id}", random_date_2025(), random_time(), d_id])
                c_id += 1

def generar_entradas():
    print("7/7 Generando Entradas.csv (24 millones)...")
    with open(os.path.join(OUT_DIR, 'entradas.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Codigo_entrada", "Localidad", "Precio", "Usuario", "Codigo_concierto"])
        for i in range(1, NUM_ENTRADAS + 1):
            # Precio como float para evitar problemas con el tipo MONEY (depende de configuración regional)
            precio = round(random.uniform(15.0, 150.0), 2)
            writer.writerow([i, f"Zona_{random.randint(1,10)}", precio, f"User_{i}", random.randint(1, NUM_CONCIERTOS)])
            if i % 4_000_000 == 0:
                print(f"   ... {i} entradas procesadas")

if __name__ == "__main__":
    print("Iniciando creación de datos con semilla fija (Seed: 42)")
    generar_musicos()
    generar_grupos()
    generar_conciertos()
    generar_relacion_grupo_musico()
    generar_relacion_grupo_conciertos()
    generar_discos_y_canciones()
    generar_entradas()
    print("Proceso finalizado. Todos los archivos CSV están listos para el COPY.")