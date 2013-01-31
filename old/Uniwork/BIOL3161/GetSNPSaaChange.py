#!/usr/bin/python

import Bio.Blast

blasthandle =   Bio.Blast.NCBIWWW.qblast("blastx", "nr", seqThis)
