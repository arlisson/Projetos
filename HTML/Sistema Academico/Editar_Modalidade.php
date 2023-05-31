<?php
//iniciando sessão
session_start();
include_once('conexao.php');

if (isset($_GET['id'])) {

    $id = $_GET['id'];
    $sql = "SELECT * FROM modalidade WHERE id = $id";
    $result = $conexao->query($sql);
    $dados = mysqli_fetch_assoc($result);

    $titulo = $dados['titulo'];
    $obs = $dados['observacao'];
    //echo $titulo, $obs;

}

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro de Modalidade</title>
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
    </p>
    </div>
    <?php
    //se existir mensagem de sessão faça...
    if (isset($_SESSION['msg'])) {
        echo $_SESSION['msg'];
        unset($_SESSION['msg']);
    }

    ?>

	<div class="primeiro", class="segundo">
    <h3>Edição de Modalidade</h3>
    </div>
    <form action="Editar_M.php" method="POST">
        <input type="hidden" value="<?php echo $id ?>" name="id" required>
        <p>
            <label>Título:</label>
            <input type="text" value="<?php echo $titulo ?>" name="titulo" required>
        </p>
        <p>
            <label>Observações:</label>
            <input type="text" value="<?php echo $obs ?>" name="obs" maxlength="250" style="width: 300px; height: 70px;"
                required>

        </p>


<div class="primeiro", class="segundo">
        <p>
            <input type="submit" value="Editar" name="Editar">
        </p>
</div>
        <p>
            <label>Menu:</label>

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