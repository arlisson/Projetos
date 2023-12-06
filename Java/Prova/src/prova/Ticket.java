package prova;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Ticket {
	
	private int codigo;
	private LocalDateTime data_i;
	private LocalDateTime data_f;
	private boolean retirado = false;
	
	public Ticket(int codigo, LocalDateTime data_i) {
		
		this.codigo = codigo;
		this.data_i = data_i;
		
	}
	public int getCodigo() {
		return codigo;
	}
	public void setCodigo(int codigo) {
		this.codigo = codigo;
	}
	public String getData_i() {
		return data_i.format(DateTimeFormatter.ofPattern("dd-MM-yyy HH:mm:ss")).toString();
	}
	public void setData_i(LocalDateTime data_i) {
		this.data_i = data_i;
	}
	public String getData_f() {
		return data_f.format(DateTimeFormatter.ofPattern("dd-MM-yyy HH:mm:ss")).toString();
	}
	public void setData_f(LocalDateTime data_f) {
		this.data_f = data_f;
	}
	
	public boolean isRetirado() {
		return retirado;
	}
	public void setRetirado(boolean retirado) {
		this.retirado = retirado;
	}
	@Override
	public String toString() {
		// TODO Auto-generated method stub
		return "\nCódigo do ticket: "+this.codigo+"\nData de entrada: "+this.data_i.format(DateTimeFormatter.ofPattern("dd-MM-yyy HH:mm:ss")).toString()
				+"\nData de Saída: "+this.data_f.format(DateTimeFormatter.ofPattern("dd-MM-yyy HH:mm:ss")).toString();
	}
	
	

}
