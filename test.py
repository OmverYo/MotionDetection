import api
import pathlib

# api.gamedata_api("/BackgroundData", "DELETE")

# result = result.replace("\"", "").replace("{", "").replace("}", "").replace(":", " ").replace(",", " ").split(" ")

# print(result)

# variable = [1, 2, 3, 4, 5, 6]

# api.gamedata_api("/PlayerData", "POST", variable)

# variable = [1, 2, 3, 4]

# api.gamedata_api("/HandData", "UPDATE", variable)

variable = [1, 2, 3, 4]

# result = api.gamedata_api("/BackgroundData", "GET", variable)

# print(result)

result = api.gamedata_api("/HandData", "GET", variable)

print(result)