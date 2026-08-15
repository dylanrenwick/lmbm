# Lean Mean Bean Machine

## How to use

LMBM is a Plinko-inspired 2d esoteric language, with a focus on randomness.

At the start of the program's execution, each row of code is right-padded with spaces to the length of the longest row, and an instruction pointer, referred to as a bean, is spawned at every uppercase `O` in the code.  
These beans always begin with a spin to the right (1), and a value of 0.

Every tick, each bean will drop down one character, then run the command, or "peg" it is on.  
Beans are calculated based on where they spawned, those that spawned in the top left will run first, then going across, then down.

After moving, if a bean is outside the bounds of the code, it is destroyed.

The program terminates when all beans are destroyed.

### Pegs

Any character that is not a valid peg is essentially a comment or no-op, including spaces.  
Note that despite being the standard spawn point for beans, `O` is otherwise considered a no-op.

    0-9    - Sets the bean's value to the single digit integer
    U      - Destroys the bean and prints its value as a Unicode character
    u      - Destroys the bean and prints its value
    /      - Moves the bean to the left, and sets its spin to -1
    \      - Moves the bean to the right, and sets its spin to 1
    |      - Reverses the bean's current spin
    v      - Halts any horizontal movement
    o      - Duplicates the bean, outputting one copy to the left and the other to the right
           - Each copy has its spin set according to the direction it was output
    "      - Enters the bean into string mode, the bean's value will be set to the Unicode 
             codepoint of the next peg it reaches, including no-ops
    !      - Prints the bean's value as a Unicode character
    $      - Prints the bean's value
    ^      - Moves the bean left or right with a uniformly random probability
    ?      - If the bean's value is truthy (not zero) set its spin to right, otherwise set its spin to left
    _      - Move left if the bean's spin is -1, and right if the bean's spin is 1
    ~      - Trampoline the bean up to the top of it's current column
    =      - Acts as "top of column" for any trampolines below it in the same column
    i      - Read one number or one character from STDIN and set the bean's value to it
           - Sets the bean's spin to 1 if a value was read, and -1 if EOF is found
           - If EOF is found, the bean's value is unchanged
    +      - Dyadic addition
    *      - Dyadic multiplication
    -      - Dyadic subtraction
    %      - Dyadic modulus
    &      - Dyadic division (design note: / is already taken)
    #      - Dyadic exponent (design note: ^ is already taken)
    @      - Dyadic sort, outputs lower value to left, higher value to right
    ;      - Destroy the bean
    (      - Increment the bean's value
    )      - Decrement the bean's value
    [      - Dyadic min; hold first bean until a second hits, output the lower value and destroy the other
    ]      - Dyadic max; hold first bean until a second hits, output the higher value and destroy the other
    :      - Set the bean's value to its spin (Right is 1, Left is -1)
    T      - Set the bean's value to 10
    x      - Set the bean's value to its x position in the code
    y      - Set the bean's value to its y position in the code
	`      - Destroys all beans, silently terminating
    ,      - Holds the bean here for 1 tick
    .      - Holds the bean here for a number of ticks equal to the bean's value

Dyadic pegs are pegs that take 2 separate beans as input. When the first bean reaches a dyadic peg, that bean will be held there until a second bean hits the peg. At that time, the operator will process with both beans as inputs.  
When a dyadic peg's operand order matters, eg subtract, exponent, and divide, bean operands are ordered in the order they arrived at the peg. 

Pegs with 2 outputs such as `o` and `@` will set the beans' spins accordingly; the bean output to the left will have a spin of -1, and the bean output to the right will have a spin of 1.

