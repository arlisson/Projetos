package pokemon;

import pokemonEntry.PokemonEntry;

public class Pokemon {
	
	private int number;
	private String name;
	private Type tipo1;
	private Type tipo2;
	private PokemonEntry pokemonentry;
	public Pokemon(int number, String name, Type tipo1, Type tipo2, PokemonEntry pokemonentry) {
		super();
		setNumber(number);
		setName(name);
		setTipo1(tipo1);
		setTipo2(tipo2);
		setPokemonentry(pokemonentry);
	}
	public int getNumber() {
		return number;
	}
	public void setNumber(int number) {
		this.number = number;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public Type getTipo1() {
		return tipo1;
	}
	public void setTipo1(Type tipo1) {
		this.tipo1 = tipo1;
	}
	public Type getTipo2() {
		return tipo2;
	}
	public void setTipo2(Type tipo2) {
		this.tipo2 = tipo2;
	}
	public PokemonEntry getPokemonentry() {
		return pokemonentry;
	}
	public void setPokemonentry(PokemonEntry pokemonentry) {
		this.pokemonentry = pokemonentry;
	}
	@Override
	public String toString() {
		return "Número: " + number + ", Nome: " + name + ", Tipo1: " + tipo1.getTipo() + ", Tipo2: " + tipo2.getTipo()+", "
				 + pokemonentry;
	}
	
	
	
	
}
