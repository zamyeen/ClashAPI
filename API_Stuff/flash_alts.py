import requests
import json
import os
import csv

headers = {
    'Accept' : 'application/json', 
    'authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImZiY2I1M2NlLTQ0YzYtNDJmNS1hNGU2LTM2YmYwYTE1YWM4NCIsImlhdCI6MTcyMjcyMzkyOCwic3ViIjoiZGV2ZWxvcGVyLzgxZjk1MDE4LWNjZDgtY2ViYi05YWVjLTZkNTA4MjhlYTk3MyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjY3LjE2MC4xMzcuMTU3Il0sInR5cGUiOiJjbGllbnQifV19.qA-2oS70YLfAhG3_vdyih73sliArrZR2fFM1bmIkDQvaP_L_kf-NZxEvP0C3lsEyc1tu_9gITa5IrrPkqLcNIA'
}

def get_user(tag, filename):
    # Replace the first character '#' with '%23' for URL encoding
    encoded_tag = f'%23{tag}'
    
    # Construct the URL with the given tag
    url = f'https://api.clashofclans.com/v1/players/{encoded_tag}'
    
    # Make the API request with headers (assuming headers are defined somewhere)
    response = requests.get(url, headers=headers)
    
    # Parse the JSON response
    user_json = response.json()
    
    # Print the user profile information
    #print(user_json)

    os.makedirs('rawJSONs', exist_ok=True)

    filepath = os.path.join('rawJSONs', f'{filename}.json')

    with open(filepath, 'w') as file:
        json.dump(user_json, file, indent=4)

def get_equip(accountName):
    # Define paths for input and output
    input_filepath = os.path.join('rawJSONs', f'{accountName}.json')
    output_filepath = os.path.join('EquipLevels', f'{accountName}.txt')
    
    # Ensure the EquipLevels directory exists
    os.makedirs('EquipLevels', exist_ok=True)
    
    try:
        # Read the JSON data from the file
        with open(input_filepath, 'r') as infile:
            data = json.load(infile)
        
        # Extract equipment levels from the JSON data
        equipment_data = []
        if "heroes" in data:
            for hero in data["heroes"]:
                if "equipment" in hero:
                    for equipment in hero["equipment"]:
                        equipment_data.append(f"{hero['name']} - {equipment['name']}: Level {equipment['level']}/{equipment['maxLevel']}\n")
        
        # Write the extracted equipment levels to the output file
        with open(output_filepath, 'w') as outfile:
            outfile.writelines(equipment_data)
        
        print(f"Equipment levels for {accountName} have been written to {output_filepath}.")
    
    except FileNotFoundError:
        print(f"File not found: {input_filepath}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {input_filepath}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_all_equip(accountName):
    # Define paths for input and output
    input_filepath = os.path.join('rawJSONs', f'{accountName}.json')
    output_filepath = os.path.join('AllEquipLevels', f'{accountName}.txt')
    
    # Ensure the EquipLevels directory exists
    os.makedirs('AllEquipLevels', exist_ok=True)
    
    try:
        # Read the JSON data from the file
        with open(input_filepath, 'r') as infile:
            data = json.load(infile)
        
        # Extract equipment levels from the "heroEquipment" section of the JSON data
        equipment_data = []
        if "heroEquipment" in data:
            for equipment in data["heroEquipment"]:
                equipment_data.append(f"{equipment['name']}: Level {equipment['level']}/{equipment['maxLevel']}\n")
        
        # Write the extracted equipment levels to the output file
        with open(output_filepath, 'w') as outfile:
            outfile.writelines(equipment_data)
        
        print(f"Equipment levels for {accountName} have been written to {output_filepath}.")
    
    except FileNotFoundError:
        print(f"File not found: {input_filepath}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {input_filepath}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_all_equips_csv(accountNames):
    # Ensure the OutputCSV directory exists
    os.makedirs('OutputCSV', exist_ok=True)
    
    # Define the output CSV file path
    output_filepath = os.path.join('OutputCSV', 'equipment_levels.csv')
    
    # Open the CSV file for writing
    with open(output_filepath, 'w', newline='') as csvfile:
        # Define the CSV writer
        csvwriter = csv.writer(csvfile)
        
        # Write the header row
        csvwriter.writerow(['Account Name', 'Equipment', 'Level', 'Max Level'])
        
        # Iterate through each account name
        for accountName in accountNames:
            # Define the input file path
            input_filepath = os.path.join('AllEquipLevels', f'{accountName}.txt')
            
            try:
                # Open the input file for reading
                with open(input_filepath, 'r') as infile:
                    # Read each line of the equipment data
                    for line in infile:
                        # Split the line into equipment name and level
                        if "Level" in line:
                            # Example line format: "Giant Gauntlet: Level 9/27"
                            equipment, level_info = line.split(': Level ')
                            current_level, max_level = level_info.strip().split('/')
                            
                            # Write the row to the CSV file
                            csvwriter.writerow([accountName, equipment.strip(), current_level, max_level])
            
            except FileNotFoundError:
                print(f"File not found: {input_filepath}")
            except Exception as e:
                print(f"An error occurred while processing {accountName}: {str(e)}")
    
    print(f"Equipment levels for all accounts have been written to {output_filepath}.")


#XS: L009882P2
#Zoom: 92J8UQY02
#Impulse: 2380QPJ8L8V
#XLR8: YJGPPUVR
# print("Getting Users/Jsons")
# get_user("L009882P2","XS")
# get_user("92J8UQY02","ZOOM")
# get_user("80QPJ8L8V","Impulse")
# get_user("YJGPPUVR","XLR8")

print("Getting Equipment")
get_equip("XS")
get_equip("Zoom")
get_equip("Impulse")
get_equip("XLR8")

# print("Getting All Equipment")
# get_all_equip("XS")
# get_all_equip("Zoom")
# get_all_equip("Impulse")
# get_all_equip("XLR8")

# print("Getting Equipment Levels Combined")
# # Example usage:
# account_names = ["XS", "Zoom", "Impulse", "XLR8"]
# get_all_equips_csv(account_names)