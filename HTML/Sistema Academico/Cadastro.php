<?php

session_start(); // iniciar sessão

//limpar buffer de saída
ob_start();

include_once('conexao.php');

//recebendo dados do formulário
$dados = filter_input_array(INPUT_POST, FILTER_DEFAULT);

//imprime os dados da array
//var_dump($dados);

//verifica se se clicou no botão cadastrar
if (!empty($dados['cadastrar'])) {
    $matricula = $dados['matricula'];
    $nome = $dados['nome'];
    $cargo = $dados['cargo'];
    $data_n = $dados['data_n'];
    $data_m = $dados['data_m'];
    $carga_h = $dados['carga_h'];
    $email = $dados['email'];
    $telefone = $dados['telefone'];
    $endereco = $dados['endereco'];
    $uf = $dados['uf'];
    $cep = $dados['cep'];

    //Verificar se o comando SQL vai funcionar
    try {
        $sql_code = "INSERT INTO pessoa (matricula, nome, cargo, data_nascimento, data_matricula, carga_horaria, email, telefone, endereco, UF, CEP)
        VALUES ('$matricula','$nome','$cargo','$data_n','$data_m',$carga_h,'$email','$telefone','$endereco','$uf','$cep')";

        //Executa o comando SQL
        $sql_query = $conexao->query($sql_code);

        if (!$sql_query) {
            throw new Exception("Erro ao executar inserção no banco de dados: " . $conexao->error);
        }

        //crianddo mensagem de sessão caso o código execute com sucesso
        $_SESSION['msg'] = "<p > <h2 class = 'sucesso'>Pessoa cadastrada com sucesso!</h2></p>";
        header("Location:Cadastro_Pessoa.php");
        exit();

    } catch (Exception $e) {
        // trata exceções geradas durante a conexão
        $_SESSION['msg'] = "<p ><h2 class = 'erro'>Erro ao cadastrar pessoa: " . $e->getMessage() . "</h2></p>";
        header("Location:Cadastro_Pessoa.php");
        exit();
    }

} else {
    $_SESSION['msg'] = "<p><h2 class = 'erro'>Erro ao cadastrar pessoa!</h2></p>";
    header("Location:Cadastro_Pessoa.php");
    exit();
}



?>