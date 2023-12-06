package principal;

import party.Party;
import pokedex.*;
import pokemon.*;
import pokemonEncounter.*;
import pokemonEntry.*;

import java.util.List;
import java.util.Scanner;
import java.util.ArrayList;

public class Principal {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		
		ArrayList<Pokemon> pokemons = new ArrayList<Pokemon>();
		ArrayList<PokemonEntry> pentries = new ArrayList<PokemonEntry>();
		Scanner sc = new Scanner(System.in);
		
		pokemons.add(new Pokemon(1, "Bulbasauro",new Type("Grama"),new Type("Venenoso"),new PokemonEntry("Semente",0.7,6.9,"Bulbapenis",false)));
		pokemons.add(new Pokemon(2, "Ivysaur", new Type("Grama"), new Type("Venenoso"), new PokemonEntry("Semente", 1.0, 13.0, "Ivypenis", false)));
		pokemons.add(new Pokemon(3, "Venusaur", new Type("Grama"), new Type("Venenoso"), new PokemonEntry("Semente", 2.0, 100.0, "Venusapenis", false)));
		pokemons.add(new Pokemon(4, "Charmander", new Type("Fogo"), new Type("Lutador"), new PokemonEntry("Chama", 0.6, 8.5, "Charmeleon", false)));
		pokemons.add(new Pokemon(5, "Charmeleon", new Type("Fogo"), new Type("Lutador"), new PokemonEntry("Chama", 1.1, 19.0, "Charizard", false)));
		pokemons.add(new Pokemon(6, "Charizard", new Type("Fogo"), new Type("Voador"), new PokemonEntry("Chama", 1.7, 90.5, "Charizard", false)));
		pokemons.add(new Pokemon(7, "Squirtle", new Type("Água"), new Type("Gelo"), new PokemonEntry("Tartaruga", 0.5, 9.0, "Wartortle", false)));
		pokemons.add(new Pokemon(8, "Wartortle", new Type("Água"), new Type("Gelo"), new PokemonEntry("Tartaruga", 1.0, 22.5, "Blastoise", false)));
		pokemons.add(new Pokemon(9, "Blastoise", new Type("Água"), new Type("Gelo"), new PokemonEntry("Tartaruga", 1.6, 85.5, "Blastoise", false)));
		pokemons.add(new Pokemon(10, "Caterpie", new Type("Inseto"), new Type("Voador"), new PokemonEntry("Lagarta", 0.3, 2.9, "Metapod", false)));
		pokemons.add(new Pokemon(11, "Metapod", new Type("Inseto"), new Type("Voador"), new PokemonEntry("Casulo", 0.7, 9.9, "Butterfree", false)));
		
		        
        int a = 0;
		
		Pokedex pokedex = Pokedex.getInstance();
		Party party = Party.getInstance();
		
		
		int escolha = 0;
		
		while (escolha!=4){
			System.out.println("1 - Visualizar Pokedex\n2 - Visualizar Equipe\n3 - Encontrar pokémon selvagem\n4 - Terminar Jogo\n");
			escolha = sc.nextInt();
			
			switch (escolha){
				
			case 1:
				
				List<PokemonEntry> pe = pokedex.getPokemon();
				if(pe.size()==0) {
					System.out.println("Nenhum Pokémon encontrado!");
				}else {
					System.out.println("\n----------Capturados----------\n");
					for(PokemonEntry p:pe) {
						if(p.isCaptured()) {						
							System.out.println(p.getPokemon().toString());
						}
						
					}
					System.out.println("\n----------Não Capturados----------\n");
					for(PokemonEntry p:pe) {
						if(!p.isCaptured()) {						
							System.out.println(p.getPokemon().toString());
						}
						
					}
					
				}
				
				break;
			
			case 2:
				List<Pokemon> pp = party.getPokemonList();
				if(pp.size()==0) {
					System.out.println("\nEquipe vazia!\n");
				}else {
					System.out.println("----------Pokémons na equipe----------");
					for(Pokemon pokemon:pp) {
						System.out.println(pokemon.toString());
					}
				
					
				}
				break;
			
			case 3:
				
				System.out.println("Você encontrou um "+ pokemons.get(a).getName() +", o que deseja fazer?\n1 - Capturar\n2 - Fujir");
				escolha = sc.nextInt();
				
				switch(escolha) {
				case 1:						
					System.out.println(a);
					new PokemonEncounter().tryCapture(pokemons.get(a));					
					
					System.out.println( pokemons.get(a).getName()+" Capturado!!");
					a++;
					break;
				
				case 2:
					
					new PokemonEncounter().runAway(pokemons.get(a));
					System.out.println( pokemons.get(a).getName()+" Fugiu!!");
					a++;
				}
				
			
			}
			
			
		}
		
	
		
		
		
	}

}
