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
if (isset($dados['buscar'])) {
    $matricula = $dados['matricula'];

    //Verificar se o comando SQL vai funcionar
    try {
        $sql_select = "SELECT * FROM pessoa WHERE matricula = '$matricula'";

        //Executa o comando SQL
        $sql_query = $conexao->query($sql_select);
        $result = mysqli_fetch_assoc($sql_query);
        if (!$sql_query) {
            throw new Exception("Erro ao executar busca no banco de dados: " . $conexao->error);
        }

        if ($sql_query->num_rows != 0) {
            //crianddo mensagem de sessão caso o código execute com sucesso


            // $_SESSION['msg'] = "<p class = 'sucesso'>Pessoa encontrada com sucesso!</p>";
            $_SESSION['tabela'] = '
            <style>         
                
              
            table{       
                border-collapse: collapse;    
            width: 100%;           
            border: 2px solid black;         
            }

            th, td {
                border-collapse: collapse;    
            text-align: center;
            padding: 8px;
            border: 2px solid black
            }            

           
            </style>
            
            <table class = ' . "my-table" . ' >
            <thread>
            <tr>
            <th scope="col">#</th>
            <th scope="col">Matrícula</th>
            <th scope="col">Nome</th>
            <th scope="col">Cargo</th>
            <th scope="col">Data de Nascimento</th>
            <th scope="col">Data de Matrícula</th>
            <th scope="col">Carga Horária</th>
            <th scope="col">E-mail</th>
            <th scope="col">Telefone</th>
            <th scope="col">Endereço</th>
            <th scope="col">UF</th>
            <th scope="col">CEP</th>
            <th scope="col">AÇÕES</th>
            </tr>
            </thread>
            <tbody>
            <tr>
            <td>' . $result['id'] . '</td>
            <td>' . $result['matricula'] . '</td>
            <td>' . $result['nome'] . '</td>
            <td>' . $result['cargo'] . '</td>
            <td>' . $result['data_nascimento'] . '</td>
            <td>' . $result['data_matricula'] . '</td>
            <td>' . $result['carga_horaria'] . '</td>
            <td>' . $result['email'] . '</td>
            <td>' . $result['telefone'] . '</td>
            <td>' . $result['endereco'] . '</td>
            <td>' . $result['UF'] . '</td>
            <td>' . $result['CEP'] . '</td>
            <td>
            <select name="menu" onchange="location = this.value;">
                <option value="">Selecione uma Ação...</option>
                <option value="Editar_Pessoa.php?id=' . $result['id'] . '"> Editar</option>
                <option value="Excluir.php?id=' . $result['id'] . '"> Excluir</option>
                <option value="Inserir_Atestado.php?id=' . $result['id'] . '"> Inserir atestado
                </option>
                <option value="Listar_Atestado.php?id=' . $result['id'] . '">Listar atestado
                </option>
                <option value="Afastamento_Pessoa.php?id=' . $result['id'] . '">Registrar Afastamento
                </option> 
                <option value="Listar_Afastamento.php?id=' . $result['id'] . '">Listar Afastamento
                </option>
                <option value="Assiduidade_Pessoa.php?id=' . $result['id'] . '">Registrar Assiduidade
                </option>
                <option value="Listar_Assiduidade.php?id=' . $result['id'] . '">Listar Assiduidade</td>
                </option>
            </select>
           
            
            </tr>
            </tbody>
            </table>';


            header("Location:Exibir_Pessoa.php");
            exit();
        } else {
            $_SESSION['msg'] = "<p><h2 class = 'erro'>Nenhuma pessoa encontrada</h2></p>";
            header("Location:Exibir_Pessoa.php");
            exit();
        }


    } catch (Exception $e) {
        // trata exceções geradas durante a conexão
        $_SESSION['msg'] = "<p><h2 class = 'erro'>Erro ao buscsar pessoa: " . $e->getMessage() . "</h2></p>";
        header("Location:Exibir_Pessoa.php");
        exit();
    }

} else {
    $_SESSION['msg'] = "<p ><h2 class = 'erro'>Erro ao buscar pessoa!</h2></p>";
    header("Location:Exibir_Pessoa.php");
    exit();
}



?>