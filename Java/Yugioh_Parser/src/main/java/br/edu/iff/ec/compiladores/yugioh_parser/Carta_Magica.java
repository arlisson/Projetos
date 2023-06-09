/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package br.edu.iff.ec.compiladores.yugioh_parser;

/**
 *
 * @author T-GAMER
 */
public class Carta_Magica {
    private String tipo_carta;
    private String nome_carta;   
    private String desc;
    private String img,pc_card,pc_desc,pc_image,pc_name;
    
    public Carta_Magica(String tipo_carta,String nome_carta,String desc, String img,String pc_card,String pc_name,String pc_desc,String pc_image) {
         
       
        this.img=img;
        this.desc=desc;        
        this.nome_carta = nome_carta;        
        this.tipo_carta=tipo_carta;
        this.pc_card=pc_card;
        this.pc_desc = pc_desc;
        this.pc_image = pc_image;
        this.pc_name = pc_name;
        
        
    }
    
     @Override
    public String toString() {
        return "Tipo-Carta: "+this.tipo_carta+", "+this.pc_card+"\n"+
                "Nome:: "+this.nome_carta+", "+this.pc_name+"\n"+                
                "Descrição:: "+this.desc+", "+this.pc_desc+"\n"+
                "Imagem:: "+this.img+", "+this.pc_image+"\n";
    }
}
