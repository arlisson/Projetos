<?php
session_start();
include_once('conexao.php');

if (!empty($_GET['id'])) {

    $id = $_GET['id'];
    $sql = "SELECT * FROM modalidade WHERE id =$id";

    $result = $conexao->query($sql);


    if ($result->num_rows > 0) {
        try {
            $sql_code = "DELETE FROM modalidade WHERE id=$id";
            $deletar = $conexao->query($sql_code);
            if (!$deletar) {
                throw new Exception("Erro ao excluir do banco de dados: " . $conexao->error);
            }
            //crianddo mensagem de sessão caso o código execute com sucesso
            $_SESSION['msg'] = "<p><h2 class = 'sucesso'>Modalidade excluída com sucesso!</h2></p>";
            header("Location:Listar_Modalidade.php");
            exit();
        } catch (Exception $e) {
            // trata exceções geradas durante a conexão
            $_SESSION['msg'] = "<p><h2 class = 'erro'>Erro ao Excluir modalidade: " . $e->getMessage() . "<h2></p>";
            header("Location:Listar_Modalidade.php");
            exit();
        }
    } else {
        $_SESSION['msg'] = "<p><h2  class = 'erro'>Modalidade Inexistente!</h2></p> ";
        header('Location:Listar_Modalidade.php');
    }

}
?>