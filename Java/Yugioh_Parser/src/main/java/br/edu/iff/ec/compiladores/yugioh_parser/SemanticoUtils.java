/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package br.edu.iff.ec.compiladores.yugioh_parser;

import java.util.ArrayList;
import java.util.List;
import org.antlr.v4.runtime.Token;

/**
 *
 * @author T-GAMER
 */
public class SemanticoUtils {
    public static List<String> errosSemanticos = new ArrayList<>();
    
    //Funcao responsavel por adicionar os erros semanticos em uma lista
    public static void adicionarErroSemantico(Token t, String mensagem)
    {
        int linha = t.getLine();
        //System.out.println("Linha "+(linha-1)+": " +mensagem); 
        errosSemanticos.add(String.format("Erro póximo a linha %d: %s", (linha), mensagem));
    }
    
    
    
    
}
