CREATE DATABASE IF NOT EXISTS db_pratiCA;
USE db_pratiCA;

/*------> TABELAS <------*/
CREATE TABLE IF NOT EXISTS cursos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS turnos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS anos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS categorias(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios(
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(255) NOT NULL,
    email_usuario VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    id_categoria INT NOT NULL,
    id_curso INT NOT NULL,
    id_turno INT NOT NULL,
    id_ano INT NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id),    
    FOREIGN KEY (id_curso) REFERENCES cursos(id),
    FOREIGN KEY (id_turno) REFERENCES turnos(id),
    FOREIGN KEY (id_ano) REFERENCES anos(id)
);

CREATE TABLE IF NOT EXISTS professores(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS horarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_professor INT NOT NULL,
    dias VARCHAR(100) NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_termino TIME NOT NULL, 
    id_curso INT NOT NULL,
    id_turno INT NOT NULL,
    id_ano INT NOT NULL,
    FOREIGN KEY (id_professor) REFERENCES professores(id),    
    FOREIGN KEY (id_curso) REFERENCES cursos(id),
    FOREIGN KEY (id_turno) REFERENCES turnos(id),
    FOREIGN KEY (id_ano) REFERENCES anos(id)
);

/*-----> INSERTS <-----*/
INSERT INTO cursos VALUES 
(DEFAULT, 'Informática'),
(DEFAULT, 'Eletrotécnica'),
(DEFAULT, 'Têxtil'),
(DEFAULT, 'Vestuário');

INSERT INTO turnos VALUES 
(DEFAULT, 'Matutino'),
(DEFAULT, 'Vespertino');

INSERT INTO anos VALUES 
(DEFAULT, '1° ano'),
(DEFAULT, '2° ano'),
(DEFAULT, '3° ano'),
(DEFAULT, '4° ano');

INSERT INTO categorias VALUES 
(DEFAULT, 'Aluno'),
(DEFAULT, 'Professor');