<?php
session_start();

include('conexao.php');

$sql_select = "SELECT * FROM reuniao";

//Executa o comando SQL
$sql_query = $conexao->query($sql_select);

?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de Reunião(ões)</title>
</head>

<body>
<div class="inside">
<div class="primeiro", class="segundo">
    <h1>Reunião(ões)</h1>
    </div>
    <?php
    //se existir mensagem de sessão faça...
    if (isset($_SESSION['msg'])) {
        echo $_SESSION['msg'];
        unset($_SESSION['msg']);
    }

    ?>
    <style>
        .erro {
            color: red;
        }

        .sucesso {
            color: green;
        }

        h1,
        h2,
        h3,
		p{
            text-align: center;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            border: 2px solid black;
        }

        th,
        td {
            border-collapse: collapse;
            text-align: center;
            padding: 8px;
            border: 2px solid black
        }
        body {
    		border: 1px solid black;
            backgound-color: #CFF4D5;
		}
        .inside {
  			border: 1px solid black;
  			background-color: #CFF4D5; 
  			padding: 10px;
		}
        .primeiro {
  			border-bottom: 2px solid black;
  			margin-bottom: 20px; /
		}
        .segundo {
  		margin-top: 20px;
}
    </style>

<div class="primeiro", class="segundo">
    <?php
    if ($sql_query->num_rows > 0) {
        echo "<table class=" . 'my-table' . ">
                <thread>
                    <tr>
                        <th scope=" . "col" . ">#</th>
                        <th scope=" . "col" . ">Referência de Modalidade</th>
                        <th scope=" . "col" . ">Data da Reunião</th> 
                        <th scope=" . "col" . ">tipo</th>                        
                        <th scope=" . "col" . ">AÇÕES</th>
                    </tr>
                </thread>
                <tbody>";
        while ($user_data = mysqli_fetch_assoc($sql_query)) {
            echo " <tr>";
            echo "<td>" . $user_data['id'] . "</td>";
            echo "<td>" . $user_data['id_modalidade'] . "</td>";
            echo "<td>" . $user_data['data_reuniao'] . "</td>";
            echo "<td>" . $user_data['tipo'] . "</td>";


            echo '<td>
            <select name="menu" onchange="location = this.value;">
            <option value="">Selecione uma Ação...</option>
                <option value="Pessoa_Reuniao.php?id=' . $user_data['id'] . '"> Adicionar Participantes</option>   
                <option value="Listar_Participantes.php?id=' . $user_data['id'] . '"> Listar Participantes</option>                     
                        
                </select></td>';

        }
        // echo "<td><a class= btn btn-primary btn-sm href=" . ' Editar_Pessoa.php?id=' . $user_data['id'] . "> Editar</a></td>";
    } else {
        echo "<p > <h2>Não há Reuniões registradas!</h2></p>";
    }

    ?>
    </tbody>
    </table>
    </div>
    <p>
        <label>Menu</label>

        <select name="menu" onchange="location = this.value;">
            <option value="">Selecione uma opção...</option>
            <option value="Menu.php">Menu Principal</option>
            <option value="Cadastro_Pessoa.php">Cadastrar Pessoa</option>
            <option value="Listar_Pessoas.php">Listar Pessoas</option>
            <option value="Exibir_Pessoa.php">Buscar Pessoa</option>
            <option value="Inserir_Modalidade.php">Cadastrar Modalidade</option>
            <option value="Listar_Modalidade.php">Listar Modalidade</option>
            <option value="Registrar_Reuniao.php">Registrar Reunião</option>
            <option value="Listar_Reuniao.php">Listar Reunião</option>

        </select>
    </p>

</div>
</body>

</html>