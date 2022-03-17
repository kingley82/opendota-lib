import dota_api

dota = dota_api.Client()

match = dota.match_info('match_id')

radiants = []
dires = []

if match["error"] == False and match["picks"] != None:
    for i in range(10):
        pick = match["picks"][i]
        hero = dota.get_hero_by_id(pick["hero_id"])
        if pick["team"] == 0:
            radiants.append(hero)
        else:
            dires.append(hero)
    print(f"Heroes in match {match['match_id']}")
    print("RADIANT:\n", "\n".join(radiants))
    print()
    print("DIRE:\n", "\n".join(dires))