// Generated from br\edu\iff\ec\compiladores\yugioh_parser\Parser.g4 by ANTLR 4.13.0
package br.edu.iff.ec.compiladores.yugioh_parser;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class ParserParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.0", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		PC_INICIO=1, PC_CARD=2, PC_CARD_MAGIC=3, PC_NAME=4, PC_LEVEL=5, PC_ATTRIBUTE=6, 
		PC_TYPE=7, PC_ATTACK=8, PC_DEFFENSE=9, PC_DESCRIPTION=10, PC_IMAGE=11, 
		PC_FIM=12, ERRO_CARD=13, CARD_MONSTER=14, CARD_MAGIC=15, ATTRIBUTE=16, 
		TYPE=17, PNG=18, DIGITO=19, CADEIA=20, FIM_CADEIA=21, ATRIBUICAO=22, VIRG=23, 
		ESPACO_BRANCO=24, COMENTARIO=25;
	public static final int
		RULE_criarCarta = 0;
	private static String[] makeRuleNames() {
		return new String[] {
			"criarCarta"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'CREATE_CARD'", "'CARD-MONSTER'", "'CARD-MAGIC'", "'NAME'", "'LEVEL'", 
			"'ATTRIBUTE'", "'TYPE'", "'ATTACK'", "'DEFFENSE'", "'DESCRIPTION'", "'IMAGE'", 
			"'END_CREATE_CARD'", null, null, null, null, null, null, null, null, 
			"';'", "':'", "','"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "PC_INICIO", "PC_CARD", "PC_CARD_MAGIC", "PC_NAME", "PC_LEVEL", 
			"PC_ATTRIBUTE", "PC_TYPE", "PC_ATTACK", "PC_DEFFENSE", "PC_DESCRIPTION", 
			"PC_IMAGE", "PC_FIM", "ERRO_CARD", "CARD_MONSTER", "CARD_MAGIC", "ATTRIBUTE", 
			"TYPE", "PNG", "DIGITO", "CADEIA", "FIM_CADEIA", "ATRIBUICAO", "VIRG", 
			"ESPACO_BRANCO", "COMENTARIO"
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
	public String getGrammarFileName() { return "Parser.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public ParserParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CriarCartaContext extends ParserRuleContext {
		public Token pc_inicio;
		public Token ERRO_CARD;
		public List<Token> erro = new ArrayList<Token>();
		public Token PC_CARD;
		public List<Token> pc_card = new ArrayList<Token>();
		public Token ATRIBUICAO;
		public List<Token> atribuicao = new ArrayList<Token>();
		public Token CARD_MONSTER;
		public List<Token> tipo_carta = new ArrayList<Token>();
		public Token FIM_CADEIA;
		public List<Token> fim_cadeia = new ArrayList<Token>();
		public Token PC_NAME;
		public List<Token> pc_name = new ArrayList<Token>();
		public Token CADEIA;
		public List<Token> monstro_nome = new ArrayList<Token>();
		public Token PC_LEVEL;
		public List<Token> pc_level = new ArrayList<Token>();
		public Token DIGITO;
		public List<Token> level = new ArrayList<Token>();
		public Token PC_ATTRIBUTE;
		public List<Token> pc_atributo = new ArrayList<Token>();
		public Token ATTRIBUTE;
		public List<Token> atributo = new ArrayList<Token>();
		public Token PC_TYPE;
		public List<Token> pc_tipo = new ArrayList<Token>();
		public Token TYPE;
		public List<Token> tipo = new ArrayList<Token>();
		public Token PC_ATTACK;
		public List<Token> pc_atk = new ArrayList<Token>();
		public List<Token> atk = new ArrayList<Token>();
		public Token PC_DEFFENSE;
		public List<Token> pc_def = new ArrayList<Token>();
		public List<Token> def = new ArrayList<Token>();
		public Token PC_DESCRIPTION;
		public List<Token> pc_desc = new ArrayList<Token>();
		public List<Token> desc = new ArrayList<Token>();
		public Token PC_IMAGE;
		public List<Token> pc_image = new ArrayList<Token>();
		public Token PNG;
		public List<Token> png = new ArrayList<Token>();
		public Token PC_CARD_MAGIC;
		public List<Token> pc_cardm = new ArrayList<Token>();
		public Token CARD_MAGIC;
		public List<Token> tipo_cartam = new ArrayList<Token>();
		public List<Token> pc_namem = new ArrayList<Token>();
		public List<Token> magic_mone = new ArrayList<Token>();
		public List<Token> pc_descm = new ArrayList<Token>();
		public List<Token> desc_m = new ArrayList<Token>();
		public List<Token> pc_imagem = new ArrayList<Token>();
		public List<Token> magic_png = new ArrayList<Token>();
		public Token pc_fim;
		public List<TerminalNode> ATRIBUICAO() { return getTokens(ParserParser.ATRIBUICAO); }
		public TerminalNode ATRIBUICAO(int i) {
			return getToken(ParserParser.ATRIBUICAO, i);
		}
		public List<TerminalNode> FIM_CADEIA() { return getTokens(ParserParser.FIM_CADEIA); }
		public TerminalNode FIM_CADEIA(int i) {
			return getToken(ParserParser.FIM_CADEIA, i);
		}
		public TerminalNode EOF() { return getToken(ParserParser.EOF, 0); }
		public TerminalNode PC_INICIO() { return getToken(ParserParser.PC_INICIO, 0); }
		public TerminalNode PC_FIM() { return getToken(ParserParser.PC_FIM, 0); }
		public List<TerminalNode> PC_CARD() { return getTokens(ParserParser.PC_CARD); }
		public TerminalNode PC_CARD(int i) {
			return getToken(ParserParser.PC_CARD, i);
		}
		public List<TerminalNode> CARD_MONSTER() { return getTokens(ParserParser.CARD_MONSTER); }
		public TerminalNode CARD_MONSTER(int i) {
			return getToken(ParserParser.CARD_MONSTER, i);
		}
		public List<TerminalNode> PC_NAME() { return getTokens(ParserParser.PC_NAME); }
		public TerminalNode PC_NAME(int i) {
			return getToken(ParserParser.PC_NAME, i);
		}
		public List<TerminalNode> CADEIA() { return getTokens(ParserParser.CADEIA); }
		public TerminalNode CADEIA(int i) {
			return getToken(ParserParser.CADEIA, i);
		}
		public List<TerminalNode> PC_LEVEL() { return getTokens(ParserParser.PC_LEVEL); }
		public TerminalNode PC_LEVEL(int i) {
			return getToken(ParserParser.PC_LEVEL, i);
		}
		public List<TerminalNode> DIGITO() { return getTokens(ParserParser.DIGITO); }
		public TerminalNode DIGITO(int i) {
			return getToken(ParserParser.DIGITO, i);
		}
		public List<TerminalNode> PC_ATTRIBUTE() { return getTokens(ParserParser.PC_ATTRIBUTE); }
		public TerminalNode PC_ATTRIBUTE(int i) {
			return getToken(ParserParser.PC_ATTRIBUTE, i);
		}
		public List<TerminalNode> ATTRIBUTE() { return getTokens(ParserParser.ATTRIBUTE); }
		public TerminalNode ATTRIBUTE(int i) {
			return getToken(ParserParser.ATTRIBUTE, i);
		}
		public List<TerminalNode> PC_TYPE() { return getTokens(ParserParser.PC_TYPE); }
		public TerminalNode PC_TYPE(int i) {
			return getToken(ParserParser.PC_TYPE, i);
		}
		public List<TerminalNode> TYPE() { return getTokens(ParserParser.TYPE); }
		public TerminalNode TYPE(int i) {
			return getToken(ParserParser.TYPE, i);
		}
		public List<TerminalNode> PC_ATTACK() { return getTokens(ParserParser.PC_ATTACK); }
		public TerminalNode PC_ATTACK(int i) {
			return getToken(ParserParser.PC_ATTACK, i);
		}
		public List<TerminalNode> PC_DEFFENSE() { return getTokens(ParserParser.PC_DEFFENSE); }
		public TerminalNode PC_DEFFENSE(int i) {
			return getToken(ParserParser.PC_DEFFENSE, i);
		}
		public List<TerminalNode> PC_DESCRIPTION() { return getTokens(ParserParser.PC_DESCRIPTION); }
		public TerminalNode PC_DESCRIPTION(int i) {
			return getToken(ParserParser.PC_DESCRIPTION, i);
		}
		public List<TerminalNode> PC_IMAGE() { return getTokens(ParserParser.PC_IMAGE); }
		public TerminalNode PC_IMAGE(int i) {
			return getToken(ParserParser.PC_IMAGE, i);
		}
		public List<TerminalNode> PNG() { return getTokens(ParserParser.PNG); }
		public TerminalNode PNG(int i) {
			return getToken(ParserParser.PNG, i);
		}
		public List<TerminalNode> PC_CARD_MAGIC() { return getTokens(ParserParser.PC_CARD_MAGIC); }
		public TerminalNode PC_CARD_MAGIC(int i) {
			return getToken(ParserParser.PC_CARD_MAGIC, i);
		}
		public List<TerminalNode> CARD_MAGIC() { return getTokens(ParserParser.CARD_MAGIC); }
		public TerminalNode CARD_MAGIC(int i) {
			return getToken(ParserParser.CARD_MAGIC, i);
		}
		public List<TerminalNode> ERRO_CARD() { return getTokens(ParserParser.ERRO_CARD); }
		public TerminalNode ERRO_CARD(int i) {
			return getToken(ParserParser.ERRO_CARD, i);
		}
		public CriarCartaContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_criarCarta; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ParserListener ) ((ParserListener)listener).enterCriarCarta(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ParserListener ) ((ParserListener)listener).exitCriarCarta(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ParserVisitor ) return ((ParserVisitor<? extends T>)visitor).visitCriarCarta(this);
			else return visitor.visitChildren(this);
		}
	}

	public final CriarCartaContext criarCarta() throws RecognitionException {
		CriarCartaContext _localctx = new CriarCartaContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_criarCarta);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2);
			((CriarCartaContext)_localctx).pc_inicio = match(PC_INICIO);
			setState(3);
			match(ATRIBUICAO);
			setState(95); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				setState(95);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,13,_ctx) ) {
				case 1:
					{
					{
					setState(5);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(4);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(7);
					((CriarCartaContext)_localctx).PC_CARD = match(PC_CARD);
					((CriarCartaContext)_localctx).pc_card.add(((CriarCartaContext)_localctx).PC_CARD);
					setState(8);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(9);
					((CriarCartaContext)_localctx).CARD_MONSTER = match(CARD_MONSTER);
					((CriarCartaContext)_localctx).tipo_carta.add(((CriarCartaContext)_localctx).CARD_MONSTER);
					setState(10);
					((CriarCartaContext)_localctx).FIM_CADEIA = match(FIM_CADEIA);
					((CriarCartaContext)_localctx).fim_cadeia.add(((CriarCartaContext)_localctx).FIM_CADEIA);
					setState(12);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(11);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(14);
					((CriarCartaContext)_localctx).PC_NAME = match(PC_NAME);
					((CriarCartaContext)_localctx).pc_name.add(((CriarCartaContext)_localctx).PC_NAME);
					setState(15);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(16);
					((CriarCartaContext)_localctx).CADEIA = match(CADEIA);
					((CriarCartaContext)_localctx).monstro_nome.add(((CriarCartaContext)_localctx).CADEIA);
					setState(17);
					((CriarCartaContext)_localctx).FIM_CADEIA = match(FIM_CADEIA);
					((CriarCartaContext)_localctx).fim_cadeia.add(((CriarCartaContext)_localctx).FIM_CADEIA);
					setState(19);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(18);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(21);
					((CriarCartaContext)_localctx).PC_LEVEL = match(PC_LEVEL);
					((CriarCartaContext)_localctx).pc_level.add(((CriarCartaContext)_localctx).PC_LEVEL);
					setState(22);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(23);
					((CriarCartaContext)_localctx).DIGITO = match(DIGITO);
					((CriarCartaContext)_localctx).level.add(((CriarCartaContext)_localctx).DIGITO);
					setState(24);
					((CriarCartaContext)_localctx).FIM_CADEIA = match(FIM_CADEIA);
					((CriarCartaContext)_localctx).fim_cadeia.add(((CriarCartaContext)_localctx).FIM_CADEIA);
					setState(26);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(25);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(28);
					((CriarCartaContext)_localctx).PC_ATTRIBUTE = match(PC_ATTRIBUTE);
					((CriarCartaContext)_localctx).pc_atributo.add(((CriarCartaContext)_localctx).PC_ATTRIBUTE);
					setState(29);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(30);
					((CriarCartaContext)_localctx).ATTRIBUTE = match(ATTRIBUTE);
					((CriarCartaContext)_localctx).atributo.add(((CriarCartaContext)_localctx).ATTRIBUTE);
					setState(31);
					((CriarCartaContext)_localctx).FIM_CADEIA = match(FIM_CADEIA);
					((CriarCartaContext)_localctx).fim_cadeia.add(((CriarCartaContext)_localctx).FIM_CADEIA);
					setState(33);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(32);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(35);
					((CriarCartaContext)_localctx).PC_TYPE = match(PC_TYPE);
					((CriarCartaContext)_localctx).pc_tipo.add(((CriarCartaContext)_localctx).PC_TYPE);
					setState(36);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(37);
					((CriarCartaContext)_localctx).TYPE = match(TYPE);
					((CriarCartaContext)_localctx).tipo.add(((CriarCartaContext)_localctx).TYPE);
					setState(38);
					((CriarCartaContext)_localctx).FIM_CADEIA = match(FIM_CADEIA);
					((CriarCartaContext)_localctx).fim_cadeia.add(((CriarCartaContext)_localctx).FIM_CADEIA);
					setState(40);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(39);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(42);
					((CriarCartaContext)_localctx).PC_ATTACK = match(PC_ATTACK);
					((CriarCartaContext)_localctx).pc_atk.add(((CriarCartaContext)_localctx).PC_ATTACK);
					setState(43);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(44);
					((CriarCartaContext)_localctx).DIGITO = match(DIGITO);
					((CriarCartaContext)_localctx).atk.add(((CriarCartaContext)_localctx).DIGITO);
					setState(45);
					((CriarCartaContext)_localctx).FIM_CADEIA = match(FIM_CADEIA);
					((CriarCartaContext)_localctx).fim_cadeia.add(((CriarCartaContext)_localctx).FIM_CADEIA);
					setState(47);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(46);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(49);
					((CriarCartaContext)_localctx).PC_DEFFENSE = match(PC_DEFFENSE);
					((CriarCartaContext)_localctx).pc_def.add(((CriarCartaContext)_localctx).PC_DEFFENSE);
					setState(50);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(51);
					((CriarCartaContext)_localctx).DIGITO = match(DIGITO);
					((CriarCartaContext)_localctx).def.add(((CriarCartaContext)_localctx).DIGITO);
					setState(52);
					((CriarCartaContext)_localctx).FIM_CADEIA = match(FIM_CADEIA);
					((CriarCartaContext)_localctx).fim_cadeia.add(((CriarCartaContext)_localctx).FIM_CADEIA);
					setState(54);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(53);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(56);
					((CriarCartaContext)_localctx).PC_DESCRIPTION = match(PC_DESCRIPTION);
					((CriarCartaContext)_localctx).pc_desc.add(((CriarCartaContext)_localctx).PC_DESCRIPTION);
					setState(57);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(58);
					((CriarCartaContext)_localctx).CADEIA = match(CADEIA);
					((CriarCartaContext)_localctx).desc.add(((CriarCartaContext)_localctx).CADEIA);
					setState(59);
					((CriarCartaContext)_localctx).FIM_CADEIA = match(FIM_CADEIA);
					((CriarCartaContext)_localctx).fim_cadeia.add(((CriarCartaContext)_localctx).FIM_CADEIA);
					setState(61);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(60);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(63);
					((CriarCartaContext)_localctx).PC_IMAGE = match(PC_IMAGE);
					((CriarCartaContext)_localctx).pc_image.add(((CriarCartaContext)_localctx).PC_IMAGE);
					setState(64);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(65);
					((CriarCartaContext)_localctx).PNG = match(PNG);
					((CriarCartaContext)_localctx).png.add(((CriarCartaContext)_localctx).PNG);
					setState(66);
					((CriarCartaContext)_localctx).FIM_CADEIA = match(FIM_CADEIA);
					((CriarCartaContext)_localctx).fim_cadeia.add(((CriarCartaContext)_localctx).FIM_CADEIA);
					}
					}
					break;
				case 2:
					{
					{
					setState(68);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(67);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(70);
					((CriarCartaContext)_localctx).PC_CARD_MAGIC = match(PC_CARD_MAGIC);
					((CriarCartaContext)_localctx).pc_cardm.add(((CriarCartaContext)_localctx).PC_CARD_MAGIC);
					setState(71);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(72);
					((CriarCartaContext)_localctx).CARD_MAGIC = match(CARD_MAGIC);
					((CriarCartaContext)_localctx).tipo_cartam.add(((CriarCartaContext)_localctx).CARD_MAGIC);
					setState(73);
					match(FIM_CADEIA);
					setState(75);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(74);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(77);
					((CriarCartaContext)_localctx).PC_NAME = match(PC_NAME);
					((CriarCartaContext)_localctx).pc_namem.add(((CriarCartaContext)_localctx).PC_NAME);
					setState(78);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(79);
					((CriarCartaContext)_localctx).CADEIA = match(CADEIA);
					((CriarCartaContext)_localctx).magic_mone.add(((CriarCartaContext)_localctx).CADEIA);
					setState(80);
					match(FIM_CADEIA);
					setState(82);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(81);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(84);
					((CriarCartaContext)_localctx).PC_DESCRIPTION = match(PC_DESCRIPTION);
					((CriarCartaContext)_localctx).pc_descm.add(((CriarCartaContext)_localctx).PC_DESCRIPTION);
					setState(85);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(86);
					((CriarCartaContext)_localctx).CADEIA = match(CADEIA);
					((CriarCartaContext)_localctx).desc_m.add(((CriarCartaContext)_localctx).CADEIA);
					setState(87);
					match(FIM_CADEIA);
					setState(89);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==ERRO_CARD) {
						{
						setState(88);
						((CriarCartaContext)_localctx).ERRO_CARD = match(ERRO_CARD);
						((CriarCartaContext)_localctx).erro.add(((CriarCartaContext)_localctx).ERRO_CARD);
						}
					}

					setState(91);
					((CriarCartaContext)_localctx).PC_IMAGE = match(PC_IMAGE);
					((CriarCartaContext)_localctx).pc_imagem.add(((CriarCartaContext)_localctx).PC_IMAGE);
					setState(92);
					((CriarCartaContext)_localctx).ATRIBUICAO = match(ATRIBUICAO);
					((CriarCartaContext)_localctx).atribuicao.add(((CriarCartaContext)_localctx).ATRIBUICAO);
					setState(93);
					((CriarCartaContext)_localctx).PNG = match(PNG);
					((CriarCartaContext)_localctx).magic_png.add(((CriarCartaContext)_localctx).PNG);
					setState(94);
					match(FIM_CADEIA);
					}
					}
					break;
				}
				}
				setState(97); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & 8204L) != 0) );
			setState(99);
			((CriarCartaContext)_localctx).pc_fim = match(PC_FIM);
			setState(100);
			match(FIM_CADEIA);
			setState(101);
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
		"\u0004\u0001\u0019h\u0002\u0000\u0007\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0003\u0000\u0006\b\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0003\u0000\r\b\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0003\u0000\u0014\b\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0003\u0000\u001b\b\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0003\u0000\"\b"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0003"+
		"\u0000)\b\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0003\u00000\b\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0003\u00007\b\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0003\u0000>\b\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0003\u0000E\b\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0003\u0000L\b"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0003"+
		"\u0000S\b\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0003\u0000Z\b\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0004\u0000`\b\u0000\u000b\u0000\f\u0000a\u0001\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0001\u0000\u0000\u0000"+
		"u\u0000\u0002\u0001\u0000\u0000\u0000\u0002\u0003\u0005\u0001\u0000\u0000"+
		"\u0003_\u0005\u0016\u0000\u0000\u0004\u0006\u0005\r\u0000\u0000\u0005"+
		"\u0004\u0001\u0000\u0000\u0000\u0005\u0006\u0001\u0000\u0000\u0000\u0006"+
		"\u0007\u0001\u0000\u0000\u0000\u0007\b\u0005\u0002\u0000\u0000\b\t\u0005"+
		"\u0016\u0000\u0000\t\n\u0005\u000e\u0000\u0000\n\f\u0005\u0015\u0000\u0000"+
		"\u000b\r\u0005\r\u0000\u0000\f\u000b\u0001\u0000\u0000\u0000\f\r\u0001"+
		"\u0000\u0000\u0000\r\u000e\u0001\u0000\u0000\u0000\u000e\u000f\u0005\u0004"+
		"\u0000\u0000\u000f\u0010\u0005\u0016\u0000\u0000\u0010\u0011\u0005\u0014"+
		"\u0000\u0000\u0011\u0013\u0005\u0015\u0000\u0000\u0012\u0014\u0005\r\u0000"+
		"\u0000\u0013\u0012\u0001\u0000\u0000\u0000\u0013\u0014\u0001\u0000\u0000"+
		"\u0000\u0014\u0015\u0001\u0000\u0000\u0000\u0015\u0016\u0005\u0005\u0000"+
		"\u0000\u0016\u0017\u0005\u0016\u0000\u0000\u0017\u0018\u0005\u0013\u0000"+
		"\u0000\u0018\u001a\u0005\u0015\u0000\u0000\u0019\u001b\u0005\r\u0000\u0000"+
		"\u001a\u0019\u0001\u0000\u0000\u0000\u001a\u001b\u0001\u0000\u0000\u0000"+
		"\u001b\u001c\u0001\u0000\u0000\u0000\u001c\u001d\u0005\u0006\u0000\u0000"+
		"\u001d\u001e\u0005\u0016\u0000\u0000\u001e\u001f\u0005\u0010\u0000\u0000"+
		"\u001f!\u0005\u0015\u0000\u0000 \"\u0005\r\u0000\u0000! \u0001\u0000\u0000"+
		"\u0000!\"\u0001\u0000\u0000\u0000\"#\u0001\u0000\u0000\u0000#$\u0005\u0007"+
		"\u0000\u0000$%\u0005\u0016\u0000\u0000%&\u0005\u0011\u0000\u0000&(\u0005"+
		"\u0015\u0000\u0000\')\u0005\r\u0000\u0000(\'\u0001\u0000\u0000\u0000("+
		")\u0001\u0000\u0000\u0000)*\u0001\u0000\u0000\u0000*+\u0005\b\u0000\u0000"+
		"+,\u0005\u0016\u0000\u0000,-\u0005\u0013\u0000\u0000-/\u0005\u0015\u0000"+
		"\u0000.0\u0005\r\u0000\u0000/.\u0001\u0000\u0000\u0000/0\u0001\u0000\u0000"+
		"\u000001\u0001\u0000\u0000\u000012\u0005\t\u0000\u000023\u0005\u0016\u0000"+
		"\u000034\u0005\u0013\u0000\u000046\u0005\u0015\u0000\u000057\u0005\r\u0000"+
		"\u000065\u0001\u0000\u0000\u000067\u0001\u0000\u0000\u000078\u0001\u0000"+
		"\u0000\u000089\u0005\n\u0000\u00009:\u0005\u0016\u0000\u0000:;\u0005\u0014"+
		"\u0000\u0000;=\u0005\u0015\u0000\u0000<>\u0005\r\u0000\u0000=<\u0001\u0000"+
		"\u0000\u0000=>\u0001\u0000\u0000\u0000>?\u0001\u0000\u0000\u0000?@\u0005"+
		"\u000b\u0000\u0000@A\u0005\u0016\u0000\u0000AB\u0005\u0012\u0000\u0000"+
		"B`\u0005\u0015\u0000\u0000CE\u0005\r\u0000\u0000DC\u0001\u0000\u0000\u0000"+
		"DE\u0001\u0000\u0000\u0000EF\u0001\u0000\u0000\u0000FG\u0005\u0003\u0000"+
		"\u0000GH\u0005\u0016\u0000\u0000HI\u0005\u000f\u0000\u0000IK\u0005\u0015"+
		"\u0000\u0000JL\u0005\r\u0000\u0000KJ\u0001\u0000\u0000\u0000KL\u0001\u0000"+
		"\u0000\u0000LM\u0001\u0000\u0000\u0000MN\u0005\u0004\u0000\u0000NO\u0005"+
		"\u0016\u0000\u0000OP\u0005\u0014\u0000\u0000PR\u0005\u0015\u0000\u0000"+
		"QS\u0005\r\u0000\u0000RQ\u0001\u0000\u0000\u0000RS\u0001\u0000\u0000\u0000"+
		"ST\u0001\u0000\u0000\u0000TU\u0005\n\u0000\u0000UV\u0005\u0016\u0000\u0000"+
		"VW\u0005\u0014\u0000\u0000WY\u0005\u0015\u0000\u0000XZ\u0005\r\u0000\u0000"+
		"YX\u0001\u0000\u0000\u0000YZ\u0001\u0000\u0000\u0000Z[\u0001\u0000\u0000"+
		"\u0000[\\\u0005\u000b\u0000\u0000\\]\u0005\u0016\u0000\u0000]^\u0005\u0012"+
		"\u0000\u0000^`\u0005\u0015\u0000\u0000_\u0005\u0001\u0000\u0000\u0000"+
		"_D\u0001\u0000\u0000\u0000`a\u0001\u0000\u0000\u0000a_\u0001\u0000\u0000"+
		"\u0000ab\u0001\u0000\u0000\u0000bc\u0001\u0000\u0000\u0000cd\u0005\f\u0000"+
		"\u0000de\u0005\u0015\u0000\u0000ef\u0005\u0000\u0000\u0001f\u0001\u0001"+
		"\u0000\u0000\u0000\u000f\u0005\f\u0013\u001a!(/6=DKRY_a";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}