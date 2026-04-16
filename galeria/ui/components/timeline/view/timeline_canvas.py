import flet.canvas as cv


class TimelineCanvas:
    def __init__(self, on_resize=None):
        self.canvas = cv.Canvas(shapes=[], expand=True, width=1900, height=300, on_resize=on_resize)

    @property
    def width(self):
        return self.canvas.width

    @property
    def height(self):
        return self.canvas.height

    def set_shapes(self, shapes):
        self.canvas.shapes = shapes
