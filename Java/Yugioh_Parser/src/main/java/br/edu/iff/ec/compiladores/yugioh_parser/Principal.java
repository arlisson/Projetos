/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package br.edu.iff.ec.compiladores.yugioh_parser;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;

/**
 *
 * @author T-GAMER
 */
public class Principal {
    public static void main(String args[]) throws IOException{        
        
        CharStream cs = CharStreams.fromFileName(args[0]);
        ParserLexer lexer = new ParserLexer(cs);              
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        ParserParser parser =  new ParserParser(tokens);        
        ParserParser.CriarCartaContext arvore = parser.criarCarta();        
         
               
            //verificação semântica
            Semantico s = new Semantico();
            s.visitCriarCarta(arvore);  
                    
           
            
            //Se encontrar erros semanticos
            if(SemanticoUtils.errosSemanticos.isEmpty()==false){
                //Escrevendo os erros gravados no LASemanticoUtils para um arquivo
                List<String> errosSemanticos = SemanticoUtils.errosSemanticos;
                for (var erroSemantico : errosSemanticos) {
                    throw new RuntimeException(erroSemantico + "\n");
                }   
            //Se não encontrar erros semanticos gera o HTML       
            }else{
                PrintWriter pw = new PrintWriter(new File(args[1]));
                GeradorYGOHTML g = new GeradorYGOHTML();
                g.visitCriarCarta(arvore);
                 try (PrintWriter pwc = new PrintWriter(args[1])) {
                    pwc.println(g.saida.toString());
                }catch(RuntimeException r){
                    r.printStackTrace(pw);
                }
                 
                
            }
                
        
        //parser.criarCarta();
        
    }
    
}
