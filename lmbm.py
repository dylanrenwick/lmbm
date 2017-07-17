from sys import argv
import random
import numpy
import os.path

class pointer:
    def __init__(self, coords, id):
        vprint('Creating pointer %s at coords [%s, %s]' % (id, coords[1], coords[0]))
        self.x = coords[1]
        self.y = coords[0]
        self.xvel = 0
        self.yvel = 1
        self.id = id
        self.alive = True
        self.value = 0
        self.spin = 0
        self.string = False
    def __repr__(self):
        return str([[self.x, self.y], [self.xvel, self.yvel]])

def is_alive(pointer_list):
    bools = [i.alive for i in pointer_list]
    vprint('Alive: %s' % bools)
    return any(bools)

def move_pointers(pointer_list):
    global maxLen
    for i in range(0, len(pointer_list)):
        p = pointer_list[i]
        if not p.alive: continue
        vprint('Moving pointer %s: [%s, %s]' % (p.id, p.xvel, p.yvel))
        p.x += p.xvel
        p.y += p.yvel
        if p.x >= maxLen or p.x < 0 or p.y >= len(code) or p.y < 0:
            vprint('Pointer %s has coords [%s, %s], killing' % (p.id, p.x, p.y))
            p.alive = False

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def vprint(obj):
    global verbose
    if verbose: print(str(obj))

def run_pointers(pointer_list):
    for i in range(0, len(pointer_list)):
        pointer = pointer_list[i]
        if not pointer.alive: continue
        char = code[pointer.y][pointer.x]
        vprint('Pointer %s is at char %s' % (i, char))

        if pointer.string:
            pointer.value = ord(char)
            pointer.string = False
        elif char == 'U':
            vprint('  Killing pointer and printing value as char')
            pointer.alive = False
            print(chr(pointer.value), end='')
        elif char == 'u':
            vprint('  Killing pointer and printing value')
            pointer.alive = False
            print(pointer.value, end='')
        elif char == '/':
            vprint('  Moving pointer left')
            pointer.x -= 1
            pointer.spin = 0
        elif char == '\\':
            vprint('  Moving pointer right')
            pointer.x += 1
            pointer.spin = 1
        elif char == '|':
            vprint('  Reflecting pointer direction')
            if pointer.spin:
                pointer.x -= 1
                pointer.spin = 0
            else:
                pointer.x += 1
                pointer.spin = 1
        elif char == 'v':
            pointer.xvel = 0
        elif char == '"':
            pointer.string = True
        elif char == '!':
            vprint('  Printing value as char')
            print(chr(pointer.value), end='')
        elif char == '$':
            vprint('  Printing value')
            print(pointer.value, end='')
        elif char == '^':
            newDir = random.choice([0, 1])
            vprint('Random number is %s' % newDir)
            pointer.spin = newDir
            pointer.x += newDir if newDir else -1
        elif char == '?':
            if pointer.value:
                pointer.spin = 1
            else:
                pointer.spin = 0
        elif char == '_':
            if pointer.spin:
                pointer.x += 1
            else:
                pointer.x -= 1
        elif char == '~':
            vprint('  Trampolining pointer to top')
            pointer.y = 0
        elif char == 'i':
            vprint('  Fetching input')
            try:
                inp = input()
                if inp:
                    if is_int(inp):
                        pointer.value = int(inp)
                    else:
                        pointer.value = ord(inp[0])
            except EOFError:
                pointer.value = pointer.value                



if len(argv) < 2:
    print('Invalid args!')
    print('Please specify a filename')
    exit()

if len(argv) == 3:
    verbose = (argv[-2] == '-v')
else:
    verbose = False

filename = argv[-1]

if not os.path.isfile(filename):
    print('File %s not found!' % filename)
    exit()

with open(filename, 'r') as f:
    code = f.read()

code = [i for i in code.splitlines()]
maxLen = len(max(code, key=len))
for i in range(0, len(code)):
    if len(code[i]) < maxLen:
        code[i] += ' ' * (maxLen - len(code[i]))
vprint(code)
code = numpy.array([[ch for ch in j] for j in code])
vprint(code)
origins = numpy.asarray(numpy.where(code == 'O')).T
vprint(origins)
pointers = []
for i in range(0, len(origins)):
    pointers.append(pointer(origins[i], i))
vprint(pointers)

while is_alive(pointers):
    move_pointers(pointers)
    run_pointers(pointers)

print('')
