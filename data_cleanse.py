import pandas as pd

data = pd.read_csv("./airports.csv")

data.drop(columns=["home_link", "wikipedia_link", "local_code", "id"], inplace=True)

data.to_csv("./updated_airports.csv", index=False)