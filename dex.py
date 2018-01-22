# Austin Hester 12/28/17
import argparse
import argcomplete
import pokespell
import dexdb as db

# Display Pokemon stats
def print_pokemon (pokemon, with_moves=False):
	if (pokemon == None):
		print "Does not exist"
		return
	pokeid = pokemon.id
	
	eggs = db.get_egg_groups (pokeid)
	print eggs
	types = db.get_type (pokeid)
	type_name = db.get_type_name(types)
	growth_rate = db.get_growth_rate (pokemon.growth_rate_id)
	abilities = db.get_abilities (pokeid)
	stats = db.get_stats (pokeid)
	evs = db.get_evs (stats)
	evolve_from = db.get_evolution_from (pokeid)
	evolve_from = db.get_by_id (evolve_from)
	evolve_to_temp = db.get_evolution_to (pokeid)
        evolve_to = []
        for et in evolve_to_temp:
            evolve_to.append (db.get_by_id (et))
	print "============================================"
	print "--------------------------------------------"
	print (u'{0.name}, the {0.genus}'.format(pokemon).upper())
	print "--------------------------------------------"
	print "--------------------------------------------"
	print "INFO"
	print "id:\t\t", pokeid
	print "type:\t\t", type_name 
	print "cap_rate:\t", (u'{0.capture_rate}'.format(pokemon))
	print "grow_rate:\t", growth_rate
	print "steps_to_hatch:\t", (255 * (pokemon.hatch_counter + 1))
	print "--------------------------------------------"
	print "============================================"
	print "--------------------------------------------"
	# Evolution needs much work 
	print "Evolves from:\t",
	if (evolve_from != None):
                method = db.get_evolution_trigger (pokeid)
                flag = 0
                for m in method:
                    if (flag):
                        print '\t\t',
		    print evolve_from.identifier, '@', m 
                    flag = 1
	else:
		print None
	print "Evolves to:\t",
	if (len(evolve_to) > 0):
                flag = 0
                for et in evolve_to:
                    method = db.get_evolution_trigger (et.id)
                    for m in method:
                        if (flag):
                            print '\t\t',
                        print et.identifier, '@', m
                        flag = 1
	else:
		print None
	print "--------------------------------------------"
	print "============================================"
	print "Abilities"
	print_abilities (abilities)
	print "--------------------------------------------"
	print "============================================"
	print "STATS"
	print "--------------------------------------------"
	print_stats (stats)
	print "--------------------------------------------"
	print_evs (evs)
	print "============================================"
    	if (with_moves):
        	print_moves (pokeid)
	if (pokemon.forms_switchable == 1):
		forms = db.get_forms (pokeid) 
		print forms

def print_moves (poke_id):
    moves = db.get_moves (poke_id)
    print "--------------------------------------------"
    print "MOVES"
    print "--------------------------------------------"
    for m in moves:
        move = db.get_move_name (m.move_id).upper()
        level = m.level
        if (level == 0):
            level = "by TM"
        else:
            level = ("@ lvl %d" % level)
        print "\t", move, level
    print "--------------------------------------------"
    print "============================================"

# Display abilities
def print_abilities (abilities):
	for a in abilities:
		info = db.get_ability_info (a[0])
		print "--------------------------------------------"
		if (a[1] == True):
			print "[Hidden]"
		print info[0].upper(), ": ",
		print info[1]

# Display stats
def print_stats (stats):
	base = 0
	for s in stats:
		base += s[1]
		print db.stat_id_to_name(s[0]),
		if (s[0] < 3 or s[0] == 6):
			print '\t\t',
		if (s[0] == 3 or s[0] == 4):
			print '\t',
		print '\t:', s[1]
	print "Base\t\t\t:", base

# Display E.V.s 
def print_evs (evs):
	print "E.V.s:\t",
	for ev in evs:
		print ev[0], ": ", ev[1], "\t",
	print ""

def print_pokemon_list (pokes):
	for p in pokes:
		print p.encode('utf-8')

def print_natures ():
	natures = db.get_natures ()
	print "============================================"
	for n in natures:
		print n[0], "++"
		print "============================================"
		for nn in n[1:]:
			nature = nn[0].encode('utf-8')
			print nature.upper(),
			if (len(nature) < 7):
				print '\t',
			print " -- ", nn[1]
		print "============================================"

def print_characteristics ():
	chars = db.get_characteristics ()
	print "============================================"
	for c in chars:
		print c[0], "++"
		print "============================================"
		print c[1].encode('utf-8'), '\t    ',
		print c[2].encode('utf-8')
		print c[3].encode('utf-8'), '\t',
		print c[4].encode('utf-8')
		print c[5].encode('utf-8')
		print "============================================"

# done displaying
#######################################################

def parse_input (pokemon):
	pokemon = pokemon.decode('utf-8')
	if (pokemon.isnumeric()):
		poke = db.get_by_id(pokemon)
	else:
		# pokespell.py cio 
		pokemon = pokespell.correction(pokemon.lower())
		poke = db.get_by_name(pokemon)
	return poke

# Parse arguments
parser = argparse.ArgumentParser(description='Which Pokemon')
parser.add_argument('pokemon', type=str, nargs='?',
                         help='Which Pokemon')
parser.add_argument('option', type=str, nargs='?',
			help='option')
argcomplete.autocomplete(parser)
args = parser.parse_args()
pokemon = args.pokemon

# start console loop
while (True):
    if (pokemon == None):
            pokemon = raw_input ("pokemon? >> ")
            opts = pokemon.split(' ')
            pokemon = opts[0]
    if (pokemon == 'quit' or pokemon == 'q'):
            break
    if (pokemon == 'help' or pokemon == 'h'):
            print "you do need help, huh?"
            pokemon = None
            continue
    if (pokemon == 'nature' or pokemon == 'natures'):
            print_natures ()
            pokemon = None
            continue
    if (pokemon == 'characteristic' or pokemon == 'chars'):
            print_characteristics ()
            pokemon = None
            continue
    if (pokemon == 'effort' or pokemon == 'evs'):
            stat = raw_input ("which stat? : ")
            #stat = pokespell.correction (stat.lower())
            pokes = db.get_poke_by_ev (stat.decode('utf-8'))
            print_pokemon_list (pokes)
            pokemon = None
            continue

    poke = parse_input (pokemon)

    flag = 0
    try:
        if (opts[1] == 'moves'):
            print_pokemon (poke, True)
            flag = 1 
    except IndexError:
        print_pokemon (poke)
        flag = 1

    # print what you just got
    if (not flag):
        print_pokemon (poke)
    pokemon = None
