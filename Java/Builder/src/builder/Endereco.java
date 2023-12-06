package builder;

public class Endereco {
	private String rua;
	private int numero;
	private String complemento;
	
	protected Endereco() {
		
	}
	public String getRua() {
		return rua;
	}
	public void setRua(String rua) {
		this.rua = rua;
	}
	public int getNumero() {
		return numero;
	}
	public void setNumero(int numero) {
		this.numero = numero;
	}
	public String getComplemento() {
		return complemento;
	}
	public void setComplemento(String complemento) {
		this.complemento = complemento;
	}
	
	@Override
	public String toString() {
		// TODO Auto-generated method stub
		return "Rua: "+getRua()+"\nNumero: "+getNumero()+"\nComplemento: "+getComplemento();
	}
	

}
