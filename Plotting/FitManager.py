import ROOT
from ROOT import RooFit, gROOT, gSystem
from uncertainties import ufloat
import uuid
import re
import random
import sys
from collections import namedtuple, OrderedDict
from functools import wraps
from DrawConfig import DrawConfig
from pprint import pprint
gSystem.Load("My_double_CB/RooDoubleCB_cc.so")
from ROOT import RooDoubleCB


ROOT.gStyle.SetPalette(ROOT.kBird)

tColor_Off="\033[0m"       # Text Reset
tPurple="\033[0;35m%s"+tColor_Off       # Purple


def f_Obsolete(f):
        @wraps(f)
        def f_wrapper(*args, **kws):
                print f.__name__,": This method is obsolete"
                return f(*args,**kws)
        return f_wrapper

def f_Dumpfname(func):
    """ decorator to show function name and caller name """
    @wraps(func)
    def echo_func(*func_args, **func_kwargs):
        print('func \033[1;31m {}()\033[0m called by \033[1;31m{}() \033[0m'.format(func.__name__,sys._getframe(1).f_code.co_name))
        return func(*func_args, **func_kwargs)
    return echo_func

xname = "Reco mass m(#gamma,e)"
class FitManager :
    """ Aim to collect all fitting machinery here """

    ParamDCB = ["dcb_mass"   ,"dcb_sigma" ,
               "dcb_alpha1" ,"dcb_power1",
               "dcb_alpha2" ,"dcb_power2"]
    setuparray = {
                    "cb":
                        [("cb_mass"  ,"Mass"  ,90,80,100),
                         ("cb_sigma" ,"Sigma" ,1,0.1,100),
                         ("cb_alpha" ,"Alpha" ,-1,-10,10),
                         ("cb_power" ,"Power" ,2,0,10),
                        ],
                    "dcbp": # reparametrize IC
                        [
                        ("x"         ,20,200),
                        ("dcb_mass"  ,91,87,95),
                        ("dcb_sigma" ,3,1,10),
                        ("dcb_alpha1",1,0.5,3),
                        ("dcb_power1",1,1,50),
                        ("dcb_alpha2",1,0.5,3),
                        ("dcb_power2",2,0.5,8),
                        ],
                    "dcb":
                        [
                        ("x"         ,20,200),
                        ("dcb_mass"  ,91,87,95),
                        ("dcb_sigma" ,3,1,10),
                        ("dcb_alpha1",1,0.2,3),
                        ("dcb_power1",1,1,100),
                        ("dcb_alpha2",1,0.2,3),
                        ("dcb_power2",2,0.5,8),
                        ],
                    "expo":
                        [
                        ('x',),#no redefinition
                        ('expo_c',0,-0.1,0.01)
                        #('expo_c',0,), # const
                        ],
                    "gauzz": # gaussian modelling Z peak
                        [
                        ("x",20,200),
                        ('gauzz_mean',90,80,100),
                        ('gauzz_sig' ,3,0.5,10),
                        ],
                    "gauszg": # model Z gamma
                        [
                        ('x',),#no redefinition
                        ('gauszg_mean', 85,60,90),
                        ('gauszg_sig' , 6,5,15),
                        ],
                    "gaus":
                        [
                        ('x',),#no redefinition
                        ('gaus_mean',100,-100,200),
                        ('gaus_sig' , 40,30,200),
                        ],
                    "simul2": # with z gamma
                        [
                        ("Nsig",100000,10000,10000000),
                        ("Nbkg", 10000,    0,10000000),
                        ("Nzg" , 10000,    0,  100000),
                        ],
                    "simul":
                        [
                        ("Nsig",100000,10000,10000000),
                        ("Nbkg", 10000, 1000,10000000),
                        ],
                    "simulzg":
                        [
                        ("Nz"  ,100000,  100,10000000),
                        ("Nzg", 100000,  100,10000000),
                        ]
                 }
    LineDefs = [
            [RooFit.LineColor(ROOT.kRed)],
            [RooFit.LineColor(ROOT.kBlue),   RooFit.LineStyle(ROOT.kDashed),],
            [RooFit.LineColor(ROOT.kCyan+1), RooFit.LineStyle(ROOT.kDashed),],
            [RooFit.LineColor(ROOT.kTeal-2), RooFit.LineStyle(ROOT.kDashed),],
               ]
    def __init__(self, fname, hist=None, xvardata = None, #,xvarfit=None,
                    label="", sample_params={},
                    norders = 2 ) :

        # initialize object container
        self.defs = OrderedDict()          # store RooRealVar for fit functions
        self.func = None
        self.func_pdf = None
        self.fit_params = {}
        self.fitrange = None
        self.loaded = 0
        self.curr_decorations = []
        self.frame=self.subframe=None

        # copy input arguments
        self.func_name = fname
        self.label = label

        self.xvardata = xvardata  # data plot range
        #self.xvarfit = xvarfit    # fit range
        # if x range is not given, then make one
        if self.xvardata == None:
                self.xvardata = ROOT.RooRealVar("x",xname,0,200,"GeV")
        if isinstance(self.xvardata,tuple):
                self.xvardata = ROOT.RooRealVar("x",xname,*self.xvardata)
        #if self.xvarfit == None:
        #        self.xvarfit = self.xvardata
        self.pdfplotrange = False

        # toggles and extra parameters
        self.sample_params = sample_params

        # set the function orders
        # only useful for dijet, power, atlas functions, etc
        self.func_norders = norders

        self.canvas = None
        self.curr_canvases = {}
        self.objs = []
        self.addhist(hist) #default hist
        self.wk = None

    def addhist(self,hist,name="datahist", bkgd = False):
        if hist:
            assert isinstance(hist,ROOT.TH1)
            his = hist.Clone()
            # histogram style
            his.SetMarkerStyle( 20 )
            his.SetMarkerSize( 1.0 )
            if bkgd == False:
                his.SetLineColor( ROOT.kBlack )
                his.SetMarkerColor( ROOT.kBlack )
                self.hist = his
                # make datahist
                self.datahist = ROOT.RooDataHist( '%s%s' %(self.label,name), 'data',
                            ROOT.RooArgList(self.xvardata), his )

                if not hasattr(self, 'datahistlist'):
                   self.datahistlist = {}
                self.datahistlist['data'] = self.datahist
                ROOT.SetOwnership( self.datahist, False )
            else:
                his.SetLineColor( ROOT.kBlue-10 )
                his.SetMarkerColor( ROOT.kBlue-10 )
                self.histlist[bkgd] = his
                self.datahistlist[bkgd] = ROOT.RooDataHist( '%s%s' %(self.label,name), 'bkgd',
                                        ROOT.RooArgList(self.xvardata), his )
                ROOT.SetOwnership(self.datahistlist[bkgd], False )
        else:
            self.hist = None #ROOT.TH1F()
            self.datahist = None
            self.histlist={}
            self.datahistlist={}

    @f_Obsolete
    def MakeROOTObj( self, root_obj, *args ) :
        """ Generic function for making ROOT objects."""

        try :
            thisobj = getattr(ROOT, root_obj)( *args )
            ROOT.SetOwnership( thisobj, False )
            return thisobj

        except TypeError :
            print '***********************************************************'
            print 'FitManager.MakeROOTObj -- Failed to create a %s.  Please check the arguments :'%root_obj
            print args
            print 'Exception is below'
            print '***********************************************************'
            raise


    def Integral( self ) :

        err = ROOT.Double()
        val = self.hist.IntegralAndError( self.hist.FindBin( self.xvardata.getMin() ), self.hist.FindBin( self.xvardata.getMax() ), err )

        return ufloat( val, err )

    def MakeIntegral(self,intrange=None, pdfname = None):
        """ make pdf integral that returns in range [0,1] """
        if intrange is None:
            intrange = self.fitrange
        if pdfname is None:
            pdf = self.func_pdf
        else:
            pdf = self.wk.pdf(pdfname)
        self.integral = pdf.createIntegral(self.xvardata,RooFit.NormSet(self.xvardata),RooFit.Range(*intrange))
        return self.integral

    def get_integral_value(self, intrange=None, pdfname = None):
        """ calculate pdf integral return [0,1] """
        ### FIXME
        pass

    def get_vals( self, name, order ) :

        return self.defs[name][order]

    def add_vars_name_power(self, i):
        if i % 2 == 0:
            short_name = 'norm%d' %(i/2)
        else:
            short_name = 'power%d' %((i-1)/2)
        return short_name

    def add_vars_name_expow(self, i):
        if i == 0:
            short_name = 'norm%d' %(i/2)
        elif i % 2 == 0:
            short_name = 'expcoef%d' %(i/2)
        else:
            short_name = 'powercoef%d' %((i-1)/2)
        return short_name

    def add_vars_name_atlas(self, i):
        if i ==0:
            short_name = 'norm'
        if i ==1:
            short_name = 'power_num'
        if i ==2:
            short_name = 'power_den'
        if i > 2 :
            short_name = 'logcoef%d' %(i-2)
        return short_name

    def add_vars_name_dijet(self, i):
        if i ==0:
            short_name = 'norm'
        if i ==1:
            short_name = 'power'
        if i > 1 :
            short_name = 'logcoef%d' %(i-1)
        return short_name

    def add_vars( self, arg_list) :
        irange = range(1,  self.dof )
        if self.func_name == 'power' :
            #irange = range( 2* self.func_norders)
            add_vars_name = self.add_vars_name_power
        elif self.func_name == 'expow' :
            add_vars_name = self.add_vars_name_expow
        elif self.func_name == 'dijet' :
            #irange = range(  self.func_norders+1 )
            add_vars_name = self.add_vars_name_dijet
        elif self.func_name == 'atlas' or self.func_name == "vvdijet":
            add_vars_name = self.add_vars_name_atlas
        else: 
            print tPurple %"*** NO VARIABLE ADDED ***"

        for i in irange:
            short_name = add_vars_name(i)
            long_name = '%s_order%d_%s' %( self.func_name, i, self.label )
            this_def = self.get_vals( self.func_name, i )
            print short_name, this_def
            var = ROOT.RooRealVar( long_name, long_name, *this_def)
            ROOT.SetOwnership(var, False)
            arg_list.add( var  )
            self.fit_params[short_name] = var
        return


    @f_Dumpfname
    def get_fit_function( self, forceUseRooFit=False ) :

        function = ''

        if self.func_name == 'dijet' :
            self.dof = self.func_norders+1
            order_entries = []

            log_str = 'TMath::Log10(@0/13000)'
            for i in range( 1, self.func_norders) :
                order_entries.append('@'+str(i+1)+'*' + '*'.join( [log_str]*i))

            function = 'TMath::Power( @0/13000., @1 + ' + '+'.join( order_entries) + ')'

            self.defs['dijet'] = {}
            self.defs['dijet'][0] = ( 1e-10,  0,  1)
            self.defs['dijet'][1] = (-11.0,  -20.0,  -10.0)
            self.defs['dijet'][2] = ( -2.0,   -9.0,  -3.0 )
            self.defs['dijet'][3] = ( -1.5,   -5.0,  -1.0 )

            print "function: ", function


        if self.func_name == 'atlas' :
            self.dof = self.func_norders+3

            function = 'TMath::Power( (1-TMath::Power(@0/13000., 1./3)), @1 ) / ( TMath::Power( @0/13000. , @2+ %s ))'
            order_entries = []
            for i in range( 0, self.func_norders ) :
                order_entries.append( '@%d*TMath::Power(TMath::Log10( @0/13000.),%d)'  %( i+3, i+1 ) )

            function = function % (' + '.join( order_entries ))

            self.defs['atlas'] = {}
            self.defs['atlas'][0] = (   1 ,      0, 100000) #norm
            self.defs['atlas'][1] = (   0 ,      0,  1000)  #power numerator
            self.defs['atlas'][2] = (   2 ,     -10,   100) #power denominator
            self.defs['atlas'][3] = (  -1 ,     -10,    10) # log coeff
            self.defs['atlas'][4] = (  -1 ,     -10,    0)
            self.defs['atlas'][5] = (  -1 ,     -5,    10)

        if self.func_name == 'vvdijet' :
            self.dof = self.func_norders+3

            if self.func_norders>1:
                function = 'TMath::Power( (1-(@0/13000.)), @1 ) / ( TMath::Power( @0/13000. , @2*(%s) ))'
                order_entries = []
                for i in range( 1, self.func_norders ) :
                    order_entries.append( 'TMath::Power(TMath::Log10( @0/13000.),%d)'  %( i ) )

                function = function % (' + '.join( order_entries ))
            else:
                function = 'TMath::Power( (1-(@0/13000.)), @1 ) / ( TMath::Power( @0/13000. , @2 ))'

            #FIXME not tested IC
            self.defs['vvdijet'] = {}
            self.defs['vvdijet'][0] = (   1 ,      0, 100000) #norm
            self.defs['vvdijet'][1] = (   0 ,      0,  1000)  #power numerator
            self.defs['vvdijet'][2] = (   2 ,     -10,   100) #power denominator
            self.defs['vvdijet'][3] = (  -1 ,     -10,    10) # log coeff
            self.defs['vvdijet'][4] = (  -1 ,     -10,    0)
            self.defs['vvdijet'][5] = (  -1 ,     -5,    10)
            self.defs['vvdijet'][6] = (  -1 ,     -5,    10)

        if self.func_name == 'expow' :
            self.dof = self.func_norders+2

            order_entries = []
            function =  'TMath::Power( @0 / 13000., @1 ) * TMath::Exp(%s)'
            for i in range( 0, self.func_norders ) :
                order_entries.append( ('@%d' %(i*2+2)) + "*@0/13000."*(i+1) )

            function = function %("+".join(order_entries))

            #FIXME not tested IC
            self.defs['expow'] = {}
            self.defs['expow'][0] = (1e-5,    0,    1e7)
            self.defs['expow'][1] = (-5,       0,   -10 )
            self.defs['expow'][2] = (-10,    -200,   -1 )
            self.defs['expow'][3] = (5,        0,    10 )
            self.defs['expow'][4] = (10,    -200,    -1 )
            self.defs['expow'][5] = (-10,    -20,     0 )

        if self.func_name == 'power' :
            self.dof = self.func_norders*2

            order_entries = []
            order_entries.append( 'TMath::Power( @0 / 13000., @1 )' )
            for i in range( 1, self.func_norders ) :
                order_entries.append( '@%d*TMath::Power( @0 / 13000., @%d )'  %( i*2+1, i*2+2 ) )

            function = '+'.join( order_entries )

            self.defs['power'] = {}
            self.defs['power'][0] = ( 1,    0,    1e7)
            self.defs['power'][1] = (-5,       0,   -10 )
            self.defs['power'][2] = (-10,    -200,   -1 )
            self.defs['power'][3] = (5,        0,    10 )
            self.defs['power'][4] = (10,    -200,    -1 )
            self.defs['power'][5] = (-10,    -20,     0 )

        if forceUseRooFit :
            # different syntax for ROOT and RooFit
            print tPurple %function
            return function
        else :
            mod_function = function.replace( '@0', 'x' )
            #if self.func_name!="power": 
            mod_function = '[0]*(%s)' %mod_function
            for i in range( 0, 9 ) :
                mod_function = mod_function.replace( '@%d' %i, '[%d]' %i )
            print tPurple %mod_function
            return mod_function

    @f_Obsolete
    def fit_histogram( self, workspace=None ) :
        self.run_fit()
        self.calculate_func_pdf()
        return self.get_results( workspace )

    def create_standard_ratio_canvas(self,name="",xsize=800,ysize=750) :
        """ ported from SampleManager: setup canvas with ratio inset"""
        self.curr_canvases['base'+name] = ROOT.TCanvas('basecan'+name, 'basecan', xsize, ysize)

        self.curr_canvases['bottom'+name] = ROOT.TPad('bottompad'+name, 'bottompad', 0.01, 0.01, 0.99, 0.34)
        self.curr_canvases['top'+name] = ROOT.TPad('toppad'+name, 'toppad', 0.01, 0.34, 0.99, 0.99)
        self.curr_canvases['top'+name].SetTopMargin(0.08)
        # so that the ratio plot touches main plot, ie no gaps in btwn
        self.curr_canvases['top'+name].SetBottomMargin(0.0)
        self.curr_canvases['top'+name].SetLeftMargin(0.1)
        self.curr_canvases['top'+name].SetRightMargin(0.05)
        self.curr_canvases['bottom'+name].SetTopMargin(0.00) #no gaps
        self.curr_canvases['bottom'+name].SetBottomMargin(0.3)
        self.curr_canvases['bottom'+name].SetLeftMargin(0.1)
        self.curr_canvases['bottom'+name].SetRightMargin(0.05)
        self.curr_canvases['base'+name].cd()
        self.curr_canvases['bottom'+name].Draw()
        self.curr_canvases['top'+name].Draw()

    def fitrangehelper(self,fitrange):
        """ Convert fit range to tuples """
        if not fitrange: return
        if isinstance(fitrange,tuple) and len(fitrange)==2:
                return fitrange
        #if isinstance(fitrange,ROOT.RooRealVar):
        #        print "updating fit range"
        #        self.xvarfit = fitrange
        #xmin = self.xvarfit.getMin()
        #xmax = self.xvarfit.getMax()
        xmin = fitrange.getMin()
        xmax = fitrange.getMax()
        return (xmin,xmax)

    def setup_fit(self ,fitrange = None, dofit=False, **setupargs) :
        """ fitter using RooFit package """
        # get fit function string if it is simple
        func_str = self.get_fit_function()
        fitrange = self.fitrangehelper(fitrange)

        #arg_list = ROOT.RooArgList()
        #ROOT.SetOwnership(arg_list, False)

        #arg_list.add( self.xvardata )
        # adding extra variables for dijet functions
        # arglist is passed to take new variables
        #self.add_vars( arg_list)

        #if self.func_name == 'bwxcb' : self.init_bwxcb()
        if self.func_name == 'dscb'  : self.init_dscb()
        elif self.func_name == 'cb'  : self.init_cb()
        elif self.func_name == 'dcb' : self.init_dcb(reparam=False, **setupargs)
        elif self.func_name == 'dcbp' : self.init_dcb(**setupargs)
        elif self.func_name == 'dcbexpo' : self.init_dcbexpo(**setupargs)
        else :
             # generic function maker
             self.func_pdf = ROOT.RooGenericPdf( '%s_%s'
                    %(self.func_name, self.label), self.func_name, func_str, arg_list)

        # do fit if requested
        if dofit:
            self.run_fit(fitrange)
        return self.func_pdf

    def run_fit(self, fitrange = None):
        """ run RooFit Fitter """
        self.fitrange = self.fitrangehelper(fitrange)
        self.xvardata.setRange("runfit",*self.fitrange)
        self.fitresult = self.func_pdf.fitTo( self.datahist,
                                         RooFit.Range("runfit"),
                                         RooFit.SumCoefRange("runfit"),
                                         #ROOT.RooFit.Range(*self.fitrange),
                                         #ROOT.RooFit.Extended(),
                                         RooFit.SumW2Error(True),
                                         ROOT.RooCmdArg( 'Strategy', 3 ) ,
                                         RooFit.Save(ROOT.kTRUE))
        return

    def run_fit_chi2(self, fitrange = None):
        """ run RooFit Chi2 Fitter
            - To be used with weighted data
        """
        self.fitrange = self.fitrangehelper(fitrange)
#        self.option = ROOT.RooLinkedList()
 #       self.option.Add(ROOT.RooFit.Range(*self.fitrange))
        self.fitresult = self.func_pdf.chi2FitTo( self.datahist,ROOT.RooLinkedList())
        #ROOT.RooFit.Range(*self.fitrange))
                     #ROOT.RooFit.SumW2Error(True), ROOT.RooCmdArg( 'Strategy', 1) ,
                     #ROOT.RooFit.SumW2Error(True), ROOT.RooCmdArg( 'Strategy', 3 ) ,
                     #ROOT.RooFit.Save(ROOT.kTRUE))
        return

    def run_fit_minuit(self, fitrange= None, debug = True ):
        """
        run the RooFit Fitter and MIGRAD, HESSE and MINOS
        """
        self.fitrange = self.fitrangehelper(fitrange)
        print self.fitrange
        self.xvardata.setRange("runfit",*self.fitrange)
        self.func_pdf.fitTo( self.datahist,
                             RooFit.Save(),
                             RooFit.Range("runfit"),
                             ROOT.RooFit.SumW2Error(True),
                             ROOT.RooCmdArg( 'Strategy', 3 ) )
        if debug:
           print "\n**************************"
           print "***** finished fitTo in RooFit ******"
           print "*********************\n"

        # construct the Log(Likelihood)
        nll = self.func_pdf.createNLL(self.datahist) ;
        m = ROOT.RooMinimizer(nll)

        m.migrad()
        if debug:
           print "\n*************************************"
           print "************ finished MIGRAD ****************"
           print "***************************************\n"
        m.hesse()
        if debug:
           print "\n*************************************"
           print "************ finished HESSE *****************"
           print "***************************************\n"
        m.minos()
        if debug:
           print "\n*************************************"
           print "************ finished MINOS *****************"
           print "***************************************\n"
        self.roofitresult = m.save()

    def setup_rootfit(self, fitrange=None ):
        """  fit in ROOT """
        fitrange = self.fitrangehelper(fitrange)
        func_str = self.get_fit_function()

        self.func = self.MakeROOTObj( 'TF1', 'tf1_%s' %self.label, func_str, fitrange[0], fitrange[1] )

        for i in range( 0, self.dof ) :
            this_def = self.get_vals( self.func_name, i )
            print i, this_def[0]
            self.func.SetParameter( i, this_def[0] )

    def run_rootfit(self):
        self.hist.Fit( self.func, 'REM' )
        ## do it a few times
        #print "********** fit again *****************"
        #for iparam in xrange( 1, self.func_norders+1 ):
        #    self.func.SetParameter( iparam, self.func.GetParameter(iparam))
        #self.hist.Fit( self.func, 'REM' )
        #print "********** fit again *****************"
        #for iparam in xrange( 1, self.func_norders+1 ):
        #    self.func.SetParameter( iparam, self.func.GetParameter(iparam))
        #self.hist.Fit( self.func, 'REM' )
        return self.func


    def get_parameters(self):
        return self.defs.items()

    def get_parameter_values(self):
        plist = {}
        for name, parm in self.get_parameters():
                plist[name] = ufloat(parm.getVal(),parm.getError()) if parm else None
        return plist


    def calculate_func_pdf( self ) :
        """
        cast a TF1 into RooGenericPdf in RooFit. So that it can be saved in RooWorkspace for the HiggsCombine
        """

        if self.func_pdf is not None :
            print 'The PDF Function already exists.  It will be overwritten'

        #if self.func_name == 'power' :
        for i in range( self.dof ) :
            fitted_result = self.func.GetParameter(i)
            fitted_error = self.func.GetParError(i)

            self.defs[self.func_name][i] = ( fitted_result, fitted_result - fitted_error, fitted_result + fitted_error )

        arg_list = self.MakeROOTObj( 'RooArgList' )
        arg_list.add( self.xvardata )
        self.add_vars( arg_list )

        for i in range( 0, arg_list.getSize() )  :
            fitted_error = self.func.GetParError(i)
            print "fitted error: ", tPurple %fitted_error
            arg_list[i].setError( fitted_error )

        func_str = self.get_fit_function( forceUseRooFit=True)

        self.func_pdf = self.MakeROOTObj( 'RooGenericPdf', '%s_%s' %( self.func_name, self.label), self.func_name, func_str, arg_list)

        #if self.func_name == 'dijet' :
        #    for i in range( 1, self.func_norders+1 ) :
        #        fitted_result = self.func.GetParameter(i)
        #        fitted_error = self.func.GetParError(i)

        #        self.defs['dijet'][i] = ( fitted_result, fitted_result - fitted_error, fitted_result + fitted_error )

        #    arg_list = self.MakeROOTObj( 'RooArgList' )
        #    arg_list.add( self.xvardata )
        #    self.add_vars( arg_list )

        #    for i in range( 1, arg_list.getSize() )  :
        #        fitted_error = self.func.GetParError(i)
        #        arg_list[i].setError( fitted_error )

        #    func_str = self.get_fit_function( forceUseRooFit=True)

        #    self.func_pdf = self.MakeROOTObj( 'RooGenericPdf', '%s_%s' %( self.func_name, self.label), self.func_name, func_str, arg_list)


    def save_fit( self, sampMan=None, workspace = None, logy=False, stats_pos='right' ) :

        if sampMan is not None :

            for name, param in self.fit_params.iteritems() :
                param.SetName( name)

            can = ROOT.TCanvas( str(uuid.uuid4()), '' )
            frame = self.xvar.frame()
            self.datahist.plotOn(frame)
            self.func_pdf.plotOn( frame )
            if stats_pos == 'left' :
                self.func_pdf.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.1,0.5,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(3)));
            if stats_pos == 'right' :
                self.func_pdf.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
            frame.Draw()
            if logy :
                ymax = frame.GetMaximum()
                frame.SetMinimum( 0.001 )
                frame.SetMaximum( ymax*10 )
                can.SetLogy()
                can.SetLogx()

            sampMan.outputs[self.label] = can

    def get_results( self, workspace = None) :
        print "get_results",workspace, self.datahist


        results = {}
        for param in self.fit_params.values() :
            ## FIXME getErrorHi ??
            results[param.GetName()] = ufloat( param.getValV(), param.getErrorHi() )
            print param.GetName(), ufloat( param.getValV(), param.getErrorHi( ))


        #power_res = ufloat( power.getValV(), power.getErrorHi() )
        #log_res   = ufloat( logcoef.getValV(), logcoef.getErrorHi())
        #int_res   = ufloat( integral, math.sqrt( integral ) )

        results['integral'] = self.Integral( )
        integral_var = ROOT.RooRealVar('%s_norm' %( self.func_pdf.GetName() ), 
                        'normalization', results['integral'].n )
        integral_var.setError( results['integral'].s )

        print "importing"
        if workspace is not None :
            ## NOTE getattr is needed to escape python keyword import
            getattr( workspace, "import" ) ( self.datahist )
            getattr( workspace, "import" ) ( self.func_pdf )
            getattr( workspace, "import" ) ( integral_var  )


        return results


    def get_correlations(self):
        ROOT.gStyle.SetOptStat(0)
        if not self.fitresult: return
        self.curr_canvases["corr"] = ROOT.TCanvas("c_corr","correlation",400,400)
        self.curr_canvases["corr"].SetLeftMargin(0.15)
        self.curr_canvases["corr"].SetRightMargin(0.15)
        self.hcorr = self.fitresult.correlationHist()
        self.hcorr.Draw("COLZ")
        return self.curr_canvases["corr"]

    @f_Obsolete ## for testing purposes: doesn't seem to work
    def updatedraw(self,subplot=""):
        if subplot:
            if "top" in self.curr_canvases:
                self.curr_canvases["top"].cd()
            else:
                print "cannot update"
                return
        elif self.canvas:
            self.canvas.cd()
        else: return
        self.frame.Draw()
        if subplot:
            self.curr_canvases["bottom"].cd()
            self.subframe.Draw()
            return self.curr_canvases["base"]
        else:
            return self.canvas



    def draw(self,title=" ",yrange=None,subplot="",component=False,**kw):
        """
            component: True: take default component list from self.component
                       list: list of component names to be drawn
                       default is false, not drawing components
            subplot  : pull or residue
        """
        # Make canvas
        dology = kw.get("logy",0)
        if subplot:
            self.create_standard_ratio_canvas()
            self.curr_canvases["top"].SetLogy(dology)
            self.curr_canvases["top"].cd()
        elif not subplot:
            self.canvas = ROOT.TCanvas("cfit%s"%self.label,"Fitter",800,500) #FIXME: change canvas
            self.canvas.SetTopMargin(0.08)
            #self.canvas.SetBottomMargin(0.0)
            self.canvas.SetLeftMargin(0.1)
            self.canvas.SetRightMargin(0.1)
            self.canvas.SetLogy(dology)
            self.canvas.cd()

        # make frame
        self.frame = self.xvardata.frame(RooFit.Title(title))
        print "initalised frame"
        self.frame.Print()
        # plot data histogram
        if component:
            hlist = [h for h in self.datahistlist.values() if h!= self.datahist]
            for h in hlist:
                h.plotOn(self.frame,RooFit.DataError(ROOT.RooAbsData.SumW2),
                    RooFit.DrawOption("B"),RooFit.DataError(ROOT.RooAbsData.None),
                        RooFit.XErrorSize(0),RooFit.FillColor(ROOT.kBlue-10))
                print "PLOTONN: ", h
        self.datahist.plotOn(self.frame,RooFit.DataError(ROOT.RooAbsData.SumW2))

        #
        # old setup fitted for the signal and MC bkg fits
        #
        useOldsetup = kw.get("useOldsetup", False)
        print "use old setup: ",useOldsetup

        # plotting fitted function
        if self.func_pdf:
            #plotparm   = [self.frame,RooFit.NormRange('myrange')]
            plotparm   = [self.frame,]
            #if  self.pdfplotrange and self.fitrange:
            #    plotparm.append(RooFit.Range(*self.fitrange))
            #if True: ## FIXME
            plotparm+=[RooFit.NormRange("runfit"),RooFit.Range("runfit")]
            if component == True:
                component = self.components
            if isinstance(component,list):
                for i,comp in enumerate(map(RooFit.Components,component)):
                    self.func_pdf.plotOn(*(plotparm+FitManager.LineDefs[i+1]+[comp,]))
                    print "PLOTONN2: ", i, comp, plotparm+FitManager.LineDefs[i+1]+[comp,]
            self.func_pdf.plotOn(*(plotparm+FitManager.LineDefs[0]))
            print "plotparm"
            print plotparm
            pmlayout = kw.get("paramlayout",(0.65,0.9,0.7))
            ## toggle off parameters with None in layout
            if  pmlayout:
                if useOldsetup:
                   # make the param names short
                   for name, param in self.fit_params.iteritems() :
                       param.SetName( name )
                   self.func_pdf.paramOn( self.frame, ROOT.RooFit.ShowConstants(True),
                                          ROOT.RooFit.Layout(*pmlayout),
                                          ROOT.RooFit.Format("NBNEU" ,
                                          ROOT.RooFit.FixedPrecision(2)) )
                   # to make the border size zero for the parameters
                   # this seems like a dangerous way to do, but currrently can not find a better way
                   self.frame.findObject("%s_paramBox"%self.func_pdf.GetName())\
                                                            .SetBorderSize(0)
                else:
                   self.func_pdf.paramOn(self.frame,
                            RooFit.Layout(*pmlayout)).Draw()
        # set y axis range
        if dology:
           self.frame.SetMinimum(1e-5)
        if isinstance(yrange,tuple):
            if yrange[0]!=None: self.frame.SetMinimum(yrange[0])
            if yrange[1]!=None: self.frame.SetMaximum(yrange[1])
        self.frame.Draw()
        ROOT.gPad.SetTicks(1,1)
        # draw the plot status label
        label_config = kw.get("label_config",{})
        label_config.update({"dx":-0.05,"dy":0.0})
        self.draw_label(label_config=label_config)
        # draw pull or residual plot
        if subplot:
            self.curr_canvases["bottom"].cd()
            if subplot == "pull": self.makepull(self.xvardata)
            if subplot == "resd": self.makeresd(self.xvardata)
            self.subframe.Draw()
            #if subplot == "pull": self.subframe.GetYaxis().SetRangeUser(-6,6)
            self.ratio_formatting()
            if useOldsetup:
               self.subframe.GetYaxis().SetNdivisions(205)
               self.subframe.GetYaxis().CenterTitle()
               self.subframe.GetYaxis().SetRangeUser(-5.0,5.0)
               self.subframe.GetXaxis().SetTitle("m_{T} [GeV]")
            ROOT.gPad.SetTicks(1,1)
            chi  =self.getchisquare()
            print "Printed Chi: ",chi
            # print chi-sq
            self.latex = ROOT.TLatex()
            self.latex.SetTextSize(0.1)
            self.latex.SetTextColor(ROOT.kRed)
            self.latex.DrawLatexNDC(0.12,0.9,"#chi^{2}/ndof = %.4g" %chi)
            self.subframe.addObject(self.latex)

            # draw line
            x=self.subframe.GetXaxis()
            xlow =  x.GetXmin()
            xhigh = x.GetXmax()
            self.line = ROOT.TLine(xlow,0,xhigh,0)
            self.line.SetLineStyle(3)
            self.line.SetLineWidth(2)
            self.line.Draw()
            self.subframe.addObject(self.line)
            return self.curr_canvases["base"]
        return self.canvas

    def getchisquare(self,dof = None):
        if dof is None:
            #return self.frame.chiSquare("simul2",6)
            return self.frame.chiSquare(self.dof) 
        return self.frame.chiSquare(dof) 

    def draw_label(self,**kw):
        draw_config = DrawConfig("","","",**kw)
        labels = draw_config.get_labels()
        for lab in labels :
            lab.Draw()
            self.curr_decorations.append( lab )

    def ratio_formatting(self):
        """ resize ratio label sizes as they are plotted in smaller pad """
        xAxs = self.subframe.GetXaxis()
        yAxs = self.subframe.GetYaxis()
        xAxs.SetTitleSize(0.085)
        xAxs.SetLabelSize(0.08)
        xAxs.SetTitleOffset(0.9)
        yAxs.SetTitleSize(0.08)
        yAxs.SetLabelSize(0.08)
        yAxs.SetTitleOffset(0.45)
        return

    def makepull(self,x):
        """ make pull histogram: helper function to FitManager.draw() """
        hpull = self.frame.pullHist()
        self.subframe = x.frame(RooFit.Title(" "))
        self.subframe.addPlotable(hpull,"P")
        self.subframe.SetYTitle("Pull")
        return

    def makeresd(self,x):
        """ make residual histogram: helper function to FitManager.draw() """
        hresd = self.frame.residHist()
        self.subframe = x.frame(RooFit.Title(" "))
        self.subframe.addPlotable(hresd,"P")
        self.subframe.SetYTitle("Residual")
        return

    @f_Obsolete
    def init_bwxcb(self):
        """ old function used for signal fitting. Not used anymore """
        mass =  self.sample_params['mass']
        width = self.sample_params['width']

        bw_width = mass*width
        if bw_width < 2  :
            bw_width = 2

        bw_m = self.MakeROOTObj( 'RooRealVar', 'bw_mass_%s' %self.label, 'Resonance  Mass', mass, xmin, xmax, 'GeV' )
        bw_w = self.MakeROOTObj('RooRealVar', 'bw_width_%s' %self.label, 'Breit-Wigner width',bw_width, 0, 200,'GeV')
        bw_m.setConstant()
        #bw_w.setConstant()
        bw = self.MakeROOTObj('RooBreitWigner','bw_%s' %self.label, 'A Breit-Wigner Distribution', self.xvar, bw_m,bw_w)

        #------------------------------
        # crystal ball, has four parameters
        #------------------------------
        sigma_vals = self.defs['cb_sigma'][mass]
        power_vals = self.defs['cb_power'][mass]
        mass_vals  = self.defs['cb_mass'][mass]
        cb_cut   = self.MakeROOTObj('RooRealVar','cb_cut_%s' %self.label, 'Cut'  , 0.5, 0.5, 0.50 , '')
        cb_sigma = self.MakeROOTObj('RooRealVar','cb_sigma_%s' %self.label, 'Width', sigma_vals[0], sigma_vals[1], sigma_vals[2], 'GeV')
        cb_power = self.MakeROOTObj('RooRealVar','cb_power_%s' %self.label, 'Power', power_vals[0], power_vals[1], power_vals[2], '')
        cb_m0    = self.MakeROOTObj('RooRealVar','cb_mass_%s' %self.label, 'mass' , mass_vals[0], mass_vals[1], mass_vals[2],'GeV')

        #cb_cut.setConstant()
        #cb_power.setConstant()
        #cb_m0.setConstant()

        cb_cut.setError( 0.05 )
        cb_sigma.setError( 0.5 )
        cb_power.setError( 1. )
        cb_m0.setError( 1. )

        cb = self.MakeROOTObj('RooCBShape','cb_%s' %self.label, 'A  Crystal Ball Lineshape', self.xvar, cb_m0, cb_sigma,cb_cut,cb_power)

        self.func_pdf = self.MakeROOTObj('RooFFTConvPdf','sig_model_%s' %self.label,'Convolution', self.xvar, bw, cb)

        self.fit_params['bw_mass'] = bw_m
        self.fit_params['bw_width'] = bw_w
        #self.fit_params['bw'] = bw

        self.fit_params['cb_cut'] = cb_cut
        self.fit_params['cb_sigma'] = cb_sigma
        self.fit_params['cb_power'] = cb_power
        self.fit_params['cb_mass'] = cb_m0
        #self.fit_params['cb'] = cb

    def init_dscb(self):
        mass =  self.sample_params['mass']
        width = self.sample_params['width']

        # TODO: this can be updated and merged to setuparray
        cut1_vals   = (  0.3,       0.1,      0.6  )
        sigma_vals  = ( 28. ,       1. ,      200. )
        power1_vals = (  2.0,       1.4,      4.6  ) if width==1e-4 else ( 3.0,        2.4,       4.0 )
        mass_vals   = ( mass,  0.5*mass,  1.1*mass)
        cut2_vals   = (  1.5,       1.,       2.5  )
        power2_vals = (  4.0,       0.,       5.0  )

        cb_cut1   = ROOT.RooRealVar('cb_cut1_%s'   %self.label,   'Cut1'  ,  cut1_vals[0],   cut1_vals[1],   cut1_vals[2],   '')
        cb_sigma  = ROOT.RooRealVar('cb_sigma_%s'  %self.label,   'Width' ,  sigma_vals[0],  sigma_vals[1],  sigma_vals[2],  'GeV')
        cb_power1 = ROOT.RooRealVar('cb_power1_%s' %self.label,   'Power' ,  power1_vals[0], power1_vals[1], power1_vals[2], '')
        cb_m0     = ROOT.RooRealVar('cb_mass_%s'   %self.label,   'mass'  ,  mass_vals[0],   mass_vals[1],   mass_vals[2],   'GeV')
        cb_cut2   = ROOT.RooRealVar('cb_cut2_%s'   %self.label,   'Cut2'  ,  cut2_vals[0],   cut2_vals[1],   cut2_vals[2],   '')
        cb_power2 = ROOT.RooRealVar('cb_power2_%s' %self.label,   'Power' ,  power2_vals[0], power2_vals[1], power2_vals[2], '')

        # fix a few params in the signal fit
        cb_cut2.setConstant()
        cb_cut2.setError(0.0)

        cb_power2.setConstant()
        cb_power2.setError(0.0)

        cb_power1.setConstant()
        cb_power1.setError(0.0)

        self.dof = 3

        self.func_pdf = ROOT.RooDoubleCB( 'cb_%s'%self.label, 'Double Sided Crystal Ball Lineshape', self.xvardata, cb_m0, cb_sigma, cb_cut1, cb_power1, cb_cut2, cb_power2)

        self.fit_params['cb_cut1'] = cb_cut1
        self.fit_params['cb_sigma'] = cb_sigma
        self.fit_params['cb_power1'] = cb_power1
        self.fit_params['cb_mass'] = cb_m0
        self.fit_params['cb_cut2'] = cb_cut2
        self.fit_params['cb_power2'] = cb_power2

    def make_factory_string(self, classname, pdfname, valsar, norange=False):
        """ input string for RooFactory custom pdf

            valsar   : list of tuples of the format
                       (variable name, range)
            classname: pdf class name
            pdfname  : pdf instance name
        """
        factstr = []
        for v in valsar:
            name = v[0]
            if not norange and v[1:]:
                vrange = ",".join(map(str,v[1:]))
                factstr.append("%s[%s]" %(name,vrange))
            else:
                factstr.append(name)

        argstr = ",".join(factstr)
        return "%s::%s(%s)" %(classname,pdfname,argstr)

    def make_expression_string(self, varname, varexp):
        """ make factory expression with name and formula of expression """
        print varexp
        varlist = re.split('[+\-*/() ]',varexp) # minus needs escape
        varlist = [v for v in varlist if v]
        varlist = ','.join(list(set(varlist)))
        return "expr::%s('%s',%s)" %(varname, varexp, varlist)

    def fact(self,factstring):
        print tPurple %factstring
        self.wk.factory(factstring)

    def retrieve_param(self,valsar):
        # retrieve parameters
        for v in valsar:
            name = v[0]
            if isinstance(v, str):
                name = v
            if name!="x":
                ## if variable is already registered
                #if name in self.defs:
                #    print "already registered: ",name, self.defs[name], self.wk.var(name)
                self.defs[name] = self.wk.var(name)
        self.xvardata = self.wk.var("x") #update xv

    def init_cb(self,icond = "cb"):
        #------------------------------
        # crystal ball, has four parameters
        #------------------------------
        valsar = FitManager.setuparray[icond] #[Setup("cb",100)] #[0][1] #FIXME
        cbvals = []
        for v in valsar:
            name = v[0] #+self.label
            vtmp = ROOT.RooRealVar(*v)
            self.defs[name] = vtmp # store in instance dict
            cbvals.append(vtmp)    # values given in

        # assume that error is relatively stable
        self.defs["cb_mass"].setError( 1. )
        self.defs["cb_sigma"].setError( 0.5 )
        self.defs["cb_alpha"].setError( 0.05 )
        self.defs["cb_power"].setError( 1. )
                                                                                                    # x mean sigma alpha n
        cb = self.MakeROOTObj('RooCBShape','cb_%s' %self.label, 'A  Crystal Ball Lineshape', self.xvardata,*cbvals)

        self.func_pdf = cb

    def init_dcb(self,icond="dcbp", pdflabel = "",
            makenewfactory = True, reparam = True, seterr = True):
        """ reparam: reparametrize by rooFactory expr
            makenewfactory: replace existing factory object
        """
        #------------------------------
        # double crystal ball reparametrized
        #------------------------------
        if pdflabel:
            pdflabel = "_"+pdflabel
            makenewfactory = False
        if isinstance(icond, list):
            valsar = icond
        elif isinstance(icond,str):
            valsar = FitManager.setuparray[icond]
        factstr = self.make_factory_string("DoubleCB","doublecb"+pdflabel,valsar)
        print factstr
        if not self.loaded:
                self.loaded = ROOT.gROOT.ProcessLineSync(".x DoubleCB.cxx+")

        # make factory
        if makenewfactory or not self.wk: self.wk = ROOT.RooWorkspace("doublecb")
        # make ordinary double crystal ball
        self.fact(factstr)
        #self.wk.factory(factstr)
        if reparam:
            # define reparametrization
            #self.wk.factory("expr::scaled_power1('dcb_power1/dcb_alpha1',
            #dcb_power1, dcb_alpha1)")
            #self.wk.factory("expr::scaled_power2('dcb_power2/dcb_alpha2',
            #dcb_power2, dcb_alpha2)")
            exprstr1 = self.make_expression_string('scaled_power1',
                    'dcb_power1/dcb_alpha1')
            exprstr2 = self.make_expression_string('scaled_power2',
                    'dcb_power2/dcb_alpha2')
            self.fact(exprstr1)
            self.fact(exprstr2)
            if reparam == 2: # also parametrize shift of mass
                exprstr3 = "expr::mass_real('dcb_mass+dcb_mass_shift',dcb_mass,dcb_mass_shift[0,-10,10])" ##FIXME later
                self.fact(exprstr3)
                self.fact("DoubleCB::dcbp2%s(x,mass_real,dcb_sigma,"
                                   "dcb_alpha1,scaled_power1, dcb_alpha2, scaled_power2)" %pdflabel)
            else:
                self.fact("DoubleCB::dcbp%s(x,dcb_mass,dcb_sigma,"
                                   "dcb_alpha1,scaled_power1, dcb_alpha2, scaled_power2)" %pdflabel)
            self.func_pdf = self.wk.pdf("dcbp"+pdflabel)
        else:
            self.func_pdf = self.wk.pdf("doublecb"+pdflabel)
        self.retrieve_param(valsar)
        if seterr: self.dcbseterr()
        # retrieve parameters
        #for v in valsar:
        #    name = v[0]
        #    if name!="x": self.defs[name] = self.wk.var(name)
        self.xvardata = self.wk.var("x") #update xvardata
        self.xvardata.SetTitle(xname)
        self.xvardata.setUnit("GeV")
        # explicitly require fit range in case of factory function
        self.pdfplotrange = True
        self.dof = 6

    def dcbseterr(self):
        # initial step sizes: set them to be reasonably small
        # ballparking only and need no change for the same category of fits
        pprint(self.defs)
        self.defs["dcb_mass"]  .setError( 0.1 )
        self.defs["dcb_sigma"] .setError( 0.1 )
        self.defs["dcb_alpha1"].setError( 0.01 )
        self.defs["dcb_power1"].setError( 0.1 )
        self.defs["dcb_alpha2"].setError( 0.01 )
        self.defs["dcb_power2"].setError( 0.1 )


    def init_dcbexpo(self, sig = "dcbp", bkgd = "gaus", bkgd2 = None, ext='simul', icparm = None):
        """ icond: initial condition for dcb """
        self.wk = ROOT.RooWorkspace("dcb_bkgd")
        name = [""]*3
        ## step 1: Double CB shape
        name[0] = sig
        if   sig == "dcbp": # redefined cutoff alpha
            valsar1 = FitManager.ParamDCB #NOTE contain no initial values
            self.init_dcb(icond = icparm.get("dcbp"), makenewfactory = False, seterr = False)
        elif  sig == "dcbp2":  #added mass shift term
            valsar1 = FitManager.ParamDCB
            self.init_dcb(icond = icparm.get("dcbp"), makenewfactory = False, seterr = False, reparam = 2)
        elif sig == "gauzz":
            valsar1 = icparm.get(sig,FitManager.setuparray[sig])
            factstr1 = self.make_factory_string("Gaussian"   ,sig,valsar1)
            self.fact(factstr1)
        ## step 2: prepare background
        name[1]   = "bkgd"
        valsar2 = icparm.get(bkgd,FitManager.setuparray[bkgd])
        if   "expo" in bkgd:
            factstr2 = self.make_factory_string("Exponential",name[1],valsar2)
        elif "gaus" in bkgd:
            factstr2 = self.make_factory_string("Gaussian"   ,name[1],valsar2)

        ## step 3: prepare optional z gamma gaussian
        factstr3 = ""
        if bkgd2 is not None:
            name[2] = "bkgd2"
            if "gaus" in bkgd2: valsar3  = list( icparm.get("gauszg"))
            if bkgd2=="gauszg2": # also parametrize shift of mass
                exprstr3 = "expr:zgmean_real('gauszg_mean+dcb_mass_shift',gauszg_mean[%g],dcb_mass_shift)" %valsar3[1][1]
                self.fact(exprstr3)
                valsar3[1]= ('zgmean_real',)
            if "gaus" in bkgd2:
                factstr3 = self.make_factory_string("Gaussian", name[2], valsar3)

        ## step 4: extended pdf
        ## SUM for pdf instead of functions
        valsarex = icparm.get(ext,FitManager.setuparray[ext])
        #factstrex = "SUM::"+ext+"(%s[%g,%g,%g]"%valsar3[0]+ "*%s," %name1+\
        #                      "%s[%g,%g,%g]"%valsar3[1]+ "*%s)" %name2
        pprint(valsarex)
        f = lambda nlist, unc: tuple(round(i * random.normalvariate(1,unc)) if isinstance(i,(int,float)) else i for i in nlist)
        factstrex = ["%s[%g,%g,%g]" %f(v,0.2) + "*%s" %name[i] for i,v in enumerate(valsarex)]
        factstrex = ",".join(factstrex)
        factstrex = "SUM::%s(%s)" %(ext,factstrex)
        ## fill component list
        self.components=[n for n in name if n]

        #make factory
        self.fact(factstr2)
        if factstr3: self.fact(factstr3)
        self.fact(factstrex)
        ## print current factory setup
        self.wk.Print()
        self.retrieve_param(valsar1)
        self.retrieve_param(valsar2)
        if bkgd2 is not None: self.retrieve_param(valsar3)
        self.retrieve_param(valsarex)
        self.func_pdf = self.wk.pdf(ext)
        print "DEFINED VARIABLES"
        pprint(self.defs.items())
        self.pdfplotrange = False ## FIXME: needed?

