package Model;

import java.util.ArrayList;
import java.util.List;

public class Carrinho {
    private List<Produto> itens;

    public Carrinho() {
        this.itens = new ArrayList<>();
    }

    public void adicionar(Produto p) {
        itens.add(p);
    }

    public void limpar() {
        itens.clear();
    }

    public double getTotal() {
        return itens.stream().mapToDouble(Produto::getPreco).sum();
    }

    public int getQuantidade() {
        return itens.size();
    }

    public List<Produto> getItens() {
        return itens;
    }

    public void exibirResumo() {
        System.out.println("\n--- Itens no Carrinho ---");
        for (Produto p : itens) {
            System.out.println(p);
        }
        System.out.printf("Total: R$ %.2f\n", getTotal());
        System.out.println("Quantidade: " + getQuantidade());
    }
}
