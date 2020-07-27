from .base_class import Stats
from .utils import ordinal as uordinal, direction
from .utils import direction as udirection
import random

# Complement
class Inning(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

    def get_text(self):
        inning = self._play_dict['inning']
        i = inning[0]
        n = int(inning[1:])

        male = [
            'inning',
            'episodio',
            'capítulo'
        ]

        l = []

        if i == 't':
            l = [
                'en el ' + uordinal[n][0] + ' ' + random.choice(male),
                'en la ' + uordinal[n][1] + ' entrada',
                'en la parte alta del ' + uordinal[n][0] + ' ' + random.choice(male),
                'en la parte alta de la ' + uordinal[n][1] + ' entrada',
                'en el inicio del ' + uordinal[n][0] + ' ' + random.choice(male),
                'en el inicio de la ' + uordinal[n][1] + ' entrada'
            ]
        else:
            l = [
                'en el ' + uordinal[n][0] + ' ' + random.choice(male),
                'en la ' + uordinal[n][1] + ' entrada',
                'en la parte baja del ' + uordinal[n][0] + ' ' + random.choice(male),
                'en la parte baja de la ' + uordinal[n][1] + ' entrada',
                'en el final del ' + uordinal[n][0] + ' ' + random.choice(male),
                'en el final de la ' + uordinal[n][1] + ' entrada'
            ]

        return random.choice(l)

# Complement
class Current_Score(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

    def get_text(self):
        current_score = self._play_dict['current_score']
        current_rival_score = self._play_dict['current_rival_score']
        text = ''

        comp = [
            'cuando',
            'al momento en que',
        ]
        subject = [
            'su equipo',
            self._player_dict['team']
        ]
        win = [
            'vencía',
            'marchaba delante',
            'iba delante',
            'ganaba',
            'iba ganando',
            'iba venciendo'
        ]
        draw = [
            'iban empatados',
            'marchaban empatados',
            'iban igualados',
            'marchaban igualados',
            'empataban',
            'igualaban'
        ]
        draw_team = [
            'ambos equipos',
            'ambos conjuntos',
            'los dos equipos',
            'los dos conjuntos'
        ]
        lose = [
            'perdía',
            'caía derrotado',
            'iba siendo derrotado',
            'marchaba debajo'
        ]

        if current_score > current_rival_score:
            text = random.choice(comp) + ' ' + \
            random.choice(subject) + ' ' + \
            random.choice(win) + ' ' + \
            str(current_score) + \
            ' a ' + str(current_rival_score)

        elif current_score < current_rival_score:
            text = random.choice(comp) + ' ' + \
            random.choice(subject) + ' ' + \
            random.choice(lose) + ' ' + \
            str(current_rival_score) + \
            ' a ' + str(current_score)

        else:
            text = random.choice(comp) + ' ' + \
            random.choice(draw_team) + ' ' + \
            random.choice(draw) + \
            ' a ' + str(current_score)

        return text

# Complement
class Outs(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

    def get_text(self):
        o = ['outs', 'out']
        comp = ['', 'en el pizarrón', 'en la pizarra']
        i = 0
        if self._play_dict['outs'] == 1:
            i = 1
        if self._play_dict['outs'] == 0:
            text = 'sin outs ' + random.choice(comp)
            return text
        text = 'con ' + str(self._play_dict['outs']) + ' ' + \
        o[i] + ' ' + random.choice(comp)
        return text

# Complement
class ROB(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

    def get_text(self):
        rob = self._play_dict['runners_on_bases_pbp']
        l = []
        if rob[0] == '-' and rob[1] == '-' and rob[2] == '-':
            l = [
                'con las bases limpias',
                'sin corredores en base'
            ]

        elif rob[0] == '1' and rob[1] == '-' and rob[2] == '-':
            l = [
                'con corredor en primera base',
                'con corredor en la inicial'
            ]

        elif rob[0] == '-' and rob[1] == '2' and rob[2] == '-':
            l = [
                'con corredor en segunda base',
                'con corredor en la intermedia',
                'con un corredor en posición anotadora',
                'con un corredor a 180 pies del home'
            ]

        elif rob[0] == '-' and rob[1] == '-' and rob[2] == '3':
            l = [
                'con corredor en tercera base',
                'con corredor en la antesala',
                'con un corredor en posición anotadora',
                'con un corredor a 90 pies del home'
            ]

        elif rob[0] == '1' and rob[1] == '2' and rob[2] == '-':
            l = [
                'con corredores en primera y segunda',
                'teniendo solamente la tercera desocupada'
            ]

        elif rob[0] == '1' and rob[1] == '-' and rob[2] == '3':
            l = [
                'con corredores en primera y tercera',
                'con corredores en las esquinas',
                'con solamente la segunda desocupada'
            ]

        elif rob[0] == '-' and rob[1] == '2' and rob[2] == '3':
            l = [
                'con corredores en segunda y tercera',
                'con solamente la primera desocupada',
                'con dos corredores en posición anotadora'
            ]

        else:
            l = [
                'con las bases llenas',
                'con la casa llena'
            ]

        return random.choice(l)

# Reaction
class Runs_Play_Result(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

    def get_text(self):
        runs_play_result = self._play_dict['runs_outs_result'].count('R')
        current_score = self._play_dict['current_score']
        current_rival_score = self._play_dict['current_rival_score']
        team = self._player_dict['team']
        rival_team = self._player_dict['rival_team']
        t = [team, 'su equipo']
        rt = [rival_team, 'el equipo contrario']

        text = ''
        comp = [
            'el marcador',
            'la pizarra',
            'el resultado'
        ]

        runs = ['carreras', 'carrera']

        if self._player_dict['position'] == 'P':
            result_rival_score = current_rival_score + runs_play_result

            if result_rival_score > current_score:
                l = [
                    'no despegar a ' + random.choice(t) + ' de ' + \
                    random.choice(comp),
                    'mantener cerca a ' + random.choice(t) + ' en ' + \
                    random.choice(comp),
                    'no permitir que ' + random.choice(rt) + ' se alejara en ' + \
                    random.choice(comp),
                    'no dejar que ' + random.choice(rt) + ' tomara mayor ventaja en '\
                    + random.choice(comp)
                ]
                text = random.choice(l)

            elif result_rival_score == current_score:
                action = [
                    'tomara ventaja',
                    'se adelantara'
                ]
                same = [
                    'el empate',
                    'el abrazo',
                    'la igualada'
                ]
                l = [
                    'no permitir que ' + random.choice(rt) + ' ' + \
                    random.choice(action),
                    'mantener ' + random.choice(same) + ' en ' + \
                    random.choice(comp)
                ]
                text = random.choice(l)

            else:
                f = [
                    'delante',
                    'al frente',
                    'ganando'
                ]
                l = [
                    'mantener a ' + random.choice(t) + ' ' + \
                    random.choice(f),
                    'permitir que ' + random.choice(t) + ' siguiera ' + \
                    random.choice(f)
                ]
                text = random.choice(l)

        else:
            result_score = current_score + runs_play_result

            if runs_play_result == 0:
                return 'mantener viva la entrada y colocar corredores en circulación'

            if result_score < current_rival_score:
                f = [
                    'favorable a',
                    'a favor de'
                ]
                l = [
                    'acercar a' + random.choice(t) + ' en ' + \
                    random.choice(comp) + ' ' + str(result_score) + \
                    ' a ' + str(current_rival_score),
                    'poner el juego ' + str(result_score) + ' a ' + \
                    str(current_rival_score) + ' ' + random.choice(f) + ' ' + \
                    random.choice(rt)
                ]

                text = random.choice(l)

            elif result_score == current_rival_score:
                act = [
                    'empatar',
                    'igualar'
                ]
                subj = [
                    'el juego',
                    'el encuentro'
                ]
                text = random.choice(act) + ' ' + \
                random.choice(subj) + ' a ' + str(result_score)

            elif current_score <= current_rival_score:
                act = [
                    'adelantar a',
                    'poner delante a',
                    'poner a ganar a'
                ]
                text = random.choice(act) + ' ' + \
                random.choice(t) + ' ' + str(result_score) + ' a ' + \
                str(current_rival_score)

            else:
                x = result_score - current_rival_score
                i = 0
                if x == 1:
                    i = 1
                text = 'aumentar la ventaja de ' + random.choice(t) + ' ' + \
                'en ' + str(x) + ' ' + runs[i]

        return text

# Reaction
class Out_Play_Results(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

    def get_text(self):
        current_outs = self._play_dict['outs']
        outs_play = self._play_dict['runs_outs_result'].count('O')
        outs_results = current_outs + outs_play

        l = []

        if outs_results == 2:
            l = [
                'meter la entrada en 2 outs',
                'casi liquidar la entrada'
            ]

        elif outs_results == 3:
            l = [
                'liquidar la entrada',
                'retirar el inning',
                'liquidar el inning',
                'retirar la entrada',
                'lograr sacar el 3er out de la entrada'
            ]

        if len(l) == 0:
            return ''

        else:
            return random.choice(l)

# NO
class Current_Batter(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

# Complement
class Current_Pitcher(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

    def get_text(self):
        current_pitcher = self._play_dict['pitcher']

        comp = ['frente a', 'contra', 'enfrentando']
        pitches = ['los lanzamientos', 'los envíos', 'los lances']

        text = random.choice(comp) + ' ' + \
        random.choice(pitches) + ' de ' + current_pitcher

        return text

# NO
class WPA(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

# Action, present always
class Event(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)
        self._player_dict = player_dict

    def get_text(self):
        event = self._play_dict['play_desc']['event']

        batter = self._play_dict['batter']

        text = ''

        hit = [
            'conectó',
            'disparó',
            'dió'
        ]

        if event == 'Single':
            e = [
                'hit',
                'imparable',
                'indiscutible',
            ]
            text = random.choice(hit) + ' un ' + \
            random.choice(e)

        elif event == 'Double':
            e = [
                'doble',
                'doblete',
                'biangular'
            ]
            text = random.choice(hit) + ' un ' + \
            random.choice(e)

        elif event == 'Triple':
            e = [
                'triple',
                'triplete'
            ]
            text = random.choice(hit) + ' un ' + \
            random.choice(e)

        elif event == 'Home Run':
            e = [
                'home run',
                'cuadrangular',
                'batazo de vuelta completa'
            ]
            text = random.choice(hit) + ' un ' + \
            random.choice(e)

        elif event == 'Walk':
            e = [
                'recibió'
            ]
            ee = [
                'la base por bolas',
                'un boleto',
                'cuatro lanzamientos malos'
            ]
            text = random.choice(e) + ' ' + \
            random.choice(ee)

        elif event == 'Groundout':
            intro = [
                'provocó que ' + batter + ' fallara',
                'hizo fallar a ' + batter,
                'dominó a ' + batter,
                'eliminó a ' + batter
            ]
            act = [
                'un roletazo de out',
                'un rolling de out',
                'rolling de out',
                'roletazo de out'
            ]
            text = random.choice(intro) + ' con ' + \
            random.choice(act)

        elif 'Double Play' in event:
            l = [
                'hizo batear a ' + batter + ' para doble play',
                'sacó dos outs de un solo golpe con un rolling de ' + batter,
                'provocó una jugada de doble matanza con un rolling de ' + batter,
            ]
            text = random.choice(l)

        elif event == 'Strikeout':
            l = [
                'ponchó a ' + batter,
                'eliminó por la vía del ponche a ' + batter,
                'dominó por la vía de los strikes a ' + batter,
                'propinó tres strikes a ' + batter
            ]
            text = random.choice(l)

        elif 'Flyball' in event and self._player_dict['position'] == 'P':
            intro = [
                'provocó que ' + batter + ' fallara',
                'hizo fallar a ' + batter,
                'dominó a ' + batter,
                'eliminó a ' + batter
            ]
            act = [
                'un fly de out',
                'un elevado de out',
                'fly de out',
                'elevado de out'
            ]
            text = random.choice(intro) + ' con ' + \
            random.choice(act)

        elif 'Sacrifice' in event and self._player_dict['position'] != 'P':
            text = 'elevó un fly de sacrificio'

        elif event == 'Lineout':
            intro = [
                'provocó que ' + batter + ' fallara',
                'hizo fallar a ' + batter,
                'dominó a ' + batter,
                'eliminó a ' + batter
            ]
            act = [
                'una línea de out',
                'línea de out'
            ]
            text = random.choice(intro) + ' con ' + \
            random.choice(act)

        elif event == 'Popfly':
            intro = [
                'provocó que ' + batter + ' fallara',
                'hizo fallar a ' + batter,
                'dominó a ' + batter,
                'eliminó a ' + batter
            ]
            act = [
                'un elevado corto de out',
                'un globito de out',
                'elevado corto de out',
            ]
            text = random.choice(intro) + ' con ' + \
            random.choice(act)

        return text

# Complement (only after Event)
class Direction(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

    def get_text(self):
        if self._play_dict['play_desc']['direction'] == '':
            return ''
        l = ['hacia', 'a', 'con dirección a', 'dirigido hacia']
        direction = self._play_dict['play_desc']['direction'].split('-')[0]
        t = udirection[direction]
        text = random.choice(l) + ' ' + random.choice(t)

        return text

# Reaction,
# TODO: no se si sea necesario todavia
class On_Base_Result(Stats):
    def __init__(self, player_name, player_dict, play_dict):
        super().__init__(player_name, player_dict, play_dict)

# Action, Reaction (only batter)
class RBI_Result(Stats):
    def __init__(self, player_name, player_dict, play_dict, act_or_react):
        super().__init__(player_name, player_dict, play_dict)
        self._act_or_react = act_or_react

    def get_text(self):
        rbi = self._play_dict['play_desc']['RBI']
        total_runs = self._play_dict['runs_outs_result'].count('R')
        text = ''
        runs = [
            ['carrera', 'anotación'],
            ['carreras', 'anotaciones']
        ]
        i = 0
        if rbi > 1:
            i = 1

        if rbi == 0:
            return ''

        if self._act_or_react == 'action':
            action = [
                'empujó',
                'impulsó'
            ]

            text = random.choice(action) + ' ' + \
            str(rbi) + ' ' + random.choice(runs[i])

            if total_runs > rbi:
                text += ' y provocó que anotaran ' + str(total_runs - rbi) + ' más'

        else:
            action = [
                'empujar',
                'impulsar'
            ]
            text = random.choice(action) + ' ' + \
            str(rbi) + ' ' + random.choice(runs[i])

        return text
