# KeyboardOptimization

Every user has a unique typing pattern that comes along a set of personal common typing errors. By analysing this pattern, a personalized keyboard is generated - decreasing the number of personal type errors. The intention is to optimize the touch space that each key should occupy to reduce typos.


# Update 15.12.2017
genetic.py usage:

```python
python3 genetic.py data_file [-h] [-o OUT] [-p POP_SIZE] [-n NUM_GENERATIONS] [-t TOURNAMENT_SIZE] [-v] [-d]               
```
positional arguments:
  data_file             File with the training data. default=output.csv

optional arguments:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     File to which to save the generated keyboard.
                        default=genetic_keyboard.txt
  -p POP_SIZE, --pop-size POP_SIZE
                        Size of the initial population. default=40
  -n NUM_GENERATIONS, --num-generations NUM_GENERATIONS
                        Number of iterations of the algorithm. default=100
  -t TOURNAMENT_SIZE, --tournament-size TOURNAMENT_SIZE
                        number of individuals to select for the tournament
                        selection process
  -v, --verbose         Print information about the program results
  -d, --debug           Print information about the program execution (Has
                        temporarily no effect)


# Update 01.12.2017
usr_kbd_model module usage:

```python
import usr_kbd_model

# build the model. "output.csv" should be the path to a file in the format that kaz's server produces
user_model = usr_kbd_model.KBDModel("/path/to/output.csv")
# get one sample for the letter "e"
user_model.get_keystroke("e")
# get s**ttons of samples for "f"
user_model.get_keystroke("f", num_samples=100000)
```
