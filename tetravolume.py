"""
Euler volume, modified by Gerald de Jong
http://www.grunch.net/synergetics/quadvols.html
Kirby Urner (c) MIT License

The tetravolume.py methods make_tet and make_tri 
assume that volume and area use R-edge cubes and 
triangles for XYZ units respectively, and D-edge 
tetrahedrons and triangles for IVM units of volume 
and area (D = 2R).

The tetrahedron of edges D has sqrt(8/9) the 
volume of a cube of edges R, yet each is unit in
its respective matrix.

The triangle of edges D has an XYZ area of sqrt(3)
i.e. an equilateral triangle of edges 2 in R-square
units.  The IVM area of the same triangle is simply 1.

The cube of edges sqrt(2) in R units, has volume 
sqrt(2) to the 3rd power.  One third of that volume
is our unit tetrahedron of edges D (cube face diagonals).

See:
http://mathforum.org/kb/thread.jspa?threadID=2836546
for explanation of quadrays, used for some unit tests
"""

from math import sqrt as rt2
from qrays import Qvector, Vector
import sys

R =0.5
D =1.0

S3    = pow(9/8, 0.5)
root2 = rt2(2)
root3 = rt2(3)
root5 = rt2(5)
root6 = rt2(6)
PHI = (1 + root5)/2.0

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

class Triangle:
    
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c  

    def ivm_area(self):
        ivmarea = self.xyz_area() * 1/rt2(3)
        return ivmarea

    def xyz_area(self):
        """
        Heron's Formula, without the 1/4
        """
        a,b,c = self.a, self.b, self.c
        xyzarea = rt2((a+b+c) * (-a+b+c) * (a-b+c) * (a+b-c))
        return xyzarea
    
def make_tri(v0,v1):
    """
    three edges from any corner, remaining three edges computed
    """
    tri = Triangle(v0.length(), v1.length(), (v1-v0).length())
    return tri.ivm_area(), tri.xyz_area()

R = 0.5
D = 1.0

import unittest
class Test_Tetrahedron(unittest.TestCase):

    def test_unit_volume(self):
        tet = Tetrahedron(D, D, D, D, D, D)
        self.assertEqual(tet.ivm_volume(), 1, "Volume not 1")

    def test_e_module(self):
        e0 = D
        e1 = root3 * PHI**-1
        e2 = rt2((5 - root5)/2)
        e3 = (3 - root5)/2
        e4 = rt2(5 - 2*root5)
        e5 = 1/PHI
        tet = Tetrahedron(e0, e1, e2, e3, e4, e5)
        self.assertTrue(1/23 > tet.ivm_volume()/8 > 1/24, "Wrong E-mod")
        
    def test_unit_volume2(self):
        tet = Tetrahedron(R, R, R, R, R, R)
        self.assertAlmostEqual(tet.xyz_volume(), 0.117851130)

    def test_unit_volume3(self):
        tet = Tetrahedron(R, R, R, R, R, R)
        self.assertAlmostEqual(tet.ivm_volume(), 0.125)
        
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
        x = Vector((R, 0, 0))
        y = Vector((0, R, 0))
        z = Vector((0, 0, R))
        tet = make_tet(x,y,z)
        self.assertAlmostEqual(tet[1], 1/6, 5) # good to 5 places

    def test_quarter_octahedron(self):
        a = Vector((D,0,0))
        b = Vector((0,D,0))
        c = Vector((R,R,root2/2))
        tet = make_tet(a, b, c)
        self.assertAlmostEqual(tet[0], 1, 5) # good to 5 places  

    def test_xyz_cube(self):
        a = Vector((R, 0.0, 0.0))
        b = Vector((0.0, R, 0.0))
        c = Vector((0.0, 0.0, R))
        R_octa = make_tet(a,b,c) 
        self.assertAlmostEqual(6 * R_octa[1], 1, 4) # good to 4 places  

    def test_s3(self):
        D_tet = Tetrahedron(D, D, D, D, D, D)
        a = Vector((R, 0.0, 0.0))
        b = Vector((0.0, R, 0.0))
        c = Vector((0.0, 0.0, R))
        R_cube = 6 * make_tet(a,b,c)[1]
        self.assertAlmostEqual(D_tet.xyz_volume() * S3, R_cube, 4)

    def test_martian(self):
        p = Qvector((2,1,0,1))
        q = Qvector((2,1,1,0))
        r = Qvector((2,0,1,1))
        result = make_tet(5*q, 2*p, 2*r)
        self.assertAlmostEqual(result[0], 20, 7)
        
    def test_area_martian1(self):
        p = Qvector((2,1,0,1))
        q = Qvector((2,1,1,0))
        result = p.area(q)
        self.assertAlmostEqual(result, 1)        
 
    def test_area_martian2(self):
        p = 3 * Qvector((2,1,0,1))
        q = 4 * Qvector((2,1,1,0))
        result = p.area(q)
        self.assertAlmostEqual(result, 12)

    def test_area_martian3(self):
        qx = Vector((D,0,0)).quadray()
        qy = Vector((R,rt2(3)/2,0)).quadray()
        result = qx.area(qy)
        self.assertAlmostEqual(result, 1, 7)
        
    def test_area_earthling1(self):
        vx = Vector((1,0,0))
        vy = Vector((0,1,0))
        result = vx.area(vy)
        self.assertAlmostEqual(result, 1)        

    def test_area_earthling2(self):
        vx = Vector((2,0,0))
        vy = Vector((1,rt2(3),0))
        result = vx.area(vy)
        self.assertAlmostEqual(result, 2*rt2(3))    
        
    def test_phi_tet(self):
        "edges from common vertex: phi, 1/phi, 1"
        p = Vector((1, 0, 0))
        q = Vector((1, 0, 0)).rotz(60) * PHI
        r = Vector((0.5, root3/6, root6/3)) * 1/PHI
        result = make_tet(p, q, r)
        self.assertAlmostEqual(result[0], 1, 7)
        
    def test_phi_tet_2(self):
        p = Qvector((2,1,0,1))
        q = Qvector((2,1,1,0))
        r = Qvector((2,0,1,1))
        result = make_tet(PHI*q, (1/PHI)*p, r)
        self.assertAlmostEqual(result[0], 1, 7)
        
    def test_phi_tet_3(self):
        T = Tetrahedron(PHI, 1/PHI, 1.0, 
                        root2, root2/PHI, root2)
        result = T.ivm_volume()
        self.assertAlmostEqual(result, 1, 7)

    def test_koski(self):
        a = 1 
        b = PHI ** -1
        c = PHI ** -2
        d = (root2) * PHI ** -1 
        e = (root2) * PHI ** -2
        f = (root2) * PHI ** -1       
        T = Tetrahedron(a,b,c,d,e,f)
        result = T.ivm_volume()
        self.assertAlmostEqual(result, PHI ** -3, 7)       

class Test_Triangle(unittest.TestCase):
    
    def test_unit_area1(self):
        tri = Triangle(D, D, D)
        self.assertEqual(tri.ivm_area(), 1)
        
    def test_unit_area2(self):
        tri = Triangle(2, 2, 2)
        self.assertEqual(tri.ivm_area(), 4)
        
    def test_xyz_area3(self):
        tri = Triangle(D, D, D)
        self.assertEqual(tri.xyz_area(), rt2(3))
        
    def test_xyz_area4(self):
        v1 = Vector((D, 0, 0))
        v2 = Vector((0, D, 0))
        xyz_area = make_tri(v1, v2)[1]
        self.assertAlmostEqual(xyz_area, 2)

    def test_xyz_area5(self):
        tri = Triangle(R, R, R)
        self.assertAlmostEqual(tri.xyz_area(), (root3)/4)
        
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
