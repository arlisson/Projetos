package Quiz;

public class Perguntas {

	
	 private String question;
	  private String[] options;
	  private String answer;
	  
	  public Perguntas(String question, String[] options, String answer) {
	    this.question = question;
	    this.options = options;
	    this.answer = answer;
	  }
	  
	  public String getQuestion() {
	    return question;
	  }
	  
	  public String[] getOptions() {
	    return options;
	  }
	  
	  public boolean checkAnswer(String answer) {
	    return this.answer.equals(answer);
	  }
	
}
