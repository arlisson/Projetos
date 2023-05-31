<?php
//iniciando sessão
session_start();
include('conexao.php');
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Listar Pessoas</title>
    <style type="text/css">
        /* body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }*/

        .erro {
            color: red;
        }

        .sucesso {
            color: green;
        }

        h1,
        h2,
        h3,
        label,
        form,
        title {
            text-align: center;
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
    <div class="primeiro", class="segundo">
    <h1>Buscar Pessoa</h1>
    </div>
    <?php
    //se existir mensagem de sessão faça...
    if (isset($_SESSION['msg'])) {
        echo $_SESSION['msg'];
        unset($_SESSION['msg']);
    }

    ?>
    <form action="Exibir.php" method="POST">
        <div class="primeiro", class="segundo">
        <p>
            <label>Buscar por matrícula:</label>
            <input type="text" placeholder="Digite a matrícula" name="matricula" maxlength="11">
            <input type="submit" value="Buscar" name="buscar">
        </p>
        </div>
        <p>

            <?php
            if (isset($_SESSION['tabela'])) {
                echo $_SESSION['tabela'];
                unset($_SESSION['tabela']);
            }
            ?>
        </p>
		
        <p>
            <label>Menu: </label>

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
    </form>
    </div>
</body>

</html>