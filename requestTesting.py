import requests
import json

def main():

    print("What agency's documents would you like to view?")
    #probably want to use natural-resources-conservation-service
    agency = input()

    print("How many documents would you like to see?")
    num_docs = input()

    print("Begining request")
    response = requests.get(f"https://www.federalregister.gov/api/v1/documents.json?fields[]=abstract&per_page={num_docs}&order=newest&conditions[agencies][]={agency}")
    print(response.status_code)


    response_json = response.json()


    results = response_json['results']

    print(type(results))

    for abstract in results:
        print(abstract)




if __name__ == "__main__":
    main()
