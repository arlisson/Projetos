package tokens;

public class Token {
	public TipoToken nome;
	public String lexema;
	public Token(TipoToken nome, String lexema)
	{
		this.nome = nome;
		this.lexema = lexema;
	}
	
	@Override
	public String toString()
	{
		return "<"+this.nome+","+this.lexema+">";
	}
}
