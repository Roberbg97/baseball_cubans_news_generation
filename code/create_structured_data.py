import joblib
import json
import numpy as np
import random
from configparser import ConfigParser
#from data_structure import *
from notice_generator import Player, Play
from notice_generator.stats_player import Highlights_Player
#from stats_player import Highlights_Player
from notice_generator.utils import get_yesterday_date as gyd
import os
try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

def get_outstandings(players_details):

    #players_details = json.load(open(os.path.join(MODULE,'game_day_data_1.json')))

    model = joblib.load(os.path.join(MODULE, 'classifier_lr_1.sav'))

    data = {}
    for player in players_details['hitters']:
        if len(players_details['hitters'][player]['plays']) == 0:
            continue
        data[player] = {}
        x = players_details['hitters'][player]['wpa_bat']
        y = players_details['hitters'][player]['leverage_index_avg']
        z = players_details['hitters'][player]['re24_bat']
        data[player]['stats'] = [float(x), float(y), float(z)]

    for player in players_details['pitchers']:
        if len(players_details['pitchers'][player]['plays']) == 0:
            continue
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

    #print(sorted_players)

    return sorted_players

def get_title(player_details, outstandings):

    '''
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

    title += 'Resumen de cubanos MLB.'

    return title
    '''
    parser = ConfigParser()
    parser.read(os.path.join(MODULE, 'config.ini'))

    country = parser.get('country', 'country')

    if country != 'Cuba':
        pass

    else:
        hitters = []
        pitchers = []

        prom_all = 0

        for coef, player, o in outstandings:
            prom_all += coef
            if player in player_details['hitters']:
                hitters.append((coef, player, o))
            else:
                pitchers.append((coef, player, o))

        prom_bat = 0
        prom_pit = 0

        for coef, _, _ in hitters:
            prom_bat += coef

        for coef, _, _ in pitchers:
            prom_pit += coef


        if len(hitters) > 0:
            prom_bat /= len(hitters)

        if len(pitchers) > 0:
            prom_pit /= len(pitchers)

        text = ''

        if len(outstandings) == 0:
            title = 'Sin participación cubana en jornada de las Grandes Ligas.'
            return title


        elif outstandings[0][2] == 1:
            if len(outstandings) > 1 and outstandings[1][2] == 1:
                name_1 = outstandings[0][1]
                name_2 = outstandings[1][1]

                text += name_1 + ' y ' + name_2 + ', '

                text += random.choice(
                    [
                        'los mejores jugadores ' + random.choice(['por Cuba ', 'cubanos ']),
                        'los más destacados ' + random.choice(['por Cuba ', 'por la armada cubana '])
                    ]
                )

            else:
                if outstandings[0] in hitters:
                    name = outstandings[0][1]
                    team = player_details['hitters'][name]['team']

                    hits = player_details['hitters'][name]['H']
                    hr = player_details['hitters'][name]['HR']
                    rbi = player_details['hitters'][name]['RBI']
                    r = player_details['hitters'][name]['R']

                    stats = [
                        (hits, 'Con ' + str(hits) + random.choice([' hits, ', ' imparables, '])),
                        (hr, 'Con ' + str(hr) + random.choice([' jonrones, ', ' cuadrangulares, '])),
                        (rbi, 'Con ' + str(rbi) + ' carreras implusadas, '),
                        (r, 'Con ' + str(r) + ' carreras anotadas')
                    ]

                    stats.sort()
                    stats.reverse()

                    text += stats[0][1]

                    if prom_bat > 1.25:
                        name = outstandings[0][1]

                        text += name + ' '
                        text += random.choice(
                            [
                                'lidera a ' + team,
                                'entre los mejores de ' + team
                            ]
                        ) + \
                        random.choice(
                            [
                                ' en jornada destacada para la ofensiva cubana.',
                                ' en buen día para los bateadores cubanos.'
                            ]
                        )

                        return text

                    elif prom_bat < 0.5:
                        text += name + ' '
                        text += random.choice(
                            [
                                'saca la cara por los bateadores cubanos en jornada de las Grandes Ligas.',
                                'sobresale en mal día para los bateadores cubanos.',
                                'resalta entre los bateadores cubanos en Grandes Ligas de béisbol.'
                            ]
                        )
                        return text
                    else:
                        text += name + ' '
                        text += random.choice(
                            [
                                'destaca entre los bateadores cubanos',
                                'lidera ofensiva cubana'
                            ]
                        )
                else:
                    name = outstandings[0][1]
                    team = player_details['pitchers'][name]['team']
                    team_rival = player_details['pitchers'][name]['rival_team']

                    if prom_pit > 1.25:
                        text += random.choice(
                            [
                                'Buena salida de ' + name + ' para ' + team,
                                name + ' dominante frente a ' + team_rival
                            ]
                        ) + random.choice(
                            [
                                ' en jornada destacada para el pitcheo cubano.',
                                ' en una buena jornada para el pitcheo cubano.',
                                ' en un buen día para el pitcheo cubano.'
                            ]
                        )
                        return text

                    elif prom_pit < 0.5:
                        text += name + ' '
                        text += random.choice(
                            [
                                'salva la honra por los lanzadores cubanos en la jornada de las Grandes Ligas.',
                                'sobresale en mal día para los lanzadores cubanos.',
                                'resalta entre los lanzadores cubanos en Grandes Ligas de béisbol.'
                            ]
                        )
                        return text
                    else:
                        text += name + ' '
                        text += random.choice(
                            [
                                ', dominante',
                                ' lidera la ofensiva cubana'
                            ]
                        )

        else:
            if prom_all > 1.00:
                text += random.choice(
                    [
                        'Jornada positiva para los cubanos en Grandes Ligas de béisbol.',
                        'Buena actuación de los cubanos en jornada de la MLB.',
                        'Actuaciones destacables para jugadores cubanos en las Grandes Ligas.'
                    ]
                )
                return text
            else:
                text += random.choice(
                    [
                        'Poco destaque de jugadores cubanos en las Grandes Ligas.',
                        'Jugadores cubanos con pobres resultados en jornada de la MLB.',
                        'Discreta actuación de los cubanos en las Grandes Ligas de béisbol.'
                    ]
                )
                return text

        text += random.choice(
            [
                ' en jornada de las Grandes Ligas de béisbol.',
                ' en una jornada más de la MLB',
                ' en la MLB.',
                ' en las Grandes Ligas.'
            ]
        )

    return text


def get_first_paragraph(outstandings, games_details):

    date = gyd()

    text = ''

    fo = [
        'En la jornada del ' + date + ' de las Grandes Ligas se disputaron ' + str(len(games_details) - 1) + \
        ' encuentros de béisbol.',
        'El ' + date + ' se jugaron ' + str(len(games_details) - 1) + ' encuentros en las Grandes Ligas.'
    ]

    if len(games_details) == 0:
        return 'En la jornada del ' + date + ' de las Grandes Ligas no se celebraron juegos de béisbol.\n'
    
    if len(games_details) == 1:
        text += 'En la jornada del ' + date + ' de la MLB se disputó solo un encuentro.'

    else:
        text += random.choice(fo)

    outs = []
    total = set()

    for coef, player, o in outstandings:
        player = player.replace('_1', '')
        player = player.replace('_2', '')
        if o == 1:
            outs.append(player)
        total.add(player)

    if len(outstandings) == 0:
        text += ' En esta jornada no hubo participación cubana.'
        return text

    verb = [
        [' tuvieron particpación ', ' tuvo participación '],
        [' jugaron ', ' jugó ']
    ]

    sust = [
        ' jugadores cubanos ', ' jugador cubano, que fue ' + outstandings[0][1]
    ]

    i = 0
    if len(total) == 1:
        i = 1

    text += ' En esta jornada' + random.choice(verb)[i] + str(len(total)) + sust[i] + '.'

    return text

def get_new(player_details, sorted_for_outstandings, top_players):

    paragraphs = []

    t = get_first_paragraph(sorted_for_outstandings, top_players)

    paragraphs.append(t)

    print(t)
    print()

    minors = ''

    outstandings = []

    tops = top_players[-1]

    print(sorted_for_outstandings)

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
            paragraphs.append(report)
        else:
            minors += p.get_minority_report()

    title = get_title(player_details, sorted_for_outstandings)

    print(minors)

    paragraphs.append(minors)

    print()

    print(title)

    return (title, paragraphs)

def flow(players_details, sorted_for_outstandings, top_players):
    #outstandings_data = get_outstandings()
    #sorted_for_outstandings = sort_for_outstandings(outstandings_data)

    #print(sorted_oustandings_players)

    #top_players = json.load(open(os.path.join(MODULE, 'games_details.json'), 'r'))

    #players_details = json.load(open(os.path.join(MODULE, 'game_day_data_1.json')))

    title, new = get_new(players_details, sorted_for_outstandings, top_players)

    return (title, new)

#flow()
