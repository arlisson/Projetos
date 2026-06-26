// Inclui a biblioteca iostream, que permite usar comandos de entrada e saída,
// como cout para imprimir mensagens na tela.
#include <iostream>

// Inclui o arquivo de cabeçalho "pilha.h".
// Esse arquivo provavelmente contém a declaração da classe pilha,
// o tipo TipoItem, a constante max_itens e os protótipos dos métodos.
#include "pilha.h"

// Permite usar elementos da biblioteca padrão sem precisar escrever std:: antes.
// Por exemplo, podemos escrever cout em vez de std::cout.
using namespace std;

// Construtor da classe pilha.
// O construtor é chamado automaticamente quando um objeto do tipo pilha é criado.
// Ele serve para inicializar os atributos da pilha.
pilha::pilha()
{
    // Define que, inicialmente, a pilha está vazia.
    // A variável tamanho representa a quantidade atual de elementos na pilha.
    // Como nenhum elemento foi inserido ainda, tamanho começa com 0.
    tamanho = 0;

    // Aloca dinamicamente um vetor de TipoItem com capacidade máxima max_itens.
    // Esse vetor será usado para armazenar os elementos da pilha.
    //
    // "estrutura" é um ponteiro que passa a apontar para esse vetor criado na memória.
    //
    // Exemplo:
    // Se max_itens for 100, será criado um vetor com 100 posições.
    estrutura = new TipoItem[max_itens];
}

// Destrutor da classe pilha.
// O destrutor é chamado automaticamente quando o objeto pilha deixa de existir.
// Ele serve para liberar recursos que foram alocados durante a execução.
pilha::~pilha()
{
    // Como no construtor foi usado "new[]" para criar um vetor dinamicamente,
    // aqui é necessário usar "delete[]" para liberar essa memória.
    //
    // Isso evita vazamento de memória, também chamado de memory leak.
    delete[] estrutura;
}

// Método que verifica se a pilha está cheia.
// Retorna true se a pilha estiver cheia.
// Retorna false se ainda houver espaço para inserir elementos.
bool pilha::esta_cheia()
{
    // A pilha estará cheia quando a quantidade de elementos armazenados,
    // representada por tamanho, for igual à capacidade máxima da pilha,
    // representada por max_itens.
    //
    // Exemplo:
    // Se max_itens = 100 e tamanho = 100,
    // significa que todas as posições do vetor já estão ocupadas.
    return (tamanho == max_itens);
}

// Método que verifica se a pilha está vazia.
// Retorna true se a pilha não possuir nenhum elemento.
// Retorna false se houver pelo menos um elemento na pilha.
bool pilha::esta_vazia()
{
    // A pilha estará vazia quando tamanho for igual a 0.
    //
    // Como tamanho representa a quantidade de elementos inseridos,
    // tamanho == 0 significa que nada foi colocado na pilha ainda
    // ou que todos os elementos já foram removidos.
    return (tamanho == 0);
}

// Método responsável por inserir um novo elemento na pilha.
// Esse método representa a operação push da pilha.
//
// Parâmetro:
// valor -> elemento que será inserido no topo da pilha.
void pilha::inserir(TipoItem valor)
{
    // Antes de inserir um elemento, é necessário verificar se a pilha já está cheia.
    // Se estiver cheia, não há espaço disponível no vetor.
    if (esta_cheia())
    {
        // Exibe uma mensagem informando que a inserção não pode ser realizada.
        cout << "A pilha está cheia, impossível inserir elemento" << endl;
    }
    else
    {
        // Insere o novo valor na posição indicada por tamanho.
        //
        // Como os índices de um vetor começam em 0, a variável tamanho
        // também funciona como o índice da próxima posição livre.
        //
        // Exemplo:
        // Se tamanho = 0, o valor será inserido em estrutura[0].
        // Se tamanho = 1, o valor será inserido em estrutura[1].
        // Se tamanho = 2, o valor será inserido em estrutura[2].
        estrutura[tamanho] = valor;

        // Após inserir o elemento, incrementa o tamanho da pilha.
        // Isso indica que a pilha agora possui um elemento a mais.
        tamanho++;
    }
} // Fim do método inserir, equivalente ao push.

// Método responsável por remover um elemento da pilha.
// Esse método representa a operação pop da pilha.
//
// Como a pilha segue o princípio LIFO,
// o elemento removido será sempre o último que foi inserido.
//
// Retorno:
// Retorna o elemento removido da pilha.
TipoItem pilha::remover()
{
    // Antes de remover um elemento, é necessário verificar se a pilha está vazia.
    // Se estiver vazia, não existe nenhum elemento para remover.
    if (esta_vazia())
    {
        // Exibe uma mensagem informando que não é possível remover.
        cout << "A pilha está vazia, impossível remover" << endl;

        // Retorna um valor sentinela para indicar erro.
        //
        // Neste caso, está sendo retornado -69.
        // Porém, isso só faz sentido se TipoItem for um tipo numérico,
        // como int ou float.
        //
        // Observação:
        // Em um código mais robusto, seria melhor tratar esse erro de outra forma,
        // como lançar uma exceção ou retornar um valor opcional.
        return -69;
    }
    else
    {
        // Decrementa o tamanho antes de acessar o elemento.
        //
        // Isso acontece porque tamanho representa a quantidade de elementos,
        // mas o índice do último elemento é sempre tamanho - 1.
        //
        // Exemplo:
        // Se existem 3 elementos na pilha:
        // estrutura[0], estrutura[1], estrutura[2]
        //
        // tamanho vale 3.
        // O último elemento está no índice 2.
        //
        // Ao fazer tamanho--, tamanho passa de 3 para 2,
        // exatamente o índice do último elemento.
        tamanho--;

        // Retorna o elemento que estava no topo da pilha.
        //
        // Esse elemento não é apagado fisicamente da memória,
        // mas deixa de fazer parte da pilha porque o tamanho foi reduzido.
        //
        // Na próxima inserção, essa posição poderá ser sobrescrita.
        return estrutura[tamanho];
    }

} // Fim do método remover, equivalente ao pop.

// Método responsável por imprimir os elementos da pilha na tela.
//
// Ele mostra os elementos armazenados no vetor desde a base da pilha
// até o topo da pilha.
void pilha::imprimir()
{
    // Imprime o início da representação visual da pilha.
    cout << "Pilha[";

    // Percorre todos os elementos válidos da pilha.
    //
    // O laço começa em i = 0, que representa a base da pilha,
    // e vai até i < tamanho.
    //
    // É importante usar i < tamanho, e não i < max_itens,
    // porque nem todas as posições do vetor podem estar ocupadas.
    for (int i = 0; i < tamanho; i++)
    {
        // Imprime o elemento armazenado na posição i.
        //
        // Um espaço é colocado após cada elemento para separar visualmente os valores.
        cout << estrutura[i] << " ";
    }

    // Fecha a representação visual da pilha e quebra a linha.
    cout << "]" << endl;
}

// Método que retorna a quantidade atual de elementos na pilha.
//
// Apesar do nome tamanho_pilha, ele não retorna a capacidade máxima da pilha.
// Ele retorna quantos elementos estão armazenados naquele momento.
TipoItem pilha::tamanho_pilha()
{
    // Retorna o valor da variável tamanho.
    //
    // Exemplo:
    // Se foram inseridos 5 elementos e nenhum foi removido,
    // tamanho será 5.
    return tamanho;
}