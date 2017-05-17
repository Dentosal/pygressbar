# Pygressbar
A simple python library for displaying text-based progress bars.

## Installing
```bash
python3 -m pip install git+https://github.com/Dentosal/pygressbar
```

## Example usage

### Indeterminate progress bar
```python
import time
from pygressbar import IndeterminateProgressBar

print("Processing a list of items: ")
ITEMS = ["Item {}".format(n) for n in range(10)]
with IndeterminateProgressBar(8).background:
    for l in ITEMS:
        print("* " + l + " " * (max(map(len, ITEMS)) - len(l)) + " ", end="")
        time.sleep(1)
        print("[OK]")
```

### Percentage progress bar
```python
import time
from pygressbar import PercentageProgressBar

print("Processing a large item:")
with PercentageProgressBar(50, show_value=True) as pb:
    pb.update(0)
    PARTS = 7
    for part in range(PARTS):
        time.sleep(0.5)
        pb.update(100*(part+1)/PARTS)
print("Done")
```


See [`example.py`](example.py) for more examples.
