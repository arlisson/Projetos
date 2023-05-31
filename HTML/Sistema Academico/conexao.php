<?php

$user = 'root';
$password = '';
$database = 'academico';
$host = 'localhost';
$port = '3306';

try {
    // tenta conectar ao banco de dados
    $conexao = new mysqli($host, $user, $password, $database);

    // verifica se a conexão foi bem-sucedida
    if ($conexao->connect_error) {
        throw new Exception("Erro ao conectar ao banco de dados: " . $conexao->connect_error);
    }
    //echo "Conexão estabelcida com sucesso!";

} catch (Exception $e) {
    // trata exceções geradas durante a conexão
    echo "Erro: " . $e->getMessage();
}



?>