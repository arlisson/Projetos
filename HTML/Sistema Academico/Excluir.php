<?php
session_start();
include_once('conexao.php');

if (!empty($_GET['id'])) {

    $id = $_GET['id'];
    $sql = "SELECT * FROM pessoa WHERE id =$id";
    echo $id;
    $result = $conexao->query($sql);


    if ($result->num_rows > 0) {
        try {
            $sql_code = "DELETE FROM pessoa WHERE id=$id";
            $deletar = $conexao->query($sql_code);
            if (!$deletar) {
                throw new Exception("Erro ao excluir do banco de dados: " . $conexao->error);
            }
            //crianddo mensagem de sessão caso o código execute com sucesso
            $_SESSION['msg'] = "<p><h2 class = 'sucesso'>Pessoa excluída com sucesso!</h2></p>";
            header("Location:Exibir_Pessoa.php");
            exit();
        } catch (Exception $e) {
            // trata exceções geradas durante a conexão
            $_SESSION['msg'] = "<p><h2 class = 'erro'>Erro ao Excluir pessoa: " . $e->getMessage() . "<h2></p>";
            header("Location:Exibir_Pessoa.php");
            exit();
        }
    } else {
        $_SESSION['msg'] = "<p><h2  class = 'erro'>Pessoa Inexistente!</h2></p> ";
        header('Location:Exibir_Pessoa.php');
    }

}
?>