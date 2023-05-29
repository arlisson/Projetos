#include <iostream>
using namespace std;

int main()
{
    // Declara Variável
    int var1;

    // Declara ponteiro
    int *pont1;

    var1 = 5;

    // Faz ponteiro apontar para uma variável que já tem nome
    pont1 = &var1;

    cout << "Hello World" << endl;

    // imprimir variável
    // cout << var1 << endl;

    // Imprimir o endereço que o ponteiro aponta
    // cout << pont1 << endl;

    // imprimir o valor armazenado na variável que o ponteiro aponta ponteiro
    // cout << *pont1 << endl;

    // Cria um poteiro int e faz ele apontar para um espaço da memória que cabe um inteiro
    int *pont2 = new int;

    *pont2 = 10;

    cout << *pont2 << endl;
    return 0;
}
