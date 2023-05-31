<?php
//iniciando sessão
session_start();

include_once('conexao.php');

$sql = "SELECT * FROM pessoa";
$result = $conexao->query($sql);

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inserir Pessoas</title>
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
        p,
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
    <p>
    <h1>Sistema Acadêmico</h1>
    </div>
    </p>
    <?php
    //se existir mensagem de sessão faça...
    if (isset($_SESSION['msg'])) {
        echo $_SESSION['msg'];
        unset($_SESSION['msg']);
    }

    ?>

<div class="primeiro", class="segundo">
    <h3>Adicionar Pessoas a Reunião</h3>
    <form action="Pessoa_R.php" method="POST">
        <input type="hidden" value="<?php echo $_GET['id'] ?>" name="id_reuniao">
        </div>
        <p>
            <label>Matrículas dos participante</label>

            <select name="id_pessoa" required>
                <option value="">Selecione uma Matricula...</option>
                <?php
                while ($dados = mysqli_fetch_assoc($result)) {

                    echo '                
            <option value="' . $dados['id'] . '">' . $dados['matricula'] . '</option>';

                }

                ?>

            </select>

        <p>
            <input type="submit" value="Cadastrar" name="cadastrar">
        </p>

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
    </form>
</div>
</body>

</html>