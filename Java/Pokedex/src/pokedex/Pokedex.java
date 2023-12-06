package pokedex;

import java.util.List;
import pokemonEntry.PokemonEntry;
import pokemon.Pokemon;
import java.util.ArrayList;

public class Pokedex {
	
	private static Pokedex pokedex;	
	private List<PokemonEntry> pokemonentries = new ArrayList<PokemonEntry>();
	private List<Pokemon> pokemon = new ArrayList<Pokemon>();
	
	
	public static Pokedex getInstance() {
		if (pokedex == null) {
			pokedex = new Pokedex();
		}
		return pokedex;
		
	}
	
	public void registerPokemon(PokemonEntry p) {
		this.pokemon.add(p.getPokemon());	
		this.pokemonentries.add(p);
		
	}
	
	public void seePokemon(PokemonEntry p) {		
		
		
	}
	
	public List<PokemonEntry> getPokemon() {
		
		return this.pokemonentries;
	}

}
