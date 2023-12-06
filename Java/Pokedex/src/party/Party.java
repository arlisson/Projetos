package party;

import java.util.List;

import pokemon.Pokemon;
import java.util.ArrayList;
public class Party {
	
	private static Party party;
	private List<Pokemon> pokemon = new ArrayList<Pokemon>();
	
	private Party() {
		// TODO Auto-generated constructor stub
	}
	
	public static Party getInstance() {
		if(party == null) {
			party = new Party();
		}
		
		return party;
	}
	
	public List<Pokemon> getPokemonList(){
		
		return this.pokemon;
	}
	
	public void remove() {
		this.pokemon.remove(0);
		
	}
	
	public void insert(Pokemon p) {
		this.pokemon.add(p);
		
	}
}
