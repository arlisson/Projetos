package tokens;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintStream;

public class LeitorArquivoTexto {
	PrintStream p = System.out;
	
	private final static int TAMANHO_BUFFER = 20;
	private int[] bufferLeitura;
	private int ponteiro;
	private int bufferAtual;
	private int inicioLexema;
	private String lexema;
	
	
	private InputStream stream;
	public LeitorArquivoTexto(String arquivo)
	{
		try {
			this.stream = new FileInputStream(new File(arquivo));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	private void inicializarBuffer()
	{
		this.bufferAtual = 2;
		this.inicioLexema = 0;
		this.bufferLeitura = new int[TAMANHO_BUFFER * 2];
		this.ponteiro = 0;
		this.recarregarBuffer1();
	}
	
	private void recarregarBuffer1()
	{
		if(this.bufferAtual == 2)
		{
			this.bufferAtual = 1;
			
			for(int i = 0; i < TAMANHO_BUFFER; i++)
			{
				try {
					this.bufferLeitura[i] = stream.read();
					if(this.bufferLeitura[i] == -1)
						break;
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
	}
	
	private void recarregarBuffer2()
	{
		if(this.bufferAtual == 1)
		{
			this.bufferAtual = 2;
			
			for(int i = TAMANHO_BUFFER; i < TAMANHO_BUFFER * 2; i++)
			{
				try {
					this.bufferLeitura[i] = stream.read();
					if(this.bufferLeitura[i] == -1)
						break;
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
	}
	
	private void incrementarPonteiro()
	{
		this.ponteiro++;
		
		if(this.ponteiro == TAMANHO_BUFFER)
		{
			this.recarregarBuffer2();
		}else if(this.ponteiro == TAMANHO_BUFFER * 2)
		{
			this.recarregarBuffer1();
			this.ponteiro = 0;
		}
	}
	
	private int lerCaractereDoBuffer()
	{
		int ret = this.bufferLeitura[this.ponteiro];
		this.incrementarPonteiro();
		return ret;
	}
	
	public int lerProximoCaractere()
	{
		int caractere = this.lerCaractereDoBuffer();
		this.lexema += (char)caractere;
		return caractere;
	}
	
	public void limpar()
	{
		this.ponteiro = this.inicioLexema;
		this.lexema = "";
	}
	public void confirmar()
	{
		this.inicioLexema = this.ponteiro;
		this.lexema = "";
	}
	
	public String getLexema()
	{
		return this.lexema;
	}
}
