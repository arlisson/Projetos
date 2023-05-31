<?php
session_start();
include_once('conexao.php');

if (isset($_POST['adicionar'])) {
    $id = $_POST['id'];
    $motivo = $_POST['motivo'];
    $data_i = $_POST['data_i'];
    $data_f = $_POST['data_f'];
    $obs = $_POST['obs'];


    try {


        $sql_atestado = "INSERT INTO atestado(motivo,data_inicial,data_final,observacoes,id_pessoa)
    VALUES ('$motivo','$data_i','$data_f','$obs',$id)";
        $result = $conexao->query($sql_atestado);
        if (!$result) {
            throw new Exception("Erro ao adicionar atestado: " . $conexao->error);
        }
        //crianddo mensagem de sessão caso o código execute com sucesso
        $_SESSION['msg'] = "<p><h2 class = 'sucesso'>Atestado inserido com sucesso!</h2></p>";
        header("Location:Inserir_Atestado.php?id=" . $id);
        exit();
    } catch (Exception $e) {
        // trata exceções geradas durante a conexão
        $_SESSION['msg'] = "<p><h2 class = 'erro'>Erro Inserir atestado: " . $e->getMessage() . "</h2></p>";
        header("Location:Inserir_Atestado.php?id=" . $id);
        exit();
    }

}



?>