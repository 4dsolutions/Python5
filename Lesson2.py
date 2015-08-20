"""
CropCircleTractor

Inherits from Tractor with same __next__ based raster pattern,
however in this subclass, planting a @ occurs when the underlying
complex number in the corresponding plane does not diverge after
10 iterations of z = z * z + c.  Creates a file of ASCII art best
viewed fixed width font, small font size.

EXAMPLE OUTPUT:  https://flic.kr/p/xyNXhN

(cl) MIT License 2015 by 4dsolutions.net
"""

from Lesson1 import Tractor, Field

class CropCircleTractor(Tractor):

    def config(self, x_scale, y_scale, x_offset, y_offset):
        self.x_scale, self.y_scale = x_scale, y_scale
        self.x_offset, self.y_offset = x_offset, y_offset

    def __next__(self):
        super().__next__()  # updates pos
        c = complex((self.col + self.y_offset) * self.y_scale, (self.row + self.x_offset) * self.x_scale)
        z = complex(0,0)
        for _ in range(10):
            z = z*z + c
        if abs(z) <= 2:
            self.plant("@")
        return z

if __name__ == "__main__":
    the_field = Field(100, 250)
    the_field.add_tractor(CropCircleTractor)  # initialized as added
    the_tractor = the_field.Ts[0] # grab reference to instance
    the_tractor.config(.025, .01, -50, -200)
    the_tractor.fuel_level = 100 * 250
    for z in the_tractor:
        if the_tractor.pos == (99, 249):
            break
    fractal = open("mandelbrot.txt", "w")
    print(the_field, file = fractal)
    fractal.close()
