import numpy as np
import pandas as pd
import os
from datetime import date, timedelta

# Semilla fija para garantizar la reproducibilidad de los datos
np.random.seed(42)

# -----------------------------------------------------------------------------
# CONSTANTES
# -----------------------------------------------------------------------------
N_MUSICOS    = 1_000_000   # Número total de músicos
N_GRUPOS     = 200_000     # Número total de grupos musicales
N_CONCIERTOS = 100_000     # Número total de conciertos
N_DISCOS     = 1_000_000   # Número total de discos
N_ENTRADAS   = 24_000_000  # Número total de entradas vendidas

# Géneros musicales
GENEROS = [
    'clásica', 'blues', 'jazz', 'rock&roll', 'góspel', 'soul',
    'rock', 'metal', 'funk', 'disco', 'techno', 'pop',
    'reggae', 'hiphop', 'salsa'
]

# países donde se celebran conciertos
PAISES = [
    'España', 'Francia', 'Alemania', 'Italia', 'Reino Unido',
    'Portugal', 'Países Bajos', 'Bélgica', 'Suecia', 'Noruega',
    'Dinamarca', 'Polonia', 'Argentina', 'México', 'Brasil',
    'Colombia', 'Chile', 'Japón', 'Australia', 'Canadá'
]

INSTRUMENTOS = [
    'guitarra', 'bajo', 'batería', 'teclado', 'violín',
    'trompeta', 'saxofón', 'flauta', 'voz', 'contrabajo',
    'acordeón', 'percusión'
]

# Directorio de salida para todos los ficheros CSV
DIR_SALIDA = 'musicos_db'
os.makedirs(DIR_SALIDA, exist_ok=True)

print("=" * 60)
print("  Generador de datos – BD MUSICOS")
print("=" * 60)

# =============================================================================
# 1. MÚSICOS
# Genera 1.000.000 de músicos con fecha de nacimiento aleatoria
# entre 1950 y 2000, e instrumento principal aleatorio.
# =============================================================================
print("\n[1/8] Generando músicos...")

ids_musicos = np.arange(1, N_MUSICOS + 1)

# Fechas de nacimiento: entre 01/01/1950 y 31/12/2000
fecha_origen = date(1950, 1, 1)
dias_aleatorios = np.random.randint(
    0, (date(2000, 12, 31) - fecha_origen).days, N_MUSICOS
)
fechas_nacimiento = [
    (fecha_origen + timedelta(int(d))).isoformat() for d in dias_aleatorios
]

df_musicos = pd.DataFrame({
    'id':               ids_musicos,
    'nombre':           [f'Musico_{i}' for i in ids_musicos],
    'fecha_nacimiento': fechas_nacimiento,
    'instrumento':      np.random.choice(INSTRUMENTOS, N_MUSICOS),
})
df_musicos.to_csv(f'{DIR_SALIDA}/musicos.csv', index=False)
print(f"  ✓ {N_MUSICOS:,} músicos generados → musicos.csv")

# =============================================================================
# 2. GRUPOS
# Genera 200.000 grupos musicales con género y año de formación aleatorios.
# El año de formación se restringe a antes de 2025 para coherencia.
# =============================================================================
print("\n[2/8] Generando grupos...")

ids_grupos = np.arange(1, N_GRUPOS + 1)

df_grupos = pd.DataFrame({
    'id':            ids_grupos,
    'nombre':        [f'Grupo_{i}' for i in ids_grupos],
    'genero':        np.random.choice(GENEROS, N_GRUPOS),
    'año_formacion': np.random.randint(1960, 2025, N_GRUPOS),
})
df_grupos.to_csv(f'{DIR_SALIDA}/grupos.csv', index=False)
print(f"  ✓ {N_GRUPOS:,} grupos generados → grupos.csv")

# =============================================================================
# 3. GRUPO_MUSICO (relación N:M entre grupos y músicos)
# Se asigna un número aleatorio de músicos (1-10) a cada grupo.
# Los músicos se escogen aleatoriamente con reemplazamiento del total.
# =============================================================================
print("\n[3/8] Generando relaciones grupo ↔ músico...")

# Número de músicos por grupo: distribución uniforme entre 1 y 10
musicos_por_grupo = np.random.randint(1, 11, N_GRUPOS)

# Expandir: cada grupo_id se repite tantas veces como músicos tiene
grupo_rep  = np.repeat(ids_grupos, musicos_por_grupo)
musico_asig = np.random.choice(ids_musicos, musicos_por_grupo.sum(), replace=True)

df_grupo_musico = pd.DataFrame({
    'grupo_id':  grupo_rep,
    'musico_id': musico_asig,
})
# Eliminar duplicados (un músico no puede estar dos veces en el mismo grupo)
df_grupo_musico.drop_duplicates(inplace=True)
df_grupo_musico.to_csv(f'{DIR_SALIDA}/grupo_musico.csv', index=False)
print(f"  ✓ {len(df_grupo_musico):,} relaciones grupo-músico → grupo_musico.csv")

# =============================================================================
# 4. CONCIERTOS
# Genera 100.000 conciertos en el año 2025, distribuidos entre 20 países.
# Hacemos que españa aparezca al menos una vez.
# =============================================================================
print("\n[4/8] Generando conciertos...")

ids_conciertos = np.arange(1, N_CONCIERTOS + 1)

# Fechas de concierto: distribuidas aleatoriamente a lo largo de 2025
inicio_2025 = date(2025, 1, 1)
dias_concierto = np.random.randint(0, 365, N_CONCIERTOS)
fechas_concierto = [
    (inicio_2025 + timedelta(int(d))).isoformat() for d in dias_concierto
]

# Distribución aleatoria entre los 20 países
paises_concierto = np.random.choice(PAISES, N_CONCIERTOS)

# Garantizar que España aparece al menos en un concierto
if 'España' not in paises_concierto:
    paises_concierto[0] = 'España'

df_conciertos = pd.DataFrame({
    'id':     ids_conciertos,
    'fecha':  fechas_concierto,
    'pais':   paises_concierto,
    'ciudad': [f'Ciudad_{i}' for i in range(N_CONCIERTOS)],
    'aforo':  np.random.randint(500, 100_001, N_CONCIERTOS),
})
df_conciertos.to_csv(f'{DIR_SALIDA}/conciertos.csv', index=False)
print(f"  ✓ {N_CONCIERTOS:,} conciertos generados → conciertos.csv")
print(f"    Países distintos: {len(set(paises_concierto))} (España presente: {'España' in paises_concierto})")

# =============================================================================
# 5. GRUPO_CONCIERTO (relación N:M entre grupos y conciertos)
# Restricciones:
#   a) Todos los grupos han realizado AL MENOS 10 conciertos.
#   b) Todos los conciertos deben estar asociados a AL MENOS 1 grupo.
#
# Estrategia:
#   1. Asignar 10 conciertos aleatorios a cada grupo (garantiza restricción a).
#   2. Detectar conciertos sin grupo asignado y asignarles uno al azar
#      (garantiza restricción b).
# =============================================================================
print("\n[5/8] Generando relaciones grupo ↔ concierto...")

# Paso 1: cada grupo participa en exactamente 10 conciertos (mínimo obligatorio)
gc_grupos   = np.repeat(ids_grupos, 10)
gc_conciertos = np.random.choice(ids_conciertos, N_GRUPOS * 10, replace=True)

df_grupo_concierto = pd.DataFrame({
    'grupo_id':     gc_grupos,
    'concierto_id': gc_conciertos,
}).drop_duplicates()

# Paso 2: verificar que todos los conciertos tienen al menos un grupo
conciertos_cubiertos = set(df_grupo_concierto['concierto_id'].unique())
conciertos_sin_grupo = np.array(list(set(ids_conciertos) - conciertos_cubiertos))

if len(conciertos_sin_grupo) > 0:
    df_extra = pd.DataFrame({
        'grupo_id':     np.random.choice(ids_grupos, len(conciertos_sin_grupo)),
        'concierto_id': conciertos_sin_grupo,
    })
    df_grupo_concierto = pd.concat(
        [df_grupo_concierto, df_extra], ignore_index=True
    ).drop_duplicates()

df_grupo_concierto.to_csv(f'{DIR_SALIDA}/grupo_concierto.csv', index=False)
print(f"  ✓ {len(df_grupo_concierto):,} relaciones grupo-concierto → grupo_concierto.csv")
print(f"    Conciertos sin grupo al inicio: {len(conciertos_sin_grupo)} → resueltos")

# =============================================================================
# 6. DISCOS
# Generamos 1.000.000 de discos del año 2025 con género aleatorio.
# Cada disco almacena el número de canciones que tendrá (media 12,
# con distribución normal, acotado entre 1 y 25).
# Los discos se asocian a grupos aleatorios.
# =============================================================================
print("\n[6/8] Generando discos...")

ids_discos = np.arange(1, N_DISCOS + 1)

# Número de canciones por disco: distribución normal media=12, desviación=2, rango [1,25]
n_canciones_por_disco = np.clip(
    np.round(np.random.normal(12, 2, N_DISCOS)).astype(int), 1, 25
)

df_discos = pd.DataFrame({
    'id':            ids_discos,
    'titulo':        [f'Disco_{i}' for i in ids_discos],
    'grupo_id':      np.random.choice(ids_grupos, N_DISCOS),
    'genero':        np.random.choice(GENEROS, N_DISCOS),  # distribución aleatoria uniforme
    'año':           2025,
    'num_canciones': n_canciones_por_disco,
})
df_discos.to_csv(f'{DIR_SALIDA}/discos.csv', index=False)
print(f"  ✓ {N_DISCOS:,} discos generados → discos.csv")
print(f"    Total canciones a generar: {n_canciones_por_disco.sum():,}")

# =============================================================================
# 7. CANCIONES
# Genera las canciones de cada disco.
# La duración de cada canción es aleatoria entre 2 min (120 s) y 7 min (420 s).
#
# Se genera por bloques de 10.000 discos para no saturar la memoria RAM,
# escribiendo en el CSV de forma incremental (modo 'append').
# =============================================================================
print("\n[7/8] Generando canciones (por bloques para optimizar memoria)...")

BLOQUE_DISCOS = 10_000   # Número de discos procesados por iteración
id_cancion    = 1        # Contador global de ID de canción
primera_vez   = True     # Controla si se escribe la cabecera del CSV

total_canciones_generadas = 0

for i in range(0, N_DISCOS, BLOQUE_DISCOS):
    # Rango de discos del bloque actual
    ids_bloque   = ids_discos[i : i + BLOQUE_DISCOS]
    n_canc_bloque = n_canciones_por_disco[i : i + BLOQUE_DISCOS]

    # Expandir: repetir el id del disco tantas veces como canciones tenga
    disco_repetido = np.repeat(ids_bloque, n_canc_bloque)
    n_total_bloque = len(disco_repetido)

    # Duración aleatoria en segundos: entre 120 s (2 min) y 420 s (7 min)
    duraciones = np.random.randint(120, 421, n_total_bloque)

    ids_canciones = np.arange(id_cancion, id_cancion + n_total_bloque)
    id_cancion   += n_total_bloque

    pd.DataFrame({
        'id':                ids_canciones,
        'titulo':            [f'Cancion_{k}' for k in ids_canciones],
        'disco_id':          disco_repetido,
        'duracion_segundos': duraciones,
    }).to_csv(
        f'{DIR_SALIDA}/canciones.csv',
        mode='a',
        header=primera_vez,
        index=False
    )
    primera_vez = False
    total_canciones_generadas += n_total_bloque

    if (i // BLOQUE_DISCOS) % 10 == 0:
        print(f"  … {min(i + BLOQUE_DISCOS, N_DISCOS):,} / {N_DISCOS:,} discos procesados")

print(f"  ✓ {total_canciones_generadas:,} canciones generadas → canciones.csv")

# =============================================================================
# 8. ENTRADAS
# Genera 24.000.000 de entradas distribuidas aleatoriamente entre todos
# los conciertos. El precio oscila entre 20 y 100 euros de forma aleatoria.
#
# Se genera por bloques de 2.000.000 de filas para no saturar la RAM,
# escribiendo en el CSV de forma incremental.
# =============================================================================
print("\n[8/8] Generando entradas (por chunks de 2M para optimizar memoria)...")

CHUNK_ENTRADAS = 2_000_000  # Entradas procesadas por iteración
id_entrada     = 1
primera_vez    = True

for inicio in range(0, N_ENTRADAS, CHUNK_ENTRADAS):
    n_chunk = min(CHUNK_ENTRADAS, N_ENTRADAS - inicio)

    pd.DataFrame({
        'id':           np.arange(id_entrada, id_entrada + n_chunk),
        # Distribución uniforme entre todos los conciertos existentes
        'concierto_id': np.random.choice(ids_conciertos, n_chunk),
        # Precio redondeado a 2 decimales, entre 20.00 y 100.00 €
        'precio':       np.round(np.random.uniform(20.0, 100.0, n_chunk), 2),
    }).to_csv(
        f'{DIR_SALIDA}/entradas.csv',
        mode='a',
        header=primera_vez,
        index=False
    )
    primera_vez = False
    id_entrada += n_chunk
    print(f"  … {min(inicio + CHUNK_ENTRADAS, N_ENTRADAS):,} / {N_ENTRADAS:,} entradas")

print(f"  ✓ {N_ENTRADAS:,} entradas generadas → entradas.csv")

# =============================================================================
# RESUMEN FINAL
# Muestra el listado de ficheros generados con su tamaño en MB.
# =============================================================================
print("\n" + "=" * 60)
print("  GENERACIÓN COMPLETADA – Ficheros en la carpeta 'musicos_db/'")
print("=" * 60)
print(f"\n{'Fichero CSV':<28} {'Tamaño (MB)':>12}")
print("-" * 42)
for fichero in sorted(os.listdir(DIR_SALIDA)):
    ruta = os.path.join(DIR_SALIDA, fichero)
    mb = os.path.getsize(ruta) / (1024 ** 2)
    print(f"  {fichero:<26} {mb:>10.1f} MB")

total_mb = sum(
    os.path.getsize(os.path.join(DIR_SALIDA, f)) / (1024 ** 2)
    for f in os.listdir(DIR_SALIDA)
)
print("-" * 42)
print(f"  {'TOTAL':<26} {total_mb:>10.1f} MB")
print("""
Ficheros generados:
  1. musicos.csv          → tabla musicos
  2. grupos.csv           → tabla grupos
  3. conciertos.csv       → tabla conciertos
  4. discos.csv           → tabla discos   (FK → grupos)
  5. canciones.csv        → tabla canciones (FK → discos)
  6. grupo_musico.csv     → tabla grupo_musico (FK → grupos, musicos)
  7. grupo_concierto.csv  → tabla grupo_concierto (FK → grupos, conciertos)
  8. entradas.csv         → tabla entradas (FK → conciertos)
""")