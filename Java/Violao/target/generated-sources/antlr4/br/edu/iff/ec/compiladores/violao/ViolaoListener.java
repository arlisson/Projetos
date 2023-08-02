// Generated from br\edu\iff\ec\compiladores\violao\Violao.g4 by ANTLR 4.13.0
package br.edu.iff.ec.compiladores.violao;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link ViolaoParser}.
 */
public interface ViolaoListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link ViolaoParser#criarCampo}.
	 * @param ctx the parse tree
	 */
	void enterCriarCampo(ViolaoParser.CriarCampoContext ctx);
	/**
	 * Exit a parse tree produced by {@link ViolaoParser#criarCampo}.
	 * @param ctx the parse tree
	 */
	void exitCriarCampo(ViolaoParser.CriarCampoContext ctx);
}