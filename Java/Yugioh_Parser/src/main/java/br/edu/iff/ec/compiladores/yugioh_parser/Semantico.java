/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package br.edu.iff.ec.compiladores.yugioh_parser;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.antlr.v4.runtime.ANTLRErrorListener;
import org.antlr.v4.runtime.Token;

/**
 *
 * @author T-GAMER
 */
public class Semantico extends ParserBaseVisitor<Void> {
     public TabelaDeSimbolos tabela;
   
    @Override
    public Void visitCriarCarta(ParserParser.CriarCartaContext ctx) {
        
        
        //lista de monstros e magias, apenas para testes
        List<Carta_Monstro> list_carta_monstro = new ArrayList<>();
        List<Carta_Magica> list_carta_magica= new ArrayList<>();
        
        String mensagem;
        
        
        String nome_carta,tipo_carta,atributo,desc,tipo;
        int level;
        int atk, def;      
        String img;
        int auxatk = 0;
        int auxdef = 0;
        int auxlevel=0;
        //criando tabela de simbolos
        tabela = new TabelaDeSimbolos();
        
        //verificação de carta de monstro
        for(int i=0; i<ctx.tipo_carta.size();i++){ 
           
            tipo= ctx.tipo.get(i).getText();
            tipo_carta= ctx.tipo_carta.get(i).getText();
            atributo = ctx.atributo.get(i).getText();
            desc = ctx.desc.get(i).getText();
            nome_carta = ctx.monstro_nome.get(i).getText();               
            
            //não podem existir cartas de monstro com nome igual
            //verifica se o nome do monstro está na tabela de simbolos
            if(!tabela.existe(nome_carta)){
            //se não estiver, será adicionado
                tabela.adicionar(nome_carta);
                
            }else{
                //se estiver cria uma mensagem de erro e adiciona a lista de mensagens de erro
                mensagem = String.format("O nome %s já foi usado em outra carta!",nome_carta );
                SemanticoUtils.adicionarErroSemantico(ctx.monstro_nome.get(i), mensagem);
            }
            img = ctx.png.get(i).getText();
            //não podem existir cartas de monstro com imagem igual
            //verifica se a imagem do monstro está na tabela de simbolos
             if(!tabela.existe(img)){
                 //se não estiver, será adicionado
                tabela.adicionar(img);
                
            }else{
                //se estiver cria uma mensagem de erro e adiciona a lista de mensagens de erro
                mensagem = String.format("A imagem %s já foi usada em outra carta!",img );
                SemanticoUtils.adicionarErroSemantico(ctx.png.get(i), mensagem);
            }  
            
             
             
            if(ctx.DIGITO().get(auxlevel).getText().contains("missing")){
                mensagem = ("Erro de declaração, level do monstro não encontrado!");
                SemanticoUtils.adicionarErroSemantico(ctx.level.get(i), mensagem);

            }else{
                  level= Integer.parseInt(ctx.level.get(i).getText());
                if(level>12){
                    mensagem = String.format("O Level do Monstro %s não pode ser superior a 12!",nome_carta );
                    SemanticoUtils.adicionarErroSemantico(ctx.level.get(i), mensagem);
                }else if(level<0){
                    mensagem = String.format("O Level do Monstro %s não pode ser Negativo!",nome_carta );
                    SemanticoUtils.adicionarErroSemantico(ctx.level.get(i), mensagem);
                }  
               
              auxlevel+=3;
            }
            
            if(ctx.DIGITO().get(auxatk+1).getText().contains("missing")){
                mensagem = ("Erro de declaração, ataque do monstro não encontrado!");
                SemanticoUtils.adicionarErroSemantico(ctx.atk.get(i), mensagem);

            }else{
                    atk = Integer.parseInt(ctx.atk.get(i).getText());
                if(atk>999999){
                    mensagem = String.format("O ATK do Monstro %s não pode ser superior a 999999!",nome_carta );
                    SemanticoUtils.adicionarErroSemantico(ctx.atk.get(i), mensagem);
                }else if(atk<0){
                    mensagem = String.format("O ATK do Monstro %s não pode ser negaivo!",nome_carta );
                    SemanticoUtils.adicionarErroSemantico(ctx.atk.get(i), mensagem);
                }
              auxatk+=3;
            }
            
            if(ctx.DIGITO().get(auxdef+2).getText().contains("missing")){
                mensagem = ("Erro de declaração, defesa do monstro não encontrado!");
                SemanticoUtils.adicionarErroSemantico(ctx.def.get(i), mensagem);

            }else{
                    def = Integer.parseInt(ctx.def.get(i).getText());
                if(def>999999){
                    mensagem = String.format("A DEF do Monstro %s não pode ser superior a 999999!",nome_carta );
                    SemanticoUtils.adicionarErroSemantico(ctx.def.get(i), mensagem);
                }else if(def<0){
                    mensagem = String.format("A DEF do Monstro %s não pode ser Negativa!",nome_carta );
                    SemanticoUtils.adicionarErroSemantico(ctx.def.get(i), mensagem);
                }
                auxdef+=3;
            }
           /*list_carta_monstro.add(new Carta_Monstro(tipo_carta,nome_carta,level,atributo,tipo,atk,def,desc,img,
             ctx.pc_card.get(i).getText(),ctx.pc_name.get(i).getText(),ctx.pc_level.get(i).getText(),ctx.pc_atributo.get(i).getText(),
           ctx.pc_atk.get(i).getText(),ctx.pc_def.get(i).getText(),ctx.pc_desc.get(i).getText(),ctx.pc_image.get(i).getText(),
           ctx.pc_tipo.get(i).getText()));*/
            
           
           
                        
        }
        //verificação de carta magica
        for(int i=0; i<ctx.tipo_cartam.size();i++){
            nome_carta = ctx.magic_mone.get(i).getText();
            tipo_carta = ctx.tipo_cartam.get(i).getText();
            desc = ctx.desc_m.get(i).getText();
            //idem carta de monstro, porém para carta magica
            if(!tabela.existe(nome_carta)){
                tabela.adicionar(nome_carta);
                
            }else{
                mensagem = String.format("O nome %s já foi usado em outra carta!",nome_carta );
                SemanticoUtils.adicionarErroSemantico(ctx.magic_mone.get(i), mensagem);
            }
            img = ctx.magic_png.get(i).getText();
             if(!tabela.existe(img)){
                tabela.adicionar(img);
                
            }else{
                mensagem = String.format("A imagem %s já foi usada em outra carta!",img );
                SemanticoUtils.adicionarErroSemantico(ctx.magic_png.get(i), mensagem);
            }
          // list_carta_magica.add(new Carta_Magica(tipo_carta,nome_carta,desc,img,ctx.pc.get(i).getText()) );
            
        }
            
            if(ctx.PC_FIM().getText().contains("missing")){
                
                mensagem = ("Fim da criação de cartas 'END_CREATE_CARD' não encontrado!");
                SemanticoUtils.adicionarErroSemantico(ctx.pc_fim, mensagem);
            }
            else if(ctx.PC_INICIO().getText().contains("missing")){
                
                mensagem = ("Inicio da criação de cartas 'CREATE_CARD' não encontrado! ");
                SemanticoUtils.adicionarErroSemantico(ctx.pc_inicio, mensagem);
            }
            
            for(int i =0; i<ctx.ATRIBUICAO().size();i++){
                if(ctx.ATRIBUICAO().get(i).getText().contains("missing")){
                    mensagem = ("Erro de atribuição, ':' não encontrado!");
                    SemanticoUtils.adicionarErroSemantico(ctx.atribuicao.get(i), mensagem);
                }
            }
            
            for(int i = 0; i<ctx.FIM_CADEIA().size();i++){
                if(ctx.FIM_CADEIA().get(i).getText().contains("missing")){
                    mensagem = ("Erro de escrita, ';' não encontrado");
                    
                    SemanticoUtils.adicionarErroSemantico(ctx.fim_cadeia.get(i), mensagem);
                }                
            }
             for(int i =0; i<ctx.CARD_MAGIC().size();i++){
                if(ctx.CARD_MAGIC().get(i).getText().contains("missing")){
                    mensagem = ("Erro de declaração, tipo da magia não encontrado!");
                    SemanticoUtils.adicionarErroSemantico(ctx.tipo_cartam.get(i), mensagem);
                }
            }
              for(int i =0; i<ctx.CARD_MONSTER().size();i++){
                if(ctx.CARD_MONSTER().get(i).getText().contains("missing")){
                    mensagem = ("Erro de declaração, tipo de monstro não encontrado!");
                    SemanticoUtils.adicionarErroSemantico(ctx.tipo_carta.get(i), mensagem);
                }
            }
             
            
            if(!ctx.ERRO_CARD().isEmpty()){
                
                mensagem = ("Erro de Declaração!");                    
                SemanticoUtils.adicionarErroSemantico(ctx.erro.get(0), mensagem);
            }
            
           
            
           
            
            
            /*System.out.println(ctx.PC_CARD());
            System.out.println(ctx.pc_card);
            System.out.println(ctx.PC_CARD_MAGIC());
            System.out.println(ctx.pc_cardm);*/
           
        
             
             
            
        
        
        return super.visitCriarCarta(ctx); 
        
        
    }
    
}
