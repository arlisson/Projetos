package prova;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.Writer;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class LogManager {

	private PrintWriter printwriter;
	private static LogManager logmanager;
	private String cpf = "Não informado";
	private Ticket ticket;
	private Pagamento pagamento;

	private LogManager() {
		try {
			FileWriter filewriter = new FileWriter("Registo_Estacionamento.txt", true);
			this.printwriter = new PrintWriter(filewriter);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public static LogManager getInstance() {
		if (logmanager == null) {
			logmanager = new LogManager();
		}
		return logmanager;
	}

	private String getDateTime() {

		return LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd-MM-yyy HH:mm:ss")).toString();
	}

	public String getCpf() {
		return cpf;
	}

	public void setCpf(String cpf) {
		this.cpf = cpf;
	}

	public Ticket getTicket() {
		return ticket;
	}

	public void setTicket(Ticket ticket) {
		this.ticket = ticket;
	}

	public Pagamento getPagamento() {
		return pagamento;
	}

	public void setPagamento(Pagamento pagamento) {
		this.pagamento = pagamento;
	}

	@Override
	public String toString() {
		return "\n----------Nota Fiscal----------\nCpf: " + cpf+ ticket + pagamento;
	}
	
	public void NotaFiscal() {
		printwriter.println("\n----------Nota Fiscal----------\nCpf: " + cpf + ticket +pagamento);
		printwriter.flush();
	}
	

}
