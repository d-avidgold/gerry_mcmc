from gerry_tools import *
import random

def run_MCMC(gerrymander, voters, nrows, ncols, niter):
	init_win = get_winner(voters, gerrymander)
	poss = get_every_poss_swap(gerrymander)
	win_rec = []
	eg = []
	reck = []
	win_record = {i / 2: 0 for i in range(len(gerrymander) * 2 + 1)}
	changed = False
	for i in range(niter):
		if i % int(niter / 10) == 0: print("Iteration Number " + str(i))
		if not changed:
			poss = get_every_poss_swap(gerrymander)
		else:
			poss = new_poss
		swap = random.choice(poss)
		orig_degree = len(poss)
		gerrymander = swap_coord(swap[0][0], swap[0][1], swap[1][0], swap[1][1], gerrymander)
		new_poss = get_every_poss_swap(gerrymander)
		new_degree = len(new_poss)
		if orig_degree > new_degree or random.random() < orig_degree / new_degree:
			changed = True
		else:
			changed = False
			gerrymander = swap_coord(swap[0][0], swap[0][1], swap[1][0], swap[1][1], gerrymander)
		win_rec.append(get_winner(voters, gerrymander))
		eg.append(get_wasted(voters, gerrymander))
		#cprint(get_reock(gerrymander))
		reck.append(get_reock(gerrymander))
		win_record[get_winner(voters, gerrymander)] += 1


	
	#print_gerrymander(voters, gerrymander, nrows, ncols)
	#print(init_win)
	#print(win_record)

	f = open("eg.txt", "w")
	f.write(str(eg))
	f.close()

	f = open("seats.txt", "w")
	f.write(str(win_rec))
	f.close()

	f = open("reock.txt", "w")
	f.write(str(reck))
	f.close()

	nsmaller = 0
	for i in range(len(gerrymander) * 2):
		if i <= init_win:
			nsmaller += win_record[i]
		else: break

	return(init_win, nsmaller / niter)


n = 8
row_board = [[[j, i] for i in range(n)] for j in range(n)]
d1 = [[0, 0], [0, 1], [0, 2], [1, 2], [1, 3], [1, 4], [2, 4], [3, 4]]
d2 = [[0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [1, 5], [1, 6], [2, 5]]
d3 = [[1, 0], [1, 1], [2, 0], [2, 1], [2, 2], [2, 3], [3, 1], [4, 1]]
d4 = [[1, 7], [2, 6], [2, 7], [3, 6], [3, 7], [4, 6], [4, 7], [5, 6]]
d5 = [[3, 0], [4, 0], [5, 0], [5, 1], [6, 0], [6, 1], [7, 0], [7, 1]]
d6 = [[3, 2], [3, 3], [4, 3], [4, 4], [4, 5], [3, 5], [5, 3], [6, 3]]
d7 = [[4, 2], [5, 2], [6, 2], [7, 2], [7, 3], [7, 4], [6, 4], [5, 4]]
d8 = [[5, 5], [6, 5], [7, 5], [6, 6], [7, 6], [5, 7], [6, 7], [7, 7]]

rep_board = [d1, d2, d3, d4, d5, d6, d7, d8]
# voters = [[random.choice(["R", "D"]) for i in range(n)] for j in range(n)]
voters = [['D', 'D', 'D', 'R', 'R', 'R', 'D', 'D'], ['D', 'R', 'D', 'D', 'D', 'R', 'R', 'R'], ['R', 'D', 'R', 'R', 'D', 'D', 'R', 'D'], ['D', 'D', 'D', 'D', 'D', 'D', 'R', 'D'], ['D', 'R', 'R', 'D', 'D', 'D', 'D', 'R'], ['D', 'D', 'D', 'D', 'R', 'R', 'R', 'D'], ['D', 'D', 'D', 'D', 'D', 'R', 'D', 'R'], ['D', 'D', 'R', 'R', 'R', 'D', 'D', 'R']]

print(voters)

print_gerrymander(voters, row_board, n, n)
print(get_winner(voters, row_board))
print_gerrymander(voters, rep_board, n, n)
print(get_winner(voters, rep_board))

ratios = []
wins = []

print(run_MCMC(rep_board, voters, n, n, 1000))

"""
for simno in range(200):
	if simno % 10 == 0: print("Simulation Number " + str(simno))
	w, ratio = run_MCMC(basic_board, voters, n, n, 200)
	ratios.append(ratio)
	wins.append(w)

print(ratios)


[[[j, i] for i in range(3)] for j in range(5)]
"""
"""
 D D D R R R D D
 D R D D D R R R
 R D R R D D R D
 D D D D D D R D
 D R R D D D D R
 D D D D R R R D
 D D D D D R D R
 D D R R R D D D


"""