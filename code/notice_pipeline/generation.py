import random
from .base import News
from notice_generator import Player, Play
from notice_generator.stats_player import Highlights_Player
from notice_generator.utils import get_yesterday_date as gyd
from gensim.summarization import summarize

class New_Templates(News):
    __slots__ = ()
    def __init__(self, player_details, sorted_for_outstandings, games_details, players_teams):
        super().__init__(player_details, sorted_for_outstandings, games_details, players_teams)

    def _get_first_paragraph(self):
        outstandings = self._sorted_for_outstandings
        games_details = self._games_details

        date = gyd()
        text = ''
        fo = [
            'En la jornada del ' + date + ' de las Grandes Ligas se disputaron ' + str(len(games_details)) + \
            ' encuentros de béisbol.',
            'El ' + date + ' se jugaron ' + str(len(games_details)) + ' encuentros en las Grandes Ligas.'
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

    @staticmethod
    def _sort_games(all_games):

        for i in all_games:
            i['checked'] = False

        all_games_sorted = []
        last = []

        for game in all_games:
            if game['checked']:
                continue
            if game['players']['home'] or game['players']['away']:
                #away = list(game.keys())[0]
                #home = list(game.keys())[1]
                if game['players']['home'] and game['players']['home'][0][1] == 1 and not game['checked']:
                    game['checked'] = True
                    all_games_sorted.append(game)
                    if game['uod'] == 2 or game['uod'] == 3:
                        index = 5 - game['uod']
                        for g in all_games:
                            x = (list(game.keys())[0], list(game.keys())[1])
                            y = (list(g.keys())[0], list(g.keys())[1])
                            if ((x[0] == y[0] and x[1] == y[1]) or (x[1] == y[0] and x[0] == y[1])) and g['uod'] == index:
                                if g['players']['home'] or g['players']['away']:
                                    g['checked'] = True
                                    all_games_sorted.append(g)
                elif game['players']['away'] and game['players']['away'][0][1] == 1 and not game['checked']:
                    game['checked'] = True
                    all_games_sorted.append(game)
                    if game['uod'] == 2 or game['uod'] == 3:
                        index = 5 - game['uod']
                        for g in all_games:
                            x = (list(game.keys())[0], list(game.keys())[1])
                            y = (list(g.keys())[0], list(g.keys())[1])
                            if ((x[0] == y[0] and x[1] == y[1]) or (x[1] == y[0] and x[0] == y[1])) and g['uod'] == index:
                                if g['players']['home'] or g['players']['away']:
                                    g['checked'] = True
                                    all_games_sorted.append(g)
                else:
                    last.append(game)

        all_games_sorted.extend(last)

        return all_games_sorted

    def _get_title(self):
        player_details = self._player_details
        outstandings = self._sorted_for_outstandings

        # parser = ConfigParser()
        # parser.read(os.path.join(MODULE, 'config.ini'))

        # country = parser.get('country', 'country')

        # if country != 'Cuba':
        #     pass

        # else:
        # TODO: cambiar las plantillas basado en la nacionalidad del jugador
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
            title = 'Sin participación cubana en jornada de las Grandes Ligas'
            return title


        elif outstandings[0][2] == 1:
            if len(outstandings) > 1 and outstandings[1][2] == 1:
                name_1 = outstandings[0][1]
                name_2 = outstandings[1][1]

                name_1 = name_1.replace('_1', '').replace('_2', '')
                name_2 = name_2.replace('_1', '').replace('_2', '')

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
                    name = name.replace('_1', '').replace('_2', '')
                    team = player_details['hitters'][name]['team']

                    hits = player_details['hitters'][name]['H']
                    hr = player_details['hitters'][name]['HR']
                    rbi = player_details['hitters'][name]['RBI']
                    r = player_details['hitters'][name]['R']

                    stats = [
                        (hits, 'Con ' + str(hits) + random.choice([' hits, ', ' imparables, '])),
                        (hr, 'Con ' + str(hr) + random.choice([' jonrones, ', ' cuadrangulares, '])),
                        (rbi, 'Con ' + str(rbi) + ' carreras impulsadas, '),
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
                                ' en jornada destacada para la ofensiva cubana',
                                ' en buen día para los bateadores cubanos'
                            ]
                        )

                        return text

                    elif prom_bat < 0.5:
                        text += name + ' '
                        text += random.choice(
                            [
                                'saca la cara por los bateadores cubanos en jornada de las Grandes Ligas',
                                'sobresale en mal día para los bateadores cubanos',
                                'resalta entre los bateadores cubanos en Grandes Ligas de béisbol'
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
                                ' en jornada destacada para el pitcheo cubano',
                                ' en una buena jornada para el pitcheo cubano',
                                ' en un buen día para el pitcheo cubano'
                            ]
                        )
                        return text

                    elif prom_pit < 0.5:
                        text += name + ' '
                        text += random.choice(
                            [
                                'salva la honra por los lanzadores cubanos en la jornada de las Grandes Ligas',
                                'sobresale en mal día para los lanzadores cubanos',
                                'resalta entre los lanzadores cubanos en Grandes Ligas de béisbol'
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
                        'Jornada positiva para los cubanos en Grandes Ligas de béisbol',
                        'Buena actuación de los cubanos en jornada de la MLB',
                        'Actuaciones destacables para jugadores cubanos en las Grandes Ligas'
                    ]
                )
                return text
            else:
                text += random.choice(
                    [
                        'Poco destaque de jugadores cubanos en las Grandes Ligas',
                        'Jugadores cubanos con pobres resultados en jornada de la MLB',
                        'Discreta actuación de los cubanos en las Grandes Ligas de béisbol'
                    ]
                )
                return text

        text += random.choice(
            [
                ' en jornada de las Grandes Ligas de béisbol',
                ' en una jornada más de la MLB',
                ' en la MLB',
                ' en las Grandes Ligas'
            ]
        )

        return text

    @staticmethod
    def _get_list_players_text(players):
        text = players[0]
        for i in range(1, len(players)):
            if i == len(players) - 1:
                text += ' y ' + players[i]
            else:
                text += ', ' + players[i]

        return text

    def _get_game_summary(self, game):

        uod = game['uod']

        away_team = list(game.keys())[0]
        home_team = list(game.keys())[1]

        stadium = game['stadium']

        winner_team = ''
        loser_team = ''

        winner_score = ''
        loser_score = ''

        if game[away_team]['score'] > game[home_team]['score']:
            winner_team = away_team
            loser_team = home_team
            winner_score = str(game[away_team]['score'])
            loser_score = str(game[home_team]['score'])
        else:
            winner_team = home_team
            loser_team = away_team
            winner_score = str(game[home_team]['score'])
            loser_score = str(game[away_team]['score'])

        o = []
        all_players = []
        winner_team_players = []
        loser_team_players = []

        for p, oo in game['players']['home']:
            if oo == 1:
                o.append(p.player_name)
            else:
                all_players.append(p.player_name)
                if p.dict_classes['team'].text == winner_team:
                    winner_team_players.append(p)
                else:
                    loser_team_players.append(p)

        for p, oo in game['players']['away']:
            if oo == 1:
                o.append(p.player_name)
            else:
                all_players.append(p.player_name)
                if p.dict_classes['team'].text == winner_team:
                    winner_team_players.append(p)
                else:
                    loser_team_players.append(p)

        outstanding_template = ''
        _get_list_players_text = self._get_list_players_text

        if len(o) > 1:
            outstanding_template = random.choice(
                [
                    'los cubanos más destacados fueron ' + _get_list_players_text(o),
                    'destacaron ' + _get_list_players_text(o),
                    _get_list_players_text(o) + ' fueron los mejores jugadores cubanos',
                    'sobresalieron ' + _get_list_players_text(o)
                ]
            )
        elif len(o) == 1:
            outstanding_template = random.choice(
                [
                    'el cubano más destacado fue ' + o[0],
                    'destacó ' + o[0],
                    o[0] + ' fue el mejor jugador de Cuba',
                    'sobresalió ' + o[0]
                ]
            )

        initial_sentence = ''

        if uod == 1:
            if o:
                if len(all_players) > 1:
                    initial_sentence = random.choice(
                        [
                            'En el juego en el cual ' + outstanding_template + \
                            ', también tuvieron participación ' + _get_list_players_text(all_players) + \
                            '.',
                            _get_list_players_text(all_players) + ' también jugaron en el encuentro en el cual ' + \
                            outstanding_template + '.',
                            'En la victoria de ' + winner_team + ' sobre ' + loser_team + ', en la cual ' + \
                            outstanding_template + ', también vieron acción ' + \
                            _get_list_players_text(all_players) + '.',
                            _get_list_players_text(all_players) + ' también saltaron al césped del terreno ' + \
                            'de juego en este enfrentamiento.',
                            'Representando a Cuba, otros de los jugadores que participaron en el juego fueron ' + \
                            _get_list_players_text(all_players) + '.'
                        ]
                    )
                else:
                    initial_sentence = random.choice(
                        [
                            'En el juego en el cual ' + outstanding_template + \
                            ', también tuvo participación ' + all_players[0] + \
                            '.',
                            all_players[0] + ' también jugó en el encuentro en el cual ' + \
                            outstanding_template + '.',
                            'En la victoria de ' + winner_team + ' sobre ' + loser_team + ', en la cual ' + \
                            outstanding_template + ', también vió acción el cubano ' + \
                            all_players[0] + '.',
                            all_players[0] + ' también saltó al césped del terreno ' + \
                            'de juego en este enfrentamiento.',
                            'Representando a Cuba, otro de los jugadores que participó en el juego fue ' + \
                            all_players[0] + '.'
                        ]
                    )
            else:
                if len(all_players) > 1:
                    initial_sentence = random.choice(
                        [
                            winner_team + ' venció ' + winner_score + ' por ' + \
                            loser_score + ' al conjunto de ' + loser_team + \
                            '. En ese encuentro por Cuba participaron ' + \
                            _get_list_players_text(all_players) + '.',
                            'En el estadio ' + stadium + ', ' + _get_list_players_text(all_players) + \
                            ' vieron acción en la victoria de ' + winner_team + ' sobre ' + loser_team + \
                            ' ' + winner_score + ' por ' + loser_score + '.',
                            _get_list_players_text(all_players) + \
                            ' fueron los cubanos que jugaron en el encuentro que enfrentó a los equipos de ' + \
                            winner_team + ' y ' + loser_team + ', con victoria para el primero.',
                            'En el enfrentamiento que tuvieron los conjuntos de ' + winner_team + ' y ' + \
                            loser_team + ', hicieron su aparición ' + _get_list_players_text(all_players) + '.',
                            _get_list_players_text(all_players) + ' tomaron parte en el partido de béisbol que ' + \
                            winner_team + ' le ganó a ' + loser_team + ' ' + winner_score + ' por ' + loser_score + '.'
                        ]
                    )
                else:
                    initial_sentence = random.choice(
                        [
                            winner_team + ' venció ' + winner_score + ' por ' + \
                            loser_score + ' al conjunto de ' + loser_team + \
                            '. En ese encuentro por Cuba participó ' + \
                            all_players[0] + '.',
                            'En el estadio ' + stadium + ', ' + all_players[0] + \
                            ' vió acción en la victoria de ' + winner_team + ' sobre ' + loser_team + \
                            ' ' + winner_score + ' por ' + loser_score + '.',
                            all_players[0] + \
                            ' fue el cubano que jugó en el encuentro que enfrentó a los equipos de ' + \
                            winner_team + ' y ' + loser_team + ', con victoria para el primero.',
                            'En el enfrentamiento que tuvieron los conjuntos de ' + winner_team + ' y ' + \
                            loser_team + ', hizo su aparición  ' + all_players[0] + '.',
                            all_players[0] + ' tomó parte en el partido de béisbol que ' + \
                            winner_team + ' le ganó a ' + loser_team + ' ' + winner_score + ' por ' + loser_score + '.'
                        ]
                    )
        elif uod == 2:
            if o:
                if len(all_players) > 1:
                    initial_sentence = random.choice(
                        [
                            _get_list_players_text(all_players) + \
                            ' también vieron acción en el primer encuentro del doble entre los equipos de ' + \
                            winner_team + ' y ' + loser_team + ', en el cual ' + outstanding_template + '.',
                            'En el primer juego del doble que tuvieron ' + winner_team + ' y ' + \
                            loser_team + ', con victoria para el primero, y en el que además ' + \
                            outstanding_template + ', también jugaron por Cuba ' + \
                            _get_list_players_text(all_players),
                            winner_team + ' venció a ' + loser_team + ' ' + winner_score + ' por ' + \
                            loser_score + ' en el primer juego de la doble jornada que disputaron ambos equipos, ' + \
                            'en el cual ' + outstanding_template + '. Además, en este encuentro participaron también ' + \
                            _get_list_players_text(all_players) + '.'
                        ]
                    )
                else:
                    initial_sentence = random.choice(
                        [
                            all_players[0] + \
                            ' también vió acción en el primer encuentro del doble entre los equipos de ' + \
                            winner_team + ' y ' + loser_team + ', en el cual ' + outstanding_template + '.',
                            'En el primer juego del doble que tuvieron ' + winner_team + ' y ' + \
                            loser_team + ', con victoria para el primero, y en el que además ' + \
                            outstanding_template + ', también jugó por Cuba ' + \
                            all_players[0],
                            winner_team + ' venció a ' + loser_team + ' ' + winner_score + ' por ' + \
                            loser_score + ' en el primer juego de la doble jornada que disputaron ambos equipos, ' + \
                            'en el cual ' + outstanding_template + '. Además, en este encuentro participó también ' + \
                            all_players[0] + '.'
                        ]
                    )
            else:
                if len(all_players) > 1:
                    initial_sentence = random.choice(
                        [
                            winner_team + ' venció ' + winner_score + ' por ' + \
                            loser_score + ' a ' + loser_team + ', en el primer encuentro del doble ' + \
                            'disputado entre estos dos conjuntos. ' + _get_list_players_text(all_players) + \
                            ' fueron los jugadores cubanos que vieron acción en este juego.',
                            'En el primero de dos juegos disputados entre ' + winner_team + ' y ' + \
                            loser_team + ', ' + _get_list_players_text(all_players) + ' fueron los ' + \
                            ' representantes cubanos en la victoria de ' + winner_team + ', ' + \
                            winner_score + ' por ' + loser_score + '.',
                            _get_list_players_text(all_players) + ' fueron los jugadores cubanos que ' + \
                            'jugaron el primer encuentro del doble disputado entre ' + winner_team + \
                            ' y ' + loser_team + '.'
                        ]
                    )
                else:
                    initial_sentence = random.choice(
                        [
                            winner_team + ' venció ' + winner_score + ' por ' + \
                            loser_score + ' a ' + loser_team + ', en el primer encuentro del doble ' + \
                            'disputado entre estos dos conjuntos. ' + all_players[0] + \
                            ' fue el único jugador cubano que vió acción en este juego.',
                            'En el primero de dos juegos disputados entre ' + winner_team + ' y ' + \
                            loser_team + ', ' + all_players[0] + ' representó a los jugadores ' + \
                            ' cubanos en la victoria de ' + winner_team + ', ' + \
                            winner_score + ' por ' + loser_score + '.',
                            all_players[0] + ' fue el jugador cubano ' + \
                            'en el primer encuentro del doble disputado entre ' + winner_team + \
                            ' y ' + loser_team + '.'
                        ]
                    )
        else:
            if o:
                initial_sentence = random.choice(
                    [
                        winner_team + ' venció a ' + loser_team + ' en el segundo encuentro del doble, ' + \
                        'en el cual ' + outstanding_template + '.',
                        'En el segundo encuentro de la jornada para ' + winner_team + \
                        ' y ' + loser_team + ', la victoria fue para ' + winner_team + ' ' + winner_score + \
                        ' por ' + loser_score + ', juego en el cual ' + outstanding_template + '.'
                    ]
                )
            else:
                initial_sentence = random.choice(
                    [
                        winner_team + ' venció a ' + loser_team + ' en el segundo encuentro del doble. ',
                        'En el segundo encuentro de la jornada para ' + winner_team + \
                        ' y ' + loser_team + ', la victoria fue para ' + winner_team + ' ' + winner_score + \
                        ' por ' + loser_score + '.'
                    ]
                )

        mr_winner = []
        mr_loser = []
        mr_all = []

        for p in winner_team_players:
            text = p.get_general_player_stats()
            mr_winner.append(text)
            mr_all.append(text)

        for p in loser_team_players:
            text = p.get_general_player_stats()
            mr_loser.append(text)
            mr_all.append(text)

        rest_of_paragraph = ''

        if winner_team_players:
            rest_of_paragraph = random.choice(
                [
                    'Por ' + winner_team + ', ',
                    'Jugando por los vencedores, ',
                    'Para el equipo ganador, ',
                    'Representando a ' + winner_team + ', '
                ]
            )
            for mw in mr_winner:
                rest_of_paragraph += mw + '. '
            if mr_loser:
                rest_of_paragraph += random.choice(
                    [
                        ' Mientras, por ' + loser_team + ', ',
                        ' Por otra parte, jugando para el equipo perdedor, ',
                        ' Para el equipo derrotado, ',
                        ' Representando a ' + loser_team + ', '
                    ]
                )
                for ml in mr_loser:
                    rest_of_paragraph += ml + '. '

        else:
            rest_of_paragraph = random.choice(
                [
                    'Por ' + loser_team + ', ',
                    'Jugando por el equipo derrotado, ',
                    'Para los perdedores, ',
                    'Representando a ' + loser_team + ', ',
                    ''
                ]
            )
            for mw in mr_loser:
                rest_of_paragraph += mw + '. '

        return initial_sentence + ' ' + rest_of_paragraph

    def _generate_game(self, game):
        paragraphs = []
        outstandings = []
        have_not_outstandings = False
        for p, o in game['players']['home']:
            if o == 1:
                outstandings.append(p)
            else:
                have_not_outstandings = True
        for p, o in game['players']['away']:
            if o == 1:
                outstandings.append(p)
            else:
                have_not_outstandings = True

        for i in range(len(outstandings)):
            paragraphs.append(outstandings[i].get_report(i))

        if have_not_outstandings:
            paragraphs.append(self._get_game_summary(game))

        return paragraphs

    def _get_game_without_cubans(self, game):
        uod = game['uod']

        away_team = list(game.keys())[0]
        home_team = list(game.keys())[1]

        #stadium = game['stadium']

        winner_team = ''
        loser_team = ''

        winner_score = ''
        loser_score = ''

        if game[away_team]['score'] > game[home_team]['score']:
            winner_team = away_team
            loser_team = home_team
            winner_score = str(game[away_team]['score'])
            loser_score = str(game[home_team]['score'])
        else:
            winner_team = home_team
            loser_team = away_team
            winner_score = str(game[home_team]['score'])
            loser_score = str(game[away_team]['score'])

        winner_pitcher = game['WP']
        loser_pitcher = game['LP']
        saver_pitcher = ''
        if 'SV' in game:
            saver_pitcher = game['SV']

        player_team = ''
        if not game['players']['home']:
            player_team = away_team
        elif not game['players']['away']:
            player_team = home_team

        all_players = []
        for p in game['players']['home']:
            all_players.append(p)
        for p in game['players']['away']:
            all_players.append(p)

        text = ''
        _get_list_players_text = self._get_list_players_text
        if uod == 1:
            if player_team != '':
                if len(all_players) > 1:
                    text = random.choice(
                        [
                            winner_team + ' venció ' + winner_score + ' por ' + loser_score + \
                            ' al conjunto de ' + loser_team + '. Los jugadores cubanos que juegan para ' + \
                            player_team + ', ' + _get_list_players_text(all_players) + ', no tuvieron ' + \
                            'participación en el encuentro.',
                            _get_list_players_text(all_players) + ' no vieron acción en el encuentro de ' + \
                            'su equipo, ' + player_team + '. En este encuentro, ' + winner_team + ' se llevó ' + \
                            'la victoria ' + winner_score + ' por ' + loser_score + ' frente a ' + loser_team + '.',
                            'Los cubanos ' + _get_list_players_text(all_players) + \
                            ' no disputaron el enfrentamiento de ' + winner_team + ' y ' + loser_team + \
                            ', con victoria para el primero.'
                        ]
                    )
                else:
                    text = random.choice(
                        [
                            winner_team + ' venció ' + winner_score + ' por ' + loser_score + \
                            ' al conjunto de ' + loser_team + '. El jugador cubano que juega para ' + \
                            player_team + ', ' + all_players[0] + ', no tuvo ' + \
                            'participación en el encuentro.',
                            all_players[0] + ' no vió acción en el encuentro de ' + \
                            'su equipo, ' + player_team + '. En este encuentro, ' + winner_team + ' se llevó ' + \
                            'la victoria ' + winner_score + ' por ' + loser_score + ' frente a ' + loser_team + '.',
                            'El cubano ' + all_players[0] + \
                            ' no disputó el enfrentamiento de ' + winner_team + ' y ' + loser_team + \
                            ', con victoria para el primero.'
                        ]
                    )
            else:
                text = random.choice(
                    [
                        winner_team + ' venció ' + winner_score + ' por ' + loser_score + \
                        ' al conjunto de ' + loser_team + '. Los cubanos ' + \
                        _get_list_players_text(all_players) + ', que juegan para los equipos ' + \
                        'implicados, no tuvieron participación en el encuentro.',
                        _get_list_players_text(all_players) + ' no vieron acción en el encuentro de ' + \
                        'sus respectivos equipos. En este encuentro, ' + winner_team + ' se llevó ' + \
                        'la victoria ' + winner_score + ' por ' + loser_score + ' frente a ' + loser_team + '.',
                        'Los cubanos ' + _get_list_players_text(all_players) + \
                        ' no disputaron el enfrentamiento de ' + winner_team + ' y ' + loser_team + \
                        ', con victoria para el primero.'
                    ]
                )
        elif uod == 2:
            if player_team != '':
                if len(all_players) > 1:
                    text = random.choice(
                        [
                            winner_team + ' venció ' + winner_score + ' por ' + loser_score + \
                            ' al conjunto de ' + loser_team + \
                            ' en el primer encuentro del doble disputado ' + \
                            'entre estos dos equipos. Los jugadores cubanos que juegan para ' + \
                            player_team + ', ' + _get_list_players_text(all_players) + ', no tuvieron ' + \
                            'participación en el encuentro.',
                            _get_list_players_text(all_players) + ' no vieron acción en el primer encuentro ' + \
                            'del doble de su equipo, ' + player_team + '. En este encuentro, ' + winner_team + \
                            ' se llevó la victoria ' + winner_score + ' por ' + loser_score + ' frente a ' + \
                            loser_team + '.',
                            'Los cubanos ' + _get_list_players_text(all_players) + \
                            ' no disputaron el primer enfrentamiento de ' + winner_team + ' y ' + loser_team + \
                            ' en la doble jornada, con victoria para el primero.'
                        ]
                    )
                else:
                    text = random.choice(
                        [
                            winner_team + ' venció ' + winner_score + ' por ' + loser_score + \
                            ' al conjunto de ' + loser_team + \
                            ' en el primer encuentro del doble disputado ' + \
                            'entre estos dos equipos. El jugador cubano que juega para ' + \
                            player_team + ', ' + all_players[0] + ', no tuvo ' + \
                            'participación en el encuentro.',
                            all_players[0] + ' no vió acción en el primer encuentro ' + \
                            'del doble de su equipo, ' + player_team + '. En este encuentro, ' + winner_team + \
                            ' se llevó la victoria ' + winner_score + ' por ' + loser_score + ' frente a ' + \
                            loser_team + '.',
                            'El cubano ' + all_players[0] + \
                            ' no disputó el primer enfrentamiento de ' + winner_team + ' y ' + loser_team + \
                            ' en la doble jornada, con victoria para el primero.'
                        ]
                    )
            else:
                text = random.choice(
                    [
                        winner_team + ' venció ' + winner_score + ' por ' + loser_score + \
                        ' al conjunto de ' + loser_team + \
                        ' en el primer encuentro del doble disputado ' + \
                        'entre estos dos equipos. Los cubanos ' + \
                        _get_list_players_text(all_players) + ', no tuvieron ' + \
                        'participación en el encuentro.',
                        _get_list_players_text(all_players) + ' no vieron acción en el primer encuentro ' + \
                        'del doble celebrado entre ' + winner_team + ' y ' + loser_team + \
                        '. En este encuentro, ' + winner_team + \
                        ' se llevó la victoria ' + winner_score + ' por ' + loser_score + ' frente a ' + \
                        loser_team + '.',
                        'Los cubanos ' + _get_list_players_text(all_players) + \
                        ' no disputaron el primer enfrentamiento de ' + winner_team + ' y ' + loser_team + \
                        ' en la doble jornada, con victoria para el primero.'
                    ]
                )
        else:
            if player_team != '':
                if len(all_players) > 1:
                    text = random.choice(
                        [
                            'En el segundo encuentro del doble, ' + _get_list_players_text(all_players) + \
                            ' tampoco disputaron el encuentro de su equipo. En esta ocasión, la victoria ' + \
                            'fue para ' + winner_team + ' ' + winner_score + ' por ' + loser_score + '.',
                            'Los cubanos tampoco vieron acción en el segundo encuentro, en el cual ' + \
                            winner_team + ' le ganó a ' + loser_team + ' ' + winner_score + ' por ' + loser_score \
                            + '.'
                        ]
                    )
                else:
                    text = random.choice(
                        [
                            'En el segundo encuentro del doble, ' + all_players[0] + \
                            ' tampoco disputó el encuentro de su equipo. En esta ocasión, la victoria ' + \
                            'fue para ' + winner_team + ' ' + winner_score + ' por ' + loser_score + '.',
                            'El cubano tampoco vió acción en el segundo encuentro, en el cual ' + \
                            winner_team + ' le ganó a ' + loser_team + ' ' + winner_score + ' por ' + loser_score \
                            + '.'
                        ]
                    )
            else:
                text = random.choice(
                        [
                            'En el segundo encuentro del doble, ' + _get_list_players_text(all_players) + \
                            ' tampoco disputaron el encuentro de sus equipos. En esta ocasión, la victoria ' + \
                            'fue para ' + winner_team + ' ' + winner_score + ' por ' + loser_score + '.',
                            'Los cubanos tampoco vieron acción en el segundo encuentro, en el cual ' + \
                            winner_team + ' le ganó a ' + loser_team + ' ' + winner_score + ' por ' + loser_score \
                            + '.'
                        ]
                    )

        text += ' '
        if saver_pitcher != '':
            text += random.choice(
                [
                    'La victoria fue para ' + winner_pitcher + ', con salvamento para ' + saver_pitcher + \
                    '. El pitcher perderor fue ' + loser_pitcher + '.',
                    winner_pitcher + ' fue el pitcher vencedor, mientras que la derrota corrió a cargo de ' + \
                    loser_pitcher + '. Hubo juego salvado para ' + saver_pitcher + '.',
                    winner_pitcher + ' se llevó el triunfo, ' + saver_pitcher + ' el salvamento y ' + \
                    loser_pitcher + ' la derrota.'
                ]
            )
        else:
            text += random.choice(
                [
                    'La victoria fue para ' + winner_pitcher + \
                    '. El pitcher perderor fue ' + loser_pitcher + '.',
                    winner_pitcher + ' fue el pitcher vencedor, mientras que la derrota corrió a cargo de ' + \
                    loser_pitcher + '.',
                    winner_pitcher + ' se llevó el triunfo y ' + \
                    loser_pitcher + ' la derrota.'
                ]
            )

        return text

    def _get_text(self):
        player_details = self._player_details
        games_details = self._games_details
        players_teams = self._players_teams

        paragraphs = []

        t = self._get_first_paragraph()
        paragraphs.append(t)

        #outstandings = []
        all_players = []

        for _, player, o in self._sorted_for_outstandings:
            if player in player_details['pitchers']:
                p = Player(player, player_details['pitchers'][player])
            else:
                p = Player(player, player_details['hitters'][player])
            all_players.append((player, o, p))

        all_games = []

        for game in games_details:
            game['players'] = {}
            game['players']['home'] = []
            game['players']['away'] = []
            k = list(game.keys())
            for player, o, p in all_players:
                if p.player_dict['team'] == k[0]:
                    if game['uod'] == 1 or (game['uod'] == 2 and p.first_game) or \
                    (game['uod'] == 3 and p.second_game):
                        game['players']['away'].append((p, o))
                elif p.player_dict['team'] == k[1]:
                    if game['uod'] == 1 or (game['uod'] == 2 and p.first_game) or \
                    (game['uod'] == 3 and p.second_game):
                        game['players']['home'].append((p, o))
            all_games.append(game)

        all_games = self._sort_games(all_games)

        title = self._get_title()

        for g in all_games:
            ps = self._generate_game(g)
            paragraphs.extend(ps)

        cont = 0

        if not all_players:
            for game in games_details:
                game['players'] = {}
                game['players']['home'] = []
                game['players']['away'] = []
                away = list(game.keys())[0]
                home = list(game.keys())[1]
                for p in players_teams:
                    team = players_teams[p]
                    if team == away:
                        game['players']['away'].append(p)
                    elif team == home:
                        game['players']['home'].append(p)
                if game['players']['home'] or game['players']['away']:
                    cont += 1
                    ps = self._get_game_without_cubans(game)
                    paragraphs.append(ps)

        if not cont and not all_players:
            paragraphs.append('En esta jornada, ningún equipo con cubanos en su roster disputó encuentros.')

        complete_new = ''

        for p in paragraphs:
            complete_new += p + '\n\n'

        summary = summarize(complete_new, word_count=70)

        return {
            'title': title,
            'paragraphs': paragraphs,
            'summary': summary,
        }