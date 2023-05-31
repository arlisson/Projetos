<?php

//iniciando sessão
session_start();
include_once('conexao.php');

if (!empty($_GET['id'])) {

    $id = $_GET['id'];
    $sql = "SELECT * FROM pessoa WHERE id =$id";

    $result = $conexao->query($sql);
    $dados = mysqli_fetch_assoc($result);

    if ($result->num_rows > 0) {

        $matricula = $dados['matricula'];
        $nome = $dados['nome'];
        $cargo = $dados['cargo'];
        $data_n = $dados['data_nascimento'];
        $data_m = $dados['data_matricula'];
        $carga_h = $dados['carga_horaria'];
        $email = $dados['email'];
        $telefone = $dados['telefone'];
        $endereco = $dados['endereco'];
        $uf = $dados['UF'];
        $cep = $dados['CEP'];
    } else {

        header('Location:Exibir_Pessoa.php');

    }


}



?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EDIÇÃO</title>
    <style type="text/css">
        /* body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }*/
        h1,
        h3,
        h2,
        label,
        form,
        title {
            text-align: center;
        }
        
        p {
        	text-align: left;
            padding-left: 230px;
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
    <h3>Edição</h3>
    </div>
    <form action="Editar.php" method="POST">

        <input type="hidden" value="<?php echo $id ?>" name="id">
        <p>
            <label>Nome</label>
            <input type="text" value="<?php echo $nome ?>" name="nome" required>
        </p>
        <p>
            <label>Matrícula</label>
            <input type="text" value="<?php echo $matricula ?>" name="matricula" required>
        </p>

        <p>
            <label>Cargo</label>
            <input type="text" value="<?php echo $cargo ?>" name="cargo" required>
        </p>
        <p>
            <label>Data de Nacimento</label>
            <input type="date" value="<?php echo $data_n ?>" name="data_n" required>
        </p>
        <p>
            <!--label>Data de Matrícula</label-->
            <input type="hidden" value="<?php echo $data_m ?>" name="data_m" required>
        </p>
        <p>
            <label>Carga Horária</label>
            <input type="text" value="<?php echo $carga_h ?>" name="carga_h" required>
        </p>
        <p>
            <label>E-mail</label>
            <input type="text" value="<?php echo $email ?>" name="email" required>
        </p>
        <p>
            <!-- Incluindo os arquivos da biblioteca Inputmask -->
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script
                src="https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/3.3.4/jquery.inputmask.bundle.min.js"></script>

            <label>Telefone</label>
            <input type="text" placeholder="Digite o telefone aqui" value="<?php echo $telefone ?>" name="telefone"
                maxLength="14" class="telefone" pattern="\(\d{2}\)\d{5}-\d{4}" required>
            <!-- Iniciando a biblioteca Inputmask -->
            <script>
                $(document).ready(function () {
                    $('.telefone').inputmask('(99)99999-9999');
                });
            </script>
        </p>
        <p>
            <label>Endereço</label>
            <input type="text" value="<?php echo $endereco ?>" name="endereco" required>
        </p>
        <p>
            <label>UF</label>
            <select name="uf">
                <option value="<?php echo $uf ?>">
                    <?php echo $uf ?>
                </option>
                <option value="AC">AC</option>
                <option value="AL">AL</option>
                <option value="AP">AP</option>
                <option value="AM">AM</option>
                <option value="BA">BA</option>
                <option value="CE">CE</option>
                <option value="DF">DF</option>
                <option value="ES">ES</option>
                <option value="GO">GO</option>
                <option value="MA">MA</option>
                <option value="MT">MT</option>
                <option value="MS">MS</option>
                <option value="MG">MG</option>
                <option value="PA">PA</option>
                <option value="PB">PB</option>
                <option value="PR">PR</option>
                <option value="PE">PE</option>
                <option value="PI">PI</option>
                <option value="RJ">RJ</option>
                <option value="RN">RN</option>
                <option value="RS">RS</option>
                <option value="RO">RO</option>
                <option value="RR">RR</option>
                <option value="SC">SC</option>
                <option value="SP">SP</option>
                <option value="SE">SE</option>
                <option value="TO">TO</option>
            </select>


        </p>
        <p>
            <label>CEP</label>
            <input type="text" value="<?php echo $cep ?>" name="cep" maxLength="9" required>
        </p>
        <p>
            <input type="submit" value="Editar" name="editar">

        </p>

        <!--a href="Exibir_Pessoa.php" type="submit" value="buscar"> Buscar Pessoa</a-->

    </form>
</div>
</body>

</html>