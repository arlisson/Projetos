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
    $titulo = $dados['titulo'];
    $obs = $dados['desc'];


    //Verificar se o comando SQL vai funcionar
    try {
        $sql_code = "INSERT INTO modalidade( titulo, observacao)
         VALUES ('$titulo','$obs')";
        //Executa o comando SQL
        $sql_query = $conexao->query($sql_code);

        if (!$sql_query) {
            throw new Exception("Erro ao executar inserção no banco de dados: " . $conexao->error);
        }

        //crianddo mensagem de sessão caso o código execute com sucesso
        $_SESSION['msg'] = "<p > <h2 class = 'sucesso'>Modalidade cadastrada com sucesso!</h2></p>";
        header("Location:Inserir_Modalidade.php");
        exit();

    } catch (Exception $e) {
        // trata exceções geradas durante a conexão
        $_SESSION['msg'] = "<p ><h2 class = 'erro'>Erro ao cadastrar modalidade: " . $e->getMessage() . "</h2></p>";
        header("Location:Inserir_Modalidade.php");
        exit();
    }

} else {
    $_SESSION['msg'] = "<p><h2 class = 'erro'>Erro ao cadastrar modalidade!</h2></p>";
    header("Location:Inserir_Modalidade.php");
    exit();
}



?>