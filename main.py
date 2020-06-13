import requests
import sys
import json
import csv

ITCH_IO_BUNDLE_ENDPOINT = "https://itch.io/bundle/520/games.json"
STEAM_ALL_GAMES_ENDPOINT = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
STEAM_GAME_REVIEW_ENDPOINT = "https://store.steampowered.com/appreviews/"
all_games = requests.get(STEAM_ALL_GAMES_ENDPOINT).json().get(
    "applist").get("apps")

all_games_dict = {}
for game in all_games:
    all_games_dict[game.get("name")] = game.get("appid")

itch_io_games = requests.get(ITCH_IO_BUNDLE_ENDPOINT).json().get("games")

with open('itch_io_games.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "URL", "Platforms",
                     "Description", "Price", "Steam Review"])

    for index, game in enumerate(itch_io_games):
        game_name = game.get("title")
        steamid = all_games_dict.get(game_name)
        if steamid:
            game_review_info = requests.get(STEAM_GAME_REVIEW_ENDPOINT + str(steamid), params={
                "json": 1, "num_per_page": 0}).json().get("query_summary")
            if game_review_info:
                steam_review_score = game_review_info.get("review_score")
 
        print(index+1, game_name)
        writer.writerow([game_name, game.get("url"),
                         ', '.join(game.get("platforms") or []),
                         game.get("short_text"),
                         game.get("price"),
                         steam_review_score or ""])
