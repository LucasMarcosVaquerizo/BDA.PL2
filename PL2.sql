
--Cuestión 2

CREATE DATABASE matriculas;

CREATE TABLE estudiantes(
    carnet NUMERIC PRIMARY KEY,
    nombre TEXT,
    apellidos TEXT,
    creditos NUMERIC
);

CREATE TABLE asignaturas (
    codigo NUMERIC PRIMARY KEY,
    nombre TEXT,
    caracter TEXT,
    creditos NUMERIC
);

CREATE TABLE matriculas (
    carnet_estu NUMERIC,
    codigo_asig NUMERIC,
    nota NUMERIC,
    PRIMARY KEY (carnet_estu, codigo_asig),
    FOREIGN KEY (carnet_estu) REFERENCES estudiantes(carnet) ON DELETE RESTRICT,
    FOREIGN KEY (codigo_asig) REFERENCES asignaturas(codigo) ON DELETE RESTRICT
);

\timin
COPY estudiantes
FROM 'C:\datos_estudiantes.csv'
DELIMITER ','
CSV;

\timin
COPY asignaturas
FROM 'C:\datos_asignaturas.csv'
DELIMITER ','
CSV;

\timin
COPY matriculas
FROM 'C:\datos_matriculas.csv'
DELIMITER ','
CSV;

--Cuestión 3:

ANALYZE estudiantes;
ANALYZE asignaturas;
ANALYZE matriculas;

SELECT *
FROM pg_stats
WHERE tablename IN ('estudiantes','asignaturas','matriculas');

SELECT relname, reltuples, relpages
FROM pg_class
WHERE relname IN ('estudiantes','asignaturas','matriculas');

--Cuestión 4:

EXPLAIN
SELECT COUNT(*)
FROM estudiantes
WHERE creditos < 100;

ANALYZE estudiantes;
EXPLAIN SELECT COUNT(*) FROM estudiantes WHERE creditos < 100;

--Cuestión 5:

EXPLAIN ANALYZE
SELECT e.nombre
FROM estudiantes e
JOIN matriculas m ON e.carnet = m.carnet_estu
WHERE e.creditos = 150
  AND m.nota >= 5
GROUP BY e.carnet, e.nombre
HAVING COUNT(*) >= 3;

SELECT count(*)
from asignaturas;

--Cuestión 6:

EXPLAIN ANALYZE
SELECT a.nombre
FROM asignaturas a
JOIN matriculas m ON a.codigo = m.codigo_asig
JOIN estudiantes e ON e.carnet = m.carnet_estu
WHERE a.creditos = 10
  AND m.nota = 7
  AND e.creditos = 50;

-- Cuestión 8:

DROP TABLE IF EXISTS "Entradas", "Grupos_Tocan_Conciertos", "Grupo_Musico", "Canciones", "Discos", "Conciertos", "Grupos", "Musicos" CASCADE;
DROP TABLE IF EXISTS "Entradas" cascade;

CREATE TABLE "Musicos" (
    codigo_musico INT PRIMARY KEY,
    DNI CHAR(10) UNIQUE NOT NULL,
    Nombre TEXT NOT NULL,
    Direccion TEXT NOT NULL,
    Codigo_Postal INT NOT NULL,
    Ciudad TEXT NOT NULL,
    Provincia TEXT NOT NULL,
    telefono INT NOT NULL,
    Instrumentos TEXT NOT NULL
);

CREATE TABLE "Grupos" (
    Codigo_grupo INT PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Genero_musical TEXT NOT NULL,
    Pais TEXT NOT NULL,
    Sitio_web TEXT NOT NULL
);

CREATE TABLE "Conciertos" (
    Codigo_concierto INT PRIMARY KEY,
    Fecha_realizacion DATE NOT NULL,
    Pais TEXT NOT NULL,
    Ciudad TEXT NOT NULL,
    Recinto TEXT NOT NULL
);

CREATE TABLE "Discos" (
    Codigo_disco INT PRIMARY KEY,
    Titulo TEXT NOT NULL,
    Fecha_edicion DATE NOT NULL,
    Genero TEXT NOT NULL,
    Formato TEXT NOT NULL,
    Codigo_grupo INT,
    FOREIGN KEY (Codigo_grupo) REFERENCES "Grupos"(Codigo_grupo)
);

CREATE TABLE "Canciones" (
    Codigo_cancion INT PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Compositor TEXT NOT NULL,
    Fecha_grabacion DATE NOT NULL,
    Duracion TIME NOT NULL,
    Codigo_disco INT,
    FOREIGN KEY (Codigo_disco) REFERENCES "Discos"(Codigo_disco)
);

CREATE TABLE "Entradas" (
    Codigo_entrada INT PRIMARY KEY,
    Localidad TEXT NOT NULL,
    Precio MONEY NOT NULL,
    Usuario TEXT NOT NULL,
    Codigo_concierto INT,
    FOREIGN KEY (Codigo_concierto) REFERENCES "Conciertos"(Codigo_concierto)
);

CREATE TABLE "Grupos_Tocan_Conciertos" (
    Codigo_grupo INT,
    Codigo_concierto INT,
    PRIMARY KEY (Codigo_grupo, Codigo_concierto),
    FOREIGN KEY (Codigo_grupo) REFERENCES "Grupos"(Codigo_grupo),
    FOREIGN KEY (Codigo_concierto) REFERENCES "Conciertos"(Codigo_concierto)
);

CREATE TABLE "Grupo_Musico" (
    Codigo_grupo INT,
    codigo_musico INT,
    PRIMARY KEY (Codigo_grupo, codigo_musico),
    FOREIGN KEY (Codigo_grupo) REFERENCES "Grupos"(Codigo_grupo),
    FOREIGN KEY (codigo_musico) REFERENCES "Musicos"(codigo_musico)
);


COPY "Musicos" FROM 'C:/Tablas_MUSICOS/musicos.csv' CSV HEADER;
COPY "Grupos" FROM 'C:/Tablas_MUSICOS/grupos.csv' CSV HEADER;
COPY "Conciertos" FROM 'C:/Tablas_MUSICOS/conciertos.csv' CSV HEADER;
COPY "Discos" FROM 'C:/Tablas_MUSICOS/discos.csv' CSV HEADER;
COPY "Canciones" FROM 'C:/Tablas_MUSICOS/canciones.csv' CSV HEADER;
COPY "Entradas" FROM 'C:/Tablas_MUSICOS/entradas.csv' CSV HEADER;
COPY "Grupo_Musico" FROM 'C:/Tablas_MUSICOS/grupo_musico.csv' CSV HEADER;
COPY "Grupos_Tocan_Conciertos" FROM 'C:/Tablas_MUSICOS/grupo_concierto.csv' CSV HEADER;


ANALYZE;