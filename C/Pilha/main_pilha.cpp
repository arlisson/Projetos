#include <iostream>
#include "pilha.h"

using namespace std;

int main()
{

    pilha pilha1;
    TipoItem item;

    int opcao;

    cout << "-----------------Gerador de Pilha-----------------\n";

    do
    {
        cout << "\n0-Sair\n1-Inserir\n2-Remover\n3-Imprimir\n4-Tamanho da Pilha\n\n";
        cin >> opcao;

        if (opcao == 1)
        {
            cout << "Digite o número para inserir: ";
            cin >> item;
            pilha1.inserir(item);
        }
        else if (opcao == 2)
        {

            item = pilha1.remover();
            cout << "Elemento " << item << " removido!\n";
        }
        else if (opcao == 3)
        {
            pilha1.imprimir();
        }
        else if (opcao == 4)
        {
            cout << "Tamanho da pilha: " << pilha1.tamanho_pilha();
        }

    } while (opcao != 0);

    return 0;
}