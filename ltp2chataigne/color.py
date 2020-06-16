from dataclasses import dataclass
from typing import List

from utils import chataigne_time


@dataclass
class Color(list):
    col: List[float]

    @property
    def r(self):
        return round(self.col[0], 3)

    @property
    def g(self):
        return round(self.col[1], 3)

    @property
    def b(self):
        return round(self.col[2], 3)

    @r.setter
    def r(self, value): self.col[0] = value

    @g.setter
    def g(self, value): self.col[1] = value

    @b.setter
    def b(self, value): self.col[2] = value

    def __repr__(self):
        return f"RGB({self.r},{self.g},{self.b})"

    def __len__(self):
        return len(self.col)

    def __iter__(self):
        return (comp for comp in self.col)

    def __eq__(self, other):
        """Overrides the default implementation"""
        return (self[0] == other[0]) and \
               (self[1] == other[1]) and \
               (self[2] == other[2])

    def __getitem__(self, idx):
        if isinstance(idx, int): return round(self.col[idx], 3)
        return [round(self.col[i], 3) for i in idx]

@dataclass
class ColorTime:
    color: Color
    time: int
    interpolated: bool = False

    def chataigne_time(self) -> float:
        return chataigne_time(self.time)


def ltp_color2color(dict) -> Color:
    b, g, r = dict['b'], dict['g'], dict['r']
    return Color([r, g, b])
