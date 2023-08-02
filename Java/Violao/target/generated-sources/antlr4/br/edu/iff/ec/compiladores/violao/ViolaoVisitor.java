// Generated from br\edu\iff\ec\compiladores\violao\Violao.g4 by ANTLR 4.13.0
package br.edu.iff.ec.compiladores.violao;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link ViolaoParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface ViolaoVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link ViolaoParser#criarCampo}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCriarCampo(ViolaoParser.CriarCampoContext ctx);
}