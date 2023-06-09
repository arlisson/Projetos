// Generated from br\edu\iff\ec\compiladores\yugioh_parser\Parser.g4 by ANTLR 4.13.0
package br.edu.iff.ec.compiladores.yugioh_parser;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link ParserParser}.
 */
public interface ParserListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link ParserParser#criarCarta}.
	 * @param ctx the parse tree
	 */
	void enterCriarCarta(ParserParser.CriarCartaContext ctx);
	/**
	 * Exit a parse tree produced by {@link ParserParser#criarCarta}.
	 * @param ctx the parse tree
	 */
	void exitCriarCarta(ParserParser.CriarCartaContext ctx);
}