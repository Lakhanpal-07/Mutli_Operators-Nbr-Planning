import pandas as pd
from geopy.distance import geodesic
from scipy.spatial import KDTree
import simplekml

# Load Excel
df = pd.read_excel("prompt base.xlsx")

# Extract Airtel and Jio sites
airtel_sites = df[['Airtel_Site_ID','Airtel_Latitude','Airtel_Longitude']].dropna()
jio_sites = df[['JIO_Site_ID','Jio_Latitude','Jio_Longitude']].dropna()

# Build KDTree for Jio coordinates
jio_coords = jio_sites[['Jio_Latitude','Jio_Longitude']].values
tree = KDTree(jio_coords)

results = []

for _, airtel in airtel_sites.iterrows():
    airtel_coord = (airtel['Airtel_Latitude'], airtel['Airtel_Longitude'])
    # Query nearest Jio site
    dist, idx = tree.query([airtel['Airtel_Latitude'], airtel['Airtel_Longitude']])
    nearest_jio = jio_sites.iloc[idx]
    # Compute accurate geodesic distance
    min_dist = geodesic(airtel_coord, (nearest_jio['Jio_Latitude'], nearest_jio['Jio_Longitude'])).km

    results.append({
        "Airtel_Site_ID": airtel['Airtel_Site_ID'],
        "Airtel_Latitude": airtel['Airtel_Latitude'],
        "Airtel_Longitude": airtel['Airtel_Longitude'],
        "Nearest_Jio_Site_ID": nearest_jio['JIO_Site_ID'],
        "Jio_Latitude": nearest_jio['Jio_Latitude'],
        "Jio_Longitude": nearest_jio['Jio_Longitude'],
        "Distance_km": round(min_dist, 2)
    })

# Save Excel
output_df = pd.DataFrame(results)
output_df.to_excel("Airtel_Jio_Nearest.xlsx", index=False)

# Save KML
kml = simplekml.Kml()
for row in results:
    airtel_coord = (row["Airtel_Longitude"], row["Airtel_Latitude"])
    jio_coord = (row["Jio_Longitude"], row["Jio_Latitude"])
    kml.newpoint(name=row["Airtel_Site_ID"], coords=[airtel_coord])
    kml.newpoint(name=row["Nearest_Jio_Site_ID"], coords=[jio_coord])
    line = kml.newlinestring(name=f"{row['Airtel_Site_ID']} → {row['Nearest_Jio_Site_ID']}",
                             coords=[airtel_coord, jio_coord])
    if row["Distance_km"] < 100:
        line.style.linestyle.color = simplekml.Color.green
    elif row["Distance_km"] <= 250:
        line.style.linestyle.color = simplekml.Color.orange
    else:
        line.style.linestyle.color = simplekml.Color.red
    line.style.linestyle.width = 3

kml.save("Airtel_Jio_Nearest.kml")
