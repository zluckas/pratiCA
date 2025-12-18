CREATE DATABASE IF NOT EXISTS db_pratica;
USE db_pratica;

-- =========================
-- Tabela usuarios (base)
-- =========================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    matricula INT UNIQUE,
    nome VARCHAR(50) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    categoria VARCHAR(20) NOT NULL
);

-- =========================
-- Tabela professores (herança JOINED)
-- =========================
CREATE TABLE professores (
    id_usuario INT PRIMARY KEY,
    CONSTRAINT fk_professor_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
);

-- =========================
-- Tabela cursos
-- =========================
CREATE TABLE cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

-- =========================
-- Tabela alunos (herança JOINED)
-- =========================
CREATE TABLE alunos (
    id_usuario INT PRIMARY KEY,
    ano VARCHAR(20) NOT NULL,
    turno VARCHAR(20) NOT NULL,
    id_curso INT NOT NULL,
    CONSTRAINT fk_aluno_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario),
    CONSTRAINT fk_aluno_curso
        FOREIGN KEY (id_curso)
        REFERENCES cursos(id)
);

-- =========================
-- Tabela horarios
-- =========================
CREATE TABLE horarios (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    id_professor INT NOT NULL,
    dias VARCHAR(50) NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_termino TIME NOT NULL,
    sala VARCHAR(50) NOT NULL,
    CONSTRAINT fk_horario_professor
        FOREIGN KEY (id_professor)
        REFERENCES professores(id_usuario)
);

-- =========================
-- Tabela associativa aluno_horario
-- =========================
CREATE TABLE aluno_horario (
    id_aluno INT NOT NULL,
    id_horario INT NOT NULL,
    PRIMARY KEY (id_aluno, id_horario),
    CONSTRAINT fk_aluno_horario_aluno
        FOREIGN KEY (id_aluno)
        REFERENCES alunos(id_usuario),
    CONSTRAINT fk_aluno_horario_horario
        FOREIGN KEY (id_horario)
        REFERENCES horarios(id_horario)
);
