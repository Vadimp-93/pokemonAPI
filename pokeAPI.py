import requests
import json
import os
import random

fileName = "pokemon_collection.json"

def loadCollection():                                    #load pokemon file is exists
    if os.path.exists(fileName):
        with open(fileName, 'r') as f:
            return json.load(f)
    return {}

def saveCollection(collection):                          #save pokemon collection to json file
    with open(fileName, 'w') as f:
        json.dump(collection, f, indent=4)

def getPokemonList():
    url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results']
    else:
        return []
    
def getPokemonDetails(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"],
            "height": data["height"],
            "abilities": [a["ability"]["name"] for a in data["abilities"]]
        }
    return None

def displayPokemon(pokemon):
    print(f"\nName: {pokemon['name'].title()}")
    print(f"Height: {pokemon['height']}")
    print("Abilities:")
    for ability in pokemon['abilities']:
        print("-", ability)

def main():
    collection = loadCollection()

    while True:
        answer = input("\nWould you like to draw a Pokémon? (yes/no): ").strip().lower()
        if answer != "yes":
            print("Goodbye!")
            break

        allPokemons = getPokemonList()
        if not allPokemons:
            print("Could not fetch Pokémon list.")
            continue

        chosen = random.choice(allPokemons)
        name = chosen["name"]

        if name in collection:
            print(f"\n{name.title()} is already in your collection!")
            displayPokemon(collection[name])
        else:
            details = getPokemonDetails(chosen["url"])
            if details:
                collection[name] = details
                saveCollection(collection)
                displayPokemon(details)
            else:
                print("Failed to fetch data for this Pokémon.")

if __name__ == "__main__":
    main()