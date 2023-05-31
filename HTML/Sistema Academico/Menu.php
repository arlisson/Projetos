<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menu</title>
    <style type="text/css">
        h1,
        h2,
        h3,
        label,
        form,
        title{
            text-align: center;
        }
        body {
    		border: 1px solid black;
            backgound-color: #CFF4D5;
            text-align: center;

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
    <h1>Sistema Acadêmico</h1>
    </div>
    <h2>Menu Principal</h2>


    <select name="menu" onchange="location = this.value;">
        <option value="">Selecione uma opção...</option>
        <option value="Cadastro_Pessoa.php">Cadastrar Pessoa</option>
        <option value="Listar_Pessoas.php">Listar Pessoas</option>
        <option value="Exibir_Pessoa.php">Buscar Pessoa</option>
        <option value="Inserir_Modalidade.php">Cadastrar Modalidade</option>
        <option value="Listar_Modalidade.php">Listar Modalidade</option>
        <option value="Registrar_Reuniao.php">Registrar Reunião</option>
        <option value="Listar_Reuniao.php">Listar Reunião</option>
        
    </select>
</div>
</body>

</html>