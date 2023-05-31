<?php
//iniciando sessão
session_start();

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro de Pessoas</title>
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
        title,
        div {
            text-align: center;
        }

        p {
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
            margin-bottom: 20px;/
        }

        .segundo {
            margin-top: 20px;
        }
    </style>


</head>

<body>
    <div class="inside">
        <div class="primeiro" , class="segundo">
            <p>
            <h1>Sistema Acadêmico</h1>
            </p>
        </div>
        <div class="primeiro" , class="segundo">
            <h3>Cadastrar Pessoa </h3>
        </div>
        <?php
        //se existir mensagem de sessão faça...
        if (isset($_SESSION['msg'])) {
            echo $_SESSION['msg'];
            unset($_SESSION['msg']);
        }

        ?>


        <h3>Insira os Dados: </h3>
        <form action="Cadastro.php" method="POST">
            <p>
                <label>Nome: </label>
                <input type="text" placeholder="Digite o nome" name="nome" required>
            </p>
            <p>
                <label>Matrícula: </label>
                <input type="text" placeholder="Digite a matrícula" name="matricula" maxLength="11" required>
            </p>

            <p>
                <label>Cargo</label>
                <input type="text" placeholder="Digite o cargo" name="cargo" required>
            </p>
            <p>
                <label>Data de Nacimento: </label>
                <input type="date" placeholder="Digite a data de nascimento" name="data_n" required>
            </p>
            <p>
                <!--label>Data de Matrícula</label-->
                <input type="hidden" placeholder="Digite a data da matrícula" name="data_m"
                    value="<?php echo date("Y-m-d") ?>" required>
            </p>
            <p>
                <label>Carga Horária: </label>
                <input type="text" placeholder="Digite a carga horária" name="carga_h" required>
            </p>
            <p>
                <label>E-mail: </label>
                <input type="text" placeholder="Digite o e-mail" name="email" required>
            </p>
            <p>
                <!-- Incluindo os arquivos da biblioteca Inputmask -->
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                <script
                    src="https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/3.3.4/jquery.inputmask.bundle.min.js"></script>

                <label>Telefone: </label>
                <input type="text" placeholder="Digite o telefone" name="telefone" maxLength="14" class="telefone"
                    pattern="\(\d{2}\)\d{5}-\d{4}" required>
                <!-- Iniciando a biblioteca Inputmask -->
                <script>
                    $(document).ready(function () {
                        $('.telefone').inputmask('(99)99999-9999');
                    });
                </script>
            </p>
            <p>
                <label>Endereço: </label>
                <textarea placeholder="Digite o endereço (rua, bairro, complemento, número, cidade)" name="endereco"
                    maxlength="240" required style="width: 300px; height: 70px;"></textarea>
            </p>
            <p>
                <label>UF: </label>

                <select name="uf" required="required">
                    <option value="">Selecione uma UF</option>
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
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                <script
                    src="https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/3.3.4/jquery.inputmask.bundle.min.js"></script>
                <label>CEP: </label>
                <input type="text" placeholder="Digite o CEP" name="cep" class="cep" maxLength="9" pattern="\d{5}-\d{3}"
                    required>
                <script>
                    $(document).ready(function () {
                        $('.cep').inputmask('99999-999');
                    });
                </script>
            </p>
            <div class="primeiro" , class="segundo">
                <p>
                    <input type="submit" value="Cadastrar" name="cadastrar">
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
        </form>
    </div>
</body>

</html>