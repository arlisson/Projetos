create database biblioteca;

use biblioteca;

create table pessoas(	
    cpf varchar(11)  primary key,
    nome varchar(255),
    endereco varchar(400)

);

create table livros (	
    isbn varchar(13) primary key,
    titulo varchar(255),
    editora varchar(255),
    categoria varchar(255)

);

create table emprestimos(
	id_emprestimo int auto_increment primary key,
	cpf_pessoa varchar(11),
    isbn_livro varchar(13),   
	data_emprestimo date,
    prazo date,
    situacao varchar(30) DEFAULT "EM ABERTO",
    data_entrega date,
	foreign key (cpf_pessoa) references pessoas (cpf) ,     
	foreign key (isbn_livro) references livros (isbn)
    
    
    on delete cascade
    on update cascade
    

);

