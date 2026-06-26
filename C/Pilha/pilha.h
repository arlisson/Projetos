// Define um apelido para o tipo int.
//
// A partir daqui, sempre que o código usar TipoItem,
// o compilador entenderá como int.
//
// Isso é útil porque, se futuramente você quiser mudar o tipo de dado
// armazenado na pilha, por exemplo de int para float ou char,
// bastaria alterar esta linha.
//
// Exemplo:
// typedef float TipoItem;
//
// Assim, toda a pilha passaria a trabalhar com valores do tipo float.
typedef int TipoItem;

// Define uma constante inteira chamada max_itens.
//
// Essa constante representa a capacidade máxima da pilha,
// ou seja, a quantidade máxima de elementos que podem ser armazenados.
//
// Neste caso, a pilha poderá guardar até 100 elementos.
const int max_itens = 100;

// Declaração da classe pilha.
//
// Uma classe em C++ funciona como um modelo para criar objetos.
// Nesse caso, a classe pilha define os dados e as operações
// necessárias para representar uma estrutura de dados do tipo pilha.
//
// A pilha segue o princípio LIFO:
// Last In, First Out.
// Ou seja, o último elemento inserido é o primeiro a ser removido.
class pilha
{

private:
    // A seção private contém atributos e métodos que só podem ser acessados
    // dentro da própria classe.
    //
    // Isso significa que, fora da classe, não será possível acessar diretamente:
    // tamanho ou estrutura.
    //
    // Essa proteção é importante para evitar alterações indevidas nos dados
    // internos da pilha.

    // Armazena a quantidade atual de elementos existentes na pilha.
    //
    // Apesar de estar usando TipoItem, que neste código é int,
    // conceitualmente esse atributo representa uma quantidade.
    //
    // Exemplo:
    // Se a pilha está vazia, tamanho vale 0.
    // Se foram inseridos 3 elementos, tamanho vale 3.
    //
    // Ele também indica a próxima posição livre do vetor.
    TipoItem tamanho;

    // Ponteiro para TipoItem.
    //
    // Esse ponteiro será usado para apontar para um vetor alocado dinamicamente.
    //
    // Esse vetor será a estrutura interna onde os elementos da pilha serão guardados.
    //
    // No construtor da classe, provavelmente será feito algo como:
    // estrutura = new TipoItem[max_itens];
    //
    // Assim, estrutura apontará para um vetor com max_itens posições.
    TipoItem *estrutura;

public:
    // A seção public contém os métodos que podem ser acessados fora da classe.
    //
    // Esses métodos formam a interface da pilha.
    //
    // Ou seja, quem usa a classe pilha não acessa diretamente os atributos internos,
    // mas interage com a pilha por meio dessas funções públicas.

    // Construtor da classe pilha.
    //
    // O construtor é chamado automaticamente quando um objeto pilha é criado.
    //
    // Ele normalmente inicializa os atributos da classe.
    // Neste caso, espera-se que ele:
    // - inicialize tamanho com 0;
    // - aloque memória para o vetor estrutura.
    pilha();

    // Destrutor da classe pilha.
    //
    // O destrutor é chamado automaticamente quando um objeto pilha deixa de existir.
    //
    // Como a pilha usa alocação dinâmica de memória por meio do ponteiro estrutura,
    // o destrutor deve liberar essa memória usando delete[].
    //
    // Isso evita vazamento de memória.
    ~pilha();

    // Verifica se a pilha está cheia.
    //
    // Retorna true se a quantidade de elementos for igual a max_itens.
    // Retorna false caso ainda exista espaço disponível.
    bool esta_cheia();

    // Verifica se a pilha está vazia.
    //
    // Retorna true se tamanho for igual a 0.
    // Retorna false se existir pelo menos um elemento na pilha.
    bool esta_vazia();

    // Insere um novo valor no topo da pilha.
    //
    // Essa operação também é conhecida como push.
    //
    // Parâmetro:
    // valor -> elemento que será colocado na pilha.
    //
    // Antes de inserir, o método deve verificar se a pilha está cheia.
    void inserir(TipoItem valor);

    // Remove e retorna o elemento que está no topo da pilha.
    //
    // Essa operação também é conhecida como pop.
    //
    // Como a pilha segue o princípio LIFO,
    // o elemento removido será o último elemento inserido.
    //
    // Antes de remover, o método deve verificar se a pilha está vazia.
    TipoItem remover();

    // Imprime na tela os elementos armazenados na pilha.
    //
    // Normalmente, imprime os elementos da base até o topo.
    //
    // Esse método é útil para visualizar o estado atual da pilha.
    void imprimir();

    // Retorna a quantidade atual de elementos armazenados na pilha.
    //
    // Apesar de retornar TipoItem, conceitualmente faria mais sentido retornar int,
    // porque tamanho da pilha representa uma quantidade, não exatamente um item.
    TipoItem tamanho_pilha();
};