// Generated from br\edu\iff\ec\compiladores\violao\Violao.g4 by ANTLR 4.13.0
package br.edu.iff.ec.compiladores.violao;
import org.antlr.v4.runtime.tree.AbstractParseTreeVisitor;

/**
 * This class provides an empty implementation of {@link ViolaoVisitor},
 * which can be extended to create a visitor which only needs to handle a subset
 * of the available methods.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
@SuppressWarnings("CheckReturnValue")
public class ViolaoBaseVisitor<T> extends AbstractParseTreeVisitor<T> implements ViolaoVisitor<T> {
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public T visitCriarCampo(ViolaoParser.CriarCampoContext ctx) { return visitChildren(ctx); }
}