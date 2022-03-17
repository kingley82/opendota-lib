#Библиотека для API Dota 2
#By @a352642 (telegram)

import os
try:
    import requests
    import json
    import datetime
except:
    os.system("pip3 install requests -q")

class Client:
    def __init__(self):
        self.api = "https://api.opendota.com/api/"
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
        }


    def get_player_info(self, id: str, file: str = None):
        response = requests.get(self.api+"players/"+id, headers=self.headers).text
        try:
            response = json.loads(response)
        except:
            return {"error": True, "message": f"Unable to parse data received by specifying the following ID: {id}"}

        try:
            data = {
                "error": False,
                "nickname": response["profile"]["personaname"],
                "dotaplus_acquired": response["profile"]["plus"],
                "steam_id": response["profile"]["steamid"],
                "steam_url": response["profile"]["profileurl"],
                "avatar": response["profile"]["avatarfull"],
                "country": response["profile"]["loccountrycode"],
                "original_json": self.api+"players/"+id
            }
        except Exception as e:
            return {"error": True, "message": f"The player with ID {id} does not exist or has restricted access to his data"}
        
        response2 = requests.get(self.api+"players/"+id+"/wl", headers=self.headers).text
        try:
            response2 = json.loads(response2)
        except:
            pass
        else:
            data["wins"] = response2["win"]
            data["loses"] = response2["lose"]
        
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps(data))
            print("Data saved in", file)
        
        return data
    

    def recent_matches(self, id: str, file: str = None):
        response = requests.get(self.api+"players/"+id+"/recentMatches", headers=self.headers).text

        try:
            response = json.loads(response)
        except:
            return {"error": True, "message": f"Unable to parse data received by specifying the following ID: {id}"}
        
        try:
            data = {
                "matches": [str(response[i]["match_id"]) for i in range(20)],
                "original_json": self.api+"players/"+id+"/recentMatches"
            }
        except Exception as e:
            return {"error": True, "message": f"The player with ID {id} does not exist or has restricted access to his data"}
        
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps(data))
            print("Data saved in", file)
        
        return data


    def match_info(self, id: str, file: str = None):
        response = requests.get(self.api+"matches/"+id, headers=self.headers).text

        try:
            response = json.loads(response)
        except:
            return {"error": True, "message": f"Unable to parse data received by specifying the following ID: {id}"}
        try:
            data = {
                "error": False,
                "match_id": response["match_id"],
                "duration": response["duration"] / 60,
                "picks": [response["picks_bans"][i] for i in range(10)] if response["picks_bans"] != None else None,
                "bans": [response["picks_bans"][i] for i in range(10, len(response["picks_bans"]))] if response["picks_bans"] != None else None,
                "start_time": datetime.datetime.fromtimestamp(response["start_time"]).strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": datetime.datetime.fromtimestamp(response["start_time"]+response["duration"]).strftime('%Y-%m-%d %H:%M:%S'),
                "winner": "radiant" if response["radiant_win"] else "dire",
                "radiant_kills": response["radiant_score"],
                "dire_kills": response["dire_score"],
                "replay": response["replay_url"],
                "original_json": self.api+"matches/"+id
            }
        except Exception as e:
            return {"error": True, "message": f"Match with ID {id} does not exist"}
        
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps(data))
            print("Data saved in", file)
        
        return data


    def heroes_info(self, id: str, file: str = None):
        response = requests.get(self.api+"players/"+id+"/heroes", headers=self.headers).text

        try:
            response = json.loads(response)
        except:
            return {"error": True, "message": f"Unable to parse data received by specifying the following ID: {id}"}
        data = {"error": False}
        for i in range(123):
            data[str(i)] = response[i]
            data[str(i)]["last_played"] = datetime.datetime.fromtimestamp(data[str(i)]["last_played"]).strftime('%Y-%m-%d %H:%M:%S')
            data[str(i)]["hero_id"] = self.get_hero_by_id(int(data[str(i)]["hero_id"]))
        
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps(data))
            print("Data saved in", file)
        
        return data


    def get_hero_by_id(self, id: int):
        a = ["", "antimage", "axe", "bane", "bloodseeker", "crystal_maiden", "drow_ranger", "earthshaker", "juggernaut", "mirana", "morphling", "shadow_fiend", "phantom_lancer", "puck", "pudge", "razor", "sand king", "storm_spirit", "sven", "tiny", "vengeful spirit", "windranger", "zeus", "kunkka", "", "lina", "lion", "shadow shaman", "slardar", "tidehunter", "witch doctor", "lich", "riki", "enigma", "tinker", "sniper", "necrophos", "warlock", "beastmaster", "queen_of_pain", "venomancer", "faceless_void", "wraith_king", "death_prophet", "phantom_assassin", "pugna", "templar_assassin", "viper", "luna", "dragon_knight", "dazzle", "clockwerk", "leshrac", "nature's prophet", "lifestealer", "dark_seer", "clinkz", "omniknight", "enchantress", "huskar", "night_stalker", "broodmother", "bounty_hunter", "weaver", "jakiro", "batrider", "chen", "spectre", "ancient_apparition", "doom", "ursa", "spirit_breaker", "gyrocopter", "alchemist", "invoker", "silencer", "outworld_destroyer", "lycan", "brewmaster", "shadow_demon", "lone_druid", "chaos_knight", "meepo", "treant_protector", "ogre_magi", "undying", "rubick", "disruptor", "nyx_assassin", "naga_siren", "keeper_of_the_light", "io", "visage", "slark", "medusa", "troll_warlord", "centaur_warrunner", "magnus", "timbersaw", "bristleback", "tusk", "skywrath_mage", "abaddon", "elder_titan", "legion_commander", "techies", "ember_spirit", "earth_spirit", "underlord", "terrorblade", "phoenix", "oracle", "winter_wyvern", "arc_warden", "monkey_king", "", "", "", "", "dark_willow", "pangolier", "grimstroke", "", "hoodwink", "", "", "void_spirit", "", "snapfire", "mars", "", "", "", "", "", "dawnbreaker", "", "primal_beast"]
        return a[id]