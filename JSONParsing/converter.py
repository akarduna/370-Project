import csv
import json
from unicodedata import name
import locale
from locale import atof
 
 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath, heartRatePath):
     
    # create a dictionary
    data = {}
    events = []
    names = []
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        with open(heartRatePath, encoding='utf-8') as heartrate:
            hr = list(csv.reader(heartrate))
        
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            if rows['event'] == 'bluename' or rows['event'] == 'redname':
                names.append(list(rows.values()))
            elif rows['event'] == 'focus':
                data['player'] = list(rows.values())
            elif rows['event'] != 'timestamp':
                row = list(rows.values())
                if row[4] != "null":
                    print(int(atof(row[4])))
                    row.append(hr[int(atof(row[4]))][0])
                events.append(row)
    data['events'] = events
    data['names'] = names
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
            # Assuming a column named 'No' to
# Driver Code
 
# Decide the two file paths according to your
# computer system
def run():
    csvFilePath = r'gamedata.csv'
    jsonFilePath = r'gamedata.json'
    heartRatePath = r'Heartrate.csv'
    # Call the make_json function
    make_json(csvFilePath, jsonFilePath, heartRatePath)
