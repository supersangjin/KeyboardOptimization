import os
import random
import argparse
import usr_kbd_model

from deap import base
from deap import creator
from deap import tools
from deap import gp

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

layer_1 = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]
layer_2 = ["a", "s", "d", "f", "g", "h", "j", "k", "l"]
layer_3 = ["z", "x", "c", "v", "b", "n", "m"]
SAMPLE_NUM = 5000
TEST_NUM = 1000


def run(args):
    # User Keyboard Model
    user_model = usr_kbd_model.KBDModel(args.data_file)

    def sample_layer(layer_num):
        sample_li = []
        for i in layer_num:
            sample_li.append(user_model.get_keystroke(i))
        return sample_li

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()

    # Attribute generator
    # Random float between 0 and 1
    toolbox.register("attr", random.random)

    # Structure initializers
    # Layer 1
    toolbox.register("individual_1", tools.initRepeat, creator.Individual, toolbox.attr, 9)
    # Layer 2
    toolbox.register("individual_2", tools.initRepeat, creator.Individual, toolbox.attr, 8)
    # Layer 3
    toolbox.register("individual_3", tools.initRepeat, creator.Individual, toolbox.attr, 6)

    # define the population to be a list of individuals
    # Layer 1
    toolbox.register("population_1", tools.initRepeat, list, toolbox.individual_1)
    # Layer 2
    toolbox.register("population_2", tools.initRepeat, list, toolbox.individual_2)
    # Layer 3
    toolbox.register("population_3", tools.initRepeat, list, toolbox.individual_3)

    # the goal ('fitness') function to be maximized
    def fitness(individual, layer_num):
        total_correct = 0
        for i in range(SAMPLE_NUM):
            correct = 0
            sample_li = sample_layer(layer_num)
            # Left most key
            if sample_li[0] < individual[0]:
                correct += 1
            # Middle keys
            for j in range(1, len(individual)):
                if individual[j - 1] < sample_li[j] < individual[j]:
                    correct += 1
            # Right most key
            if individual[-1] < sample_li[-1]:
                correct += 1
            total_correct += correct
        return total_correct / float(SAMPLE_NUM),

    # ----------
    # Operator registration
    # ----------
    # register the goal / fitness function
    toolbox.register("evaluate_1", fitness, layer_num=layer_1)
    toolbox.register("evaluate_2", fitness, layer_num=layer_2)
    toolbox.register("evaluate_3", fitness, layer_num=layer_3)

    # register the crossover operator
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.decorate("mate", gp.staticLimit(key=max, max_value=1.0))

    # register a mutation operator with a probability to
    # mutate each attribute/gene of 0.05
    toolbox.register("mutate", tools.mutGaussian, mu=0.0, sigma=0.02, indpb=0.2)
    toolbox.decorate("mutate", gp.staticLimit(key=max, max_value=1.0))

    # operator for selecting individuals for breeding the next
    # generation: each individual of the current generation
    # is replaced by the 'fittest' (best) of three individuals
    # drawn randomly from the current generation.
    toolbox.register("select", tools.selTournament, tournsize=args.tournament_size)
    main(args, toolbox, user_model)


# ----------

def main(args, toolbox, user_model):
    random.seed(64)
    GENERATION_NUM = args.num_generations

    # create an initial population of 100 individuals each for layer
    pop_1 = toolbox.population_1(n=args.pop_size)
    pop_2 = toolbox.population_2(n=args.pop_size)
    pop_3 = toolbox.population_3(n=args.pop_size)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2

    print("Start of evolution")

    # Evaluate the entire population
    # Layer 1
    fitnesses = list(map(toolbox.evaluate_1, pop_1))
    for ind, fit in zip(pop_1, fitnesses):
        ind.fitness.values = fit
    print("  Evaluated %i individuals for layer 1" % len(pop_1))

    # Layer 2
    fitnesses = list(map(toolbox.evaluate_2, pop_2))
    for ind, fit in zip(pop_2, fitnesses):
        ind.fitness.values = fit
    print("  Evaluated %i individuals for layer 2" % len(pop_2))

    # Layer 3
    fitnesses = list(map(toolbox.evaluate_3, pop_3))
    for ind, fit in zip(pop_3, fitnesses):
        ind.fitness.values = fit
    print("  Evaluated %i individuals for layer 3" % len(pop_3))

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while g < GENERATION_NUM:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring_1 = toolbox.select(pop_1, len(pop_1))
        offspring_2 = toolbox.select(pop_2, len(pop_2))
        offspring_3 = toolbox.select(pop_3, len(pop_3))

        # Clone the selected individuals
        offspring_1 = list(map(toolbox.clone, offspring_1))
        offspring_2 = list(map(toolbox.clone, offspring_2))
        offspring_3 = list(map(toolbox.clone, offspring_3))

        # Apply crossover and mutation on the offspring
        # Layer 1 crossover
        for child1, child2 in zip(offspring_1[::2], offspring_1[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        # Layer 2 crossover
        for child1, child2 in zip(offspring_2[::2], offspring_2[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        # Layer 3 crossover
        for child1, child2 in zip(offspring_3[::2], offspring_3[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        # Layer 1 mutation
        for mutant in offspring_1:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Layer 2 mutation
        for mutant in offspring_2:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Layer 3 mutation
        for mutant in offspring_3:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Sort the individual
        # Layer 1 sort
        for individual in offspring_1:
            individual.sort()
        # Layer 2 sort
        for individual in offspring_2:
            individual.sort()
        # Layer 3 sort
        for individual in offspring_3:
            individual.sort()

        # Evaluate the individuals with an invalid fitness
        # Layer 1
        invalid_ind = [ind for ind in offspring_1 if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate_1, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        print("  Evaluated %i individuals in layer 1" % len(invalid_ind))

        # Layer 2
        invalid_ind = [ind for ind in offspring_2 if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate_2, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        print("  Evaluated %i individuals in layer 2" % len(invalid_ind))

        # Layer 3
        invalid_ind = [ind for ind in offspring_3 if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate_3, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals in layer 3" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop_1[:] = offspring_1
        pop_2[:] = offspring_2
        pop_3[:] = offspring_3

        # Gather all the fitnesses in one list and print the stats
        fits_1 = [ind.fitness.values[0] for ind in pop_1]
        fits_2 = [ind.fitness.values[0] for ind in pop_2]
        fits_3 = [ind.fitness.values[0] for ind in pop_3]

        # Layer 1
        length_1 = len(pop_1)
        mean_1 = sum(fits_1) / length_1
        sum2_1 = sum(x * x for x in fits_1)
        std_1 = abs(sum2_1 / length_1 - mean_1 ** 2) ** 0.5

        # Layer 2
        length_2 = len(pop_2)
        mean_2 = sum(fits_2) / length_2
        sum2_2 = sum(x * x for x in fits_2)
        std_2 = abs(sum2_2 / length_2 - mean_2 ** 2) ** 0.5

        # Layer 3
        length_3 = len(pop_3)
        mean_3 = sum(fits_3) / length_3
        sum2_3 = sum(x * x for x in fits_3)
        std_3 = abs(sum2_3 / length_3 - mean_3 ** 2) ** 0.5

        print("      \t\tLayer 1\t\tLayer 2\t\tLayer 3")
        print("  Min \t\t%.5f\t\t%.5f\t\t%.5f" % (min(fits_1), min(fits_2), min(fits_3)))
        print("  Max \t\t%.5f\t\t%.5f\t\t%.5f" % (max(fits_1), max(fits_2), max(fits_3)))
        print("  Avg \t\t%.5f\t\t%.5f\t\t%.5f" % (mean_1, mean_2, mean_3))
        print("  Std \t\t%.5f\t\t%.5f\t\t%.5f" % (std_1, std_2, std_3))

    print("-- End of (successful) evolution --")

    best_ind_1 = tools.selBest(pop_1, 1)[0]
    best_ind_2 = tools.selBest(pop_2, 1)[0]
    best_ind_3 = tools.selBest(pop_3, 1)[0]
    print("Best Keyboard")
    print("Layer 1")
    for i in range(len(best_ind_1)):
        print(layer_1[i] + " : " + str(best_ind_1[i]))
    print("Layer 2")
    for i in range(len(best_ind_2)):
        print(layer_2[i] + " : " + str(best_ind_2[i]))
    print("Layer 3")
    for i in range(len(best_ind_3)):
        print(layer_3[i] + " : " + str(best_ind_3[i]))

    print("\n\nTesting for " + str(TEST_NUM) + " samples")

    total_correct = 0
    for i in range(TEST_NUM):
        rand = random.randint(0, 25)
        sample = user_model.get_keystroke(alphabet[rand])
        if alphabet[rand] in layer_1:
            node = layer_1.index(alphabet[rand])
            if node == 0:
                if sample < best_ind_1[0]:
                    total_correct += 1
            elif node == 9:
                if best_ind_1[-1] < sample:
                    total_correct += 1
            else:
                if best_ind_1[node - 1] < sample < best_ind_1[node]:
                    total_correct += 1
        elif alphabet[rand] in layer_2:
            node = layer_2.index(alphabet[rand])
            if node == 0:
                if sample < best_ind_2[0]:
                    total_correct += 1
            elif node == 8:
                if best_ind_2[-1] < sample:
                    total_correct += 1
            else:
                if best_ind_2[node - 1] < sample < best_ind_2[node]:
                    total_correct += 1
        else:
            node = layer_3.index(alphabet[rand])
            if node == 0:
                if sample < best_ind_3[0]:
                    total_correct += 1
            elif node == 6:
                if best_ind_3[-1] < sample:
                    total_correct += 1
            else:
                if best_ind_3[node - 1] < sample < best_ind_3[node]:
                    total_correct += 1

    print("\nOut of " + str(TEST_NUM) + " user inputs " + str(TEST_NUM - total_correct) + " typos")
    print(str((TEST_NUM - total_correct) * 100 / float(TEST_NUM)) + " % typos")

    # Write keyboard layout to output file
    f = open(args.out, 'w')
    for i in best_ind_1:
        f.write(str(i) + "\n")
    for i in best_ind_2:
        f.write(str(i) + "\n")
    for i in best_ind_3:
        f.write(str(i) + "\n")
    f.close()


if __name__ == "__main__":
    def type_poupulation(x):
        x = int(x)
        if x < 10:
            raise argparse.ArgumentTypeError(
                "For this implementation the minimum number of individuals must be 10")
        return x

    def type_generations(x):
        x = int(x)
        if x < 1:
            raise argparse.ArgumentTypeError(
                "Min number of generations is 1")
        return x

    def type_tournament(x):
        x = int(x)
        if x < 2:
            raise argparse.ArgumentTypeError(
                "Size must be at least 2")
        return x

    def type_keyboard(kbd_name):
        counter = 1
        orig_name = kbd_name
        while kbd_name in os.listdir("."):
            kbd_name = orig_name + str(counter)
            counter += 1
        return kbd_name

    description = ("Find the optimal keyboard touchspace")

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("data_file",
                        # type=argparse.FileType("r"),
                        type=str,
                        help="File with the training data. default=output.csv",
                        default="output.csv")
    parser.add_argument("-o",
                        "--out",
                        type=type_keyboard,
                        help="File to which to save the generated keyboard. default=genetic_keyboard.txt",
                        default="genetic_keyboard.txt")
    parser.add_argument("-p",
                        "--pop-size",
                        help="Size of the initial population. default=40",
                        type=type_poupulation,
                        default=40)
    parser.add_argument("-n",
                        "--num-generations",
                        help="Number of iterations of the algorithm. default=100",
                        type=type_generations,
                        default=100)
    parser.add_argument("-t",
                        "--tournament-size",
                        help="number of individuals to select for the tournament selection process",
                        type=type_tournament,
                        default=3)
    parser.add_argument("-v",
                        "--verbose",
                        help="Print information about the program results (Has temporarily no effect)",
                        action="store_true")
    parser.add_argument("-d",
                        "--debug",
                        help="Print information about the program execution (Has temporarily no effect)",
                        action="store_true")
    args = parser.parse_args()

    if int(args.tournament_size) > int(args.pop_size):
        raise Exception("tournament_size cannot be greater than population_size!")

    run(args)
