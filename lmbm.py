import argparse
import random
from pathlib import Path
from sys import argv

class Pointer:
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
        self.spin = 1
        self.string = False
        self.pause = 0
    def __repr__(self):
        return str('Pointer %s(%s, %s, val=%s, alv=%s, hld=%s)' % (self.id, [self.x, self.y], 'Right' if self.spin > 0 else 'Left', self.value, self.alive, self.held))

def get_held_operators(pointer_list, pointer):
    held_pointers = [p for p in pointer_list if p.x == pointer.x and p.y == pointer.y and p.held and p.alive]
    vprint('  Found %s held pointers' % len(held_pointers))
    return held_pointers if held_pointers else False

def hold_for_all(pointer_list, pointer, operand_count):
    held = get_held_operators(pointer_list, pointer)
    if not held or len(held) < operand_count - 1:
        vprint('  Holding pointer at [%s, %s]' % (pointer.x, pointer.y))
        pointer.held = True
        return False
    else:
        held.append(pointer)
        return held

def is_int(s):
    try:
        return int(s)
    except ValueError:
        return False

def vprint(obj):
    global verbose
    if verbose: print(str(obj))

def main():
    parser = argparse.ArgumentParser('lmbm')
    parser.add_argument('file', type=Path)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-t', '--ticks', type=int, default=0)
    args = parser.parse_args()

    if not args.file.is_file():
        print('File %s not found!' % args.file)
        return

    global verbose
    verbose = args.verbose

    vprint('Reading %s' % args.file)
    with open(args.file,'r') as f:
        code = f.read()
    lines = code.splitlines()
    width = max([len(l) for l in lines])
    vprint('Normalizing width to %s' % width)
    for i in range(0, len(lines)):
        if len(lines[i]) < width:
            lines[i] += ' ' * (width - len(lines[i]))
    grid = [[ch for ch in l] for l in lines]
    vprint('Parsed grid as:')
    vprint(grid)

    origins = []
    for y in range(0, len(lines)):
        for x in range(0, width):
            ch = grid[y][x]
            if ch == 'O':
                origins.append([y, x])
    vprint('Found origins: %s' % origins)

    pointers = []
    for i in range(0, len(origins)):
        pointers.append(Pointer(origins[i], i))
    vprint(pointers)

    input_buffer = []

    while True:
        if not any([p.alive for p in pointers]):
            break

        vprint(pointers)
        new_pointers = []
        for p in pointers:
            if p.held or not p.alive:
                continue
            if p.pause > 0:
                p.pause -= 1
                if p.pause > 0:
                    continue
                else:
                    vprint('  Pointer %s done pausing' % p.id)

            p.x += p.xvel
            p.y += p.yvel
            vprint('Moving pointer %s: [%s, %s], new pos is [%s, %s]' % (p.id, p.xvel, p.yvel, p.x, p.y))
            if p.x >= width or p.x < 0 or p.y >= len(lines) or p.y < 0:
                vprint('Pointer %s has coords [%s, %s], killing' % (p.id, p.x, p.y))
                p.alive = False
                continue

            char = grid[p.y][p.x]
            vprint('Pointer %s is at char %s' % (p.id, char))
            digit = is_int(char)

            # string mode
            if p.string:
                vprint('  Setting pointer to %s' % ord(char))
                p.value = ord(char)
                p.string = False
            elif char == '"':
                vprint('  Entering string mode')
                p.string = True
            # consts
            elif digit is not False:
                vprint('  Setting value to %s' % digit)
                p.value = digit
            elif char == 'T':
                vprint('  Setting value to 10')
                p.value = 10
            # terminals
            elif char == ';':
                vprint('  Killing pointer')
                p.alive = False
            elif char == 'U':
                vprint('  Killing pointer and printing value as char')
                p.alive = False
                print(chr(p.value), end='')
            elif char == 'u':
                vprint('  Killing pointer and printing value')
                p.alive = False
                print(p.value, end='')
            elif char == '`':
                vprint('Terminating')
                for pntr in pointers:
                    pntr.alive = False
            # control
            elif char == '/':
                vprint('  Moving pointer left')
                p.x -= 1
                p.spin = -1
            elif char == '\\':
                vprint('  Moving pointer right')
                p.x += 1
                p.spin = 1
            elif char == '_':
                vprint('  Moving %s' % ('Left' if p.spin == -1 else 'Right'))
                p.x += p.spin
            elif char == '^':
                newDir = random.choice([0, 1])
                vprint('  Random number is %s' % newDir)
                p.spin = newDir
                p.x += newDir if newDir else -1
            elif char == '~':
                vprint('  Trampolining pointer to top')
                p.y -= 1
                while p.y >= 0 and grid[p.y][p.x] != '=':
                    p.y -= 1
                vprint('  Found top at %s' % p.y)
            # spin
            elif char == '|':
                vprint('  Reflecting pointer direction')
                p.spin = -p.spin
            elif char == ':':
                vprint('  Pointer spin is %s, setting value to %s' % (('Right' if p.spin == 1 else 'Left'), p.spin))
                p.value = p.spin
            # comparison
            elif char == '?':
                vprint('  Value of %s is %szero' % (p.value, 'non-' if p.value else ''))
                if p.value:
                    p.spin = 1
                else:
                    p.spin = -1
            elif char == '@':
                held = hold_for_all(pointers, p, 2)
                if held:
                    left = held[1] if held[1].value < held[0].value else held[0]
                    right = held[0] if held[1].value < held[0].value else held[1]
                    left.x -= 1
                    left.spin = -1
                    right.x += 1
                    right.spin = 1
            elif char == '[':
                held = hold_for_all(pointers, p, 2)
                if held:
                    result = min(held[0].value, held[1].value)
                    vprint('  min(%s, %s) = %s' % (held[0].value, held[1].value, result))
                    held[1].value = result
                    held[0].alive = False
            elif char == ']':
                held = hold_for_all(pointers, p, 2)
                if held:
                    result = max(held[0].value, held[1].value)
                    vprint('  max(%s, %s) = %s' % (held[0].value, held[1].value, result))
                    held[1].value = result
                    held[0].alive = False
            # arithmetic
            elif char == '+':
                held = hold_for_all(pointers, p, 2)
                if held:
                    result = held[0].value + held[1].value
                    vprint('  %s + %s = %s' % (held[0].value, held[1].value, result))
                    held[1].value = result
                    held[0].alive = False
            elif char == '*':
                held = hold_for_all(pointers, p, 2)
                if held:
                    result = held[0].value * held[1].value
                    vprint('  %s * %s = %s' % (held[0].value, held[1].value, result))
                    held[1].value = result
                    held[0].alive = False
            elif char == '-':
                held = hold_for_all(pointers, p, 2)
                if held:
                    result = held[0].value - held[1].value
                    vprint('  %s - %s = %s' % (held[0].value, held[1].value, result))
                    held[1].value = result
                    held[0].alive = False
            elif char == '&':
                held = hold_for_all(pointers, p, 2)
                if held:
                    result = held[0].value / held[1].value
                    vprint('  %s / %s = %s' % (held[0].value, held[1].value, result))
                    held[1].value = result
                    held[0].alive = False
            elif char == '#':
                held = hold_for_all(pointers, p, 2)
                if held:
                    result = held[0].value ** held[1].value
                    vprint('  %s ** %s = %s' % (held[0].value, held[1].value, result))
                    held[1].value = result
                    held[0].alive = False
            elif char == '%':
                held = hold_for_all(pointers, p, 2)
                if held:
                    result = held[0].value % held[1].value
                    vprint('  %s % %s = %s' % (held[0].value, held[1].value, result))
                    held[1].value = result
                    held[0].alive = False
            # math
            elif char == 'a':
                vprint('  Absoluting')
                p.value = abs(p.value)
            elif char == '(':
                vprint('  Incrementing')
                p.value += 1
            elif char == ')':
                vprint('  Decrementing')
                p.value -= 1
            # input
            elif char == 'i':
                # read input to buffer
                if len(input_buffer) == 0:
                    vprint('  Reading next line of input')
                    try:
                        inp = input()
                    except EOFError:
                        inp = ''
                    if len(inp) == 0:
                        vprint('  Input was empty')
                    else:
                        if is_int(inp) is not False:
                            vprint('  Input was int %s' % inp)
                        else:
                            vprint('  Input was "%s"' % inp)
                        input_buffer = list(inp)
                # input empty
                if len(input_buffer) == 0:
                    vprint('  No input, spinning left')
                    p.spin = -1
                else:
                    read_value = is_int(''.join(input_buffer))
                    # take first char if not int
                    if read_value is False:
                        next_chr = input_buffer.pop(0)
                        vprint('  Read %s from input' % next_chr)
                        read_value =  ord(next_chr)
                    # clear input buffer if int
                    else:
                        input_buffer.clear()
                    p.spin = 1
                    p.value = read_value
            # output
            elif char == '!':
                vprint('  Printing value as char')
                print(chr(p.value), end='')
            elif char == '$':
                vprint('  Printing value')
                print(p.value, end='')
            # split
            elif char == 'o':
                vprint('  Creating new marble')
                new_pointer = Pointer([p.y, p.x - 1], len(pointers))
                new_pointer.spin = -1
                new_pointer.value = p.value
                new_pointers.append(new_pointer)
                p.x += 1
                p.spin = 1
            # pause
            elif char == ',':
                vprint('  Pausing pointer for 1 tick')
                p.pause = 2
            elif char == '.':
                vprint('  Pausing pointer for %s ticks' % p.value)
                p.pause = p.value + 1
        for p in new_pointers:
            pointers.append(p)

if __name__ == '__main__':
    main()

