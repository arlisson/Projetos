/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package br.edu.iff.ec.compiladores.violao;

/**
 *
 * @author T-GAMER
 */
public class Semantico extends ViolaoBaseVisitor<Void>{

   public TabelaDeSimbolos tabela;

    @Override
    public Void visitCriarCampo(ViolaoParser.CriarCampoContext ctx) {
        
        
        String mensagem;
        
        tabela = new TabelaDeSimbolos();
        
        try{
            if(ctx.pc_inicio.get(0).getText().contains("missing")){
                mensagem = ("Erro de Declaração");                    
                SemanticoUtils.adicionarErroSemantico(ctx.getStart(), mensagem);
                        
            }  
            if(!ctx.erro.isEmpty()){
                mensagem = ("Erro de escrita");                    
                SemanticoUtils.adicionarErroSemantico(ctx.erro.get(0), mensagem);
            }
            
            if(ctx.abre_chave.get(0).getText().contains("missing")){
                mensagem = ("Erro de Declaração");                    
                SemanticoUtils.adicionarErroSemantico(ctx.getStart(), mensagem);
                
            }
                        
           
            for(int i = 0; i<ctx.acorde.size();i++){
                
                if(ctx.pc_acordes.get(i).getText().contains("missing")){
                    mensagem = String.format("Acorde não encontrado!",ctx.pc_acordes.get(i).getText() );
                    SemanticoUtils.adicionarErroSemantico(ctx.pc_acordes.get(i), mensagem);
                }else{
                   if(!tabela.existe(ctx.pc_acordes.get(i).getText())){
                        //se não estiver, será adicionado
                        tabela.adicionar(ctx.pc_acordes.get(i).getText());
                
                    }else{
                        //se estiver cria uma mensagem de erro e adiciona a lista de mensagens de erro
                        mensagem = String.format("O Acorde %s já foi declarado",ctx.pc_acordes.get(i).getText() );
                        SemanticoUtils.adicionarErroSemantico(ctx.pc_acordes.get(i), mensagem);
                    }  
                }
                
            }
            for(int i=0; i<ctx.atribuir.size(); i++){
                if(ctx.atribuir.get(i).getText().contains("missing")){
                    mensagem = String.format("Erro: ':' não encontrado!" );
                    SemanticoUtils.adicionarErroSemantico(ctx.atribuir.get(i), mensagem);
                }
            }
            
            for(int i = 0; i<ctx.fim_cadeia.size();i++){
                if(ctx.fim_cadeia.get(i).getText().contains("missing")){
                    mensagem = String.format("Erro: ';' não encontrado!",ctx.pc_acordes.get(i).getText() );
                    SemanticoUtils.adicionarErroSemantico(ctx.pc_acordes.get(i), mensagem);
                }
            
            }
            
            for(int i =0; i<1;i++){
                ctx.fecha_chave.get(i);                
            }
            
            
           /* 
            System.out.println(ctx.acorde);
            System.out.println(ctx.pc_acordes);
            System.out.println(ctx.atribuir);
            System.out.println(ctx.fim_cadeia);
            System.out.println(ctx.erro);
            System.out.println(ctx.fecha_chave);
            */
           
        }catch(Exception e){
        throw new RuntimeException("Impossível continuar, ocorreu algum erro de escrita!");
    }
        
           
           
        return super.visitCriarCampo(ctx);
    }
   
   
    
}
