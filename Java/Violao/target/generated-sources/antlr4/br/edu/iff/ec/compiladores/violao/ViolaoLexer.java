// Generated from br\edu\iff\ec\compiladores\violao\Violao.g4 by ANTLR 4.13.0
package br.edu.iff.ec.compiladores.violao;
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class ViolaoLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.13.0", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		PC_INICIO=1, ABRE_CHAVE=2, FECHA_CHAVE=3, ACORDE=4, ATRIBUIR=5, FIM_CADEIA=6, 
		FINAL=7, PC_ACORDES=8, ERRO=9, ESPACO_BRANCO=10;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"PC_INICIO", "ABRE_CHAVE", "FECHA_CHAVE", "ACORDE", "ATRIBUIR", "FIM_CADEIA", 
			"FINAL", "PC_ACORDES", "ERRO", "ESPACO_BRANCO"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'CAMPO-HARMONICO-MAIOR'", "'{'", "'}'", "'ACORDE'", "':'", "';'", 
			"'.'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "PC_INICIO", "ABRE_CHAVE", "FECHA_CHAVE", "ACORDE", "ATRIBUIR", 
			"FIM_CADEIA", "FINAL", "PC_ACORDES", "ERRO", "ESPACO_BRANCO"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public ViolaoLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "Violao.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\u0004\u0000\no\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002\u0001"+
		"\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004"+
		"\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007"+
		"\u0007\u0007\u0002\b\u0007\b\u0002\t\u0007\t\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001"+
		"\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001"+
		"\u0003\u0001\u0004\u0001\u0004\u0001\u0005\u0001\u0005\u0001\u0006\u0001"+
		"\u0006\u0001\u0007\u0001\u0007\u0001\b\u0001\b\u0005\bA\b\b\n\b\f\bD\t"+
		"\b\u0001\b\u0001\b\u0001\b\u0005\bI\b\b\n\b\f\bL\t\b\u0001\b\u0001\b\u0001"+
		"\b\u0005\bQ\b\b\n\b\f\bT\t\b\u0001\b\u0001\b\u0001\b\u0001\b\u0005\bZ"+
		"\b\b\n\b\f\b]\t\b\u0001\b\u0001\b\u0001\b\u0001\b\u0005\bc\b\b\n\b\f\b"+
		"f\t\b\u0001\b\u0001\b\u0003\bj\b\b\u0001\t\u0001\t\u0001\t\u0001\t\u0004"+
		"BJR[\u0000\n\u0001\u0001\u0003\u0002\u0005\u0003\u0007\u0004\t\u0005\u000b"+
		"\u0006\r\u0007\u000f\b\u0011\t\u0013\n\u0001\u0000\u0001\u0003\u0000\t"+
		"\n\r\r  w\u0000\u0001\u0001\u0000\u0000\u0000\u0000\u0003\u0001\u0000"+
		"\u0000\u0000\u0000\u0005\u0001\u0000\u0000\u0000\u0000\u0007\u0001\u0000"+
		"\u0000\u0000\u0000\t\u0001\u0000\u0000\u0000\u0000\u000b\u0001\u0000\u0000"+
		"\u0000\u0000\r\u0001\u0000\u0000\u0000\u0000\u000f\u0001\u0000\u0000\u0000"+
		"\u0000\u0011\u0001\u0000\u0000\u0000\u0000\u0013\u0001\u0000\u0000\u0000"+
		"\u0001\u0015\u0001\u0000\u0000\u0000\u0003+\u0001\u0000\u0000\u0000\u0005"+
		"-\u0001\u0000\u0000\u0000\u0007/\u0001\u0000\u0000\u0000\t6\u0001\u0000"+
		"\u0000\u0000\u000b8\u0001\u0000\u0000\u0000\r:\u0001\u0000\u0000\u0000"+
		"\u000f<\u0001\u0000\u0000\u0000\u0011i\u0001\u0000\u0000\u0000\u0013k"+
		"\u0001\u0000\u0000\u0000\u0015\u0016\u0005C\u0000\u0000\u0016\u0017\u0005"+
		"A\u0000\u0000\u0017\u0018\u0005M\u0000\u0000\u0018\u0019\u0005P\u0000"+
		"\u0000\u0019\u001a\u0005O\u0000\u0000\u001a\u001b\u0005-\u0000\u0000\u001b"+
		"\u001c\u0005H\u0000\u0000\u001c\u001d\u0005A\u0000\u0000\u001d\u001e\u0005"+
		"R\u0000\u0000\u001e\u001f\u0005M\u0000\u0000\u001f \u0005O\u0000\u0000"+
		" !\u0005N\u0000\u0000!\"\u0005I\u0000\u0000\"#\u0005C\u0000\u0000#$\u0005"+
		"O\u0000\u0000$%\u0005-\u0000\u0000%&\u0005M\u0000\u0000&\'\u0005A\u0000"+
		"\u0000\'(\u0005I\u0000\u0000()\u0005O\u0000\u0000)*\u0005R\u0000\u0000"+
		"*\u0002\u0001\u0000\u0000\u0000+,\u0005{\u0000\u0000,\u0004\u0001\u0000"+
		"\u0000\u0000-.\u0005}\u0000\u0000.\u0006\u0001\u0000\u0000\u0000/0\u0005"+
		"A\u0000\u000001\u0005C\u0000\u000012\u0005O\u0000\u000023\u0005R\u0000"+
		"\u000034\u0005D\u0000\u000045\u0005E\u0000\u00005\b\u0001\u0000\u0000"+
		"\u000067\u0005:\u0000\u00007\n\u0001\u0000\u0000\u000089\u0005;\u0000"+
		"\u00009\f\u0001\u0000\u0000\u0000:;\u0005.\u0000\u0000;\u000e\u0001\u0000"+
		"\u0000\u0000<=\u0002AG\u0000=\u0010\u0001\u0000\u0000\u0000>B\u0003\u0003"+
		"\u0001\u0000?A\u0003\u0013\t\u0000@?\u0001\u0000\u0000\u0000AD\u0001\u0000"+
		"\u0000\u0000BC\u0001\u0000\u0000\u0000B@\u0001\u0000\u0000\u0000CE\u0001"+
		"\u0000\u0000\u0000DB\u0001\u0000\u0000\u0000EF\u0003\t\u0004\u0000Fj\u0001"+
		"\u0000\u0000\u0000GI\u0003\u0013\t\u0000HG\u0001\u0000\u0000\u0000IL\u0001"+
		"\u0000\u0000\u0000JK\u0001\u0000\u0000\u0000JH\u0001\u0000\u0000\u0000"+
		"KM\u0001\u0000\u0000\u0000LJ\u0001\u0000\u0000\u0000Mj\u0003\t\u0004\u0000"+
		"NR\u0003\u000b\u0005\u0000OQ\u0003\u0013\t\u0000PO\u0001\u0000\u0000\u0000"+
		"QT\u0001\u0000\u0000\u0000RS\u0001\u0000\u0000\u0000RP\u0001\u0000\u0000"+
		"\u0000SU\u0001\u0000\u0000\u0000TR\u0001\u0000\u0000\u0000UV\u0003\u000b"+
		"\u0005\u0000Vj\u0001\u0000\u0000\u0000W[\u0003\u0003\u0001\u0000XZ\u0003"+
		"\u0013\t\u0000YX\u0001\u0000\u0000\u0000Z]\u0001\u0000\u0000\u0000[\\"+
		"\u0001\u0000\u0000\u0000[Y\u0001\u0000\u0000\u0000\\^\u0001\u0000\u0000"+
		"\u0000][\u0001\u0000\u0000\u0000^_\u0003\u000b\u0005\u0000_j\u0001\u0000"+
		"\u0000\u0000`d\u0003\t\u0004\u0000ac\u0003\u0013\t\u0000ba\u0001\u0000"+
		"\u0000\u0000cf\u0001\u0000\u0000\u0000db\u0001\u0000\u0000\u0000de\u0001"+
		"\u0000\u0000\u0000eg\u0001\u0000\u0000\u0000fd\u0001\u0000\u0000\u0000"+
		"gh\u0003\t\u0004\u0000hj\u0001\u0000\u0000\u0000i>\u0001\u0000\u0000\u0000"+
		"iJ\u0001\u0000\u0000\u0000iN\u0001\u0000\u0000\u0000iW\u0001\u0000\u0000"+
		"\u0000i`\u0001\u0000\u0000\u0000j\u0012\u0001\u0000\u0000\u0000kl\u0007"+
		"\u0000\u0000\u0000lm\u0001\u0000\u0000\u0000mn\u0006\t\u0000\u0000n\u0014"+
		"\u0001\u0000\u0000\u0000\u0007\u0000BJR[di\u0001\u0006\u0000\u0000";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}