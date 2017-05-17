import sys

class WrappedOutput(object):
    """Adds a callback for stdout operations."""
    def __init__(self, before=None, after=None):
        assert before is None or callable(before)
        assert after is None or callable(after)
        self.before = before
        self.after = after

        sys.stdout = self

    def stop(self):
        sys.stdout.flush()
        sys.stdout = sys.__stdout__

    def write(self, text):
        if self.before:
            x = self.before()

        sys.__stdout__.write(text)

        if self.after:
            self.after()

    def put(self, text):
        sys.__stdout__.write(text)

    def __getattr__(self, name):
        """Pass through all stdin."""
        return getattr(sys.__stdout__, name)

class DynamicText(object):
    def __init__(self, text=""):
        self._text = text
        self._drawn = False
        self._output = WrappedOutput(
            self.hide_before_print,
            self.show_after_print
        )

    @property
    def text(self):
        return self._text

    def hide_before_print(self):
        self.clear()

    def show_after_print(self):
        self._drawn = False
        self.update()

    def stop(self):
        self._output.stop()

    def jump_start(self, flush=False):
        self._output.put("\b"*len(self._text))
        if flush:
            self._output.flush()

    def clear(self, flush=True):
        if self._drawn:
            self.jump_start()
        self._output.put(" " * len(self._text))
        self.jump_start()
        if flush:
            self._output.flush()

    def update(self, newtext=None):
        if self._drawn:
            self.jump_start()

        if newtext is not None:
            self._text = newtext

        self._output.put(self._text)
        self._output.flush()
        self._drawn = True
