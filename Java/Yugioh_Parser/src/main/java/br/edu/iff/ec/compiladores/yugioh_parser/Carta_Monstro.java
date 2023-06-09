/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package br.edu.iff.ec.compiladores.yugioh_parser;

/**
 *
 * @author T-GAMER
 */
public class Carta_Monstro {
    private String tipo_carta;
    private String nome_carta;
    private int level;
    private String atributo;
    private String tipo;
    private int atk, def;
    private String desc;
    private String img, pc_card, pc_name,pc_level, pc_atributo,pc_atk,pc_def,pc_des,pc_img,pc_tipo;

    
    
    public Carta_Monstro(String tipo_carta,String nome_carta, int level, String atributo, String tipo, int atk, int def, String desc, String img,
    String pc_card, String pc_name,String pc_level,String pc_atributo,String pc_atk,String pc_def,String pc_des,String pc_img,String pc_tipo) {
        
        this.atk=atk;
        this.atributo = atributo;
        this.def=def;
        this.img=img;
        this.desc=desc;
        this.level=level;
        this.nome_carta = nome_carta;
        this.tipo=tipo;
        this.tipo_carta=tipo_carta;
        this.pc_atk=pc_atk;
        this.pc_atributo = pc_atributo;
        this.pc_card = pc_card;
        this.pc_def=pc_def;
        this.pc_des = pc_des;
        this.pc_img =pc_img;
        this.pc_level=pc_level;
        this.pc_name = pc_name;
        this.pc_tipo=pc_tipo;
        
    }

    @Override
    public String toString() {
        return "Tipo-Carta: "+this.tipo_carta+", "+this.pc_card+"\n"+
                "Nome:: "+this.nome_carta+", "+this.pc_name+"\n"+
                "Level:: "+this.level+", "+this.pc_level+"\n"+
                "Atributo:: "+this.atributo+", "+this.pc_atributo+"\n"+
                "Tipo:: "+this.tipo+", "+this.pc_tipo+"\n"+
                "ATK:: "+this.atk+", "+this.pc_atk+"\n"+
                "DEF:: "+this.def+", "+this.pc_def+"\n"+
                "Descrição:: "+this.desc+", "+this.pc_des+"\n"+
                "Imagem:: "+this.img+", "+this.pc_img+"\n";
    }
    public String getTipo_carta() {
        return this.tipo_carta;
    }

    public String getNome_carta() {
        return this.nome_carta;
    }

    public int getLevel() {
        return this.level;
    }

    public String getAtributo() {
        return this.atributo;
    }

    public String getTipo() {
        return this.tipo;
    }

    public int getAtk() {
        return this.atk;
    }

    public int getDef() {
        return this.def;
    }

    public String getDesc() {
        return this.desc;
    }

    public String getImg() {
        return this.img;
    }

    public String getPc_card() {
        return this.pc_card;
    }

    public String getPc_name() {
        return this.pc_name;
    }

    public String getPc_level() {
        return this.pc_level;
    }

    public String getPc_atributo() {
        return this.pc_atributo;
    }

    public String getPc_atk() {
        return this.pc_atk;
    }

    public String getPc_def() {
        return this.pc_def;
    }

    public String getPc_des() {
        return this.pc_des;
    }

    public String getPc_img() {
        return this.pc_img;
    }
}
