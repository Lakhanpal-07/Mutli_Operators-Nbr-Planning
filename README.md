# Mutli_Operators-Nbr-Planning
This repo finds the nearest Operator-A site for each Operator-B site using geographic coordinates, calculates accurate geodesic distances, and exports the matched results to Excel. It also creates a KML file for map visualization, with colored connection lines based on distance ranges, making network planning and site analysis easier.

Step-by-step working
1.	Import libraries
•	pandas is used to read and write Excel data.
•	geopy.distance.geodesic calculates the real-world distance between two latitude/longitude points.
•	scipy.spatial.KDTree helps quickly find the nearest site.
•	simplekml creates the KML map file.
2.	Load the Excel file
•	The script reads prompt base.xlsx into a DataFrame named df.
•	This file contains Operator A and Operator B site coordinates.
3.	Extract Operator A and Operator B site data
•	Operator A columns are selected into operator_a_sites.
•	Operator B columns are selected into operator_b_sites.
•	dropna() removes rows with missing coordinate values.
4.	Build the KDTree
•	Operator B latitude and longitude values are converted into a coordinate array.
•	A KDTree is built from the Operator B coordinates.
•	This makes nearest-site searching faster.
5.	Loop through each Operator A site
•	For every Operator A site, the script takes its latitude and longitude.
•	It queries the KDTree to find the closest Operator B site by coordinate proximity.
6.	Calculate exact distance
•	The nearest Operator B site found by KDTree is not enough by itself.
•	The script uses geodesic() to calculate the accurate distance on the earth’s surface.
•	The distance is stored in kilometers.
7.	Save results
•	The script stores:
•	Operator A site ID
•	Operator A coordinates
•	nearest Operator B site ID
•	Operator B coordinates
•	distance in km
•	All results are converted into a new DataFrame.
•	This DataFrame is exported to Operator_A_Operator_B_Nearest.xlsx.
8.	Create KML file
•	A KML object is created for map visualization.
•	For each matched pair:
•	one point is added for Operator A
•	one point is added for Operator B
•	a line is drawn between them
9.	Apply line colors
•	If distance is less than 100 km, the line is green.
•	If distance is between 100 and 250 km, the line is orange.
•	If distance is more than 250 km, the line is red.
10.	Save KML output
•	The final map file is saved as Operator_A_Operator_B_Nearest.kml.
•	This can be opened in tools like Google Earth for visualization.
Simple summary
The script compares each Operator A site with all Operator B sites, finds the closest match, calculates the exact distance, then exports the matches into an Excel sheet and a KML map file.