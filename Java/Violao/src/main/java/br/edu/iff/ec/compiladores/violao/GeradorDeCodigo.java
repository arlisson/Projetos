/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package br.edu.iff.ec.compiladores.violao;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author T-GAMER
 */
public class GeradorDeCodigo extends ViolaoBaseVisitor<Void>{
    StringBuilder saida;

    public GeradorDeCodigo() {
        saida = new StringBuilder();
    }

    @Override
    public Void visitCriarCampo(ViolaoParser.CriarCampoContext ctx) {
        
        
        
        saida.append("from tabulate import tabulate\n" +
"\n" +
"# Lista de graus das notas\n" +
"degrees = [\"I\", \"ii\", \"iii\", \"IV\", \"V\", \"vi\", \"vii°\"]\n" +
"\n"+"\nfields = []");
        
        for(int i=0; i<ctx.acorde.size();i++){
            switch(ctx.pc_acordes.get(i).getText()){
                
                case "C":
                    saida.append("\nc = [\"C\", \"Dm\", \"Em\", \"F\", \"G\", \"Am\", \"B°\"]");
                 
                    break;
                
                case "D":
                    saida.append("\nd = [\"D\", \"Em\", \"F#m\", \"G\", \"A\", \"Bm\", \"C#°\"]");
                    break;
                    
                case "E":
                    saida.append("\ne = [\"E\", \"F#m\", \"G#m\", \"A\", \"B\", \"C#m\", \"D#°\"]");
                    break;
                
                    
                case "F":
                    saida.append("\nf = [\"F\", \"Gm\", \"Am\", \"Bb\", \"C\", \"Dm\", \"E°\"]");
                    break;
                    
                case "G":
                    saida.append("\ng = [\"G\", \"Am\", \"Bm\", \"C\", \"D\", \"Em\", \"F#°\"]");
                    break;
                    
                    
                case "A":
                    saida.append("\na =  [\"A\", \"Bm\", \"C#m\", \"D\", \"E\", \"F#m\", \"G#°\"]");
                    break;
                    
                case "B":
                    saida.append("\nb =  [\"B\", \"C#m\", \"D#m\", \"E\", \"F#\", \"G#m\", \"A#°\"]");
                    break;
            }
           
        }
        
        for(int i = 0; i<ctx.pc_acordes.size();i++){
            saida.append("\nfields.append("+ctx.pc_acordes.get(i).getText().toLowerCase()+")\n");
        }
        
        if(ctx.pc_acordes.size()==1){
            saida.append("\nprint(\"{} Campo Harmônico de "+ctx.pc_acordes.get(0).getText()+" Maior {}\".format(\"-\"*14, \"-\"*14))");
        }else{
            saida.append("print(\"{} Campo Harmônico Maior {}\".format(\"-\"*14, \"-\"*14))");
        }
        
        saida.append("# Lista de listas para armazenar os dados da tabela\n" +
"data = [degrees]\n" +
"\n" +
"# Preenchendo a lista de listas com os acordes de cada campo harmônico maior\n" +
"for chords in fields:\n" +
"    data.append(chords)\n" +
"\n" +
"# Exibição dos dados formatados como tabela no terminal\n" +
"print(tabulate(data, headers=\"firstrow\", tablefmt=\"grid\"))");
        
        return super.visitCriarCampo(ctx); 
    }
    
    
    
    
}
