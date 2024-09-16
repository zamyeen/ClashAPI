import requests
import json
import os
import csv

headers = {
    'Accept' : 'application/json', 
    'authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImZiY2I1M2NlLTQ0YzYtNDJmNS1hNGU2LTM2YmYwYTE1YWM4NCIsImlhdCI6MTcyMjcyMzkyOCwic3ViIjoiZGV2ZWxvcGVyLzgxZjk1MDE4LWNjZDgtY2ViYi05YWVjLTZkNTA4MjhlYTk3MyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjY3LjE2MC4xMzcuMTU3Il0sInR5cGUiOiJjbGllbnQifV19.qA-2oS70YLfAhG3_vdyih73sliArrZR2fFM1bmIkDQvaP_L_kf-NZxEvP0C3lsEyc1tu_9gITa5IrrPkqLcNIA'
}

class ClanMember:
    def __init__(self, tag, name, role, town_hall_level, exp_level, trophies, donations, donations_received, heroes):
        self.tag = tag                   # Unique identifier for the clan member
        self.name = name                 # Name of the clan member
        self.role = role                 # Role of the clan member (e.g., leader, co-leader, member)
        self.townhall_level = townhall_level  # Town Hall level of the clan member
        self.exp_level = exp_level       # Experience level of the clan member
        self.heroes = heroes  # List of tuples for each hero

    def display_info(self):
        """Displays basic information about the clan member."""
        print(f'Tag: {self.tag}')
        print(f'Name: {self.name}')
        print(f'Role: {self.role}')
        print(f'Town Hall Level: {self.townhall_level}')
        print(f'Experience Level: {self.exp_level}')
    
    def __repr__(self):
        return (f"ClanMember(tag={self.tag}, name={self.name}, role={self.role}, "
                f"town_hall_level={self.town_hall_level}, exp_level={self.exp_level}, "
                f"trophies={self.trophies}, donations={self.donations}, "
                f"donations_received={self.donations_received}, heroes={self.heroes})")

    @staticmethod
    def from_json(data):
        heroes = []
        for hero in data.get("heroes", []):
            # Fetch equipment details
            equipment_list = hero.get("equipment", [])
            equipment_1 = Equipment(
                equipment_list[0]['name'], equipment_list[0]['level'], equipment_list[0]['maxLevel']
            ) if len(equipment_list) > 0 else None
            equipment_2 = Equipment(
                equipment_list[1]['name'], equipment_list[1]['level'], equipment_list[1]['maxLevel']
            ) if len(equipment_list) > 1 else None

            hero_tuple = (
                hero["name"],
                hero["level"],
                hero["maxLevel"],
                equipment_1,
                equipment_2
            )
            heroes.append(hero_tuple)

        return ClanMember(
            tag=data["tag"],
            name=data["name"],
            role=data["role"],
            town_hall_level=data["townHallLevel"],
            exp_level=data["expLevel"],
            trophies=data["trophies"],
            donations=data["donations"],
            donations_received=data["donationsReceived"],
            heroes=heroes
        )

class Equipment:
    def __init__(self, name, level, max_level):
        self.name = name
        self.level = level
        self.max_level = max_level

    def __repr__(self):
        return f"Equipment(name={self.name}, level={self.level}, max_level={self.max_level})"


def update_json():
    url = f'https://api.clashofclans.com/v1/clans/%238289P9VC/members'
    response = requests.get(url, headers=headers)
    clan_json = response.json()

    directory_name='WarHawksClanInfo'

    filename = 'clan_info.json'
    file_path = os.path.join(directory_name, filename)

    os.makedirs(directory_name, exist_ok=True)

    with open(file_path, 'w') as json_file:
        json.dump(clan_json, json_file, indent=4)
    # print(clan_json)

def get_json():
    url = f'https://api.clashofclans.com/v1/clans/%238289P9VC/members'
    response = requests.get(url, headers=headers)
    clan_json = response.json()
    return clan_json

def get_clan_members(json_data):
    """
    Parses the JSON data to extract clan members and stores them in a list of ClanMember objects.
    
    :param json_data: The JSON data containing information about the clan.
    :return: A list of ClanMember objects.
    """
    # Extract the list of members from the JSON data
    member_list = json_data.get("items", [])
    
    # Create a list to store ClanMember objects
    clan_members = []
    
    # Iterate over each member in the member list
    for member in member_list:
        # Extract relevant information for each clan member
        tag = member.get("tag")
        name = member.get("name")
        role = member.get("role")
        townhall_level = member.get("townHallLevel")
        exp_level = member.get("expLevel")
        
        # Create a ClanMember object and add it to the clan_members list
        clan_member = ClanMember(tag, name, role, townhall_level, exp_level)
        clan_members.append(clan_member)
    
    return clan_members

update_json()
# print(get_json())
members = get_clan_members(get_json())

for member in members:
    member.display_info()