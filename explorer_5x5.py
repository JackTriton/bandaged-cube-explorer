"""
Bandaged 5x5x5 Solver / Explorer

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

default_cube = list(range(125))

cube_part = {
    **{k: 0 for k in ["UBL","ULB","LBU","LUB","BUL","BLU"]},
    **{k: 4 for k in ["UBR","URB","RBU","RUB","BUR","BRU"]},
    **{k: 20 for k in ["UFL","ULF","LFU","LUF","FUL","FLU"]},
    **{k: 24 for k in ["UFR","URF","RFU","RUF","FUR","FRU"]},
    **{k: 100 for k in ["DBL","DLB","LBD","LDB","BDL","BLD"]},
    **{k: 104 for k in ["DBR","DRB","RBD","RDB","BDR","BRD"]},
    **{k: 120 for k in ["DFL","DLF","LFD","LDF","FDL","FLD"]},
    **{k: 124 for k in ["DFR","DRF","RFD","RDF","FDR","FRD"]},
    **{k: 6 for k in ["UB1L1","UL1B1","L1B1U","L1UB1","B1UL1","B1L1U"]},
    **{k: 8 for k in ["UB1R1","UR1B1","R1B1U","R1UB1","B1UR1","B1R1U"]},
    **{k: 16 for k in ["UF1L1","UL1F1","L1F1U","L1UF1","F1UL1","F1L1U"]},
    **{k: 18 for k in ["UF1R1","UR1F1","R1F1U","R1UF1","F1UR1","F1R1U"]},
    **{k: 106 for k in ["DB1L1","DL1B1","L1B1D","L1DB1","B1DL1","B1L1D"]},
    **{k: 108 for k in ["DB1R1","DR1B1","R1B1D","R1DB1","B1DR1","B1R1D"]},
    **{k: 116 for k in ["DF1L1","DL1F1","L1F1D","L1DF1","F1DL1","F1L1D"]},
    **{k: 118 for k in ["DF1R1","DR1F1","R1F1D","R1DF1","F1DR1","F1R1D"]},
    **{k: 26 for k in ["U1BL1","U1L1B","L1BU1","L1U1B","BU1L1","BL1U1"]},
    **{k: 28 for k in ["U1BR1","U1R1B","R1BU1","R1U1B","BU1R1","BR1U1"]},
    **{k: 46 for k in ["U1FL1","U1L1F","L1FU1","L1U1F","FU1L1","FL1U1"]},
    **{k: 48 for k in ["U1FR1","U1R1F","R1FU1","R1U1F","FU1R1","FR1U1"]},
    **{k: 76 for k in ["D1BL1","D1L1B","L1BD1","L1D1B","BD1L1","BL1D1"]},
    **{k: 78 for k in ["D1BR1","D1R1B","R1BD1","R1D1B","BD1R1","BR1D1"]},
    **{k: 96 for k in ["D1FL1","D1L1F","L1FD1","L1D1F","FD1L1","FL1D1"]},
    **{k: 98 for k in ["D1FR1","D1R1F","R1FD1","R1D1F","FD1R1","FR1D1"]},
    **{k: 30 for k in ["U1B1L","U1LB1","LB1U1","LU1B1","B1U1L","B1LU1"]},
    **{k: 34 for k in ["U1B1R","U1RB1","RB1U1","RU1B1","B1U1R","B1RU1"]},
    **{k: 40 for k in ["U1F1L","U1LF1","LF1U1","LU1F1","F1U1L","F1LU1"]},
    **{k: 44 for k in ["U1F1R","U1RF1","RF1U1","RU1F1","F1U1R","F1RU1"]},
    **{k: 80 for k in ["D1B1L","D1LB1","LB1D1","LD1B1","B1D1L","B1LD1"]},
    **{k: 84 for k in ["D1B1R","D1RB1","RB1D1","RD1B1","B1D1R","B1RD1"]},
    **{k: 90 for k in ["D1F1L","D1LF1","LF1D1","LD1F1","F1D1L","F1LD1"]},
    **{k: 94 for k in ["D1F1R","D1RF1","RF1D1","RD1F1","F1D1R","F1RD1"]},
    **{k: 2 for k in ["UB","BU"]},
    **{k: 10 for k in ["UL","LU"]},
    **{k: 14 for k in ["UR","RU"]},
    **{k: 22 for k in ["UF","FU"]},
    **{k: 50 for k in ["LB","BL"]},
    **{k: 54 for k in ["RB","BR"]},
    **{k: 70 for k in ["LF","FL"]},
    **{k: 74 for k in ["RF","FR"]},
    **{k: 102 for k in ["DB","BD"]},
    **{k: 110 for k in ["DL","LD"]},
    **{k: 114 for k in ["DR","RD"]},
    **{k: 122 for k in ["DF","FD"]},
    **{k: 1 for k in ["UBL1","UL1B","BL1U","BUL1","L1BU","L1UB"]},
    **{k: 3 for k in ["UBR1","UR1B","BR1U","BUR1","R1BU","R1UB"]},
    **{k: 5 for k in ["ULB1","UB1L","LB1U","LUB1","B1UL","B1LU"]},
    **{k: 15 for k in ["ULF1","UF1L","LF1U","LUF1","F1UL","F1LU"]},
    **{k: 9 for k in ["URB1","UB1R","RB1U","RUB1","B1UR","B1RU"]},
    **{k: 19 for k in ["URF1","UF1R","RF1U","RUF1","F1UR","F1RU"]},
    **{k: 21 for k in ["UFL1","UL1F","FL1U","FUL1","L1FU","L1UF"]},
    **{k: 23 for k in ["UFR1","UR1F","FR1U","FUR1","R1FU","R1UF"]},
    **{k: 25 for k in ["U1BL","U1LB","LBU1","LU1B","BU1L","BLU1"]},
    **{k: 75 for k in ["D1BL","D1LB","LBD1","LD1B","BD1L","BLD1"]},
    **{k: 29 for k in ["U1BR","U1RB","RBU1","RU1B","BU1R","BRU1"]},
    **{k: 79 for k in ["D1BR","D1RB","RBD1","RD1B","BD1R","BRD1"]},
    **{k: 45 for k in ["U1FL","U1LF","LFU1","LU1F","FU1L","FLU1"]},
    **{k: 95 for k in ["D1FL","D1LF","LFD1","LD1F","FD1L","FLD1"]},
    **{k: 49 for k in ["U1FR","U1RF","RFU1","RU1F","FU1R","FRU1"]},
    **{k: 99 for k in ["D1FR","D1RF","RFD1","RD1F","FD1R","FRD1"]},
    **{k: 101 for k in ["DBL1","DL1B","BL1D","BDL1","L1BD","L1DB"]},
    **{k: 103 for k in ["DBR1","DR1B","BR1D","BDR1","R1BD","R1DB"]},
    **{k: 105 for k in ["DLB1","DB1L","LB1D","LDB1","B1DL","B1LD"]},
    **{k: 115 for k in ["DLF1","DF1L","LF1D","LDF1","F1DL","F1LD"]},
    **{k: 109 for k in ["DRB1","DB1R","RB1D","RDB1","B1DR","B1RD"]},
    **{k: 119 for k in ["DRF1","DF1R","RF1D","RDF1","F1DR","F1RD"]},
    **{k: 121 for k in ["DFL1","DL1F","FL1D","FDL1","L1FD","L1DF"]},
    **{k: 123 for k in ["DFR1","DR1F","FR1D","FDR1","R1FD","R1DF"]},
    **{k: 7 for k in ["UB1","B1U"]},
    **{k: 11 for k in ["UL1","L1U"]},
    **{k: 13 for k in ["UR1","R1U"]},
    **{k: 17 for k in ["UF1","F1U"]},
    **{k: 55 for k in ["LB1","B1L"]},
    **{k: 59 for k in ["RB1","B1R"]},
    **{k: 65 for k in ["LF1","F1L"]},
    **{k: 69 for k in ["RF1","F1R"]},
    **{k: 107 for k in ["DB1","B1D"]},
    **{k: 111 for k in ["DL1","L1D"]},
    **{k: 113 for k in ["DR1","R1D"]},
    **{k: 117 for k in ["DF1","F1D"]},
    **{k: 27 for k in ["U1B","BU1"]},
    **{k: 35 for k in ["U1L","LU1"]},
    **{k: 39 for k in ["U1R","RU1"]},
    **{k: 47 for k in ["U1F","FU1"]},
    **{k: 51 for k in ["L1B","BL1"]},
    **{k: 53 for k in ["R1B","BR1"]},
    **{k: 71 for k in ["L1F","FL1"]},
    **{k: 73 for k in ["R1F","FR1"]},
    **{k: 77 for k in ["D1B","BD1"]},
    **{k: 85 for k in ["D1L","LD1"]},
    **{k: 89 for k in ["D1R","RD1"]},
    **{k: 97 for k in ["D1F","FD1"]},
    "U": 12,
    "B": 52,
    "L": 60,
    "C": 62,
    "R": 64,
    "F": 72,
    "D": 112}

FACES = {"L":   [a*25 + b*5 + c for a in (0,1,2,3,4) for b in (0,1,2,3,4) for c in (0,)],
         "1L":  [a*25 + b*5 + c for a in (0,1,2,3,4) for b in (0,1,2,3,4) for c in (1,)],
         "M":   [a*25 + b*5 + c for a in (0,1,2,3,4) for b in (0,1,2,3,4) for c in (2,)],
         "1R":  [a*25 + b*5 + c for a in (0,1,2,3,4) for b in (0,1,2,3,4) for c in (3,)],
         "R":   [a*25 + b*5 + c for a in (0,1,2,3,4) for b in (0,1,2,3,4) for c in (4,)],
         "B":   [a*25 + b*5 + c for a in (0,1,2,3,4) for b in (0,) for c in (0,1,2,3,4)],
         "1B":  [a*25 + b*5 + c for a in (0,1,2,3,4) for b in (1,) for c in (0,1,2,3,4)],
         "S":   [a*25 + b*5 + c for a in (0,1,2,3,4) for b in (2,) for c in (0,1,2,3,4)],
         "1F":  [a*25 + b*5 + c for a in (0,1,2,3,4) for b in (3,) for c in (0,1,2,3,4)],
         "F":   [a*25 + b*5 + c for a in (0,1,2,3,4) for b in (4,) for c in (0,1,2,3,4)],
         "U":   [a*25 + b*5 + c for a in (0,) for b in (0,1,2,3,4) for c in (0,1,2,3,4)],
         "1U":  [a*25 + b*5 + c for a in (1,) for b in (0,1,2,3,4) for c in (0,1,2,3,4)],
         "E":   [a*25 + b*5 + c for a in (2,) for b in (0,1,2,3,4) for c in (0,1,2,3,4)],
         "1D":  [a*25 + b*5 + c for a in (3,) for b in (0,1,2,3,4) for c in (0,1,2,3,4)],
         "D":   [a*25 + b*5 + c for a in (4,) for b in (0,1,2,3,4) for c in (0,1,2,3,4)]}

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

    def __init__(self, cp, co, ep, e1p, eo, cep, ccp):
        self.cp = cp
        self.co = co
        self.ep = ep
        self.e1p = e1p
        self.eo = eo
        self.cep = cep
        self.ccp = ccp

    def apply_move(self, move):
        """
        Apply moves and get the new states
        """
        new_cp = [self.cp[p] for p in move.cp]
        new_co = [(self.co[p] + move.co[i]) % 3 for i, p in enumerate(move.cp)]
        new_ep = [self.ep[p] for p in move.ep]
        new_e1p = [self.e1p[p] for p in move.e1p]
        new_eo = [(self.eo[p] + move.eo[i]) % 2 for i, p in enumerate(move.ep)]
        new_cep = [self.cep[p] for p in move.cep]
        new_ccp = [self.ccp[p] for p in move.ccp]
        return State(new_cp, new_co, new_ep, new_eo, new_cep, new_ccp)


# Solved state instance
solved_state = State(
    [0, 1, 2, 3, 4, 5, 6, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
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
