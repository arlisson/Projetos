<?php
session_start();
include_once('conexao.php');

if (isset($_POST['adicionar'])) {
    $id = $_POST['id'];
    $desc = $_POST['desc'];
    $data_i = $_POST['data_i'];
    $data_f = $_POST['data_f'];


    try {


        $sql_atestado = "INSERT INTO afastamento(data_inicial, data_final, descricao, id_pessoa)
         VALUES('$data_i','$data_f','$desc',$id)";
        $result = $conexao->query($sql_atestado);
        if (!$result) {
            throw new Exception("Erro ao adicionar afastamento: " . $conexao->error);
        }
        //crianddo mensagem de sessão caso o código execute com sucesso
        $_SESSION['msg'] = "<p><h2 class = 'sucesso'>Afastamento inserido com sucesso!</h2></p>";
        header("Location:Afastamento_Pessoa.php?id=" . $id);
        exit();
    } catch (Exception $e) {
        // trata exceções geradas durante a conexão
        $_SESSION['msg'] = "<p><h2 class = 'erro'>Erro Inserir Afastamento: " . $e->getMessage() . "</h2></p>";
        header("Location:Afastamento_Pessoa.php?id=" . $id);
        exit();
    }

}



?>