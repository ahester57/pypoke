# Austin Hester
# 12/24/17
# veekun pokemon db handler
from pokedex.db import connect, tables, util

session = connect()
# begin getting

# Get Pokemon by name
def get_by_name (name):
    query = session.query(tables.PokemonSpecies)
    query = query.filter(tables.PokemonSpecies.identifier==name)
    try:
        poke = query[0]
    except IndexError:
        poke = None
    return poke

# Get pokemon by Id
def get_by_id (poke_id):
    query = session.query(tables.PokemonSpecies)
    query = query.filter(tables.PokemonSpecies.id==poke_id)
    try:
        poke = query[0]
    except IndexError:
        poke = None
    return poke

# Get Pokemon forms
def get_forms (poke_id):
	query = session.query(tables.Pokemon)
	query = query.filter(tables.Pokemon.species_id==poke_id)
	forms = []
	try:
		for q in query:
			forms.append(q.id)
	except IndexError:
		pass
	return forms

# Get Evolution Poke IDs
def get_evolution_to (poke_id):
    filt = tables.PokemonSpecies
    query = session.query(filt)
    query = query.filter(filt.evolves_from_species_id==poke_id)
    evolves_to = []
    try:
        for q in query:
            to = q
            evolves_to.append(to.id)
    except:
        evolves_to = None
    return evolves_to 

# Get Evolution Poke IDs
def get_evolution_from (poke_id):
    query = session.query(tables.PokemonSpecies)
    #try:
    fromq = query.filter(tables.PokemonSpecies.id==poke_id)
    chain_id = 0
    try:
        fromm = fromq[0]	
        evolves_from = fromm.evolves_from_species_id
    except IndexError:
        evolves_from = None
    return evolves_from

# Get how they evolve. Warning: long
def get_evolution_trigger (poke_id):
    query = session.query(tables.PokemonEvolution)
    query = query.filter(tables.PokemonEvolution.evolved_species_id==poke_id)
    methods = []
    for q in query:
        try:
            trigger = q.evolution_trigger_id
        except IndexError:
            trigger = None

        if (trigger == 1):
            # level-up
            method = get_evolution_level (poke_id) 
        elif (trigger == 2):
            # trade
            method = 'trade'
            try:
                trade_species = q.trade_species_id
            except IndexError:
                trade_species = None

            if (trade_species != None):
                trade_species = get_by_id (trade_species)
                method = ("%s for a %s" % (method, trade_species.identifier)) 

        elif (trigger == 3):
            # use-item
            try:
                method = q.trigger_item_id
                method = ("use %s" % get_item_name (method))
            except IndexError:
                method = None

        elif (trigger == 4):
            # shed
            method = 'shed, have empty slot in party'

        try:
            time = q.time_of_day
            happiness = q.minimum_happiness
            held_item = q.held_item_id
            location = q.location_id
            sex = q.gender_id
            party_type = q.party_type_id
            party_species = q.party_species_id
            move_type = q.known_move_type_id
            upside_down = q.turn_upside_down
            rain = q.needs_overworld_rain
            beauty = q.minimum_beauty
            affection = q.minimum_affection
        except IndexError:
            time = None
            happiness = None
            held_item = None
            sex = None
            party_type = None
            party_species = None
            move_type = None
            upside_down = None
            rain = None
            beauty = None
            affection = None
        
        if (method == None):
            method = ''
        if (happiness != None):
            method = ("%s %d friendship" % (method, happiness))
        if (held_item != None):
            item = get_item_name (held_item)
            method = ("%s & hold %s" % (method, item))
        if (location != None):
            method = ("%s in %s" % (method, get_location_name (location)))
        if (party_type != None):
            p_type = get_type_name ([party_type])
            method = ("%s with %s type in party" % (method, p_type))
        if (party_species != None):
            p_species = get_by_id (party_species)
            method = ("%s with %s in party" % (method, p_species.identifier))
        if (move_type != None):
            m_type = get_type_name ([move_type])
            method = ("%s with a %s type move" % (method, m_type))
        if (upside_down == 1):
            method = ("%s while upside-down" % method)
        if (rain == 1):
            method = ("%s while raining" % method)
        if (beauty != None):
            method = ("%s %d beauty" % (method, beauty))
        if (affection != None):
            method = ("%s %d affection" % (method, affection))
        if (sex != None):
            if (sex == 1):
                sex = 'female'
            elif (sex == 2):
                sex = 'male'
            method = ("%s, %s only" % (method, sex))
        if (time != None):
            method = ("%s @ %s" % (method, time))
        methods.append(method)
    return methods

# Get the level or move they must be to 'volve
def get_evolution_level (poke_id):
    query = session.query(tables.PokemonEvolution)
    query = query.filter(tables.PokemonEvolution.evolved_species_id==poke_id)
    try:
        level = query[0].minimum_level
    except IndexError:
        level = None
    if (level == None):
        try:
            level = query[0].known_move_id
            if (level != None):
                level = ("know %s" % get_move_name (level))
        except IndexError:
            level = None
    return level

# Get item name by item_id
def get_item_name (item_id):
    query = session.query(tables.Item)
    query = query.filter(tables.Item.id==item_id)
    try:
        item = query[0].identifier
    except IndexError:
        item = None
    return item

# Get region location name
def get_location_name (loc_id):
    query = session.query(tables.Location)
    query = query.filter(tables.Location.id==loc_id)
    try:
        location = query[0].identifier
    except IndexError:
        location = None
    return location 

# Get name of move given by id
def get_move_name (move_id):
    query = session.query(tables.Move)
    query = query.filter(tables.Move.id==move_id)
    try:
        move = query[0].identifier
    except IndexError:
        move = None
    return move

# Get the moves a pokemon can learnn
def get_moves (poke_id):
    query = session.query(tables.PokemonMove).order_by(tables.PokemonMove.level)
    query = query.filter(tables.PokemonMove.pokemon_id==poke_id)
    query = query.filter(tables.PokemonMove.version_group_id==18)
    moves = []
    for m in query:
        moves.append(m)
    return moves

# Get type name
def get_type_name (types):
    query = session.query(tables.Type)
    l = []
    for t in types:
        tmp = query.filter(tables.Type.id == t)
        l.append(tmp[0].identifier.encode('utf-8').upper())	
    if (len(l) > 1):
        l = '/'.join(l)
    else:
        l = l[0]
    return l

# Get type_id
def get_type (poke_id):
    query = session.query(tables.PokemonType)
    query = query.filter(tables.PokemonType.pokemon_id==poke_id)
    types = []
    for t in query:
        types.append(t.type_id)
    return types	
	
# Get abilities
def get_abilities (poke_id):
    query = session.query(tables.PokemonAbility)
    abilities = query.filter(tables.PokemonAbility.pokemon_id==poke_id)
    ab_ids = []
    for a in abilities:
        ab_ids.append([a.ability_id, a.is_hidden])
    return ab_ids

# Get ability name, description from id
def get_ability_info (ability_id):
    query = session.query(tables.Ability)
    query = query.filter(tables.Ability.id==ability_id)
    name = query[0].identifier
    query = session.query(tables.Ability)
    query = query.filter(tables.Ability.id==ability_id)
    desc = query[0].short_effect
    return name, desc

# Get stats
def get_stats (poke_id):
    query = session.query(tables.PokemonStat)
    query = query.filter(tables.PokemonStat.pokemon_id==poke_id)
    stats = []
    for s in query:
        stats.append([s.stat_id, s.base_stat, s.effort])
    return stats

# Get E.V.s
def get_evs (stats):
    evs = []
    for s in stats:
        if (s[2] != 0):
            evs.append([stat_id_to_name(s[0]), s[2]])
    return evs

def get_egg_groups (poke_id):
	query = session.query(tables.PokemonEggGroup)
	query = query.filter(tables.PokemonEggGroup.species_id==poke_id)
	groups = []
	return groups

# Get natures
def get_natures ():
    query = session.query(tables.Nature)
    a = stat_name_to_id (u'attack')
    atk = query.filter(tables.Nature.increased_stat_id==a)
    attack = ["Attack"]
    for i in atk:
        lower = stat_id_to_name (i.decreased_stat_id)
        attack.append([i.identifier, lower])
    d = stat_name_to_id (u'defense')
    deff = query.filter(tables.Nature.increased_stat_id==d)
    defense = ["Defense"]
    for i in deff:
        lower = stat_id_to_name (i.decreased_stat_id)
        defense.append([i.identifier, lower])
    sa = stat_name_to_id (u'special-attack')
    spatk = query.filter(tables.Nature.increased_stat_id==sa)
    spattack = ["Special Attack"]
    for i in spatk:
        lower = stat_id_to_name (i.decreased_stat_id)
        spattack.append([i.identifier, lower])
    sd = stat_name_to_id (u'special-defense')
    spdef = query.filter(tables.Nature.increased_stat_id==sd)
    spdefense = ["Special Defense"]
    for i in spdef:
        lower = stat_id_to_name (i.decreased_stat_id)
        spdefense.append([i.identifier, lower])
    spd = stat_name_to_id (u'speed')
    sped = query.filter(tables.Nature.increased_stat_id==spd)
    speed = ["Speed"]
    for i in sped:
        lower = stat_id_to_name (i.decreased_stat_id)
        speed.append([i.identifier, lower])
    return attack, defense, spattack, spdefense, speed

# Get characteristics
def get_characteristics ():
    query = session.query(tables.Characteristic)
    # hp
    h = stat_name_to_id (u'hp')
    text = filter_characteristics (query, h) 
    hp = ["HP"]
    for t in text:
            hp.append(t.message)
    # atk
    a = stat_name_to_id (u'attack')
    text = filter_characteristics (query, a) 
    attack = ["Attack"]
    for t in text:
            attack.append(t.message)
    # def
    d = stat_name_to_id (u'defense')
    text = filter_characteristics (query, d) 
    defense = ["Defense"]
    for t in text:
            defense.append(t.message)
    # spatk
    spa = stat_name_to_id (u'special-attack')
    text = filter_characteristics (query, spa) 
    spatk = ["SpAtk"]
    for t in text:
            spatk.append(t.message)
    # spdef
    spdf = stat_name_to_id (u'special-defense')
    text = filter_characteristics (query, spdf) 
    spdef = ["SpDef"]
    for t in text:
            spdef.append(t.message)
    # speed
    spd = stat_name_to_id (u'speed')
    text = filter_characteristics (query, spd) 
    speed = ["Speed"]
    for t in text:
            speed.append(t.message)

    return hp, attack, defense, spatk, spdef, speed

# I only want English {u'en'}
def filter_characteristics (query, stat_id):
    lang = get_language_id (u'en')
    filt = query.filter(tables.Characteristic.stat_id==stat_id)
    filt = filt.filter(tables.Language.id==lang)
    return filt
	
# Get all pokemon that give a certain effort value
def get_poke_by_ev (stat):
    stat_id = stat_name_to_id(stat)
    print stat_id, stat
    pokes = []
    query = session.query(tables.PokemonStat)
    query = query.filter(tables.PokemonStat.stat_id==stat_id)
    for p in query:
        if (p.effort != 0):
            try:
                name = get_by_id (p.pokemon_id).identifier
                pokes.append(name)
            except AttributeError:
                pass
    return pokes

# Get growth rate
def get_growth_rate (growth_rate_id):
    query = session.query(tables.GrowthRate)
    query = query.filter(tables.GrowthRate.id==growth_rate_id)
    try:
        return query[0].identifier
    except IndexError:
        return None

# stat_id to stat name
def stat_id_to_name (stat_id):
    query = session.query(tables.Stat)
    query = query.filter(tables.Stat.id==stat_id)
    try:
        stat = query[0].identifier	
    except IndexError:
        stat = None
    return stat

# stat name to stat_id
def stat_name_to_id (stat):
    query = session.query(tables.Stat)
    query = query.filter(tables.Stat.identifier==stat)
    try:
        stat_id = query[0].id	
    except IndexError:
        stat_id = None
    return stat_id

# Get language id, e.g. get_language_id (u'en')
def get_language_id (lang):
    query = session.query(tables.Language)
    lang_id = query.filter(tables.Language.iso639==lang)
    try:
        lang_id = lang_id[0].id
    except IndexError:
        return None
    return lang_id
