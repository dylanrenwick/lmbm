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
        self.held = False
        self.value = 0
        self.spin = 0
        self.string = False
    def __repr__(self):
        return str([[self.x, self.y], [self.xvel, self.yvel]])

def is_alive(pointer_list):
    bools = [i.alive for i in pointer_list]
    vprint('Alive: %s' % bools)
    return any(bools)

def find_held_pointers(pointer_list, x, y):
    return [i for i in pointer_list if i.x == x and i.y == y and i.held and i.alive]

def move_pointers(pointer_list):
    global maxLen
    for i in range(0, len(pointer_list)):
        p = pointer_list[i]
        if p.held or not p.alive: continue
        p.x += p.xvel
        p.y += p.yvel
        vprint('Moving pointer %s: [%s, %s], new pos is [%s, %s]' % (p.id, p.xvel, p.yvel, p.x, p.y))
        if p.x >= maxLen or p.x < 0 or p.y >= len(code) or p.y < 0:
            vprint('Pointer %s has coords [%s, %s], killing' % (p.id, p.x, p.y))
            p.alive = False

def handle_operator_held(pointer_list, pointer):
    held_pointers = find_held_pointers(pointer_list, pointer.x, pointer.y)
    vprint('  Found %s held pointers' % len(held_pointers))
    if not held_pointers:
        vprint('  Holding pointer')
        pointer.held = True
        return False
    else:
        return held_pointers

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
        p = pointer_list[i]
        if p.held or not p.alive: continue
        char = code[p.y][p.x]
        vprint('Pointer %s is at char %s' % (i, char))

        if p.string:
            vprint('  Setting pointer to %s' % ord(char))
            p.value = ord(char)
            p.string = False
        elif is_int(char):
            p.value = int(char)
        elif char == 'U':
            vprint('  Killing pointer and printing value as char')
            p.alive = False
            print(chr(p.value), end='')
        elif char == 'u':
            vprint('  Killing pointer and printing value')
            p.alive = False
            print(p.value, end='')
        elif char == '/':
            vprint('  Moving pointer left')
            p.x -= 1
            p.spin = 0
        elif char == '\\':
            vprint('  Moving pointer right')
            p.x += 1
            p.spin = 1
        elif char == '|':
            vprint('  Reflecting pointer direction')
            if p.spin:
                p.x -= 1
                p.spin = 0
            else:
                p.x += 1
                p.spin = 1
        elif char == 'v':
            p.xvel = 0
        elif char == 'o':
            vprint('  Creating new marble')
            if p.spin:
                p.x += 1
            else:
                p.x -= 1
            newPoint = pointer([p.x - (1 if p.spin else -1), p.y], len(pointer_list))
            newPoint.spin = 0 if p.spin else 0
            newPoint.value = p.value
            pointer_list.append(newPoint)
        elif char == '"':
            vprint('  Entering string mode')
            p.string = True
        elif char == '!':
            vprint('  Printing value as char')
            print(chr(p.value), end='')
        elif char == '$':
            vprint('  Printing value')
            print(p.value, end='')
        elif char == '^':
            newDir = random.choice([0, 1])
            vprint('Random number is %s' % newDir)
            p.spin = newDir
            p.x += newDir if newDir else -1
        elif char == '?':
            if p.value:
                p.spin = 1
            else:
                p.spin = 0
        elif char == '_':
            if p.spin:
                p.x += 1
            else:
                p.x -= 1
        elif char == '~':
            vprint('  Trampolining pointer to top')
            p.y = -1
        elif char == 'i':
            vprint('  Fetching input')
            try:
                inp = input()
                if inp:
                    if is_int(inp):
                        p.value = int(inp)
                    else:
                        p.value = ord(inp[0])
            except EOFError:
                p.value = p.value
        elif char == '+':
            held = handle_operator_held(pointer_list, p)
            if held:
                p.value += held[0].value
                held[0].alive = False
        elif char == '*':
            held = handle_operator_held(pointer_list, p)
            if held:
                p.value *= held[0].value
                held[0].alive = False
        elif char == '-':
            held = handle_operator_held(pointer_list, p)
            if held:
                p.value -= held[0].value
                held[0].alive = False
        elif char == '&':
            held = handle_operator_held(pointer_list, p)
            if held:
                p.value /= held[0].value
                held[0].alive = False
        elif char == '#':
            held = handle_operator_held(pointer_list, p)
            if held:
                p.value = p.value ** held[0].value
                held[0].alive = False
        elif char == '%':
            held = handle_operator_held(pointer_list, p)
            if held:
                p.value %= held[0].value
                held[0].aluve = False
        elif char == ';':
            p.alive = False
        elif char == '(':
            p.value += 1
        elif char == ')':
            p.value -= 1
        elif char == ':':
            p.value = p.spin



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
