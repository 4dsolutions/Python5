"""
Field & Tractor

Tractor behaves as an iterator wrapping around a
field in a spiral by default, returning from lower
right (n-1, m-1) to upper left (0, 0) where n, m is
number of rows and columns respectively.

The TractorWriter takes a string and starts planting
it sequentially at a preset position.

Background:  R&D into Python5 open course with private
mentor option and assuming as background content
Python1 - Python4
@ http://courses.oreillyschool.com/courseList.html

(cl) MIT License 2015 by 4dsolutions.net 
"""


class Field(dict):
    """
    Field is a mapping, subclass of dict, with keys (x, y)
    """

    def __init__(self, rows, columns, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dims = (rows, columns)
        self.Ts = [ ]  # add tractors to this list

    @property
    def rows(self):
        return self.dims[0]

    @property
    def columns(self):
        return self.dims[1]


    def __str__(self):
        """
        output the field as a string
        """
        s = ""
        for x in range(self.rows):
            s += "\n"
            for y in range(self.columns):
                s = (s + self[x,y]) if (x,y) in self else (s + ".")
        return s

    def __repr__(self):
        return "Field({}, {})".format(self.rows, self.columns)

    def add_tractor(self, T):
        """
        A tractor gains a reference to this very field when added thereto
        """
        the_gen = T(self)
        self.Ts.append( the_gen )


class Tractor:
    """
    An iterator, spirals through Field and rasters to top again by default
    """

    def __init__(self, my_field):
        self._myfield = my_field  # shows up when added to a field
        self.pos = (0, 0)  # changing internal state
        self.fuel_level = 150  # might run out of gas,

    def plant(self, the_crop):
        self._myfield[self.pos] = the_crop

    def __iter__(self):
        return self

    def __next__(self):
        self.fuel_level -= 1  # decrement fuel
        if self.col + 1 < self._myfield.columns:
            self.pos = (self.row, self.col + 1)
        else:
            if self.row + 1 < self._myfield.rows:
                self.pos = (self.row + 1, 0)
            else:
                self.pos = (0, 0)
        return self.pos

    @property
    def row(self):
        return self.pos[0]

    @property
    def col(self):
        return self.pos[1]

    def __repr__(self):
        return "<Tractor @ {}; Fuel {}>".format(self.pos, self.fuel_level)

class TractorWriter(Tractor):

    def write(self, what, where):
        self.what = what
        self.start_point = where
        self.cnt = 0
        self.writing = False

    def __next__(self):
        super().__next__()  # updates pos
        if self.pos == self.start_point:
            self.writing = True
        if self.writing:
            if self.cnt == len(self.what):
                self.writing = False
                self.cnt = 0
            else:
                self.plant(self.what[self.cnt])
            self.cnt += 1

    def __repr__(self):
        return "<Tractor @ {}; Fuel {}; Phrase {}>".format(self.pos, self.fuel_level, self.what)

if __name__ == "__main__":
    the_field = Field(11, 11)
    the_field.add_tractor(TractorWriter)
    the_tractor = the_field.Ts[0]
    the_tractor.write("JUST USE IT", (5,3))
    for _ in range(101):
        next(the_tractor)
    print(the_tractor)
    print(the_field)
