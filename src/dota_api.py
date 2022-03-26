#Библиотека для API Dota 2
#By @a352642 (telegram)

import os
try:
    import requests
    import json
    import datetime
except:
    print("Installing module 'requests'")
    os.system("pip3 install requests -q")

class Client:
    def __init__(self):
        self.api = "https://api.opendota.com/api/" #URL API Opendota
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
        }


    def get_player_info(self, id: str, file: str = None): #Функция для получения информации об игроке
        response = requests.get(self.api+"players/"+id, headers=self.headers).text #Посылаем GET запрос
        try:
            response = json.loads(response) #Пробуем перевести ответ запроса в JSON
        except:
            return {"error": True, "message": f"Unable to parse player data received by specifying the following player ID: {id}"} #При ошибке выходим из функции

        try: #Пробуем получить нужные нам данные
            data = {
                "error": False, 
                "nickname": response["profile"]["personaname"], #Никнейм игрока
                "dotaplus_acquired": response["profile"]["plus"], #Подписка на Dota Plus
                "steam_id": response["profile"]["steamid"], #ID в Steam
                "steam_url": response["profile"]["profileurl"], #Ссылка на профиль в Steam
                "avatar": response["profile"]["avatarfull"], #Ссылка на аватар игрока
                "country": response["profile"]["loccountrycode"], #Код страны
                "original_json": self.api+"players/"+id #Оригинальный JSON ответ
            }
        except Exception as e: #Если не удается получить эти данные то выходим из функции
            return {"error": True, "message": f"The player with ID {id} does not exist or has restricted access to his data"}
        
        response2 = requests.get(self.api+"players/"+id+"/wl", headers=self.headers).text #Второй GET запрос (для побед/поражений)
        try: #Пробуем получить нужные нам данные
            response2 = json.loads(response2) #Пробуем перевести ответ запроса в JSON
        except:
            pass #При ошибке ничего не делаем, не критично
        else:
            data["wins"] = response2["win"] #Кол-во побед игрока
            data["loses"] = response2["lose"] #Кол-во поражений игрока
        
        if file: #Если пользователь указал файл для записи
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps(data)) #Записываем туда информацию
            print("Data saved in", file)
        
        return data #Возвращаем словарь с данными
    

    def recent_matches(self, id: str, file: str = None): #Функция для получения информации о недавних играх пользователя
        response = requests.get(self.api+"players/"+id+"/recentMatches", headers=self.headers).text #Посылаем GET запрос

        try:
            response = json.loads(response) #Пробуем перевести ответ запроса в JSON
        except:
            return {"error": True, "message": f"Unable to parse matches data received by specifying the following player ID: {id}"} #При ошибке выходим из функции
        
        try: #Пробуем получить нужные нам данные
            data = {
                "matches": [str(response[i]["match_id"]) for i in range(20)], #ID матчей (в кол-ве 20 штук)
                "original_json": self.api+"players/"+id+"/recentMatches" #Оригинальный JSON ответ
            }
        except Exception as e: #Если не удается получить эти данные то выходим из функции
            return {"error": True, "message": f"The player with ID {id} does not exist or has restricted access to his data"}
        
        if file: #Если пользователь указал файл для записи
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps(data)) #Записываем туда информацию
            print("Data saved in", file)
        
        return data #Возвращаем словарь с данными


    def match_info(self, id: str, file: str = None): #Получаем информацию о матче
        response = requests.get(self.api+"matches/"+id, headers=self.headers).text #Посылаем GET запрос

        try:
            response = json.loads(response) #Пробуем перевести ответ запроса в JSON
        except:
            return {"error": True, "message": f"Unable to parse match data received by specifying the following match ID: {id}"} #При ошибке выходим из функции
        try: #Пробуем получить нужные нам данные
            data = {
                "error": False,
                "match_id": response["match_id"], #ID матча (внезапно)
                "duration_mins": response["duration"] / 60, #Длительность в минутах
                "duration_secs": response["duration"], #Длительность в секундах
                "picks": [response["picks_bans"][i] for i in range(10)] if response["picks_bans"] != None else None, #Выбранные герои
                "bans": [response["picks_bans"][i] for i in range(10, len(response["picks_bans"]))] if response["picks_bans"] != None else None, #Забаненные герои
                "start_time": datetime.datetime.fromtimestamp(response["start_time"]).strftime('%Y-%m-%d %H:%M:%S'), #Начало матча в формате ГГ-ММ-ДД ЧЧ:ММ:СС
                "end_time": datetime.datetime.fromtimestamp(response["start_time"]+response["duration"]).strftime('%Y-%m-%d %H:%M:%S'), #Конец матча в формате ГГ-ММ-ДД ЧЧ:ММ:СС
                "winner": "radiant" if response["radiant_win"] else "dire", #Победитель (radiant - Силы Света, dire - Силы Тьмы)
                "radiant_kills": response["radiant_score"], #Убийств у Сил Света
                "dire_kills": response["dire_score"], #Убийств у Сил Тьмы
                "replay": response["replay_url"], #Ссылка на запись матча
                "original_json": self.api+"matches/"+id #Оригинальный JSON ответ
            }
        except Exception as e: #Если не удается получить эти данные то выходим из функции
            return {"error": True, "message": f"Match with ID {id} does not exist"}
        
        if file: #Если пользователь указал файл для записи
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps(data)) #Записываем туда информацию
            print("Data saved in", file)
        
        return data #Возвращаем словарь с данными


    def heroes_info(self, id: str, file: str = None): #Получить информацию о статистике игрока на героях
        response = requests.get(self.api+"players/"+id+"/heroes", headers=self.headers).text #Посылаем GET запрос

        try:
            response = json.loads(response) #Пробуем перевести ответ запроса в JSON
        except:
            return {"error": True, "message": f"Unable to parse data received by specifying the following ID: {id}"} #При ошибке выходим из функции
        data = {"error": False}
        try: #Пробуем получить нужные нам данные
            for i in range(123):
                data[str(i)] = response[i] #Номер
                data[str(i)]["last_played"] = datetime.datetime.fromtimestamp(data[str(i)]["last_played"]).strftime('%Y-%m-%d %H:%M:%S') #Время последнего матча на герое
                data[str(i)]["hero_id"] = self.get_hero_by_id(int(data[str(i)]["hero_id"])) #Герой
        except Exception as e: #Если не удается получить эти данные то выходим из функции
            return {"error": True, "message": f"Match with ID {id} does not exist"}
        
        if file: #Если пользователь указал файл для записи
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps(data)) #Записываем туда информацию
            print("Data saved in", file)
        
        return data #Возвращаем словарь с данными


    def get_hero_by_id(self, id: int): #Узнать героя по его ID
        a = ["", "antimage", "axe", "bane", "bloodseeker", "crystal_maiden", "drow_ranger", "earthshaker", "juggernaut", "mirana", "morphling", "shadow_fiend", "phantom_lancer", "puck", "pudge", "razor", "sand king", "storm_spirit", "sven", "tiny", "vengeful spirit", "windranger", "zeus", "kunkka", "", "lina", "lion", "shadow shaman", "slardar", "tidehunter", "witch doctor", "lich", "riki", "enigma", "tinker", "sniper", "necrophos", "warlock", "beastmaster", "queen_of_pain", "venomancer", "faceless_void", "wraith_king", "death_prophet", "phantom_assassin", "pugna", "templar_assassin", "viper", "luna", "dragon_knight", "dazzle", "clockwerk", "leshrac", "nature's prophet", "lifestealer", "dark_seer", "clinkz", "omniknight", "enchantress", "huskar", "night_stalker", "broodmother", "bounty_hunter", "weaver", "jakiro", "batrider", "chen", "spectre", "ancient_apparition", "doom", "ursa", "spirit_breaker", "gyrocopter", "alchemist", "invoker", "silencer", "outworld_destroyer", "lycan", "brewmaster", "shadow_demon", "lone_druid", "chaos_knight", "meepo", "treant_protector", "ogre_magi", "undying", "rubick", "disruptor", "nyx_assassin", "naga_siren", "keeper_of_the_light", "io", "visage", "slark", "medusa", "troll_warlord", "centaur_warrunner", "magnus", "timbersaw", "bristleback", "tusk", "skywrath_mage", "abaddon", "elder_titan", "legion_commander", "techies", "ember_spirit", "earth_spirit", "underlord", "terrorblade", "phoenix", "oracle", "winter_wyvern", "arc_warden", "monkey_king", "", "", "", "", "dark_willow", "pangolier", "grimstroke", "", "hoodwink", "", "", "void_spirit", "", "snapfire", "mars", "", "", "", "", "", "dawnbreaker", "", "primal_beast"]
        return a[id] #Возвращаем героя