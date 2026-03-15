import requests

def get_number_fact(number):
    response = requests.get(f"https://catfact.ninja/fact")
    data = response.json()
    print(data["fact"])

get_number_fact(42)

