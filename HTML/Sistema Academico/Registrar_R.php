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
if (!empty($dados['registrar'])) {
    $id_modalidade = $dados['modalidade'];
    $data = $dados['data_r'];
    $tipo = $dados['tipo'];


    //Verificar se o comando SQL vai funcionar
    try {

        $sql_code = "INSERT INTO reuniao( id_modalidade,data_reuniao,tipo)
         VALUES ('$id_modalidade','$data','$tipo')";
        //Executa o comando SQL
        $sql_query = $conexao->query($sql_code);

        if (!$sql_query) {
            throw new Exception("Erro ao executar inserção no banco de dados: " . $conexao->error);
        }

        //crianddo mensagem de sessão caso o código execute com sucesso
        $_SESSION['msg'] = "<p > <h2 class = 'sucesso'>Reunião registrada com sucesso!</h2></p>";
        header("Location:Registrar_Reuniao.php");
        exit();

    } catch (Exception $e) {
        // trata exceções geradas durante a conexão
        $_SESSION['msg'] = "<p ><h2 class = 'erro'>Erro ao registrar reunião: " . $e->getMessage() . "</h2></p>";
        header("Location:Registrar_Reuniao.php");
        exit();
    }

} else {
    $_SESSION['msg'] = "<p><h2 class = 'erro'>Erro ao registrar reunião!</h2></p>";
    header("Location:Registrar_Reuniao.php");
    exit();
}



?>