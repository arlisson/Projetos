package Quiz;

import java.util.Scanner;

public class Principal {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner scanner = new Scanner(System.in);
	    
	    // Criação de perguntas
	    Perguntas[] Perguntass = {
	      new Perguntas("Qual é a capital do Brasil?", new String[] {"São Paulo", "Rio de Janeiro", "Brasília"}, "Brasília"),
	      new Perguntas("Quem pintou a Mona Lisa?", new String[] {"Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso"}, "Leonardo da Vinci"),
	      new Perguntas("Quem escreveu o livro 'Dom Quixote'?", new String[] {"Miguel de Cervantes", "Jorge Luis Borges", "Gabriel Garcia Marquez"}, "Miguel de Cervantes")
	    };
	    
	    // Mostra as perguntas e pede as respostas
	    int score = 0;
	    for (Perguntas Perguntas : Perguntass) {
	      System.out.println(Perguntas.getQuestion());
	      String[] options = Perguntas.getOptions();
	      for (int i = 0; i < options.length; i++) {
	        System.out.println((i+1) + ". " + options[i]);
	      }
	      System.out.print("Resposta: ");
	      String answer = scanner.nextLine();
	      
	      if (Perguntas.checkAnswer(answer)) {
	        score++;
	        System.out.println("Correto!");
	      } else {
	        System.out.println("Incorreto!");
	      }
	    }
	    
	    // Mostra a pontuação final
	    System.out.println("Você acertou " + score + " de " + Perguntass.length + " perguntas.");
	  }
}
