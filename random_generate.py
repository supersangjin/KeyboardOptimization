import random
import usr_kbd_model

NUM_ITERATION = 100000

output = open("example.txt", "w")
user_model = usr_kbd_model.KBDModel("output.csv")
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
for i in range(NUM_ITERATION):
    rand = random.randint(-1, 25)
    sample = user_model.get_keystroke(alphabet[rand])
    output.write(("%s %s\n") % (alphabet[rand], sample))
