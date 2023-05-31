<?php

session_start();

if (!empty($_GET['id'])) {

    $id = $_GET['id'];

}

?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Adicionar Afastamento</title>
    <style type="text/css">
        /* body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }*/
        h1,
        p,
        h3,
        h2,
        label,
        form,
        title {
            text-align: center;
        }

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

<body style="background-color: #FFFFFF;">
    <div class="inside">
    <div class="primeiro", class="segundo">
    <h1>Inserir Atestados</h1>
    </div>
    <?php
    //se existir mensagem de sessão faça...
    if (isset($_SESSION['msg'])) {
        echo $_SESSION['msg'];
        unset($_SESSION['msg']);
    }

    ?>
    <form action="Afastamento.php" method="POST">
        <input type="hidden" value="<?php echo $id ?>" name="id">

        <label style="display: block;">Descrição: </label>
<textarea placeholder="Digite a Descrição" name="desc" maxlength="240" required style="width: 300px; height: 70px;"></textarea>


        </p>
        <p>
            <label>Data Inicial: </label>
            <input type="date" placeholder="Digite a data inicial" name="data_i" required>
        </p>
        <p>
            <label>Data Final: </label>
            <input type="date" placeholder="Digite a data final" name="data_f" required>
        </p>
        <div class="primeiro", class="segundo">
        <p>
            <input type="submit" value="Adicionar" name="adicionar">

        </p>
        </div>
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
	</div>
</body>

</html>