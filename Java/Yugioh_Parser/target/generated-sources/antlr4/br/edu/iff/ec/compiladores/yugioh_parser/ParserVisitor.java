// Generated from br\edu\iff\ec\compiladores\yugioh_parser\Parser.g4 by ANTLR 4.13.0
package br.edu.iff.ec.compiladores.yugioh_parser;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link ParserParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface ParserVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link ParserParser#criarCarta}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCriarCarta(ParserParser.CriarCartaContext ctx);
}