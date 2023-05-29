
typedef int TipoItem;
const int max_itens = 100;

class pilha
{

private:
    TipoItem tamanho;
    TipoItem *estrutura;

public:
    pilha();  // construtor
    ~pilha(); // destrutor
    bool esta_cheia();
    bool esta_vazia();
    void inserir(TipoItem valor); // push
    TipoItem remover();           // pop
    void imprimir();
    TipoItem tamanho_pilha();
};
