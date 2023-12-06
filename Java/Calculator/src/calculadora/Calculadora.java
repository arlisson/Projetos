package calculadora;

import log.LogManager;

public class Calculadora {
	private static LogManager logger = LogManager.getInstance();

	public double soma(double a, double b) {
		logger.logInfo("Realizada a soma entre " + a + " e " + b);
		return a + b;
	}

	public double diminui(double a, double b) {
		logger.logInfo("Realizada a subtração entre " + a + " e " + b);
		return a - b;
	}

	public double multiplica(double a, double b) {
		logger.logInfo("Realizada a multiplicação entre " + a + " e " + b);
		return a * b;
	}

	public double divide(double a, double b) {
		if (b == 0) {
			logger.logError("Foi feita uma tentativa de divisão por zero");
			throw new RuntimeException("Divisão por zero!");
		}
		logger.logInfo("Realizada a divisão entre " + a + " e " + b);
		return a / b;
	}
}
