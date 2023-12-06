package tokens;

public class AlgumaLexico {
	private LeitorArquivoTexto texto;
	
	public AlgumaLexico(String arquivo)
	{
		this.texto = new LeitorArquivoTexto(arquivo);
	}
	
	public Token proximoToken()
	{
		int caractereLido = -1; // this.texto.lerProximoCaractere();
		/*
		 * if(caractereLido == -1) return null;
		 */
		do
		{
			char c = (char) caractereLido;
			if(c == ' ' || c == '\n')
				continue;
			if(c == ':')
				return new Token(TipoToken.PCDelim,":");
			else if(c == '*')
				return new Token(TipoToken.OpAritiMult, "*");
			else if(c == '+')
				return new Token(TipoToken.OpAritSoma, "+");
			else if(c == '-')
				return new Token(TipoToken.OpAritSub, "-");
			else if(c == '/')
				return new Token(TipoToken.OpAritDiv, "/");
			else if(c == '>')
			{
				caractereLido = (char) texto.lerProximoCaractere();
				
				c = (char) caractereLido;
				
				if(c == '=')
					return new Token(TipoToken.OpRelMaiorIgual, ">=");
				else
					return new Token(TipoToken.OpRelMaior, ">");
			}else if(c == '<')
			{
				caractereLido = (char) texto.lerProximoCaractere();
				
				c = (char) caractereLido;
				
				if(c == '>')
					return new Token(TipoToken.OpRelDif, "<>");
				else if(c == '=')
					return new Token(TipoToken.OpRelMenorIgual, "<=");
				else
					return new Token(TipoToken.OPRelMenor, "<");
			}
			
		}while((caractereLido = texto.lerProximoCaractere()) != -1);
		return null;
	}
	
	private Token operadorRelacional()
	{
		return null;
	}
	
	private Token palavraChave()
	{
		return null;
	}
	
	private Token parenteses()
	{
		return null;
	}
	
	private Token numeros()
	{
		return null;
	}
	
	private Token variavel()
	{
		return null;
	}
}
