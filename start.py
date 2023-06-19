from explorer import Bandager, Search, scramble2state,finer, faces
import re
import time
import math
def explorer(bandage_arg, scramble_scr, name, length=25, get=5, export=None):
    cube = Bandager(bandage_arg)

    scramble = scramble_scr
    solution_name = name
    scrambled_state, scrambled_cube = scramble2state(scramble, cube)
    search = Search(cube, scrambled_cube)
    start = time.time()
    solution = search.start_search(scrambled_state, scrambled_cube, max_length=length, get=get)

    fine_dict = {}
    for k, sol in solution.items():
        solen = len(re.findall(r"[^2'\s]",sol))
        
        a = len(re.findall(r"([^2'\s])[2'\s]{1,2}([^2'\s])[2'\s]{1,2}\1[2'\s]{1,2}\2[2'\s]{1,2}",sol))
        b = len(re.findall(r"([^2'\s])[2'\s]{1,2}([^2'\s])[2'\s]{1,2}\1[2'\s]{1,2}",sol))
        extra = b - a
        
        get = {}
        for face_name in faces:
            get[face_name] = sol.count(face_name + "2") + sol.count(face_name)
        i = 0
        h = 0
        b = []
        for y, co in get.items():
            if co == 0:
                b.append(y)
            else:
                h += co
                i += 1
        for g in b:
            del get[g]
        median = h / i
        r = 0
        for y, co in get.items():
            r += (co - median) ** 2
        disability = math.ceil((len(get)/2)*math.sqrt(r/i))
        usability = 25 - solen + (extra * 0.25) - (disability * 0.125)
        if usability < 0:
            continue
        fine_sol = finer(sol)
        f_solution = f"Length: {solen} Usability: {usability:.3f}\n{fine_sol}"
        fine_dict[f_solution] = usability

    fined_list = sorted(fine_dict.items(), key = lambda x:float(x[1]), reverse=True)
    fine_solution = ""
    for i, d in enumerate(fined_list):
        fine_solution += f"\n{i+1}: {d[0]}\n"
    print(f"Finished! ({time.time() - start:.2f} sec.)\n")
    if export is not None:
        with open(export, mode="a+") as exp:
            if solution:
              print(f"{solution_name}\nScramble: {scramble}\nSolution: \n{fine_solution}\n")
              exp.write(f"{solution_name}\nScramble: {scramble}\nSolution: \n{fine_solution}\n")
            else:
              print(f"{solution_name}\nScramble: {scramble}\nSolution not found.\n\n")
              exp.write(f"{solution_name}\nScramble: {scramble}\nSolution not found.\n\n")
    else:
        if solution:
          print(f"{solution_name}\nScramble: {scramble}\nSolution: \n{fine_solution}\n")
        else:
          print(f"{solution_name}\nScramble: {scramble}\nSolution not found.\n\n")

bandage_seq="UBL+UB,UBR+UR,U+UL,UF+UFL,F+FD,FL+FDL,FR+FRD,L+LD,BL+BLD,B+BD+D,R+RB,RD+RDB"
scramble_name="TEST"
scramble="R U R' F2 L F L' U' F R U2 L' U R' U2 L U' R U R' F2 L F L' U' F"
explorer(bandage_seq, scramble, scramble_name, 25, 5, "test.txt")
