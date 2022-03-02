""" Sample Manager: Store imported Samples, General Plot methods
"""
import os
import pdb
import sys
import math
import re
import imp
import ROOT
import copy
import getpass
import uuid
import itertools
import eos_utilities
import random
from array import array
import time
import analysis_utils
from functools import wraps
from uncertainties import ufloat, umath
import pickle
import core
import subprocess
import multiprocessing
import fnmatch
from collections import OrderedDict
from DrawConfig import DrawConfig, LegendConfig, LabelConfig, HistConfig

ROOT.gROOT.SetBatch(False)

ROOT.gStyle.SetPalette(1)
tColor_Off="\033[0m"                       # Color Reset
tRed      ="\033[1;31m%s"+tColor_Off       # Red
tPurple   ="\033[0;35m%s"+tColor_Off       # Purple

_STACKNAME = '__AllStack__'
_DEFAULTCOLORS = [
    #ROOT.kGray,
    ROOT.kRed+1, ROOT.kAzure+2, ROOT.kGreen+2, ROOT.kMagenta+2, ROOT.kOrange+1, ROOT.kOrange+3
]

def f_Obsolete(f):

    @wraps(f)
    def f_wrapper(*args, **kws):
            print "This method is obsolete"
            return f(*args,**kws)

    return f_wrapper

def f_Dumpfname(func):
    """ decorator to show function name and caller name """

    @wraps(func)
    def echo_func(*func_args, **func_kwargs):
        print('func \033[1;31m {}()\033[0m called by \033[1;31m{}() \033[0m'\
                        .format(func.__name__,sys._getframe(1).f_code.co_name))
        return func(*func_args, **func_kwargs)

    return echo_func

def latex_float(f, u=None):

    if f!=0 and abs(f)<0.1: float_str = "{0:.2e}".format(f)
    else:          float_str = "{0:.4g}".format(f)

    if "e" in float_str:

        base, exponent = float_str.split("e")

        if u is not None:

            u=u/10**int(exponent)
            uncer_str = "{0:.3g}".format(u)
            return r"${0}$ & $\pm {1} \times 10^{{{2}}}$"\
                        .format(base, uncer_str, int(exponent))

        return r"${0} \times 10^{{{1}}}$&"\
                        .format(base, int(exponent))

    elif u:
        return r"${0}$ & $\pm {1:.3g}$".format(float_str, u)

    else:
        return float_str



def normalize_hist_by_width( hist , norm = 1. ):
    ## or h.Scale(1., "width")

    if not isinstance( hist, ROOT.TH1 ):
        raise TypeError

    hist.Scale( norm, "width")
    for i in range(1,hist.GetNbinsX()+1):
        y  = hist.GetBinContent(i)
        ye = hist.GetBinError(i)
        wd = hist.GetBinWidth(i)
        hist.SetBinContent(i, y /wd)
        hist.SetBinError  (i, ye/wd)
    return

    #--------------------------------

class Sample :
    """ Store information about one sample """

    def __init__ ( self, name, **kwargs ) :

        self.name = name
        self.path = kwargs.get('path', '')
        self.hist = None
        self.count = None
        self.loop_hists = []

        # list of open files. Only used if extracting histograms
        self.ofiles = []

        # chain is the TChain for this sample.
        # Will be created/overwritten if Addfiles is callled.
        # Should not be filled for a sample group
        self.chain = kwargs.get('chain', None)

        # contain RDataFrame
        self.rd    = None

        # link to the hosting sample manager
        self.manager = kwargs.get('manager', None)

        # isActive determines if the sample will be drawn, default=True
        self.init_isActive = kwargs.get('isActive', True)
        self.isActive      = self.init_isActive
        self.isActiveReq   = self.init_isActive

        # if isData is true the sample will be drawn as points with an error
        # bar, default=False
        self.isData   = kwargs.get('isData', False)
        # if isSignal is true the sample will be drawn as a line and not
        # stacked, default=False
        self.isSignal = kwargs.get('isSignal', False)
        self.lineStyle = kwargs.get('sigLineStyle', 7 )
        self.lineWidth = kwargs.get('sigLineWidth', 2 )

        # if the sample is to be used as a ratio
        self.isRatio = kwargs.get('isRatio', False)

        # if true for any of the samples that are drawn
        # a shaded error band is drawn on the top of the stack
        # using errors from all samples
        self.displayErrBand = kwargs.get('displayErrBand', False)

        # color determines the histogram or line color, default=black
        self.color = kwargs.get('color', ROOT.kBlack)

        # Provide a legend name.  by default the legend name will be
        # the sample name
        self.legendName = kwargs.get('legendName', name)
        if self.legendName is None :
            self.legendName = name

        # if drawRatio is true, the ratio between this and the stack will be
        # drawn in the ratio box, default=False
        self.drawRatio = kwargs.get('drawRatio', False)

        self.weightmap = kwargs.get('weightmap', None)
        #print "weightmap", self.name, self.weightmap
        if self.weightmap == None:
            self.weightmap = { }

        ## preference goes in the order of keyword argument, then weightmap,
        ## then default value
        wmap = lambda v_, def_: kwargs.get(v_, self.weightmap.get(v_, def_))
        self.scale         = wmap ('scale', 1.0)
        self.lumi          = wmap ('lumi', 1.0)
        self.cross_section = wmap ('cross_section', 1.0)
        self.total_events  = wmap ('n_evt', 1.0)
        self.k_factor      = wmap ('k_factor', 1.0)
        self.gen_eff       = wmap ('gen_eff', 1.0)

        self.averageSamples = kwargs.get('averageSamples', False )

        # groupedSampleNames is filled if this is a grouping of other samples.
        # if a sample is grouped, it is drawn as the sum of all entries
        # in this list.  Be careful to set isActive to False for the
        # sub samples or they will be drawn as well.  Grouped samples
        # can be further grouped default=[]
        self.groupedSampleNames = []
        self.groupedSamples     = set()
        self.AddGroupSamples( kwargs.get('groupedSampleNames', []) )

        # set a sample to temporary to delete it
        # when clear_all is called
        self.temporary = False

        self.failed_draw = False

        ## if the sample histogram is normalized by bin width
        ## if the bins are equal but not having width of unit 1
        ## then the integral is off by a constant factor that is the width
        ## ie integral of histogram is sum(bincontent[i]*binwidth[i])
        self.widthnormalize = False

        self.list_of_branches = []

        self.weightHist = None


    #--------------------------------

    def __repr__ (self) :
        #<SampleManager.Sample instance at 0x>
        return "<Sample %s at %x>" %(self.name,id(self))


    #--------------------------------

    def SetHist( self, hist=None ) :
        if hist is not None :
            self.hist = hist
        self.InitHist()

    #--------------------------------

    def quietprint(self, msg = " "):
            if self.manager and self.manager.quiet:
                    return
            print msg

    #--------------------------------

    def getrdataframe(self):
        return self.rd

    #--------------------------------

    def scale_calc(self, onthefly=True):
        if self.cross_section <=0 or self.lumi <=0:
            print "no valid luminosity or cross section - not scaling"
            return 1
        if onthefly:
            return analysis_utils.scale_calc(self.cross_section, self.lumi,
                    self.total_events_onthefly, self.gen_eff, self.k_factor)
        else:
            return analysis_utils.scale_calc(self.cross_section, self.lumi,
                    self.total_events         , self.gen_eff, self.k_factor)


    #--------------------------------

    def nevt_calc(self):
        """ calculate expected number of events for MC normalization """
        if self.isData:
            print "Nevents invalid for Data sample"
            return -1
        if self.IsGroupedSample():
            return sum([ samp.nevt_calc() for samp in self.groupedSamples ])
        return analysis_utils.nevents_calc(self.cross_section, self.lumi,
                        self.gen_eff, self.k_factor)


    #--------------------------------

    def InitHist(self, onthefly = True, bywidth = False) :

        self.hist.SetLineColor( self.color )
        self.hist.SetMarkerColor( self.color )
        self.hist.SetTitle('')

        ## get correct rescaling factor
        if onthefly and not (self.isData or self.IsGroupedSample() or \
                self.name == _STACKNAME or self.isRatio==True):
            #scale = self.cross_section*self.lumi/self.total_events_onthefly
            scale = self.scale_calc()
        else: scale = self.scale

        if bywidth:
            self.normalize_by_width( scale )
        else:
            self.hist.Scale( scale )


        nevt_otf = getattr(self,"total_events_onthefly",-1)
        self.quietprint( \
            'XS: %f  sample lumi: %f sample total events otf: %g logged: %g' \
            %( self.cross_section, self.lumi, nevt_otf, self.total_events))
        self.quietprint( 'Scale %s by %f logged value: %f' \
                                         %( self.name, scale, self.scale ))
        if self.isData :
            self.quietprint(self.name+" is DATA!!")
            self.hist.SetMarkerStyle( 20 )
            self.hist.SetMarkerSize( 1.15 )
            self.hist.SetStats(0)
        if self.isSignal :
            self.hist.SetLineWidth(self.lineWidth)
        if self.isRatio :
            self.hist.SetMarkerStyle( 10 )
            self.hist.SetMarkerSize( 1.1 )
            #self.hist.SetNdivisions(509, True )



    #--------------------------------

    def AddFiles( self, files, treeName=None, readHists=False , weightHistName=None, dataFrame=True) :
        """ Add one or more files and grab the tree named treeName """

        if not isinstance(files, list) :
            files = [files]

        if treeName is not None :
            self.chain = ROOT.TChain(treeName, self.name)
            for f in files :
                ## add weighted number of events histogram if not data
                if not self.isData and weightHistName:
                    rf = ROOT.TFile(f)
                    wh = rf.Get(weightHistName)
                    if not wh:
                        print "weight histogram does not exist for %s" %f
                        continue
                    wh.SetDirectory(0)
                    if self.weightHist == None:
                        self.weightHist = wh
                    else:
                        self.weightHist.Add(wh)
                    rf.Close()
                self.chain.Add(f)


        if self.weightHist:
            ## using python slicing syntax on TH1
            totevt = self.weightHist[2] - self.weightHist[1]
            self.total_events_onthefly = totevt
            if totevt!=self.total_events:
                print "total event from histogram: %.8g total event in"\
                      "imported XS file: %.8g ratio: %g"  \
                       %(totevt, self.total_events, totevt/self.total_events)
                ## Yihui -- not correct number
                #if('ChargedResonance' in str(files[0]) and totevt!= 50000):
                #     print('-----------',files[0])

        if readHists:
            for f in files :
                self.ofiles.append( f )

        # make RDataFrame
        if dataFrame:
            self.rd = ROOT.RDataFrame(self.chain)
        else:
            self.chain.SetBranchStatus('*', 0 ) #FIXME move to Draw function


    #--------------------------------

    def AddGroupSamples( self, samplenames ) :
        """ Add subsamples to this sample by samplenames"""

        if not isinstance( samplenames, list) :
            samplenames = [samplenames]

        self.groupedSampleNames += samplenames
        foundsamples = [self.manager.get_samples(name=n) for n in samplenames]
        # select only found samples
        self.groupedSamples .update( [s[0] for s in foundsamples if s] )


    #--------------------------------

    def IsGroupedSample(self) :
        return ( len( self.groupedSampleNames ) > 0 )

    #--------------------------------

    def enable_parsed_branches( self, brstr ) :
        """ Set Branch status to 1 """
        if self.chain is not None and self.chain.GetEntries():
            for br in self.chain.GetListOfBranches() :
                if brstr.count( br.GetName() ) > 0 and\
                    self.chain.GetBranchStatus( br.GetName() ) == 0 :
                    self.chain.SetBranchStatus( br.GetName(), 1)


    #--------------------------------

    def get_list_of_branches(self) :
        if self.list_of_branches :
            return self.list_of_branches
        else :
            branches = []
            if self.chain is not None and self.chain.GetEntries():
                for br in self.chain.GetListOfBranches() :
                    branches.append(br.GetName())

            self.list_of_branches = branches

            return branches


    #--------------------------------

    def reset_status( self ) :
        """ Reset sample to the initial status """
        self.isActive = self.isActiveReq


    #--------------------------------

    def getLineStyle( self ) :
        return self.lineStyle


    #--------------------------------

    def walk_text(self, index=0):
        if not self.ofiles: return []
        return list( analysis_utils.walk_root_text\
                         ( ROOT.TFile( self.ofiles[index] ) ) )


    #--------------------------------

    @f_Dumpfname
    def normalize_by_width( self , norm = 1.):
        if self.widthnormalize:
            ## throw error the check bit is flipped already
            raise RuntimeError("histogram is already normalized by width")
        if self.IsGroupedSample():
            print "warning: grouped samples inherit width-normalization"
            #raise RuntimeError("grouped samples inherit width-normalization")
        normalize_hist_by_width( self.hist , norm )
        self.widthnormalize = True

    #--------------------------------


    def acceptance( self, irange = None, option = "" ):
        """ calculate acceptance from integral """

        return self.integral( irange, option, norm = self.nevt_calc() )


    #--------------------------------


    def integral( self, irange = None, option = "", norm = None):
        """ calculate integral. option='width' for bin width normalization"""

        if not self.hist:
            raise TypeError("No histogram is found")
        err = array('d',[0])

        ## set bin to first and last one if whole range is needed
        ## range is given in bin number and inclusive
        ## h.Integral( n, n ) is same as h.GetBinContent( n )
        if irange == None:
            minibin, maxibin = 1, self.hist.GetNbinsX()
        else:
            minibin = self.hist.FindBin(irange[0])
            maxibin = self.hist.FindBin(irange[1])

        ## calculate integral and error
        intg = self.hist.IntegralAndError( minibin, maxibin, err, option )
        error = err[0]

        if norm: return intg/norm, error/norm
        return intg, error



class SampleFrame(object):
    """ Manage RDataFrame pointers """

    def __init__(self, sampleptr=None, samplemanager=None, dataFrame=True):
        self.sampleptr = {}
        self.dataset = set() # set of data samples
        self.state = ""
        self.dataFrame = dataFrame
        self.sm = samplemanager

    #--------------------------------

    def SetFilter(self,*filterexp):
        return self.SetHelper(filterexp,lambda sp,exp: sp.Filter(*exp))

    #--------------------------------

    def SetDefine(self,*defineexp):
        return self.SetHelper(defineexp,lambda sp,exp: sp.Define(*exp))

    #--------------------------------

    def SetHisto1DFast(self, var, selection, histpars, weight = None,
                        hist_conf={}, legend_conf={}, label_conf={}, save_as = None, data_exp = False):
        """ data_exp: skip data when True
                      different var, selection with dict (not implemented yet)
                      defaults to false
        """

        print 'Booking 1D hist  ' + var+ "[%i,%g,%g] : "%histpars + tRed %selection + " *%s %s" %(weight, "skipdata" if data_exp else "")
        sf = self
        if selection and isinstance(selection, str):
            sf = self.SetFilter(selection)
            ## FIXME: case without weights, data requiring different selection
        if data_exp:
            sf = sf.SkipData().SetDefine("var", var).SetDefine("weight",weight)
            #sf = sf.SetDefine("var", var, skipdata=True).SetDefine("weight",weight)
            sf = sf.SetHisto1D("var",histpars, weight="weight")
        else:
            sf = sf.SetDefine("var", var).SetDefine("weight",weight)
            sf = sf.SetHisto1D("var",histpars, weight="weight")

        # copy configurations
        sf.hist_conf = hist_conf.copy()
        sf.legend_conf = legend_conf.copy()
        sf.label_conf = label_conf.copy()
        sf.save_as = save_as
        sf.state = "histo1dfast"
        return sf

    #--------------------------------

    def SkipData(self):
        #sf = SampleFrame(samplemanager = self.sm)
        #sf.state = self.state
        #sf.sampleptr = {s: df.Define("nodata","1") for s, df in self.sampleptr.iteritems() if not s.isData}
        #for s,df in self.sampleptr.viewitems():
        #    print s, df
            #if not s.isData:
        #        sf.sampleptr[s] = df.Define("nodata","1")
            #else:
            #    print "skipped ", s
        sf = SampleFrame(samplemanager = self.sm)
        for s, sp in  self.sampleptr.iteritems():
            if not s.isData:
                try:
                    sf.sampleptr[s] = sp.Define("nodata","1")
                except TypeError:
                    print "error with sample ", s
            else:
                sf.dataset.add(sp.Define("nodata","1"))
        return sf

    #--------------------------------

    def SetHisto1D(self, var, histpars, weight = None):
        # make histogram model
        histo1dexp = (("dfh1d","dfh1d")+histpars, var)
        if weight: histo1dexp = (("dfh1d","dfh1d",) + histpars, var, weight)

        sf = self.SetHelper(histo1dexp,lambda sp,exp: sp.Histo1D(*exp), state = "histo1d")
        sf.histpars = histpars
        return sf

    #--------------------------------

    def SetCount(self,weight=None):
        if weight:
            sqweight = "%s*%s" %(weight,weight)
            return self.SetHelper(" "      ,lambda sp,exp: (sp.Sum(weight),sp.Define("sqw",sqweight).Sum("sqw")), state = "count")
        else:
            return self.SetHelper(" "      ,lambda sp,exp: sp.Count(), state = "count")

    #--------------------------------

    def GetValue(self):
        return self.SetHelper(" "  ,lambda sp,exp: sp.GetValue(), state=self.state + "value")

    #--------------------------------

    def SetHelper(self,filterexp,function,state=""):
        ## sentinel checks
        if not self.dataFrame:
            print "DataFrame not available"
            return self
        if filterexp==None:
            print "noactions: empty string"
            return None
        if isinstance(filterexp,str):
            filterexp = (filterexp,) #move it into a tuple if a string is given

        ## make new sampleframe
        sf = SampleFrame(samplemanager = self.sm)
        sf.state = state
        sf.dataset = self.dataset.copy()
        for s, sp in  self.sampleptr.iteritems():
            try:
                sf.sampleptr[s] = function(sp, filterexp)
            except TypeError:
                print "error with sample ", s
        return sf

    #--------------------------------

    def DrawSave(self):

        if "histo" in self.state and "fast" in  self.state:
                self.sm.Draw(self,"",self.histpars, self.hist_conf, self.legend_conf, self.label_conf)
                if self.save_as:
                    self.sm.SaveStack(*self.save_as)
        else:
            print "Not a FastHisto"
    #--------------------------------

    def Draw(self, *arg, **kwarg):
        """
        Two forms are possible (second for compatibility, only configs have an effect):
            Draw(hist_config={}, legend_config={}, label_config={})
            Draw(varexp, selection, histpars, hist_config={}, legend_config={}, label_config={}) """

        if "histo" in self.state:
            if len(arg)>1 and isinstance(arg[0],str):
                self.sm.Draw(self,"",self.histpars, *arg[3:], **kwarg)
            else:
                self.sm.Draw(self,"",self.histpars, *arg, **kwarg)
        else:
            print "Not a Histo"

    #--------------------------------

    def ShowCount(self, *arg):
        if self.state == "count":
            return self.sm.ShowCount(self,*arg)
        else:
            print "Not a Counter"



class SampleManager(SampleFrame) :

    """ Manage input samples and drawn histograms, inherits SampleFrame """

    def __init__(self, base_path, treeName=None, mcweight=1.0,
            treeNameModel='events', filename='ntuple.root',
            base_path_model=None, xsFile=None, lumi=1, readHists=False,
            dataFrame=True, quiet=False, weightHistName = "weighthist") :

        #
        # This plotting module assumes that root files are
        # organized under sample directories.  The directories
        # that are read are configured through the module passed
        # to ReadSamples
        #
        # All drawn objects are kept in SampleManager in variables
        # starting with curr_
        #

        # inheriting attribute and methods from SampleFrame
        super(SampleManager,self).__init__(samplemanager=self, dataFrame=dataFrame)
        self.state = "samplemanager"

        # size of standard canvas
        self.XSIZE=800
        self.YSIZE=750

        #
        # path to directory containing samples
        # the samples that are read are configured through
        # the input module
        #
        self.base_path       = base_path

        # the name of the tree to read
        self.treeName        = treeName

        # the name of weighed event count histogram; Don't import and override
        # hard coded totevt if none
        self.weightHistName  = weightHistName

        # Name of the file.  This can be overwritten in the configuration module
        self.fileName        = filename

        #the name of the tree to read for models
        self.treeNameModel   = treeNameModel

        # dummy sample
        self.dummysample = Sample("")

        #
        # path to directory containing samples for models
        # the samples that are read are configured through
        # the input module
        #
        self.base_path_model = base_path_model


        # weight that is applied to all
        # samples not labeled as Data
        self.mcweight        = mcweight

        # store all samples
        self.samples               = []

        # store model samples
        self.modelSamples          = []

        # store log messages
        self.logmessage            = []

        # store the order that the samples were added
        # in the configuration module.  The samples
        # are stacked in this order
        self.stack_order                 = []
        self.stack_order_original_active = []

        # if the cross section file is given, open it
        # and grab the cross section map out of it
        # weightMap[name]["scale","cross_section","n_evt"]
        # scale = lumi*corss_section/n_evt
        self.weightMap, self.weightprinter = \
             analysis_utils.read_xsfile( xsFile, lumi, print_values=not quiet )

        if quiet: self.logmessage.extend(self.weightprinter.GetMessage())

        self.lumi = lumi

        self.curr_hists            = {}
        self.curr_canvases         = {}
        self.curr_stack            = None
        self.curr_legend           = None
        self.curr_sig_legend       = None
        self.curr_sampleframe      = None

        self.legendLimits          = None

        self.legendLoc             = 'Nominal'
        self.legendCompress        = 1.0
        self.legendWiden           = 1.0
        self.legendTranslateX      = 0.0
        self.legendTranslateY      = 0.0
        self.entryWidth            = 0.07
        # Save any plot decorations such as labels here
        # This guarantees that the objects stay in memory
        self.curr_decorations      = []

        # When variable binning is used the binning is stored
        # so that it can be used in future calls
        self.binning = None

        # read histograms instead of trees
        self.readHists = readHists


        self.quiet = quiet

        self.transient_data = {}

        self.samples_conf=None

        self.draw_commands=[]

        self.collect_commands=False

        # make a unique ID
        # this is used to indicate
        # to which SampleManger
        # a DrawConfig was associated to
        self.id = str(uuid.uuid4()) # important to change - to _ -- Yihui

        # keep track if a sample group has been added
        self.added_sample_group=False

        self._STACKNAME = '__AllStack__'


        if dataFrame:
            try:
                ROOT.ROOT.EnableImplicitMT()
                ROOT.RDataFrame
            except Exception as ex:
                 print('Using TChain.'+\
                 'Please consider switching to ROOT >= 6.18 to use RDataFrame')
                 dataFrame = False

        # store dataframe bit
        self.dataFrame = dataFrame

    #--------------------------------

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.samples[index]
        if isinstance(index, str):
            return self.get_samples(name = index)[0]

    #--------------------------------
    def quietprint(self,*msg):
        """ samplemanager.quietprint(*msg)
            if samplemanager.quiet is set to True
            message is not printed, but saved to samplemanager.logmessage
            else it is printed
        """

        if self.quiet:
                self.logmessage.extend(msg)
                return
        for m in msg: print m
        return

    #--------------------------------
    def printcrosssection(self):
        self.weightprinter.Print()

    #--------------------------------
    def create_sample( self, name, **kwargs ) :

        if name in self.get_sample_names() :
            print 'Sample with name %s already exists' %name
            return None

        new_sample = Sample( name=name , manager = self)
        new_sample.hist = kwargs.pop('hist', None)
        for arg, val in kwargs.iteritems() :
            if hasattr( new_sample, arg ) :
                setattr( new_sample, arg, val )

        if new_sample.hist is not None :
            new_sample.SetHist( )

        self.samples.append(new_sample)
        return new_sample

    #--------------------------------
    def clone_sample( self, oldname, newname, **kwargs ) :

        if isinstance( oldname, Sample ) :
            oldsample = oldname
        else :
            _oldsample = self.get_samples( name=oldname )

            if _oldsample :
                oldsample = _oldsample[0]
            else :
                print 'Could not locate old sample'
                print 'new name = ', newname
                print 'old name = ', oldname
                return None

        newsample = copy.copy( oldsample )
        newsample.name = newname

        histval = kwargs.pop('hist', None)
        for arg, val in kwargs.iteritems() :
            if hasattr( newsample, arg ) :
                setattr( newsample, arg, val )

        if histval is not None :
            newsample.SetHist( histval )
        else :
            newsample.hist=None

        self.samples.append(newsample)

        return newsample

    #--------------------------------
    def create_ratio_sample( self, name, num_sample, den_sample,
                                   color = ROOT.kBlack, reverseratio = False, 
                                   binomunc = False, dodiff = False) :

        if name in self.get_sample_names() :
            print 'Sample %s already exists!  Will not create!' %name
            return None

        if not isinstance( num_sample, Sample ) :
            num_sample_list = self.get_samples( name=num_sample )
            if not num_sample_list :
                print 'create_ratio_sample - ERROR : '\
                      'Numerator sample does not exist, %s' %num_sample
                return None
            num_sample = num_sample_list[0]

        if not isinstance( den_sample, Sample ) :
            den_sample_list = self.get_samples( name=den_sample )
            if not den_sample_list :
                print 'create_ratio_sample - ERROR : '\
                      'Denominator sample does not exist'
                return None
            den_sample = den_sample_list[0]

        if reverseratio:
            tmp_sample = den_sample
            den_sample = num_sample
            num_sample = tmp_sample

        ratio_hist = num_sample.hist.Clone( name )
        divoptn = ""
        if binomunc:
                divoptn += "b"
        if dodiff:
            ratio_hist.Add( num_sample.hist, den_sample.hist, 1, -1 )
        else:
            ratio_hist.Divide( num_sample.hist, den_sample.hist, 1, 1, divoptn )


        ratio_hist.SetMarkerStyle(47)
        ratio_hist.SetMarkerSize(1.1)
        # better axis division display
        #ratio_hist.SetNdivisions(509 )
        ratio_hist.SetStats(0)
        ratio_hist.SetTitle('')

        return self.create_sample( name=name, isRatio=True, hist=ratio_hist,
                                   temporary=True, color=color )

    #--------------------------------
    def Merge(self, samplemanager, suffix= ""):
        """ Merge SampleManagers
            suffix: add suffix to sample names of the merged SampleManager
            destructive to merged SampleManager
        """
        ## add suffix to merged sample names to avoid clash with the original
        for samp in samplemanager.samples:

            samp.name += suffix
            for i, n in enumerate(samp.groupedSampleNames):
                samp.groupedSampleNames[i] = n + suffix

            samp.manager = self

            self.stack_order.append(samp.name)
            if samp.isActive:
                self.stack_order_original_active.append(samp.name)

        self.samples+= samplemanager.samples

    #--------------------------------
    def config_legend(self, **kwargs ) :

        config = {}

        config['legendLoc']        = kwargs.pop('legendLoc'        , 'Nominal')
        config['legendCompress']   = kwargs.pop('legendCompress'   , 1.0)
        config['legendWiden']      = kwargs.pop('legendWiden'      , 1.0)
        config['legendTranslateX'] = kwargs.pop('legendTranslateX' , 0.0)
        config['legendTranslateY'] = kwargs.pop('legendTranslateY' , 0.0)
        config['entryWidth']       = kwargs.pop('entryWidth' , 0.08)

        for key, val in kwargs.iteritems() :
            config[key] = val
        return config

    #--------------------------------
    def apply_lenged_conf(self, config ) :

        if config is None :
            return

        for key, val in config.iteritems() :
            if hasattr( self, key ) :
                setattr(self, key, val)

    #--------------------------------
    def get_samples(self, **kwargs) :

        # if no arguments provided, return all samples
        if not kwargs :
            return self.samples[:]

        # collect results for each argument provided
        # then require and AND of samples matching each
        # criteria
        each_results = []
        for arg, val in kwargs.iteritems() :
            val_list = val
            if not isinstance(val_list, list) :
                val_list = [val_list]
            if val_list is None or None in val_list:
                #clone list if None is included
                each_results.append(list(self.samples))
                continue
            if hasattr( self.dummysample , arg ) :
                each_results.append([ samp for samp in self.samples \
                                      if getattr( samp, arg ) in val_list\
                          or (isinstance(val, str) and fnmatch.fnmatch(getattr(samp, arg), val_list[0])) ])

        fx = lambda x,y : set(x) & set(y)
        common_results = list( reduce( fx , each_results ) )
        if not common_results :
            self.quietprint('WARNING : Found zero samples matching criteria!'\
                            ' Sample matching criteria were : ', kwargs)
            return []

        return common_results
        ## default, return all samples
        #if names is None :
        #    return self.samples

        ## empty list provided, return empty list
        #if not names :
        #    return []

        #if not isinstance(names, list) :
        #    names = [names]

        #return filter( lambda x : x.name in names, self.samples )

    #--------------------------------
    def get_model_samples(self, names=[]) :
        if not isinstance(names, list) :
            names = [names]

        if names :
            return filter( lambda x : x.name in names, self.modelSamples )
        else :
           return self.modelSamples

    #--------------------------------
    def get_signal_samples(self) :
        return filter( lambda x : x.isSignal and x.isActive , self.samples )

    #--------------------------------
    def get_sample_names(self) :
        return [x.name for x in self.samples]

    #--------------------------------
    def get_model_sample_names(self) :
        return [x.name for x in self.modelSamples]


    #--------------------------------
    def add_decoration(self, obj) :
        self.curr_decorations.append(obj)

    #--------------------------------
    def activate_sample(self, samp_name) :
        if isinstance(samp_name, list):
                for s in samp_name:
                        self.activate_sample(s)
                return

        name = samp_name
        if not isinstance( samp_name, str ) :
            name = samp_name.name

        sel_samps = self.get_samples(name=name)
        if not sel_samps :
            print 'No sample with name %s' %name
        elif len(sel_samps) > 1 :
            print 'Located multiple samples with name %s' %name
        else :
            print 'Activate sample %s' %sel_samps[0].name
            sel_samps[0].isActiveReq=True
            sel_samps[0].isActive=True

    #--------------------------------
    def deactivate_sample(self, samp_name) :
        sel_samps = self.get_samples(name=samp_name)
        if not sel_samps :
            print 'No sample with name %s' %samp_name
        elif len(sel_samps) > 1 :
            print 'Located multiple samples with name %s' %samp_name
        else :
            print 'Deactivate sample %s' %sel_samps[0].name
            sel_samps[0].isActiveReq=False
            sel_samps[0].isActive=False

    #--------------------------------
    def deactivate_all_samples(self) :
        sel_samps = self.get_samples()
        for samp in sel_samps :
            samp.isActive=False
            samp.isActiveReq=False

    #--------------------------------
    def clear_all(self) :
        """ clear all objects """

        self.clear_hists()

        for can in self.curr_canvases.values() :
            if can != None :
                can.Close()
        self.curr_canvases         = {}

        #if self.curr_stack != None :
        ##    self.curr_stack.Delete()
        #    self.curr_stack.Clear()
        #    self.curr_stack.Delete()
        if self.curr_legend != None :
            #self.curr_legend.Delete()
            self.curr_legend = None

        self.curr_decorations      = []

        self.legendLoc='Nominal'
        self.legendCompress=1.0
        self.legendWiden=1.0
        self.legendTranslateX=0.0
        self.legendTranslateY=0.0
        self.entryWidth = 0.048
        self.siglegPos = 'bottom'

        self.transient_data= {}
        self.stored_command=''

        for samp in self.samples :
            samp.reset_status()


    #--------------------------------
    def clear_hists(self) :
        rm_samples = []
        for idx, samp in enumerate(self.samples) :
            samp.hist=None

            ## reset bit indicating sample histogram is normalized by width
            samp.widthnormalize = False

            if samp.temporary :
                self.quietprint( 'removing sample %s' %samp.name)
                rm_samples.append(samp)

        ## fully remove sample if sample is tagged temporary
        for samp in rm_samples:
            if samp.hist is not None :
                samp.hist.Delete()
            self.samples.remove(samp)

        for samp in self.modelSamples :
            samp.hist=None

    #--------------------------------
    def clear_samples(self) :
        for samp in self.samples :
            if samp.chain is not None :
                for fileobj in samp.chain.GetListOfFiles() :
                    file = ROOT.TFile(fileobj.GetTitle())
                    file.Close()

        self.samples = []

    #--------------------------------
    def get_grouped_sample_names(self) :
        names = []
        for samp in self.samples :
            if samp.IsGroupedSample() :
                names.append(samp.name)

        return names


    #--------------------------------

    def get_sample_branch_minmax( self, samp, branch ) :

        print 'Get %s, %s' %( samp, branch)

        if isinstance( samp, str ) :
            samp = self.get_samples(name=samp)[0]

        if samp.groupedSampleNames :
            min_val_tot = None
            max_val_tot = None
            for subsampname in samp.groupedSampleNames :
                min_val, max_val = self.get_sample_branch_minmax(subsampname, branch )
                if min_val_tot is None or min_val_tot < min_val :
                    min_val_tot = min_val
                if max_val_tot is None or max_val_tot > max_val :
                    max_val_tot = max_val
            return (min_val_tot, max_val_tot )

        else :

            samp.chain.SetBranchStatus(branch, 1)
            max_val = samp.chain.GetMaximum(branch)
            min_val = samp.chain.GetMinimum(branch)

            return (min_val, max_val)

    #--------------------------------
    def add_temp_sample(self, samp) :
        samp.temporary = True
        self.samples.append(samp)

    #--------------------------------
    def get_stack_order( self ) :

        out_order = []

        samps = self.get_samples( name=self.stack_order )

        for samp in samps :
            if not samp.isData and not samp.isSignal and samp.isActive :
                out_order.append( samp.name )

        return out_order

    #---------------------------------------
    def change_stack_order(self,iorder,forder):
            if isinstance(iorder,int) and isinstance(forder,int):
                self.samples.insert(forder,self.samples.pop(iorder)) # index of the original
                return
            ordr = [iorder,forder]
            for i in (0,1):
                if isinstance(ordr[i],str):
                    samp = self.get_samples(name = ordr[i])
                    if samp:
                        ordr[i] = self.samples.index(samp[0])
                    else:
                            print "WARNING: cannot find sample with name %s" %(ordr[i])
                            return
            self.change_stack_order(*ordr)
            return

    #---------------------------------------
    def GetLowestGroupedSamples( self, sample ) :
        lowest = []
        for subsamp in self.get_samples(name=sample.groupedSampleNames ) :
            if subsamp.IsGroupedSample() :
                lowest += self.GetLowestGroupedSamples( subsamp )
            else :
                lowest.append(subsamp)
        return lowest


    #---------------------------------------
    def start_command_collection( self ) :
        self.collect_commands = True
        for sample in self.samples :
            sample.loop_hists=[]


    #---------------------------------------
    def add_draw_config( self, varexp, selection, histpars, hist_config={}, label_config={}, legend_config={}, replace_selection_for_sample={}  ) :
        self.draw_commands.append( DrawConfig( varexp, selection, histpars, hist_config=hist_config, label_config=label_config, legend_config=legend_config, replace_selection_for_sample=replace_selection_for_sample ) )

        self.draw_commands[-1].samp_man_id = self.id

        return self.draw_commands[-1]

    #---------------------------------------
    def add_compare_config( self, varexp, selection, samples, histpars, hist_config={}, label_config={}, legend_config={}, replace_selection_for_sample={}  ) :
        self.draw_commands.append( DrawConfig( varexp, selection, histpars, samples=samples, hist_config=hist_config, label_config=label_config, legend_config=legend_config, replace_selection_for_sample=replace_selection_for_sample ) )

        self.draw_commands[-1].compare_hists=True

        self.draw_commands[-1].samp_man_id = self.id

        return self.draw_commands[-1]

    #---------------------------------------
    def config_and_queue_hist( self, samp, var, sel, binning ) :

        self.activate_sample( samp )
        draw_conf = DrawConfig( var, sel, binning, samples=samp )
        self.queue_draw( draw_conf)
        return draw_conf

    #---------------------------------------
    def queue_draw( self, draw_config ) :
        self.draw_commands.append( draw_config )

        self.draw_commands[-1].samp_man_id = self.id

        self.draw_commands[-1].no_auto_draw=True

    #---------------------------------------
    def add_save_stack( self, filename, outputDir, canname=None) :
        if canname is None :
            canname = 'base'
        self.draw_commands[-1].save_stack( filename, outputDir, canname )

    #---------------------------------------
    def add_dump_stack( self, filename, outputDir) :
        self.draw_commands[-1].dump_stack( filename, outputDir )

    #---------------------------------------
    def run_commands( self, nsplit=0, nFilesPerJob=5, treeName='' ) :

        self.collect_commands = False

        #------------------------------------------------------------
        # 1) Write the code that loads braches, loops, and fills hists
        # 2) compile and run the code
        # 3) Loop over the draw configs and make and save canvases
        #------------------------------------------------------------

        workarea = os.getenv('WorkArea')
        user = getpass.getuser()

        #compile_base = '%s/../Plotting/compiled_code' %workarea
        compile_base = '/tmp/%s/compiled_code/%s' %(user,self.id)
        os.makedirs( '%s/include' %compile_base)
        os.makedirs( '%s/src' %compile_base)
        os.makedirs( '%s/obj' %compile_base)
        os.system( 'cp %s/../Plotting/compiled_code/Makefile %s '%( workarea, compile_base ))

        brdef_file_name = '%s/include/BranchDefs.h'  %( compile_base )
        header_file_name = '%s/include/BranchInit.h' %( compile_base )
        source_file_name = '%s/src/BranchInit.cxx'   %( compile_base )
        linkdef_file_name = '%s/include/LinkDef.h'   %( compile_base )

        runsrc_file_name = '%s/src/RunAnalysis.cxx' %compile_base
        runinc_file_name = '%s/include/RunAnalysis.h' %compile_base

        # collect a complete list of branches used in all draw commands
        # normally this'll be fine, but its possible to
        # run into the situation where some trees may not have certain
        # branches and it'll break
        all_sample_branches = set()
        all_sample_chains = []
        for sample in self.samples :
            if sample.chain is not None :
                all_sample_chains.append( sample.chain )

        all_sample_branches = core.get_branch_mapping_from_trees( all_sample_chains )

        draw_branches = []
        draw_names = []
        for draw_config in self.draw_commands:
            draw_strs = ''
            for var in draw_config.var :
                draw_strs += var
            for sel in draw_config.selection :
                draw_strs += sel
            for br in all_sample_branches :
                if draw_strs.count(br['name']) :
                    if br['name'] not in draw_names :
                        draw_branches.append( br )
                        draw_names.append( br['name'] )

        n_tot = 0
        for draw_command in self.draw_commands :
            draw_command.create_hist_configs( draw_branches )
            n_tot += len(draw_command.hist_configs)

        print 'Will create %d histograms!' %n_tot

        if n_tot == 0 :
            print 'No histograms were scheduled.  Aborting!'
            return

        output_loc = '/tmp/%s/drawn_histograms/%s' %(user,self.id)
        os.makedirs( output_loc )

        # create the source code file
        self.write_source_code( self.draw_commands, runsrc_file_name, draw_branches )

        # create the header code file
        self.write_header_code( self.draw_commands, runinc_file_name )

        # Write the c++ files having the branch definitions and
        # SetBranchAddress calls
        core.write_header_files(brdef_file_name, linkdef_file_name, draw_branches )

        core.write_source_file(source_file_name, header_file_name, draw_branches )

        # compile
        exename= 'RunAnalysis.exe'
        os.system( 'cd %s ; rm %s ; make EXENAME=%s; cd - '%(compile_base, exename, exename) )

        all_samples = []
        for sample in self.samples :
            if sample.isActive :
                if sample.IsGroupedSample() :
                    for subsamp in self.GetLowestGroupedSamples(sample) :
                        all_samples.append(subsamp)
                else :
                    all_samples.append(sample)

        # remove output directory
        if os.path.isdir( output_loc ) :
            os.system( 'rm -rf %s' %output_loc )

        output_file = 'hist.root'

        configs = []
        for sample in all_samples :
            config_name = '%s/configs/config_%s.txt' %(compile_base, sample.name)
            entries = sample.chain.GetEntries()
            #file_evt_map = core.get_file_evt_map( [f.GetTitle() for f in sample.chain.GetListOfFiles()], nsplit=nsplit, nFilesPerJob=nFilesPerJob, totalEvents=None, treeName='ggNtuplizer/EventTree')

            #exe_path = '%s/RunAnalysis' %compile_base

            #options = {}
            #options['nproc']             = 6
            #options['outputDir']         = '%s/%s' %(output_loc, sample.name)
            #options['confFileName']      = 'config_%s.txt' %sample.name
            #options['treeName']          = sample.chain.GetName()
            #options['outputFile']        = output_file
            #options['storagePath']       = None
            #options['sample']            = sample.name
            #options['disableOutputTree'] = True
            #options['nPrint']            = 10000

            #commands_orig = core.generate_multiprocessing_commands( file_evt_map, [], exe_path, options )

            #configs += commands_orig

            ##core.write_config([], config_name, sample.chain.GetName(), output_loc, '%s.root'%sample.name, file_evt_map, sample=sample.name, disableOutputTree=True )
            ##configs.append((entries, config_name))
            file_evt_map = core.get_file_evt_map( [f.GetTitle() for f in sample.chain.GetListOfFiles()], nsplit=nsplit, nFilesPerJob=nFilesPerJob, totalEvents=None, treeName=treeName)
            core.write_config([], config_name, sample.chain.GetName(), output_loc, '%s.root'%sample.name, file_evt_map, sample=sample.name, disableOutputTree=True )
            configs.append((entries, config_name))


        #configs.sort(reverse=True)

        run_cmds = ['%s/%s --conf_file %s' %( compile_base,exename, c[1] ) for c in configs ]
        print run_cmds

        nproc = 6
        if len(run_cmds) < nproc :
            nproc = len(run_cmds)


        p=multiprocessing.Pool(nproc)
        p.map(os.system, run_cmds)

        file_map = {}
        # ------------------------
        # For older style without multiprocessing
        #for file in os.listdir( '%s/Job_0000' %output_loc ) :
        #    file_map[file] = []

        #for top, dirs, files in os.walk( output_loc ) :
        #    for file in files :
        #        if file in file_map.keys() :
        #            file_map[file].append( top+'/'+file )

        #comb_dir = output_loc+'/COMB'
        #os.makedirs( comb_dir )
        #for base, files in file_map.iteritems() :
        #    if len(files) == 1 :
        #        cp_cmd = 'cp %s %s/' %(files[0], comb_dir )
        #        print cp_cmd
        #        os.system( cp_cmd )
        #    else :
        #        os.system( 'hadd %s/%s %s' %( comb_dir, base, ' '.join( files ) ) )
        # ------------------------
        for sample in all_samples :
            os.system( 'hadd %s/%s/%s %s/%s/Job*/%s' %( output_loc, sample.name, output_file, output_loc, sample.name, output_file ) )

        self.output_loc = output_loc

        # Now get the histograms and draw
        for draw_config in self.draw_commands:
            if draw_config.no_auto_draw :
                continue
            if draw_config.compare_hists :
                self.CompareFromHistFiles( draw_config )
            else :
                self.DrawFromHistFiles( draw_config )

    def DrawFromHistFiles(self,  draw_config ) :

        self.clear_all()

        all_samples = []
        for sample in self.get_samples(isActive=True):
            if sample.IsGroupedSample() :
                for subsamp in self.GetLowestGroupedSamples(sample) :
                    all_samples.append( subsamp)
            else :
                all_samples.append( sample )

        for sample in all_samples :
            # ------------------------
            # For older style without multiprocessing
            #filename = '%s/%s.root' %( self.output_loc, sample.name )
            # ------------------------
            filename = '%s/%s/hist.root' %( self.output_loc, sample.name )
            for name  in draw_config.hist_configs.keys() :
                self.load_hist_from_file_cache( sample, name, filename )

        # handle grouped samples
        for sample in self.samples :
            if sample.IsGroupedSample() and sample.isActive :
                self.group_sample(sample, isModel=False)

        if isinstance( draw_config.histpars, tuple) and len(draw_config.histpars) == 4 :
            if isinstance( draw_config.histpars[3], list ) :
                self.variable_rebinning(binning=draw_config.histpars[3])
            else :
                self.variable_rebinning(threshold=draw_config.histpars[3])

        self.MakeStack( draw_config )

        self.DrawCanvas(self.curr_stack, draw_config, datahists=['Data'], sighists=self.get_signal_samples())

        if draw_config.stack_dump_params :
            self.DumpStack( draw_config.stack_dump_params['dirname'], draw_config.stack_dump_params['filename'] )
        if draw_config.stack_save_params :
            self.SaveStack( draw_config.stack_save_params['filename'], draw_config.stack_save_params['dirname'], draw_config.stack_save_params['canname'] )



    #--------------------------------

    def CompareFromHistFiles(self, draw_config ) :

        self.clear_all()

        ##-------------------
        ## list of samples may have duplicates
        ## get_samples does not pay attention to
        ## duplicates, go one-by-one
        ##-------------------
        #in_samples = []
        #for rsamp in draw_config.samples :
        #    in_samples += self.get_samples(name=rsamp)

        #-----------------------
        # To handle the case when the
        # same sample is requested multiple
        # times, create a new sample for each
        # hist config
        #-----------------------
        created_samples = []
        for name, conf in draw_config.hist_configs.iteritems() :

            newsamp = self.clone_sample( oldname=conf['sample'], newname=name, temporary=True )
            print 'Create %s' %name

            if newsamp.IsGroupedSample() :
                for subsamp in self.GetLowestGroupedSamples(newsamp) :
                    # ------------------------
                    # For older style without multiprocessing
                    #filename = '%s/%s.root' %( self.output_loc, subsamp.name )
                    # ------------------------
                    filename = '%s/%s/hist.root' %( self.output_loc, subsamp.name )
                    self.load_hist_from_file_cache( subsamp, name, filename, debug=True )
                    subsamp.hist.Draw()

                self.group_sample(newsamp, isModel=False)
                newsamp.hist.Draw()

            else :
                filename = '%s/%s.root' %( self.output_loc, newsamp.name )
                self.load_hist_from_file_cache( newsamp , name, filename )

            created_samples.append(newsamp)

        if not created_samples :
            print 'No hists were created from samples %s' %(', '.join(reqsamples) )
            return created_samples

        if isinstance( draw_config.histpars, tuple) and len(draw_config.histpars) == 4 :
            if isinstance( draw_config.histpars[3], list ) :
                self.variable_rebinning(binning=draw_config.histpars[3], samples=created_samples)
            else :
                self.variable_rebinning(threshold=draw_config.histpars[3], samples=created_samples)

        if draw_config.get_doratio() :
            self.create_top_canvas_for_ratio('same')
        else :
            self.create_standard_canvas('same')

        self.curr_canvases['same'].cd()

        self.DrawSameCanvas( self.curr_canvases['same'], created_samples, draw_config )

        if draw_config.get_doratio() :
            #rname = created_samples[0].name + '_ratio'
            for samp, hc in zip(created_samples[1:], draw_config.hist_configs.values()[1:]) :

                color = hc['color']
                rcolor = color

                if len( created_samples ) == 2 :
                    rcolor = ROOT.kBlack

                rname = 'ratio%s' %samp.name
                rsamp = self.create_ratio_sample( rname, num_sample = created_samples[0], den_sample=samp, color=rcolor)

                rsamp.legend_entry = hc.get('legend_entry', None )


        # make the legend
        step = len(created_samples)
        self.curr_legend = self.create_standard_legend(step, draw_config=draw_config )

        self.create_same_legend( draw_config.get_legend_entries() , created_samples )

        self.DrawCanvas(self.curr_canvases['same'], draw_config)

        if draw_config.stack_dump_params :
            self.DumpStack( draw_config.stack_dump_params['dirname'], draw_config.stack_dump_params['filename'], doRatio=draw_config.get_doratio() )
        if draw_config.stack_save_params :
            self.SaveStack( draw_config.stack_save_params['filename'], draw_config.stack_save_params['dirname'], draw_config.stack_save_params['canname'] )


    #--------------------------------

    def load_samples( self, draw_config ) :

        if draw_config.samp_man_id is not None and draw_config.samp_man_id != self.id :
            print 'Provided DrawConfig was not made with this SampleManager.  Exiting!'
            return []

        created_samples = []

        if not draw_config.hist_configs :
            print draw_config.samples[0].name
            matched_samples = self.get_samples( name=draw_config.samples[0].name)
            print matched_samples
            if matched_samples :
                if matched_samples[0].hist is not None :
                    created_samples.append( matched_samples[0] )

        else :
            for name, conf in draw_config.hist_configs.iteritems() :


                newsamp = self.clone_sample( oldname=conf['sample'], newname=name, temporary=True )
                print 'Create %s' %name

                if newsamp.IsGroupedSample() :
                    for subsamp in self.GetLowestGroupedSamples(newsamp) :
                        # ------------------------
                        # For older style without multiprocessing
                        #filename = '%s/%s.root' %( self.output_loc, subsamp.name )
                        # ------------------------
                        filename = '%s/%s/hist.root' %( self.output_loc, subsamp.name )
                        self.load_hist_from_file_cache( subsamp, name, filename, debug=True )
                        subsamp.hist.Draw()

                    self.group_sample(newsamp, isModel=False)

                else :
                    # ------------------------
                    # For older style without multiprocessing
                    # filename = '%s/%s.root' %( self.output_loc, conf['sample'].name )
                    # ------------------------
                    filename = '%s/%s/hist.root' %( self.output_loc, conf['sample'].name )
                    self.load_hist_from_file_cache( newsamp , name, filename )

                created_samples.append(newsamp)

        if not created_samples :
            print 'No hists were created'
            return created_samples

        if isinstance( draw_config.histpars, tuple) and len(draw_config.histpars) == 4 :
            if isinstance( draw_config.histpars[3], list ) :
                self.variable_rebinning(binning=draw_config.histpars[3], samples=created_samples)
            else :
                self.variable_rebinning(threshold=draw_config.histpars[3], samples=created_samples)

        return created_samples




    #--------------------------------

    def load_hist_from_file_cache( self, sample, name, filename, debug=False ) :
        """ load histogram from file by histogram name """

        if debug :
            print 'Load hist %s from %s into sample %s' %( name, filename, sample.name )
        sample.hist = None
        if not hasattr(sample, 'file' ) :
            sample.file = ROOT.TFile.Open( filename, 'READ')
        sample.hist = sample.file.Get(name).Clone()
        sample.hist.SetDirectory(0)
        sample.hist.Sumw2()
        self.format_hist( sample )



    #--------------------------------

    def write_source_code( self, draw_commands, file, branches ) :

        text = ''

        text += r'#include "include/RunAnalysis.h"' + '\n'
        text += r'#include <iostream>' + '\n'
        text += r'#include <iomanip>' + '\n'
        text += r'#include <fstream>' + '\n'
        text += r'#include <sstream>' + '\n'
        text += r'#include <boost/foreach.hpp>' + '\n'
        text += r'#include <boost/algorithm/string.hpp>' + '\n'
        text += r'#include <sys/types.h>' + '\n'
        text += r'#include <sys/stat.h>' + '\n'
        text += r'#include <math.h>' + '\n'
        text += r'#include <stdlib.h>' + '\n'
        text += r'#include "include/BranchDefs.h"' + '\n'
        text += r'#include "include/BranchInit.h"' + '\n'
        text += r'#include "Core/Util.h"' + '\n'
        text += r'#include "TFile.h"' + '\n'
        text += r'int main(int argc, char **argv)' + '\n'
        text += r'{' + '\n'
        text += r'    CmdOptions options = ParseOptions( argc, argv );' + '\n'
        text += r'    AnaConfig ana_config = ParseConfig( options.config_file, options );' + '\n'
        text += r'    RunModule runmod;' + '\n'
        text += r'    ana_config.Run(runmod, options);' + '\n'
        text += r'    std::cout << "^_^ Finished ^_^" << std::endl;' + '\n'
        text += r'}' + '\n'
        text += r'void RunModule::initialize( TChain * chain, TTree * outtree, TFile *outfile,' + '\n'
        text += r'                            const CmdOptions & options, std::vector<ModuleConfig> &configs ) {' + '\n'
        text += r'    f = outfile; '+ '\n'
        text += r'    f->cd(); '+ '\n'
        text += r'    InitINTree(chain);' + '\n'

        for draw_config in draw_commands :
            for hist_str in draw_config.get_hist_declarations() :
               text += r' %s' %( hist_str ) + '\n\n';
               #text += r' hist_%s = new TH1F( "%s", "", %d, %f, %f );' %( draw_config.name, draw_config.name, draw_config.histpars[0], draw_config.histpars[1], draw_config.histpars[2] ) + '\n\n';
        text += r'}' + '\n'
        text += r'bool RunModule::execute( std::vector<ModuleConfig> & configs ) {' + '\n'
        for draw_config in self.draw_commands :
            for name in draw_config.get_names() :
                text += '    Draw%s(  ); \n' %name
            #text += '    Draw%s(  ); \n' %draw_config.name
        text += r'    return false;' + '\n'
        text += r'}' + '\n\n'

        text += r'void RunModule::finalize(  ) {' + '\n'
        for draw_config in self.draw_commands :
            for name in draw_config.get_names() :
                text += '    hist_%s->Write(); \n' %name
        text += r'}' + '\n\n'

        for draw_config in self.draw_commands :
            for name, config in draw_config.hist_configs.iteritems() :

                text += 'void RunModule::Draw%s( ) const { \n' %name
                first_replace = True
                for samp, rselection in draw_config.replace_selection_for_sample.iteritems() :
                    if first_replace :
                        text += '    if( curr_sample == %s ) { \n ' %samp
                        first_replace=False
                    else :
                        text += '    else if( curr_sample == %s ) { \n ' %samp

                    text += '        weight = %s; \n ' %rselection
                    text += '        if( weight != 0 ) { \n '
                    text += '        hist_%s->Fill(%s, weight); \n ' %(name, config['cppvar'])
                    text += '        } \n '
                    text += '    } \n '


                # just check if the replacement was done
                if first_replace : # no replacement
                    text += '    // Original selection : %s \n ' %config['selection']
                    text += '    float weight = %s; \n ' %config['cppselection']
                    text += '        if( weight != 0 ) { \n '
                    text += '        hist_%s->Fill(%s, weight); \n '  %(name, config['cppvar'])
                    text += '        } \n '
                else :
                    text += '    else { \n'
                    text += '        // Original selection : %s \n ' %config['selection']
                    text += '        float weight = %s; \n ' %config['cppselection']
                    text += '        if( weight != 0 ) { \n '
                    text += '        hist_%s->Fill(%s, weight); \n '  %(name, config['cppvar'])
                    text += '        } \n '
                    text += '    }\n '
                text += '}\n'


        ofile = open( file, 'w' )
        ofile.write(text)
        ofile.close()



    #--------------------------------

    def write_header_code( self, draw_commands, file ) :

        text = ''

        text += '#ifndef RUNANALYSIS_H' + '\n'
        text += '#define RUNANALYSIS_H' + '\n'
        text += '#include "../../../Analysis/TreeFilter/Core/Core/AnalysisBase.h"' + '\n'
        text += '#include <string>' + '\n'
        text += '#include <vector>' + '\n'
        text += '#include "TTree.h"' + '\n'
        text += '#include "TChain.h"' + '\n'
        text += '#include "TH1F.h"' + '\n'
        text += '#include "TH2F.h"' + '\n'
        text += '#include "TH3F.h"' + '\n'
        text += '#include "TLorentzVector.h"' + '\n'
        text += 'class RunModule : public virtual RunModuleBase {' + '\n'
        text += '    public :' + '\n'
        text += '        RunModule() {}' + '\n'
        text += '        void initialize( TChain * chain, TTree *outtree, TFile *outfile, const CmdOptions & options, std::vector<ModuleConfig> & configs) ;' + '\n'
        text += '        bool execute( std::vector<ModuleConfig> & config ) ;' + '\n'
        text += '        void finalize( ) ;' + '\n'

        for draw_config in draw_commands :
            for name in draw_config.get_names() :
                text += '        void Draw%s ( ) const;' %name + '\n'

        for draw_config in draw_commands :
            for name in draw_config.get_names() :
                text += '        %s * hist_%s; '%(draw_config.get_hist_type(), name) + '\n'

        text += '            TFile * f;\n '

        text += '};' + '\n'
        text += 'namespace OUT {' + '\n'
        text += '};' + '\n'
        text += '#endif' + '\n'

        ofile = open( file, 'w' )
        ofile.write(text)
        ofile.close()


    #---------------------------------------
    def create_queued_hists( self, sample ) :


        for draw_config in self.draw_commands :
            sample.loop_hists.append( draw_config.init_hist(sample.name) )


        nentries = sample.chain.GetEntries()

        sample.chain.SetBranchStatus('*', 1)

        for draw_config in self.draw_commands :
            draw_config.compile_selection_string(sample, treename='sample.chain')
            draw_config.compile_var_string(sample, treename='sample.chain')

        for entry in sample.chain :

            for draw_config, hist in zip(self.draw_commands, sample.loop_hists ) :

                try :
                    weight = eval(draw_config.get_compiled_selection_string() )
                except :
                    print 'Failed to evaluate draw command.  Please check command and fix'
                    print draw_config.get_eval_selection_string(sample, treename='sample.chain')
                    raise
                if weight != 0 :
                    try :
                        hist.Fill( eval(draw_config.get_compiled_var( ) ), weight )
                    except :
                        print 'Failed to eval var.  Please check and fix'
                        print draw_config.get_var_val(sample, treename='sample.chain')
                        raise

        return len(sample.loop_hists)


    #---------------------------------------
    def ListBranches(self, key=None ) :
        """ List all available branches.  If key is provided only show those that match the key """

        # grab list from 0th sample.  This may not work in some cases
        for br in self.samples[0].chain.GetListOfBranches() :
            if key is None :
                print br.GetName()
            else :
                if br.GetName().count(key) :
                    print br.GetName()

    #---------------------------------------
    def list_hists( self ) :
        all_hists = []
        for samp in self.get_samples() :
            for ofile in samp.ofiles :
                if ofile is not None :
                    for objkey in ofile.GetListOfKeys() :
                        obj = ofile.Get( objkey.GetName() )
                        class_name = obj.ClassName()
                        if class_name.count( 'TH1' ) :
                            all_hists.append(obj.GetName() )

        uniq_hists = list( set( all_hists ) )
        uniq_hists.sort()

        for h in uniq_hists :
            print h

    #---------------------------------------
    def SaveStack( self, filename, outputDir=None, canname=None, write_command=False, command_file='commands.txt'  ) :
        """ Save current plot to filename.  Must supply outputDir
            write_command to write to a command file
        """

        if outputDir is None :
            print 'No output directory provided.  Will not save.'
        else :

            # write the command to a file if requested
            if write_command :
                if not os.path.isdir( outputDir ) :
                    os.makedirs( outputDir )
                cmdfile = open( outputDir +'/' +command_file, 'a' )
                cmdfile.write( '%s : %s \n' %( filename, self.transient_data.get( 'command', 'NO COMMAND STORED') ) )
                cmdfile.close()

            if self.collect_commands :
                self.add_save_stack( filename, outputDir, canname )
                return

            print 'Creating directory %s' %outputDir
            if "~" in outputDir:
                outputDir = os.path.expanduser(outputDir)
                print "expand bash home directory: ", outputDir
            if "$" in outputDir:
                outputDir = os.path.expandvars(outputDir)
                print "expand bash variable: ", outputDir
            if not os.path.isdir( outputDir ) :
                os.makedirs(outputDir)

            filenamesplit = filename.split('.')
            if len( filenamesplit ) > 1 :
                filenamestrip = '.'.join( filenamesplit[:-1] )
            else :
                filenamestrip = filenamesplit[0]

            #histnameeps = outputDir + '/' + filenamestrip+'.eps'
            histnameeps = outputDir + '/' + filenamestrip+'.C'
            histnameroot = outputDir + '/' + filenamestrip+'.root'
            histnamepng = outputDir + '/' + filenamestrip+'.png'
            if not (filename.count( '.pdf' ) or filename.count('.png') ):
                histnamepdf = outputDir + '/' + filenamestrip+'.pdf'
            else :
                histnamepdf = outputDir + '/' +filename

            if len( self.curr_canvases ) == 0 :
                print 'No canvases to save'
            elif len( self.curr_canvases ) == 1  :
                self.curr_canvases.values()[0].SaveAs(histnamepdf)
                self.curr_canvases.values()[0].SaveAs(histnameeps)
                self.curr_canvases.values()[0].SaveAs(histnameroot)
                self.curr_canvases.values()[0].SaveAs(histnamepng)
            else :
                if canname is not None :
                    if canname not in self.curr_canvases :
                        print 'provided can name does not exist'
                    #Yihui - seems to cause the MakeSystematics.py error 
                    else :
                        self.curr_canvases[canname].SaveAs(histnamepdf)
                        self.curr_canvases[canname].SaveAs(histnameeps)
                        self.curr_canvases[canname].SaveAs(histnameroot)
                        self.curr_canvases[canname].SaveAs(histnamepng)

                else :

                    print 'Multiple canvases available.  Select which to save'
                    keys = self.curr_canvases.keys()
                    for idx, key in enumerate(keys) :
                        print '%s (%d)' %(key, idx)
                    selidx = int(raw_input('enter number 0 - %d' %( len(keys)-1 )))
                    selkey = keys[selidx]
                    self.curr_canvases[selkey].SaveAs(histnamepdf)
                    self.curr_canvases[selkey].SaveAs(histnameeps)
                    self.curr_canvases[selkey].SaveAs(histnameroot)
                    self.curr_canvases[selkey].SaveAs(histnamepng)


    #---------------------------------------
    def DumpStack( self, outputDir=None, txtname=None, doRatio=None, details=False , cut = None) :

        if self.collect_commands :
            self.add_dump_stack( txtname, outputDir )
            return

        if doRatio is None :
            if self.draw_commands :
                doRatio = self.draw_commands[-1].get_doratio()

        # store the signal and stack entries
        stack_entries  = {}
        signal_entries = {}
        ratio_entries  = {}
        detail_entries = {}

        # get samples with the MC stack, data, and signal samples
        samp_list = self.get_samples(name=self.get_stack_order()) + self.get_samples(isData=True) + self.get_samples(isSignal=True)

        # get the integrals
        for samp in samp_list :
            if samp.hist == None :
                continue
            if cut:
               try:
                 icut = float(cut)
               except ValueError:
                 print "Input cut {cut} is not a float. Please check".format(cut = cut)
               ifirst = samp.hist.FindBin( icut )
            else:
               ifirst = 1
            err = ROOT.Double()
            integral = samp.hist.IntegralAndError( ifirst,
                            samp.hist.GetNbinsX(), err )

            if samp.isSignal :
                signal_entries[samp.name] = ufloat(integral, err)
            else :
                stack_entries[samp.name] = ufloat(integral, err )

        #collect the list to be printed
        order = list(self.get_stack_order())
        if 'Data' in stack_entries :
            order.insert(0, 'Data')

        # get the sum over the full stack
        bkg_sum = ufloat(0.0, 0.0)
        for name, vals in stack_entries.iteritems() :
            if name != 'Data' :
                bkg_sum += vals

        sig_sum = ufloat(0.0, 0.0)
        for name, vals in signal_entries.iteritems() :
            sig_sum += vals

        latex_lines = []
        latex_lines.append( r'\begin{tabular}{ll} ' )
        latex_lines.append( r'\hline Process & Events \\ \hline ' )

        lines = []
        lines.append('Process \t Events')
        for nm in order :
            if nm in stack_entries :
                lines.append('{nm}  \t {val:.0f}'.format( nm=nm, val=stack_entries[nm] ))
                latex_lines.append( '{nm} & {val:.0f} '.format( nm=nm, val=stack_entries[nm] ) + r'\\')

        for sig in signal_entries :
            lines.append('{nm}  \t {val:.0f}'.format( nm=sig, val=signal_entries[sig] ))
            latex_lines.append( '{nm} & {val:.0f} '.format( nm=sig, val=signal_entries[sig] )  + r'\\')

        lines.append('{{Stack Sum}}  \t {val:.0f}'.format(val=bkg_sum))
        latex_lines.append('\hline Stack Sum & {val:.0f} '.format(val=bkg_sum) + r'\\')

        '''
        for sig in signal_entries :
            den = umath.sqrt(signal_entries[sig] + bkg_sum )
            if den != 0 :
                lines.append('S/sqrt(S+B) (S=%s,B=All Bkg) : %s' %( sig, (signal_entries[sig]/den )) )
                latex_lines.append('S/sqrt(S+B) (S=%s) & %s ' %( sig, (signal_entries[sig]/den ) ) + r'\\')
            else :
                lines.append('S/sqrt(S+B) (S=%s,B=All Bkg) : nan' %( sig ) )
                latex_lines.append('S/sqrt(S+B) (S=%s) & nan ' %( sig) + r'\\')

        for sig in signal_entries :
            for st in stack_entries :
                den = umath.sqrt(signal_entries[sig] + stack_entries[st] )
                if den.n != 0 :
                    lines.append('S/sqrt(S+B) (S=%s,B=%s) : %s' %( sig, st,  (signal_entries[sig]/ den)  ))
                    #latex_lines.append('S/sqrt(S+B) (S=%s,B=%s) & %.2f' %( sig, st,  signal_entries[sig][0]/ den ) + r'\\')
                else :
                    lines.append('S/sqrt(S+B) (S=%s,B=%s) : NAN +- NAN' %( sig, st  ))
                    #latex_lines.append('S/sqrt(S+B) (S=%s,B=%s) & NAN' %( sig, st  ) + r'\\')
        '''

        if doRatio is not None and doRatio :
            rsamps = self.get_samples( isRatio=True )
            if rsamps :
                for rsamp in rsamps :
                    legend_entry = None
                    if hasattr( rsamp, 'legend_entry' ) :
                        legend_entry = rsamp.legend_entry
                    ratio_entries[rsamp.name] = {'legend_entry' : legend_entry, 'bins' : [] }
                    for _bin in range( 0, rsamp.hist.GetNbinsX() ) :
                        bin = _bin + 1
                        lines.append('%s, bin %d : %.3f += %.4f ' %( rsamp.name, bin, rsamp.hist.GetBinContent(bin), rsamp.hist.GetBinError(bin) ) )
                        ratio_entries[rsamp.name]['bins'].append(
                                                           {'bin' : bin, 'val' : rsamp.hist.GetBinContent(bin), 'err' : rsamp.hist.GetBinError(bin),
                                                           'min' : rsamp.hist.GetXaxis().GetBinLowEdge(bin),
                                                           'max' : rsamp.hist.GetXaxis().GetBinUpEdge(bin) }  )

        if details :
            detail_entries['detail'] = {}

            active_samps = self.get_samples(isActive=True)

            for samp in active_samps :
                if samp.hist is None :
                    continue
                detail_entries['detail'][samp.name] = {'bins' : {} }
                for bin in range(1, samp.hist.GetNbinsX()+1) :
                    val = samp.hist.GetBinContent(bin)
                    err = samp.hist.GetBinError(bin)

                    min = samp.hist.GetXaxis().GetBinLowEdge(bin)
                    max = samp.hist.GetXaxis().GetBinUpEdge(bin)

                    detail_entries['detail'][samp.name]['bins'][str(bin)] = {}
                    detail_entries['detail'][samp.name]['bins'][str(bin)]['val'] = ufloat( val, err )
                    detail_entries['detail'][samp.name]['bins'][str(bin)]['min'] = min
                    detail_entries['detail'][samp.name]['bins'][str(bin)]['max'] = max

                    lines.append('%s, bin %d (%s-%s) : %.3f += %.4f ' %( samp.name, bin, str(min), str(max), val, err ) )

        for line in lines :
            print line

        latex_lines.append( r'\hline\hline\end{tabular}' )

        if txtname is not None and outputDir is not None  :
            if cut:
               txtname += "_cut" + cut

            if txtname.count('.txt') == 0 :
                latexname = txtname + '.tex'
                picname = txtname + '.pickle'
                txtname += '.txt'
            else :
                latexname = txtname.rstrip('txt') + 'tex'
                picname = txtname.rstrip('txt') + 'pickle'

            if not os.path.isdir(outputDir ) :
                os.makedirs( outputDir )

            txtfile = open( outputDir + '/' + txtname, 'w')
            #txtfile = open( txtname, 'w')
            for line in lines :
                txtfile.write( line + '\n' )
            txtfile.close()
            #os.system( 'mv %s %s' %( txtname, outputDir ) )

            latexfile = open(outputDir + '/' + latexname, 'w')
            #latexfile = open(latexname, 'w')
            for line in latex_lines  :
                latexfile.write( line + '\n' )
            latexfile.close()
            #os.system( 'mv %s %s' %( latexname, outputDir ) )

            # write a pickle file
            stack_entries.update(signal_entries)
            stack_entries.update(ratio_entries)
            stack_entries.update(detail_entries)
            stack_entries['All Bkg'] = bkg_sum
            stack_entries['Total Expected'] = bkg_sum+sig_sum

            picfile = open( outputDir + '/' + picname, 'w' )
            pickle.dump( stack_entries, picfile )
            picfile.close()

        return

    #---------------------------------------
    def DumpRoc( self, outputDir=None, txtname=None, inDirs='' ) :

        output = []
        for title, entries in self.transient_data.iteritems() :
            output.append( title )
            print output[-1]
            for entry in entries :
                output.append('Cutval=%(CutVal)f, nSig=%(nSig)f, nBkg=%(nBkg)f, sigEff=%(sigEff)f, bkgEff=%(bkgEff)f, S/sqrt(S+B)=%(SoverRootSplusB)f ' %entry )
                print output[-1]

        if txtname is not None and outputDir is not None  :

            outdir = outputDir + '/' + inDirs

            if not os.path.isdir( outdir ) :
                print 'Making directory : ', outdir
                os.makedirs( outdir )

            if txtname.count('.txt') == 0 :
                txtname += '.txt'

            txtfile = open( outdir + '/' + txtname, 'w' )
            for out in output :
                txtfile.write( out + '\n' )
            txtfile.close()


    def ReloadSamples(self ) :

        #for samp in self.samples :
        #    if samp.chain is not None :
        #        samp.chain.Delete()

        self.samples = []

        self.ReadSamples(self.samples_conf )

    #--------------------------------
    def AddSample(self, name, path=None, filekey=None, isData=False, isSignal=False, sigLineStyle=7, sigLineWidth=2, drawRatio=False, plotColor=ROOT.kBlack, lineColor=None, isActive=True, required=False, displayErrBand=False, useXSFile=False, XSName=None, legend_name=None) :
        """ Create an entry for this sample """

        if self.added_sample_group :
            print 'WARNING -- Please add all samples before adding a sample group, othwerise you may see funny behavior'

        # get all root files under this sample
        input_files = []

        # accept path as string (-> single entry list) or list
        if not isinstance(path, list) :
            path = [path]

        # collect files from each path
        #
        # keep a list of paths that have
        # been traveresed and print a warning
        # if we're reading inconsistent paths
        subpaths_used = []
        paths_used    = []

        input_files = self.collect_input_files( self.base_path, path, paths_used, subpaths_used, filekey=filekey)

        if input_files :
            #
            # Print a warning if we might be getting the wrong files
            #
            n_unique_pathlenghts = len( set( [ len( upath.split('/') ) for upath in paths_used ] ) )
            if n_unique_pathlenghts > 1 :
                print 'Found ntuples in parent directories, these may be duplicates'

            thisscale = 1.0
            # multiply by command line MC weight only for MC
            #if self.mcweight is not None and not isData :
            if self.mcweight is not None  : ## FIXME
                thisscale *= self.mcweight

            xsname = name
            ## in case XS name does not match sample name
            if XSName is not None :
                xsname = XSName

            if useXSFile and xsname in self.weightMap  :
                self.weightMap[xsname]['scale'] *= thisscale
                thisSample = Sample(name, manager=self, isActive=isActive, isData=isData, isSignal=isSignal,
                                sigLineStyle=sigLineStyle, sigLineWidth=sigLineWidth, displayErrBand=displayErrBand,
                                color=plotColor, drawRatio=drawRatio, weightmap= self.weightMap[xsname], lumi=self.lumi, legendName=legend_name, path=path)
            else:
                thisSample = Sample(name, manager=self, isActive=isActive, isData=isData, isSignal=isSignal,
                                sigLineStyle=sigLineStyle, sigLineWidth=sigLineWidth, displayErrBand=displayErrBand,
                                color=plotColor, drawRatio=drawRatio, scale=thisscale, lumi=self.lumi,  legendName=legend_name, path=path)

            thisSample.AddFiles( input_files, self.treeName, self.readHists, self.weightHistName, self.dataFrame)
            rd = thisSample.getrdataframe()
            self.sampleptr[thisSample] = rd
            if isData: self.dataset.add(thisSample)

            self.samples.append(thisSample)

            # keep the order that this sample was added
            self.stack_order.append(name)
            if isActive: self.stack_order_original_active.append(name)

        if not input_files and required :
            print '***********************************************'
            print 'Sample, %s does not exist and is required by this module' %name
            print self.base_path
            print '***********************************************'
            sys.exit(-1)
        print_prefix = "AddSample: Reading %s " %( path[0] )
        print_prefix = print_prefix.ljust(60)
        if not input_files :
            self.quietprint(print_prefix + " [ \033[1;31mFailed\033[0m  ]")
        else :
            if len(set(path) & set(subpaths_used)) != len(path) :
                print print_prefix + " [ \033[1;33mPartial\033[0m ]"
                print path
                print subpaths_used
            else :
                self.quietprint( print_prefix + " [ \033[1;32mSuccess\033[0m ]" )

    #--------------------------------
    def collect_input_files( self, base_path, path_list, paths_used, subpaths_used, filekey=None ) :

        input_files = []

        # if the necessary inputs are not provided return an empty list
        if base_path is None or path_list is None or not path_list :
            return input_files

        for subpath in path_list :
            fullpath = base_path + '/' + subpath
            # if files have been provided, read them directly
            if os.path.isfile(fullpath) :
                input_files.append(fullpath)
            else : #otherwise search directories for the needed files
                if base_path.count( 'root://eoscms' ) :
                    for top, dirs, files, sizes in eos_utilities.walk_eos( base_path + '/' + subpath ) :
                        for file in files :
                            if filekey is not None :
                                if file.count(filekey) == 0 :
                                    continue
                            elif file.count(self.fileName) == 0 :
                                continue
                            paths_used.append(top)
                            subpaths_used.append(subpath)
                            input_files.append(top+'/'+file)

                else : # local directories
                    for top, dirs, files in os.walk( base_path +'/' + subpath , followlinks=True) :
                        for file in files :
                            if filekey is not None :
                                if file.count(filekey) == 0 :
                                    continue
                            elif file.count(self.fileName) == 0 :
                                continue
                            paths_used.append(top)
                            subpaths_used.append(subpath)
                            input_files.append(top+'/'+file)

        return input_files

    #--------------------------------
    def AddSampleGroup(self, name, input_samples=[], isData=False, scale=None, isSignal=False, sigLineStyle=7,drawRatio=False, plotColor=ROOT.kBlack, lineColor=None, legend_name=None, isActive=True, displayErrBand=False, averageSamples=False ) :
        """Make a new sample from any number of samples that have already been added via AddSample

           For example if a process is made of a number of individual samples that each have their
           own weight, first add those samples using AddSample with their own scale ( be sure
           to also give isActive=True or the individual samples will be drawn).  Then call
           Group Samples with the list of input samples and the new name.
        """

        self.added_sample_group=True
        #check if input samples actually exist
        available_samples = []
        for samp in input_samples :
            if samp not in self.get_sample_names() :
                print 'WARNING - Child sample, %s, does not exist!' %samp
            else :
                available_samples.append(samp)

        # if no input samples exist, exit
        if not available_samples :
            return

        # keep the order that this sample was added
        self.stack_order.append(name)
        if isActive: self.stack_order_original_active.append(name)

        thisscale = 1.0
        # multply by scale provided to this function (MCweight is applied to input samples)
        if scale is not None :
            thisscale *= scale

        print 'Grouping %s' %name
        thisSample = Sample(name, manager = self, isActive=isActive, isData=isData, isSignal=isSignal, sigLineStyle=sigLineStyle, displayErrBand=displayErrBand, color=plotColor, drawRatio=drawRatio, scale=thisscale, legendName=legend_name, averageSamples=averageSamples)

        for samp in available_samples :

            is_a_grouped_sample = ( name in self.get_grouped_sample_names() )

            if is_a_grouped_sample :
                group_samples = self.get_samples(name=name)[0].groupedSampleNames
                thisSample.AddGroupSamples( group_samples )
            else :
                thisSample.AddGroupSamples( samp )

        self.samples.append(thisSample)


    #--------------------------------

    def AddModelSampleGroup( self, name, input_samples=[],
                             isData = False, scale = None, isSignal = False,
                             drawRatio = False, plotColor = ROOT.kBlack,
                             lineColor = None, legend_name = None,
                             isActive = True) :
        """
        Make a new sample from any number of samples that have already been
        added via AddSample For example if a process is made of a number of
        individual samples that each have their own weight, first add those
        samples using AddSample with their own scale ( be sure to also give
        isActive=True or the individual samples will be drawn).  Then
        call Group Samples with the list of input samples and the new name.
        """

        thisscale = 1.0
        # multply by scale provided to this function (MCweight is applied to input samples)
        if scale is not None :
            thisscale *= scale

        print 'Grouping %s' %name
        thisSample = Sample(name, manager = self, isActive=isActive,
                isData=isData, isSignal=isSignal, color=plotColor,
                drawRatio=drawRatio, scale=thisscale, legendName=legend_name)

        for samp in input_samples :
            is_a_grouped_sample = ( name in self.get_grouped_sample_names() )

            if is_a_grouped_sample :
                group_samples = self.get_samples(name=name).groupedSampleNames
                thisSample.AddGroupSamples( group_samples )
            else :
                thisSample.AddGroupSamples( samp )

        self.modelSamples.append(thisSample)



    #--------------------------------
    def AddModelSample(self, name, legend_name=None, path=None, scale=1.0 ,
                            filekey=None, plotColor=ROOT.kBlack) :
        input_files = []

        if not isinstance(path, list) :
            path = [path]

        # keep a list of paths that have
        # been traveresed and print a warning
        # if we're reading inconsistent paths
        subpaths_used = []
        paths_used    = []

        input_files = self.collect_input_files( self.base_path_model, path,
                                paths_used, subpaths_used, filekey=filekey)

        if input_files :
            #
            # Print a warning if we might be getting the wrong files
            #
            n_unique_pathlenghts = len( set( [ len( upath.split('/') )\
                                        for upath in paths_used ] ) )
            if n_unique_pathlenghts > 1 :
                print 'Found ntuples in parent directories, '+\
                      'these may be duplicates'

            thisscale = 1.0
            if scale is not None :
                thisscale *= scale

            thisSample = Sample(name, manager = self, color=plotColor,
                                scale=thisscale, legend_name=legend_name)
            thisSample.AddFiles( self.treeNameModel, input_files )
            self.modelSamples.append(thisSample)

        print_prefix = "AddModelSample: Reading %s (%s) " %(name, path )
        print_prefix = print_prefix.ljust(60)
        if not input_files :
            print print_prefix + " [ \033[1;31mFailed\033[0m  ]"
        else :
            if len(set(path) & set(subpaths_used)) != len(path) :
                print print_prefix + " [ \033[1;33mPartial\033[0m ]"
            else :
                print print_prefix + " [ \033[1;32mSuccess\033[0m ]"



    #--------------------------------

    def ReadSamples(self, conf, expected=[], failOnMissing=False ) :

        self.samples_conf = conf

        self.expected_samples = expected
        self.fail_on_missing = failOnMissing

        ImportedModule=None

        ispath = ( conf.count('/') > 0 )
        module_path = None
        if ispath :
            module_path = conf
        else :
            #get path of this script
            script_path = os.path.realpath(__file__)
            module_path = os.path.dirname(script_path) + '/' + conf

        try :
            ImportedModule = imp.load_source(conf.split('.')[0], module_path)
        except IOError :
            print 'Could not import module %s' %module_path

        if hasattr(ImportedModule, 'config_samples') :
            if not self.quiet:
                print '-------------------------------------'
                print 'BEGIN READING SAMPLES'
                print '-------------------------------------'
            ImportedModule.config_samples(self)
        else :
            print 'ERROR - samplesConf does not implement a function called config_samples '
            sys.exit(-1)

        if hasattr(ImportedModule, 'print_examples') :
            ImportedModule.print_examples()
        else :
            print 'WARNING - samplesConf does not implement a function called print_examples '



    #--------------------------------

    def DrawHist(self, histpath, rebin=None, varRebinThresh=None, doratio=False, subtract_bkg=False, ylabel=None, xlabel=None, rlabel=None, logy=False, ymin=None, ymax=None, rmin=None, rmax=None, xmin=None, xmax=None, normalize=False, ticks_x=None, ticks_y=None, label_config={}, legend_config={}) :

        self.clear_all()
        for sample in self.samples :
            self.get_hist( sample, histpath )

        if varRebinThresh is not None :
            self.variable_rebinning(varRebinThresh)

        if rebin is not None :
            for samp in self.get_samples( isActive=True ) :
                if samp.hist is not None :
                    samp.hist.Rebin(rebin)

        draw_config = DrawConfig( histpath, None, None, hist_config={'doratio' : doratio, 'xlabel' : xlabel, 'ylabel' : ylabel, 'ymin' : ymin, 'ymax' : ymax, 'logy' : logy, 'rmin' : rmin, 'rmax' : rmax, 'normalize' : normalize, 'ticks_x' : ticks_x, 'ticks_y' : ticks_y} , label_config=label_config, legend_config=legend_config)

        # make a stack if there are samples to be
        # stacked.  If no stacked samples exist
        # then just histograms are being drawn
        if self.get_stack_order()  :
            self.MakeStack(draw_config )

        if ylabel is None :
            binwidth = self.get_samples(isActive=True)[0].hist.GetBinWidth(1)
            ylabel = 'Events / %.1f GeV' %binwidth
        if rlabel is None :
            rlabel = 'Data / MC'

        datahists = ['Data']
        if subtract_bkg :
            new_data = self.clone_sample( 'Data', 'DataSub', temporary=True )
            data_hist = self.get_samples( name='Data' )[0].hist
            bkg_hist = self.get_samples( name='Background' )[0].hist
            new_bkg = self.clone_sample( 'Background', 'BackgroundSub', temporary=True )

            new_data.hist = data_hist.Clone( 'DataSub' )
            new_bkg.hist = bkg_hist.Clone( 'BackgroundSub' )
            for bin in range( 1, data_hist.GetNbinsX() + 1 ) :
                data_val = data_hist.GetBinContent( bin )
                data_err = data_hist.GetBinError( bin )

                bkg_val = bkg_hist.GetBinContent( bin )
                bkg_err = bkg_hist.GetBinError( bin )

                new_bkg.hist.SetBinContent( bin, 0. )

                new_val = data_val - bkg_val
                #new_err = math.sqrt( data_err*data_err + bkg_err*bkg_err )
                new_err = data_err

                new_data.hist.SetBinContent( bin, new_val )
                new_data.hist.SetBinError( bin, new_err )

            datahists = ['DataSub']

        errSamp = None
        err_samp_list = [ s for s in self.get_samples( isActive=True ) if s.displayErrBand ]
        if subtract_bkg :
            err_samp_list = self.get_samples( name='DataSub' )
            #err_samp_list = []

        for samp in err_samp_list :
            bkg_name = _STACKNAME
            if subtract_bkg :
                bkg_name = 'BackgroundSub'

            all_stack_hist = self.get_samples( name=bkg_name )[0].hist
            if errSamp is None :
                errSamp = self.clone_sample( samp.name, 'err_band', temporary=True )
                errSamp.hist = all_stack_hist.Clone('err_band')
                for bin in range(1, errSamp.hist.GetNbinsX() + 1 ) :
                    errSamp.hist.SetBinContent(bin, 0)
                    errSamp.hist.SetBinError(bin, 0)
            for bin in range(1, all_stack_hist.GetNbinsX()+1 ) :
                # set the bin content to the stack sum
                # unless the background is subtracted
                # at which point it should be at zero
                if not subtract_bkg :
                    errSamp.hist.SetBinContent( bin, all_stack_hist.GetBinContent( bin ) )
                curr_err = errSamp.hist.GetBinError( bin )
                this_err = samp.hist.GetBinError(bin)
                errSamp.hist.SetBinError( bin, math.sqrt( curr_err*curr_err + this_err*this_err )  )


        # for plotting a TGraphErrors is needed
        if errSamp is not None :
            errSamp.graph = ROOT.TGraphErrors( errSamp.hist )

        # calculate a chi-2 with respect to the errors
        if errSamp is not None :
            chi2sum = 0
            dataSamp = self.get_samples( name=datahists[0] )[0]
            nbins = errSamp.hist.GetNbinsX()
            for binnum in range( 1,  nbins +1 ) :

                exp_bkg = errSamp.hist.GetBinContent( binnum )
                exp_err = errSamp.hist.GetBinError( binnum )
                data_val = dataSamp.hist.GetBinContent( binnum )
                data_err = dataSamp.hist.GetBinError( binnum )

                tot_err = math.sqrt( data_err*data_err + exp_err*exp_err )

                if not tot_err == 0 :
                    chi2sum += math.pow( (exp_bkg-data_val) / tot_err, 2 )

            pzero = ROOT.TMath.Prob( chi2sum, nbins )
            print pzero

            kstest = dataSamp.hist.KolmogorovTest( errSamp.hist  )
            print kstest

            label_style = label_config.get('labelStyle', '')
            if not label_style.count( 'nostats' ) :
                draw_config.label_config['statsLabel'] = '#chi^{2} = %.1f, p0 = %.3f ' %(chi2sum , pzero )

        topcan = self.curr_stack

        self.DrawCanvas(topcan, draw_config, datahists=datahists, sighists=self.get_signal_samples(), errhists=['err_band']  )

        if xmin is not None and xmax is not None :
            for prim in self.curr_canvases['top'].GetListOfPrimitives() :
                if isinstance( prim, ROOT.TH1F ) :
                    prim.GetXaxis().SetRangeUser( xmin, xmax )

        if not self.get_stack_order()  :
            # if histograms are being drawn then
            # most of the work happens in DrawCanvas
            # but we still need to create a legend

            # first find the active samples
            active_samps = self.get_samples( isActive=True )
            self.curr_legend = self.create_standard_legend( len( active_samps ), draw_config=draw_config)

            legendOrder = legend_config.get( 'legendOrder', [] )

            if legendOrder :
                active_samps = []

                for entry in legendOrder :
                    active_samps.append( self.get_samples( name = entry )[0] )


            self.create_same_legend(legend_entries=legendOrder, created_samples=active_samps)

            self.curr_legend.Draw()


    #--------------------------------

    def ShowCount(self, counter=None, dolatex=False, isActive=True, includeData=False, sort=True):
        """ Show count result after SampleFrame.SetCounter(), triggers loop """

        if counter == None:
            print "no counter"
            return

        ## check that SampleFrame is passed
        if not isinstance(counter, SampleFrame) and counter.state == "count":
            return

        for sample in self.samples :
            if sample.isData and not includeData:
                continue
            if sample.isActive:
                self.create_count(sample, counter)

        result = [(s.legendName if dolatex else s.name,(s.count.n, s.count.s))\
                         for s in self.get_samples(isActive=isActive,isData=False) if s.name != "ratio" and s.count is not None]
        total = sum([s.count for s in self.get_samples(isSignal=False,isActive=isActive,isData=False)\
                if s.name != "ratio" and s.count is not None])
        if sort: result.sort(key=lambda x: -x[1][0])
        resultdict = OrderedDict(result)
        resultdict["TOTAL"] = (total.n, total.s) if total !=0 else (0,0)
        self.print_stackresult(resultdict)
        return resultdict

    #--------------------------------

    def Draw(self, varexp, selection="", histpars=None,
                   hist_config = {}, legend_config = {}, label_config = {},
                   treeHist=None, treeSelection=None, useModel=False,
                   generate_data_from_sample = None,
                   replace_selection_for_sample = {} ):
        """
        Draw 1D histogram with all active samples

        Arguments:
                - varexp: plot variable
                - selection: selection passed to all samples
                - histpars: for 1D histogram, a tuple with (Nbins, lower bound,
                  upper bound) for variable bins use a list [] of bin
                  boundaries for 2D histogram, either a 6-tuple, or a tuple
                  with two lists

        produces a histogram and displayed through a TCanvas
        """

        if self.quiet : print "%s :\033[1;36m %s\033[0m" %(varexp,selection)

        if self.collect_commands :

            self.add_draw_config( varexp, selection, histpars,
                                          hist_config   = hist_config,
                                          label_config  = label_config,
                                          legend_config = legend_config,
                     replace_selection_for_sample=replace_selection_for_sample )
            return

        if not isinstance(varexp, SampleFrame):
            command = 'samples.Draw(\'%s\',  \'%s\', %s )' \
                                %( varexp, selection, str( histpars ) )
            self.transient_data['command'] = command

        draw_config = DrawConfig( varexp, selection, histpars,
                                          hist_config   = hist_config,
                                          label_config  = label_config,
                                          legend_config = legend_config,
                    replace_selection_for_sample=replace_selection_for_sample )

        self.draw_and_configure( draw_config, treeHist=treeHist,
                        generate_data_from_sample=generate_data_from_sample,
                        useModel=useModel,
                        treeSelection=treeSelection )

        self.curr_sampleframe.histpars = histpars
        return self.curr_sampleframe



    #--------------------------------

    def draw_and_configure( self, draw_config, generate_data_from_sample=None,
                          useModel=False, treeHist=None, treeSelection=None ) :
        """
             calls makestack, implment option to imitate data,
             helper function for SampleManager.Draw
        """

        self.clear_all()

        self.curr_sampleframe = SampleFrame(samplemanager=self)
        self.curr_sampleframe.state = "histo"

        ### histograms for most MC samples are filled here
        res = self.draw_active_samples( draw_config )
        if not res :
            return

        if generate_data_from_sample is not None :
            samp_list = self.get_samples( name=generate_data_from_sample )

            if samp_list :
                rand = ROOT.TRandom3()
                rand.SetSeed( int( time.time() ) )
                nbins = samp_list[0].hist.GetNbinsX()

                for bin in range( 1, nbins+1 ) :
                    newval = rand.Poisson( samp_list[0].hist.GetBinContent(bin) )
                    samp_list[0].hist.SetBinContent( bin, newval )
                    if newval > 0 :
                        samp_list[0].hist.SetBinError( bin, math.sqrt(newval) )


        if useModel :
            for sample in self.modelSamples :
                self.create_hist_new( draw_config, sample, isModel=True )

            # Model is created, replace the sample in self.samples with the
            # sample having the same name in self.modelSamples
            for samp in self.modelSamples :
                if samp.name in self.get_sample_names() :
                    self.get_samples(name=name).hist = samp.hist
                    self.get_samples(name=name).legendName = samp.legendName

        if isinstance( draw_config.histpars, tuple) \
                                        and len(draw_config.histpars) == 4 :
            if isinstance( draw_config.histpars[3], list ) :
                self.variable_rebinning(binning=draw_config.histpars[3])
            else :
                self.variable_rebinning(threshold=draw_config.histpars[3])

        self.MakeStack(draw_config, useModel, treeHist, treeSelection )

        self.DrawCanvas(self.curr_stack, draw_config,
                                datahists=['Data'],
                                sighists=self.get_signal_samples(),
                                errhists = [_STACKNAME] )


    #--------------------------------

    def Draw3DProjections(self, varexp, selection, histpars=None, x_by_y_bin_vals={}, doratio=False, ylabel=None, xlabel=None, rlabel=None, logy=False, ymin=None, ymax=None, ymax_scale=None, rmin=None, rmax=None, showBackgroundTotal=False, backgroundLabel='AllBkg', removeFromBkg=[], addToBkg=[], useModel=False, treeHist=None, treeSelection=None, labelStyle=None, extra_label=None, extra_label_loc=None, generate_data_from_sample=None, replace_selection_for_sample={}, legendConfig=None  ) :

        command = 'samples.Draw(\'%s\',  \'%s\', %s )' %( varexp, selection, str( histpars ) )

        if not x_by_y_bin_vals :
            print 'Must give a dictionary that maps y bins to x bins'

        self.clear_all()

        self.transient_data['command'] = command

        self.apply_lenged_conf( legendConfig )

        res = self.draw_active_samples( draw_config )

        if not res :
            return

        if generate_data_from_sample is not None :
            samp_list = self.get_samples( name=generate_data_from_sample )
            if samp_list :
                rand = ROOT.TRandom3()
                rand.SetSeed( int( time.time() ) )
                nbins = samp_list[0].hist.GetNbinsX()
                for bin in range( 1, nbins+1 ) :
                    newval = rand.Poisson( samp_list[0].hist.GetBinContent(bin) )
                    samp_list[0].hist.SetBinContent( bin, newval )
                    if newval > 0 :
                        samp_list[0].hist.SetBinError( bin, math.sqrt(newval) )


        if useModel :
            for sample in self.modelSamples :
                self.create_hist( sample, treeHist, treeSelection, histpars, isModel=True )

            # Model is created, replace the sample in self.samples with the
            # sample having the same name in self.modelSamples
            for samp in self.modelSamples :
                if samp.name in self.get_sample_names() :
                    self.get_samples(name=name).hist = samp.hist
                    self.get_samples(name=name).legendName = samp.legendName

        for sample in self.get_samples() :
            if sample.hist is not None :
                sample.main_hist = sample.hist.Clone( )


            else :
                sample.main_hist = None

        for (xmin, xmax), yvals_raw in x_by_y_bin_vals.iteritems() :

            if not isinstance( yvals_raw[0], tuple) :
                yvals = []
                for idx, yval_raw_min in enumerate( yvals_raw[:-1] ) :
                    yval_raw_max = yvals_raw[idx+1]
                    yvals.append( (yval_raw_min, yval_raw_max) )
            else :
                yvals = yvals_raw

            for ymin, ymax in yvals :
                for sample in self.get_samples() :
                    if hasattr(sample, 'main_hist' ) and sample.main_hist is not None :

                        if xmin is None :
                            xbin_min = 1
                        else :
                            xbin_min = sample.main_hist.GetXaxis().FindBin( xmin )

                        if xmax is None :
                            xbin_max = sample.main_hist.GetNbinsX()
                        else :
                            xbin_max = sample.main_hist.GetXaxis().FindBin( xmax )

                        if ymin is None :
                            ybin_min = 1
                        else :
                            ybin_min = sample.main_hist.GetYaxis().FindBin( ymin )

                        if ymax is None :
                            ybin_max = sample.main_hist.GetNbinsY()
                        else :
                            ybin_max = sample.main_hist.GetYaxis().FindBin( ymax )

                        print 'xmin = %d, xmax = %s, ymin = %f, ymax = %f, xbinmin = %d, xbinmax = %d, ybinmin = %d, yminmax = %d' %( xmin, xmax, ymin, ymax, xbin_min, xbin_max, ybin_min, ybin_max)
                        sample.hist = sample.main_hist.ProjectionZ( 'h_'+str( uuid.uuid4()).replace('-','_'), xbin_min, xbin_max, ybin_min, ybin_max )  # important to change - to _ -- Yihui
                    else :
                        sample.hist = None


                self.MakeStack(varexp, doratio, showBackgroundTotal, backgroundLabel, removeFromBkg, addToBkg, useModel, treeHist, treeSelection )

                if ylabel is None :
                    bin_width = ( histpars[2] - histpars[1] )/histpars[0]
                    bin_width_f = ( histpars[2] - histpars[1] )/float(histpars[0])
                    if math.fabs(bin_width_f - bin_width) != 0 :
                        ylabel = 'Events / %.1f GeV' %bin_width_f
                    else :
                        ylabel = 'Events / %d GeV' %bin_width
                if rlabel is None :
                    rlabel = 'Data / MC'

                self.DrawCanvas(self.curr_stack, ylabel=ylabel, xlabel=xlabel, rlabel=rlabel, logy=logy, ymin=ymin, ymax=ymax, ymax_scale=ymax_scale, rmin=rmin, rmax=rmax, datahists=['Data'], sighists=self.get_signal_samples(), doratio=doratio, labelStyle=labelStyle, extra_label=extra_label, extra_label_loc=extra_label_loc )

                yield (xmin, xmax, ymin, ymax)



    #--------------------------------

    def DrawSamples(self, varexp, selection, samples, histpars=None, normalize=False, doratio=False, useTreeModel=False, treeHist=None, treeSelection=None ) :
        if not isinstance( samples, list ) :
            samples = [samples]

        self.MakeSameCanvas(samples, varexp, selection, histpars, doratio)
        self.DrawSameCanvas(normalize, doratio)


    #--------------------------------

    def MakeStack(self, draw_config, useModel=False, treeHist=None,
                        treeSelection=None ) :

        # get all stacked histograms and add them
        stack_samples = self.get_samples( name=self.get_stack_order() )
        doratio = draw_config.get_doratio()
        normalize = draw_config.get_normalize()
        bywidth = draw_config.get_bywidth()

        if stack_samples :
            sum_hist = stack_samples[0].hist.Clone(_STACKNAME)
            for samp in stack_samples[1:] :
                sum_hist.Add(samp.hist)

            if bywidth:
                stack_sum = sum_hist.Integral("width")
            else:
                stack_sum = sum_hist.Integral()
            if normalize:
                sum_hist.Scale(1./stack_sum)
            # TODO: divide by bin width here? Or below? Add some printout...
            self.create_sample( _STACKNAME, isActive=False, hist=sum_hist,
                                temporary=True )

        if doratio :
            # when stacking, the ratio is made with respect to the data.  Find
            # the sample that is labeled as data.  Throw an error if one data
            # sample is not found

            data_samples = self.get_samples(isData=True, isActive=True)
            if not data_samples :
                print 'MakeStack - ERROR : No data samples found!'
            assert len(data_samples)>=1

            self.create_ratio_sample( 'ratio', num_sample = data_samples[0],
                                               den_sample = _STACKNAME )

            # make ratio histograms for signal samples
            signal_samples = self.get_samples( isSignal=True, drawRatio=True )
            for sample in signal_samples :
                ratio_samp = self.create_ratio_sample( sample.name + '_ratio',
                                                 num_sample = data_samples[0],
                                                 den_sample = sample )
                ratio_samp.hist.SetLineColor( sample.color )
                ratio_samp.isSignal = True

        #make the stack and fill
        self.curr_stack = (ROOT.THStack('stack' + str(uuid.uuid4()).replace('-','_'), '')) # important to change - to _ -- Yihui

        # reverse so that the stack is in the correct order
        orderd_samples = []

        for sampname in self.get_stack_order():
            samplist = self.get_samples(name=sampname, isActive=True )
            if samplist :
                orderd_samples.append(samplist[0])

        for samp in reversed(orderd_samples) :
            samp.hist.SetFillColor( samp.color )
            samp.hist.SetLineColor( ROOT.kBlack )
            samp.hist.SetLineWidth( 1 )
            if normalize:
                samp.hist.Scale(1./stack_sum)
            self.curr_stack.Add(samp.hist, 'HIST')

        # additional formatting
        data_samp = self.get_samples(name='Data')

        # make the legend
        # In placing the legend move the bottom down 0.05 for each entry
        # calculate the step usa
        drawn_samples = []
        for sname in self.get_stack_order():
            drawn_samples+=self.get_samples( name=sname, failed_draw=False, isActive=True )
        step = len(drawn_samples)

        self.curr_legend = self.create_standard_legend( step, draw_config=draw_config)

        nsigsamp = len(self.get_signal_samples())
        if nsigsamp:
           ## neeed to plot signal distributions
           self.curr_sig_legend = self.create_standard_legend( step, draw_config=draw_config, isSignalLegend = True, nSigEntries = nsigsamp)
        else:
           self.curr_sig_legend = None

        legendTextSize = draw_config.legend_config.get('legendTextSize', 0.04 )
        #legendTextSize = 0.04

        # format the entries
        tmp_legend_entries = []
        #tmp_sig_legend_entries = []
        legend_entries = []
        #sig_legend_entries = []

        if data_samp and data_samp[0].isActive and draw_config.get_unblind() :
            tmp_legend_entries.append(  (data_samp[0].hist, data_samp[0].legendName, 'PE') )

        for samp in drawn_samples :
            if samp.isSignal:
               tmp_sig_legend_entries.append( (samp.hist, samp.legendName, 'L'))
            else:
               tmp_legend_entries.append( ( samp.hist, samp.legendName,  'F') )
        print "tmp_legend_entries", tmp_legend_entries

        self.quietprint( '********************NOT FILLING SIGNAL ENTRY IN LEGEND**********************')
        #for samp in self.get_signal_samples() :
        #    if samp.isActive :
        #        tmp_legend_entries.append( ( samp.hist, samp.legendName, 'L') )

        if self.legendLoc=='Double' :
            legend_entries = [None]*len(tmp_legend_entries)
            if len(legend_entries)%2 == 0 :
                n_first_col = len(legend_entries)/2
            else :
                n_first_col = (len(legend_entries)/2) + 1
            n_2nd_col = 0
            for idx in range(0, len(tmp_legend_entries) ) :
                if idx%2 == 0 :
                    if idx < n_first_col :
                        newidx = idx*2
                        legend_entries[newidx] = tmp_legend_entries[idx]
                    else :
                        n_2nd_col+=1
                        newidx = n_2nd_col*2-1
                        legend_entries[newidx] = tmp_legend_entries[idx]
                else :
                    if idx < n_first_col :
                        newidx = idx*2;
                        legend_entries[newidx] = tmp_legend_entries[idx]
                    else :
                        n_2nd_col+=1
                        newidx = n_2nd_col*2-1
                        legend_entries[newidx] = tmp_legend_entries[idx]

        else :
            legend_entries = tmp_legend_entries
        #sig_legend_entries = tmp_sig_legend_entries
        for le in legend_entries :
            entry = self.curr_legend.AddEntry(le[0], le[1], le[2])
            if legendTextSize is not None :
                entry.SetTextSize(legendTextSize)

        #for le in sig_legend_entries :
        #    entry = self.curr_sig_legend.AddEntry(le[0], le[1], le[2])
        #    if legendTextSize is not None :
        #        entry.SetTextSize(legendTextSize)


    #----------------------------------------------------

    def MakeSameCanvas(self, draw_config, useStoredBinning=False, preserve_hists=False, useModel=False, treeHist=None, treeSelection=None, readhist = False) :
        """
            Called by CompareSelections
            Clone sample and fill histograms
        """

        if not preserve_hists :
            self.clear_all()

        created_samples = []
        for hist_name, hist_config in draw_config.hist_configs.iteritems() :

            samp = hist_config['sample']
            selection = hist_config['selection']
            sblind  = draw_config.get_unblind()
            sweight = draw_config.get_weight()
            if samp=="Data" and isinstance(sblind,str):
                    selection = "(%s)&&(%s)" %(selection,sblind)
            if isinstance(sweight,str) and sweight:
                    selection = "(%s)*%s" %(selection,sweight)

            # In this case the same sample may be drawn multiple
            # times.  to avoid any conflicts, add new samples
            # and draw into those

            newname = samp+"_"+hist_name

            newsamp = self.clone_sample( oldname=samp, newname=newname,
                                         temporary=True )

            if readhist:
                self.read_hist(newsamp, hist_config['var'], draw_config)
            elif useModel :
                self.create_hist( newsamp, treeHist, treeSelection,
                                  draw_config.histpars, isModel=True )
            else :
                self.create_hist( newsamp, hist_config['var'],
                                  selection, draw_config.histpars)

            created_samples.append( newsamp )

        if not created_samples :
            print 'No hists were created'
            return created_samples

        if isinstance( draw_config.histpars, tuple) and \
                len(draw_config.histpars) == 4 :

            if isinstance( draw_config.histpars[3], list ) :
                self.variable_rebinning(binning=draw_config.histpars[3],
                                        samples=created_samples,
                                        useStoredBinning=useStoredBinning)
            else :
                self.variable_rebinning(threshold=draw_config.histpars[3],
                                        samples=created_samples,
                                        useStoredBinning=useStoredBinning)

        if draw_config.get_doratio() :
            self.create_top_canvas_for_ratio('same')
        else :
            self.create_standard_canvas('same')

        self.curr_canvases['same'].cd()

        #
        # Calls DrawSameCanvas
        self.DrawSameCanvas( self.curr_canvases['same'], created_samples, draw_config )

        if draw_config.get_doratio() :
            #rname = created_samples[0].name + '_ratio'
            refhist_config = draw_config.hist_configs.items()[0]
            refname = refhist_config[1]["sample"]+"_"+refhist_config[0]
            for hist_name in draw_config.hist_configs.keys()[1:] :
                hist_config = draw_config.hist_configs[hist_name]

                samp = hist_config['sample']
                color = hist_config['color']

                rcolor = color
                if len( draw_config.hist_configs ) == 2 :
                    rcolor = ROOT.kBlack

                rname = 'ratio%s' %samp
                if rname in self.get_sample_names() :
                    for i in range(0, 100 ) :
                        rname = 'ratio%s_%d' %(samp, i)
                        if rname not in self.get_sample_names() :
                            break
                reverseratio = draw_config.get_reverseratio()
                binomunc = draw_config.get_binomunc()
                doratio =  draw_config.get_doratio()
                dodiff = doratio == "dodiff"
                rsamp = self.create_ratio_sample( rname, num_sample = refname
                         , den_sample=samp+"_"+hist_name, color=rcolor, reverseratio=reverseratio,binomunc=binomunc, dodiff = dodiff)
                rsamp.legend_entry = hist_config.get('legend_entry', None )

        return created_samples



    #--------------------------------

    def get_hist( self, sample, histpath ) :
        sampname = sample.name
        print 'Getting hist for %s' %sampname

        # check that this histogram hasn't been drawn
        if sample.hist is not None :
            print 'Histogram already extracted for %s' %sampname
            return

        # Draw the histogram.  Use histpars as the bin limits if given
        if sample.IsGroupedSample() :
            for subsampname in sample.groupedSampleNames :
                subsamp = self.get_samples( name=subsampname )[0]
                print 'Extract grouped hist %s' %subsampname
                if subsampname in self.get_sample_names() :
                    self.get_hist( subsamp, histpath )


            self.group_sample( sample )
            return

        else :

            thishist = sample.ofiles[0].Get(histpath)
            if thishist == None :
                print 'Could not get hist!'
                sample.isActive=False
            else :
                for ofile in sample.ofiles[1:] :
                    thishist.Add( ofile.Get(histpath) )

                if sample.hist is not None :
                    sample.hist.Delete()

                sample.hist = thishist
                if sample.hist is not None :
                    self.format_hist( sample )


    #--------------------------------

    @f_Dumpfname
    def read_hist( self, sample, histname , draw_config) :

        if isinstance( sample, str) :
            slist = self.get_samples( name=sample )
            if not slist :
                print 'Could not retrieve sample, %s' %sample
                return False
            if len(slist) > 1 :
                print 'Located multiple samples with name %s' %sample
                return False
            sample = slist[0]

        sampname = sample.name

        if not self.quiet : print 'obtaining hist %s : %s ' %( sample, histname )

        #histname = str(uuid.uuid4())

        sample.hist = None


        # Draw the histogram.  Use histpars as the bin limits if given
        if sample.IsGroupedSample() :
            for subsampname in sample.groupedSampleNames :
                subsamp = self.get_samples( name=subsampname )[0]

                if not self.quiet : print 'Draw grouped hist %s' %subsampname

                if subsampname in [s.name for s in self.get_model_samples()] :
                    self.read_hist( subsamp, histname)
                elif subsampname in self.get_sample_names() :
                    self.read_hist( subsamp, histname)

            sample.failed_draw=False
            for subsampname in sample.groupedSampleNames :
                subsamp = self.get_samples( name=subsampname )[0]
                if subsamp.failed_draw :
                    sample.failed_draw=True


            self.group_sample( sample )

            return True

        else :
            sample.failed_draw=False
            print sample.name
            for f in sample.ofiles:
                f = ROOT.TFile(f)
                histtemp = f.Get(histname)
                print f, histtemp, histname
                if histtemp and not sample.hist:
                    sample.hist = histtemp.Clone()
                    sample.hist.SetDirectory(0) ## safe for TFile::Close
                elif histtemp:
                    sample.hist.Add(histtemp)
                else:
                    sample.failed_draw=True
            ## normalize to cross_section
            if sample.hist is not None :
                sample.hist.SetTitle( sampname )
                sample.hist.Sumw2()
                ROOT.SetOwnership(sample.hist, False )
            sample.InitHist(onthefly = draw_config.get_onthefly())
            return True


    #--------------------------------

    def parsehist(self, histpars, varexp, histname=None,
                             returnmodel = False):
        """
            helper function to parse histogram inputs
            return histogram type and model
            1D histogram: condition - varexp = "varx"
                          histpars  - 1. (Nbinx, xbinlow, xbinhigh)
                                    - 2. [xbins]
            2D histogram: condition - varexp = "varx:vary"
                          histpars  - 1. (Nbinx, xbinlow, xbinhigh,
                                          Nbiny, ybinlow, ybinhigh)
                                    - 2. ([xbins],[ybins])
            3D histogram: condition - varexp = "varx:vary:varz"
                          histpars  - 1. (Nbinx, xbinlow, xbinhigh,
                                          Nbiny, ybinlow, ybinhigh,
                                          Nbinz, zbinlow, zbinhigh

            if returnmodel is True, only the function model is
            returned. This is used by RDataFrame booking

        """

        if histname==None: histname = 'h_'+str(uuid.uuid4()).replace('-','_') # important to change - to _ -- Yihui
        if type( histpars ) is tuple :
            if varexp.count(':') == 1 :
                if len(histpars) == 2 and type( histpars[0] ) is list and \
                                          type( histpars[1] ) is list :
                    fx = ROOT.TH2F
                    model = ( histname, '',
                            len(histpars[0])-1, array('f', histpars[0]),
                            len(histpars[1])-1, array('f', histpars[1]) )
                else :
                    if len(histpars) != 6 :
                        print 'varable expression, %s,  requests a 2-d'\
                               'histogram, please provide 6 hist parameters,'\
                               'nbinsx, xmin, xmax, nbinsy, ymin, ymax' %varexp
                        return

                    fx = ROOT.TH2F
                    model = ( histname, '',
                              histpars[0], histpars[1], histpars[2],
                              histpars[3], histpars[4], histpars[5] )

            elif varexp.count(':') == 2 and not varexp.count('::') :

                # make a 3-d histogram
                if len(histpars) != 9 :
                    print 'varable expression, %s,  requests a 3-d histogram,'\
                          'please provide 9 hist parameters, nbinsx, xmin,'\
                          'xmax, nbinsy, ymin, ymax, nbinsz, zmin, zmax' %varexp
                    return
                fx = ROOT.TH3F
                model = ( histname, '',
                          histpars[0], histpars[1], histpars[2],
                          histpars[3], histpars[4], histpars[5],
                          histpars[6], histpars[7], histpars[8] )
            else : # 1-d histogram
                fx = ROOT.TH1F
                model = (histname,'',int(histpars[0]), histpars[1], histpars[2])

        elif type( histpars ) is list :
            fx = ROOT.TH1F
            model = ( histname, '', len(histpars)-1, array('f', histpars))
        else :
            print 'No histogram parameters were passed'
            return

        if returnmodel:
            return model

        return fx(*model)



    #--------------------------------

    def create_hist( self, sample, varexp, selection, histpars,
                           ismodel = False, overflow = True) :

        if isinstance( sample, str) :
            slist = self.get_samples( name=sample )
            if not slist :
                print 'Could not retrieve sample, %s' %sample
                return False
            if len(slist) > 1 :
                print 'Located multiple samples with name %s' %sample
                return False
            sample = slist[0]

        sampname = sample.name

        #if not self.quiet : print 'Creating hist for %s' %sampname
        #if not self.quiet : print '%s : %s ' %( varexp, selection )
        #if not self.quiet : print histpars

        ## check that this histogram hasn't been drawn
        #if sample.hist is not None :
        #    print 'Histogram already drawn for %s' %sampname
        #    return

        full_selection = selection

        # enable branches for all variables matched in the varexp and selection
        sample.enable_parsed_branches( varexp+selection )

        sample.hist = None
        histname = sampname + str(uuid.uuid4()).replace('-','_') # important to change - to _ -- Yihui
        sample.hist = self.parsehist(histpars, varexp, histname)
        if sample.hist is not None :
            sample.hist.SetTitle( sampname )
            sample.hist.Sumw2()
            ROOT.SetOwnership(sample.hist, False )

        # Draw the histogram.  Use histpars as the bin limits if given
        if sample.IsGroupedSample() :
            for subsampname in sample.groupedSampleNames :
                subsamp = self.get_samples( name=subsampname )[0]

                if not self.quiet : print 'Draw grouped hist %s' %subsampname


                subsampnamelist = [s.name for s in self.get_model_samples()]
                ### case 1: if sample is model
                if ismodel and subsampname in subsampnamelist:
                    self.create_hist( subsamp, varexp, selection, histpars,
                                      ismodel=ismodel ,overflow=overflow)
                elif subsampname in self.get_sample_names() :
                    self.create_hist( subsamp, varexp, selection, histpars,
                                      ismodel=ismodel ,overflow=overflow)

            sample.failed_draw=False
            for subsampname in sample.groupedSampleNames :
                subsamp = self.get_samples( name=subsampname )[0]
                if subsamp.failed_draw :
                    sample.failed_draw=True


            self.group_sample( sample, isModel=ismodel )

            return True

        else :
            if sample.chain is not None :
                if not self.quiet or sample.isData: print 'Creating hist for %s  %s : ' %(sample.name, varexp) + tRed %selection
                #self.draw_hist( sample, varexp, histname, full_selection, draw_opt='goff' )
                res = sample.chain.Draw(varexp + ' >> ' + histname, full_selection, 'goff' )
                if res < 0 :
                    sample.failed_draw=True
                else :
                    sample.failed_draw=False
            else :
                sample.failed_draw=True

            if sample.hist is not None :
                if overflow: self.AddOverflow( sample.hist )
                sample.SetHist()

            return True

        # Group draw parallelization
        # wait for draws to finish
        #self.wait_on_draws()


    #--------------------------------

    def create_count( self, sample = None, counter = None, onthefly = True) :
        print "create count", sample

        if isinstance( sample, str) :
            slist = self.get_samples( name=sample )
            if not slist :
                print 'Could not retrieve sample, %s' %sample
            if len(slist) > 1 :
                print 'Located multiple samples with name %s' %sample
            sample = slist[0]

        if sample.IsGroupedSample() :
            for subsampname in sample.groupedSampleNames :
                subsamp = self.get_samples( name=subsampname )[0]

                if not self.quiet : print 'Counting grouped sample %s' %subsampname
                if subsampname in self.get_sample_names() :
                    self.create_count( subsamp, counter, onthefly )

            self.group_sample_count( sample )

            return

        else :
            ## calculate the appropriate scaling
            if onthefly and not (sample.isData or sample.IsGroupedSample()\
                   or sample.name == _STACKNAME or sample.isRatio==True):
                scale = sample.scale_calc()
            else: scale = sample.scale
            ## retrieve the dataframe object by Sample
            #count = counter.sampleptr[sample].GetValue()
            scounter = counter.sampleptr[sample]
            if isinstance(scounter, tuple):
                count = scounter[0].GetValue()
                errsq = scounter[1].GetValue()
            else:
                count = scounter.GetValue()
                errsq = count
            sample.count = ufloat(count * scale, math.sqrt(errsq)*scale)


    #--------------------------------

    def create_hist_new( self, draw_config, sample=None, isModel=False ) :
        """ Used by Draw(). Use draw_config instead of the old version . BookMarker -- Yihui"""

        if sample is None :
            sample = draw_config.samples[0]

        if isinstance( sample, str) :
            slist = self.get_samples( name=sample )
            if not slist :
                print 'Could not retrieve sample, %s' %sample
            if len(slist) > 1 :
                print 'Located multiple samples with name %s' %sample
            sample = slist[0]



        selection   = draw_config.get_selection_string( sample.name )
        varexp      = draw_config.var[0]
        usedataframe = isinstance(varexp, SampleFrame)
        sblind      = draw_config.get_unblind()
        sweight     = draw_config.get_weight()
        overflow    = draw_config.get_overflow()
        bywidth     = draw_config.get_bywidth()
        onthefly    = draw_config.get_onthefly()
        #sample.hist = draw_config.init_hist(sample.name)

        if usedataframe:
            sample.hist = None

        else: 
            # Here is where the hist binning initialized  -- Yihui
            sample.hist = self.parsehist(draw_config.histpars, varexp)  
            if sample.hist is not None :
                sample.hist.SetTitle( sample.name )
                #sample.hist.SetName( sample.name.replace('-','') )
                sample.hist.Sumw2()
            if sample.isData and isinstance(sblind,str):
                    selection = "(%s)&&(%s)" %(selection,sblind)

            if isinstance(sweight,str) and sweight and not sample.isData:
                    selection = "(%s)*%s" %(selection,sweight)

            # enable branches for variables matched in the varexp and selection
            sample.enable_parsed_branches( varexp+selection )
        print(self.curr_stack)
        if sample.IsGroupedSample() :

            for subsampname in sample.groupedSampleNames :

                subsamp = self.get_samples( name=subsampname )[0]

                if not self.quiet : print 'Draw grouped hist %s' %subsampname

                if isModel and subsampname in \
                        [s.name for s in self.get_model_samples()] :
                    self.create_hist_new( draw_config, subsamp, isModel=isModel )
                elif subsampname in self.get_sample_names() :
                    self.create_hist_new( draw_config, subsamp, isModel=isModel )

            sample.failed_draw=False
            for subsampname in sample.groupedSampleNames :
                subsamp = self.get_samples( name=subsampname )[0]
                if subsamp.failed_draw :
                    sample.failed_draw=True


            self.group_sample( sample, isModel=isModel )
            ## no need to rescale by width if it is a grouped sample
            sample.InitHist( onthefly )

            return

        else :
            start = time.time()
            if usedataframe:
                sample.hist = varexp.sampleptr[sample].GetValue().Clone()
            elif sample.chain is not None:

                if sample.chain.GetEntries() == 0:
                   print tRed%('WARNING: No entries from sample '+sample.name)

                if not self.quiet or sample.isData:
                    print 'Make %s hist %s : ' %(sample.name, varexp) \
                            + tRed %selection

                dataframefailed=False
                # Speed up with RDataFrame
                if self.dataFrame:
                    try:

                        rdf_hist_resultptr = self. create_hist_rdfhelper( sample,
                                        varexp, selection, draw_config.histpars)
                        rdf_hist = rdf_hist_resultptr.DrawCopy()

                        # save histogram to current sampleframe
                        if self.curr_sampleframe and rdf_hist_resultptr:
                            self.curr_sampleframe.sampleptr[sample] = \
                                                        rdf_hist_resultptr

                        res = sample.hist.Add(rdf_hist)

                    ## you don't want to catch keyboard interrupt here
                    except KeyboardInterrupt as ex:
                            raise ex

                    except Exception as ex:
                        print('Falling back to TChain. '\
                     'Please consider switching to ROOT >= 6.18 to use RDataFrame')
                        dataframefailed=True

                if not self.dataFrame or dataframefailed:
                    drawstr = varexp + ' >> ' + sample.hist.GetName()
                    #print('drawstr, selection', drawstr, selection)
                    #Yihui --- unblind error
                    res = sample.chain.Draw( drawstr, selection , '' )
                    #res = sample.chain.Draw( drawstr, selection , 'goff' )

                if res < 0 :
                    sample.failed_draw=True
                    print('WARNING: failed_draw, '\
                            'unexpected result for sample %s' % sample.name)

                else :
                    sample.failed_draw=False

            else :
                sample.failed_draw=True
                print('WARNING: failed_draw, '\
                        'TChain for sample %s is None' % sample.name)

            self.quietprint("time (s): %g " %(time.time()-start) )

            if sample.hist is not None :
                if overflow:
                    if bywidth:
                        mesg = "no overflow bin when normalized by binwidth"
                        self.quietprint( mesg )
                    else:
                        self.AddOverflow( sample.hist )
                ## set histogram style, scale
                sample.InitHist( onthefly, bywidth )

        # Group draw parallelization
        # wait for draws to finish
        #self.wait_on_draws()



    #--------------------------------


    def create_hist_rdfhelper( self, sample, varexp, selection, histpars ):

        rdf = ROOT.RDataFrame(sample.chain)
        rdf = rdf.Define('varexp', varexp)
        rdf = rdf.Define('selection', selection)

        ht = self.parsehist( histpars, varexp, 'rdf_hist',
                             returnmodel = True )
        rdf_hist_resultptr = rdf.Histo1D( ht , 'varexp', 'selection')

        return rdf_hist_resultptr


    #--------------------------------

    def format_hist( self, sample ) :
        self.AddOverflow( sample.hist )
        sample.SetHist()


    #--------------------------------

    def AddOverflow(self,  hist ) :

        # account for overflow and underflow
        # go 3-2-1 because TH3 inherits from TH2 etc..
        if isinstance( hist, ROOT.TH3 ) :
            nbinsx = hist.GetNbinsX()
            nbinsy = hist.GetNbinsY()
            nbinsz = hist.GetNbinsZ()

            #print 'Content before'
            #sum = 0
            #for xbin in range( 0, nbinsx+2 ) :
            #    for ybin in range( 0, nbinsy+2 ) :
            #        for zbin in range( 0, nbinsz+2 ) :
            #            sum += hist.GetBinContent( xbin, ybin, zbin )
            #            print 'Content (%d, %d, %d) = %d' %( xbin, ybin, zbin, hist.GetBinContent( xbin, ybin, zbin ) )
            #print 'SUM = ', sum
            for xbin in range( 1, nbinsx+1 ) :
                for ybin in range( 1, nbinsy+1 ) :
                    for zbin in range( 1, nbinsz+1 ) :
                        if xbin == 1 or xbin == nbinsx or ybin == 1 or ybin == nbinsy or zbin == 1 or zbin == nbinsz  :
                            # only combine on edge bins

                            bin = [ xbin, ybin, zbin ]

                            all_mod_bins = {}
                            # get singly modified bins (TH1, TH2, TH3)
                            self.get_single_mod_bins( bin, all_mod_bins )
                            # get doubly modified bins (TH2, TH3)
                            self.get_multi_mod_bins( bin, all_mod_bins )
                            # get triply modified bins (TH3)
                            self.get_multi_mod_bins( bin, all_mod_bins )

                            #get the full list of bins that are overflow
                            all_bins = []
                            #print all_mod_bins
                            for vals in all_mod_bins.values() :
                                for val in vals :
                                    if ( (val[0]==nbinsx+1 or val[0]==0 or val[0]==xbin) and
                                         (val[1]==nbinsy+1 or val[1]==0 or val[1]==ybin) and
                                         (val[2]==nbinsz+1 or val[2]==0 or val[2]==zbin) ) :
                                        all_bins.append(val)

                            # unique the list
                            unique_bins = [list(x) for x in set( tuple(x)  for x in all_bins) ]

                            for ovbin in unique_bins :
                                #print 'Combine bin %s with bin %s' %( str(bin), str(ovbin) )
                                self.combine_overflow_bin( hist, bin, ovbin )
            #print 'Content after'
            #sum = 0
            #for xbin in range( 0, nbinsx+2 ) :
            #    for ybin in range( 0, nbinsy+2 ) :
            #        for zbin in range( 0, nbinsz+2 ) :
            #            sum += hist.GetBinContent( xbin, ybin, zbin )
            #            print 'Content (%d, %d, %d) = %d' %( xbin, ybin, zbin, hist.GetBinContent( xbin, ybin, zbin ) )
            #print 'SUM = ', sum

        elif isinstance( hist, ROOT.TH2 ) :

            nbinsx = hist.GetNbinsX()
            nbinsy = hist.GetNbinsY()
            #print 'Content before'
            #sum = 0
            #for xbin in range( 0, nbinsx+2 ) :
            #    for ybin in range( 0, nbinsy+2 ) :
            #        sum += hist.GetBinContent( xbin, ybin )
            #        print 'Content (%d, %d ) = %d' %( xbin, ybin,  hist.GetBinContent( xbin, ybin ) )
            #print 'SUM = ', sum

            for xbin in range( 1, nbinsx+1 ) :
                for ybin in range( 1, nbinsy+1 ) :
                    if xbin == 1 or xbin == nbinsx  or ybin == 1 or ybin == nbinsy :
                        bin = [ xbin, ybin ]

                        all_mod_bins = {}
                        # get singly modified bins (TH1, TH2, TH3)
                        self.get_single_mod_bins( bin, all_mod_bins )
                        # get doubly modified bins (TH2, TH3)
                        self.get_multi_mod_bins( bin, all_mod_bins )

                        #print all_mod_bins

                        #get the full list of bins that are overflow
                        all_bins = []
                        for vals in all_mod_bins.values() :
                            for val in vals :
                                if ( (val[0]==nbinsx+1 or val[0]==0 or val[0]==xbin) and
                                    (val[1]==nbinsy+1 or val[1]==0 or val[1]==ybin) ) :
                                    all_bins.append(val)

                        # unique the list
                        unique_bins = [list(x) for x in set( tuple(x)  for x in all_bins) ]

                        for ovbin in unique_bins :
                            self.combine_overflow_bin( hist, bin, ovbin )

            #print 'Content after'
            #sum = 0
            #for xbin in range( 0, nbinsx+2 ) :
            #    for ybin in range( 0, nbinsy+2 ) :
            #        sum += hist.GetBinContent( xbin, ybin )
            #        print 'Content (%d, %d) = %d' %( xbin, ybin,  hist.GetBinContent( xbin, ybin ) )
            #print 'SUM = ', sum
        elif isinstance( hist, ROOT.TH1 ) :

            nbinsx = hist.GetNbinsX()
            #overflow
            self.combine_overflow_bin( hist, nbinsx, nbinsx+1 )
            #underflow
            self.combine_overflow_bin( hist, 1, 0 )



    #--------------------------------

    def get_single_mod_bins( self, bin, bin_collection ) :
        # for each entry in the bin,
        # make a modified bin
        # for that value up and that value down
        for binentry in range(0, len( bin ) ):
            binup = list(bin)
            binup [binentry]+=1
            bindn = list(bin)
            bindn [binentry]-=1
            bin_collection.setdefault( (binentry,), []).append(binup)
            bin_collection.setdefault( (binentry,), []).append(bindn)


    #--------------------------------

    def get_multi_mod_bins( self, bin, bin_collection ) :
        if not bin_collection :
            print 'Must have already defined bins to run multi'
            return

        # loop over the already defined bins
        for modbinval in bin_collection.keys() :
            modbins = bin_collection[modbinval]
            # grab entries that have fewer than the number of axes modified
            if len(modbinval) < len(bin) :
                for modbin in modbins :
                    # get an entry that was not modified before
                    # and modify it
                    for binentry in range(0, len( bin ) ) :
                        if binentry in modbinval :
                            continue
                        binup = list( modbin )
                        binup[binentry]+=1
                        bindn = list( modbin )
                        bindn[binentry]-=1
                        bin_collection.setdefault( modbinval+(binentry,), []).append(binup)
                        bin_collection.setdefault( modbinval+(binentry,), []).append(bindn)



    #--------------------------------

    def combine_overflow_bin( self, hist, bin, overbin ) :

        if not isinstance( overbin, tuple ) :
            if isinstance( overbin, list ) :
                overbin = tuple( overbin )
            else :
                overbin = (overbin,)
        if not isinstance( bin, tuple ) :
            if isinstance( bin, list) :
                bin = tuple( bin )
            else :
                bin = (bin,)

        over_val = hist.GetBinContent( *overbin )

        if over_val != 0 :

            orig_val = hist.GetBinContent( *bin )
            orig_err = hist.GetBinError( *bin )
            over_err = hist.GetBinError( *overbin )

            new_val = orig_val + over_val

            if orig_val == 0 :
                new_err = over_err
            else :
                new_err = math.sqrt( orig_err*orig_err + over_err*over_err )

            hist.SetBinContent( *( bin + (new_val,) ) )
            hist.SetBinError( *( bin + (new_err,) ) )
            hist.SetBinContent( *( overbin + (0,) ) )
            hist.SetBinError( *( overbin + (0,) ) )


    def get_active_samples( self, histpath ) :
        """
        calls get_hist to obtain histograms: may be updated in near future
        """

        for sample in self.samples :
            if sample.isActive :
                self.get_hist( sample, histpath )

    def draw_active_samples( self, draw_config ) :

        failed_samples = []
        success_samples = []
        for sample in self.samples :

            # skip blinded data
            if sample.isData:
                if not draw_config.get_unblind() :
                    continue

            # skip signal if requested
            if sample.isSignal:
                if not draw_config.get_drawsignal():
                    continue

            if sample.isActive :
                self.create_hist_new( draw_config, sample )
                if sample.failed_draw :
                    failed_samples.append( sample.name )
                else :
                    success_samples.append( sample.name )
                    #print "Sample : %s; Total Events: %f"%(sample.name, sample.hist.Integral())
                    #print "Histogram min: %d max :%d"%(sample.hist.GetBinLowEdge(1), sample.hist.GetXaxis().GetBinUpEdge( sample.hist.GetNbinsX() ))
                    #print "first bin: %d %d content %d"%(sample.hist.GetBinLowEdge(1), sample.hist.GetXaxis().GetBinUpEdge(1), sample.hist.GetBinContent(1))

        for samp in failed_samples :
            print 'Failed to draw sample %s' %samp

        if not success_samples :
            return False

        return True



    #--------------------------------

    def variable_rebinning(self, threshold=None, binning=None, samples=[], useStoredBinning=False) :

        if not samples:
            samples = self.get_samples(name=self.get_stack_order())

        # variable r
        if binning is not None :
            for samp in self.get_samples() :
                if samp.hist is not None :
                    samp.SetHist(self.do_variable_rebinning(samp, binning))
            return

        elif threshold is not None :

            if useStoredBinning :
                binning = self.binning
            else :
                all_stack_hists = []
                for samp in samples :
                    all_stack_hists.append(samp.hist)

                binning = self.make_variable_binning( all_stack_hists, threshold)

                # store binning for future use
                self.binning = binning

            for samp in self.get_samples() :
                if samp.hist is not None :
                    samp.SetHist(self.do_variable_rebinning(samp, binning))
            return

        else :
            print 'variable_rebinning : Must provide a rebinning threshold, or a binning scheme'
            return



    #--------------------------------

    def group_sample_count(self, sample) :

        if not sample.IsGroupedSample() :
            print 'Trying to group a sample that is not a grouped sample'
            return

        subsamp_names = sample.groupedSampleNames
        if not self.quiet : print 'RUN GROUPING FOR %s' %sample.name
        if not self.quiet : print subsamp_names

        subsamps = self.get_samples(name=subsamp_names)

        for samp in subsamps :
            if samp.IsGroupedSample() :
                self.group_sample_count( samp )

        sample.count = sum([s.count for s in subsamps if s.count is not None])* sample.scale

    #--------------------------------

    def group_sample(self, sample, isModel=False) :

        if not sample.IsGroupedSample() :
            print 'Trying to group a sample that is not a grouped sample'
            return

        subsamp_names = sample.groupedSampleNames
        if not self.quiet : print 'RUN GROUPING FOR %s' %sample.name
        if not self.quiet : print subsamp_names

        if isModel :
            model_subsamps = self.get_model_samples(subsamp_names)
            sample.hist = model_subsamps[0].hist.Clone()
            for msamp in model_subsamps[1:] :

                if sample.averageSamples :
                    self.addHistsWeightedAvg( sample.hist, samp.hist )

                sample.hist.Add( msamp.hist )
                sample.hist.Draw()
            #sample.hist.Scale(sample.scale)
            #self.modelSamples.append(sample)
        else :
            subsamps = self.get_samples(name=subsamp_names)

            for samp in subsamps :
                if samp.IsGroupedSample() :
                    self.group_sample( samp, isModel=False )

            valid_samps = [s for s in subsamps if s.hist is not None]

            sample.hist = valid_samps[0].hist.Clone()
            for samp in valid_samps[1:] :

                if sample.averageSamples :
                    self.addHistsWeightedAvg( sample.hist, samp.hist )

                sample.hist.Add( samp.hist )
                #sample.hist.Draw()
            #sample.hist.Scale(sample.scale)

        #sample.InitHist()


    #--------------------------------

    def get_list_from_tree(self, vars, selection, sample ) :

        output = []

        if not isinstance( vars, list ) :
            vars = [vars]

        if sample.IsGroupedSample() :
            for subsampname in sample.groupedSampleNames :
                subsamp = self.get_samples( name=subsampname )[0]

                if not self.quiet : print 'running on grouped hist %s' %subsampname

                if subsampname in self.get_sample_names() :
                    output += self.get_list_from_tree( vars, selection, subsamp )

            return output

        else :

            sample.copied_tree = sample.chain.CopyTree( selection )

            nentries = sample.copied_tree.GetEntries()

            for i in xrange( 0, nentries ) :
                sample.copied_tree.GetEntry( i )
                evt_entries = []
                for var in vars :

                    newvar = var
                    #if an index is requested, get the name and index separately
                    res = re.match( '(\w+)\[(\d)\]', var )
                    if res is not None :
                        newvar = res.group(1)
                        idx = int(res.group(2) )
                        vec = getattr( sample.copied_tree, newvar )
                        evt_entries.append( vec[idx] )
                    else :
                        evt_entries.append( getattr( sample.copied_tree, var ) )

                evt_entries.append( sample.scale )

                output.append( tuple( evt_entries ) )

        return output

#### formatter and canvas makers ####


    #--------------------------------

    def set_canvas_default_formatting(self, topcan, doratio, logy=False, ylabel=None, ymin=None, ymax=None ) :

        for prim in topcan.GetListOfPrimitives() :
            if isinstance(prim, ROOT.TH1F) :
                if ymin is not None and ymax is not None :
                    print "set_canvas_default_formatting:SetRangeUser ",ymin, ymax
                    prim.GetYaxis().SetRangeUser( ymin, ymax )
                prim.SetTitle('')
                offset = 1.15
                if logy :
                    offset = 1.1
                if doratio == True or doratio == 1 : # canvas sizes differ for ratio, so title, label sizes are different
                    prim.GetYaxis().SetTitleSize(0.06)
                    prim.GetYaxis().SetTitleOffset(offset)
                    prim.GetYaxis().SetLabelSize(0.06)
                    prim.GetXaxis().SetLabelSize(0.0)
                    prim.GetXaxis().SetTitleSize(0.0)
                elif doratio == 2 :
                    prim.GetYaxis().SetTitleSize(0.06)
                    prim.GetYaxis().SetTitleOffset(offset)
                    prim.GetYaxis().SetLabelSize(0.06)
                    prim.GetXaxis().SetLabelSize(0.06)
                    prim.GetXaxis().SetTitleSize(0.06)
                else :
                    prim.GetYaxis().SetTitleSize(0.030)
                    prim.GetYaxis().SetTitleOffset( offset + .5)
                    prim.GetYaxis().SetLabelSize(0.015)
                    prim.GetXaxis().SetLabelSize(0.04)
                    prim.GetXaxis().SetTitleSize(0.04)


    #--------------------------------

    def set_stack_default_formatting(self, topcan, doratio, logy=False ) :
        if topcan.GetHists() != None :
            if topcan.GetHists().GetSize() > 0 :
                if isinstance(topcan.GetHists()[0],ROOT.TH2):
                    return
                offset = 1.15
                if logy :
                    offset = 1.1
                if doratio : # canvas sizes differ for ratio, so title, label sizes are different
                    topcan.GetHistogram().GetYaxis().SetTitleSize(0.06)
                    topcan.GetHistogram().GetYaxis().SetTitleOffset(offset)
                    topcan.GetHistogram().GetYaxis().SetLabelSize(0.06)
                    topcan.GetHistogram().GetXaxis().SetLabelSize(0.0)
                    topcan.GetHistogram().GetXaxis().SetTitleSize(0.0)
                    topcan.GetHistogram().GetXaxis().SetTitleOffset(1.1)
                else :
                    topcan.GetHistogram().GetYaxis().SetTitleSize(0.045)
                    topcan.GetHistogram().GetYaxis().SetTitleOffset(0.9)
                    topcan.GetHistogram().GetYaxis().SetLabelSize(0.04)
                    topcan.GetHistogram().GetXaxis().SetLabelSize(0.04)
                    topcan.GetHistogram().GetXaxis().SetTitleSize(0.045)


    #--------------------------------

    def set_ratio_default_formatting(self, canvas, ratiosamps, draw_config ) :

            canvas.cd()

            doratio = draw_config.get_doratio()
            rlabel = draw_config.get_rlabel()
            rmin   = draw_config.get_rmin()
            rmax   = draw_config.get_rmax()



            for idx, ratiosamp in enumerate( ratiosamps ) :
                drawopt = 'same'
                if idx == 0 :
                    drawopt = ''
                if ratiosamp.isSignal :
                    drawopt += 'HIST'

                ratiosamp.hist.SetLineWidth(2)
                if   doratio == True or doratio == 1 :
                    ratiosamp.hist.GetYaxis().SetTitleSize(0.1)
                    ratiosamp.hist.GetYaxis().SetTitleOffset(0.5)
                    ratiosamp.hist.GetYaxis().SetLabelSize(0.08)
                    ratiosamp.hist.GetXaxis().SetLabelSize(0.08)
                    ratiosamp.hist.GetXaxis().SetTitleSize(0.08)
                    ratiosamp.hist.GetXaxis().SetTitleOffset(1.1)
                elif doratio: #doratio==2 :
                    ratiosamp.hist.GetYaxis().SetTitleSize(0.06)
                    ratiosamp.hist.GetYaxis().SetTitleOffset(0.8)
                    ratiosamp.hist.GetYaxis().SetLabelSize(0.06)
                    ratiosamp.hist.GetXaxis().SetLabelSize(0.06)
                    ratiosamp.hist.GetXaxis().SetTitleSize(0.06)
                    ratiosamp.hist.GetXaxis().SetTitleOffset(1.0)

                ratiosamp.hist.SetStats(0)
                ratiosamp.hist.SetMarkerStyle(1)
                ratiosamp.hist.SetMarkerSize(0.1)
                ratiosamp.hist.SetTitle('')
                ratiosamp.hist.GetYaxis().CenterTitle()
                #ratiosamp.hist.GetYaxis().SetNdivisions(506, True)
                ratiosamp.hist.GetYaxis().SetNdivisions(506)
                #ratiosamp.hist.GetYaxis().SetNdivisions(8)
                if rlabel is not None :
                    ratiosamp.hist.GetYaxis().SetTitle(rlabel)
                if rmin is not None and rmax is not None :
                    ratiosamp.hist.GetYaxis().SetRangeUser(rmin, rmax)

            #left_edge  = ratiosamps[0].hist.GetXaxis().GetXmin()
            #right_edge = ratiosamps[0].hist.GetXaxis().GetXmax()

            #canvas.cd()

            #oneline = ROOT.TLine(left_edge, 1, right_edge, 1)
            #oneline.SetLineStyle(3)
            #oneline.SetLineWidth(2)
            #oneline.SetLineColor(ROOT.kBlack)
            #oneline.Draw()
            #self.add_decoration(oneline)


    #--------------------------------

    @f_Dumpfname
    def calc_yaxis_limits(self, draw_config, samplist = None) :

        ymindef     = draw_config.get_ymin()
        ymaxdef     = draw_config.get_ymax()
        ymax_scale  = draw_config.get_ymax_scale()
        logy        = draw_config.get_logy()
        normalize = draw_config.get_normalize()

        if not samplist: samplist = self.get_samples()
        #if not normalize: samplist+=self.get_samples( name='__AllStack__' )

        return self.calc_yranges(samplist, ymindef, ymaxdef,
                                  ymax_scale, logy, normalize)

    def calc_yranges( self, samplist, ymindef = None, ymaxdef = None,
                            ymax_scale = 1.2, logy = False, normalize = False ):
        """ Calculate y axis ranges """

        ymin,ymax   = ymindef, ymaxdef
        maxarray, minarray = [], []

        if ymaxdef is None :

            #if normalize == "Total":
            #    maxarray =[samp.hist.GetMaximum()/samp.hist.GetBinContent(1) \
            #                    for samp in samplist \
            #                    if samp.hist and samp.hist.GetBinContent(1)>0]

            #elif normalize and not (isinstance(normalize,str) and "Width" in normalize):
            #    ## FIXME separate width from normalize
            #    maxarray =[samp.hist.GetMaximum()/samp.hist.Integral() \
            #                    for samp in samplist \
            #                    if samp.hist and samp.hist.Integral()>0]
            #elif isinstance(normalize,str) and "Width" in normalize:
            #    ## FIXME separate width from normalize
            #    maxarray =[samp.hist.GetMaximum()/samp.hist.Integral() \
            #                    for samp in samplist \
            #                    if samp.hist and samp.hist.Integral()>0]
            #else:
            maxarray =[samp.hist.GetMaximum()
                        for samp in samplist if samp.hist]

            ymax = max(maxarray)

        if ymindef is None :

            #if normalize == "Total":
            #    minarray =[samp.hist.GetMinimum(0)/samp.hist.GetBinContent(1) \
            #                    for samp in samplist\
            #                    if samp.hist and samp.hist.GetBinContent(1)>0]

            #elif normalize and normalize != "Width":
            #    minarray =[samp.hist.GetMinimum(0)/samp.hist.Integral() \
            #                    for samp in samplist \
            #                    if samp.hist and samp.hist.Integral()>0]

            #else:
            minarray =[samp.hist.GetMinimum(0) \
                        for samp in samplist if samp.hist]

            ymin = min(minarray)

        if ymax_scale is None :
            ymax_scale = 1.2

        # scale ymax, only if default is not given
        if ymin is not None and ymax is not None:
            if logy:

                # log scale only makes sense with positive numbers
                if ymax<=0:
                    ymax=None
                if ymin<=0:
                    ymin=None

                if not ymaxdef and ymax: ymax *= pow(ymax/ymin,ymax_scale-1)
                if not ymindef and ymin and ymax: ymin *= pow(ymax/ymin,0.9-1)

            else :

                if not ymaxdef: ymax += (ymax-ymin)*(ymax_scale-1)
        print ymax_scale, ymax, ymin, maxarray, minarray

        return (ymin, ymax)


    #--------------------------------

    def create_standard_canvas(self, name='base') :
        """create_standard_canvas"""

        self.curr_canvases[name] = ROOT.TCanvas(name, name, self.XSIZE, self.YSIZE)

        self.curr_canvases['top'] = self.curr_canvases[name]
        self.curr_canvases[name].SetTopMargin(0.08)
        self.curr_canvases[name].SetBottomMargin(0.13)
        self.curr_canvases[name].SetLeftMargin(0.15)
        self.curr_canvases[name].SetRightMargin(0.05)
        self.curr_canvases[name].SetTitle('')


    #--------------------------------

    def create_standard_ratio_canvas(self) :

        xsize = 800
        ysize = 1000
        self.curr_canvases['base'] = ROOT.TCanvas('basecan', 'basecan', xsize, ysize)

        self.curr_canvases['bottom'] = ROOT.TPad('bottompad', 'bottompad', 0.01, 0.01, 0.99, 0.34)
        self.curr_canvases['top'] = ROOT.TPad('toppad', 'toppad', 0.01, 0.35, 0.99, 0.99)
        self.curr_canvases['top'].SetTopMargin(0.08)
        #self.curr_canvases['top'].SetBottomMargin(0.06)
        self.curr_canvases['top'].SetBottomMargin(0.02)
        self.curr_canvases['top'].SetLeftMargin(0.15)
        self.curr_canvases['top'].SetRightMargin(0.05)
        self.curr_canvases['bottom'].SetTopMargin(0.05)
        #self.curr_canvases['bottom'].SetTopMargin(0.00)
        self.curr_canvases['bottom'].SetBottomMargin(0.3)
        self.curr_canvases['bottom'].SetLeftMargin(0.15)
        self.curr_canvases['bottom'].SetRightMargin(0.05)
        self.curr_canvases['base'].cd()
        self.curr_canvases['bottom'].Draw()
        self.curr_canvases['top'].Draw()


    #--------------------------------

    def create_large_ratio_canvas(self) :

        xsize = 600
        ysize = 850
        self.curr_canvases['base'] = ROOT.TCanvas('basecan', 'basecan', xsize, ysize)

        self.curr_canvases['bottom'] = ROOT.TPad('bottompad', 'bottompad', 0.01, 0.01, 0.99, 0.48)
        self.curr_canvases['top'] = ROOT.TPad('toppad', 'toppad', 0.01, 0.49, 0.99, 0.99)
        self.curr_canvases['top'].SetTopMargin(0.08)
        self.curr_canvases['top'].SetBottomMargin(0.02)
        self.curr_canvases['top'].SetLeftMargin(0.15)
        self.curr_canvases['top'].SetRightMargin(0.05)
        #self.curr_canvases['bottom'].SetTopMargin(0.05)
        self.curr_canvases['bottom'].SetTopMargin(0.03)  # non-zero to allow space for numbers on the axis that go above the plot
        self.curr_canvases['bottom'].SetBottomMargin(0.2)
        self.curr_canvases['bottom'].SetLeftMargin(0.15)
        self.curr_canvases['bottom'].SetRightMargin(0.05)
        self.curr_canvases['base'].cd()
        self.curr_canvases['bottom'].Draw()
        self.curr_canvases['top'].Draw()


    #--------------------------------

    def create_top_canvas_for_ratio(self, name='can') :

        xsize = 650
        ysize = 500
        self.curr_canvases[name] = ROOT.TCanvas(name, name, xsize, ysize)

        self.curr_canvases[name].SetTopMargin(0.08)
        self.curr_canvases[name].SetBottomMargin(0.08)
        self.curr_canvases[name].SetLeftMargin(0.15)
        self.curr_canvases[name].SetRightMargin(0.05)
        self.curr_canvases[name].SetTitle('')

#### stack utilities ####

    #--------------------------------

    def get_stack_pdf(self,method=1, bywidth = False):
        """ extract unit normalized pdf after Draw command """
        if method==1:
            samp= self.get_samples(name='__AllStack__')
            if not (samp and samp[0].hist):
                print "no stack saved"
                return
            h2 =samp[0].hist.Clone()
        if method==2:
            h2=self.get_stack_aggregate()
            if h2==None: return

        ## normalize according to method: width if content is scaled by bin
        if bywidth:
            h2.Scale(1./h2.Integral("width"))
        else:
            h2.Scale(1./h2.Integral())

        return h2


    #--------------------------------

    def get_stack_aggregate( self ):
        """ Get aggregate histogram from current stack """
        if hasattr(self,"curr_stack") and \
                 isinstance(self.curr_stack, ROOT.THStack):
            h1 = self.curr_stack.GetStack().Last().Clone()
            h1.SetMarkerStyle(15)
            h1.SetMarkerColor(1)
            h1.SetMarkerSize(.75)
            h1.SetLineWidth(2)
            h1.SetTitle('curr_stack')
            h1.SetName('curr_stack')
            xtitle = self.curr_stack.GetXaxis().GetTitle()
            ytitle = self.curr_stack.GetYaxis().GetTitle()
            h1.GetXaxis().SetTitle(xtitle)
            h1.GetYaxis().SetTitle(ytitle)
            return h1
        else:
            print "No stack found"
        return


    #--------------------------------

    def get_stack_count( self, integralrange = None, sort = True,
                     includeData = False, isActive = True, dolatex = False,
                     doacceptance = False, bywidth = False ):
        """ integralrange: ntuple: x bin range to be integrated """

        samplelist      = self.get_samples(isActive=isActive,isData=False)
        data_samplelist = self.get_samples(isActive=isActive,isData=True)

        option = "width" if bywidth else ""
        ## one line magic
        result = [ ( s.legendName if dolatex else s.name,
                   ( s.acceptance if doacceptance else s.integral )\
                                        ( integralrange, option ) )\
                    for s in samplelist if s.name != "ratio" and s.hist ]

        if sort: result.sort(key=lambda x: -x[1][0])
        #htotal = self.get_stack_aggregate()

        if includeData:
            result += [ (s.name, (s.acceptance if doacceptance else s.integral)\
                          ( integralrange, option ) ) for s in data_samplelist ]

        ## get stack sample
        stotal = self.get_samples( name = _STACKNAME )
        if len(stotal) > 1:
            print "WARNING dupilcate sample %s" %_STACKNAME

        if stotal and not doacceptance:
            result.append( ( "TOTAL", stotal[0].integral \
                                                ( integralrange, option ) ) )

        resultdict = OrderedDict(result)
        return resultdict


    #--------------------------------

    def latex_replacement(self, text):
        if "#" in text:
            text = "$%s$" %text
        return text.replace("#","\\")

    def print_stack_count(self, integralrange = None, dolatex=False, **kwargs):
        result = self.get_stack_count(integralrange, dolatex = dolatex,
                                                     **kwargs).items()
        if dolatex:
            #result = [ (r1,)+tuple(map(latex_float,r2)) for r1, r2 in result]
            #result = [ (r1.replace("gamma","\\gamma ").replace("Gamma","\\gamma ").replace("\\gamma$$\\gamma","\\gamma\\gamma"),
            #result = [ (r1.replace("#","\\"),
            result = [ (self.latex_replacement(r1),
                        latex_float(*r2)) for r1, r2 in result]
            printline = ""
            for r in result[:-1]: printline+= "%20s & %s\\\\\n" %r
            printline+= "\\hline\\hline\n%20s & %s\\\\\n" %result[-1]
            print printline
            return
        self.print_stackresult(result)
        return


    #--------------------------------

    def print_stackresult(self,result):
        if isinstance(result, dict):
            result = result.items()

        result = [ (r1,)+r2 for r1, r2 in result]
        totalresult = None
        if len(result)>1 and result[-1][0]=="TOTAL":
            totalresult = result[-1]
            result = result[:-1]
        for r in result: print "%30s %8.3g +/- %5.3g" %r
        if totalresult: print "="*45+"\n%30s %8.3g +/- %5.3g" %totalresult
        return


    #--------------------------------

    def DrawCanvas(self, topcan, draw_config,
                         datahists = [], sighists = [], errhists = [] ) :
        """
        Draw Data, Signal and legend. Called by SampleManager.Draw()  as
        well as CompareSelections()
        """

        datadrawn  = False # is data drawn?
        doratio=draw_config.get_doratio()
        if doratio == True or doratio == 1 or doratio == "dodiff":
            self.create_standard_ratio_canvas()
        elif doratio == 2 :
            self.create_large_ratio_canvas()
        else :
            self.create_standard_canvas()


        self.curr_canvases['top'].cd()

        ylabel = draw_config.get_ylabel()
        ticksx = draw_config.get_tick_x_format()
        ticksy = draw_config.get_tick_y_format()
        normalize = draw_config.get_normalize()
        bywidth = draw_config.get_bywidth()

        ## normalize signal if necessary
        if sighists and draw_config.get_drawsignal():
            for samp in sighists :
                if samp.isActive :
                    ## normalize signal samples
                    if samp.hist.Integral()==0:
                        break
                    if normalize == "Total":
                        samp.hist.Scale(1./samp.hist.GetBinContent(1))
                    elif normalize :
                        if bywidth:
                            samp.hist.Scale(1./samp.hist.Integral("width"))
                        else:
                            samp.hist.Scale(1./samp.hist.Integral())

        # in what cases is topcan an already filled TCanvas?
        # ratio plot from compareselections()

        if isinstance( topcan, ROOT.TCanvas ) :
            for prim in topcan.GetListOfPrimitives() :
                if isinstance(prim, ROOT.TH1F) :
                    if ylabel is not None :
                        prim.GetYaxis().SetTitle(ylabel)
                    if ticksx is not None :
                        prim.GetXaxis().SetNdivisions( *ticksx )
                    if ticksy is not None :
                        prim.GetYaxis().SetNdivisions( *ticksy )
            topcan.DrawClonePad()

        if isinstance( topcan, ROOT.THStack ) :
            drawopt = draw_config.get_drawopt()
            samplist = self.get_samples(isSignal=True,isActive=True)+\
                       self.get_samples(name="__AllStack__")+\
                       self.get_samples(isData=True,isActive=True)
            (ymin, ymax) = self.calc_yaxis_limits( draw_config, samplist)
            if topcan.GetHists() == None :
                print 'Top stack has no hists! Exiting'
                return
            topcan.Draw(drawopt)
            logy = draw_config.get_logy()
            if ymin and not (logy and ymin<=0):
                topcan.SetMinimum(ymin)
                print "SetMinimum ",ymin
            if ymax and not (logy and ymax<=0):
                topcan.SetMaximum(ymax)
                print "SetMaximum ",ymax
            self.set_stack_default_formatting( topcan, doratio, logy=logy)


        # draw the data
        for dsamp in self.get_samples( name=datahists, isActive=True ):
            if not draw_config.get_unblind() and dsamp.isData:
                    print "skipped ",dsamp
                    continue
            if normalize == "Total":
                # assume total is the first bin
                dsamp.hist.Scale(1./dsamp.hist.GetBinContent(1))
                dsamp.hist.Draw('PE same')
            elif normalize == "Width":
                ## should be the same as normal
                # dsamp.normalize_by_width() # not necessary
                dsamp.hist.Draw('PE same')
            elif normalize:
            #dsamp.hist.SetMarkerStyle(8)
                dsamp.hist.DrawNormalized('PE same')
            else :
                dsamp.hist.Draw('PE same')
            datadrawn = True


        # draw the signals
        legendTextSize = draw_config.legend_config.get('legendTextSize', 0.035 )
        #print legendTextSize
        if sighists and draw_config.get_drawsignal():
            #sigsamps = self.get_samples(name=sighists)
            for samp in sighists :
                #print samp.isActive
                if samp.isActive :

                    print 'Draw Signal hist ', samp.name
                    samp.hist.SetLineStyle(samp.getLineStyle())
                    samp.hist.SetStats(0)

                    ## draw signal
                    samp.hist.Draw('HIST same')

                    entry = self.curr_sig_legend.AddEntry( samp.hist,
                                                           samp.legendName, 'L')
                    entry.SetTextSize(legendTextSize)

        if errhists :
            errsamps = self.get_samples(name=errhists )
            for samp in errsamps :
                if not hasattr(samp,"graph") and hasattr(samp, "hist"):
                    samp.graph = ROOT.TGraphErrors(samp.hist)
                samp.graph.SetFillStyle(3004)
                samp.graph.SetFillColor(ROOT.kBlack)
                samp.graph.Draw('2same')

                entry = self.curr_legend.AddEntry( samp.graph,
                                                   'Stat. unc.', 'F')
                entry.SetTextSize(legendTextSize)


        if doratio :
            self.curr_canvases['bottom'].cd()
            ratiosamps =  self.get_samples( isRatio=True )
            self.set_ratio_default_formatting( self.curr_canvases['bottom'],
                                               ratiosamps, draw_config )

            drawoptbase = draw_config.get_drawopt()
            for idx, samp in enumerate(ratiosamps) :
                drawopt = 'same'
                if idx == 0 :
                    drawopt = ''
                if drawoptbase:
                    drawopt+=drawoptbase
                if samp.isSignal :
                    drawopt += 'HIST'

                samp.hist.Draw(drawopt)


        self.curr_canvases['top'].cd()

        # if topcan is None then a new
        # canvas has been created above
        # and the formatting should be set
        if topcan is None :
            self.set_canvas_default_formatting(self.curr_canvases['top'], doratio, logy=draw_config.get_logy(), ylabel=ylabel, ymin=ymin, ymax=ymax )

        # draw the legend
        if self.curr_legend is not None :
            self.curr_legend.Draw()

        if self.curr_sig_legend is not None and draw_config.get_drawsignal():
            self.curr_sig_legend.Draw()

        # draw the plot status label
        labels = draw_config.get_labels(datadrawn = datadrawn)
        for lab in labels :
            lab.Draw()
            self.curr_decorations.append( lab )

        if doratio :

            self.curr_canvases['bottom'].cd()

            left_edge  = ratiosamps[0].hist.GetXaxis().GetXmin()
            right_edge = ratiosamps[0].hist.GetXaxis().GetXmax()

            oneline = ROOT.TLine(left_edge, 1, right_edge, 1)
            oneline.SetLineStyle(3)
            oneline.SetLineWidth(2)
            oneline.SetLineColor(ROOT.kBlack)
            oneline.Draw()
            self.add_decoration(oneline)

        xlabel = draw_config.get_xlabel()
        if xlabel is not None :
            if doratio :
                ratiosamp = self.get_samples(isRatio=True)[0]
                ratiosamp.hist.GetXaxis().SetTitle(xlabel)
            else :
                if isinstance(topcan, ROOT.THStack ) :
                    topcan.GetHistogram().GetXaxis().SetTitle(xlabel)

                for samp in self.get_samples() :
                    if samp.hist :
                        samp.hist.GetXaxis().SetTitle(xlabel)

        if isinstance(topcan, ROOT.THStack ) :
            #print topcan.GetHistogram().GetNdivisions()
            #raw_input('cont')
            if ylabel is not None :
                topcan.GetHistogram().GetYaxis().SetTitle(ylabel)
            if ticksx is not None :
                topcan.GetHistogram().GetXaxis().SetNdivisions(ticksx[0], ticksx[1], ticksx[2],True)
            if ticksy is not None :
                topcan.GetHistogram().GetYaxis().SetNdivisions(ticksy[0], ticksy[1], ticksy[2], True)


            wh = self.curr_canvases['top'].GetWh()
            ww = self.curr_canvases['top'].GetWw()

            tl = 15.

            tick_frac_y = tl / ( ww )
            tick_frac_x = tl / ( wh )


            topcan.GetHistogram().GetXaxis().SetTickLength(tick_frac_x)
            topcan.GetHistogram().GetYaxis().SetTickLength(tick_frac_y)

        if draw_config.get_logy():
            self.curr_canvases['top'].SetLogy()


    #--------------------------------

    def DrawSameCanvas(self, canvas, samples, draw_config, drawHist=False ) :
        """  
            Called by CompareSelections, CompareHists
        """

        canvas.cd()

        if not drawHist :
            drawHist = [0]*len(samples)

        ymin = draw_config.get_ymin()
        ymax = draw_config.get_ymax()
        ymax_scale = draw_config.get_ymax_scale()
        normalize = draw_config.get_normalize()
        bywidth = draw_config.get_bywidth()
        drawopt = draw_config.get_drawopt()
        drawhist = draw_config.get_drawhist()


        first = True
        draw_samps_list = []
        for hist_name, hist_config in draw_config.hist_configs.iteritems() :

            draw_samp = self.get_samples( name=hist_config['sample']+"_"+hist_name  )
            if draw_samp :
                draw_samp = draw_samp[0]
            else :
                draw_samp = None
                print 'WARNING Did not get a sample associated with the hist_config'
                raise RuntimeError
            draw_samps_list.append(draw_samp)

            ## perform normalization
            if bywidth:
                draw_samp.normalize_by_width()
                integral = draw_samp.hist.Integral("width")
            else:
                integral = draw_samp.hist.Integral()

            if normalize == "Total" and draw_samp.hist.GetBinContent(1) :
                draw_samp.hist.Scale(1.0/draw_samp.hist.GetBinContent(1))
            elif normalize and integral!=0:
                draw_samp.hist.Scale(1.0/integral)
            draw_samp.hist.SetLineColor( hist_config['color'] )
            draw_samp.color =  hist_config['color'] 
            if "e2" in drawopt: 
                draw_samp.hist.SetFillColor(hist_config['color'])
                draw_samp.hist.SetFillStyle(3018)
            draw_samp.hist.SetMarkerColor(hist_config['color'])
            draw_samp.hist.GetYaxis().SetTitleOffset(1.1)
            draw_samp.hist.GetYaxis().SetTitleSize(0.045)
            draw_samp.hist.GetYaxis().SetLabelSize(0.03)
            draw_samp.hist.SetLineWidth( 2 )
            draw_samp.hist.SetMarkerSize( 0 )
            if "text" in drawopt: draw_samp.hist.SetMarkerSize( 1 ) ## font size for histogram text option
            draw_samp.hist.SetMarkerStyle( 7 )
            draw_samp.hist.SetStats(0)
            if draw_samp.isSignal  :
                draw_samp.hist.SetMarkerSize( 1 )
                draw_samp.hist.SetMarkerStyle(20)

        samplist = self.get_samples(temporary=True,isRatio=False)
        assert set(samplist)==set(draw_samps_list)
        ## calculate proper y axis limits after all normalization is done
        ymin, ymax = self.calc_yaxis_limits( draw_config , samplist )

        for draw_samp in draw_samps_list:
            drawcmd = drawopt+' same'
            if first :
                drawcmd = drawopt
                first = False
            if not draw_samp.isSignal and drawhist:
                drawcmd+='hist'

            draw_samp.hist.GetYaxis().SetTitle( draw_config.get_ylabel() )
            if not draw_config.get_doratio()  :
                draw_samp.hist.GetXaxis().SetTitle( draw_config.get_xlabel() )


            if ymin is not None and ymax is not None and ymin < ymax :
                print "set %s histogram y range: %g, %g" %(draw_samp.name, ymin, ymax)
                draw_samp.hist.GetYaxis().SetRangeUser(ymin, ymax)
            else:
                print "warning: %s histogram fail to set range "%draw_samp.name, ymin, ymax

            #draw_samp.hist.Draw(drawcmd+'goff')
            draw_samp.hist.Draw(drawcmd)



    #--------------------------------

    def CompareHists( self, histname, reqsamples, histpars, hist_config={}, label_config={}, legend_config={}, same=False, useModel=False, treeHist=None, treeSelection=None ) :
        """ provide hist name and compare histogram from TFiles; useful with cutflows """

        self.curr_sig_legend = None

        if 'colors' not in hist_config :
            hist_config['colors'] = _DEFAULTCOLORS[:len(reqsamples)]
        if len(hist_config['colors']) < len( reqsamples ) :
            print 'Size of colors input does not match size of vars input!'
            reqnum = len(hist_config['colors']) - len( reqsamples )
            hist_config['colors'].extend([ self.get_samples(name=s)[0].color
                                            for s in reqsamples[reqnum:] ])

        if not same :
            self.clear_all()

		# initialize DrawConfig
        config = DrawConfig( histname, selection=[" "]*len(reqsamples), histpars="", samples=reqsamples,
                      hist_config=hist_config, label_config=label_config, legend_config=legend_config )
        config.create_hist_configs()

        self.draw_commands.append(config)

        created_samples = self.MakeSameCanvas(config, preserve_hists=True, readhist=True )
        print created_samples
        if not created_samples :
            print 'No histograms were created'
            return

        # make the legend
        step = len(created_samples)
        self.curr_legend = self.create_standard_legend(step, draw_config=config )

        legend_entries = config.get_legend_entries()
        self.create_same_legend( legend_entries , created_samples )

        #self.DrawCanvas(self.curr_canvases['same'], ylabel=ylabel, xlabel=xlabel, rlabel=rlabel, doratio=doratio, labelStyle=labelStyle, rmin=rmin, rmax=rmax, ymax=ymax, ymin=ymin, logy=logy, extra_label=extra_label, extra_label_loc=extra_label_loc)
        self.DrawCanvas(self.curr_canvases['same'], config )





    #--------------------------------

    def CompareSelections( self, varexp, selections, reqsamples, histpars, hist_config={}, label_config={}, legend_config={}, same=False, useModel=False, treeHist=None, treeSelection=None ) :
        assert len(selections) == len(reqsamples), 'selections and samples must have same length'

        self.curr_sig_legend = None

        if 'colors' not in hist_config :
            hist_config['colors'] = _DEFAULTCOLORS[:len(reqsamples)]

        if len(hist_config['colors']) < len( reqsamples ) :
            print 'Size of colors input does not match size of vars input!'
            reqnum = len(hist_config['colors']) - len( reqsamples )
            hist_config['colors'].extend([ self.get_samples(name=s)[0].color
                                            for s in reqsamples[reqnum:] ])

        if self.collect_commands :
            self.add_compare_config( varexp, selections, reqsamples, histpars,
                       hist_config=hist_config, label_config=label_config, legend_config=legend_config)
            return

        if not same :
            self.clear_all()

		# initialize DrawConfig
        config = DrawConfig( varexp, selections, histpars, samples=reqsamples,
                      hist_config=hist_config, label_config=label_config, legend_config=legend_config )
        config.create_hist_configs()

        self.draw_commands.append(config)

        created_samples = self.MakeSameCanvas(config, preserve_hists=True, useModel=useModel, treeHist=treeHist, treeSelection=treeSelection )
        print created_samples
        if not created_samples :
            print 'No histograms were created'
            return

        # make the legend
        step = len(created_samples)
        self.curr_legend = self.create_standard_legend(step, draw_config=config )

        legend_entries = config.get_legend_entries()
        self.create_same_legend( legend_entries , created_samples )

        #self.DrawCanvas(self.curr_canvases['same'], ylabel=ylabel, xlabel=xlabel, rlabel=rlabel, doratio=doratio, labelStyle=labelStyle, rmin=rmin, rmax=rmax, ymax=ymax, ymin=ymin, logy=logy, extra_label=extra_label, extra_label_loc=extra_label_loc)
        self.DrawCanvas(self.curr_canvases['same'], config )


    #--------------------------------

    def create_same_legend(self,  legend_entries, created_samples ) :

        # check for an input legend_entries
        if not legend_entries:
            legend_entries = [s.legendName for s in created_samples]

        for idx, samp in enumerate(created_samples) :
            drawopt = 'PL'
            if samp.isSignal :
                drawopt = 'L'
            legname = legend_entries[idx]
            self.curr_legend.AddEntry(samp.hist, legname,  drawopt)
            self.curr_legend.SetMargin(0.2)


    #--------------------------------

    def Draw2D( self, varexp, selections, sample_names, histpars=None, drawopts='', xlabel=None, ylabel=None, logz = True) :

        self.clear_hists()

        if not isinstance(sample_names, list) :
            sample_names = [sample_names]
        if not isinstance(selections, list) :
            selections = [selections]

        if len(sample_names) != len(selections) :
            print 'Length of samples does not match length of selections'

        created_samples=[]
        for idx, (samp_name, selection) in enumerate(zip(sample_names, selections)) :

            if not self.get_samples(name=samp_name) :
                print 'No sample with name ', samp_name
            samp = self.get_samples(name=samp_name)[0]
            newname = '%s_%d' %(samp.name, idx)
            newsamp = self.clone_sample( oldname=samp.name, newname=newname, temporary=True )
            newsamp.hist = None

            self.create_hist( newsamp, varexp, selection, histpars)

            if xlabel is None :
                xlabel = varexp.split(":")[1]
            newsamp.hist.GetXaxis().SetTitle( xlabel )
            if ylabel is None :
                ylabel = varexp.split(":")[0]
            newsamp.hist.GetYaxis().SetTitle( ylabel )

            created_samples.append(newsamp)
            zmin, zmax = self.calc_yranges(created_samples, ymax_scale=1, logy=logz)

        for idx, samp in enumerate(created_samples) :

            self.curr_canvases['base%d'%idx] = ROOT.TCanvas('basecan%d'%idx, '', self.XSIZE, self.YSIZE)
            if logz: self.curr_canvases['base%d'%idx].SetLogz()
            self.curr_canvases['base%d'%idx].SetRightMargin(0.15)
            self.curr_canvases['base%d'%idx].cd()

            if zmin and zmax:
                samp.hist.GetZaxis().SetRangeUser(zmin,zmax) # same z scale to all 2D histograms
            samp.hist.Draw(drawopts)


    #--------------------------------

    def CompareVars( self, varexps, selections, sample_names, histpars=None, hist_config={}, label_config={}, legend_config={}, same=False ) :
        """ similar to CompareSelection """

        self.clear_all()

        if not isinstance( varexps, list ) : varexps = [varexps]
        if not isinstance( selections, list ) : selections= [selections]
        if not isinstance( sample_names, list ) : sample_names= [sample_names]

        if len(selections) < len(varexps) and len(selections)==1 :
            selections = [selections[0]]*len(varexps)


        if 'colors' in hist_config :
            if len(hist_config['colors']) != len( selections ) :
                print 'Size of colors input does not match size of vars input!'

                hist_config['colors'] = [ self.get_samples(name=s)[0].color for s in reqsamples ]

        config = DrawConfig( varexps, selections, histpars, samples=sample_names, hist_config=hist_config, label_config=label_config, legend_config=legend_config )
        config.create_hist_configs()
        self.draw_commands.append(config)

        created_samples = self.MakeSameCanvas(config, preserve_hists=True )
        if not created_samples :
            print 'No histograms were created'
            return

        #samples = []
        #for sn in sample_names :
        #    samples.append( self.get_samples( name=sn )[0] )

        #if len(samples) < len(varexps) and len(samples)==1 :
        #    samples = [samples[0]]*len(varexps)

        #created_hists = []
        #for var, selection, sample in zip(varexps, selections, samples) :

        #    newname = '%s_%s' %(sample.name, var)
        #    newsamp = self.clone_sample( oldname=sample.name, newname = newname, temporary=True )
        #    created_hists.append(newsamp.name)
        #    self.create_hist( newsamp, var, selection, histpars)
        #    self.curr_hists[newsamp.name] = newsamp.hist.Clone(var)

        #if doratio :
        #    self.create_ratio_sample( 'ratio', num_sample=created_hists[0], den_sample=created_hists[1] )


        #self.curr_canvases['same'] = ROOT.TCanvas('same', '')
        #for idx, name in enumerate( created_hists ) :
        #    self.curr_hists[name].SetMarkerColor( colors[idx] )
        #    self.curr_hists[name].SetLineColor( colors[idx] )

        #    if idx == 0 :
        #        if normalize :
        #            self.curr_hists[name].DrawNormalized('hist')
        #        else :
        #            self.curr_hists[name].Draw('hist')
        #    else :
        #        if normalize :
        #            self.curr_hists[name].DrawNormalized('samehist')
        #        else :
        #            self.curr_hists[name].Draw('samehist')

        ##self.DrawCanvas(self.curr_canvases['same'])

        ## make the legend
        ## In placing the legend move the bottom down 0.05 for each entry
        ##step = len(varexps)
        ##self.curr_legend = self.create_standard_legend(step, doratio)

        ##for var, lab in zip( varexps, labels ) :
        ##    histname = '%s_%s' %(sample.name, var)
        ##    self.curr_legend.AddEntry(self.curr_hists[histname], lab, 'L' )
        ##
        #self.DrawCanvas(self.curr_canvases['same'], ylabel=ylabel, xlabel=xlabel, doratio=doratio)

        # make the legend
        step = len(created_samples)
        self.curr_legend = self.create_standard_legend(step, draw_config=config )

        legend_entries = config.get_legend_entries()
        self.create_same_legend( legend_entries , created_samples )

        #self.DrawCanvas(self.curr_canvases['same'], ylabel=ylabel, xlabel=xlabel, rlabel=rlabel, doratio=doratio, labelStyle=labelStyle, rmin=rmin, rmax=rmax, ymax=ymax, ymin=ymin, logy=logy, extra_label=extra_label, extra_label_loc=extra_label_loc)
        self.DrawCanvas(self.curr_canvases['same'], config )

    #---------------------------------------
    def CompareRatios( self, varexp, selections, samples, histpars=None, normalize=False, doratio=False, colors = [], legend_entries=[], xlabel=None, ylabel=None, rlabel=None, rmin=None, rmax=None, ymin=None, ymax=None, logy=False ) :

        self.clear_all()

        assert  len(samples) == len(selections), 'sample and selection must have the same length'

        if len( selections )%2 != 0 :
            print 'Expect an even number of selecitions, even entries should be numerators, odd entries are denominators '

        if len(colors) != (len( samples )/2) :
            if colors :
                print 'Size of colors input does not match size of vars input!'

            colors = [ self.get_samples(name=s)[0].color for s in samples ]


        num_samps = []
        den_samps = []
        for idx, (selection, samplename) in enumerate(zip(selections, samples)) :

            sample = self.get_samples(name=samplename)[0]

            if idx%2 == 0 :
                newname = '%snum%d' %(sample.name, idx)
            else :
                newname = '%sden%d' %(sample.name, idx)

            newsamp = self.clone_sample( oldname=sample.name, newname=newname, temporary=True )
            self.create_hist( newsamp, varexp, selection, histpars)

            if normalize :
                newsamp.hist.Scale( 1.0/newsamp.hist.Integral() )

            if idx%2 == 0 :
                num_samps.append( newsamp )
            else :
                den_samps.append( newsamp )

        ratio_samps = []
        for num, den in zip( num_samps, den_samps ) :
            rsamp = self.create_ratio_sample( num.name+'ratio', num_sample=num, den_sample=den )
            rsamp.isRatio=False #trick it into not counting these as ratios
            ratio_samps.append(rsamp)

        if doratio :
            self.create_top_canvas_for_ratio('same')
        else :
            self.create_standard_canvas('same')

        self.DrawSameCanvas(self.curr_canvases['same'], ratio_samps, draw_config)


        if not legend_entries :
            legend_entries = [s.name for s in ratio_samps]

        self.curr_legend = self.create_standard_legend( len(ratio_samps) )
        for idx, samp in enumerate(ratio_samps) :
            drawopt = 'PL'
            if samp.isSignal :
                drawopt = 'L'
            legname = legend_entries[idx]
            self.curr_legend.AddEntry(samp.hist, legname,  drawopt)
            self.curr_legend.SetMargin(0.2)

            samp.hist.SetLineColor( colors[idx] )
            samp.hist.SetMarkerColor( colors[idx] )

        self.DrawCanvas(self.curr_canvases['same'], ylabel=ylabel, xlabel=xlabel, rlabel=rlabel, doratio=doratio, rmin=rmin, rmax=rmax, ymax=ymax, ymin=ymin, logy=logy)


    #---------------------------------------


    # ------------------------------------------------------------
    #   Do variable rebinning for a stack plot
    # ------------------------------------------------------------
    def make_variable_binning(self, stacklist,threshold=3):

        if not isinstance(stacklist, list) :
            stacklist = [stacklist]

        # sum stack list
        sum = stacklist[0].Clone('sum')
        sum.Reset()
        for h in stacklist:
            sum.Add(h)

        # make binning
        bins=[]
        axis=sum.GetXaxis()
        bins.append(axis.GetXmin())
        count=0
        for b in range(1, sum.GetNbinsX()+1):
            # this special case is to not extend the first
            # filled bin to the edge of the histogram
            if sum.GetBinContent(b)>0 and count==0 and len(bins)==1:
                bins.append(axis.GetBinLowEdge(b))
            count+=sum.GetBinContent(b)
            if count>threshold:
                bins.append(axis.GetBinUpEdge(b))
                count=0
        if count!=0:
            bins.append(axis.GetXmax())
        print bins,count
        return bins

    # ------------------------------------------------------------
    #   Do variable rebinning for a stack plot
    # ------------------------------------------------------------
    def do_variable_rebinning(self, samp,bins):

        if isinstance( samp, Sample ) :
            oldhist = samp.hist
        if isinstance( samp, ROOT.TH1 ) :
            oldhist = samp
        newhist=ROOT.TH1F(oldhist.GetName()+"_rebin",
        oldhist.GetTitle()+";"+oldhist.GetXaxis().GetTitle()+";"+oldhist.GetYaxis().GetTitle(),len(bins)-1,array('d',bins))
        a=oldhist.GetXaxis()
        newa=newhist.GetXaxis()
        for b in range(1, oldhist.GetNbinsX()+1):
            newb=newa.FindBin(a.GetBinCenter(b))
            val=newhist.GetBinContent(newb)
            err=newhist.GetBinError(newb)
            ratio_bin_widths=newa.GetBinWidth(newb)/a.GetBinWidth(b)
            val=val+oldhist.GetBinContent(b)/ratio_bin_widths
            err=math.sqrt(err*err+oldhist.GetBinError(b)/ratio_bin_widths*oldhist.GetBinError(b)/ratio_bin_widths)
            newhist.SetBinContent(newb,val)
            newhist.SetBinError(newb,err)

        return newhist

    # ----------------------------------------------------------------------------
    # TLegend is initialized
    def create_standard_legend(self, nentries,draw_config=None , isSignalLegend = False, nSigEntries = 0) :

        legend_config = {}
        if draw_config is not None :
            legend_config = draw_config.legend_config

        legendTranslateX = legend_config.get('legendTranslateX', self.legendTranslateX )
        legendTranslateY = legend_config.get('legendTranslateY', self.legendTranslateY )

        legendWiden      = legend_config.get('legendWiden'   , self.legendWiden    )
        legendCompress   = legend_config.get('legendCompress', self.legendCompress )

        legendLoc        = legend_config.get('legendLoc', self.legendLoc )

        entryWidth       = legend_config.get('entryWidth', self.entryWidth )

        siglegPos        = legend_config.get('siglegPos',  self.siglegPos)
        fillalpha        = legend_config.get('fillalpha',  True)


        if legendLoc == 'TopLeft' :
            legend_limits = { 'x1' : 0.2+legendTranslateX, 'y1' : 0.88-legendCompress*entryWidth*nentries+legendTranslateY, 'x2' : 0.5*legendWiden+legendTranslateX, 'y2' : 0.88+legendTranslateY }
        elif legendLoc == 'Double' :
            legend_limits = { 'x1' : 0.18+legendTranslateX, 'y1' : 0.88-legendCompress*entryWidth*nentries/2+legendTranslateY ,
                              'x2' : 0.6*legendWiden+legendTranslateX, 'y2' : 0.85+legendTranslateY }
        else :
            legend_limits = { 'x1' : 0.9-0.25*legendWiden+legendTranslateX, 'y1' : 0.85-legendCompress*entryWidth*nentries+legendTranslateY,
                              'x2' : 0.90+legendTranslateX,                 'y2' : 0.85+legendTranslateY }

        # modify for different canvas size
        if draw_config.get_doratio():
            legend_limits['y1'] = legend_limits['y1']*0.90

        # grab stored legend limits
        if self.legendLimits :
            legend_limits = self.legendLimits

        if isSignalLegend:
            if siglegPos == 'right':
                legend_sig_temp = {'x1': legend_limits['x2'], 'y1': legend_limits['y1'], 'x2': legend_limits['x2']+0.3*legendWiden, 'y2': legend_limits['y2']}
            elif siglegPos == 'bottom':
                legend_sig_temp = {'x1': legend_limits['x1'], 'y1': legend_limits['y1']-legendCompress*entryWidth*nSigEntries, 'x2': legend_limits['x2'], 'y2': legend_limits['y1']}
            legend_limits = legend_sig_temp

        leg = ROOT.TLegend(legend_limits['x1'], legend_limits['y1'],
                           legend_limits['x2'], legend_limits['y2'])

        if fillalpha == True:
            leg.SetFillColorAlpha(ROOT.kWhite,0) # transparent if fillalpha is float or True(0: transparent)
        elif isinstance(fillalpha,float) and fillalpha<=1 and fillalpha>=0:
            leg.SetFillColorAlpha(ROOT.kWhite, fillalpha)
        else:
            leg.SetFillColor(ROOT.kWhite)
        leg.SetBorderSize(0)

        if legendLoc == 'Double' and not isSignalLegend:
            leg.SetNColumns(2)

        return leg


    # ----------------------------------------------------------------------------
    def store_current_legend_placement(self) :

        self.legendLimits = {}

        leg = self.curr_legend
        self.legendLimits['x1'] = leg.GetX1NDC()
        self.legendLimits['y1'] = leg.GetY1NDC()
        self.legendLimits['x2'] = leg.GetX2NDC()
        self.legendLimits['y2'] = leg.GetY2NDC()

        print "legendlimits:", self.legendLimits

    # ----------------------------------------------------------------------------
    def outputExists(self, name, dir) :
        exists = False
        if os.path.isdir(dir) :
            for file in os.listdir( dir ) :
                if file.count(name) :
                    exists=True

        return exists

    # ----------------------------------------------------------------------------
    def addHistsWeightedAvg( self, dest_hist, add_hist ) :

        def _add_generic_bin( dest_hist, add_hist, ibin ) :
            dest_val = dest_hist.GetBinContent( ibin )
            dest_err = dest_hist.GetBinError( ibin )

            add_val  = add_hist.GetBinContent( ibin )
            add_err  = add_hist.GetBinError( ibin )

            if dest_val == 0 :
                avg = ufloat( add_val, add_err )
            elif add_val == 0 :
                avg = ufloat( dest_val, dest_err )
            else :
                dest_uf = ufloat( dest_val, dest_err )
                add_uf  = ufloat( add_val , add_err )

                dest_w = 1./( dest_err * dest_err )
                add_w   = 1./( add_err * add_err )

                avg = (dest_w * dest_uf + add_w * add_uf) / ( dest_w + add_w )

                print 'bin = ', ibin
                print 'dest = ${:.2ufL}$' .format( dest_uf )
                print 'add = ${:.2ufL}$' .format( add_uf )
                print 'avg = ${:.2ufL}$' .format( avg )

            dest_hist.SetBinContent( ibin, avg.n )
            dest_hist.SetBinError( ibin, avg.s )



        if isinstance( dest_hist, ROOT.TH3 ) :
            if dest_hist.GetNbinsX() != add_hist.GetNbinsX() or dest_hist.GetNbinsY() != add_hist.GetNbinsY() or dest_hist.GetNbinsZ() != add_hist.GetNbinsZ() :
                print 'addHistsWeightedAvg: ERROR Bins must have the same lengths!  Exiting!'
                return

            for xbin in range( 1, dest_hist.GetNbinsX()+1 ) :
                for ybin in range( 1, dest_hist.GetNbinsY()+1 ) :
                    for zbin in range( 1, dest_hist.GetNbinsZ()+1 ) :
                        ibin = dest_hist.GetBin( xbin, ybin, zbin )
                        _add_generic_bin( dest_hist, add_hist, ibin )

        elif isinstance( dest_hist, ROOT.TH2 ) :
            if dest_hist.GetNbinsX() != add_hist.GetNbinsX() or dest_hist.GetNbinsY() != add_hist.GetNbinsY() :
                print 'addHistsWeightedAvg: ERROR Bins must have the same lengths!  Exiting!'
                return

            for xbin in range( 1, dest_hist.GetNbinsX()+1 ) :
                for ybin in range( 1, dest_hist.GetNbinsY()+1 ) :
                    ibin = dest_hist.GetBin( xbin, ybin )
                    _add_generic_bin( dest_hist, add_hist, ibin )

        elif isinstance( dest_hist, ROOT.TH1 ) :
            if dest_hist.GetNbinsX() != add_hist.GetNbinsX() :
                print 'addHistsWeightedAvg: ERROR Bins must have the same lengths!  Exiting!'
                return

            for xbin in range( 1, dest_hist.GetNbinsX()+1 ) :
                ibin = dest_hist.GetBin( xbin )
                _add_generic_bin( dest_hist, add_hist, ibin )


# A simple helper function to fill a test tree: this makes the example stand-alone.
def fill_tree(treeName, fileName, b2exp):
    tdf = ROOT.ROOT.RDataFrame(10)
    b2exp = b2exp.replace("X", "tdfentry_")
    tdf.Define("b1", "(double) tdfentry_")\
       .Define("b2", b2exp ).Snapshot(treeName, fileName)


if __name__ == "__main__":
    print "TEST SEQUENCE for RDataFrame"
    # We prepare an input tree to run on
    fileName = "tree.root"
    treeName = "UMDNTuple/EventTree"
    confFile = "Modules/ResonanceTest.py"
    dir1 = "test/zzz/"
    dir2 = "test/www/"
    if not os.path.isdir(dir1): os.makedirs(dir1)
    if not os.path.isdir(dir2): os.makedirs(dir2)
    fill_tree(treeName, dir1+fileName, "(int) X * X")
    fill_tree(treeName, dir2+fileName, "(int) X * X * X")
    samples = SampleManager("test/", treeName, filename=fileName,  xsFile=None,
                                     lumi=10000, readHists=False)
    samples.ReadSamples(confFile)
    print samples.samples


