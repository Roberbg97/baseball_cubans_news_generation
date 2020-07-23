from sklearn.externals import joblib
import json
import numpy as np
#from data_structure import *
from notice_generator import Player, Play
from notice_generator.stats_player import Highlights_Player
#from stats_player import Highlights_Player

def get_outstandings():

    with open('game_day_data_1.json', 'r') as json_data:
        players_details = json.load(json_data)
        json_data.close()

    model = joblib.load('../classifier_lr_1.sav')

    data = {}
    for player in players_details['hitters']:
        data[player] = {}
        x = players_details['hitters'][player]['wpa_bat']
        y = players_details['hitters'][player]['leverage_index_avg']
        z = players_details['hitters'][player]['re24_bat']
        data[player]['stats'] = [float(x), float(y), float(z)]

    for player in players_details['pitchers']:
        data[player] = {}
        x = players_details['pitchers'][player]['wpa_def']
        y = players_details['pitchers'][player]['leverage_index_avg']
        z = players_details['pitchers'][player]['re24_def']
        data[player]['stats'] = [float(x), float(y), float(z)]

    coefs = model.coef_
    for player in data:
        stats = data[player]['stats']
        stats_for_pred = np.array(stats)
        stats_for_pred = stats_for_pred.reshape(1, -1)
        outstanding = model.predict(stats_for_pred)
        data[player]['outstanding'] = outstanding[0]
        data[player]['coef'] = stats[0]*coefs[0][0] + stats[1]*coefs[0][1] + stats[2]*coefs[0][2]

    return data

def sort_for_outstandings(data):
    sorted_players = []
    for player in data:
        coef = data[player]['coef']
        outstanding = data[player]['outstanding']
        sorted_players.append( (coef, player, outstanding) )

    sorted_players.sort()
    sorted_players.reverse()

    return sorted_players

def get_title(player_details, outstandings):
    title = ''

    list_of_h = []

    stats_pitchers = {
        'SC': 0,
        'W': 0,
        'SV': 0,
        'R': 0,
        'K': 0,
        'NHNR': 0
    }

    stats_hitters = {
        'PG': 0,
        'HR': 0,
        'RBI': 0,
        'R': 0,
        'H': 0,
        'EB': 0
    }

    for player in outstandings:
        if player in player_details['pitchers']:
            h = Highlights_Player(player, player_details['pitchers'][player])
            d = h.get_dict_of_texts()
            if 'NHNR' in d:
                list_of_h.append(d[ 'NHNR' ][ stats_pitchers[ 'NHNR' ] ])
                stats_pitchers[ 'NHNR' ] += 1
            elif 'W' in d:
                list_of_h.append(d[ 'W' ][ stats_pitchers[ 'W' ] ])
                stats_pitchers[ 'W' ] += 1
            elif 'SV' in d:
                list_of_h.append(d[ 'SV' ][ stats_pitchers[ 'SV' ] ])
                stats_pitchers[ 'SV' ] += 1
            elif 'SC' in d:
                list_of_h.append(d[ 'SC' ][ stats_pitchers[ 'SC' ] ])
                stats_pitchers[ 'SC' ] += 1
            elif 'R' in d:
                list_of_h.append(d[ 'R' ][ stats_pitchers[ 'R' ] ])
                stats_pitchers[ 'R' ] += 1
            elif 'K' in d:
                list_of_h.append(d[ 'K' ][ stats_pitchers[ 'K' ] ])
                stats_pitchers[ 'K' ] += 1
        else:
            h = Highlights_Player(player, player_details['hitters'][player])
            d = h.get_dict_of_texts()
            if 'PG' in d:
                list_of_h.append(d[ 'PG' ][ stats_hitters[ 'PG' ] ])
                stats_hitterd[ 'PG' ] += 1
            elif 'HR' in d:
                list_of_h.append(d[ 'HR' ][ stats_hitters[ 'HR' ] ])
                stats_hitters[ 'HR' ] += 1
            elif 'EB' in d:
                list_of_h.append(d[ 'EB' ][ stats_hitters[ 'EB' ] ])
                stats_hitters[ 'EB' ] += 1
            elif 'RBI' in d:
                list_of_h.append(d[ 'RBI' ][ stats_hitters[ 'RBI' ] ])
                stats_hitters[ 'RBI' ] += 1
            elif 'R' in d:
                list_of_h.append(d[ 'R' ][ stats_hitters[ 'R' ] ])
                stats_hitters[ 'R' ] += 1
            elif 'H' in d:
                list_of_h.append(d[ 'H' ][ stats_hitters[ 'H' ] ])
                stats_hitters[ 'H' ] += 1

    for t in list_of_h:
        title += t + '. '

    title += ' Resumen de cubanos MLB.'

    return title

def get_new(player_details, sorted_for_outstandings):

    new = ''

    minors = ''

    outstandings = []

    for coef, player, o in sorted_for_outstandings:
        if player in player_details['pitchers']:
            p = Player(player, player_details['pitchers'][player])
        else:
            p = Player(player, player_details['hitters'][player])
        if o == 1:
            outstandings.append(player)
            report = p.get_report()
            print(report)
            print()
            new += report + '\n\n'
        else:
            minors += p.get_minority_report()

    title = get_title(player_details, outstandings)

    print(minors)
    new += minors

    print()

    print(title)

    return (title, new)

def flow(players_details, sorted_for_outstandings):
    #outstandings_data = get_outstandings()
    #sorted_for_outstandings = sort_for_outstandings(outstandings_data)

    #print(sorted_oustandings_players)

    with open('game_day_data_1.json', 'r') as json_data:
        players_details = json.load(json_data)
        json_data.close()

    title, new = get_new(players_details, sorted_for_outstandings)

    return (title, new)

#flow()