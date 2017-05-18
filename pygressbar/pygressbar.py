import time
import threading
import sys

from .io import DynamicText

class ProgressBar(object):
    locked = False

    def __init__(self, width=10, char="|", bc_char=" "):
        assert (isinstance(width, int) and width >= 4) or isinstance(width, property)
        assert len(char) == 1
        assert isinstance(char, str)
        assert len(bc_char) == 1
        assert isinstance(bc_char, str)

        self._width = width
        if self.content_width < 10:
            self.bar_count = max(1, int((self.content_width) / 2))
        else:
            self.bar_count = max(4, int((self.content_width) / 4))
        self.char = char
        self.bc_char = bc_char

    @property
    def width(self):
        return self._width

    @property
    def content_width(self):
        return self.width - 2

    @property
    def dynamic(self):
        return hasattr(self, "_text")

    def text_for(self, *args):
        raise NotImplementeError

    def clear_text(self, *args):
        print("\b" * self.width + " " * self.width + "\b" * self.width, end="")

    def start(self):
        assert not ProgressBar.locked, "Cannot create progress multiple simultaneous progress bars"
        ProgressBar.locked = True
        self._text = DynamicText()
        self._text.update()

    def stop(self):
        self._text.clear()
        self._text.stop()
        sys.stdout = sys.__stdout__
        ProgressBar.locked = False

    @staticmethod
    def _text_label(text, label):
        text = list(text)
        label_text = list(label)
        middle = len(text) // 2
        ptext_start = middle - len(label_text)//2
        text[ptext_start : ptext_start + len(label_text)] = label_text
        return "".join(text)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._text.clear()
        self.stop()

class BackgroundUpdatable(threading.Thread):
    def __init__(self, bar):
        super().__init__()
        self.bar = bar
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.bar.update()
            time.sleep(0.1)

    def __enter__(self):
        self.bar.start()
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        self.bar.stop()

class IndeterminateProgressBar(ProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def text_for(self):
        return "[" + self.char * self.bar_count + self.bc_char * (self.content_width - self.bar_count) + "]"

    def update(self):
        # shift right
        if self._text.text == "":
            assert len(self.text_for()) == self.width
            self._text.update(self.text_for())
        else:
            self._text.update("[" + self._text.text[-2] + self._text.text[1:-2] + "]")

    @property
    def background(self):
        return BackgroundUpdatable(self)

class ValueProgressBar(ProgressBar):
    def __init__(self, max_value, *args, show_value=False, **kwargs):
        assert isinstance(show_value, bool)
        assert isinstance(max_value, (int, float))
        super().__init__(*args, **kwargs)

        self.max_value = max_value
        self.show_value = show_value

    def text_for(self, value):
        assert isinstance(value, (int, float))
        assert 0 <= value <= self.max_value
        progress = (value * self.content_width) // self.max_value
        if value == int(value) and self.max_value == int(self.max_value):
            label = "{}/{}".format(int(value), int(self.max_value))
        else:
            label = "{:.2f}/{:.2f}".format(value, self.max_value)
        if self.content_width > len(label) * 2 and self.show_value:
            text = list(progress * self.char + (self.content_width - progress) * self.bc_char)
            return "[" + ProgressBar._text_label(text, label) + "]"
        else:
            return "[" + progress * self.char + (self.content_width - progress) * self.bc_char + "]"

    def update(self, value, update_max_value=None):
        if update_max_value is not None:
            assert isinstance(update_max_value, (int, float))
            self.max_value = update_max_value
        assert len(self.text_for(value)) == self.width
        self._text.update(self.text_for(value))

class PercentageProgressBar(ValueProgressBar):
    def __init__(self, max_value=100, *args, **kwargs):
        super().__init__(max_value, *args, **kwargs)

    def text_for(self, value):
        assert isinstance(value, (int, float))
        assert 0 <= value <= self.max_value
        progress = int((value * self.content_width) // self.max_value)
        if self.content_width > 20 and self.show_value:
            text = list(progress * self.char + (self.content_width - progress) * self.bc_char)
            return "[" + ProgressBar._text_label(text, str(int(value)) + "%") + "]"
        else:
            return "[" + progress * self.char + (self.content_width - progress) * self.bc_char + "]"

class MultiProgressBar(ProgressBar):
    def __init__(self, subbars):
        assert isinstance(subbars, (list, tuple))

        self.bars = subbars
        super().__init__()

    @property
    def width(self):
        return sum(sb.width for sb in self.bars) + len(self.bars) - 1

    def add(self, item):
        self.bars.append(item)

    def remove_all(self):
        if self.dynamic:
            self._text.clear()
        sys.stdout.flush()
        time.sleep(2)

        self.bars = []

    def remove_first(self):
        assert self.bars

        if self.dynamic:
            self._text.clear()

        self.bars.pop(0)

    def remove_last(self):
        assert self.bars

        if self.dynamic:
            self._text.clear()

        self.bars.pop()

    def text_for(self, *values):
        assert len(self.bars) == len(values)
        return " ".join([b.text_for(v) for b, v in zip(self.bars, values)])

    def update(self, *values):
        self._text.update(self.text_for(*values))
