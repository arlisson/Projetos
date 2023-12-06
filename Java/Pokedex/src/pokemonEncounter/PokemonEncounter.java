package pokemonEncounter;

import pokemon.Pokemon;
import pokemon.Type;
import pokemonEntry.PokemonEntry;
import pokedex.Pokedex;
import party.Party;

public class PokemonEncounter {
	
	private Pokemon pokemon;
	
	
	public void tryCapture(Pokemon p) {
		Pokedex pokedex = Pokedex.getInstance();
		p.getPokemonentry().setCaptured(true);
		p.setPokemonentry(new PokemonEntry(p.getPokemonentry().getCategory(),p.getPokemonentry().getWight(),p.getPokemonentry().getHeight(),p.getPokemonentry().getDescription(),p.getPokemonentry().isCaptured(),p));
		Party party = Party.getInstance();		
		
		pokedex.registerPokemon(p.getPokemonentry());
		if(party.getPokemonList().size()<6) {
			party.insert(p);
		}else {
			party.remove();
			party.insert(p);
		}
		
		
	}
	
	public void runAway(Pokemon p) {
		Pokedex pokedex = Pokedex.getInstance();
		p.setPokemonentry(new PokemonEntry("Desconhecido",0,0,"Desconhecido",false,p));
		p.setTipo1(new Type("Desconhecido"));
		p.setTipo2(new Type("Desconhecido"));
		pokedex.registerPokemon(p.getPokemonentry());
		
	}

}
