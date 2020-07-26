import datetime

player_position = {
    '1B': ['el primera base', 'el inicialista'],
    '2B': ['el segunda base', 'el camarero'],
    'SS': ['el campo corto'],
    '3B': ['el tercera base', 'el antesalista'],
    'C' : ['el receptor', 'el catcher'],
    'LF': ['el jardinero izquierdo', 'el left fielder'],
    'CF': ['el jardinero central', 'el center fielder'],
    'RF': ['el jardinero derecho', 'el rigth fielder'],
    'P' : ['el lanzador', 'el pitcher'],
    'DH': ['el bateador designado', 'el designado']
}

ordinal = {
    1: ['primer', 'primera',],
    2: ['segundo', 'segunda'],
    3: ['tercer', 'tercera'],
    4: ['cuarto', 'cuarta'],
    5: ['quinto', 'quinta'],
    6: ['sexto', 'sexta'],
    7: ['séptimo', 'séptima'],
    8: ['octavo', 'octava'],
    9: ['noveno', 'novena'],
    10: ['décimo', 'décima'],
    11: ['onceno', 'oncena'],
    12: ['duodécimo', 'duodécima']
}

direction = {
    '1B': ['primera base', 'la inicial'],
    '2B': ['segunda base', 'la intermedia'],
    'SS': ['el campo corto'],
    '3B': ['tercera base', 'la antesala'],
    'LF': ['el jardín izquierdo', 'la pradera izquierda', 'el left field'],
    'CF': ['el jardín central', 'la pradera central', 'el center field'],
    'RF': ['el jardín derecho', 'la pradera derecha', 'el rigth field'],
    'C': ['el receptor', 'el catcher'],
    'P': ['el pitcher', 'el lanzador']
}

month = {
    1: 'enero',
    2: 'febrero',
    3: 'marzo',
    4: 'abril',
    5: 'mayo',
    6: 'junio',
    7: 'julio',
    8: 'agosto',
    9: 'septiembre',
    10: 'octubre',
    11: 'noviembre',
    12: 'diciembre'
}

def get_yesterday_date():
    today = datetime.date.today() 
    oneday = datetime.timedelta(days=1) 
    yesterday = today - oneday

    a = ['ro de ', ' de ']

    i = 1
    if yesterday.day == 1:
        i = 0

    return str(yesterday.day) + a[i] + month[yesterday.month]