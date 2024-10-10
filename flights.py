import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Step 1: Authenticate and connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Provide the path to your downloaded JSON key file here
creds = ServiceAccountCredentials.from_json_keyfile_name('glass-arcade-438218-n3-8ff5c184e029.json', scope)

# Authorize the client to interact with Google Sheets
client = gspread.authorize(creds)

# Open your Google Sheet by name
# Make sure you replace "Your Google Sheet Name" with the actual name of your Google Sheet
sheet = client.open("2024 Flights").sheet1

# Step 2: Get all the data from the sheet
# Ensure your Google Sheet has columns like 'Flight Number', 'Departure Airport', 'Arrival Airport', etc.
data = sheet.get_all_records()

# Convert the data into a pandas DataFrame for easier manipulation
df = pd.DataFrame(data)

# Step 3: Geocoding airports to latitude and longitude
# Initialize the geolocator to convert airport codes to lat/long
geolocator = Nominatim(user_agent="flight_visualization")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Find unique airports from the departure and arrival columns
airports = pd.Series(df['Departure Airport'].tolist() + df['Arrival Airport'].tolist()).unique()

# Create a dictionary to store latitude and longitude for each airport
airport_locations = {}

# Geocode each unique airport
for airport in airports:
    location = geocode(airport)
    if location:
        airport_locations[airport] = (location.latitude, location.longitude)

# Step 4: Visualize the flights on a map
# Get a base map of the world using geopandas
# Replace 'path_to_your_shapefile' with the actual path to the downloaded shapefile
world = gpd.read_file('ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')


# Create a figure for the map
fig, ax = plt.subplots(figsize=(10, 7))

# Plot the base world map
world.plot(ax=ax, color='lightblue', edgecolor='black')

# Plot the flight paths from the DataFrame
for _, row in df.iterrows():
    dep_airport = row["Departure Airport"]
    arr_airport = row["Arrival Airport"]
    
    # Make sure both the departure and arrival airports have been geocoded
    if dep_airport in airport_locations and arr_airport in airport_locations:
        dep_location = airport_locations[dep_airport]
        arr_location = airport_locations[arr_airport]
        
        # Plot a line between the two airports (as a flight path)
        ax.plot([dep_location[1], arr_location[1]], [dep_location[0], arr_location[0]], 
                color='red', linestyle='-', linewidth=2, marker='o')

# Add labels to the airports on the map
for airport, (lat, lon) in airport_locations.items():
    ax.text(lon, lat, airport, fontsize=10, ha='right', color='blue')

# Add title and labels
ax.set_title('Flight Paths from Google Sheets Data', fontsize=14)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Show the map
plt.show()
