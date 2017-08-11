import ROOT
import numpy
import math

class Calculator( ) :

    def __init__(self) :

        self.values = None
        self.err_matrix = None
        self.alpha_array = None
        self.calc_err = False

    def clear(self) :
        self.__init__()

    def SetMeasurementValues( self, values ) :

        if self.err_matrix is not None :
            if len(values) != len(self.err_matrix) :
                print 'Input data size does not match size of error matrix!'
                return

        self.values = numpy.array( values )

    def AddErrorMatrix( self, matrix ) :

        if self.values is not None :
            if len( matrix ) != len( self.values ) :
                print 'Input matrix size does not match value size!'
                return
        if self.err_matrix is not None :
            if len( matrix ) != len( self.err_matrix ) :
                print 'Input matrix size does not match size of previously added matrix!'
                return

        this_matrix = numpy.matrix( matrix )

        if self.err_matrix is None :
            self.err_matrix = this_matrix
        else :
            self.err_matrix = self.err_matrix + this_matrix

    def CalculateCombinedValue(self) :

        if self.alpha_array is None :
           self.__calculate_alphas()

        if self.calc_err :
            return -1
        else :
            val = self.values.transpose().dot( self.alpha_array )
            return val

    def CalculateCombinedUncertainty(self) :

        if self.alpha_array is None :
           self.__calculate_alphas()

        if self.calc_err :
            return 0
        else :
            errsq = self.alpha_array.transpose().dot( self.err_matrix.dot( self.alpha_array ).getA1() )
            return math.sqrt(errsq)

    def SetAlphas( self, alphas ) :

        self.alpha_array = alphas

    def GetAlphas( self ) :
    
        if self.alpha_array is None :
           self.__calculate_alphas()

        return self.alpha_array

    def __calculate_alphas(self) :

        self.calc_err = False

        # method of lagrange multipliers
        unity_vec = numpy.array( [1]*len(self.values) )

        try :
            denominator = unity_vec.transpose().dot((self.err_matrix.getI().dot(unity_vec)).getA1())
        except numpy.linalg.linalg.LinAlgError :
            self.calc_err = True
            return

        numerator = self.err_matrix.getI().dot(unity_vec).getA1()

        self.alpha_array = numerator/denominator



