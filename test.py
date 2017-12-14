import sys
import random
import argparse
import usr_kbd_model

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
layer_1 = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]
layer_2 = ["a", "s", "d", "f", "g", "h", "j", "k", "l"]
layer_3 = ["z", "x", "c", "v", "b", "n", "m"]
TEST_NUM = 100000

keyboard_layer_1 = []
keyboard_layer_2 = []
keyboard_layer_3 = []


def test(args):
    file = open(args.keyboard_file, 'r')
    keyboard_list = file.readlines()
    file.close()
    n = 0
    for node in keyboard_list:
        if n < 9:
            keyboard_layer_1.append(float(node))
        elif n < 17:
            keyboard_layer_2.append(float(node))
        else:
            keyboard_layer_3.append(float(node))
        n += 1

    # User Keyboard Model
    user_model = usr_kbd_model.KBDModel(args.data_file)

    print("\nKeyboard Layout\n")
    print(keyboard_layer_1)
    print(keyboard_layer_2)
    print(keyboard_layer_3)
    print("\nTesting for " + str(TEST_NUM) + " samples")


    total_correct = 0
    for i in range(TEST_NUM):
        rand = random.randint(0, 25)
        sample = user_model.get_keystroke(alphabet[rand])
        if alphabet[rand] in layer_1:
            node = layer_1.index(alphabet[rand])
            if node == 0:
                if sample < keyboard_layer_1[0]:
                    total_correct += 1
            elif node == 9:
                if keyboard_layer_1[-1] < sample:
                    total_correct += 1
            else:
                if keyboard_layer_1[node - 1] < sample < keyboard_layer_1[node]:
                    total_correct += 1
        elif alphabet[rand] in layer_2:
            node = layer_2.index(alphabet[rand])
            if node == 0:
                if sample < keyboard_layer_2[0]:
                    total_correct += 1
            elif node == 8:
                if keyboard_layer_2[-1] < sample:
                    total_correct += 1
            else:
                if keyboard_layer_2[node - 1] < sample < keyboard_layer_2[node]:
                    total_correct += 1
        else:
            node = layer_3.index(alphabet[rand])
            if node == 0:
                if sample < keyboard_layer_3[0]:
                    total_correct += 1
            elif node == 6:
                if keyboard_layer_3[-1] < sample:
                    total_correct += 1
            else:
                if keyboard_layer_3[node - 1] < sample < keyboard_layer_3[node]:
                    total_correct += 1

    print("\nOut of " + str(TEST_NUM) + " user inputs " + str(TEST_NUM - total_correct) + " typos")
    print(str((TEST_NUM - total_correct)*100/float(TEST_NUM)) + " % typos")


def main(args):
    # if len(sys.argv) != 2:
    #     sys.stderr.write("Usage : python3 test.py keyboard.txt\n")
    #     sys.exit(9)
    # file = sys.argv[1]
    # if not file.endswith(".txt"):
    #     sys.stderr.write("input file should be .txt\n")
    #     sys.exit(9)
    test(args)


if __name__ == "__main__":
    if sys.version_info[0] is not 3:
        print("ERROR: Please use Python version 3. (Your version: {0})".format(sys.version))
        exit(1)

    description = ("Test keyboard accuracy")

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("keyboard_file",
                        type=str,
                        default="keyboard.txt",
                        help="File containing the to-test keyboard")
    parser.add_argument("-f",
                        "--data-file",
                        type=str,
                        help="File from which to read test data",
                        default="output.csv")
    parser.add_argument("-v",
                        "--verbose",
                        help="Print information about the program results",
                        action="store_true")
    parser.add_argument("-d",
                        "--debug",
                        help="Print information about the program execution (Has temporarily no effect)",
                        action="store_true")
    args = parser.parse_args()

    main(args)