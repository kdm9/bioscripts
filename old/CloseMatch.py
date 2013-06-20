class CloseMatch(Token):
    def __init__(self, seq, maxMismatches=1):
        super(CloseMatch,self).__init__()
        self.name = seq
        self.sequence = seq
        self.maxMismatches = maxMismatches
        self.errmsg = "Expected " + self.sequence
        self.mayIndexError = False
        self.mayReturnEmpty = False

    def parseImpl( self, instring, loc, doActions=True ):
        start = loc
        instrlen = len(instring)
        maxloc = start + len(self.sequence)

        if maxloc <= instrlen:
            seq = self.sequence
            seqloc = 0
            mismatches = []
            throwException = False
            done = False
            while loc < maxloc and not done:
                if instring[loc] != seq[seqloc]:
                    mismatches.append(seqloc)
                    if len(mismatches) > self.maxMismatches:
                        throwException = True
                        done = True
                loc += 1
                seqloc += 1
        else:
            throwException = True

        if throwException:
            exc = self.myException
            exc.loc = loc
            exc.pstr = instring
            raise exc

        return loc, (instring[start:loc],mismatches)

searchseq = CloseMatch("ATCATCGAATGGAATCTAATGGAAT", 2)
