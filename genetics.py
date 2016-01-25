# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 10:07:57 2015

@author: kurner, 4dsolutions (.net)
(copyleft MIT license, 2015)

Example:  Rich Data Structures
(for learning Python, including sqlite3)

Source:

http://www.soc-bdr.org/rds/authors/unit_tables_conversions_and_genetic_dictionaries/e5202/index_en.html

Any errors you discover in transcribing will be mine, please
let me know and I'll correct my copy as well.

kirby.urner@gmail.com

Re:  "Rich Data Structures"
https://mail.python.org/pipermail/edu-sig/2006-June/006608.html

(a more obvious need now that "big data" examples are in demand,
for learning map/reduce techniques etc.).  Indeed, we have many
public raw data sets.  A goal is to have some already in Python,
as ready-to-go native data types.  As here.  This is not "big
data", just data.

Another experiment:
https://mail.python.org/pipermail/edu-sig/2012-December/010709.html
(same caveats about errors)

Adding to PythonAnywhere/thekirbster account for sharing with <guild />
classes etc.  You may wish to contribute to Github projects from your
PythonAnywhere account.


"""

amino_acid_abbrevs = \
dict(
Phe = 'Phenyalinine',
Leu = 'Leucine',
Ser = 'Serine',
Tyr = 'Tyrosine',
Cys = 'Cysteine',
Trp = 'Tryptophan',
Pro = 'Proline',
His = 'Histidine',
Gln = 'Glutamine',
Arg = 'Arginine',
Ile = 'Isoleucine',
Met = 'Methionine',
Thr = 'Threonine',
Asn = 'Asparagine',
Lys = 'Lysine',
Val = 'Valine',
Ala = 'Alanine',
Asp = 'Aspartate',
Glu = 'Glutamate',
Cly = 'Glycine')

combos = [(a, b, c) for a in ('G','U','A','C')
for b in ('G','U','A','C')
for c in ('G','U','A','C')]


# Also see:
# https://flic.kr/p/BeVwN2
# (American Scientist Vol. 97)

mRNA = \
{
('G', 'G', 'G') : 'Gly',
('G', 'G', 'U') : 'Gly',
('G', 'G', 'A') : 'Gly',
('G', 'G', 'C') : 'Gly',
('G', 'U', 'G') : 'Val',
('G', 'U', 'U') : 'Val',
('G', 'U', 'A') : 'Val',
('G', 'U', 'C') : 'Val',
('G', 'A', 'G') : 'Glu',
('G', 'A', 'U') : 'Asp',
('G', 'A', 'A') : 'Glu',
('G', 'A', 'C') : 'Asp',
('G', 'C', 'G') : 'Ala',
('G', 'C', 'U') : 'Ala',
('G', 'C', 'A') : 'Ala',
('G', 'C', 'C') : 'Ala',

('U', 'G', 'G') : 'Trp',
('U', 'G', 'U') : 'Cys',
('U', 'G', 'A') : 'STOP',
('U', 'G', 'C') : 'Cys',
('U', 'U', 'G') : 'Leu',
('U', 'U', 'U') : 'Phe',
('U', 'U', 'A') : 'Leu',
('U', 'U', 'C') : 'Phe',
('U', 'A', 'G') : 'STOP',
('U', 'A', 'U') : 'Tyr',
('U', 'A', 'A') : 'STOP',
('U', 'A', 'C') : 'Tyr',
('U', 'C', 'G') : 'Ser',
('U', 'C', 'U') : 'Ser',
('U', 'C', 'A') : 'Ser',
('U', 'C', 'C') : 'Ser',

('A', 'G', 'G') : 'Arg',
('A', 'G', 'U') : 'Ser',
('A', 'G', 'A') : 'Arg',
('A', 'G', 'C') : 'Ser',
('A', 'U', 'G') : 'Met',
('A', 'U', 'U') : 'Ile',
('A', 'U', 'A') : 'Ile',
('A', 'U', 'C') : 'Ile',
('A', 'A', 'G') : 'Lys',
('A', 'A', 'U') : 'Asn',
('A', 'A', 'A') : 'Lys',
('A', 'A', 'C') : 'Asn',
('A', 'C', 'G') : 'Thr',
('A', 'C', 'U') : 'Thr',
('A', 'C', 'A') : 'Thr',
('A', 'C', 'C') : 'Thr',

('C', 'G', 'G') : 'Arg',
('C', 'G', 'U') : 'Arg',
('C', 'G', 'A') : 'Arg',
('C', 'G', 'C') : 'Arg',
('C', 'U', 'G') : 'Leu',
('C', 'U', 'U') : 'Leu',
('C', 'U', 'A') : 'Leu',
('C', 'U', 'C') : 'Leu',
('C', 'A', 'G') : 'Gln',
('C', 'A', 'U') : 'His',
('C', 'A', 'A') : 'Gln',
('C', 'A', 'C') : 'His',
('C', 'C', 'G') : 'Pro',
('C', 'C', 'U') : 'Pro',
('C', 'C', 'A') : 'Pro',
('C', 'C', 'C') : 'Pro'}


# [Ibid, www.soc-bdr.org] from Table 5. Genetic Code:
# mRNA condon -> tRNA anti-codon
# DNA column dropped (computable, replace mRNA U with T)
# last column also not included.

tRNA = \
{
('U','U','U'):(('A','A','A'), ('A','A','G')),
('U','U','C'):(('A','A','G'),),
('U','U','A'):(('A','A','U'),),
('U','U','G'):(('A','A','U'),('A','A','C')),
('U','C','U'):(('A','G','I'),('A','G','G'), ('A','G','A')),
('U','C','C'):(('A','G','I'),('A','G','G')),
('U','C','A'):(('A','G','I'),('A','G','U')),
('U','C','G'):(('A','G','C'),('A','G','U')),
('U','A','U'):(('A','U','A'),('A','U','G'),),
('U','A','C'):(('A','U','G'),),
('U','A','A'):(('A','U','U'),),
('U','A','G'):(('A','U','C'),('A','U','U')),
('U','G','U'):(('A','C','A'),('A','C','G')),
('U','G','C'):(('A','C','G'),),
('U','G','A'):(('A','C','U'),),
('U','G','G'):(('A','C','C'),),

('C','U','U'):(('G','A','I'),('G','A','G'),('G','A','A')),
('C','U','C'):(('G','A','I'),('G','A','G')),
('C','U','A'):(('G','A','I'),('G','A','U')),
('C','U','G'):(('G','A','C'),('G','A','U')),
('C','C','U'):(('G','G','I'),('G','G','G'),('G','G','A')),
('C','C','C'):(('G','G','I'),('G','G','G')),
('C','C','A'):(('G','G','I'),('G','G','U')),
('C','C','G'):(('G','G','C'),('G','G','U')),
('C','A','U'):(('G','U','A'),('G','U','G')),
('C','A','C'):(('G','U','G'),),
('C','A','A'):(('G','U','U'),),
('C','A','G'):(('G','U','C'),('G','U','U')),
('C','G','U'):(('G','C','I'),('G','C','G'),('G','C','A')),
('C','G','C'):(('G','C','I'),('G','C','G')),
('C','G','A'):(('G','C','I'),('G','C','U')),
('C','G','G'):(('G','C','C'),('G','C','U')),

('A','U','U'):(('U','A','I'),('U','A','G'),('U','A','A')),
('A','U','C'):(('U','A','I'),('U','A','G')),
('A','U','A'):(('U','A','I'),('U','A','U')),
('A','U','G'):(('U','A','C'),),
('A','C','U'):(('U','G','I'),('U','G','G'),('U','G','A')),
('A','C','C'):(('U','G','I'),('U','G','G')),
('A','C','A'):(('U','G','I'),('U','G','U')),
('A','C','G'):(('U','G','C'),('U','G','U')),
('A','A','U'):(('U','U','A'),('U','U','G')),
('A','A','C'):(('U','U','G'),),
('A','A','A'):(('U','U','U'),),
('A','A','G'):(('U','U','C'),('U','U','U')),
('A','G','U'):(('U','C','A'),('U','C','G')),
('A','G','C'):(('U','C','G'),),
('A','G','A'):(('U','C','U'),),
('A','G','G'):(('U','C','C'),('U','C','U')),

('G','U','U'):(('C','A','I'),('C','A','G'),('C','A','A')),
('G','U','C'):(('C','A','I'),('C','A','G')),
('G','U','A'):(('C','A','I'),('C','A','U')),
('G','U','G'):(('C','A','C'),('C','A','U')),
('G','C','U'):(('C','G','I'),('C','G','G'),('C','G','A')),
('G','C','C'):(('C','G','I'),('C','G','G')),
('G','C','A'):(('C','G','I'),('C','G','U')),
('G','C','G'):(('C','G','C'),('C','G','U')),
('G','A','U'):(('C','U','G'),('C','U','A')),
('G','A','C'):(('C','U','G'),),
('G','A','A'):(('C','U','U'),),
('G','A','G'):(('C','U','U'),('C','U','C')),
('G','G','U'):(('C','C','I'),('C','C','G'),('C','C','A')),
('G','G','C'):(('C','C','I'),('C','C','G')),
('G','G','A'):(('C','C','I'),('C','C','U')),
('G','G','G'):(('C','C','C'),('C','C','U'))
}
