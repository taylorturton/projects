# Import necessary libraries for making API requests and data visualization
import requests
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Define the API endpoint URL and query parameters
url = "https://free-nba.p.rapidapi.com/stats"
querystring = {"page": "0", "per_page": "25"}

# Define API request headers, including API key and host information
headers = {
    "X-RapidAPI-Key": "d26b153c50mshae9ed05ad727befp1bfbbejsnae454649e1fd",
    "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
}

# Make an HTTP GET request to the API endpoint with headers and query parameters
response = requests.get(url, headers=headers, params=querystring)

# Check if the API request was successful (HTTP status code 200) and parse the response data
if response.status_code == 200:
    data = response.json()

    # Extract player names and points
    players = []
    points = []

    # Create a set to track players and avoid duplicates
    seen_players = set()

    # Iterate through NBA player data and extract player names and points
    for item in data["data"]:
        player = item["player"]["first_name"] + " " + item["player"]["last_name"]
        player_points = item["pts"]

        players.append(player)
        points.append(player_points)
        seen_players.add(player)

    # Sort players by points in descending order, handling None values
    sorted_players = [x for _, x in sorted(zip(points, players), key=lambda item: (item[0] is None, item[0]), reverse=True)]
    sorted_points = sorted(points, key=lambda x: x if x is not None else 0, reverse=True)

    # Select the top 20 players
    top_players = sorted_players[:20]
    top_points = sorted_points[:20]

   # Create a custom colormap with orange for higher values and black for lower values
    cmap = LinearSegmentedColormap.from_list("Custom", [(0, "black"), (0.5, "orange"), (1, "orange")])

    # Replace None values in top_points with a value lower than 0
    top_points = [0 if point is None else point for point in top_points]

    # Normalize the values in top_points to the range [0, 1]
    normalized_points = [(point - min(top_points)) / (max(top_points) - min(top_points)) for point in top_points]

    # Create colors based on the normalized values using the colormap
    colors = cmap(normalized_points)

# Create a Matplotlib bar chart
plt.figure(figsize=(10, 6))
plt.bar(top_players, top_points, color=colors, width=0.7)
plt.xlabel("Player")
plt.ylabel("Points")
plt.title("Top 20 NBA Points Scorers")
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()
