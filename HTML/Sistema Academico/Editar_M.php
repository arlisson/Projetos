<?php
//iniciando sessão
session_start();
include_once('conexao.php');
$dados = filter_input_array(INPUT_POST, FILTER_DEFAULT);

if (isset($_POST['Editar'])) {

    $id = $dados['id'];
    $sql = "SELECT * FROM modalidade WHERE id = $id";
    $result = $conexao->query($sql);
    $dados_r = mysqli_fetch_assoc($result);

    $titulo = $dados['titulo'];
    $obs = $dados['obs'];



    if (isset($_POST['id'])) {

        //Verificar se o comando SQL vai funcionar
        try {
            $sql_code = "UPDATE modalidade SET titulo='$titulo', observacao='$obs' WHERE id=$id";
            //Executa o comando SQL
            $sql_query = $conexao->query($sql_code);
            if (!$sql_query) {
                throw new Exception("Erro ao executar Alteração no banco de dados: " . $conexao->error);
            }
            //crianddo mensagem de sessão caso o código execute com sucesso
            $_SESSION['msg'] = "<p > <h2 class = 'sucesso'>Modalidade alterada com sucesso!</h2></p>";
            header("Location:Editar_Modalidade.php?id=" . $id);
            exit();
        } catch (Exception $e) {
            // trata exceções geradas durante a conexão
            $_SESSION['msg'] = "<p ><h2 class = 'erro'>Erro ao alterar modalidade: " . $e->getMessage() . "</h2></p>";
            header("Location:Editar_Modalidade.php?id=" . $id);
            exit();
        }
    } else {
        $_SESSION['msg'] = "<p><h2 class = 'erro'>Erro ao alterar modalidade!</h2></p>";
        header("Location:Editar_Modalidade.php?id=" . $id);
        exit();
    }
}

?>