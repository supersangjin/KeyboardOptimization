import getopt # get input data

class Data:
    def __init__(self, alphabet, x): # target alphabet, user input x-coordinate
        self.alphabet = alphabet
        self.x = x

    def getUser(self):
        return self.user

    def getAlphabet(self):
        return self.alphabet

    def getX(self):
        return self.x

class DataList: # Collection of user data
    def __init__(self, user):
        self.dataList = []
        self.user = user

    def addData(self, data):
        self.dataList.append(data)

class Node:
    def __init__(self, alphabet, x): # alphabet, center x-coordinate,
        self.alphabet = alphabet
        self.x = x
        self.weight = 0 # 0 ~ 10
        self.width = 0

    def getAlphabet(self):
        return self.alphabet

    def getX(self):
        return self.x

    def getWeight(self):
        return self.weight

    def getWidth(self):
        return self.width

class Layer:
    def __init__(self, layer): # layer = 0 or 1 or 2
        self.nodeList = []
        self.layer = layer

    def initialize(self):
        if (self.layer == 0):
            q = Node('q',0.0)
            w = Node('w',0.0)
            e = Node('e',0.0)
            r = Node('r',0.0)
            t = Node('t',0.0)
            y = Node('y',0.0)
            u = Node('u',0.0)
            i = Node('i',0.0)
            o = Node('o',0.0)
            p = Node('p',0.0)
            self.nodeList = [q, w, e, r, t, y, u, i, o, p]
        elif (self.layer == 1):
            a = Node('a',0.0)
            s = Node('s',0.0)
            d = Node('d',0.0)
            f = Node('f',0.0)
            g = Node('g',0.0)
            h = Node('h',0.0)
            j = Node('j',0.0)
            k = Node('k',0.0)
            l = Node('l',0.0)
            self.nodeList = [a, s, d, f, g, h, j, k, l]
        elif (self.layer == 2):
            z = Node('z',0.0)
            x = Node('x',0.0)
            c = Node('c',0.0)
            v = Node('v',0.0)
            b = Node('b',0.0)
            n = Node('n',0.0)
            m = Node('m',0.0)
            self.nodeList = [z, x, c, v, b, n, m]

    def normalize(self): # TODO calculate x-coordnate and width according to each node's weight

    def calculateFitness(self): # TODO calculate fitness of the layer

    def


class Keyboard:
    def __init__(self, user):
        self.layerList = []
        self.user = user

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

    def calculateFitness(self):


if __name__ == 'main':
    # parse data from input

    # make Keyboard
    keyboard = Keyboard('user')
    keyboard.initialize()

    # TODO make search problem
