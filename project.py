import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# API request to get NBA player stats
url = "https://free-nba.p.rapidapi.com/stats"
querystring = {"page": "0", "per_page": "25"}

headers = {
    "X-RapidAPI-Key": "d26b153c50mshae9ed05ad727befp1bfbbejsnae454649e1fd",
    "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
    data = response.json()

    # Extract player names and points
    players = []
    points = []

    # Create a set to track players and avoid duplicates
    seen_players = set()

    for item in data["data"]:
        player = item["player"]["first_name"] + " " + item["player"]["last_name"]
        player_points = item["pts"]
        
        # Filter out data with missing points and avoid duplicates
        if player_points is not None and player not in seen_players:
            players.append(player)
            points.append(player_points)
            seen_players.add(player)

    # Sort players by points in descending order
    sorted_players = [x for _, x in sorted(zip(points, players), reverse=True)]
    sorted_points = sorted(points, reverse=True)

    # Select the top 20 players
    top_players = sorted_players[:20]
    top_points = sorted_points[:20]

    # Create a custom colormap with orange for higher values and black for lower values
    cmap = LinearSegmentedColormap.from_list("Custom", [(0, "black"), (0.5, "orange"), (1, "orange")])
    colors = cmap(np.interp(top_points, (min(top_points), max(top_points)), (0, 1)))

    # Create a Matplotlib bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(top_players, top_points, color=colors, width=0.7)
    plt.xlabel("Player")
    plt.ylabel("Points")
    plt.title("Top 20 NBA Points Scorers")
    plt.xticks(rotation=45, ha='right')

    # Annotate the bars with the point numbers inside the bars in white
    for i, v in enumerate(top_points):
        plt.text(i, v, str(v), color='white', va='bottom', ha='center')

    plt.tight_layout()
    plt.show()
else:
    print("Failed to fetch NBA stats.")
