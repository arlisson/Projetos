/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package br.edu.iff.ec.compiladores.yugioh_parser;

/**
 *
 * @author T-GAMER
 */
public class GeradorYGOHTML extends ParserBaseVisitor<Void>{
    StringBuilder saida;

    public GeradorYGOHTML() {
        saida = new StringBuilder();    
        
        
    }

    @Override
    public Void visitCriarCarta(ParserParser.CriarCartaContext ctx) {
        
        saida.append("<!DOCTYPE html>\n" +
"<html>\n" +
"\n" +
"<head>\n" +
"    <meta charset=\"UTF-8\">\n" +
"    <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n" +
"    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n" +
"    <title>Trading Card Game</title>\n" +
"    <style>\n" +
"        * {\n" +
"            padding: 0;\n" +
"            margin: 0;\n" +
"        }\n" +
"\n" +
"        p {\n" +
"            text-align: justify;\n" +
"        }\n" +
"\n" +
"        .Profile {\n" +
"\n" +
"            padding: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_monster_effect {\n" +
"            background-image: url(\"monster_effect.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: right top;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_monster_normal {\n" +
"            background-image: url(\"fundo_normal.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: right top;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_monster_fusion {\n" +
"            background-image: url(\"fundo_fusao.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: right top;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_monster_sincro {\n" +
"            background-repeat: repeat;\n" +
"            background-position: right top;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_monster_xyz {\n" +
"            background-image: url(\"fundo_xyz.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: right top;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_monster_ritual {\n" +
"            background-image: url(\"fundo_ritual.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: center;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_normal_spell {\n" +
"            background-image: url(\"fundo_spell.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: center;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_spell_continuous {\n" +
"            background-image: url(\"fundo_spell.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: center;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_spell_equip {\n" +
"            background-image: url(\"fundo_spell.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: center;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_spell_field {\n" +
"            background-image: url(\"fundo_spell.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: center;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_spell_quick {\n" +
"            background-image: url(\"fundo_spell.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: center;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_spell_ritual {\n" +
"            background-image: url(\"fundo_spell.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: center;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_normal_trap {\n" +
"            background-image: url(\"fundo_trap.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: center;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_counter_trap {\n" +
"            background-image: url(\"fundo_trap.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: center;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .profile_continuous_trap {\n" +
"            background-image: url(\"fundo_trap.jpg\");\n" +
"            background-repeat: repeat;\n" +
"            background-position: center;\n" +
"            background-attachment: fixed;\n" +
"            width: 280px;\n" +
"            height: auto;\n" +
"            padding: 5px;\n" +
"            overflow: hidden;\n" +
"            border: 5px solid #363636;\n" +
"            border-radius: 5px;\n" +
"        }\n" +
"\n" +
"        .pname {\n" +
"            display: flex;\n" +
"            font-size: 20px;\n" +
"            white-space: nowrap;\n" +
"            font-weight: bold;\n" +
"            text-align: center;\n" +
"            color: #000;\n" +
"            align-items: center;\n" +
"\n" +
"        }\n" +
"\n" +
"        .pname_xyz {\n" +
"            font-weight: bold;\n" +
"            color: #fff;\n" +
"            display: flex;\n" +
"            font-size: 20px;\n" +
"            white-space: nowrap;\n" +
"            text-align: center;\n" +
"            align-items: center;\n" +
"\n" +
"        }\n" +
"\n" +
"        .pname_fusion {\n" +
"            display: flex;\n" +
"            font-size: 20px;\n" +
"            white-space: nowrap;\n" +
"            font-weight: bold;\n" +
"            text-align: center;\n" +
"            color: #000;\n" +
"            align-items: center;\n" +
"        }\n" +
"\n" +
"        .pname_ritual {\n" +
"            display: flex;\n" +
"            font-size: 20px;\n" +
"            white-space: nowrap;\n" +
"            font-weight: bold;\n" +
"            text-align: center;\n" +
"            color: #000;\n" +
"            align-items: center;\n" +
"        }\n" +
"\n" +
"        .profile-name {\n" +
"            background: rgba(255, 255, 255, 0.2);\n" +
"            padding: 3px;\n" +
"            border-radius: 0px;\n" +
"            /*box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.6), -2px -2px 5px rgba(255, 255, 255, 0.8);*/\n" +
"            margin: 6px 3px 5px 3px;\n" +
"            border-top: outset rgba(255, 255, 255, 0.6);\n" +
"            border-bottom: outset rgba(0, 0, 0, 0.6);\n" +
"            border-left: outset rgba(255, 255, 255, 0.6);\n" +
"            border-right: outset rgba(0, 0, 0, 0.6);\n" +
"        }\n" +
"\n" +
"        .profile_name {\n" +
"            text-transform: uppercase;\n" +
"            overflow: hidden;\n" +
"\n" +
"        }\n" +
"\n" +
"        .profile_left {\n" +
"            width: 80%;\n" +
"            float: left;\n" +
"        }\n" +
"\n" +
"        .profile_right {\n" +
"            width: 20%;\n" +
"            float: right;\n" +
"        }\n" +
"\n" +
"        .profile_right img {\n" +
"\n" +
"            float: right;\n" +
"        }\n" +
"\n" +
"        .profile-level {\n" +
"            padding: 0px;\n" +
"        }\n" +
"\n" +
"        .profile_level {\n" +
"            padding-right: 5px;\n" +
"            overflow: hidden;\n" +
"            width: 100%;\n" +
"        }\n" +
"\n" +
"        .profile_level img {\n" +
"            float: right;\n" +
"            padding: 0px;\n" +
"        }\n" +
"\n" +
"        .profile_level_xyz {\n" +
"            padding-right: 5px;\n" +
"            overflow: hidden;\n" +
"            width: 100%;\n" +
"        }\n" +
"\n" +
"        .profile_level_xyz img {\n" +
"            float: left;\n" +
"            padding: 0px;\n" +
"        }\n" +
"\n" +
"        .profile_spell {\n" +
"            float: right;\n" +
"        }\n" +
"\n" +
"        .profile-img {\n" +
"            border-radius: 0px;\n" +
"            overflow: hidden;\n" +
"            padding: 2px;\n" +
"            background: rgba(0, 0, 0, 0.6);\n" +
"            margin: 2px 2px;\n" +
"        }\n" +
"\n" +
"        .profile_img {\n" +
"            border-radius: 1px;\n" +
"            margin: 2px 2px 2px 2px;\n" +
"        }\n" +
"\n" +
"        .profile_desc {\n" +
"            background: rgba(255, 255, 255, 0.7);\n" +
"            overflow: auto;\n" +
"            margin-top: 5px;\n" +
"            border-radius: 0px;\n" +
"            border: solid 3px rgb(219, 58, 58, 0.8);\n" +
"            width: 50px 50px;\n" +
"\n" +
"\n" +
"        }\n" +
"\n" +
"        .profile_desc h4 {\n" +
"            font-size: 13px;\n" +
"            font-weight: bold;\n" +
"        }\n" +
"\n" +
"        .profile_desc p {\n" +
"            font-size: 10px;\n" +
"            padding: 2px;\n" +
"\n" +
"        }\n" +
"\n" +
"        .profile_attack {\n" +
"            margin: 3px;\n" +
"            font-weight: bold;\n" +
"            border-top: solid #000;\n" +
"\n" +
"        }\n" +
"    </style>\n" +
"</head>\n"+
                "<body>");
       
        for(int i=0;i<ctx.tipo_carta.size();i++){
            switch(ctx.tipo_carta.get(i).getText()){
                
                case "NORMAL-MONSTER":
                    saida.append("<br>\n" +
"\n" +
"    <div class=\"Profile\">\n" +
"        <div class=\"profile_monster_normal\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.monstro_nome.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n"+
        "<div class=\"profile_right\">\n");
                    break;
                    
                case "EFFECT-MONSTER":
                    saida.append("<br>\n" +
     "<div class=\"Profile\">\n" +
"        <div class=\"profile_monster_effect\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.monstro_nome.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">");
                    break;
                 
                case "XYZ-MONSTER":
                    saida.append("<br>\n" +
"\n" +
"    <div class=\"Profile\">\n" +
"        <div class=\"profile_monster_xyz\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname_xyz\">"+ctx.monstro_nome.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">");
                    
                    break;
                    
                    case "XYZ-EFFECT-MONSTER":
                    saida.append("<br>\n" +
"\n" +
"    <div class=\"Profile\">\n" +
"        <div class=\"profile_monster_xyz\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname_xyz\">"+ctx.monstro_nome.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">");
                    
                    break;
                    
                     case "RITUAL-MONSTER":
                    saida.append("<div class=\"Profile\">\n" +
"        <div class=\"profile_monster_ritual\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname_ritual\">"+ctx.monstro_nome.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">");
                    
                    break;
                    
                case "RITUAL-EFFECT-MONSTER":
                    saida.append("<div class=\"Profile\">\n" +
"        <div class=\"profile_monster_ritual\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname_ritual\">"+ctx.monstro_nome.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">");
                    
                    break;
                
                case "FUSION-MONSTER":
                    saida.append(" <br>\n" +
"\n" +
"    <div class=\"Profile\">\n" +
"        <div class=\"profile_monster_fusion\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname_fusion\">"+ctx.monstro_nome.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">");
                      break;
                
                      case "FUSION-EFFECT-MONSTER":
                    saida.append(" <br>\n" +
"\n" +
"    <div class=\"Profile\">\n" +
"        <div class=\"profile_monster_fusion\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname_fusion\">"+ctx.monstro_nome.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">");
                      break;
                      
                case "SYNCRO-MONSTER":
                    saida.append("<br>\n" +
"\n" +
"    <div class=\"Profile\">\n" +
"        <div class=\"profile_monster_sincro\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.monstro_nome.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">");
                    break;
                 case "SYNCRO-EFFECT-MONSTER":
                    saida.append("<br>\n" +
"\n" +
"    <div class=\"Profile\">\n" +
"        <div class=\"profile_monster_sincro\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.monstro_nome.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">");
                    break;
               
            }
            
            switch(ctx.atributo.get(i).getText()){
                case "DARK":
                    saida.append("<img src=\"trevas.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>");
                    break;
                    
                case "FIRE":
                    saida.append("<img src=\"fogo.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>");
                    break;
                case "EARTH":
                    saida.append("<img src=\"terra.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>");
                    break;
                    
                case "LIGHT":
                    saida.append("<img src=\"luz.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>");
                    break;
                    
                case "WIND":
                    saida.append("<img src=\"vento.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>");
                    break;  
                    
                case "WATER":
                    saida.append("<img src=\"agua.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>");
                    break;
                 
                case "DIVINE":
                    saida.append("<img src=\"divino.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>");
                    break;
            }
            
            if(ctx.tipo_carta.get(i).getText().equals("XYZ-MONSTER")){
                saida.append(" <div class=\"profile_level_xyz\">\n" +
"                <div class=\"profile-level\" id=\"image-container-xyz\">");
            }else{
                saida.append("<div class=\"profile_level\">\n" +
"                <div class=\"profile-level\" id=\"image-container\">");
            }
            
            for(int j =0;j<Integer.parseInt(ctx.level.get(i).getText());j++){
                saida.append(" <img src=\"Level.jpg\" style=\"width: 20px;\">");
            }
            
           
            switch (ctx.tipo_carta.get(i).getText()){
                case "NORMAL-MONSTER":
                    saida.append(" </div>\n" +
"            </div>\n" +
"\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <h4>["+ctx.tipo.get(i).getText()+"]</h4>\n" +
"                    <p>"+ctx.desc.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"                <div class=\"profile_attack\"></div>\n" +
"                <p style=\"float:right;padding:3px\">ATK"+ctx.atk.get(i).getText()+" / DEF "+ctx.def.get(i).getText()+"</p>\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                    break;
                    
                case "EFFECT-MONSTER":
                   saida.append(" </div>\n" +
"            </div>\n" +
"\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <h4>["+ctx.tipo.get(i).getText()+"/EFFECT]</h4>\n" +
"                    <p>"+ctx.desc.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"                <div class=\"profile_attack\"></div>\n" +
"                <p style=\"float:right;padding:3px\">ATK"+ctx.atk.get(i).getText()+" / DEF "+ctx.def.get(i).getText()+"</p>\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                    break;
                 
                case "XYZ-MONSTER":
                    saida.append(" </div>\n" +
"            </div>\n" +
"\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <h4>["+ctx.tipo.get(i).getText()+"/XYZ]</h4>\n" +
"                    <p>"+ctx.desc.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"                <div class=\"profile_attack\"></div>\n" +
"                <p style=\"float:right;padding:3px\">ATK"+ctx.atk.get(i).getText()+" / DEF "+ctx.def.get(i).getText()+"</p>\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                    
                    break;
                     case "XYZ-EFFECT-MONSTER":
                    saida.append(" </div>\n" +
"            </div>\n" +
"\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <h4>["+ctx.tipo.get(i).getText()+"/XYZ/EFFECT]</h4>\n" +
"                    <p>"+ctx.desc.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"                <div class=\"profile_attack\"></div>\n" +
"                <p style=\"float:right;padding:3px\">ATK"+ctx.atk.get(i).getText()+" / DEF "+ctx.def.get(i).getText()+"</p>\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                    
                    break;
                    
                case "RITUAL-MONSTER":
                   saida.append(" </div>\n" +
"            </div>\n" +
"\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <h4>["+ctx.tipo.get(i).getText()+"/RITUAL]</h4>\n" +
"                    <p>"+ctx.desc.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"                <div class=\"profile_attack\"></div>\n" +
"                <p style=\"float:right;padding:3px\">ATK"+ctx.atk.get(i).getText()+" / DEF "+ctx.def.get(i).getText()+"</p>\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                    
                    break;
                
                    case "RITUAL-EFFECT-MONSTER":
                   saida.append(" </div>\n" +
"            </div>\n" +
"\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <h4>["+ctx.tipo.get(i).getText()+"/RITUAL/EFFECT]</h4>\n" +
"                    <p>"+ctx.desc.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"                <div class=\"profile_attack\"></div>\n" +
"                <p style=\"float:right;padding:3px\">ATK"+ctx.atk.get(i).getText()+" / DEF "+ctx.def.get(i).getText()+"</p>\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                    
                    break;
                case "FUSION-MONSTER":
                    saida.append(" </div>\n" +
"            </div>\n" +
"\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <h4>["+ctx.tipo.get(i).getText()+"/FUSION]</h4>\n" +
"                    <p>"+ctx.desc.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"                <div class=\"profile_attack\"></div>\n" +
"                <p style=\"float:right;padding:3px\">ATK"+ctx.atk.get(i).getText()+" / DEF "+ctx.def.get(i).getText()+"</p>\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                      break;
                
                case "FUSION-EFFECT-MONSTER":
                    saida.append(" </div>\n" +
"            </div>\n" +
"\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <h4>["+ctx.tipo.get(i).getText()+"/FUSION/EFFECT]</h4>\n" +
"                    <p>"+ctx.desc.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"                <div class=\"profile_attack\"></div>\n" +
"                <p style=\"float:right;padding:3px\">ATK"+ctx.atk.get(i).getText()+" / DEF "+ctx.def.get(i).getText()+"</p>\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                      break;
                      
                case "SYNCRO-MONSTER":
                    saida.append(" </div>\n" +
"            </div>\n" +
"\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <h4>["+ctx.tipo.get(i).getText()+"/SYNCRO]</h4>\n" +
"                    <p>"+ctx.desc.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"                <div class=\"profile_attack\"></div>\n" +
"                <p style=\"float:right;padding:3px\">ATK"+ctx.atk.get(i).getText()+" / DEF "+ctx.def.get(i).getText()+"</p>\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                    break;
                    
                     case "SYNCRO-EFFECT-MONSTER":
                    saida.append(" </div>\n" +
"            </div>\n" +
"\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <h4>["+ctx.tipo.get(i).getText()+"/SYNCRO/EFFECT]</h4>\n" +
"                    <p>"+ctx.desc.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"                <div class=\"profile_attack\"></div>\n" +
"                <p style=\"float:right;padding:3px\">ATK"+ctx.atk.get(i).getText()+" / DEF "+ctx.def.get(i).getText()+"</p>\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                    break;
            }
       
        
        }
        
        for(int i =0;i<ctx.tipo_cartam.size();i++){
            switch(ctx.tipo_cartam.get(i).getText()){
                case "NORMAL-SPELL":
                   saida.append("<br>\n" +
"\n" +
"    <div class=\"Profile\">\n" +
"        <div class=\"profile_normal_spell\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.magic_mone.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">\n" +
"                        <img src=\"SPELL.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_level\">\n" +
"                <h4 class=\"profile_spell\">[SPELL CARD]</h4>\n" +
"            </div>\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.magic_png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <p>"+ctx.desc_m.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                    break;
                    
                case "CONTINUOUS-SPELL" :
                    
                    saida.append("<div class=\"Profile\">\n" +
"        <div class=\"profile_spell_continuous\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.magic_mone.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">\n" +
"                        <img src=\"SPELL.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_level\">\n" +
"                <h4 class=\"profile_spell\">]</h4>\n" +
"                <img src=\"Continuous.jpg\" width=\" 20px\">\n" +
"                <h4 class=\"profile_spell\">[SPELL CARD</h4>\n" +
"\n" +
"            </div>\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.magic_png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <p>"+ctx.desc_m.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                    
                    break;
                    
                case "EQUIP-SPELL":
                    saida.append("<div class=\"Profile\">\n" +
"        <div class=\"profile_spell_equip\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.magic_mone.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">\n" +
"                        <img src=\"SPELL.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_level\">\n" +
"                <h4 class=\"profile_spell\">]</h4>\n" +
"                <img src=\"Equip.jpg\" width=\" 20px\">\n" +
"                <h4 class=\"profile_spell\">[SPELL CARD</h4>\n" +
"\n" +
"            </div>\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.magic_png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <p>"+ctx.desc_m.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"\n" +
"            </div>\n" +
"        </div>\n" +
"    </div> \n"+"<br>");
                    break;
                 
                case "FIELD-SPELL":
                    saida.append("<div class=\"Profile\">\n" +
"        <div class=\"profile_spell_field\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.magic_mone.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">\n" +
"                        <img src=\"SPELL.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_level\">\n" +
"                <h4 class=\"profile_spell\">]</h4>\n" +
"                <img src=\"Field.jpg\" width=\" 20px\">\n" +
"                <h4 class=\"profile_spell\">[SPELL CARD</h4>\n" +
"\n" +
"            </div>\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.magic_png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <p>"+ctx.desc_m.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"\n" +
"    <br>");
                    
                    break;
                    
                case "RITUAL-SPELL":
                    saida.append("<div class=\"Profile\">\n" +
"        <div class=\"profile_spell_ritual\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.magic_mone.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">\n" +
"                        <img src=\"SPELL.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_level\">\n" +
"                <h4 class=\"profile_spell\">]</h4>\n" +
"                <img src=\"Ritual.jpg\" width=\" 20px\">\n" +
"                <h4 class=\"profile_spell\">[SPELL CARD</h4>\n" +
"\n" +
"            </div>\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.magic_png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <p>"+ctx.desc_m.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");
                    
                    break;
                    
                case "QUICK-SPELL":
                    saida.append("<div class=\"Profile\">\n" +
"        <div class=\"profile_spell_quick\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.magic_mone.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">\n" +
"                        <img src=\"SPELL.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_level\">\n" +
"                <h4 class=\"profile_spell\">]</h4>\n" +
"                <img src=\"Quick.jpg\" width=\" 20px\">\n" +
"                <h4 class=\"profile_spell\">[SPELL CARD</h4>\n" +
"\n" +
"            </div>\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.magic_png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <p>"+ctx.desc_m.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"    <br>");                   
                    
                    break;
                       
                case "TRAP-CARD":
                    saida.append("<br>\n" +
"\n" +
"    <div class=\"Profile\">\n" +
"        <div class=\"profile_counter_trap\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.magic_mone.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">\n" +
"                        <img src=\"Trap.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_level\">\n" +
"                <h4 class=\"profile_spell\">[TRAP CARD]</h4>\n" +
"\n" +
"            </div>\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.magic_png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <p>"+ctx.desc_m.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>");
                    break;
                    
                case "CONTINUOUS-TRAP":
                    
                    saida.append(" <div class=\"Profile\">\n" +
"        <div class=\"profile_continuous_trap\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.magic_mone.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">\n" +
"                        <img src=\"Trap.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_level\">\n" +
"                <h4 class=\"profile_spell\">]</h4>\n" +
"                <img src=\"Continuous.jpg\" width=\" 20px\">\n" +
"                <h4 class=\"profile_spell\">[TRAP CARD</h4>\n" +
"\n" +
"            </div>\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.magic_png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <p>"+ctx.desc_m.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>\n" +
"\n" +
"    <br>");
                    
                    break;
                case "COUNTER-TRAP":
                    saida.append("<div class=\"Profile\">\n" +
"        <div class=\"profile_counter_trap\">\n" +
"            <div class=\"profile-name\">\n" +
"                <div class=\"profile_name\">\n" +
"                    <div class=\"profile_left\">\n" +
"                        <p class=\"pname\">"+ctx.magic_mone.get(i).getText().replace("\"","")+"</p>\n" +
"                    </div>\n" +
"                    <div class=\"profile_right\">\n" +
"                        <img src=\"Trap.jpg\" width=\" 25px\">\n" +
"                    </div>\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_level\">\n" +
"                <h4 class=\"profile_spell\">]</h4>\n" +
"                <img src=\"Counter.jpg\" width=\" 20px\">\n" +
"                <h4 class=\"profile_spell\">[TRAP CARD</h4>\n" +
"\n" +
"            </div>\n" +
"\n" +
"            <div class=\"profile_img\">\n" +
"                <div class=\"profile-img\">\n" +
"                    <img src=\""+ctx.magic_png.get(i).getText().replace("\"","")+"\" width=\"100%\">\n" +
"                </div>\n" +
"            </div>\n" +
"            <div class=\"profile_desc\">\n" +
"                <div class=\"profile-desc\">\n" +
"                    <p>"+ctx.desc_m.get(i).getText().replace("\"","")+"</p>\n" +
"                </div>\n" +
"\n" +
"            </div>\n" +
"        </div>\n" +
"    </div>");
                    break;
            }
            
        }
        
         saida.append("<script>\n" +
"        const containers = document.querySelectorAll('.profile_name');\n" +
"        const texts = document.querySelectorAll('.pname');\n" +
"\n" +
"        texts.forEach((text, index) => {\n" +
"            const container = containers[index];\n" +
"\n" +
"            while (text.scrollHeight > container.offsetHeight || text.scrollWidth > container.offsetWidth) {\n" +
"                let fontSize = parseInt(window.getComputedStyle(text).fontSize);\n" +
"                fontSize -= 3.0001;\n" +
"                text.style.fontSize = `${fontSize}px`;\n" +
"            }\n" +
"        });\n" +
"\n" +
"        const xyz = document.querySelectorAll('.profile_name');\n" +
"        const xyztext = document.querySelectorAll('.pname_xyz');\n" +
"\n" +
"        xyztext.forEach((text, index) => {\n" +
"            const container = xyz[index];\n" +
"\n" +
"            while (text.scrollHeight > container.offsetHeight || text.scrollWidth > container.offsetWidth) {\n" +
"                let fontSize = parseInt(window.getComputedStyle(text).fontSize);\n" +
"                fontSize -= 3.0001;\n" +
"                text.style.fontSize = `${fontSize}px`;\n" +
"            }\n" +
"        });\n" +
"\n" +
"\n" +
"        const fusion = document.querySelectorAll('.profile_name');\n" +
"        const fusiontext = document.querySelectorAll('.pname_fusion');\n" +
"\n" +
"        fusiontext.forEach((text, index) => {\n" +
"            const container = fusion[index];\n" +
"\n" +
"            while (text.scrollHeight > container.offsetHeight || text.scrollWidth > container.offsetWidth) {\n" +
"                let fontSize = parseInt(window.getComputedStyle(text).fontSize);\n" +
"                fontSize -= 3.0001;\n" +
"                text.style.fontSize = `${fontSize}px`;\n" +
"            }\n" +
"        });\n" +
"\n" +
"        const ritual = document.querySelectorAll('.profile_name');\n" +
"        const ritualtext = document.querySelectorAll('.pname_ritual');\n" +
"\n" +
"        ritualtext.forEach((text, index) => {\n" +
"            const container = ritual[index];\n" +
"\n" +
"            while (text.scrollHeight > container.offsetHeight || text.scrollWidth > container.offsetWidth) {\n" +
"                let fontSize = parseInt(window.getComputedStyle(text).fontSize);\n" +
"                fontSize -= 3.0001;\n" +
"                text.style.fontSize = `${fontSize}px`;\n" +
"            }\n" +
"        });\n" +
"\n" +
"\n" +
"\n" +
"\n" +
"    </script>\n" +
"\n" +
"</body>\n" +
"\n" +
"</html>");
        return null;
        
        
        
        
        
        
        }  
    }
       
    
    
    
    

