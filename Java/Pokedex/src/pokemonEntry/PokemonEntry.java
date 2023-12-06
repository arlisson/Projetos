package pokemonEntry;

import pokemon.Pokemon;

public class PokemonEntry {
	
	private String category;
	private double wight;
	private double height;
	private String description;
	private boolean captured;
	private Pokemon pokemon;
	

	public PokemonEntry(String category, double wight, double height, String description, boolean captured) {
		
		setCategory(category);
		setWight(wight);
		setHeight(height);
		setDescription(description);
		setCaptured(captured);
		
		
	}
	public PokemonEntry(String category, double wight, double height, String description, boolean captured,Pokemon p) {
		
		setCategory(category);
		setWight(wight);
		setHeight(height);
		setDescription(description);
		setCaptured(captured);
		setPokemon(p);
		
		
	}

	public String getCategory() {
		return category;
	}

	public void setCategory(String category) {
		this.category = category;
	}

	public double getWight() {
		return wight;
	}

	public void setWight(double wight) {
		this.wight = wight;
	}

	public double getHeight() {
		return height;
	}

	public void setHeight(double height) {
		this.height = height;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public boolean isCaptured() {
		return captured;
	}

	public void setCaptured(boolean captured) {
		this.captured = captured;
	}
	
	
	public Pokemon getPokemon() {
		return pokemon;
	}

	public void setPokemon(Pokemon pokemon) {
		this.pokemon = pokemon;
	}

	@Override
	public String toString() {
		return " Categoria: " + category + ", Peso: " + wight + ", Altura: " + height + ", Descrição: "
				+ description + "\n";
	}
	
	

}
