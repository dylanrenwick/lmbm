# Lean Mean Bean Machine

## How to use

LMBM is a Plinko-inspired 2d esoteric language, with a focus on randomness.

At the start of the program's execution, each row of code is right-padded with spaces to the length of the longest row, and an instruction pointer, referred to as a marble, is spawned at every uppercase `O` in the code.  
These marbles always begin with a spin to the right, and a value of 0.

Every tick, each marble will drop down one character, then run the command, or "peg" it is on.  
Marbles are calculated based on where they spawned, those that spawned in the top left will run first, then going across, then down.

After moving, if a marble is outside the bounds of the code, it is destroyed.

The program terminates when all marbles are destroyed.

### Pegs

Any character that is not a valid peg is essentially a comment or no-op, including spaces.

    0-9    - Sets the marble's value to the single digit integer
    U      - Destroys the marble and prints its value as a Unicode character
    u      - Destroys the marble and prints its value
    /      - Moves the marble to the left, and sets its spin to left
    \      - Moves the marble to the right, and sets its spin to right
    |      - Reverses the marble's current spin and horizontal direction
    v      - Halts any horizontal movement
    o      - Moves the marble one space in the direction of its spin, and creates a second marble with 
             the same value but opposite spin, and moves it one space in the opposite direction
    "      - Enters the marble into string mode, the marble's value will be set to the Unicode 
             codepoint of the next peg it reaches, including no-ops
    !      - Prints the marble's value as a Unicode character
    $      - Prints the marble's value
    ^      - Moves the marble left or right with a uniformly random probability
    ?      - If the marble's value is truthy (not zero) set its spin to right, otherwise set its spin to left
    _      - Move one space in the direction of the marble's spin
    ~      - Trampoline the marble up to the top of it's current column
    i      - Read one number or one character from STDIN and set the marble's value to it
    +*/-%# - Mathematical operators, the first marble to hit these are "held", and upon a second marble 
             hitting the peg, the held marble's value is applied to the second marble using the relevant
             operator, then the held marble is destroyed, note that # is exponentiation
    ;      - Destroy the marble
    (      - Increment the marble's value
    )      - Decrement the marble's value
    :      - Set the marble's value to its spin (Right is 1, Left is 0)
    T      - Set the marble's value to 10
    x      - Set the marble's value to its x position in the code
    y      - Set the marble's value to its y position in the code
