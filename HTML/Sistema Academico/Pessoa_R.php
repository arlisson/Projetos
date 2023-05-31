<?php

session_start(); // iniciar sessão

//limpar buffer de saída
ob_start();

include_once('conexao.php');

//recebendo dados do formulário
$dados = filter_input_array(INPUT_POST, FILTER_DEFAULT);

//imprime os dados da array
var_dump($dados);

//verifica se se clicou no botão cadastrar
if (!empty($dados['cadastrar'])) {

    $id_pessoa = $dados['id_pessoa'];
    $id_reuniao = $dados['id_reuniao'];



    //Verificar se o comando SQL vai funcionar
    try {
        $sql_code = "INSERT INTO reuniao_pessoa( id_pessoa, id_reuniao)
         VALUES ('$id_pessoa','$id_reuniao')";
        //Executa o comando SQL
        $sql_query = $conexao->query($sql_code);

        if (!$sql_query) {
            throw new Exception("Erro ao executar inserção no banco de dados: " . $conexao->error);
        }

        //crianddo mensagem de sessão caso o código execute com sucesso
        $_SESSION['msg'] = "<p > <h2 class = 'sucesso'>Pessoa adicionada a reuinão sucesso!</h2></p>";
        header("Location:Pessoa_Reuniao.php?id=" . $id_reuniao);
        exit();

    } catch (Exception $e) {
        // trata exceções geradas durante a conexão
        $_SESSION['msg'] = "<p ><h2 class = 'erro'>Erro ao adicionar pessoa: " . $e->getMessage() . "</h2></p>";
        header("Location:Pessoa_Reuniao.php?id=" . $id_reuniao);
        exit();
    }

} else {
    $_SESSION['msg'] = "<p><h2 class = 'erro'>Erro ao adicionar pessoa!</h2></p>";
    header("Location:Pessoa_Reuniao.php?id=" . $id_reuniao);
    exit();
}



?>