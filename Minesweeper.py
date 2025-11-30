import sys
import subprocess
from itertools import combinations

def min_clauses(vars, k):
    clauses = []
    n = len(vars)
    m = n - k + 1
    if m < 0:
        return [()]
    for subset in combinations(vars, m):
        clauses.append(tuple(subset))
    return clauses


def max_clauses(vars, k):
    clauses = []
    for subset in combinations(vars, k + 1):
        clauses.append(tuple(-v for v in subset))
    return clauses


def all_clauses(vars, k):
    return min_clauses(vars, k) + max_clauses(vars, k)




rows, cols = input().split()
cols = int(cols)
rows = int(rows)
board = []
language = {}
v_i = {}
for r in sys.stdin:
    k = len(r)
    board += r.strip().split()
variable = 1

clauses = set()
i = 0
variable = 1
for x in board:
    neighs = []
    vars = []
    if x != '?':
        if i == 0:
           for n in [1, cols, cols + 1] if rows > 1 and cols > 1 else [1] if rows == 1 else [cols]:
               if board[n%(rows*cols)] == '?':
                   if n not in language:
                       language[n] = variable
                       v_i[variable] = n
                       variable +=1
                   neighs.append(n)
        elif i == cols - 1:
            for n in [i - 1, i + cols, i + cols - 1] if rows > 1 and cols > 1 else [i - 1] if rows == 1 else [i + cols]:
               if board[n%(rows*cols)] == '?':
                   if n not in language:
                       language[n] = variable
                       v_i[variable] = n
                       variable +=1
                   neighs.append(n)
        elif i == cols * (rows - 1):
            for n in [i - cols, i - cols + 1, i + 1] if rows > 1 and cols > 1 else [i + 1] if rows == 1 else [i - cols]:
               if board[n%(rows*cols)] == '?':
                   if n not in language:
                       language[n] = variable
                       v_i[variable] = n
                       variable +=1
                   neighs.append(n)
        elif i == cols * rows - 1:
            for n in [i - 1, i - cols, i - cols - 1] if rows > 1 and cols > 1 else [i - 1] if rows == 1 else [i - cols]:
               if board[n%(rows*cols)] == '?':
                   if n not in language:
                       language[n] = variable
                       v_i[variable] = n
                       variable +=1
                   neighs.append(n)
        elif i % cols == 0:
            for n in [i - cols, i - cols + 1, i + 1, i + cols, i + cols + 1] if rows > 1 and cols > 1 else [i + 1] if rows == 1 else [i - cols, i + cols]:
               if board[n%(rows*cols)] == '?':
                   if n not in language:
                       language[n] = variable
                       v_i[variable] = n
                       variable +=1
                   neighs.append(n)
        elif (i + 1) % cols == 0:
            for n in [i - 1, i - cols, i - cols - 1, i + cols, i + cols - 1] if rows > 1 and cols > 1 else [i - 1] if rows == 1 else [i - cols, i + cols]:
               if board[n%(rows*cols)] == '?':
                   if n not in language:
                       language[n] = variable
                       v_i[variable] = n
                       variable +=1
                   neighs.append(n)
        elif 0 < i < cols:
            for n in [i - 1, i + cols - 1, i + cols , i + cols + 1, i + 1] if rows > 1 and cols > 1 else [i - 1, i + 1] if rows == 1 else [i + cols]:
               if board[n%(rows*cols)] == '?':
                   if n not in language:
                       language[n] = variable
                       v_i[variable] = n
                       variable +=1
                   neighs.append(n)
        elif cols * (rows - 1) < i < cols * rows:
            for n in [i - 1, i - cols - 1, i - cols , i - cols + 1, i + 1] if rows > 1 and cols > 1 else [i + 1, i - 1] if rows == 1 else [i - cols]:
               if board[n%(rows*cols)] == '?':
                   if n not in language:
                       language[n] = variable
                       v_i[variable] = n
                       variable +=1
                   neighs.append(n)
        else:
            for n in [i - cols - 1, i - cols, i - cols + 1, i - 1, i + 1, i + cols - 1, i + cols, i + cols + 1]:
               if board[n%(rows*cols)] == '?':
                   if n not in language:
                       language[n] = variable
                       v_i[variable] = n
                       variable +=1
                   neighs.append(n)
        for y in neighs:
            vars.append(language[y])
        for c in all_clauses(vars, int(x)):
            clauses.add(c)
    i += 1
with open('input.cnf', 'w') as f:
    f.write(f'p cnf {len(language)} {len(clauses)}\n')
    for c in clauses:
        for l in c:
            f.write(str(l) + ' ')
        f.write('0\n')
result = subprocess.run(
    ['glucose-syrup.exe', '-model', 'input.cnf'],
    capture_output=True,
    text=True
)
with open('output.txt', 'w') as f:
    f.write(result.stdout)
with open('output.txt') as o:
    stats = ''
    l = o.readline()
    while l[0] != 's':
        stats += l
        l = o.readline()
    if l[2] == 'S':
        print('Satisfiable!')
        l = o.readline()
        for x in l.strip().split():
            if x == 'v':
                continue
            if x == '0':
                break
            if x[0] != '-':
                board[v_i[int(x)]%(rows*cols)] = '*'
            else:
                board[v_i[int(x[1:len(x)])]%(rows*cols)] = 's'
        for x in range(0, len(board), cols):
            r = ''
            for y in range(x, x + cols):
                r += board[y] + ' '
            print(r)
    else:
        print('Unsatisfiable!')
print('For stats input "s", for CNF formula input "c", for both input "s+c"')
f = open('input.cnf')
appendix = input()
if appendix == 's':
    print(stats)
elif appendix == 'c':
    print(f.read())
elif appendix == 's+c':

    print(stats + f.read())
