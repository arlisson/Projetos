package log;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.Writer;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class LogManager {

	private PrintWriter printwriter;
	private static LogManager logmanager;

	private LogManager() {
		try {
			FileWriter filewriter = new FileWriter("log.txt", true);
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

		return LocalDateTime.now().format(DateTimeFormatter.ofPattern("MM-dd-yyy HH:mm:ss")).toString();
	}

	private String PrepareMessage(String type, String message) {
		return "[" + getDateTime() + "]" + type + ": " + message;
	}

	public void logInfo(String message) {
		printwriter.println(PrepareMessage("INFO", message));
		printwriter.flush();
	}

	public void logWarning(String message) {
		printwriter.println(PrepareMessage("WARNING", message));
		printwriter.flush();
	}

	public void logError(String message) {
		printwriter.println(PrepareMessage("ERROR", message));
		printwriter.flush();
	}

}
