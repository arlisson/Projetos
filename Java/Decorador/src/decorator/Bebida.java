package decorator;

public abstract class Bebida {
	private String desc;

	public String getDescricao() {
		return desc;
	}

	public void setDescricao(String desc) {
		this.desc = desc;
	}
	
	public abstract double valor();
	
	
	
	
	
}
