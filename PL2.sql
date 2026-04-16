
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
