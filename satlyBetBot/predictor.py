import json

def fight_predictions(home, away, tier):
    with open("data.txt") as json_file:
        data = json.load(json_file)
    # check fighters in dict
    home_wl = 0
    away_wl = 0
    hist = data['tiers'].get(tier)
    if home in hist and away in hist:
        if away in hist.get(home)['opponents']:
            home_lose_to_away = hist.get(home)['opponents'].get(away).get('lose')
            home_win_to_away = hist.get(home)['opponents'].get(away).get('win')
            total = home_lose_to_away + home_win_to_away
            if home_win_to_away != 0:
                home_wl = (home_win_to_away/total)*100
                away_wl = 100 - home_wl
            else:
                home_wl = 0
                away_wl = 100
            return (f"Fighters have fought before, {home}: {home_wl}%, {away}: {away_wl}%")
        else:
            home_win = hist.get(home).get('win')
            home_total = hist.get(home).get('total_games')
            if home_win != 0:
                home_wl = (home_win/home_total)*100

            away_win = hist.get(away).get('win')
            away_total = hist.get(away).get('total_games')
            if away_win != 0:
                away_wl = (away_win/away_total)*100
            return (f"Fighters have not fought each other: {home}:{home_wl}% (Total games: {home_total}), {away}:{away_wl}% (Total games: {away_total})")
    elif home in hist and away not in hist:
        home_win = hist.get(home).get('win')
        home_total = hist.get(home).get('total_games')
        if home_win != 0:
            home_wl = (home_win/home_total)*100
        else:
            home_wl = 0
        return (f"{away} not in data, {home} win/lose: {home_wl}% (Total games: {home_total})")
    elif home not in hist and away in hist:
        away_win = hist.get(away).get('win')
        away_total = hist.get(away).get('total_games')
        if away_win != 0:
            away_wl = (away_win/away_total)*100
        else:
            away_wl = 0
        return (f"{home} not in data, {away} win/lose: {away_wl}% (Total games: {away_total})")
    else:
        return("No data on either fighter its 50/50")
