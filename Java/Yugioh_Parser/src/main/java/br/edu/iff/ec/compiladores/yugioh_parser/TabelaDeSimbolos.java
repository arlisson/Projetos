/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package br.edu.iff.ec.compiladores.yugioh_parser;

import java.util.HashMap;
import java.util.Map;

/**
 *
 * @author T-GAMER
 */
public class TabelaDeSimbolos {
    class EntradaTabelaDeSimbolos {
        String nome;
        
        private EntradaTabelaDeSimbolos(String nome) {
            this.nome = nome;
        }
    }
    
    private final Map<String, EntradaTabelaDeSimbolos> tabela;
    
    public TabelaDeSimbolos() {
        this.tabela = new HashMap<>();
    }
    
    public void adicionar(String nome) {
        tabela.put(nome, new EntradaTabelaDeSimbolos(nome));
    }
    
    public boolean existe(String nome) {
        return tabela.containsKey(nome);
    }
}
