<?php
session_start();
include_once('conexao.php');

if (isset($_POST['editar'])) {

    $id = $_POST['id'];
    $matricula = $_POST['matricula'];
    $nome = $_POST['nome'];
    $cargo = $_POST['cargo'];
    $data_n = $_POST['data_n'];
    $data_m = $_POST['data_m'];
    $carga_h = $_POST['carga_h'];
    $email = $_POST['email'];
    $telefone = $_POST['telefone'];
    $endereco = $_POST['endereco'];
    $uf = $_POST['uf'];
    $cep = $_POST['cep'];


    try {
        $sql_update = "UPDATE pessoa SET matricula = '$matricula', nome='$nome', cargo = '$cargo', data_nascimento ='$data_n', data_matricula='$data_m', carga_horaria='$carga_h', email='$email',telefone='$telefone', endereco='$endereco', UF='$uf', CEP = '$cep'
    WHERE id = $id";
        $result = $conexao->query($sql_update);
        if (!$result) {
            throw new Exception("Erro ao alterar dados: " . $conexao->error);
        }
        //crianddo mensagem de sessão caso o código execute com sucesso
        $_SESSION['msg'] = "<p><h2 class = 'sucesso'>Dados alterados com sucesso!</h2></p>";
        header("Location:Listar_Pessoas.php");
        exit();
    } catch (Exception $e) {
        // trata exceções geradas durante a conexão
        $_SESSION['msg'] = "<p><h2 class = 'erro'>Erro ao alterar dados: " . $e->getMessage() . "</h2></p>";
        header("Location:Listar_Pessoas.php");
        exit();
    }

}



?>