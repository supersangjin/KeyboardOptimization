import random

WIDTH_KEY_DEFAULT = 100
WIDTH_EMPTY_DEFAULT = 5
START_FIRST_AXIS = 0
START_SECOND_AXIS = 20
START_THIRD_AXIS = START_SECOND_AXIS + WIDTH_KEY_DEFAULT + WIDTH_EMPTY_DEFAULT
WIDTH_KEY_AND_EMPTY = WIDTH_KEY_DEFAULT + WIDTH_EMPTY_DEFAULT
DEFAULT_END_AXIS = 9 * WIDTH_KEY_AND_EMPTY + WIDTH_KEY_DEFAULT
NUM_ITERATION = 100000

output = open("example.txt", "w")

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
for i in range(NUM_ITERATION):
    output.write(("%s %s\n") % (alphabet[random.randint(-1,25)], random.randint(START_FIRST_AXIS - 1, DEFAULT_END_AXIS))) 
