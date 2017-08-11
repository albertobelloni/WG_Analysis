import math
from ROOT import Double as rDouble

class data_pair :

    def __init__(self, val=None, stat=None, syst=None) :
        self.set( val, stat, syst)

    def set( self, val=None, stat=None, syst=None ) :
        if isinstance( val, rDouble ) :
            val = float(val)
        if isinstance( stat, rDouble ) :
            stat = float(stat)
        if isinstance( syst, rDouble ) :
            syst = float(syst)
        
        if val != None :
            self.val = val
        else :
            self.val = 0.0
        if stat != None :
            self.stat = stat 
        else :
            self.stat = 0.0
        if syst != None :
            self.syst = syst
        else :
            self.syst = 0.0

    def Print(self) :

        #determine precision
        if self.stat > 0 :
            celratio = abs(int(math.log10(self.stat)))
        else :
            celratio = 1

        if math.fabs(self.stat) > 1 :
            prec = 1
        else :
            prec = celratio+2

        return '%.*f $\pm$ %.*f' %(prec, self.val, prec, self.stat)

    def __str__(self) :
        return self.Print()

    def __add__(self, other) :
        if type(other) is int or type(other) is float :
            new_val = self.val + other
            new_stat = self.stat
            new_syst = self.syst
            return data_pair(new_val, new_stat, new_syst)
        new_val = self.val + other.val
        new_stat = self._abserr(self.stat, other.stat)
        new_syst = self._abserr(self.syst, other.syst)
        return data_pair(new_val, new_stat, new_syst)

    def __iadd__(self, other) :
        self = self + other
        return self

    def __sub__(self, other) :
        if type(other) is int or type(other) is float :
            new_val = self.val - other
            new_stat = self.stat
            new_syst = self.syst
            return data_pair(new_val, new_stat, new_syst)
        else :
            'Subtract %s from %s' %( self.Print(), other.Print() )
            new_val = self.val - other.val
            new_stat = self._abserr(self.stat, other.stat) 
            new_syst = self._abserr(self.syst, other.syst) 
            'Result = %s' %(data_pair(new_val, new_stat, new_syst).Print())
            return data_pair(new_val, new_stat, new_syst)

    def __rsub__(self, other) :
        return -1*(self-other)
        

    def __mul__(self, other) :
        if type(other) is int or type(other) is float :
            new_val = self.val * other
            new_stat = math.fabs(self.stat * other)
            new_syst = math.fabs(self.syst * other)
            return data_pair(new_val, new_stat, new_syst)
        else:
            try :
                new_stat = self._fracerr(self.val*other.val, self.stat/self.val, other.stat/other.val)
            except ZeroDivisionError :
                new_stat = 0.0
            try :
                new_syst = self._fracerr(self.val*other.val, self.syst/self.val, other.syst/other.val)
            except ZeroDivisionError :
                new_syst = 0.0
            new_val = self.val*other.val
            return data_pair(new_val, new_stat, new_syst)

    def __rmul__(self, other) :
        return self*other

    def __div__(self, other) :
        if type(other) is int or type(other) is float :
            new_val = self.val / other
            new_stat = self.stat / other
            new_syst = self.syst / other
            return data_pair(new_val, new_stat, new_syst)
        else:
            try :
                new_stat = self._fracerr(self.val/other.val, self.stat/self.val, other.stat/other.val)
            except ZeroDivisionError :
                new_stat = 0.0
            try :
                new_syst = self._fracerr(self.val/other.val, self.syst/self.val, other.syst/other.val)
            except ZeroDivisionError :
                new_syst = 0.0

            try :
                new_val = self.val/other.val
            except ZeroDivisionError :
                new_val = 0.0
            return data_pair(new_val, new_stat, new_syst)

    def __rdiv__(self, other) :
        if self.val != 0 :
            new_val = other/self.val
        else :
            new_val = 0
        
        if self.stat != 0 :
            new_stat = new_val * self.stat/self.val
        else :
            new_stat = 0

        if self.syst != 0 :
            new_syst = new_val * self.syst/self.val
        else :
            new_syst = 0;

        return data_pair( new_val, new_stat, new_syst)



    def __eq__(self, other) :
        if type( other ) is type(self) :
            return (self.val == other.val) & (self.stat==other.stat) & (self.syst==other.syst)
        elif type(other) is int or type(other) is float :
            return self.val == other

    def __str__(self):
        return '%f +- %f' %(self.val, self.stat)

    def _abserr(self, val1, val2) :
        return math.sqrt(val1*val1 + val2*val2)
    def _fracerr(self, res, frac1, frac2) :
        return res*math.sqrt(math.pow(frac1, 2) + math.pow(frac2, 2))

    def sqrt( self ) :
        new_val = math.sqrt( self.val )
        new_stat = new_val*0.5*self.stat/self.val
        new_syst = new_val*0.5*self.syst/self.val
        return data_pair( new_val, new_stat, new_syst )

    def fabs(self) :
        self.val = math.fabs(self.val)

    def waverage(self, other) :
        err2 = 1./((1./(self.stat*self.stat)) + (1./(other.stat*other.stat)))
        newval = ((self.val/(self.stat*self.stat)) + (other.val/(other.stat*other.stat)))*err2
        newerr = math.sqrt(err2)
        return data_pair(newval, newerr)

