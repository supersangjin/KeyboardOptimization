import random
import usr_kbd_model

WIDTH_KEY_DEFAULT = 0.05
WIDTH_EMPTY_DEFAULT = 0.0555555556
START_FIRST_AXIS = 0.00952
START_SECOND_AXIS = 0.0571428
START_THIRD_AXIS = 0.158730158
WIDTH_KEY_AND_EMPTY = WIDTH_KEY_DEFAULT + WIDTH_EMPTY_DEFAULT
DEFAULT_END_AXIS = 9 * WIDTH_KEY_AND_EMPTY + WIDTH_KEY_DEFAULT
NUM_ITERATION = 10
PERMUTATION_LIST = [[], [], []]
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
SAMPLE_ITERATION = 100000


class Node:
    def __init__(self, alphabet, x): # alphabet, center x-coordinate,
        self.alphabet = alphabet
        self.x = x
        self.original_weight = 0 # 0 ~ 10
        self.weight = 0 # 0 ~ 10
        self.max_weight = 0 # 0 ~ 10
        self.width = WIDTH_KEY_DEFAULT
        self.normalized_left = WIDTH_EMPTY_DEFAULT/2.0
        self.normalized_right = WIDTH_EMPTY_DEFAULT/2.0
    
    def __str__(self):
        return "%s:%s" % (self.alphabet, self.weight)


    def getAlphabet(self):
        return self.alphabet

    def getX(self):
        return self.x

    def getWeight(self):
        return self.weight

    def getWidth(self):
        return self.width
    
    def get_N_left_right(self):
        return (self.normalized_left, self.normalized_right)

class Layer:
    def __init__(self, layer): # layer = 0 or 1 or 2
        self.nodeList = []
        self.layer = layer

    def initialize(self):
        if (self.layer == 0):
            q = Node('q',START_FIRST_AXIS)
            w = Node('w',START_FIRST_AXIS + WIDTH_KEY_AND_EMPTY)
            e = Node('e',START_FIRST_AXIS + 2 * WIDTH_KEY_AND_EMPTY)
            r = Node('r',START_FIRST_AXIS + 3 * WIDTH_KEY_AND_EMPTY)
            t = Node('t',START_FIRST_AXIS + 4 * WIDTH_KEY_AND_EMPTY)
            y = Node('y',START_FIRST_AXIS + 5 * WIDTH_KEY_AND_EMPTY)
            u = Node('u',START_FIRST_AXIS + 6 * WIDTH_KEY_AND_EMPTY)
            i = Node('i',START_FIRST_AXIS + 7 * WIDTH_KEY_AND_EMPTY)
            o = Node('o',START_FIRST_AXIS + 8 * WIDTH_KEY_AND_EMPTY)
            p = Node('p',START_FIRST_AXIS + 9 * WIDTH_KEY_AND_EMPTY)
            self.nodeList = [q, w, e, r, t, y, u, i, o, p]
        elif (self.layer == 1):
            a = Node('a',START_SECOND_AXIS)
            s = Node('s',START_SECOND_AXIS + WIDTH_KEY_AND_EMPTY)
            d = Node('d',START_SECOND_AXIS + 2 * WIDTH_KEY_AND_EMPTY)
            f = Node('f',START_SECOND_AXIS + 3 * WIDTH_KEY_AND_EMPTY)
            g = Node('g',START_SECOND_AXIS + 4 * WIDTH_KEY_AND_EMPTY)
            h = Node('h',START_SECOND_AXIS + 5 * WIDTH_KEY_AND_EMPTY)
            j = Node('j',START_SECOND_AXIS + 6 * WIDTH_KEY_AND_EMPTY)
            k = Node('k',START_SECOND_AXIS + 7 * WIDTH_KEY_AND_EMPTY)
            l = Node('l',START_SECOND_AXIS + 8 * WIDTH_KEY_AND_EMPTY)
            self.nodeList = [a, s, d, f, g, h, j, k, l]
        elif (self.layer == 2):
            z = Node('z',START_THIRD_AXIS)
            x = Node('x',START_THIRD_AXIS + WIDTH_KEY_AND_EMPTY)
            c = Node('c',START_THIRD_AXIS + 2 * WIDTH_KEY_AND_EMPTY)
            v = Node('v',START_THIRD_AXIS + 3 * WIDTH_KEY_AND_EMPTY)
            b = Node('b',START_THIRD_AXIS + 4 * WIDTH_KEY_AND_EMPTY)
            n = Node('n',START_THIRD_AXIS + 5 * WIDTH_KEY_AND_EMPTY)
            m = Node('m',START_THIRD_AXIS + 6 * WIDTH_KEY_AND_EMPTY)
            self.nodeList = [z, x, c, v, b, n, m]

    def normalize(self): # TODO calculate x-coordnate and width according to each node's weight
        for i in range(len(self.nodeList)):
            if(i != (len(self.nodeList) - 1)):
                diff = self.nodeList[i].weight - self.nodeList[i+1].weight
                self.nodeList[i].normalized_right = WIDTH_EMPTY_DEFAULT / 2 + (diff / 10.0) * (WIDTH_EMPTY_DEFAULT / 2)
            if(i != 0):
                diff = self.nodeList[i].weight - self.nodeList[i-1].weight
                self.nodeList[i].normalized_left = WIDTH_EMPTY_DEFAULT / 2 + (diff / 10.0) * (WIDTH_EMPTY_DEFAULT / 2)
        
        
    def calculateFitness(self, data_list): # TODO calculate fitness of the layer
        num = 0
        for i in range(len(data_list)):
            node = self.get_node(data_list[i][0])
            l_and_r = node.get_N_left_right()
            if((max(0, node.getX() - l_and_r[0]) <= (float)(data_list[i][1])) and ((float)(data_list[i][1]) <= min(node.getX() + WIDTH_KEY_DEFAULT + l_and_r[1], DEFAULT_END_AXIS))):
                num = num + 1
   
        return num
    
    def get_node(self, char): # get node from the alphabet. 'a' -> get node a
        for i in range(len(self.nodeList)):
            if(char == self.nodeList[i].getAlphabet()):
                return self.nodeList[i]        

    def explore_neighborhood(self, data_list): # search all the neighborhoods of given layer
        max_fitness = self.calculateFitness(data_list)
        for i in range(len(self.nodeList)): # original weight is assumed to be maximum, at first.
            self.nodeList[i].max_weight = self.nodeList[i].original_weight
        
        if(len(PERMUTATION_LIST[self.layer]) == 0):
            for i in range(len(self.nodeList)): # to search all the neighborhoods, make permutation
                PERMUTATION_LIST[self.layer].append([-1, 0, 1])
            PERMUTATION_LIST[self.layer] = make_permutation(PERMUTATION_LIST[self.layer])
        for i in range(len(PERMUTATION_LIST[self.layer])):
            end = 0
            for j in range(len(self.nodeList)):
                self.nodeList[j].weight = self.nodeList[j].original_weight + PERMUTATION_LIST[self.layer][i][j]
                if(self.nodeList[j].weight < 0 or self.nodeList[j].weight > 10):
                    end = 1
                    break
            if(end == 1):
                continue
            self.normalize() # apply the weight to change the space in between nodes
            new_fitness = self.calculateFitness(data_list)
            #print(new_fitness, max_fitness)
            #if(new_fitness != max_fitness):
            #    print(new_fitness, max_fitness)
            if(new_fitness >= max_fitness):
                for k in range(len(self.nodeList)):
                    self.nodeList[k].max_weight = self.nodeList[k].weight
                    max_fitness = new_fitness
        for i in range(len(self.nodeList)):
            self.nodeList[i].original_weight = self.nodeList[i].max_weight
            self.nodeList[i].weight = self.nodeList[i].max_weight
        self.normalize()
        
        
class Keyboard:
    def __init__(self, user):
        self.layerList = []
        self.user = user

    def __str__(self):
        str_keyboard = ""
        for i in range(3):
            for elem in self.getLayer(i).nodeList:
                str_keyboard += str(elem)
                str_keyboard += " "
            str_keyboard += "\n"
        return str_keyboard
    
    def initialize(self):
        layer_0 = Layer(0)
        layer_0.initialize()
        layer_1 = Layer(1)
        layer_1.initialize()
        layer_2 = Layer(2)
        layer_2.initialize()
        self.addLayer(layer_0)
        self.addLayer(layer_1)
        self.addLayer(layer_2)

    def addLayer(self, layer): # Must add 1 layer -> 2 layer -> 3 layer in order
        self.layerList.append(layer)

    def getList(self):
        return self.layerList

    def getLayer(self, n): # return nth layer
        return self.layerList[n]
            
    def calculateFitness(self, data_list): # to optimize each layer, return fitness_list : list of fitness of each layer
        Fitness_List = []
        for i in range(3):
            Fitness_List.append (self.getLayer(i).calculateFitness(data_list[i]))
        return Fitness_List

    def get_layer(self, char): # from the alphabet, get the layer. ex) q -> layer 0, a -> layer 1, z -> layer 2
        for i in range(3):
            for elem in self.getLayer(i).nodeList:
                if(char == elem.getAlphabet()):
                    return i

            
    def seperate_data(self, data_list): # make new list of 3 lists from the data list, each list is containing data for each layer
        new_data_list = [[], [], []]
        for i in range(len(data_list)):
            new_data_list[self.get_layer(data_list[i][0])].append(data_list[i])
        return new_data_list

    def explore_neighborhood(self, data_list): # search all the neighborhoods
        for i in range(3):
            self.getLayer(i).explore_neighborhood(data_list[i])
            

def parse_data(file_name):
    file = open(file_name, 'r')
    data_list = file.readlines()
    for i in range(len(data_list)):
        data_list[i] = data_list[i].strip('\n')
        data_list[i] = data_list[i].split(' ')
    return data_list


def make_permutation(permutation_list): # to explore all the neighborhoods, we need permutation. like n = 2 -> [-1,-1], [-1,0], [-1,1], ... , [1,1], the numbers to apply for each weight
    if(len(permutation_list) == 1):
        new_list = []
        for i in range(len(permutation_list[0])):
            new_list.append([permutation_list[0][i]])
        return new_list
    prev_comb_list = make_permutation(permutation_list[1:len(permutation_list)])
    new_list = []
    for i in range(len(permutation_list[0])):
        for j in range(len(prev_comb_list)):
            append_list = [permutation_list[0][i]]
            append_list.extend(prev_comb_list[j])
            new_list.append(append_list)
    return new_list
    
    
if __name__ == '__main__':
    # parse data from input
    #file_name = "example.txt"
    #data_list = parse_data(file_name)

    user_model = usr_kbd_model.KBDModel("output.csv")

    data_list = []
    for i in range(SAMPLE_ITERATION):
        rand = random.randint(0, 25)
        sample = user_model.get_keystroke(alphabet[rand])
        data_list.append([alphabet[rand], sample])
    
    # make Keyboard
    keyboard = Keyboard('user')
    keyboard.initialize()

    before = keyboard.calculateFitness(data_list)
    # TODO make search problem
    for i in range(NUM_ITERATION):
        data_list = []
        for j in range(SAMPLE_ITERATION):
            rand = random.randint(0, 25)
            sample = user_model.get_keystroke(alphabet[rand])
            data_list.append([alphabet[rand], str(sample)])
        # seperate data to each layer
        data_list = keyboard.seperate_data(data_list)
        keyboard.explore_neighborhood(data_list)
        print(str(NUM_ITERATION) + "th iteration " + str(sum(keyboard.calculateFitness(data_list))))
        print(keyboard)
    print("Before : " + str(sum(before)))
    print("After : " + str(sum(keyboard.calculateFitness(data_list))))
