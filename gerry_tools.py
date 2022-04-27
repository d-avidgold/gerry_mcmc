"""
gerrymander - array with arrays consisting of sets of points in the grid
voters - 2d array with values D,R

"""
import copy

def get_winner(voters, gerrymander):
	dem_dists = 0
	for district in gerrymander:
		dist_votes = {"D": 0, "R":0}
		for spot in district:
			dist_votes[voters[spot[0]][spot[1]]] += 1
		if dist_votes["R"] < dist_votes["D"]:
			dem_dists += 1
		if dist_votes["R"] == dist_votes["D"]:
			dem_dists += 0.5
	return(dem_dists)

def get_wasted(voters, gerrymander):
	dem_wasted = 0
	rep_wasted = 0
	for district in gerrymander:
		dist_votes = {"D": 0, "R":0}
		for spot in district:
			dist_votes[voters[spot[0]][spot[1]]] += 1
		# print(dist_votes["D"], dist_votes["R"])
		if dist_votes["D"] < dist_votes["R"]:
			dem_wasted += dist_votes["D"]
			rep_wasted += dist_votes["R"] - len(gerrymander)/2
			# print(dist_votes["D"] - (dist_votes["R"] - len(gerrymander)/2))
		elif dist_votes["D"] >= dist_votes["R"]:
			rep_wasted += dist_votes["R"]
			dem_wasted += dist_votes["D"] - len(gerrymander)/2
			# print(dist_votes["D"] - len(gerrymander)/2 - dist_votes["R"])
		# print()
	return(dem_wasted - rep_wasted)

def get_reock(gerrymander):
	tot_comp = 0
	for district in gerrymander:
		minx = min(district[i][0] for i in range(len(district)))
		maxx = max(district[i][0] for i in range(len(district)))
		miny = min(district[i][1] for i in range(len(district)))
		maxy = max(district[i][1] for i in range(len(district)))
		tot_comp += 1 / ((maxx - minx + 1) * (maxy - miny + 1))
		# print(((maxx - minx + 1) * (maxy - miny + 1)))
	return(tot_comp / len(gerrymander))

def is_valid_region(region_no, gerrymander):
	seen_bad = 0
	init_pos = gerrymander[region_no][0]
	to_be_seen = copy.deepcopy(gerrymander[region_no])
	#print(to_be_seen)
	stack = [init_pos]
	while len(to_be_seen) > 0 and len(stack) > 0:
		look_at_me = stack.pop()
		if look_at_me in to_be_seen:
			to_be_seen.remove(look_at_me)
		x = look_at_me[0]
		y = look_at_me[1]
		#print(to_be_seen)
		stack += [pos for pos in to_be_seen if (pos in [[x, y + 1], [x, y - 1], [x + 1, y], [x - 1, y]])]
	if len(to_be_seen) == 0:
		return(True)
	return(False)

def print_gerrymander(voters, gerrymander, nrows, ncols):
	dno = 1
	for district in gerrymander:
		print("District " + str(dno))
		for i in range(nrows):
			rowstr = ""
			for j in range(ncols):
				if [i, j] in district:
					rowstr += voters[i][j]
				else: rowstr += "."
			print(rowstr)
		dno += 1
		print()
	return()

def swap_coord(x0, y0, x1, y1, gerrymander):
	for district in gerrymander:
		if [x0, y0] in district:
			district.append("HOLD")
			district.remove([x0, y0])

	for district in gerrymander:
		if [x1, y1] in district:
			district.remove([x1, y1])
			district.append([x0, y0])

	for district in gerrymander:
		if "HOLD" in district:
			district.remove("HOLD")
			district.append([x1, y1])
	return(gerrymander)

def get_region_neighbors(region_no, x, y, gerrymander):
	region_points = gerrymander[region_no]
	overlap = [point for point in region_points if point in [[x, y + 1], [x, y - 1], [x + 1, y], [x - 1, y]]]
	return(overlap)

def get_poss_swaps_with_region(orig_region, new_region, x, y, gerrymander):
	if orig_region > new_region: return([])
	poss_swaps = []
	for point in copy.deepcopy(gerrymander[new_region]):
		#print(point)
		if len(get_region_neighbors(orig_region, point[0], point[1], gerrymander)) > 0:
			gerrymander = swap_coord(x, y, point[0], point[1], gerrymander)
			if is_valid_region(orig_region, gerrymander) and is_valid_region(new_region, gerrymander):
				poss_swaps.append(point)
			gerrymander = swap_coord(x, y, point[0], point[1], gerrymander)
	return(poss_swaps)

def get_all_poss_swaps_from_point(orig_region, x, y, gerrymander):
	poss_swaps = []
	for new_region in range(len(gerrymander)):
		if new_region != orig_region:
			poss_swaps += get_poss_swaps_with_region(orig_region, new_region, x, y, copy.deepcopy(gerrymander))
	return(poss_swaps)

def get_all_poss_swaps_in_region(orig_region, gerrymander):
	poss_swaps = []
	for pos in gerrymander[orig_region]:
		#print(pos)
		possibilities = get_all_poss_swaps_from_point(orig_region, pos[0], pos[1], copy.deepcopy(gerrymander))
		#print(possibilities)
		poss_swaps += [[pos, j] for j in possibilities]
	return(poss_swaps)

def get_every_poss_swap(gerrymander):
	poss_swaps = []
	for region in range(len(gerrymander)):
		poss_swaps += get_all_poss_swaps_in_region(region, copy.deepcopy(gerrymander))
	return(poss_swaps)


D = "D"
R = "R"


voters = [[D,R,D,R], [D,R,D,R], [D,R,D,R], [D,R,D,R]]
gerrymander = [[[0, 0], [0, 1], [1, 0], [1,1]], [[0, 2], [0, 3], [1, 2], [1,3 ]], [[2, 0], [3, 0], [2, 1], [3, 1]], [[2, 2], [2, 3], [3, 2], [3, 3]]]

print_gerrymander(voters, gerrymander, 4, 4)
print(get_every_poss_swap( gerrymander))

d1 = [[0, 0], [0, 1], [0, 2], [1, 2], [1, 3], [1, 4], [2, 4], [3, 4]]
d2 = [[0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [1, 5], [1, 6], [2, 5]]
d3 = [[1, 0], [1, 1], [2, 0], [2, 1], [2, 2], [2, 3], [3, 1], [4, 1]]
d4 = [[1, 7], [2, 6], [2, 7], [3, 6], [3, 7], [4, 6], [4, 7], [5, 6]]
d5 = [[3, 0], [4, 0], [5, 0], [5, 1], [6, 0], [6, 1], [7, 0], [7, 1]]
d6 = [[3, 2], [3, 3], [4, 3], [4, 4], [4, 5], [3, 5], [5, 3], [6, 3]]
d7 = [[4, 2], [5, 2], [6, 2], [7, 2], [7, 3], [7, 4], [6, 4], [5, 4]]
d8 = [[5, 5], [6, 5], [7, 5], [6, 6], [7, 6], [5, 7], [6, 7], [7, 7]]

rep_board = [d1, d2, d3, d4, d5, d6, d7, d8]
voters = [['D', 'D', 'D', 'R', 'R', 'R', 'D', 'D'], ['D', 'R', 'D', 'D', 'D', 'R', 'R', 'R'], ['R', 'D', 'R', 'R', 'D', 'D', 'R', 'D'], ['D', 'D', 'D', 'D', 'D', 'D', 'R', 'D'], ['D', 'R', 'R', 'D', 'D', 'D', 'D', 'R'], ['D', 'D', 'D', 'D', 'R', 'R', 'R', 'D'], ['D', 'D', 'D', 'D', 'D', 'R', 'D', 'R'], ['D', 'D', 'R', 'R', 'R', 'D', 'D', 'R']]

print(get_reock(rep_board))



