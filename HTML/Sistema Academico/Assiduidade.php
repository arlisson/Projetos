<?php
session_start();
include_once('conexao.php');

if (isset($_POST['adicionar'])) {
    $id = $_POST['id'];
    $assiduidade = $_POST['assiduidade'];
    $data = $_POST['data'];



    try {


        $sql_assiduidade = "INSERT INTO assiduidade(`data`, `assiduidade`, `id_pessoa`)
         VALUES ('$data','$assiduidade',$id)";
        $result = $conexao->query($sql_assiduidade);
        if (!$result) {
            throw new Exception("Erro ao adicionar atestado: " . $conexao->error);
        }
        //crianddo mensagem de sessão caso o código execute com sucesso
        $_SESSION['msg'] = "<p><h2 class = 'sucesso'>Assiduidade Registrada!</h2></p>";
        header("Location:Assiduidade_Pessoa.php?id=" . $id);
        exit();
    } catch (Exception $e) {
        // trata exceções geradas durante a conexão
        $_SESSION['msg'] = "<p><h2 class = 'erro'>Erro ao registrar Assiduidade: " . $e->getMessage() . "</h2></p>";
        header("Location:Assiduidade_Pessoa.php" . $id);
        exit();
    }

}



?>