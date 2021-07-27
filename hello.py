import json


def main():
    print("starting main method")
    with open("C:/Baka-Bot/11.11.1/data/en_US/champion/Aatrox.json") as access_json:
        file_access = json.load(access_json)
    
    data_access = file_access['data']

    champion_access = data_access['Aatrox']
    
    spells_access = champion_access['spells']
    
    print(type(spells_access))
    print(spells_access[0])
    


if __name__ == "__main__":
    main()



