grammar Parser;

PC_INICIO: 'CREATE_CARD';
PC_CARD: 'CARD-MONSTER' ;
PC_CARD_MAGIC: 'CARD-MAGIC';
PC_NAME:'NAME';
PC_LEVEL:'LEVEL';
PC_ATTRIBUTE: 'ATTRIBUTE';
PC_TYPE: 'TYPE';
PC_ATTACK: 'ATTACK';
PC_DEFFENSE:'DEFFENSE';
PC_DESCRIPTION:'DESCRIPTION';
PC_IMAGE:'IMAGE';
PC_FIM: 'END_CREATE_CARD';

ERRO_CARD: ((FIM_CADEIA|ATRIBUICAO)(ESPACO_BRANCO)*)ATRIBUICAO;


CARD_MONSTER:'NORMAL-MONSTER'| 'EFFECT-MONSTER'| 'XYZ-MONSTER'|'XYZ-EFFECT-MONSTER'| 'RITUAL-MONSTER'|'RITUAL-EFFECT-MONSTER'
            | 'FUSION-MONSTER'|'FUSION-EFFECT-MONSTER'| 'SYNCRO-MONSTER'|'SYNCRO-EFFECT-MONSTER';
            
CARD_MAGIC: 'NORMAL-SPELL'| 'CONTINUOUS-SPELL'| 'EQUIP-SPELL'| 'FIELD-SPELL'| 'RITUAL-SPELL'|
             'TRAP-CARD'|'CONTINUOUS-TRAP'| 'COUNTER-TRAP'|'QUICK-SPELL';
ATTRIBUTE: 'DARK'|'FIRE'|'LIGHT'|'WIND'|'WATER'|'EARTH'|'DIVINE';           
TYPE: 'AQUA'| 'SPELLCASTER'| 'FIEND'| 'DINOSSAUR'|'NORMAL'|'EFFECT'|'DRAGON'|
      'FAIRY'|'BEAST'|'WARRIOR-BEAST'|'WINGED-BEAST'|'DIVINE-BEAST'|'WARRIOR'|
      'INSECT'|'MACHINE'|'FISH'|'PLANT'|'PSYCHIC'|'PYRO'|'REPTILE'|'ROCK'|'SEA-SERPENT'|
      'THUNDER'|'WYRM'|'ZOMBIE'|'CREATOR-GOD'|'CIBERSE'|'FUSION'|'XYZ'|'SYNCRO'|'REGULATOR';


PNG: '"'(PALAVRA|DIGITO)('_')*(PALAVRA|DIGITO)*('.png'|'.jpg')'"';

DIGITO: ('+'|'-')?'0'..'9'('0'..'9')*;
CADEIA: '"'.*?'"';
FIM_CADEIA:';';
ATRIBUICAO: ':';

fragment
PALAVRA: 'a'..'z'|'A'..'Z';
VIRG: ',';
ESPACO_BRANCO: (' '|'\n'|'\t'|'\r') -> skip;
COMENTARIO: ('/*'.*?'*/')->skip;


criarCarta:
    pc_inicio=PC_INICIO ATRIBUICAO
    
   (((erro+=ERRO_CARD)?pc_card+=PC_CARD atribuicao+=ATRIBUICAO tipo_carta+=CARD_MONSTER fim_cadeia+=FIM_CADEIA
    (erro+=ERRO_CARD)?pc_name+=PC_NAME atribuicao+=ATRIBUICAO  monstro_nome+=CADEIA fim_cadeia+=FIM_CADEIA
    (erro+=ERRO_CARD)?pc_level+=PC_LEVEL atribuicao+=ATRIBUICAO level += DIGITO fim_cadeia+=FIM_CADEIA 
    (erro+=ERRO_CARD)?pc_atributo+=PC_ATTRIBUTE atribuicao+=ATRIBUICAO atributo+=ATTRIBUTE fim_cadeia+=FIM_CADEIA 
    (erro+=ERRO_CARD)?pc_tipo+=PC_TYPE atribuicao+=ATRIBUICAO tipo+=TYPE fim_cadeia+=FIM_CADEIA 
    (erro+=ERRO_CARD)?pc_atk+=PC_ATTACK atribuicao+=ATRIBUICAO atk+=DIGITO fim_cadeia+=FIM_CADEIA 
    (erro+=ERRO_CARD)?pc_def+=PC_DEFFENSE atribuicao+=ATRIBUICAO def+=DIGITO fim_cadeia+=FIM_CADEIA 
    (erro+=ERRO_CARD)?pc_desc+=PC_DESCRIPTION atribuicao+=ATRIBUICAO  desc+=CADEIA fim_cadeia+=FIM_CADEIA 
    (erro+=ERRO_CARD)?pc_image+=PC_IMAGE atribuicao+=ATRIBUICAO png+=PNG fim_cadeia+=FIM_CADEIA )
    |    
    ((erro+=ERRO_CARD)?pc_cardm+=PC_CARD_MAGIC atribuicao+=ATRIBUICAO tipo_cartam+=CARD_MAGIC FIM_CADEIA
    (erro+=ERRO_CARD)?pc_namem+=PC_NAME atribuicao+=ATRIBUICAO  magic_mone+=CADEIA FIM_CADEIA    
    (erro+=ERRO_CARD)?pc_descm+=PC_DESCRIPTION atribuicao+=ATRIBUICAO desc_m+=CADEIA FIM_CADEIA 
    (erro+=ERRO_CARD)?pc_imagem+=PC_IMAGE atribuicao+=ATRIBUICAO magic_png+=PNG FIM_CADEIA ))+
    
    pc_fim=PC_FIM FIM_CADEIA EOF

;



 



    

