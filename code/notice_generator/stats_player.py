from .base_class import Stats, Entity, Highlights
from .base_class import Action, EntityCont
import random
import utils as u

# Entity
class Player_name(Entity):
    def get_text(self):
        spl = self._player_name.split()
        c = ''
        for i in spl[1:]:
            c += i + ' '
        return c

# Entity
class Position(Entity):
    def get_text(self):
        pos = self._player_dict['position'].split('-')[0]
        l_pos = u.player_position[pos]
        return random.choice(l_pos)

# Entity
class Team(Entity):
    def get_text(self):
        return self._player_dict['team']

# Entity
class Rival_Team(Entity):
    def get_text(self):
        return self._player_dict['rival_team']

# Entity
class Referring(Entity):
    def __init__(self, referring_list):
        self._referring_list = referring_list

    def get_text(self):
        return random.choice(self._referring_list)

# NO
class Result(EntityCont):
    # win or lose
    def get_text(self):
        return str(self._cont)

###########################################
################ GENERIC ##################
###########################################

# Entity, Action
class Hits(Action):
    def get_text(self):
        cant = self._player_dict['H']

        text = ''
        comp = [
            ['hit', 'hits'],
            ['imparable', 'imparables'],
            ['indiscutible', 'indiscutibles']
        ]
        i = 1
        if cant == 1:
            i = 0

        if self._condition == 'entity':
            return str(cant) + ' ' + random.choice(comp)[i]

        else:
            if self._player_dict['position'] == 'P':
                if cant == 0:
                    text = 'no permitió ' + random.choice(comp)[1]
                else:
                    text = 'permitió ' + str(cant) + ' ' + \
                    random.choice(comp)[i]

            else:
                act = [
                    'disparó',
                    'conectó',
                    'dió'
                ]
                if cant == 0:
                    text = 'no ' + random.choice(act) + ' ' + \
                    random.choice(comp)[1]
                else:
                    text = random.choice(act) + ' ' + str(cant) + \
                    ' ' + random.choice(comp)[i]

        return text

# Entity, Action
class Runs(Action):
    def get_text(self):
        cant = self._player_dict['R']
        comp = [
            ['carrera', 'carreras'],
            ['anotación', 'anotaciones']
        ]
        comp_batter = [
            ['carrera anotada', 'carreras anotadas'],
            ['anotación', 'anotaciones']
        ]

        l = [
            'ninguna anotación',
            'ninguna carrera anotada'
        ]
        i = 1
        if cant == 1:
            i = 0

        text = ''

        if self._condition == 'entity':
            if cant == 0:
                return random.choice(l)
            else:
                text = str(cant) + ' ' + random.choice(comp_batter)[i]

        else:
            if self._player_dict['position'] == 'P':
                er = self._player_dict['ER']
                if cant == 0:
                    c = [
                        'no toleró ' + random.choice(comp)[1],
                        'no dejó que entraran ' + random.choice(comp)[1]
                    ]
                    text = random.choice(c)
                    return text
                else:
                    text = 'permitió ' + str(cant) + ' ' + random.choice(comp)[1]

                if er == cant:
                    text += ', todas limpias'

                elif er == 0:
                    text += ', todas sucias'

                else:
                    text += ', de ellas ' + str(er) + ' limpias'

            else:
                if cant == 0:
                    return ''
                else:
                    i = 1
                    if cant == 1:
                        i = 0
                    text = 'anotó ' + str(cant) + ' ' + random.choice(comp)[i]

        return text

# Entity
class BB(Entity):
    def get_text(self):
        cant = self._player_dict['BB']

        comp = [
            ['base por bola', 'bases por bolas'],
            ['boleto', 'boletos'],
        ]
        i = 1
        if cant == 1:
            i = 0

        if cant == 0:
            l = [
                'ninguna base por bola',
                'ningún boleto'
            ]
            return random.choice(l)

        return str(cant) + ' ' + random.choice(comp)[i]


###########################################
################ HITTERS ##################
###########################################

# Complement
class AB(Entity):
    def get_text(self):
        ab = self._player_dict['AB']
        comp = [
            ['oportunidad al bate', 'oportunidades al bate'],
            ['aparición en el home', 'apariciones en el home'],
            ['turno al bate', 'turnos al bate']
        ]
        i = 1
        if ab == 1:
            i = 0
        text = 'en ' + str(ab) + random.choice(comp)[i]
        return text

# Entity
class Doubles(Entity):
    def get_text(self):
        cant = self._player_dict['Double']
        comp = [
            ['doble', 'dobles'],
            ['doblete', 'dobletes']
        ]
        l = [
            'ningún doble',
            'ningún doblete'
        ]
        i = 1
        if cant == 1:
            i = 0

        text = ''

        if cant == 0:
            return random.choice(l)
        else:
            text = str(cant) + ' ' + random.choice(comp)[i]

        return text

# Entity
class Triples(Entity):
    def get_text(self):
        cant = self._player_dict['Triple']
        comp = [
            ['triple', 'triples'],
            ['triplete', 'tripletes']
        ]
        l = [
            'ningún triple',
            'ningún triplete'
        ]
        i = 1
        if cant == 1:
            i = 0

        text = ''

        if cant == 0:
            return random.choice(l)
        else:
            text = str(cant) + ' ' + random.choice(comp)[i]

        return text

# Entity
class Home_Runs(Entity):
    def get_text(self):
        cant = self._player_dict['HR']
        comp = [
            ['jonrón', 'jonrones'],
            ['cuadrangular', 'cuadrangulares']
        ]
        l = [
            'ningún jonrón',
            'ningún cuadrangular'
        ]
        i = 1
        if cant == 1:
            i = 0

        text = ''

        if cant == 0:
            return random.choice(l)
        else:
            text = str(cant) + ' ' + random.choice(comp)[i]

        return text

# Action, Entity
class RBI(Action):
    def __init__(self, player_name, player_dict, condition='action'):
        super().__init__(player_name, player_dict, condition)

    def get_text(self):
        cant = self._player_dict['RBI']

        comp = [
            ['empujada', 'empujadas'],
            ['impulsada', 'impulsadas']
        ]
        l = [
            'ninguna carrera empujada',
            'ninguna carrera impulsada'
        ]
        i = 1
        if cant == 1:
            i = 0

        text = ''

        if self._condition == 'entity':
            if cant == 0:
                text = random.choice(l)
            else:
                text = str(cant) + ' ' + random.choice(comp)[i]

        else:
            if cant == 0:
                text = 'no impulsó carreras'
            else:
                i = 1
                if cant == 1:
                    i = 0
                comp_rbi = ['carrera', 'carreras']

                c = [
                    'empujó ' + str(cant) + ' ' + comp_rbi[i],
                    'impulsó ' + str(cant) + ' ' + comp_rbi[i]
                ]
                text = random.choice(c)

        return text


###########################################
################ PITCHERS #################
###########################################

# Complement
class IP(Entity):
    def get_text(self):
        ip = self._player_dict['IP']

        comp = [
            'entradas', 'innings'
        ]
        c = [
            ['lanzadas', 'de labor'],
            ['lanzados', 'de labor']
        ]

        text = 'en ' + ip + ' ' + random.choice(comp) + \
        ' ' + random.choice(random.choice(c))

        return text

# Action, Entity, NO
class ER(EntityCont):
    def get_text(self):
        return str(self._cont)

# Entity
class SO(Entity):
    def get_text(self):
        cant = self._player_dict['SO']
        comp = [
            ['ponche', 'ponches']
        ]
        i = 1
        if cant == 1:
            i = 0

        text = ''

        if cant == 0:
            return 'ningún ponche'
        else:
            text = str(cant) + ' ' + random.choice(comp)[i]

        return text

# Action
class Impact(Entity):
    def get_text(self):
        impact = self._player_dict['impact']

        text = ''

        if 'W' in impact:
            l = [
                'se apuntó la victoria',
                'fue el pitcher ganador'
            ]
            text = random.choice(l)

        elif 'S' in impact:
            l = [
                'se apuntó el salvamento',
                'salvó el juego para su equipo'
            ]

        return text

# Action
class Batters_faced(Entity):
    def get_text(self):
        cant = self._player_dict['batters_faced']

        a = [
            'enfrentó a',
            'lanzó contra',
            'hizo lanzamientos contra'
        ]

        b = ['bateador', 'bateadores']

        i = 1
        if cant == 1:
            i = 0

        text = random.choice(a) + ' ' + str(cant) + ' ' + b[i]

        return text

###########################################
############### HIGHLIGHTS ################
###########################################

class Highlights_Player(Highlights):
    def __init__(self, player_name, player_dict):
        super().__init__(player_name, player_dict)

    def get_dict_of_texts(self):
        name = self._player_name
        templates_stats = {}

        if self._player_dict['position'] == 'P':
            ip = self._player_dict['IP']
            h = self._player_dict['H']
            impact = self._player_dict['impact']
            r = self._player_dict['R']
            k = self._player_dict['SO']
            bb = self._player_dict['BB']

            if ip >= '6.0' and r <= 3:
                l = []
                ss = ['apertura', 'salida']
                l.append(name + ' tuvo  ' + random.choice(ss) +' de calidad')
                l.append(name + ' también tuvo '+ random.choice(ss) +' de calidad')
                l.append('otra '+ random.choice(ss) +' de calidad para ' + name)
                templates_stats['SC'] = l

            if impact == 'W':
                l = []

                f = [
                    ' se apuntó la victoria de su equipo',
                    ' ganó el juego',
                ]
                f1 = [
                    'victoria para ',
                    'juego ganado para '
                ]
                ff = [
                    name + random.choice(f),
                    random.choice + name
                ]

                s = ' también ganó el juego para su equipo'

                x = random.choice(ff)

                l.append(x)
                l.append(s)
                templates_stats['W'] = l

            if impact == 'SV':
                l = []

                f = [
                    ' se apuntó el salvamento para su equipo',
                    ' salvó el juego',
                ]
                f1 = [
                    'juego salvado para ',
                    'salvamento para '
                ]
                ff = [
                    name + random.choice(f),
                    random.choice + name
                ]

                s = ' también salvó el juego para su equipo'

                x = random.choice(ff)

                l.append(x)
                l.append(s)
                templates_stats['SV'] = l

            if r <= 3:
                l = []
                zero = [
                    name + ' no permitió ninguna anotación',
                    name + ' no recibió carreras'
                ]
                c = ['carrera', 'carreras']
                a = ['anotación', 'anotaciones']

                i = 1
                if r == 1:
                    i = 0

                l.append(name + ' permitió solamente ' + str(r) + ' ' + c[i])
                l.append(name + ' recibió solo ' + str(r) + ' ' + a[i])

                templates_stats['R'] = l

            if k >= 5:
                l = []

                l.append(name + ' ponchó a ' + str(k) + ' bateadores')
                l.append(name + ' propinó ' + str(k) + ' ponches')
                l.append('juego de ' + str(k) + ' ponches para ' + name)

                templates_stats['K'] = l

            if IP >= '9.0' and h == 0:
                l = []

                l.append(name + 'propinó no hit no run al rival')
                l.append('no hit no run también para ' + name)

                templates_stats['NHNR'] = l

        else:
            ab = self._player_dict['AB']
            h = self._player_dict['H']
            r = self._player_dict['R']
            rbi = self._player_dict['RBI']
            hr = self._player_dict['HR']
            double = self._player_dict['Double']
            triple = self._player_dict['Triple']

            if ab == h and h > 2:
                l = []

                l.append('juego perfecto para ' + name)
                l.append(name + ' tampoco falló al bate')

                templates_stats['PG'] = l

            if hr > 0:
                l = []

                if hr == 1:
                    l.append(name + ' pegó jonrón')
                    l.append('otro cuadrangular de ' + name)
                    l.append(name + ' también disparó jonrón')

                else:
                    l.append(name + ' pegó ' + str(hr) + ' jonrones')
                    l.append(' otros ' + str(hr) + ' jonrones de ' + name)
                    l.append(name + ' también pegó ' + str(hr) + ' jonrones')

                templates_stats['HR'] = l

            if rbi > 0:
                l = []

                a = ['carrera', 'carreras']
                b = ['anotación', 'anotaciones']

                i = 1
                if rbi == 1:
                    i = 0

                l.append(name + ' impulsó ' + str(rbi) + ' ' + a[i])
                l.append(name + ' también empujó ' + str(rbi) + ' ' + b[i])

                templates_stats['RBI'] = l

            if r > 0:
                l = []

                a = ['carrera', 'carreras']
                b = ['vez', 'veces']

                i = 1
                if rbi == 1:
                    i = 0

                l.append(name + ' anotó ' + str(rbi) + ' ' + a[i])
                l.append(name + ' también pisó ' + str(rbi) + b[i] + ' el home')

                templates_stats['R'] = l

            if h > 1:
                l = []

                l.append('multihits de ' + name)
                l.append(name + 'pegó ' + str(h) + ' hits')
                l.append('juego de ' + str(h) + ' indiscutibles para ' + name)

                templates_stats['H'] = l

            if double + triple + hr > 1:
                l = []

                eb = double + triple + hr

                l.append(name + ' disparó ' + str(eb) + ' extrabases')
                l.append('juego de ' + str(h) + ' extrabases para ' + name)

                templates_stats['EB'] = l
                
        return templates_stats
