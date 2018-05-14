"""
Euler volume, modified by Gerald de Jong
http://www.grunch.net/synergetics/quadvols.html
Kirby Urner (c) MIT License

See:
http://mathforum.org/kb/thread.jspa?threadID=2836546
for explanation of quadrays, used for some unit tests
"""

from math import sqrt as rt2
from qrays import Qvector, Vector
import sys

S3    = pow(9/8, 0.5)
root2 = rt2(2)
root5 = rt2(5)

class Tetrahedron:
    """
    Takes six edges of tetrahedron with faces
    (a,b,d)(b,c,e)(c,a,f)(d,e,f) -- returns volume
    if ivm and xyz
    """

    def __init__(self, a, b, c, d, e, f):
        # a,b,c,d,e,f = [Decimal(i) for i in (a,b,c,d,e,f)]
        self.a, self.a2 = a, a**2
        self.b, self.b2 = b, b**2
        self.c, self.c2 = c, c**2
        self.d, self.d2 = d, d**2
        self.e, self.e2 = e, e**2
        self.f, self.f2 = f, f**2

    def ivm_volume(self):
        ivmvol = ((self._addopen() 
                    - self._addclosed() 
                    - self._addopposite())/2) ** 0.5
        return ivmvol

    def xyz_volume(self):
        xyzvol = 1/S3 * self.ivm_volume()
        return xyzvol

    def _addopen(self):
        a2,b2,c2,d2,e2,f2 = self.a2, self.b2, self.c2, self.d2, self.e2, self.f2
        sumval = f2*a2*b2
        sumval +=  d2 * a2 * c2
        sumval +=  a2 * b2 * e2
        sumval +=  c2 * b2 * d2
        sumval +=  e2 * c2 * a2
        sumval +=  f2 * c2 * b2
        sumval +=  e2 * d2 * a2
        sumval +=  b2 * d2 * f2
        sumval +=  b2 * e2 * f2
        sumval +=  d2 * e2 * c2
        sumval +=  a2 * f2 * e2
        sumval +=  d2 * f2 * c2
        return sumval

    def _addclosed(self):
        a2,b2,c2,d2,e2,f2 = self.a2, self.b2, self.c2, self.d2, self.e2, self.f2
        sumval =   a2 * b2 * d2
        sumval +=  d2 * e2 * f2
        sumval +=  b2 * c2 * e2
        sumval +=  a2 * c2 * f2
        return sumval

    def _addopposite(self):
        a2,b2,c2,d2,e2,f2 = self.a2, self.b2, self.c2, self.d2, self.e2, self.f2
        sumval =  a2 * e2 * (a2 + e2)
        sumval += b2 * f2 * (b2 + f2)
        sumval += c2 * d2 * (c2 + d2)
        return sumval

def make_tet(v0,v1,v2):
    """
    three edges from any corner, remaining three edges computed
    """
    tet = Tetrahedron(v0.length(), v1.length(), v2.length(), 
                      (v0-v1).length(), (v1-v2).length(), (v2-v0).length())
    return tet.ivm_volume(), tet.xyz_volume()

PHI = (1 + root5)/2.0

R = 0.5
D = 1.0
root3 = pow(3, .5)
root2 = pow(2, .5)

import unittest
class Test_Tetrahedron(unittest.TestCase):

    def test_unit_volume(self):
        tet = Tetrahedron(D, D, D, D, D, D)
        self.assertEqual(tet.ivm_volume(), 1, "Volume not 1")

    def test_e_module(self):
        e0 = D
        e1 = rt2(3) * PHI**-1
        e2 = rt2((5 - root5)/2)
        e3 = (3 - root5)/2
        e4 = rt2(5 - 2*root5)
        e5 = 1/PHI
        tet = Tetrahedron(e0, e1, e2, e3, e4, e5)
        self.assertTrue(1/23 > tet.ivm_volume()/8 > 1/24, "Wrong E-mod")
        
    def test_unit_volume2(self):
        tet = Tetrahedron(R, R, R, R, R, R)
        self.assertAlmostEqual(float(tet.xyz_volume()), 0.117851130)

    def test_phi_edge_tetra(self):
        tet = Tetrahedron(D, D, D, D, D, PHI)
        self.assertAlmostEqual(float(tet.ivm_volume()), 0.70710678)

    def test_right_tetra(self):
        e = pow((root3/2)**2 + (root3/2)**2, 0.5)  # right tetrahedron
        tet = Tetrahedron(D, D, D, D, D, e)
        self.assertAlmostEqual(tet.xyz_volume(), 1)

    def test_quadrant(self):
        qA = Qvector((1,0,0,0))
        qB = Qvector((0,1,0,0))
        qC = Qvector((0,0,1,0))
        tet = make_tet(qA, qB, qC) 
        self.assertAlmostEqual(tet[0], 0.25) 

    def test_octant(self):
        x = Vector((0.5, 0,   0))
        y = Vector((0  , 0.5, 0))
        z = Vector((0  , 0  , 0.5))
        tet = make_tet(x,y,z)
        self.assertAlmostEqual(tet[1], 1/6, 5) # good to 5 places

    def test_quarter_octahedron(self):
        a = Vector((1,0,0))
        b = Vector((0,1,0))
        c = Vector((0.5,0.5,root2/2))
        tet = make_tet(a, b, c)
        self.assertAlmostEqual(tet[0], 1, 5) # good to 5 places  

    def test_xyz_cube(self):
        a = Vector((0.5, 0.0, 0.0))
        b = Vector((0.0, 0.5, 0.0))
        c = Vector((0.0, 0.0, 0.5))
        R_octa = make_tet(a,b,c) 
        self.assertAlmostEqual(6 * R_octa[1], 1, 4) # good to 4 places  

    def test_s3(self):
        D_tet = Tetrahedron(D, D, D, D, D, D)
        a = Vector((0.5, 0.0, 0.0))
        b = Vector((0.0, 0.5, 0.0))
        c = Vector((0.0, 0.0, 0.5))
        R_cube = 6 * make_tet(a,b,c)[1]
        self.assertAlmostEqual(D_tet.xyz_volume() * S3, R_cube, 4)

    def test_martian(self):
        p = Qvector((2,1,0,1))
        q = Qvector((2,1,1,0))
        r = Qvector((2,0,1,1))
        result = make_tet(5*q, 2*p, 2*r)
        self.assertAlmostEqual(result[0], 20, 7)
        
def command_line():
    args = sys.argv[1:]
    try:
        args = [float(x) for x in args] # floats
        t = Tetrahedron(*args)
    except TypeError:
        t = Tetrahedron(1,1,1,1,1,1)
        print("defaults used")
    print(t.ivm_volume())
    print(t.xyz_volume())
        
if __name__ == "__main__":
    if len(sys.argv)==7:
        command_line()  
    else:
        unittest.main()
