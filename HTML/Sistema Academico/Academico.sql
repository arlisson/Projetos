CREATE DATABASE academico;
use academico;

CREATE TABLE pessoa (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT ,
    matricula VARCHAR(12) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(40) NOT NULL,
    data_nascimento Date NOT NULL,
    data_matricula Date NOT NULL ,
    carga_horaria INT NOT NULL,
    email VARCHAR(200) NOT NULL,
    telefone VARCHAR(14) NOT NULL,  
    endereco Varchar (400) NOT NULL,
    UF VARCHAR(2) NOT NULL,    
    CEP VARCHAR(9) NOT NULL
);
CREATE TABLE afastamento (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    data_inicial Date NOT NULL,
    data_final Date NOT NULL,
    descricao VARCHAR(240),
    id_pessoa INT NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE atestado(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    motivo VARCHAR(250) NOT NULL,
    data_inicial Date NOT NULL,
    data_final Date NOT NULL,
    observacoes VARCHAR(250) NOT NULL,
    id_pessoa INT NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id) ON DELETE CASCADE ON UPDATE CASCADE
    
);
CREATE TABLE assiduidade (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    data Date NOT NULL,
    assiduidade BIT NOT NULL,
    id_pessoa INT NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE modalidade (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(125) NOT NULL UNIQUE,
    observacao VARCHAR(250)
);
CREATE TABLE reuniao (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_modalidade INT NOT NULL,
    data_reuniao Date NOT NULL,
    tipo VARCHAR(150) NOT NULL,
    FOREIGN KEY (id_modalidade) REFERENCES modalidade(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE reuniao_pessoa (
    id_pessoa INT NOT NULL UNIQUE,
    id_reuniao INT NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id),
    FOREIGN KEY (id_reuniao) REFERENCES reuniao(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE projeto (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(250) NOT NULL,
    descricao VARCHAR(250) NOT NULL,
    data_inicial Date NOT NULL,
    data_fim Date NOT NULL
);
CREATE TABLE pessoa_projeto(
    id_pessoa INT NOT NULL,
    id_projeto INT NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id),
    FOREIGN KEY (id_projeto) REFERENCES projeto(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE turma (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(250) NOT NULL
);
CREATE TABLE curso (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(250) NOT NULL,
    nome VARCHAR(120) NOT NULL,
    descricao VARCHAR(250) NOT NULL
);
CREATE TABLE grade (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_curso INT NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES curso(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE disciplina (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome VARCHAR(120) NOT NULL,
    descricao VARCHAR(250) NOT NULL
);
CREATE TABLE grade_disciplina (
    id_disciplina INT NOT NULL,
    id_curso INT NOT NULL,
    FOREIGN KEY (id_disciplina) REFERENCES disciplina(id),
    FOREIGN KEY (id_curso) REFERENCES curso(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE diario (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    data_entrega Date NOT NULL,
    id_disciplina INT NOT NULL,
    id_turma INT NOT NULL,
    FOREIGN KEY (id_disciplina) REFERENCES disciplina(id),
    FOREIGN KEY (id_turma) REFERENCES turma(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE pessoa_diario(
    id_pessoa INT NOT NULL,
    id_diario INT NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id),
    FOREIGN KEY (id_diario) REFERENCES diario(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE entrega_plano_ensino (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_pessoa INT NOT NULL,
    id_disciplina INT NOT NULL,
    data_entrega Date NOT NULL,
    acesso_turma BIT NOT NULL,
    FOREIGN KEY (id_disciplina) REFERENCES disciplina(id),
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE horario_atendimento (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    data_ini Date NOT NULL,
    data_fim Date NOT NULL,
    horario_ini Date NOT NULL,
    horario_fim Date NOT NULL
);
CREATE TABLE diario_horario(
    id_diario INT NOT NULL,
    id_horario INT NOT NULL,
    FOREIGN KEY (id_diario) REFERENCES diario(id),
    FOREIGN KEY (id_horario) REFERENCES horario_atendimento(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE projeto_horario(
    id_projeto INT NOT NULL,
    id_horario INT NOT NULL,
    FOREIGN KEY (id_projeto) REFERENCES projeto(id),
    FOREIGN KEY (id_horario) REFERENCES horario_atendimento(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE conselho (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    data_conselho Date NOT NULL,
    periodo INT NOT NULL,
    id_turma INT NOT NULL,
    id_modalidade INT NOT NULL,
    FOREIGN KEY (id_turma) REFERENCES turma(id),
    FOREIGN KEY (id_modalidade) REFERENCES modalidade(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE pessoa_conselho(
    id_pessoa INT NOT NULL,
    id_conselho INT NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id),
    FOREIGN KEY (id_conselho) REFERENCES conselho(id) ON DELETE CASCADE ON UPDATE CASCADE
);
