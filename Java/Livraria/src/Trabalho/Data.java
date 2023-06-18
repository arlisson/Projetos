package Trabalho;

public class Data {
	private int dia;
	private int mes;
	private int ano;
	
	
	public Data(int dia, int mes, int ano) {	
		this.mes = mes;
		this.ano = ano;
		this.dia = dia;
			
		
		
	}

	
public int getDia() {
		return dia;
	}


	public int getMes() {
		return mes;
	}


	public int getAno() {
		return ano;
	}

static boolean verifica_ano(int ano) {
	
	if(ano>0) {
		return true;
	}	
	return false;
}
static boolean verifica_mes(int mes) {
	if(mes<13 && mes>0) {
		return true;
		
	}
	return false;
}

static boolean verifica_dia(int dia, int mes, int ano) {	
	
	int[] dias = {31,28,31,30,31,30,31,31,30,31,30,31};		
	
	if(dia <= dias[mes-1] && dia>0 && mes!=2) {
		return true;
	}
	
	if(mes == 2) {
		boolean bissexto = (ano % 4 == 0 && ano % 100 != 0) || (ano % 400 == 0);
		if(bissexto && dia <30 && dia >0) {
			return true;
		}else if(bissexto == false && dia <29 && dia >0) {
			return true;
		}
	}
	
	return false;
}


	
}
