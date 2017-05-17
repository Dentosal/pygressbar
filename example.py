import time
import random
from pygressbar import IndeterminateProgressBar, PercentageProgressBar, ValueProgressBar, MultiProgressBar

print("Processing order... ", end="")
with IndeterminateProgressBar(8).background:
    time.sleep(2)
print("Complete")

print("Processing a list of languages: ")
LANGUAGES = ("Python", "Rust", "Scala", "C")
with IndeterminateProgressBar(10).background:
    for l in LANGUAGES:
        print("* " + l + " " * (max(map(len, LANGUAGES)) - len(l)) + " ", end="")
        time.sleep(1)
        print("[OK]")

print("Downloading a large file:")
with PercentageProgressBar(50, show_value=True) as pb:
    pb.update(0)
    PARTS = 7
    for part in range(PARTS):
        time.sleep(0.5)
        pb.update(100*(part+1)/PARTS)
print("Done")

print("Downloading a few smaller files:")
PARTS = 7
top_level_bar = ValueProgressBar(7, 50, show_value=True)
print(top_level_bar.text_for(0), end="")
with IndeterminateProgressBar(10).background:
    for part in range(PARTS):
        time.sleep(1)
        top_level_bar.clear_text()
        print(top_level_bar.text_for(part+1), end="")
top_level_bar.clear_text()
print("Done")

print("Downloading a few big files:")
with MultiProgressBar([
    ValueProgressBar(7, 25, show_value=True),
    PercentageProgressBar(25, show_value=True)
]) as pbs:
    FILES = 7
    PARTS = 7
    for fp in range(FILES):
        time.sleep(0.5)
        pbs.update(fp, 0)
        for part in range(PARTS):
            time.sleep(0.2)
            pbs.update(fp, (part+1)/PARTS * 100)
        pbs.update(fp+1, 100)
print("Done")
