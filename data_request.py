import requests as rq
import pandas as pd

response = rq.get("https://davidmegginson.github.io/ourairports-data/airports.csv", allow_redirects=True)

with open("./data/airports_requested.csv", "w", encoding="utf-8") as file:
    file.write(response.content.decode("utf-8"))
