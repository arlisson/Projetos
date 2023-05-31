<?php
session_start();

include('conexao.php');

$id = $_GET['id'];
$sql_assiduidade = "SELECT * FROM assiduidade WHERE id_pessoa = $id";

$sql = "SELECT * FROM pessoa WHERE id =$id";

//Executa o comando SQL
$sql_query = $conexao->query($sql_assiduidade);
$sql_m = $conexao->query($sql);
$result = mysqli_fetch_assoc($sql_m);

if ($sql_query->num_rows == 0) {
    $_SESSION['msg'] = "<p><h2 class= 'erro'>Essa pessoa não possui assiduidade(s)</h2></p>";
}


?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assiduidade</title>
    <style>
        .erro {
            color: red;
        }

        .sucesso {
            color: green;
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
</head>

<body>
<div class="inside">
    <h1>Lista de Assiduidade(s) de
        <?php echo $result['nome'] ?> Número de Matrícula:
        <?php echo $result['matricula'] ?>
    </h1>
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
        body {
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
    </style>
    <?php
    if ($sql_query->num_rows > 0) {
        echo " <table class=" . 'my-table' . ">
       <thread>
           <tr>
               <th scope=" . 'col' . ">#</th>               
               <th scope=" . 'col' . ">Data da Assiduidade</th>              
                               
           </tr>
       </thread>
       <tbody>";
    }
    while ($user_data = mysqli_fetch_assoc($sql_query)) {
        echo " <tr>";
        echo "<td>" . $user_data['id'] . "</td>";
        echo "<td>" . $user_data['data'] . "</td>";
    }

    ?>

    </tbody>
    </table>
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