from collections import namedtuple
import matplotlib.pyplot as plt
from scipy import optimize
import pandas as pd
import numpy as np
from string import ascii_letters

Params = namedtuple("Params", ["h", "mean", "std"])


class KBDModel(object):
    """Capture user's behaviour of keybouard use"""

    def __init__(self, input_file, num_bins=100, precalc=False):
        super(KBDModel, self).__init__()
        self.num_bins = num_bins
        self.letters_distribution = {}
        # precalc means we already know the distribution moments (mean, std_dev)
        if precalc is False:
            self.read_values(input_file)
            self.calculate_distributions()
        else:
            # if it takes too long to initialize object, we could pickle the optimized moments for each key
            # and initialize the object from those values, but at least as far as I've tested initialization
            # is rather fast
            pass

    def parse_file(self, file_name):
        try:
            with open(file_name, "r+") as f:
                lines = f.readlines()
                f.seek(0)
                f.truncate()
                for line in lines:
                    # we don't need the message line in the csv file
                    if line.split(",")[0] == "Message":
                        continue
                    # if line has a coma at the end delete it, since in
                    # this case it would mean a badly formated csv. Remove
                    # trailing spaces, carriage return or line feeds for
                    # easier comparison
                    line = line.rstrip("\n\r ")
                    if line[-1] == ',':
                        # I'm writing the lines using *nix style with only a
                        # line feed... sorry! Screw Windows and its
                        # carriage return!
                        line = line[:-1] + "\n"
                    f.write(line)
        except Exception as e:
            raise e

    def read_values(self, keystrokes_file):
        """Read and filter values from csv file"""
        try:
            self.parse_file(keystrokes_file)
            # header = None -> first row is not to be taken as the column names
            df = pd.read_csv(keystrokes_file, header=None, names=["letter", "x_pos"])
            # drop rows without a value
            df = df.dropna()
            # drop all rows that do not have a single letter in the
            # "letter" column
            df = df[df["letter"].isin(list(ascii_letters))]
            # values can also have noise; Remove it
            df = df[df["x_pos"] != "?"]
            # because of noise values might have not been read as floats,
            # so we explicitly tranform them
            df["x_pos"] = df["x_pos"].astype(float)
            # store the values in case we need them for sth
            self.raw_values = df
        except Exception:
            raise

    def estimate_parameters(self, heights, centers):
        """Calculate initial distribution parameters to increase fitting speed"""
        try:
            # highest peak of histogram is taken as initial guess for height
            h = np.ndarray.max(heights)
            max_idx = np.argmax(heights)
            # the center value of the bin where the highest peak is in
            # should be pretty close to the mean
            mean = centers[max_idx]
            # calculate std_dev
            std = np.sqrt(np.sum((centers - mean) ** 2 * heights) / np.sum(heights))
            return Params(h, mean, std)
        except:
            raise

    def calculate_distributions(self):
        """Calculate the user's typing style (distribution) for each keyboard letter"""
        # we want to know the values for each letter
        groups = self.raw_values.groupby("letter")
        for name, group in groups:
            heights, edges = np.histogram(group["x_pos"], self.num_bins, (0, 1))
            centers = [(edges[x] + edges[x + 1]) / 2.0 for x in range(len(edges) - 1)]
            params = self.estimate_parameters(heights, centers)
            # shape of a gaussian function
            gauss = lambda params, x: params[0] * np.exp(-(((x - params[1]) ** 2) / (2 * params[2] ** 2)))
            # metric for the fitting step
            errfunc = lambda params, x, y: gauss(params, x) - y
            # params are the parameters to be optimized (mean, std_dev).
            # x will be the bin_centers and y the bar_heights.
            # Heights (should) form a gaussian distribution so they are our
            # guide
            opt_params, res = optimize.leastsq(errfunc, params[:], args=(centers, heights))
            opt_params[2] = abs(opt_params[2])
            # msg = "group:{0}\nestimated:\nmu: {1}, sig: {2}"
            # msg = msg.format(name, params.mean, params.std, opt_params[1], opt_params[2])
            # print(msg)
            params = Params._make(opt_params)
            # print("optimized\nmu:{0}, sig: {1}".format(params.mean, params.std))
            # lambda resolves namespace when being called, not when
            # assigned, therefore create new scope to get correct params
            func = lambda x, params=params: np.random.normal(params.mean, params.std, x)
            self.letters_distribution[name] = func

    def get_keystroke(self, letter, num_samples=None):
        """Get num_samples of x-coordinate values according to the distribution of the letter"""
        try:
            sample = self.letters_distribution[letter](num_samples)
            return sample
        except KeyError:
            print("No distribution for letter '{0}'".format(letter))
            return None
        except Exception:
            raise
