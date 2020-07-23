from bs4 import BeautifulSoup
from bs4 import Comment
import requests
#import dryscrape
import json

with open('../cubans.json', 'r') as json_data:
    cubans_players = json.load(json_data)
    json_data.close()

players_details = {}
players_details['hitters'] = {}
players_details['pitchers'] = {}

###############################################
############# INITIAL SCRAPPING ###############
###############################################

def get_links_games(session, base_url):
    games_links = []

    print("visiting games links...")
    r = session.get(base_url+"/boxes/?month=5&day=27&year=2019")
    print("visited")

    bsObj = BeautifulSoup(r.text, 'lxml')

    games_refs = bsObj.findAll('td', {'class': 'right gamelink'})

    for l in games_refs[1:]:
        games_links.append(l.a['href'])

    return games_links

def get_game_score(bsObj):

    game_details = {}

    scorebox = bsObj.find('div', {'class': 'scorebox'})

    names_teams = scorebox.findAll('strong')[:2]

    away = names_teams[0].a.get_text()
    home = names_teams[1].a.get_text()

    game_details[away] = {}
    game_details[home] = {}

    scores = scorebox.findAll('div', {'class': 'score'})

    game_details[away]['score'] = int(scores[0].get_text())
    game_details[home]['score'] = int(scores[1].get_text())

    divs = scorebox.findAll('div')

    game_details[away]['season_score'] = divs[5].get_text()
    game_details[home]['season_score'] = divs[12].get_text()

    return game_details

def get_cubans_players(game_bsObj, game_details):

    away_team = list(game_details.keys())[0]
    home_team = list(game_details.keys())[1]

    away_team = away_team.replace('.', '').replace(' ', '')
    home_team = home_team.replace('.', '').replace(' ', '')

    players = {}
    #away team players
    _get_hitters(away_team, game_bsObj, players, game_details)
    _get_pitchers(away_team, game_bsObj, players, game_details)

    #home team players
    _get_hitters(home_team, game_bsObj, players, game_details)
    _get_pitchers(home_team, game_bsObj, players, game_details)
    #print(players_details)
    _get_plays(players, game_bsObj)

def _get_hitters(name_team, game_bsObj, players_p, game_details):
    comments = game_bsObj.find_all(string=lambda text: isinstance(text, Comment))
    for i in comments:
        bs = BeautifulSoup(i, 'lxml')
        players = bs.find('table', {'id': name_team + 'batting'})
        if players is not None:
            players = players.tbody.findAll('tr')
            break

    for p in players:
        position = p.find('th')
        link = position.find('a')
        if link is None:
            continue
        name = link.get_text()
        name_and_pos = position.get_text().lstrip()
        pos = name_and_pos.replace(name, '').lstrip()
        if pos == 'P':
            continue
        name = link.get_text()
        if name not in cubans_players:
            continue
        if name in players_details.keys():
            name = name + '_2'
        players_p[name] = 'batter'
        players_details['hitters'][name] = {}
        players_details['hitters'][name]['position'] = pos
        players_details['hitters'][name]['plays'] = []
        players_details['hitters'][name]['game_details'] = game_details
        stats = p.findAll('td')
        for s in stats:
            k = s['data-stat']
            v = s.get_text()
            players_details['hitters'][name][k] = v

def _get_pitchers(name_team, game_bsObj, players_p, game_details):
    comments = game_bsObj.find_all(string=lambda text: isinstance(text, Comment))
    for i in comments:
        bs = BeautifulSoup(i, 'lxml')
        players = bs.find('table', {'id': name_team + 'pitching'})
        if players is not None:
            players = players.tbody.findAll('tr')
            break

    for p in players:
        position = p.find('th')
        link = position.find('a')
        if link is None:
            continue
        name_and_impact = position.get_text().lstrip()
        name = link.get_text()
        impact = name_and_impact.replace(name, '')
        if name not in cubans_players:
            continue
        if name in players_details.keys():
            name = name + '_2'
        players_p[name] = 'pitcher'
        players_details['pitchers'][name] = {}
        players_details['pitchers'][name]['position'] = 'P'
        players_details['pitchers'][name]['impact'] = impact
        players_details['pitchers'][name]['plays'] = []
        players_details['pitchers'][name]['game_details'] = game_details
        stats = p.findAll('td')
        for s in stats:
            k = s['data-stat']
            v = s.get_text()
            players_details['pitchers'][name][k] = v

def _get_plays(players, game_bsObj):
    comments = game_bsObj.find_all(string=lambda text: isinstance(text, Comment))
    for i in comments:
        bs = BeautifulSoup(i, 'lxml')
        plays = bs.find('table', {'id': 'play_by_play'})
        if plays is not None:
            plays = plays.tbody.findAll('tr')
            break

    for p in plays:
        if not p.has_attr('id'):
            continue
        details = {}
        play_details = p.findAll('td')
        details['inning'] = p.find('th').get_text()
        for pd in play_details:
            details[pd['data-stat']] = pd.get_text()
        details['batter'] = details['batter'].replace('\xa0', ' ')
        details['pitcher'] = details['pitcher'].replace('\xa0', ' ')
        batter = details['batter']
        pitcher = details['pitcher']
        if batter in players and players[batter] == 'batter':
            players_details['hitters'][batter]['plays'].append( details )
        if pitcher in players and players[pitcher] == 'pitcher':
            players_details['pitchers'][pitcher]['plays'].append( details )

###############################################
################ DEVELOPMENT ##################
###############################################

def _get_team_and_rival(player, player_details):
    play_1 = player_details['plays'][0]
    top_or_bottom = play_1['inning'][0]
    batter = play_1['batter']
    pitcher = play_1['pitcher']
    teams = list(player_details['game_details'].keys())
    if batter == player and top_or_bottom == 't':
        return (teams[0], teams[1])
    elif pitcher == player and top_or_bottom == 'b':
        return (teams[0], teams[1])
    return (teams[1], teams[0])

def _win_or_lose(player_details):
    teams = list(player_details['game_details'].keys())
    away_score = player_details['game_details'][teams[0]]['score']
    home_score = player_details['game_details'][teams[1]]['score']
    if teams[0] == player_details['team'] and away_score > home_score:
        return 'win'
    elif teams[1] == player_details['team'] and home_score > away_score:
        return 'win'
    return 'lose'

def _get_current_score_team(player_details, play_dict):
    scores = play_dict['score_batting_team'].split('-')
    if player_details['position'] == 'P':
        return (int(scores[1]), int(scores[0]))
    return (int(scores[0]), int(scores[1]))

def _get_runs_outs_result(play_dict):
    result = play_dict['runs_outs_result']
    return ( result.count('R'), result.count('O') )

def _get_on_base_result(play_dict):
    x = play_dict['play_desc']['on_bases']['1B']
    y = play_dict['play_desc']['on_bases']['2B']
    z = play_dict['play_desc']['on_bases']['3B']
    return (x, y, z)

def _get_real_wpa(player_details, play_dict):
    w = play_dict['win_probability_added'].replace('%', '')
    wpa = int(w)
    wl = _win_or_lose(player_details)
    if wl == 'win':
        return wpa
    return -wpa

def _get_extra_bases(player_details):
    double = 0
    triple = 0
    home_run = 0
    plays = player_details['plays']
    for p in plays:
        if p['play_desc']['event'] == 'Double':
            double += 1
        elif p['play_desc']['event'] == 'Triple':
            triple += 1
        elif p['play_desc']['event'] == 'Home Run':
            home_run += 1
    return (double, triple, home_run)

def get_play_description(play):
    play_details = {}
    play_details['event'] = ''
    play_details['direction'] = ''
    direction_details = ''
    play_and_runnbases = play.split(';')
    event = play_and_runnbases[0]
    play_details['on_bases'] = {'1B': False, '2B': False, '3B': False}
    play_details['RBI'] = 0

    d = {
        'Single': '1B',
        'Double': '2B',
        'Triple': '3B',
        'Walk': '1B'
    }

    if 'Walk' in event:
        play_details['on_bases']['1B'] = True

    if 'Single to' in event or 'Double to' in event or 'Triple to' in event or 'Home Run' in event:
        event_splitted = event.split()
        if event_splitted[0] == 'Home':
            play_details['event'] = 'Home Run'
            play_details['RBI'] += 1
        else:
            play_details['on_bases'][d[event_splitted[0]]] = True
            play_details['event'] = event_splitted[0]
            direction_details = event_splitted[2]

    elif ':' in event:
        event_splitted = event.split(':')
        play_details['event'] = event_splitted[0]
        direction_details = event_splitted[1].lstrip().split('(')[0].split()[0].split('/')[0]


    elif 'Walk' in event or 'Strikeout' in event:
        cur = event.split()
        play_details['event'] = cur[0]

    else:
        play_details['event'] = 'DISCARD'


    #print(direction_details)
    for adv in play_and_runnbases[1:]:
        details = adv.split()
        if ' to ' in adv:
            play_details['on_bases'][details[2]] = True
        else:
            if 'No RBI' not in adv:
                play_details['RBI'] += 1

    play_details['direction'] = direction_details

    return play_details

def convert_player(player, player_details):

    if not 'position' in player_details:
        player_details['position'] = 'P'

    player_details['team'], player_details['rival_team'] = _get_team_and_rival(player, player_details)
    player_details['result'] = _win_or_lose(player_details)

    score_team = int(player_details['game_details'][player_details['team']]['score'])
    player_details['game_details'][player_details['team']]['score'] = score_team
    score_rival_team = int(player_details['game_details'][player_details['rival_team']]['score'])
    player_details['game_details'][player_details['rival_team']]['score'] = score_rival_team

    plays = player_details['plays']
    for p in plays:
        p['current_score'], p['current_rival_score'] = _get_current_score_team(player_details, p)
        p['outs'] = int(p['outs'])
        p['runs_play_result'], p['outs_play_result'] = _get_runs_outs_result(p)
        p['wpa'] = _get_real_wpa(player_details, p)
        p['on_base_result'] = _get_on_base_result(p)

def convert_hitter(player, player_details):
    player_details['AB'] = int(player_details['AB'])
    player_details['H'] = int(player_details['H'])
    player_details['R'] = int(player_details['R'])
    player_details['RBI'] = int(player_details['RBI'])
    player_details['BB'] = int(player_details['BB'])
    player_details['SO'] = int(player_details['SO'])
    x, y, z = _get_extra_bases(player_details)
    player_details['Double'], player_details['Triple'], player_details['HR'] = (x, y, z)

def convert_pitcher(player, player_details):
    player_details['IP'] = player_details['IP'].strip()
    player_details['H'] = int(player_details['H'])
    player_details['R'] = int(player_details['R'])
    player_details['ER'] = int(player_details['ER'])
    player_details['BB'] = int(player_details['BB'])
    player_details['SO'] = int(player_details['SO'])
    player_details['batters_faced'] = int(player_details['batters_faced'])

###############################################
################### FLOW ######################
###############################################

def flow():
    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Safari/537.36'
    base_url = 'https://www.baseball-reference.com'

    games_links = get_links_games(session, base_url)

    cont = 1

    for l in games_links:
        print('visiting game', cont)
        r = session.get(base_url+l)
        bsObj = BeautifulSoup(r.text, 'lxml')
        game_details = get_game_score(bsObj)
        get_cubans_players(bsObj, game_details)
        cont += 1

    for player in players_details['hitters']:
        for play in players_details['hitters'][player]['plays']:
            play_desc = get_play_description(play['play_desc'])
            play['play_desc'] = play_desc
            #print(play['play_desc'], get_play_description(play['play_desc']))

    for player in players_details['pitchers']:
        for play in players_details['pitchers'][player]['plays']:
            play_desc = get_play_description(play['play_desc'])
            play['play_desc'] = play_desc
            #print(play['play_desc'], get_play_description(play['play_desc']))

    hitters = list(players_details['hitters'].keys())
    pitchers = list(players_details['pitchers'].keys())

    #x = players_details['hitters'][hitters[1]]
    #y = players_details['pitchers'][pitchers[0]]
    #print(json.dumps(x, indent=4))
    #print(json.dumps(y, indent=4))

    for h in hitters:
        pd = players_details['hitters'][h]
        convert_player(h, pd)
        convert_hitter(h, pd)

    for p in pitchers:
        pd = players_details['pitchers'][p]
        convert_player(p, pd)
        convert_pitcher(p, pd)


    with open('game_day_data_1.json', 'w') as json_data:
        json.dump(players_details, json_data)
        json_data.close()

#flow()
