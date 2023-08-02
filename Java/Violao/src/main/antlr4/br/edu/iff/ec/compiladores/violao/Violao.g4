grammar Violao;


PC_INICIO: 'CAMPO-HARMONICO-MAIOR';
//PC_FIM: 'FIM-CAMPO-HARMONICO';
ABRE_CHAVE:'{';
FECHA_CHAVE:'}';
ACORDE: 'ACORDE';
ATRIBUIR: ':';
FIM_CADEIA:';';
FINAL: '.';
PC_ACORDES:'C'|'D'|'E'|'F'|'G'|'A'|'B';

ERRO: (ABRE_CHAVE ESPACO_BRANCO*? ATRIBUIR)|(ESPACO_BRANCO*? ATRIBUIR)|
        (FIM_CADEIA ESPACO_BRANCO*? FIM_CADEIA)|(ABRE_CHAVE ESPACO_BRANCO*? FIM_CADEIA)|
        (ATRIBUIR ESPACO_BRANCO* ATRIBUIR) ;
        



ESPACO_BRANCO: (' '|'\n'|'\t'|'\r') -> skip;

criarCampo:
    pc_inicio += PC_INICIO abre_chave+=ABRE_CHAVE
    ((erro+=ERRO)? acorde+=ACORDE atribuir+=ATRIBUIR pc_acordes+=PC_ACORDES fim_cadeia+=FIM_CADEIA (erro+=ERRO)?)+  
    
    
     
   fecha_chave+=FECHA_CHAVE EOF
;
