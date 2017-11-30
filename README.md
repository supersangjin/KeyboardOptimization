# KeyboardOptimization

CS454 Group Project 

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
