package tokens;

import java.io.PrintStream;

public class Alguma
{
	public static void main(String[] args)
	{
		PrintStream p = System.out;
		AlgumaLexico lexico = new AlgumaLexico(args[0]);
		Token t = null;
		
		while((t = lexico.proximoToken()) != null)
		{
			p.print(t);
		}
	}
}