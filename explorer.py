"""
Bandaged 3x3x3 Solver / Explorer

Credit goes to
    Kentaro Nishi(https://qiita.com/7y2n),
    Ika no Osushi(https://twitter.com/cube_224)
    and Ladislav Dubravský(https://github.com/ladislavdubravsky).

Usage:
    Bandager: X+Y to connect part X and part Y
    
"""
import copy
import time
import re
import math

default_cube = [  0, 1, 2,
                 3, 4, 5,
                6, 7, 8,
                  9, 10, 11,
                 12, 13, 14,
                15, 16, 17,
                  18, 19, 20,
                 21, 22, 23,
                24, 25, 26]

cube_part = {
    **{k: 0 for k in ["UBL","ULB","LBU","LUB","BUL","BLU"]},
    **{k: 2 for k in ["UBR","URB","RBU","RUB","BUR","BRU"]},
    **{k: 6 for k in ["UFL","ULF","LFU","LUF","FUL","FLU"]},
    **{k: 8 for k in ["UFR","URF","RFU","RUF","FUR","FRU"]},
    **{k: 18 for k in ["DBL","DLB","LBD","LDB","BDL","BLD"]},
    **{k: 20 for k in ["DBR","DRB","RBD","RDB","BDR","BRD"]},
    **{k: 24 for k in ["DFL","DLF","LFD","LDF","FDL","FLD"]},
    **{k: 26 for k in ["DFR","DRF","RFD","RDF","FDR","FRD"]},
    **{k: 1 for k in ["UB","BU"]},
    **{k: 3 for k in ["UL","LU"]},
    **{k: 5 for k in ["UR","RU"]},
    **{k: 7 for k in ["UF","FU"]},
    **{k: 9 for k in ["LB","BL"]},
    **{k: 11 for k in ["RB","BR"]},
    **{k: 15 for k in ["LF","FL"]},
    **{k: 17 for k in ["RF","FR"]},
    **{k: 19 for k in ["DB","BD"]},
    **{k: 21 for k in ["DL","LD"]},
    **{k: 23 for k in ["DR","RD"]},
    **{k: 25 for k in ["DF","FD"]},
    "U": 4,
    "B": 10,
    "L": 12,
    "C": 13,
    "R": 14,
    "F": 16,
    "D": 22}

FACES = {"L": [a*9 + b*3 + c for a in (0,1,2) for b in (0,1,2) for c in (0,)],
         "M": [a*9 + b*3 + c for a in (0,1,2) for b in (0,1,2) for c in (1,)],
         "R": [a*9 + b*3 + c for a in (0,1,2) for b in (0,1,2) for c in (2,)],
         "B": [a*9 + b*3 + c for a in (0,1,2) for b in (0,) for c in (0,1,2)],
         "S": [a*9 + b*3 + c for a in (0,1,2) for b in (1,) for c in (0,1,2)],
         "F": [a*9 + b*3 + c for a in (0,1,2) for b in (2,) for c in (0,1,2)],
         "U": [a*9 + b*3 + c for a in (0,) for b in (0,1,2) for c in (0,1,2)],
         "E": [a*9 + b*3 + c for a in (1,) for b in (0,1,2) for c in (0,1,2)],
         "D": [a*9 + b*3 + c for a in (2,) for b in (0,1,2) for c in (0,1,2)]}

def normalize(cubelist, keepzeros=False):
    """ Normalize a cubelist to get unique bandage shape representation. You
    don't normally need to be calling this. """
    cube = copy.deepcopy(cubelist)
    # handle zeros, which represent non-connected cubies, first
    if not keepzeros:
        blockno = 1 + max([1] + cube)
        for i, v in enumerate(cube):
            if v == 0:
                cube[i] = blockno
                blockno += 1

    # now re-number blocks in reading order
    blockno = 1
    mapping = {0: 0}
    for v in cube:
        if v in mapping or v == 0:
            continue
        else:
            mapping[v] = blockno
            blockno += 1
    return list(map(lambda x: mapping[x], cube))

class ScrumbleError(Exception):
    pass

class State:
    """
    Class represent the cube states
    """

    def __init__(self, cp, co, ep, eo, cep, ceo):
        self.cp = cp
        self.co = co
        self.ep = ep
        self.eo = eo
        self.cep = cep
        self.ceo = ceo

    def apply_move(self, move):
        """
        Apply moves and get the new states
        """
        new_cp = [self.cp[p] for p in move.cp]
        new_co = [(self.co[p] + move.co[i]) % 3 for i, p in enumerate(move.cp)]
        new_ep = [self.ep[p] for p in move.ep]
        new_eo = [(self.eo[p] + move.eo[i]) % 2 for i, p in enumerate(move.ep)]
        new_cep = [self.cep[p] for p in move.cep]
        new_ceo = [(self.ceo[p] + move.ceo[i]) % 4 for i, p in enumerate(move.cep)]
        return State(new_cp, new_co, new_ep, new_eo, new_cep, new_ceo)


# Solved state instance
solved_state = State(
    [0, 1, 2, 3, 4, 5, 6, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 3, 4, 5],
    [0, 0, 0, 0, 0, 0]
)

# Classify 18 1-movers
moves = {
    'U': State([3, 0, 1, 2, 4, 5, 6, 7],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 11],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 2, 3, 4, 5],
               [1, 0, 0, 0, 0, 0]),
    'D': State([0, 1, 2, 3, 5, 6, 7, 4],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 2, 3, 4, 5],
               [0, 3, 0, 0, 0, 0]),
    'L': State([4, 1, 2, 0, 7, 5, 6, 3],
               [2, 0, 0, 1, 1, 0, 0, 2],
               [11, 1, 2, 7, 4, 5, 6, 0, 8, 9, 10, 3],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 2, 3, 4, 5],
               [0, 0, 3, 0, 0, 0]),
    'R': State([0, 2, 6, 3, 4, 1, 5, 7],
               [0, 1, 2, 0, 0, 2, 1, 0],
               [0, 5, 9, 3, 4, 2, 6, 7, 8, 1, 10, 11],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 2, 3, 4, 5],
               [0, 0, 0, 1, 0, 0]),
    'F': State([0, 1, 3, 7, 4, 5, 2, 6],
               [0, 0, 1, 2, 0, 0, 2, 1],
               [0, 1, 6, 10, 4, 5, 3, 7, 8, 9, 2, 11],
               [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
               [0, 1, 2, 3, 4, 5],
               [0, 0, 0, 0, 1, 0]),
    'B': State([1, 5, 2, 3, 0, 4, 6, 7],
               [1, 2, 0, 0, 2, 1, 0, 0],
               [4, 8, 2, 3, 1, 5, 6, 7, 0, 9, 10, 11],
               [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
               [0, 1, 2, 3, 4, 5],
               [0, 0, 0, 0, 0, 3]
               )}

wide_moves = {
    'u': State([3, 0, 1, 2, 4, 5, 6, 7],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [3, 0, 1, 2, 7, 4, 5, 6, 8, 9, 10, 11],
               [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 4, 5, 3, 2],
               [1, 0, 0, 0, 0, 0]),
    'd': State([0, 1, 2, 3, 5, 6, 7, 4],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [1, 2, 3, 0, 4, 5, 6, 7, 9, 10, 11, 8],
               [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 5, 4, 2, 3],
               [0, 3, 0, 0, 0, 0]),
    'l': State([4, 1, 2, 0, 7, 5, 6, 3],
               [2, 0, 0, 1, 1, 0, 0, 2],
               [11, 1, 2, 7, 8, 5, 4, 0, 10, 9, 6, 3],
               [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
               [5, 4, 2, 3, 0, 1],
               [0, 0, 3, 0, 0, 0]),
    'r': State([0, 2, 6, 3, 4, 1, 5, 7],
               [0, 1, 2, 0, 0, 2, 1, 0],
               [0, 5, 9, 3, 4, 2, 6, 7, 8, 1, 10, 11],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [4, 5, 2, 3, 1, 0],
               [0, 0, 0, 1, 0, 0]),
    'f': State([0, 1, 3, 7, 4, 5, 2, 6],
               [0, 0, 1, 2, 0, 0, 2, 1],
               [0, 1, 6, 10, 4, 5, 3, 7, 8, 9, 2, 11],
               [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
               [2, 3, 1, 0, 4, 5],
               [0, 0, 0, 0, 1, 0]),
    'b': State([1, 5, 2, 3, 0, 4, 6, 7],
               [1, 2, 0, 0, 2, 1, 0, 0],
               [4, 8, 2, 3, 1, 5, 6, 7, 0, 9, 10, 11],
               [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
               [3, 2, 0, 1, 4, 5],
               [0, 0, 0, 0, 0, 3]
               )}

move_names = []
faces = list(moves.keys())
for face_name in faces:
    move_names += [face_name, face_name + '2', face_name + '\'']
    moves[face_name + '2'] = moves[face_name].apply_move(moves[face_name])
    moves[face_name + '\''] = moves[face_name].apply_move(moves[face_name]).apply_move(moves[face_name])

def _rotate(fc):
    """ Rotate a length-9 list representing a layer 90 degrees. """
    return [fc[6], fc[3], fc[0], fc[7], fc[4], fc[1], fc[8], fc[5], fc[2]]

def turn(move, cube):
    """ Do a single face turn and return the new cube. """
    if "'" in move:
        num = 3
    elif "2" in move:
        num = 2
    else:
        num = 1
    face = FACES[move[0]]
    facecontent = [cube[i] for i in range(27) if i in face]
    if (num == 1 and face[0] not in [1, 2]) or (num == 3 and face[0] in [1, 2]):
        turned = _rotate(facecontent)
    elif num == 2:
        turned = _rotate(_rotate(facecontent))
    elif (num == 3 and face[0] not in [1, 2]) or (num == 1 and face[0] in [1, 2]):
        turned = _rotate(_rotate(_rotate(facecontent)))
    newcube = copy.deepcopy(cube) # consider list(cube)
    for i, fi in enumerate(face):
        newcube[fi] = turned[i]
    return normalize(newcube)

def scramble2state(scramble, cube):
    """
    Return state that aplied the scramble
    """
    cur_cube = copy.deepcopy(cube)
    cur_cube = normalize(cur_cube)
    scrambled_state = solved_state
    for move_name in scramble.split(" "):
        move_state = moves[move_name]
        scrambled_state = scrambled_state.apply_move(move_state)
        cur_cube = turn(move_name, cur_cube)
    return scrambled_state, cur_cube

def is_solved(state, check_center=False):
    if check_center:
        und = (state.ceo == [0] * 6 and state.cep == list(range(6)))
    else:
        und = True
    return (state.eo == [0] * 12  # Solved EO
            and state.co == [0] * 8  # Solved CO
            and state.ep == list(range(12))  # Solved EP
            and state.cp == list(range(8))  # Solved CP
            and und
            )

# Dict that to get opposite side
inv_face = {
    "U": "D",
    "D": "U",
    "L": "R",
    "R": "L",
    "F": "B",
    "B": "F"
}

def is_move_available(cube, prev_move, move):
    """
    - Cannot turn same face e.g.) R' R2 is not avaiable
    - If opposite face is going to move, the order is always same e.g.) can do U D but cannot do D U
    - If the bandaging is blocking the face to turn, it cannot turn
    """
    faceblocks = set([cube[i] for i in FACES[move[0]]])
    restblocks = set([cube[i] for i in set(range(27)) - set(FACES[move[0]])])
    if faceblocks & restblocks: # Check if the number of bandaging is same or not
        return False
    if prev_move is None:
        return True  # Avaiable if this is first move
    prev_face = prev_move[0]  # Previous move
    if prev_face == move[0]:
        return False # Turning same face is not avaiable
    if inv_face[prev_face] == move[0]:
        return prev_face < move[0] # If opposite face, the order would be same as in dict
    return True

def count_solved_corners(state):
    """
    Count solved corners
    """
    return sum([state.cp[i] == i and state.co[i] == 0 for i in range(8)])


def count_solved_edges(state):
    """
    Count solved edges
    """
    return sum([state.ep[i] == i and state.eo[i] == 0 for i in range(12)])

def count_solved_centers(state):
    """
    Count solved centers
    """
    return sum([state.cep[i] == i and state.ceo[i] == 0 for i in range(6)])


def prune(depth, state):
    """
    Give back True if the program doesn't have to be run
    """
    if depth == 1 and (count_solved_corners(state) < 4 or count_solved_edges(state) < 8):
        # If there is only 1 move and solved corner is less than 4 or solved edge is less than 8, it cannot be solved
        return True
    if depth == 2 and count_solved_edges(state) < 4:
        # If there are only 2 moves and solved edge is less than 4, it cannot be solved
        return True
    if depth == 3 and count_solved_edges(state) < 2:
        # If there are only 3 moves and solved edge is less than 2, it cannot be solved
        return True
    return False

class Search:
    def __init__(self,initcube,scrcube,centers=False,wide=False):
        self.current_solution = []
        self.initcube = copy.deepcopy(normalize(initcube))
        self.scrcube = scrcube
        self.curcube_state = {}
        self.curcube_state[""] = scrcube
        self.res = {}
        self.count = 0
        self.use_center = centers
        self.wide = wide

    def depth_limited_search(self, state, scrcube, depth, get=1):
        comp = get
        if depth == 0 and is_solved(state,self.wide or self.use_center):
            self.res[str(self.count)] = " ".join(self.current_solution)
            self.count += 1
            if self.count == get:
                return True
            else:
                return False
        if depth == 0:
            return False

        if prune(depth, state):
            return False
        
        prev_move = self.current_solution[-1] if self.current_solution else None  # Previous move
        for move_name in move_names:
            if not is_move_available(scrcube, prev_move, move_name):
                continue
            self.current_solution.append(move_name)
            cursolt = " ".join(self.current_solution)
            self.curcube_state[cursolt] = turn(move_name, scrcube)
            if self.depth_limited_search(state.apply_move(moves[move_name]), self.curcube_state[cursolt], depth - 1, comp):
                return True
            self.current_solution.pop()

    def start_search(self, state, scrcube, max_length=20, get=1):
        for depth in range(0, max_length):
            print(f"# Start searching length {depth}")
            if self.depth_limited_search(state, scrcube, depth, get):
                return self.res
        if self.res:
            return self.res
        return None

def finer(text):
    text = " " + text + " "
    reg = re.findall(r"(([^2'\s])[2'\s]{1,2}([^2'\s])[2'\s]{1,2}\2[2'\s]{1,2}\3[2'\s]{1,2})",text)
    t = [reg[k][0][:-1] for k in range(len(reg))]
    for a in t:
        setter = a
        term = text.split(setter)
        meg = term[0]
        for b in range(text.count(setter)):
            meg += "(" + setter + ")" + term[b+1]
        text = meg
    reg = re.findall(r"\s(([^2'\s])[2'\s]{1,2}([^2'\s])[2'\s]{1,2}\2[2'\s]{1,2}\s)",text)
    t = [reg[k][0][:-1] for k in range(len(reg))]
    for a in t:
        setter = a
        term = text.split(setter)
        meg = term[0]
        for b in range(text.count(setter)):
            meg += "(" + setter + ")" + term[b+1]
        text = meg
    if text.startswith(" "):
        text = text[1:]
    if text.endswith(" "):
        text = text[:-1]
    return text

def Bandager(bandage_arg):
    bandaged_cube = copy.deepcopy(default_cube)
    bandage = bandage_arg.replace(" ","").split(",")
    for bd in bandage:
        connect = bd.split("+")
        head = connect.pop(0)
        head_num = cube_part[head]
        for c in connect:
            connect_num = cube_part[c]
            bandaged_cube[connect_num] = bandaged_cube[head_num]
    get_num = {}
    t = 1
    for a in range(27):
        try:
            bandaged_cube[a] = get_num[str(bandaged_cube[a])]
        except:
            get_num[str(bandaged_cube[a])] = t
            bandaged_cube[a] = t
            t += 1
    return bandaged_cube
