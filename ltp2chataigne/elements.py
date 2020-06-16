from color import *

COL_BLACK = Color([0,0,0])

class Element:
    type = None

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def is_all_black(self) -> bool:
        return True

    def right_edge(self) -> Color:
        return COL_BLACK

    def left_edge(self) -> Color:
        return COL_BLACK

    @property
    def duration(self) -> int:
        return self.end_time - self.start_time

    def offset(self, time):
        self.start_time += time
        self.end_time += time
        if self.start_time < 0:
            self.end_time -= abs(self.start_time)
            self.start_time = 0

    def get_colors(self) -> List[ColorTime]:
        return []


class SolidElement(Element):
    type = "solid"

    def __init__(self, start_time, duration, color: Color):
        super().__init__(start_time, duration)
        self.color = color

    def right_edge(self) -> Color:
        return self.color

    def left_edge(self) -> Color:
        return self.color

    def is_all_black(self) -> bool:
        return self.color == COL_BLACK

    def get_colors(self) -> List[ColorTime]:
        return [ColorTime(self.color, self.start_time, False)]


class GradientElement(Element):
    type = "gradient"

    def __init__(self, start_time, duration, start_color: Color, end_color: Color):
        super().__init__(start_time, duration)
        self.start_color = start_color
        self.end_color = end_color

    def right_edge(self) -> Color:
        return self.end_color

    def left_edge(self) -> Color:
        return self.start_color

    def is_all_black(self) -> bool:
        return self.start_color == COL_BLACK and self.end_color == COL_BLACK

    def get_colors(self) -> List[ColorTime]:
        return [ColorTime(self.start_color, self.start_time, True),
                ColorTime(self.end_color, self.end_time, False)]


class FlashElement(Element):
    type = "flash"

    def __init__(self, start_time, duration, start_color, end_color, period, ratio):
        super().__init__(start_time, duration)
        self.start_color = start_color
        self.end_color = end_color
        self.period = period
        self.ratio = ratio

    def right_edge(self) -> Color:
        # calculate precise moment
        if self.duration % self.period < self.period * self.ratio:
            return self.start_color

        return self.end_color

    def left_edge(self) -> Color:
        return self.start_color

    def is_all_black(self) -> bool:
        return self.start_color == COL_BLACK and self.end_color == COL_BLACK

    def get_colors(self) -> List[ColorTime]:
        result = []
        time = self.start_time
        ratio = self.ratio / 100.0

        for i in range(self.duration // self.period):
            result += [ColorTime(self.start_color, time, False)]
            result += [ColorTime(self.end_color, time + self.period * ratio, False)]
            time += self.period

        # last round
        if time < self.end_time:
            result += [ColorTime(self.start_color, time, False)]

        if time + self.period * ratio < self.end_time:
            result += [ColorTime(self.start_color, time + self.period * ratio, False)]

        return result


class RainbowElement(FlashElement):
    type = "rainbow"

    def __init__(self, start_time, duration, start_color, period):
        super().__init__(start_time, duration, start_color, None, period, None)
        self.start_color = start_color
        self.period = period

