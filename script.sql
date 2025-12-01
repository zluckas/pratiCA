CREATE DATABASE IF NOT EXISTS db_pratica;
USE db_pratica;

/*------> TABELAS <------*/
CREATE TABLE IF NOT EXISTS cursos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios(
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    matricula BIGINT NOT NULL UNIQUE,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    ano VARCHAR(20) NOT NULL,
    turno VARCHAR(20) NOT NULL,
    categoria VARCHAR(20) NOT NULL,
    id_curso INT NOT NULL,
     
    FOREIGN KEY (id_curso) REFERENCES cursos(id)
);

CREATE TABLE IF NOT EXISTS horarios(
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    dias VARCHAR(100) NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_termino TIME NOT NULL,
    sala VARCHAR(50) NOT NULL,
    id_professor INT NOT NULL,

    FOREIGN KEY (id_professor) REFERENCES usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS usuario_horario(
    id_usuario INT NOT NULL,
    id_horario INT NOT NULL,
    PRIMARY KEY (id_usuario, id_horario),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_horario) REFERENCES horarios(id_horario)
);


/*-----> INSERTS <-----*/
INSERT INTO cursos VALUES 
(DEFAULT, 'Informática'),
(DEFAULT, 'Eletrotécnica'),
(DEFAULT, 'Têxtil'),
(DEFAULT, 'Vestuário');
