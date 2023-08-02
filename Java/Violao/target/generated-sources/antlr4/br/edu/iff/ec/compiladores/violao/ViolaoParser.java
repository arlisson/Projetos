// Generated from br\edu\iff\ec\compiladores\violao\Violao.g4 by ANTLR 4.13.0
package br.edu.iff.ec.compiladores.violao;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class ViolaoParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.0", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		PC_INICIO=1, ABRE_CHAVE=2, FECHA_CHAVE=3, ACORDE=4, ATRIBUIR=5, FIM_CADEIA=6, 
		FINAL=7, PC_ACORDES=8, ERRO=9, ESPACO_BRANCO=10;
	public static final int
		RULE_criarCampo = 0;
	private static String[] makeRuleNames() {
		return new String[] {
			"criarCampo"
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

	@Override
	public String getGrammarFileName() { return "Violao.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public ViolaoParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CriarCampoContext extends ParserRuleContext {
		public Token PC_INICIO;
		public List<Token> pc_inicio = new ArrayList<Token>();
		public Token ABRE_CHAVE;
		public List<Token> abre_chave = new ArrayList<Token>();
		public Token ERRO;
		public List<Token> erro = new ArrayList<Token>();
		public Token ACORDE;
		public List<Token> acorde = new ArrayList<Token>();
		public Token ATRIBUIR;
		public List<Token> atribuir = new ArrayList<Token>();
		public Token PC_ACORDES;
		public List<Token> pc_acordes = new ArrayList<Token>();
		public Token FIM_CADEIA;
		public List<Token> fim_cadeia = new ArrayList<Token>();
		public Token FECHA_CHAVE;
		public List<Token> fecha_chave = new ArrayList<Token>();
		public TerminalNode EOF() { return getToken(ViolaoParser.EOF, 0); }
		public TerminalNode PC_INICIO() { return getToken(ViolaoParser.PC_INICIO, 0); }
		public TerminalNode ABRE_CHAVE() { return getToken(ViolaoParser.ABRE_CHAVE, 0); }
		public TerminalNode FECHA_CHAVE() { return getToken(ViolaoParser.FECHA_CHAVE, 0); }
		public List<TerminalNode> ACORDE() { return getTokens(ViolaoParser.ACORDE); }
		public TerminalNode ACORDE(int i) {
			return getToken(ViolaoParser.ACORDE, i);
		}
		public List<TerminalNode> ATRIBUIR() { return getTokens(ViolaoParser.ATRIBUIR); }
		public TerminalNode ATRIBUIR(int i) {
			return getToken(ViolaoParser.ATRIBUIR, i);
		}
		public List<TerminalNode> PC_ACORDES() { return getTokens(ViolaoParser.PC_ACORDES); }
		public TerminalNode PC_ACORDES(int i) {
			return getToken(ViolaoParser.PC_ACORDES, i);
		}
		public List<TerminalNode> FIM_CADEIA() { return getTokens(ViolaoParser.FIM_CADEIA); }
		public TerminalNode FIM_CADEIA(int i) {
			return getToken(ViolaoParser.FIM_CADEIA, i);
		}
		public List<TerminalNode> ERRO() { return getTokens(ViolaoParser.ERRO); }
		public TerminalNode ERRO(int i) {
			return getToken(ViolaoParser.ERRO, i);
		}
		public CriarCampoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_criarCampo; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ViolaoListener ) ((ViolaoListener)listener).enterCriarCampo(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ViolaoListener ) ((ViolaoListener)listener).exitCriarCampo(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ViolaoVisitor ) return ((ViolaoVisitor<? extends T>)visitor).visitCriarCampo(this);
			else return visitor.visitChildren(this);
		}
	}

	public final CriarCampoContext criarCampo() throws RecognitionException {
		CriarCampoContext _localctx = new CriarCampoContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_criarCampo);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2);
			((CriarCampoContext)_localctx).PC_INICIO = match(PC_INICIO);
			((CriarCampoContext)_localctx).pc_inicio.add(((CriarCampoContext)_localctx).PC_INICIO);
			setState(3);
			((CriarCampoContext)_localctx).ABRE_CHAVE = match(ABRE_CHAVE);
			((CriarCampoContext)_localctx).abre_chave.add(((CriarCampoContext)_localctx).ABRE_CHAVE);
			setState(14); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(5);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==ERRO) {
					{
					setState(4);
					((CriarCampoContext)_localctx).ERRO = match(ERRO);
					((CriarCampoContext)_localctx).erro.add(((CriarCampoContext)_localctx).ERRO);
					}
				}

				setState(7);
				((CriarCampoContext)_localctx).ACORDE = match(ACORDE);
				((CriarCampoContext)_localctx).acorde.add(((CriarCampoContext)_localctx).ACORDE);
				setState(8);
				((CriarCampoContext)_localctx).ATRIBUIR = match(ATRIBUIR);
				((CriarCampoContext)_localctx).atribuir.add(((CriarCampoContext)_localctx).ATRIBUIR);
				setState(9);
				((CriarCampoContext)_localctx).PC_ACORDES = match(PC_ACORDES);
				((CriarCampoContext)_localctx).pc_acordes.add(((CriarCampoContext)_localctx).PC_ACORDES);
				setState(10);
				((CriarCampoContext)_localctx).FIM_CADEIA = match(FIM_CADEIA);
				((CriarCampoContext)_localctx).fim_cadeia.add(((CriarCampoContext)_localctx).FIM_CADEIA);
				setState(12);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,1,_ctx) ) {
				case 1:
					{
					setState(11);
					((CriarCampoContext)_localctx).ERRO = match(ERRO);
					((CriarCampoContext)_localctx).erro.add(((CriarCampoContext)_localctx).ERRO);
					}
					break;
				}
				}
				}
				setState(16); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==ACORDE || _la==ERRO );
			setState(18);
			((CriarCampoContext)_localctx).FECHA_CHAVE = match(FECHA_CHAVE);
			((CriarCampoContext)_localctx).fecha_chave.add(((CriarCampoContext)_localctx).FECHA_CHAVE);
			setState(19);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001\n\u0016\u0002\u0000\u0007\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0003\u0000\u0006\b\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0003\u0000\r\b\u0000\u0004\u0000\u000f\b\u0000\u000b"+
		"\u0000\f\u0000\u0010\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0000"+
		"\u0000\u0001\u0000\u0000\u0000\u0017\u0000\u0002\u0001\u0000\u0000\u0000"+
		"\u0002\u0003\u0005\u0001\u0000\u0000\u0003\u000e\u0005\u0002\u0000\u0000"+
		"\u0004\u0006\u0005\t\u0000\u0000\u0005\u0004\u0001\u0000\u0000\u0000\u0005"+
		"\u0006\u0001\u0000\u0000\u0000\u0006\u0007\u0001\u0000\u0000\u0000\u0007"+
		"\b\u0005\u0004\u0000\u0000\b\t\u0005\u0005\u0000\u0000\t\n\u0005\b\u0000"+
		"\u0000\n\f\u0005\u0006\u0000\u0000\u000b\r\u0005\t\u0000\u0000\f\u000b"+
		"\u0001\u0000\u0000\u0000\f\r\u0001\u0000\u0000\u0000\r\u000f\u0001\u0000"+
		"\u0000\u0000\u000e\u0005\u0001\u0000\u0000\u0000\u000f\u0010\u0001\u0000"+
		"\u0000\u0000\u0010\u000e\u0001\u0000\u0000\u0000\u0010\u0011\u0001\u0000"+
		"\u0000\u0000\u0011\u0012\u0001\u0000\u0000\u0000\u0012\u0013\u0005\u0003"+
		"\u0000\u0000\u0013\u0014\u0005\u0000\u0000\u0001\u0014\u0001\u0001\u0000"+
		"\u0000\u0000\u0003\u0005\f\u0010";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}