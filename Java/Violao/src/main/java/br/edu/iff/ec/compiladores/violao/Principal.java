/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package br.edu.iff.ec.compiladores.violao;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.DefaultErrorStrategy;
import org.antlr.v4.runtime.RecognitionException;
import org.antlr.v4.runtime.Token;

/**
 *
 * @author T-GAMER
 */
public class Principal {
    public static void main(String args[]) throws IOException{
        CharStream cs = CharStreams.fromFileName(args[0]) ;
        ViolaoLexer lexer = new ViolaoLexer(cs); //Depende do leitor de arquivos, no caso o CharStream cs                
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        ViolaoParser parser = new ViolaoParser(tokens);
        ViolaoParser.CriarCampoContext arvore = parser.criarCampo();
            

      
        Semantico s = new Semantico();
        s.visitCriarCampo(arvore);  

       
    
       
        
       if(SemanticoUtils.errosSemanticos.isEmpty()==false){
                //Escrevendo os erros gravados no LASemanticoUtils para um arquivo
                List<String> errosSemanticos = SemanticoUtils.errosSemanticos;
                for (var erroSemantico : errosSemanticos) {
                    throw new RuntimeException(erroSemantico + "\n");
                }   
            //Se não encontrar erros semanticos gera o HTML       
            }else{
                PrintWriter pw = new PrintWriter(new File(args[1]));
                GeradorDeCodigo g = new GeradorDeCodigo();
                g.visitCriarCampo(arvore);
                 try (PrintWriter pwc = new PrintWriter(args[1])) {
                    pwc.println(g.saida.toString());
                }catch(RuntimeException r){
                    r.printStackTrace(pw);
                }
                 
                
            }
        
        
        //parser.criarCampo();
        /*Token t = null;
        while((t=lexer.nextToken()).getType()!=Token.EOF){
            System.out.println("<"+ViolaoLexer.VOCABULARY.getDisplayName(t.getType())+","+t.getText()+">");
        }*/
        
    }
}
