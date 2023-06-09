// Generated from br\edu\iff\ec\compiladores\yugioh_parser\Parser.g4 by ANTLR 4.13.0
package br.edu.iff.ec.compiladores.yugioh_parser;
import org.antlr.v4.runtime.tree.AbstractParseTreeVisitor;

/**
 * This class provides an empty implementation of {@link ParserVisitor},
 * which can be extended to create a visitor which only needs to handle a subset
 * of the available methods.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
@SuppressWarnings("CheckReturnValue")
public class ParserBaseVisitor<T> extends AbstractParseTreeVisitor<T> implements ParserVisitor<T> {
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public T visitCriarCarta(ParserParser.CriarCartaContext ctx) { return visitChildren(ctx); }
}