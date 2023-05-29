#include <iostream>
#include "pilha.h"

using namespace std;

pilha::pilha()
{ // construtor

    tamanho = 0;
    estrutura = new TipoItem[max_itens];
}

pilha::~pilha() // destrutor
{
    delete[] estrutura;
}

bool pilha::esta_cheia()
{

    return (tamanho == max_itens);
}

bool pilha::esta_vazia()
{

    return (tamanho == 0);
}

void pilha::inserir(TipoItem valor)
{
    if (esta_cheia())
    {
        cout << "A pilha está cheia, impossível inserir elemento" << endl;
    }
    else
    {
        estrutura[tamanho] = valor;
        tamanho++;
    }
} // push
TipoItem pilha::remover()
{

    if (esta_vazia())
    {
        cout << "A pilha está vazia, impossível remover" << endl;
        return -69;
    }
    else
    {
        tamanho--;
        return estrutura[tamanho];
    }

} // pop
void pilha::imprimir()
{

    cout << "Pilha[";
    for (int i = 0; i < tamanho; i++)
    {
        cout << estrutura[i] << " ";
    }
    cout << "]" << endl;
}
TipoItem pilha::tamanho_pilha()
{

    return tamanho;
}