# this imports are ugly but necessary
from .stats_play import *
from .stats_player import *
import random

class Player:
    def __init__(self, player_name, player_dict):
        self.dict_classes = {}
        self.player_dict = player_dict
        self.player_name = player_name
        self.init_classes()

    def init_classes(self):

        self.dict_classes['player_name'] = Player_name(self.player_name, self.player_dict)
        self.dict_classes['position'] = Position(self.player_name, self.player_dict)
        self.dict_classes['team'] = Team(self.player_name, self.player_dict)
        self.dict_classes['rival_team'] = Rival_Team(self.player_name, self.player_dict)
        self.dict_classes['H'] = Hits(self.player_name, self.player_dict, 'Entity')

        self.dict_classes['plays'] = []

        for play in self.player_dict['plays']:
            self.dict_classes['plays'].append(Play(self.player_name, self.player_dict, play))

    def get_general_player_stats(self):

        text = ''
        self.dict_classes['hits'] = {}
        self.dict_classes['runs'] = {}

        self.dict_classes['hits']['entity'] = Hits(self.player_name, self.player_dict, 'entity')
        self.dict_classes['hits']['action'] = Hits(self.player_name, self.player_dict)
        self.dict_classes['runs']['entity'] = Runs(self.player_name, self.player_dict, 'entity')
        self.dict_classes['runs']['action'] = Runs(self.player_name, self.player_dict)
        self.dict_classes['BB'] = BB(self.player_name, self.player_dict)

        if self.player_dict['position'] != 'P':

            self.dict_classes['RBI'] = {}

            self.dict_classes['AB'] = AB(self.player_name, self.player_dict)
            self.dict_classes['Double'] = Doubles(self.player_name, self.player_dict)
            self.dict_classes['Triple'] = Triples(self.player_name, self.player_dict)
            self.dict_classes['HR'] = Home_Runs(self.player_name, self.player_dict)
            self.dict_classes['RBI']['entity'] = RBI(self.player_name, self.player_dict, 'entity')
            self.dict_classes['RBI']['action'] = RBI(self.player_name, self.player_dict)

            # complement = self.dict_classes['AB'].text

            ads = []
            if self.player_dict['HR'] > 0:
                ads.append(self.dict_classes['HR'])
            if self.player_dict['Triple'] > 0:
                ads.append(self.dict_classes['Triple'])
            if self.player_dict['Double'] > 0:
                ads.append(self.dict_classes['Double'])

            ads.append(self.dict_classes['BB'])

            values = [self.player_dict['RBI'], self.player_dict['R'], self.player_dict['H']]

            l = [
                [self.dict_classes['RBI']['action'], self.dict_classes['runs']['entity'], self.dict_classes['hits']['entity']],
                [self.dict_classes['runs']['action'], self.dict_classes['RBI']['entity'], self.dict_classes['hits']['entity']],
                [self.dict_classes['hits']['action'], self.dict_classes['RBI']['entity'], self.dict_classes['runs']['entity']]
            ]

            ll = l[values.index(max(values))]

            ll.extend(ads)

            text = ll[0].text + ', con ' + ll[1].text

            for i in range(2, len(ll)):
                if i == len(ll) - 1:
                    text += ' y ' + ll[i].text + '. '
                else:
                    text += ', ' + ll[i].text

            fc = text[0].upper()

            text = text[1:]
            text = fc + text

        else:
            self.dict_classes['impact'] = Impact(self.player_name, self.player_dict)
            self.dict_classes['IP'] = IP(self.player_name, self.player_dict)
            self.dict_classes['SO'] = SO(self.player_name, self.player_dict)
            self.dict_classes['batters_faced'] = Batters_faced(self.player_name, self.player_dict)


            text = self.dict_classes['IP'].text + ' ' + \
            self.dict_classes['batters_faced'].text + ', ' + \
            self.dict_classes['runs']['action'].text + ', ' + \
            self.dict_classes['hits']['action'].text + ', con ' + \
            self.dict_classes['SO'].text + ' y ' + self.dict_classes['BB'].text

            impact = self.dict_classes['impact'].text
            if impact != '':
                text += ', y ' + impact + '. '
            else:
                text += '. '

            fc = text[0].upper()

            text = text[1:]
            text = fc + text

        return text

    def get_initial_sentence(self):
        text = ''
        l = [
            'tuvo una destacada labor en su encuentro, ',
            'destacó entre los demás jugadores en el juego, ',
            'tuvo una buena actuación en el juego, '
        ]
        against = [
            'frente a',
            'contra',
            'ante',
            'enfrentado a'
        ]

        wl = self.player_dict['result']

        score_team = self.player_dict['game_details'][self.player_dict['team']]['score']
        score_rival_team = self.player_dict['game_details'][self.player_dict['rival_team']]['score']
        season_rival_score = \
        self.player_dict['game_details'][self.player_dict['rival_team']]['season_score']
        season_score = self.player_dict['game_details'][self.player_dict['team']]['season_score']

        text2 = str(score_team) + ' por ' + str(score_rival_team) + ' ' + \
        random.choice(against) + ' ' + self.player_dict['rival_team'] + ' (' + \
        season_rival_score + '). '

        if wl == 'win':
            act = [
                'apoyar', 'favorecer'
            ]
            ww = [
                'en la victoria de ' + self.player_dict['team'] + ' (' + season_score + ')',
                'en el triunfo de ' + self.player_dict['team'] + ' (' + season_score + ')'
            ]

            text = self.player_name + ' ' + random.choice(l) + 'para ' + \
            random.choice(act) + ' ' + random.choice(ww) + ' ' + \
            text2

        else:
            act = [
                'no pudo evitar',
                'no evitó'
            ]

            ll = [
                'la derrota de ' + self.player_dict['team'] + ' (' + season_score + ')',
                'que cayera ' + self.player_dict['team'] + ' (' + season_score + ')'
            ]

            text = self.player_name + ' ' + random.choice(l) + 'pero ' + \
            random.choice(act) + ' ' + random.choice(ll) + ' ' + \
            text2

        return text

    def get_report(self):
        self.dict_classes['plays'].sort()

        plays = self.dict_classes['plays']
        text = ''

        ic = self.get_initial_sentence()

        ps = []

        ps.append(ic)

        for p in plays:
            if p.wpa >= 4:
                ps.append(p.get_text_play())

        gp = self.get_general_player_stats()

        if self.player_dict['position'] != 'P':
            fc = gp[0].lower()

            gp = gp[1:]
            gp = fc + gp

            gp = 'En el juego ' + gp

        ps.insert(2, gp)

        for p in ps:
            text += p

        text = text.replace(' de el ', ' del ')
        text = text.replace(' a el ', ' al ')
        text = text.replace('  ', ' ')
        text = text.replace(' ,', ',')

        return text

    def get_minority_report(self):
        text = ''

        text2 = 'en '

        if self.player_dict['result'] == 'win':
            text2 += 'la victoria de '
        else:
            text2 += 'la derrota de '

        team = self.player_dict['team']
        score_team = self.player_dict['game_details'][team]['score']
        season_team = self.player_dict['game_details'][team]['season_score']

        rival_team = self.player_dict['rival_team']
        score_rival_team = self.player_dict['game_details'][rival_team]['score']
        season_rival_team = self.player_dict['game_details'][rival_team]['season_score']

        text2 += team + ' (' + season_team + ') ' + str(score_team) + '-' + str(score_rival_team) + \
        ' contra ' + rival_team + ' (' + season_rival_team + '). '

        general_stats = self.get_general_player_stats()

        fc = general_stats[0].lower()

        general_stats = general_stats[1:]
        general_stats = fc + general_stats

        text = self.player_name + ' ' + general_stats[:-2] + ', ' + text2

        return text

class Play:
    def __init__(self, player_name, player_dict, play_dict):
        #super().__init__(player_name, player_dict)
        self.player_name = player_name
        self.player_dict = player_dict
        self.play_dict = play_dict
        self.wpa = play_dict['wpa']
        self.dict_classes = {}
        self.init_classes()
        self.init_c()

    def __lt__(self, play):
        return self.wpa < play.wpa

    def init_c(self):
        self.dict_classes['player_name'] = Player_name(self.player_name, self.player_dict)
        self.dict_classes['position'] = Position(self.player_name, self.player_dict)
        self.dict_classes['team'] = Team(self.player_name, self.player_dict)
        self.dict_classes['rival_team'] = Rival_Team(self.player_name, self.player_dict)
        self.dict_classes['referring'] = Referring([self.dict_classes['player_name'].text, \
        self.dict_classes['position'].text, 'el cubano'])

    def init_classes(self):
        self.dict_classes['play_desc'] = {}
        self.dict_classes['inning'] = Inning(self.player_name, self.player_dict, self.play_dict)
        self.dict_classes['current_score'] = \
        Current_Score(self.player_name, self.player_dict, self.play_dict)
        self.dict_classes['outs'] = Outs(self.player_name, self.player_dict, self.play_dict)
        self.dict_classes['rob'] = ROB(self.player_name, self.player_dict, self.play_dict)
        self.dict_classes['pitcher'] = \
        Current_Pitcher(self.player_name, self.player_dict, self.play_dict)
        self.dict_classes['play_desc']['direction'] = \
        Direction(self.player_name, self.player_dict, self.play_dict)
        self.dict_classes['play_desc']['event'] = \
        Event(self.player_name, self.player_dict, self.play_dict)
        self.dict_classes['play_desc']['RBI'] = {}
        self.dict_classes['play_desc']['RBI']['action'] = \
        RBI_Result(self.player_name, self.player_dict, self.play_dict, 'action')
        self.dict_classes['play_desc']['RBI']['reaction'] = \
        RBI_Result(self.player_name, self.player_dict, self.play_dict, 'reaction')
        self.dict_classes['outs_play_result'] = \
        Out_Play_Results(self.player_name, self.player_dict, self.play_dict)
        self.dict_classes['score_result'] = \
        Runs_Play_Result(self.player_name, self.player_dict, self.play_dict)

    def get_text_play(self):
        if self.player_dict['position'] != 'P':

            entity = self.dict_classes['referring'].text

            inning = self.dict_classes['inning'].text
            rob = self.dict_classes['rob'].text

            complements = [
                self.dict_classes['current_score'].text,
                self.dict_classes['outs'].text,
                self.dict_classes['pitcher'].text,
            ]

            comp = [rob, random.choice(complements)]

            action = self.dict_classes['play_desc']['event'].text

            reaction = [
                self.dict_classes['score_result'].text,
                self.dict_classes['play_desc']['RBI']['reaction'].text
            ]

            while '' in reaction:
                reaction.remove('')

            comp_after_event = self.dict_classes['play_desc']['direction'].text

            react = [
                'para',
                'y logró',
                'para conseguir'
            ]

            b = [
                'Gracias a ello consiguió',
                'Esto le permitió'
            ]

            #TODO: revisar esto q no se usa
            # x = np.random.randint(len(complements))
            # y = np.random.randint(len(complements))
            # while y == x:
            #     y = np.random.randint(len(complements))

        else:
            entity = self.dict_classes['referring'].text

            inning = self.dict_classes['inning'].text

            #current_score = self.dict_classes['current_score'].text
            #outs = self.dict_classes['outs'].text
            rob = self.dict_classes['rob'].text

            complements = [
                self.dict_classes['current_score'].text,
                self.dict_classes['outs'].text,
            ]

            comp = [rob, random.choice(complements)]

            action = self.dict_classes['play_desc']['event'].text

            reaction = [
                self.dict_classes['score_result'].text,
                self.dict_classes['outs_play_result'].text
            ]

            #score_result = self.dict_classes['score_result'].text
            #outs_play_result = self.dict_classes['outs_play_result'].text


            while '' in reaction:
                reaction.remove('')

            comp_after_event = self.dict_classes['play_desc']['direction'].text

            #contents = [
            #    [],
            #    []
            #]

            react = [
                'para',
                'y logró',
                'para conseguir'
            ]

            b = [
                'Gracias a ello consiguió',
                'Esto le permitió'
            ]

            #TODO: revisar esto q no se usa
            # x = np.random.randint(len(complements))
            # y = np.random.randint(len(complements))
            # while y == x:
            #     y = np.random.randint(len(complements))


        text = [
            entity + ', ' + comp[1] + ', ' + action + ' ' + comp_after_event + \
            ' ' + random.choice(react) + ' ' + \
            random.choice(reaction) + ', ' + comp[0] + ' ' + \
            inning + '. ',
            inning + ' y ' + comp[0] + ', ' + entity + ' ' + action + ' ' + \
            comp_after_event + ' ' + random.choice(react) + ' ' + \
            random.choice(reaction) + '. ',
            entity + ', ' + comp[0] + ', ' + action + \
            ' ' + comp_after_event + ' ' + random.choice(react) + ' ' + \
            random.choice(reaction) + ' ' + inning + '. ',
            comp[0] + ', ' + entity + ' ' + action + ' ' + comp_after_event + ' ' + \
            inning + '. ' + random.choice(b) + ' ' + \
            random.choice(reaction) + ', ' + comp[1] + '. '
        ]

        return_text = random.choice(text)

        fc = return_text[0].upper()

        return_text = return_text[1:]
        return_text = fc + return_text

        return return_text
