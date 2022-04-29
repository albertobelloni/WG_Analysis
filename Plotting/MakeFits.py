#!/usr/bin/env python3
from functools import wraps
import sys
import pdb
import ROOT
import uuid
import os
import time
import subprocess
import multiprocessing
ROOT.PyConfig.IgnoreCommandLineOptions = True
from argparse import ArgumentParser
from collections import OrderedDict,defaultdict
import selection_defs as defs
from pprint import pprint
import json
from ROOT import gSystem
from SampleInfo import SampleInfo
from SampleManager import f_Obsolete

## need to read the xsection info
import analysis_utils

#ROOT.gSystem.Load('My_double_CB/RooDoubleCB_cc.so')
parser = ArgumentParser()

parser.add_argument( '--baseDir',                            help='path to workspace directory' )
parser.add_argument( '--outputDir',     default=None,        help='name of output diretory for cards')
#parser.add_argument( '--doStatTests',  action='store_true', help='run statistical tests of WGamma background')
#parser.add_argument( '--doWJetsTests', action='store_true', help='run tests of Wjets background' )
#parser.add_argument( '--doFinalFit',   action='store_true', help='run fit to data and background' )
parser.add_argument( '--useHistTemp',   action='store_true', help='use histogram templates' )
parser.add_argument( '--useToySignal',  action='store_true', help='use gaussian as signal' )
parser.add_argument( '--useToyBkgd',    action='store_true', help='use exponential as background ' )
parser.add_argument( '--noRunCombine',  action='store_true', help='Dont run combine, use existing results' )
parser.add_argument( '--combineDir',    default=None,        help='path to combine directory' )
parser.add_argument( '--condor',        action='store_true', help='run condor jobs' )
parser.add_argument( '--paramodel',        action='store_true', help='Use fully para model' )
parser.add_argument( '--usedata',        action='store_true', help='Unblind data' )
parser.add_argument( '--GoF',        action='store_true', help='Do Goodness of Fit' )
parser.add_argument( '--NoBKGUnc',        action='store_true', help='No bkg uncertainty, because use data as template' )
parser.add_argument( '--BiasStudy',        action='store_true', help='Add other function to the work space for bias study' )

options = parser.parse_args()

_WLEPBR = (1.-0.6741)
#_XSFILE   = 'cross_sections/photon16_smallsig.py'
_XSFILE   = 'cross_sections/photon_expect.py'
_LUMI16   = 36330*0.2
_LUMI17   = 41530*0.2
_LUMI18   = 59740*0.2

DEBUG = 0

tColor_Off = "\033[0m"                    # Text Reset
tPurple = "\033[0;35m%s"+tColor_Off       # Purple
tRed    = "\033[1;31m%s"+tColor_Off       # Red



# ---------------------------------------------------


def f_Dumpfname(func):
    """ decorator to show function name and caller name """
    @wraps(func)
    def echo_func(*func_args, **func_kwargs):
        if DEBUG: print(('func \033[1;31m {}()\033[0m called by \033[1;31m{}() \033[0m'.format(func.__name__,sys._getframe(1).f_code.co_name)))
        return func(*func_args, **func_kwargs)
    return echo_func

recdd = lambda : defaultdict(recdd) ## define recursive defaultdict

targetfunc = 'MultiPdf'
#targetfunc = '_atlas'
#targetfunc = '_dijet' 

testfunc = "_atlas"
#testfunc = "_dijet"
#testfunc = '_vvdijet'

sourceOfBKG = 'bkgfit_data'
injectsignal='1'

# dijet 1,2,3,4: 0,1,2,3
# vvdijet 1,2,3,4: 4,5,6,7
# expow 1,2,3,4: 8,9,10,11

genindex='2'
fitindex='-1'

ntoy = '150'
rseed = '160'
rname = '_expow2enve_160'

options.outputDir = "/data/users/yihuilai/test_code/WG_Analysis_clean_clean/Plotting/data/wg/"

def main() :

    pdf_prefix, bkgparams ="dijet", ["dijet_order1", "dijet_order2"]
    if 'expow' in targetfunc:
        pdf_prefix, bkgparams ="expow", ["expow_order1", "expow_order2"]
    if 'atlas' in targetfunc:
        pdf_prefix, bkgparams ="atlas", ["atlas_order1", "atlas_order2", "atlas_order3"]
    if 'vvdijet' in targetfunc:
        pdf_prefix, bkgparams ="vvdijet", ["vvdijet_order1", "vvdijet_order2"]
    pdf_prefix, bkgparams ="MultiPdf", []

    ws_keys = {
              # this can be made to a class
              'signal'   : SampleInfo ( pdf_prefix = 'cb_MG',
                             params_prefix = [ 'cb_cut1_MG',
                                               'cb_cut2_MG',
                                               'cb_mass_MG',
                                               'cb_sigma_MG',
                                               'cb_power1_MG',
                                               'cb_power2_MG' ],
                           useLumi = True, useMET = True, usePDF = True,),
              'All'        : SampleInfo( name = 'All', useLumi = True,
                                            pdf_prefix=pdf_prefix, params_prefix=bkgparams,
                                            useMET = False, usePDF = False, ),
              'WGamma'        : SampleInfo( name = 'WGamma', useLumi = True,
                                            useMET = False, usePDF = False, ),
              'TTbar'         : SampleInfo( name = 'TTbar', useLumi = False,
                                             useMET = False, usePDF = False, ),
              'TTG'           : SampleInfo( name = 'TTG',   useLumi = False,
                                             useMET = False, usePDF = False, ),
              'Wjets'         : SampleInfo( name = 'Wjets', useLumi = False,
                                             useMET = False, usePDF = False, ),
              'Zgamma'        : SampleInfo( name = 'Zgamma', useLumi = False,
                                             useMET = False, usePDF = False, ),
              'GammaGamma'    : SampleInfo( name = 'GammaGamma',
                                useLumi = False, useMET = False, usePDF = False, ),
              'Backgrounds'   : SampleInfo( name = 'Backgrounds',
                                useLumi = False, useMET = False, usePDF = False, ),
              'toydata'       : {'pdf': 'toydata'},
              'toysignal'     : {'pdf': 'gauss'},
              'toybkg'        : {'pdf': 'exp'},
             }


    bins = [
        # mu/el channel, photons in th barrel/endcap
        {'channel' : 'mu', 'year': 2016},
        {'channel' : 'el', 'year': 2016},
        {'channel' : 'mu', 'year': 2017},
        {'channel' : 'el', 'year': 2017},
        {'channel' : 'mu', 'year': 2018},
        {'channel' : 'el', 'year': 2018},
    ]

    global binid
    def binid(ibin): return "".join(map(str,list(ibin.values())))

    global lumi
    def lumi(ibin):
        year = ibin['year']
        if year == 2016: return _LUMI16
        if year == 2017: return _LUMI17
        if year == 2018: return _LUMI18
        raise RuntimeError

    if options.outputDir is None :
        options.outputDir = "/data/users/yihuilai/test_code/WG_Analysis_clean_clean/Plotting/data/wg"
    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )

    if options.baseDir is None :
        options.baseDir = "/data/users/yihuilai/test_code/WG_Analysis_clean_clean/Plotting/data/"

    if options.combineDir == None:
        options.combineDir = "/data/users/yihuilai/combine/CMSSW_11_0_0/src/"


    #signal_masses   = [900]
    #signal_masses   = [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400,
    #                   1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3500, 4000]
    signal_masses    = [300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
    signal_widths    = ['5', '0p01']
    if options.GoF:
        signal_masses    = [600]
        signal_widths    = ['5']
    #signal_masses    = [300, 2000]

    fitrangefx = lambda m : (200,200+1.5*m) if m<625 else (400,2000)

    ROOT.RooRandom.randomGenerator().SetSeed(int(12345))
    var_opt = MakeLimits(  var=  "mt_res" ,
                           wskeys = ws_keys,
                           masspoints  = signal_masses,
                           widthpoints = signal_widths,
                           #backgrounds=['WGamma', 'TTG', 'TTbar', 'Wjets', 'Zgamma'],
                           backgrounds = ['All'],
                           baseDir = options.baseDir,
                           bins = bins,
                           cutsetlist = "A",
                           outputDir = options.outputDir,
                           useToySignal = options.useToySignal,
                           useToyBackground = options.useToyBkgd,
                           # don't put norms in new file
                           #keepNorms = False, FIXME
                           noShapeUnc = True,
                           addShapeUnc2Mass = True,
                           #method = 'AsymptoticLimitsManual', ## only use --condor with manual
                           #manualpoints = [ -1., -0.1,0,0.001,0.01,0.03,0.1,0.2,0.3,0.5,1.,1.5,2.,2.3,2.6,3,
                           #                 3.5,4.,5.,8.,10.]
                           #rmin = 0.1,
                           #rmax = 20,
                           #seed = 123456,
                           doImpact=False,
                           floatBkg =True, ## background parameters will be contrained if False
                           #numberOfToys = 2, ## -1 for Asimov, 0 for "data" (or homemade toy)
                           #freezeParameter = "all", ## "all", "bkg" or "sig", or "s+b", or "constrained"
                           #fitrange = fitrangefx # a function that takes mass and return fit range
                         )

    var_opt.setup()

    combine_jobs = var_opt.get_combine_files()

    if not options.noRunCombine :

        if options.condor:
            ### run condor jobs
            jdl_name = '%s/job_desc.jdl'  %( options.outputDir )
            make_jdl( combine_jobs, jdl_name )
            
            os.system( 'condor_submit %s' %jdl_name )

            print((tPurple% "WARNING: unstable method"))
            #wait_for_jobs( 'run_combine')
            wait_for_jobs( 'yihuilai')
        else:
            ### run local shell commands in parallel
            var_opt.run_commands()

    results = var_opt.get_combine_results()



# ---------------------------------------------------


@f_Dumpfname
def make_jdl( exe_list, output_file ) :

    base_dir = os.path.dirname( output_file )

    file_entries = [
    'universe = vanilla',
    '# This is the executable to run.  If a script,',
    '# be sure to mark it "#!<path to interp>" on the first line.',
    '# Filename for stdout, otherwise it is lost',
    '# Copy the submittor environment variables',
    'getenv = True',
    '# Require to run on SL/CentOS7',
    'Requirements = (TARGET.OpSysMajorVer == 7)',
    'when_to_transfer_output = ON_EXIT_OR_EVICT',
    #'+IsTestJob=True'
    ]

    for exe in exe_list :

        file_entries.append('output = %s'%exe.replace('.sh', '_out.txt'))
        file_entries.append('error = %s'%exe.replace('.sh', '_err.txt'))
        file_entries.append('log = %s'%exe.replace('.sh', '_log.txt'))

        file_entries.append('Executable = %s' %exe)
        file_entries.append('Initialdir = %s' %base_dir)
        file_entries.append('# This is the argument line to the Executable')
        file_entries.append('# Queue job')
        file_entries.append('queue')

    ofile = open( output_file, 'w' )

    for line in file_entries :
        ofile.write(  line + '\n' )

    ofile.close()



# ---------------------------------------------------


def listformat(liste=[],form="%-14s"):
        return form*len(liste) %tuple(liste)



# ---------------------------------------------------


def Width_str2float( width ):
    widthdict = {"5": 5, "0p01": 0.01}
    try:
       fwidth = float(widthdict[width])
    except KeyError:
       print("Can not turn the width into float")
    return fwidth



# ---------------------------------------------------


def wait_for_jobs( job_tag ) :

    while 1 :
        time.sleep(20)
        status = subprocess.Popen( ['condor_q'], stdout=subprocess.PIPE) \
                           .communicate()[0]

        n_limits = 0

        for line in status.split('\n') :
            if line.count(job_tag ) :
                n_limits += 1

        if n_limits == 1 :
            return
        else :
            print(('%d Jobs still running' %(n_limits-1)))


# ---------------------------------------------------

def import_workspace( ws , objects):
    """ import objects into workspace """

    if not isinstance( objects, list ):
        objects = [objects,]

    ## NOTE getattr is needed to escape python keyword import
    for o in objects:
        getattr( ws, "import") ( o )

# ---------------------------------------------------


class MakeLimits( ) :

    def __init__(self, **kwargs) :

        self.fail=False

        self.var              = kwargs.get('var'        ,  None )
        self.masspoints       = kwargs.get('masspoints' ,  None )
        self.widthpoints      = kwargs.get('widthpoints',  None )
        self.cutsetlist       = kwargs.get('cutsetlist' ,  None )
        self.baseDir          = kwargs.get('baseDir'    ,  None )
        self.outputDir        = kwargs.get('outputDir'  ,  None )
        self.bins             = kwargs.get('bins'       ,  None )
        self.bkgnames         = kwargs.get('backgrounds',  None )
        self.rmin             = kwargs.get('rmin'       ,  None )
        self.rmax             = kwargs.get('rmax'       ,  None )
        self.seed             = kwargs.get('seed'       ,  None )
        self.fitrange         = kwargs.get('fitrange'   ,  None )

        self.wskeys           = kwargs.get('wskeys'     ,  None )

        self.useToySignal     = kwargs.get('useToySignal',     False )
        self.useToyBackground = kwargs.get('useToyBackground', False )

        #self.keepNorms        = kwargs.get('keepNorms', False )
        self.noShapeUnc       = kwargs.get('noShapeUnc', False)
        self.addShapeUnc2Mass = kwargs.get('addShapeUnc2Mass', False)
        self.doImpact         = kwargs.get("doImpact", False)
        self.floatBkg         = kwargs.get("floatBkg", False)
        self.numberOfToys     = kwargs.get("numberOfToys", None)
        self.freezeParameter  = kwargs.get("freezeParameter", None)


        self.wstag = kwargs.get('wsTag', 'base' )
        self.method = kwargs.get('method', 'AsymptoticLimits' )
        self.manualpoints = kwargs.get('manualpoints', [] )

        self.xvarname = kwargs.get('xvarname', 'mt_res')

        self.signals = OrderedDict()
        self.backgrounds = OrderedDict()
        self.datas = OrderedDict()

        self.params = OrderedDict()

        ## format checks
        if self.masspoints == None or not isinstance( self.masspoints, list ) :
            print('Must provide a list of mass points')
            self.fail = True;

        if self.widthpoints == None or not isinstance( self.widthpoints, list):
            print('Must provide a list of width points')
            self.fail = True;

        if self.var == None or not isinstance( self.var, str ) :
            print('Must provide a plot var as a string')
            self.fail = True

        if self.bins == None or not isinstance( self.bins, list ) :
            print('Must provide a list of bins ')
            self.fail = True

        if self.wskeys == None or not isinstance( self.wskeys, dict) :
            print("Must provide a dictionary of workspace names")
            self.fail = True

        if self.baseDir == None or not isinstance( self.baseDir, str ) :
            print('Must provide a base directory')
            self.fail = True

        #--------------------

        if self.useToyBackground :
            print("use exponential toy background. Will ignore the input backgrounds...")
            self.bkgnames = ['toybkg']

        if self.useToySignal :
            print("use gaussian toy signal. Will ignore the input signals...")
            self.signame = 'toysignal'
        else:
            self.signame = 'signal'

        if not self.useToySignal:
           print("have to load cross sections for signals for normalization. :( ")
           self.weightMap,_ = analysis_utils.read_xsfile( _XSFILE, 1, print_values=True )



# ---------------------------------------------------






# ---------------------------------------------------


    @f_Dumpfname
    def setup( self ):

        if self.fail :
            print('Initialzation failed, will not setup')
            return

        # -------------------------------------------------
        # Prepare workspaces
        # -------------------------------------------------

        # -------------------------------------------------
        # background
        # -------------------------------------------------

        for bkgn in self.bkgnames:
            if not os.path.isdir( self.outputDir+'/'+bkgn ) :
               print(("creating directory %s/%s"%(self.outputDir, bkgn )))
               os.makedirs( self.outputDir+'/'+ bkgn )

        if self.useToyBackground :
            # -------------------------------------------------
            # if testing using an exponential background, make that workspace
            # -------------------------------------------------
            self.make_exp_background(  -0.01, 200 )

        else:
            # -------------------------------------------------
            # Copy the background funcitons and set variables to constant as needed
            # -------------------------------------------------
            self.prepare_background_functions( )

        # ---------------------------------------------------
        # signal
        # ---------------------------------------------------

        if not os.path.isdir( self.outputDir+'/'+self.signame ) :
           print((" creating directory %s/%s"%(self.outputDir, self.signame)))
           os.makedirs( self.outputDir+'/'+self.signame )

        if options.useToySignal :
            # -------------------------------------------------
            # if testing using a gauss signal, make that workspace
            # -------------------------------------------------
            self.make_gauss_signal(  50 )

        else:
            # -------------------------------------------------
            # Copy the signal funcitons and set variables to constant as needed
            # -------------------------------------------------
            self.prepare_signal_functions( )

        #signal_data = {}
        if options.useHistTemp :
            # -------------------------------------------------
            # Get the normalization info from the samples
            # -------------------------------------------------
            signal_file = '%s/%s.root' %( self.baseDir, self.signal_ws)
            signal_data = self.get_signal_data( signal_file, self.signal_ws,  self.mass_points, self.plot_var, self.bins )


        # -------------------------------------------------
        # Since we're blind, make toy data
        # -------------------------------------------------
        self.dataname = 'toydata'
        #binid = '%s_%s' %( ibin['channel'], ibin['eta'] )

        #wgamma_entry = get_workspace_entry( 'Wgamma', ibin['channel'], ibin['eta'], self.plot_var )
        #wjets_entry  = get_workspace_entry( 'wjets' , ibin['channel'], ibin['eta'], self.plot_var )

        if options.useHistTemp :
            wgamma_entry = wgamma_entry.replace( 'dijet', 'datahist' )

        #self.generate_toy_data(  sigpars = ['M900_W5_mu'],
        #                         signorms = [2.0], data_norm=20.0)
        self.generate_toy_data( )


        #---------------------------------------
        # Add systematics
        #---------------------------------------
        self.add_systematics()

        # Make Signal uncertainty plots --Yihui
        makesysplots=False
        if makesysplots:
            c=ROOT.TCanvas("c","c",1200,600)
            c.SetFillColor(0)
            c.SetBorderMode(0)
            c.SetBorderSize(2)
            c.SetFrameBorderMode(0)
            ROOT.gStyle.SetOptStat(0)
            c.SetLogy()
            leg = ROOT.TLegend(0.72,0.3,0.85,0.8)
            leg.SetBorderSize(0)
            leg.SetLineStyle(1)
            leg.SetLineWidth(1)
            i=0
            xs={}
            ys={}
            Graphs={}
            gm = ROOT.TMultiGraph()
            signal_masses    = [300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
            from array import array
            n = len(signal_masses)
            graphColors = [ROOT.kBlack, ROOT.kGray+1, ROOT.kRed +1, ROOT.kAzure+1, ROOT.kAzure-2,
               ROOT.kSpring-1, ROOT.kYellow -2 , ROOT.kYellow+1,
               ROOT.kRed, ROOT.kOrange, ROOT.kGreen, ROOT.kBlue, ROOT.kBlack, ROOT.kBlack, ROOT.kBlack ]
            for ch in ['el','mu']:
                for wid in ['5']:#,'0p01']:
                    for year in ['2016','2017','2018']:
                           labelStyle = ch+'_'+year+wid
                           labelStyle = labelStyle.replace("5",",#Gamma_{x}/m_{x}=5%")
                           labelStyle = labelStyle.replace("0p01",",#Gamma_{x}/m_{x}=0.01%")
                           if ch == 'el':
                               sys_error = ['CMS_ph_eff','CMS_ph_scale','CMS_el_eff','CMS_el_scale','CMS_el_trig','pdf','qcd_scale', 'CMS_jer','CMS_jec','CMS_pile','CMS_bjetsf','CMS_psv']
                           else:
                               sys_error = ['CMS_ph_eff','CMS_ph_scale','CMS_mu_eff','CMS_mu_scale','CMS_mu_trig','pdf','qcd_scale', 'CMS_jer','CMS_jec','CMS_pile','CMS_bjetsf','CMS_psv']
                           xs[labelStyle] = array( 'd' )
                           ys[labelStyle] = array( 'd' )
                           totunc=0
                           for isigm in signal_masses:
                               xs[labelStyle].append( isigm )
                               for isys in sys_error:
                                   sigkey = "M%i_W%s_%s%s" %(isigm,wid,ch,year)
                                   if float(self.signals[sigkey]["sys"][isys][0]) > float(self.signals[sigkey]["sys"][isys][1]):
                                       syseUp = float(self.signals[sigkey]["sys"][isys][0])
                                       syseDown = float(self.signals[sigkey]["sys"][isys][1])
                                   else:
                                       syseUp = float(self.signals[sigkey]["sys"][isys][1])
                                       syseDown = float(self.signals[sigkey]["sys"][isys][0]) 
                                   totunc+=( 100*(abs(syseUp-1)+abs(syseDown-1))/2.0 )**2
                               ys[labelStyle].append( ROOT.TMath.Sqrt(totunc) )

                           Graphs[labelStyle] = ROOT.TGraph( n, xs[labelStyle],ys[labelStyle])
                           Graphs[labelStyle].SetMarkerStyle(20)
                           Graphs[labelStyle].SetMarkerColor(graphColors[i])
                           Graphs[labelStyle].SetLineColor(graphColors[i])
                           Graphs[labelStyle].SetLineWidth(2)
                           gm.Add(Graphs[labelStyle])
                           entry=leg.AddEntry(Graphs[labelStyle],labelStyle ,"lp")
                           entry.SetFillStyle(1001)
                           entry.SetMarkerStyle(9)
                           entry.SetMarkerSize(1.5)
                           entry.SetLineStyle(1)
                           entry.SetLineWidth(3)
                           entry.SetTextFont(42)
                           entry.SetTextSize(0.03)
                           i+=1
            gm.Draw("ALP same")
            gm.GetXaxis().SetTitle("m_{X} [GeV]")
            gm.GetXaxis().SetTitleSize(0.05)
            gm.GetXaxis().SetTitleOffset(0.8)
            gm.GetXaxis().SetTitleFont(42)
            gm.GetYaxis().SetTitle("Relative uncertainty (%)")
            gm.GetYaxis().SetLabelFont(42)
            gm.GetYaxis().SetLabelSize(0.05)
            gm.GetYaxis().SetTitleSize(0.05)
            gm.GetYaxis().SetTitleFont(42)
            gm.GetYaxis().SetTitleOffset(0.8)
            gm.GetXaxis().SetLimits(200,2600)  # #
            gm.GetXaxis().SetRangeUser(200,2600)  # #
            gm.GetYaxis().SetRangeUser(1,100)  # #
            leg.Draw()
            tex = ROOT.TLatex(0.14,0.95,"CMS")
            tex.SetNDC()
            tex.SetTextAlign(13)
            tex.SetTextSize(0.048)
            tex.SetLineWidth(2)
            tex.Draw()
            labeltext = ' (13 TeV)'
            tex2 = ROOT.TLatex(0.75,0.95,labeltext)
            tex2.SetNDC()
            tex2.SetTextAlign(13)
            tex2.SetTextFont(42)
            tex2.SetTextSize(0.03648)
            tex2.SetLineWidth(2)
            tex2.Draw()
            line = ROOT.TLine(200,1,2000,1);
            line.SetLineStyle(2)
            line.SetLineWidth(2)
            line.Draw()
            line2 = ROOT.TLine(200,10,2000,10);
            line2.SetLineStyle(2)
            line2.SetLineWidth(2)
            line2.Draw()
            c.SaveAs('sys_all.pdf')
            c.SaveAs('sys_all.C')
            input("")
            exit()


            for ch in ['el','mu']:
                for wid in ['5','0p01']:
                    for year in ['2016','2017','2018']:
                       for index in ['A','B']:
                           c=ROOT.TCanvas("c","c",1200,600)
                           c.SetFillColor(0)
                           c.SetBorderMode(0)
                           c.SetBorderSize(2)
                           c.SetFrameBorderMode(0)
                           ROOT.gStyle.SetOptStat(0)
                           c.SetLogy()
                           leg = ROOT.TLegend(0.75,0.3,0.88,0.8)
                           leg.SetBorderSize(0)
                           leg.SetLineStyle(1)
                           leg.SetLineWidth(1)
                           i=0
                           labelStyle = ch+'_'+wid+'_'+year+'_'+index
                           signal_masses    = [300, 350, 400, 450, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
                           if ch == 'el':
                               sys_error = ['CMS_ph_eff','CMS_ph_scale','CMS_el_eff','CMS_el_scale','CMS_el_trig','pdf',]
                           else:
                               sys_error = ['CMS_ph_eff','CMS_ph_scale','CMS_mu_eff','CMS_mu_scale','CMS_mu_trig','pdf',]
                           if index=='B':
                               sys_error = ['qcd_scale', 'CMS_jer','CMS_jec','CMS_pile','CMS_bjetsf','CMS_psv']
                               if year != '2018': sys_error.append('CMS_pref')

                           nickName = {'CMS_psv':'PSV', 'CMS_jer':'JER', 'qcd_scale':'qcd scale', 'CMS_jec':'JEC','CMS_pile':'PileUp', 'CMS_el_eff':'Electron ID', 'CMS_bjetsf':'BJet', 'CMS_ph_eff':'Photon ID', 'CMS_pref':'Prefire', 'CMS_el_trig':'Electron Trigger', 'pdf':'PDF', 'CMS_el_scale':'Electron Energy', 'CMS_ph_scale':'Photon Energy','CMS_mu_eff':'Muon ID','CMS_mu_trig':'Muon Trigger','CMS_mu_scale':'Muon Energy'}
                           from array import array
                           n = len(signal_masses)
                           xs={}
                           ys={}
                           xes={}
                           y_eus={}
                           y_eds={}
                           Graphs={}
                           graphColors = [ROOT.kBlack, ROOT.kGray+1, ROOT.kRed +1, ROOT.kAzure+1, ROOT.kAzure-2,
                              ROOT.kSpring-1, ROOT.kYellow -2 , ROOT.kYellow+1,
                              ROOT.kBlack, ROOT.kBlack, ROOT.kBlack, ROOT.kBlack, ROOT.kBlack, ROOT.kBlack, ROOT.kBlack ]
                           gm = ROOT.TMultiGraph()
                           for isys in sys_error:
                               xs[isys] = array( 'd' )
                               xes[isys] = array( 'd' )
                               ys[isys] = array( 'd' )
                               y_eus[isys] = array( 'd' )
                               y_eds[isys] = array( 'd' )
                               for isigm in signal_masses:
                                   sigkey = "M%i_W%s_%s%s" %(isigm,wid,ch,year)
                                   if float(self.signals[sigkey]["sys"][isys][0]) > float(self.signals[sigkey]["sys"][isys][1]):
                                       syseUp = float(self.signals[sigkey]["sys"][isys][0])
                                       syseDown = float(self.signals[sigkey]["sys"][isys][1])
                                   else:
                                       syseUp = float(self.signals[sigkey]["sys"][isys][1])
                                       syseDown = float(self.signals[sigkey]["sys"][isys][0])
                                   xs[isys].append( isigm )
                                   xes[isys].append( 0 )
                                   #print(syseUp, syseDown)
                                   ys[isys].append( 100*(abs(syseUp-1)+abs(syseDown-1))/2.0 )
                                   y_eus[isys].append( 100*abs(abs(syseUp-1)-abs(syseDown-1))/2.0 )
                                   y_eds[isys].append( 100*abs(abs(syseUp-1)-abs(syseDown-1))/2.0 )
                               Graphs[isys] = ROOT.TGraphAsymmErrors( n, xs[isys],ys[isys], xes[isys],xes[isys] ,y_eds[isys],y_eus[isys] )
                               Graphs[isys].SetMarkerStyle(20)
                               Graphs[isys].SetMarkerColor(graphColors[i])
                               Graphs[isys].SetLineColor(graphColors[i])
                               Graphs[isys].SetLineWidth(2)
                               gm.Add(Graphs[isys])
                               entry=leg.AddEntry(Graphs[isys],nickName[isys] ,"lp")
                               entry.SetFillStyle(1001)
                               entry.SetMarkerStyle(9)
                               entry.SetMarkerSize(1.5)
                               entry.SetLineStyle(1)
                               entry.SetLineWidth(3)
                               entry.SetTextFont(42)
                               entry.SetTextSize(0.03)
                               i+=1
                           gm.Draw("ALP same")
                           gm.GetXaxis().SetTitle("m_{X} [GeV]")
                           gm.GetXaxis().SetTitleSize(0.05)
                           gm.GetXaxis().SetTitleOffset(0.8)
                           gm.GetXaxis().SetTitleFont(42)
                           gm.GetYaxis().SetTitle("Relative uncertainty (%)")
                           gm.GetYaxis().SetLabelFont(42)
                           gm.GetYaxis().SetLabelSize(0.05)
                           gm.GetYaxis().SetTitleSize(0.05)
                           gm.GetYaxis().SetTitleFont(42)
                           gm.GetYaxis().SetTitleOffset(0.8)
                           gm.GetXaxis().SetLimits(200,2500)  # #
                           gm.GetXaxis().SetRangeUser(200,2500)  # #
                           gm.GetYaxis().SetRangeUser(0.01,100)  # #
                           leg.Draw()
                           tex = ROOT.TLatex(0.14,0.95,"CMS")
                           tex.SetNDC()
                           tex.SetTextAlign(13)
                           tex.SetTextSize(0.048)
                           tex.SetLineWidth(2)
                           tex.Draw()
                           labeltext1 = '2016 '
                           labeltext2 = '#Gamma_{X}/m_{X} = 0.01%'
                           if labelStyle:
                               if labelStyle.count('2017') :
                                   labeltext1 = '2017 '
                               if labelStyle.count('2018') :
                                   labeltext1 = '2018 '
                               if labelStyle.count('el') :
                                   labeltext1 += 'Electron Channel'
                               if labelStyle.count('mu') :
                                   labeltext1 += 'Muon Channel'
                               if labelStyle.count('5') :
                                   labeltext2 = '#Gamma_{X}/m_{X} = 5%'
                           tex1 = ROOT.TLatex(0.14,0.85,labeltext1)
                           tex1.SetNDC()
                           tex1.SetTextAlign(13)
                           tex1.SetTextSize(0.048)
                           tex1.SetLineWidth(2)
                           tex1.Draw()
                           tex11 = ROOT.TLatex(0.14,0.78,labeltext2)
                           tex11.SetNDC()
                           tex11.SetTextAlign(13)
                           tex11.SetTextSize(0.048)
                           tex11.SetLineWidth(2)
                           tex11.Draw()
                           labeltext = '36 fb^{-1} (13 TeV)'
                           if labelStyle:
                               if labelStyle.count('2016') :
                                   labeltext = '36.3 fb^{-1} (13 TeV)'
                               if labelStyle.count('2017') :
                                   labeltext = '41.5 fb^{-1} (13 TeV)'
                               if labelStyle.count('2018') :
                                   labeltext = '59.7 fb^{-1} (13 TeV)'
                           tex2 = ROOT.TLatex(0.75,0.95,labeltext)
                           tex2.SetNDC()
                           tex2.SetTextAlign(13)
                           tex2.SetTextFont(42)
                           tex2.SetTextSize(0.03648)
                           tex2.SetLineWidth(2)
                           tex2.Draw()
                           line = ROOT.TLine(200,1,2000,1);
                           line.SetLineStyle(2)
                           line.SetLineWidth(2)
                           line.Draw()
                           line2 = ROOT.TLine(200,10,2000,10);
                           line2.SetLineStyle(2)
                           line2.SetLineWidth(2)
                           line2.Draw()
                           c.SaveAs('sys_'+labelStyle+'.pdf')
                           c.SaveAs('sys_'+labelStyle+'.C')
            exit()
        #---------------------------------------
        # Prepare the data cards for limits
        #---------------------------------------

        self.allcards = {}

        self.generate_all_cards( )



# ---------------------------------------------------

    def add_systematics( self ):

        for bn in self.bkgnames:
            self.backgrounds[bn].sys = recdd()

        for ibin in self.bins:
            self.add_systematics_channel( ibin )

    def add_systematics_channel( self, ibin ):
        ch, year = ibin["channel"], ibin["year"]
        binname = binid(ibin)

        ## opening json storing normalization information
        with open('data/%sgsys%i.json'%(ch,year)) as fo:
            systematic_dict = json.load(fo)

            #Add More systematics from pdf -- Yihui
            morefiles = ['0_4', '5_9', '10_14', '15_19', '20_24', '25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_74', '75_79', '80_84', '85_89', '90_94', '95_99','100_100']
            for ifil in morefiles:
                f = open('data/%sgsys%i_pdf_%s.json'%(ch,year,ifil))
                dd = json.load(f)
                for sys in list(dd['A'].keys()):
                    systematic_dict['A'][sys] = dd['A'][sys]
            ### process background systematics
            sysdict = recdd()
            for cuttag in self.cutsetlist:
                for sys in  list(systematic_dict[cuttag].keys()):
                    sysdict[cuttag][sys] = systematic_dict[cuttag][sys]["background"]


            sysdict = { k: self.process_systematics(sd, ch, year) for k, sd in list(sysdict.items()) }

            for bn in self.bkgnames:
                self.backgrounds[bn].sys[binname] = sysdict

            ### process signal systematics

            for width in self.widthpoints:
                for mass in self.masspoints:

                    cuttag = defs.selectcuttag(mass,year)
                    sysdict = recdd()
                    sampname = "MadGraphResonanceMass%i_width%s"%(mass,width)

                    for sys in list(systematic_dict[cuttag].keys()):
                        sysdict[sys] = systematic_dict[cuttag][sys][sampname]

                    sysdict = self.process_systematics( sysdict, ch, year )

                    sigkey = "M%i_W%s_%s%i" %(mass,width,ch,year)
                    if sigkey in self.signals:
                        self.signals[sigkey]["sys"]= sysdict

    def process_systematics(self, sysdict, ch, yr):

        ##
        ## manually distribute systematic values
        ##
        ## hard-coded
        ## lumi, PU
        ##
        ## Take up/down values
        ## trigger, JEC, gamma ID
        ##
        ## Take max/min
        ## PDF scale
        ##
        ## screen for unreasonable values
        ## PSV, prefiring weights
        syslist = [
             ('jet_btagSFUP','jet_btagSFDN'),
             ('JetResUp', 'JetResDown'),
             ('JetEnUp', 'JetEnDown'),
             ('MuonEnUp', 'MuonEnDown'),
             ('ElectronEnUp', 'ElectronEnDown'),
             ('PhotonEnUp', 'PhotonEnDown'),
             ('UnclusteredEnUp', 'UnclusteredEnDown'),
             ('el_trigSFUP', 'el_trigSFDN'),
             ('el_idSFUP', 'el_idSFDN'),
             ('el_recoSFUP', 'el_recoSFDN'),
             ('ph_idSFUP', 'ph_idSFDN'),
             ('ph_psvSFUP', 'ph_psvSFDN'),
             ("mu_trigSFUP", "mu_trigSFDN"),
             ("mu_idSFUP", "mu_idSFDN"),
             ("mu_trkSFUP", "mu_trkSFDN"),
             ("mu_isoSFUP", "mu_isoSFDN"),]

        bjetsfnames= ( 'jet_btagSFUP',   'jet_btagSFDN'   )
        prefnames  = ( 'prefup',         'prefdown'    )
        punames    = ( 'PUUP5',          'PUDN5'       )
        qcdscalenames = ( 'muR1muF2',    'muR1muFp5',
                       'muR2muF1',       'muR2muF2',
                       'muRp5muF1',      'muRp5muFp5'  )
        pdfnames   = ['NNPDF3.0:Member%i'%i for i in range(101)]
        mutrnames  = ( 'mu_trigSFUP',    'mu_trigSFDN' )
        eltrnames  = ( 'el_trigSFUP',    'el_trigSFDN' )
        jecnames   = ( 'JetEnUp',        'JetEnDown'   )
        jernames   = ( 'JetResUp',       'JetResDown'  )
        phidnames  = ( 'ph_idSFUP',      'ph_idSFDN'   )
        phpsnames  = ( 'ph_psvSFUP',     'ph_psvSFDN'  )
        muidnames  = ( 'mu_idSFUP',      'mu_idSFDN'   )
        elidnames  = ( 'el_idSFUP',      'el_idSFDN'   )
        muennames  = ( 'MuonEnUp',       'MuonEnDown'  )
        elennames  = ( 'ElectronEnUp',   'ElectronEnDown')
        phennames  = ( 'PhotonEnUp',     'PhotonEnDown' )


        newsysdict = recdd()

        ## LUMI POG
        ## https://twiki.cern.ch/twiki/bin/viewauth/CMS/TWikiLUM

        #newsysdict["CMS_lumi"] = 1.023 if yr == 2017 else 1.025
        if yr ==2016: newsysdict["CMS_lumi2016"] = 1.010
        if yr ==2017: newsysdict["CMS_lumi2017"] = 1.020
        if yr ==2018: newsysdict["CMS_lumi2018"] = 1.015
        newsysdict["CMS_lumicorr"]  = {2016:1.006,2017:1.009,2018:1.02}[yr]
        if yr !=2016: newsysdict["CMS_lumicorr2"] = {2017:1.006,2018:1.002}[yr]

        ## trigger
        if ch == "mu":
            newsysdict["CMS_mu_trig"] = tuple(sysdict[s]/100.+1 for s in mutrnames)
        if ch == "el":
            newsysdict["CMS_el_trig"] = tuple(sysdict[s]/100.+1 for s in eltrnames)

        ## btag SF
        newsysdict["CMS_bjetsf"]  = tuple(sysdict[s]/100.+1 for s in bjetsfnames)

        ## PU
        newsysdict["CMS_pile"] = tuple(sysdict[s]/100.+1 for s in punames)

        ## JEC
        newsysdict["CMS_jec"]  = tuple(sysdict[s]/100.+1 for s in jecnames)

        ## JER
        newsysdict["CMS_jer"]  = tuple(sysdict[s]/100.+1 for s in jernames)

        ## ph ID
        newsysdict["CMS_ph_eff"]  = tuple(sysdict[s]/100.+1 for s in phidnames)

        ## ph PSV
        newsysdict["CMS_psv"]  = tuple(sysdict[s]/100.+1 for s in phpsnames)

        ## FIXME
        if newsysdict["CMS_psv"][0]>1.5  or newsysdict["CMS_psv"][1]>1.5:
            newsysdict["CMS_psv"]  = None


        ## ph energy
        newsysdict["CMS_ph_scale"]  = tuple(sysdict[s]/100.+1 for s in phennames)

        ## mu ID
        if ch == "mu":
            newsysdict["CMS_mu_eff"]  = tuple(sysdict[s]/100.+1 for s in muidnames)

        ## el ID
        if ch == "el":
            newsysdict["CMS_el_eff"]  = tuple(sysdict[s]/100.+1 for s in elidnames)

        ## mu scale
        if ch == "mu":
            newsysdict["CMS_mu_scale"]  = tuple(sysdict[s]/100.+1 for s in muennames)

        ## el scale
        if ch == "el":
            newsysdict["CMS_el_scale"]  = tuple(sysdict[s]/100.+1 for s in elennames)

        ## prefiring
        newsysdict["CMS_pref"]  = tuple(sysdict[s]/100.+1 for s in prefnames)

        ## renormalization/factorization scales
        qcdscales = [sysdict[s]/100.+1 for s in qcdscalenames]
        newsysdict["qcd_scale"]  = ( max(qcdscales), min(qcdscales) )
        
        ## PDF variations (NNPDF3.0 -> take RMS as uncertainty)
        import numpy as np
        pdfvars = [sysdict[s]/100.+1 for s in pdfnames]
        if yr == 2016:
            # 2016 samples produced with NNPDF30_lo_as_0130_nf_4
            # Variations are from NNPDF30_lo_as_0130 (replicas)
            width = np.std(pdfvars/np.mean(pdfvars))
            newsysdict["pdf"] = ( 1.+width, 1.-width )
        else:
            # 2017/2018 samples produced with NNPDF31_nnlo_as_0118_nf_4
            # Variations are from NNPDF31_nnlo_hessian_pdfas.LHgrid
            # SetDesc: "Hessian conversion of NNPDF31_nnlo_as_0118_1000, mem=0 central value => Alphas(MZ)=0.118; mem=1-100 => PDF eig.; mem=101 => central value Alphas(MZ)=0.116; mem=102 => central value Alphas(MZ)=0.120"
            pdfsyst2 = 0.
            pdfcentral = pdfvars[0]
#            for i in range(101):
#                shift = abs(pdfvars[i]/pdfcentral - 1.)
#                pdfsyst2 += shift**2
#            newsysdict["pdf"] = ( 1.+np.sqrt(pdfsyst2), 1.-np.sqrt(pdfsyst2) )
            for i in range(101):
                shift = abs(pdfvars[i]/pdfcentral - 1.)
                pdfsyst2 += shift**2
            newsysdict["pdf"] = ( 1.+np.sqrt(pdfsyst2), 1.-np.sqrt(pdfsyst2) )            

        return newsysdict

# ---------------------------------------------------


    @f_Dumpfname
    def get_combine_files( self ) :

        if self.fail :
            print('Initialzation failed, will not setup')
            return []

        print("all cards: ")
        pprint(self.allcards)
        print(("method: ",     self.method))
        print(("outputDir: ",  self.outputDir))

        jobs, output_files = self.write_combine_files()

        self.output_files = output_files

        return jobs



# ---------------------------------------------------

    ## FIXME move to SampleInfo

# ---------------------------------------------------


    @f_Dumpfname
    def generate_all_cards( self ):

        for width in self.widthpoints:

            for mass in self.masspoints:

                outputdir = self.outputDir + '/' + 'Width' + width + '/' + 'all' + '/' + 'Mass%i' %mass
                if not os.path.isdir( outputdir ) :
                   print((" creating directory", outputdir))
                   os.makedirs( outputdir )

                for obin in self.bins:
                    suboutputdir = self.outputDir + '/' + 'Width' + width + '/' + binid(obin) + '/' + 'Mass%i' %mass
                    if not os.path.isdir( suboutputdir ) :
                       print((" creating directory", suboutputdir))
                       os.makedirs( suboutputdir )
                    cuttag = defs.selectcuttag(mass,obin["year"]) ## returns A, B, C

                    sigpar = "_".join( ['M'+ str(mass), 'W'+width] )

                    card_path = '%s/wgamma_test_%s_%s_%s%s.txt' %(suboutputdir, self.var, sigpar, binid(obin),targetfunc )

                    self.generate_card( card_path, sigpar, cuttag = cuttag , obin = obin, imass=int(mass), iwid=width)

                    self.allcards[sigpar+"_"+binid(obin)] =  card_path

                cuttag = defs.selectcuttag(mass,obin["year"]) ## returns A, B, C

                sigpar = "_".join( ['M'+ str(mass), 'W'+width] )

                card_path = '%s/wgamma_test_%s_%s%s.txt' %(outputdir, self.var, sigpar,targetfunc )

                self.generate_card( card_path, sigpar, cuttag = cuttag , imass=int(mass), iwid=width)

                self.allcards[sigpar + '_all'] =  card_path




# ---------------------------------------------------


    @f_Dumpfname
    def generate_card( self, outputCard, sigpar,  tag='base' , cuttag = "", obin = None, imass = 300, iwid='0p01') :
        """

            generates card
            input:
                outputCard      output card?
                sigpar          list of signal parameters
                tag             tag (still used?)
                cuttag          tag for cutset used (for background shape)
            output:
                none

        """
        def sysstr(svalues):
            if svalues == None or isinstance(svalues, defaultdict):
                return "-"
            if isinstance(svalues,tuple):
                return "%.3f/%.3f" %svalues
            else:
                return "%.3f" %svalues

        card_entries = []
        viablebins , viablesig= [], []

        section_divider = '-'*100

        if obin == None:
            binlist = self.bins
        if isinstance( obin, dict):
            binlist = [obin,]

        ## check if signal channel exists
        #for ibin in self.bins :
        for ibin in binlist :
            sig = self.signals.get(sigpar+"_"+ibin['channel']+str(ibin['year']))
            if not sig: ## model not exist: exclude them for now
                print(("WARNING MODEL NOT EXIST: ", sigpar, ibin))
                continue
            viablebins.append(ibin)
            viablesig.append((ibin, sig))

        ############################################
        ##  channel declaration
        ##
        ##  imax 6 number of bins
        ##  jmax * number of backgrounds
        ##  kmax * number of nuisance parameters
        ############################################
        card_entries.append( 'imax %d number of bins' %len( viablebins ) )
        card_entries.append( 'jmax * number of backgrounds' )
        card_entries.append( 'kmax * number of nuisance parameters' )
        #card_entries.append( 'jmax %d number of backgrounds' %len( self.backgrounds) ) ## optional now

        card_entries.append( section_divider )

        max_name_len = max( [len(x) for x in self.bkgnames ] )
        max_path_len = max( [len(x.GetOutputName(self.outputDir, **ibin)) for x in list(self.backgrounds.values()) for ibin in binlist] )

        all_binids = []
        #signal_norm = 1.0

        ############################################
        ##  shape decaration
        ##  num of lines: (SIG+BKG+DATA=1)XCH
        ##
        ##  shapes Resonance mu_2016 2016/wssignal_M350_W5_mu.root ws:cbmu2016
        ##  shapes Resonance el_2016 2016/wssignal_M350_W5_el.root ws:cbel2016
        ##  shapes Resonance mu_2018 2018/wssignal_M350_W5_mu.root ws:cbmu2018
        ##  shapes WGamma el_2018    higgs/dijet.root ws:dijet_mu2016_wgamma
        ##  shapes data_obs el_2018  higgs/wtoydata.root ws:toydata_mu2016
        ############################################



        for ibin, sig in viablesig:
            bin_id = binid(ibin)
            all_binids.append(bin_id)
            if self.noShapeUnc:
                card_entries.append( 'shapes Resonance %s %s %s:%s'\
                  #%( bin_id, sig['file'], sig['workspace'], sig['pdf'] ) ) 
                  %( bin_id, sig['file'].replace('/data/users/yihuilai/test_code/WG_Analysis_clean_clean/Plotting/data/wg/','.'), sig['workspace'], sig['pdf'] ) ) # For exo-datacards -- Yihui
            else:
                card_entries.append( 'shapes Resonance %s %s %s:%s %s:%s'\
                  %( bin_id, sig['file'], sig['workspace'], sig['pdf'], sig['workspace'], sig['pdf_sys'] ) )

        for ibin in viablebins:
            bin_id = binid(ibin)
            for bkgname, bkg in list(self.backgrounds.items()) :
                ### BKG X CH
                if options.useHistTemp :
                    bkg_entry = bkg_entry.replace('dijet', 'datahist' )
                card_entries.append( 'shapes %s %s %s %s:%s' %( bkgname.ljust( max_name_len ),
                    bin_id, 'data/'+str(ibin['year'])+'/workspace_all.root',bkg.GetWSName(),
                    #bin_id, bkg.GetOutputName(options.outputDir,**ibin).ljust( max_path_len ).replace('/data/users/yihuilai/test_code/WG_Analysis_clean_clean/Plotting/data/wg/','.'), bkg.GetWSName(), # For exo-datacards -- Yihui
                    #bin_id, bkg.GetOutputName(options.outputDir,**ibin).ljust( max_path_len ), bkg.GetWSName(),
                    bkg.GetPDFName( self.var , ibin['channel'] + cuttag, ibin['year']) ) )

        for ibin in viablebins:
            bin_id = binid(ibin)
            ###  DATA (=1) X CH
            #temp no toydata -- Yihui
            #data = self.datas[self.dataname+binid(ibin)]
            if options.usedata:
                card_entries.append( 'shapes data_obs %s %s %s:%s' %( bin_id, 'data/'+str(ibin['year'])+'/workspace_all.root', 'workspace_all', 'data_'+str(ibin['channel'])+'A'+str(ibin['year'])+'_mt_res_base' ) ) # For exo-datacards -- Yihui
                #card_entries.append( 'shapes data_obs %s %s %s:%s' %( bin_id, options.baseDir+'/'+sourceOfBKG+'/'+str(ibin['year'])+'/workspace_all.root', 'workspace_all', 'data_'+str(ibin['channel'])+'A'+str(ibin['year'])+'_mt_res_base' ) )
            else:
                card_entries.append( 'shapes data_obs %s %s %s:%s' %( bin_id, data['file'], data['workspace'], data['data'][cuttag] ) )


        card_entries.append( section_divider )

        ############################################
        ##  channel declaration
        ##
        ##  imax 6 number of bins
        ##  jmax * number of backgrounds
        ##  kmax * number of nuisance parameters
        ############################################

        card_entries.append( 'bin          ' + listformat( all_binids ) )
        card_entries.append( 'observation  ' + listformat( [-1.]*len(all_binids) ,form="%-13g ") )

        card_entries.append( section_divider )
        ############################################
        ##  rate declaration
        ##  column: CH X (BKG + Data=1)
        ##
        ##  bin      mu_2016    mu_2016     el_2016     el_2016
        ##  process  Resonance  WGamma      Resonance   WGamma
        ##  process  0          1           0           1
        ##  rate     670611     4915        515811      4915
        ############################################

        rate_entries = []
        for ibin, sig in viablesig :
            # bin_id = '%s_%s' %( ibin['channel'], ibin['eta'] )
            #bin_id = "_".join(str(ibin.values()))
            bin_id = binid(ibin)

            # signal rate
            # use signal _norm to normalize signal distributions
            #rate_entries.append( str(1.0) )
            #sig = self.signals.get(sigpar+"_"+ibin['channel']+str(ibin['year']))
            #if not sig: ## model not exist
            #    continue
            rate_entries.append( sig['rate'] )
            #for bkgdic in self.backgrounds :
            for bkgname, bkg in list(self.backgrounds.items()):
                #rate_entries.append( str(bkgdic['norm'][bin_id]) )
                jbin = ibin['channel']+cuttag+str(ibin["year"])
                #print jbin
                #rate_entries.append( bkg.norm[jbin][0] )
                #bkg rate set to 1 --Yihui
                rate_entries.append( 1.0 )

        bin_entries = []
        for b in all_binids :
            bin_entries += [b]*(len(self.backgrounds)+1)

        card_entries.append( 'bin         ' + listformat(bin_entries )  )
        card_entries.append( 'process     ' + listformat((['Resonance'] + [x for x in self.bkgnames])*len(viablebins) ) )
        card_entries.append( 'process     ' + listformat( list(range(len(self.backgrounds) +1))*len(viablebins), form = "%-14d" ) )
        #card_entries.append( 'rate     ' + '    '.join( [str(signal_norm), str(backgrounds[0]['norm']) ]*len(bins) ) )
        card_entries.append( 'rate        ' + listformat( rate_entries,"%-13g " )  )
        card_entries.append( section_divider )
        ############################################
        ##  systematics declaration
        ##
        ##  lumi       lnN    1.025    1.0250
        ##  met        lnN    1.03    -    1.03    -    1.03    -    1.03    -
        ##  pdf        lnN    1.05    -    1.05    -    1.05    -    1.05    -
        ##  cms_e      shape  1.00    -    1.00    -    1.00    -    1.00    -
        ##  dijet_order1_el2018_wgamma flatParam
        ##  dijet_order2_el2018_wgamma flatParam
        ##  cb_cut1_MG_M350_W5_mu2016 param 0.60000 0.00005
        ##  cb_mass_MG_M350_W5_mu2016 param 329.58155 0.06551
        ############################################

        syslist = set()
        for ibin, sig in viablesig:
            syslist.update(list(sig["sys"].keys()))

        syslist = list(syslist)
        for sn in syslist:
            sys_line = [sn, "lnN"]

            for ibin, sig in viablesig:
                bin_id = binid(ibin)

                sigsysstr = sysstr(sig["sys"][sn])

                sys_line.append(sigsysstr)

                for bkgname, bkg in list(self.backgrounds.items()):
                    bkgsysstr = sysstr(bkg.sys[bin_id][cuttag].get(sn))
                    if options.NoBKGUnc:
                        sys_line.append('-')
                    else:
                        sys_line.append(bkgsysstr)
            #FIXME Yihui -- comment out for no syst
            card_entries.append( listformat(sys_line, "%-15s"))

        ## hard coded shape uncertainty
        sys_line = ["cms_e", "shape"]
        for ibin, sig in viablesig:
            bin_id = binid(ibin)
            sys_line.append("1.00")

            for bkgname, bkg in list(self.backgrounds.items()):
                sys_line.append('-')
        if not self.noShapeUnc: card_entries.append( listformat(sys_line, "%-15s"))


        #lumi_vals = ["%-13g "%1.025] * (len(all_binids)*( len(self.backgrounds) + 1 ))
        ##lumi_vals = ['1.025'] + [ '1.025' if bkg.useLumi else '-' for bkg in self.backgrounds.values() ]
        #bkg_vals = (['-'+' '*13] + ["%-13g " %1.20]*len(self.backgrounds) )*len(all_binids)
        #signal_met = ( ["%-13g " %1.03] + ['-'+' '*13]*len(self.backgrounds) )*len( all_binids)
        #signal_pdf = ( ["%-13g " %1.05] + ['-'+' '*13]*len(self.backgrounds) )*len( all_binids)

        #card_entries.append( 'lumi  lnN   ' + ''.join(lumi_vals) )
        ##card_entries.append( 'bkgelse   lnN    ' + '    '.join(bkg_vals    ) )
        #card_entries.append( 'met   lnN   ' + ''.join(signal_met) )
        #card_entries.append( 'pdf   lnN   ' + ''.join(signal_pdf) )

        ## assign 30% normalization uncertainty in all backgrounds from data-driven
        #for bkgname in self.backgrounds:
        #    if not self.backgrounds[bkgname].useLumi:
        #       bkg_norms = ['-'] + ['1.30' if namebkg == bkgname else '-' for namebkg in self.backgrounds]
        #       card_entries.append('%s_norm lnN    '%bkgname + '    '.join( bkg_norms ))

        #Yihui -- use MultiPdf
        looplist=[]
        if 'mu2016' in outputCard: looplist.append('muA2016')
        elif 'mu2017' in outputCard: looplist.append('muA2017')
        elif 'mu2018' in outputCard: looplist.append('muA2018')
        elif 'el2016' in outputCard: looplist.append('elA2016')
        elif 'el2017' in outputCard: looplist.append('elA2017')
        elif 'el2018' in outputCard: looplist.append('elA2018')
        elif 'all' in outputCard: looplist = ['elA2016','elA2017','elA2018','muA2016','muA2017','muA2018']
        #elif 'all' in outputCard: looplist = ['elA2018','muA2018','elA2017','muA2017']
        else: exit()
        for ich in looplist:
            if ich =='elA2016' or ich =='elA2018' :
                varnames=['vvdijet_order1__all_vvdijet','vvdijet_order2__all_vvdijet','dijet_order1__all_dijet','dijet_order2__all_dijet','expow_order1__all_expow','expow_order2__all_expow']
            else:
                varnames=['vvdijet_order1__all_vvdijet','vvdijet_order2__all_vvdijet','dijet_order1__all_dijet','dijet_order2__all_dijet','expow_order1__all_expow','expow_order2__all_expow','expow_order3__all_expow','vvdijet_order3__all_vvdijet']
            varnames=['vvdijet_order1__all_vvdijet','vvdijet_order2__all_vvdijet','dijet_order1__all_dijet','dijet_order2__all_dijet','expow_order1__all_expow','expow_order2__all_expow'] # All order 2
            varnames=['vvdijet2_order1__all_vvdijet','vvdijet2_order2__all_vvdijet','dijet2_order1__all_dijet','dijet2_order2__all_dijet','expow2_order1__all_expow','expow2_order2__all_expow',
            #    'vvdijet3_order1__all_vvdijet','vvdijet3_order2__all_vvdijet','dijet3_order1__all_dijet','dijet3_order2__all_dijet','expow3_order1__all_expow','expow3_order2__all_expow','vvdijet3_order3__all_vvdijet','dijet3_order3__all_dijet','expow3_order3__all_expow',   # order3
            #    'vvdijet4_order1__all_vvdijet','vvdijet4_order2__all_vvdijet','dijet4_order1__all_dijet','dijet4_order2__all_dijet','expow4_order1__all_expow','expow4_order2__all_expow','vvdijet4_order3__all_vvdijet','dijet4_order3__all_dijet','expow4_order3__all_expow','vvdijet4_order4__all_vvdijet','dijet4_order4__all_dijet','expow4_order4__all_expow',  #order 4
            #    'vvdijet1_order1__all_vvdijet','dijet1_order1__all_dijet','expow1_order1__all_expow' #order1
            ] 
            for ivar in varnames:
                card_entries.append( ivar.replace('__all','_'+ich+'_all') +'  flatParam')
            card_entries.append('pdf_index_%s                             discrete'%(ich.replace('A','')))

        #Yihui -- add shape uncertainty into signal mean mass uncertainty
        maxshift = 0
        minshift = 0
        if self.addShapeUnc2Mass:
            filepath = "data/sigfit/fitted_mass%i.txt" %ibin['year']
            with open(filepath, "r") as fo:
                mshifts = json.load(fo)
            w="5.0" if iwid=="5" else "0.01"
            maxshift = mshifts[ibin["channel"]]["%.1f"%int(imass)][w]["max"][1]
            minshift = mshifts[ibin["channel"]]["%.1f"%int(imass)][w]["min"][1]
        for ibin, sig in viablesig:
            #sig = self.signals.get(sigpar+"_"+ibin['channel']+str(ibin['year']))
            #if not sig: ## model not exist
            #    continue
            for iparname, iparval in list(sig['params'].items()):
                if iparval[1] != 0:
                   #Yihui --- use smooth signal model
                   if 'cb_mass_MG' in iparname and self.addShapeUnc2Mass:
                       card_entries.append('%s param %.5f %.5f'%(iparname, iparval[0], (ROOT.TMath.Sqrt(maxshift**2+ iparval[1]**2)+ ROOT.TMath.Sqrt(minshift**2+ iparval[1]**2))/2.0))
                   else:
                       card_entries.append('%s param %.5f %.5f'%(iparname, iparval[0], iparval[1]))
        
        card_entries.append( section_divider )

        if outputCard is not None :
            print(('Write file ', outputCard))
            ofile = open( outputCard, 'w' )
            for line in card_entries :
                ofile.write( line + '\n' )
            ofile.close()
        else :
            for ent in card_entries :
                print(ent)




# ---------------------------------------------------


    @f_Dumpfname
    def generate_toy_data( self,  sigpars=None, signorms = None, data_norm=None ) :

        if not os.path.isdir( self.outputDir+'/'+self.dataname ) :
           print((" creating directory %s/%s"%(self.outputDir, self.dataname)))
           os.makedirs( self.outputDir+'/'+self.dataname )


        ##loop over bins
        for ibin in self.bins :
            ## background
            for bkgname, bkg in list(self.backgrounds.items()):
                self.generate_toy_data_helper( ibin, bkgname, bkg,
                                        sigpars, signorms, data_norm)



# ---------------------------------------------------


    def generate_toy_data_helper( self, ibin, bkgname, bkg,
                                  sigpars=None, signorms = None, data_norm=None ) :

       workspace = ROOT.RooWorkspace( '_'.join(['workspace', self.dataname, binid(ibin)]) )


       datasetname={}

       #if bkgname != 'WGamma':
       #   print "[ \033[1;31mProblem running the toy data generation process. Skip %s. Only play with WGamma for now\033[0m  ]"%bkgname
       #   continue

       #full_path = bkg['file']
       #ofile = ROOT.TFile.Open( full_path )
       # FIXME print "bkg.outputfname", bkg.outputfname
       ofile = ROOT.TFile.Open( bkg.GetOutputName( self.outputDir ,**ibin) )

       #ws = ofile.Get( bkg['workspace'] )
       ws = ofile.Get( bkg.GetWSName() )
       print((bkg.GetOutputName( self.outputDir ,**ibin ), ":", bkg.GetWSName( )))
       print((ofile, ws))

       for cutset in self.cutsetlist:
           pdfs = []
           norms = []
           xvar = None
           jbin = ibin.copy()
           jbin['channel'] += cutset ## add cutset tag
           suffix = "%s_%s_%s"%(binid(jbin), self.var, self.wstag)

           if options.useHistTemp :
               print(hist_key)
               pdfs.append(ws.data( hist_key ))
               norms.append(pdfs[-1].sumEntries())
           else :
               #norms.append( ws.var( '%s_norm'%bkg['pdf'] ).getVal() )
               #pdfs.append(  ws.pdf( bkg['pdf'] ) )
               #norms.append( ws.var('%s_norm'%bkg.GetPDFName(self.var, self.bins[0]['channel'])).getVal() )
               norms.append( bkg.norm[binid(jbin)][0] )
               print((bkg.GetPDFName(self.var, **jbin)))
               ws.Print()
               pdfs.append( ws.pdf( bkg.GetPDFName(self.var, **jbin)) )

           if xvar is None :
               xvar = ws.var( self.xvarname )
           xvar.setRange( 230 ,2300)
           #xvar.setRange( defs.bkgfitlowbin(cutset) ,2200)
           xvar.setBins(500)
           xvar.Print()

           ofile.Close()

           ## mix into some fake signal
           if sigpars:
              print("add some fake signals for fun...")
              for sigpar, signorm in zip(sigpars, signorms):
                  try:
                      sig = self.signals[sigpar+str(ibin['year'])]
                      print(("sig: ", sig))
                      ofile = ROOT.TFile.Open( sig['file'] )
                  except:
                      print((list(self.signals.keys())))
                      print(("can not open the signal workspace file: "\
                            "%s Please x-check self.signals collection"\
                                %self.signals[sigpar]['file']))
                      raise
                  print((sigpar, sig['file'], sig['pdf']))

                  ## escape if pdf name is set to $PROCESS or other higgscombine shorthand
                  pdfname = "Resonance" if "$" in sig['pdf'] else sig['pdf']

                  wssig = ofile.Get( sig['workspace'] )
                  pdfs.append( wssig.pdf( pdfname ) )
                  #norms.append( wssig.var( '%s_norm'%sig['pdf']).getVal() * signorm )
                  norms.append( sig['rate']*signorm)

           print(("Normalization:: ", norms))

           if len( pdfs ) == 1 :
               ### there is only 1 pdf. save toy data
               if options.useHistTemp :
                   dataset = ROOT.RooDataHist( pdfs[0], 'toydata_%s' %suffix )
               else :
                   if data_norm is None :
                       norm = int(norms[0])
                   else :
                       norm = data_norm
                   print(("toy data #: ",norm))
                   dataset = pdfs[0].generate(ROOT.RooArgSet(xvar) , int(norm),
                             ROOT.RooCmdArg( 'Name', 0, 0, 0, 0,
                                             'toydata_%s' %suffix ) )
           else :
               print(("norms: ", norms))
               total = sum( [int(x) for x in norms ] )

               fractions = [ float(x)/total for x in norms ]

               print(("total ", total, " fractions", fractions))

               if options.useHistTemp :

                   dataset = ROOT.RooDataHist( pdfs[0], 'toydata_%s' %suffix )

                   for pdf in pdfs[1:] :
                       dataset.add( pdf )

               else :
                   print("**** start generate toy data *****")
                   pdfList = ROOT.RooArgList()
                   print(pdfs)
                   for p in pdfs :
                       p.Print()
                       pdfList.add( p )

                   fracList = ROOT.RooArgList()
                   idx = 0
                   myvar = []
                   for f in fractions[:-1] :
                   #for f in fractions:
                       #myvar = ROOT.RooRealVar( str(uuid.uuid4()), str(uuid.uuid4()), f, 0,  f )
                       myvar.append( ROOT.RooRealVar("fraction_%d"%idx, "fraction_%d"%idx, f, 0, f) )
                       fracList.add( myvar[idx] )
                       idx += 1

                   pdfList.Print()
                   print(fracList)
                   summed = ROOT.RooAddPdf( 'summed' ,'summed', pdfList , fracList )
                   print(("xvar", xvar))
                   dataset = summed.generate( ROOT.RooArgSet(xvar), int(total),
                                              ROOT.RooCmdArg( 'Name', 0, 0, 0, 0,
                                                        'toydata_%s' %suffix ) )

           import_workspace( workspace, dataset)
           datasetname[cutset]=dataset.GetName()

       outputfile = '%s/%s/%s.root' %( self.outputDir, self.dataname, workspace.GetName() )

       workspace.writeToFile( outputfile )

       self.datas.update(
                          { self.dataname+binid(ibin): { 'channel':
                              binid(ibin), 'file': outputfile, 'workspace':
                              workspace.GetName(), 'data': datasetname }
                              }
                        )



# ---------------------------------------------------


    @f_Dumpfname
    def prepare_background_functions( self ) :
        ##loop over bins
        for ibin in self.bins :
           ## loop over backgrounds
           for bkgn in self.bkgnames:
               self.prepare_background_functions_helper(bkgn, ibin)


    def prepare_background_functions_helper(self, bkgn, ibin):
        print((" prepare background functions for ", bkgn))

        fname = '%s/bkgfit/%i/%s' %( self.baseDir, ibin['year'],
                                     self.wskeys[bkgn].GetRootFileName() )
        #Use data as bkg template ---Yihui
        if options.usedata:
            fname = self.baseDir+'/'+sourceOfBKG+'/%i/%s' %( ibin['year'],
                                         self.wskeys[bkgn].GetRootFileName() )
        ofile = ROOT.TFile.Open( fname , 'READ' )

        ws_in = ofile.Get( self.wskeys[bkgn].GetWSName() )

        ws_out = ROOT.RooWorkspace( self.wskeys[bkgn].GetWSName() )

        var = ws_in.var(self.var)
        # Yihui -- set x range 
        #var.setRange( 220 ,2000)
        #var.setBins(500)
        import_workspace( ws_out, var)

        for cutset in self.cutsetlist:

            #suffix = "_".join([bkgn, self.bins[0]['channel'], self.var, self.wstag, self.bins[0]['eta']])

            #ws_entry = "_".join( [self.wskeys[bkgn].pdf_prefix, suffix])
            jbin = ibin.copy()
            jbin['channel'] += cutset ## add cutset tag

            ws_entry = self.wskeys[bkgn].GetPDFName( self.var, **jbin)

            if DEBUG:
               print(ws_entry)

            if options.useHistTemp :
                datahist = ws_in.data(ws_entry.replace('dijet', 'datahist') )
                import_workspace( ws_out, datahist)
            else :
                pdf = ws_in.pdf( ws_entry )
                for ipar in self.wskeys[bkgn].GetParNames( **jbin):
                    #Yihui --- create WS for para of bkg
                    #correlated channels
                    #ipar=ipar.replace("mu",'')
                    #ipar=ipar.replace("el",'')
                    #ipar=ipar.replace("2016",'')
                    #ipar=ipar.replace("2017",'')
                    #ipar=ipar.replace("2018",'')
                    if DEBUG:
                       print(ipar)
                    oldvar = ws_in.var( ipar )
                    varrange = (-50, -0.01)
                    varsetvalue = -3.4
                    if 'vvdijet_order1' in ipar:
                        varrange = (-50, -0.01)
                        varsetvalue = -3.4
                    elif 'vvdijet_order2' in ipar:
                        varrange = (0.01, 50)
                        varsetvalue = 9.8
                    elif 'vvdijet_order3' in ipar:
                        varrange = (0.01, 50)
                        varsetvalue = 1.9
                    elif 'vvdijet_order4' in ipar:
                        varrange = (-20, 20.0)
                        varsetvalue = -0.000531
                    if 'dijet' in ipar and 'vvdijet' not in ipar:
                        if 'order1' in ipar:
                            varrange = (-50.0, -0.01)
                            varsetvalue = -7.5
                        elif 'order2' in ipar:
                            varrange = (-10.0, -0.01)
                            varsetvalue = -0.58
                        elif 'order3' in ipar:
                            varrange = (0.01, 10)
                            varsetvalue = 0.27
                        elif 'order4' in ipar:
                            varrange = (-10.0, 50)
                            varsetvalue = -0.01
                    var =  ROOT.RooRealVar( ipar, ipar, varsetvalue, varrange[0], varrange[1] )
                    #print oldvar
                    # save the value and errors of the fit parameters, to be used for card generation
                    self.params.update( {ipar: (oldvar.getVal(), oldvar.getError())} )
                    #var.setError(0.0)
                    if not self.noShapeUnc: var.setError(oldvar.getError())
                    #var.setConstant()
                    import_workspace( ws_out, var)
                print(("%s_norm" %ws_entry))
                norm_var = ws_in.var( '%s_norm'% ws_entry.replace(self.wskeys[bkgn].pdf_prefix,'MultiPdf') )
                print(("norm ", norm_var.getVal()))
                self.wskeys[bkgn].SetNorm( norm_var.getVal(), norm_var.getError() , cuttag = binid(jbin))
                print(("SampleInfo.norm: ", self.wskeys[bkgn].norm))
                #norm_var.setError( 0.3*norm_var.getValV() )
                #norm_var.setVal( norm_var.getValV() )
                #norm_var.setError( 0.0 )
                #norm_var.setConstant()
                getattr( ws_out, 'import' ) ( norm_var )
                import_workspace( ws_out, pdf)

        #outputfile = '%s/%s/%s.root' %( self.outputDir, bkgn, ws_out.GetName() )
        #ws_out.writeToFile( outputfile )
        outputname = self.wskeys[bkgn].GetOutputName( self.outputDir , **ibin)
        ws_out.writeToFile( outputname )

        ## infor for generating toy data and datacard
        #self.backgrounds.update(
        #                       { bkgn: { 'channel': "%s_%s"%(self.bins[0]['channel'], self.bins[0]['eta']), 'file': outputfile, 'workspace': ws_out.GetName(), 'pdf': pdf.GetName(), 'params': params} }
        #                       )
        self.backgrounds.update( { bkgn: self.wskeys[bkgn]} )
        print(("BACKGROUND: ",self.backgrounds))



# ---------------------------------------------------


    @f_Dumpfname
    def prepare_signal_functions( self) :


        for mass in self.masspoints:
            for width in self.widthpoints:
                for ibin in self.bins :
                    self.prepare_signal_functions_helper( mass, width, ibin )


# ---------------------------------------------------


    def prepare_signal_functions_helper( self, mass, width, ibin ) :

        sigpar = "_".join(['M'+str(mass), 'W'+str(width), binid(ibin)])
        inpar = "_".join(['M'+str(mass), 'W'+str(width), ibin['channel']])

        ## get the cross section and scale factor information
        scale = self.weightMap['ResonanceMass%d'%mass]['cross_section'] * lumi(ibin)

        fname= '%s/sigfit/%i/ws%s_%s.root' %( self.baseDir, ibin['year'], self.signame, inpar )
        if options.paramodel :
            print("will use the parameterized model! ")
            fname= '%s/sigfit_para/%i/ws%s_%s.root' %( self.baseDir, ibin['year'], self.signame, inpar )
        wsname = "ws" + self.signame + '_' + inpar
        if DEBUG:
            print((fname, " : ", wsname))
        ifile = ROOT.TFile.Open( fname, 'READ' )
        if not ifile:
            print(("skipping ", fname))
            return


        ws_in = ifile.Get( wsname )

        ws_out = ROOT.RooWorkspace( "workspace_" + self.signame + '_' + sigpar )

        sigfitparams = OrderedDict()

        suffix = sigpar
        ws_entry = "_".join([self.wskeys[self.signame].pdf_prefix, suffix])
        ws_entry_sysdown = "_".join([self.wskeys[self.signame].pdf_prefix, suffix, "down"])
        ws_entry_sysup   = "_".join([self.wskeys[self.signame].pdf_prefix, suffix, "up"])

        ## open json file for shifted mean value
        if not self.noShapeUnc:
            filepath = "data/sigfit/fitted_mass%i.txt" %ibin['year']
            #if options.paramodel :
            #    filepath = "data/sigfit_para/fitted_mass%i.txt" %ibin['year']
            with open(filepath, "r") as fo:
                mshifts = json.load(fo)
            w="5.0" if width=="5" else "0.01"
            maxshift = mshifts[ibin["channel"]]["%.1f"%mass][w]["max"][1]
            minshift = mshifts[ibin["channel"]]["%.1f"%mass][w]["min"][1]

        if DEBUG:
           print(ws_entry)

        ## Resonance mass shift
        pdf = ws_in.pdf( ws_entry )
        pdf.SetName("Resonance")


        for ipar in self.wskeys[self.signame].params_prefix:
            if DEBUG:
               print((ipar+ '_' + suffix))
            var = ws_in.var( ipar  + '_' + suffix )
            sigfitparams.update( {ipar + '_' + suffix: (var.getVal(), var.getError())} )
            #var.setError(0.0)
            #var.setConstant()
            import_workspace( ws_out, var)

        var = ws_in.var(self.var)
        #var.setRange(200,2000)
        var.setBins(360)
        import_workspace( ws_out, var)

        norm_var = ws_in.var( '%s_norm' %ws_entry )

        rate = norm_var.getVal() * scale
        #don't need if use para signal model -- Yihui
        #if("%s_%s_%s"%(str(mass),width,ibin['year']) in N_tot):
        #    rate = rate* 50000.0/N_tot["%s_%s_%s"%(str(mass),width,ibin['year'])]
        print((tPurple%("norm %g scale %g rate %g" \
                                   %(norm_var.getVal(),scale,rate))))
      #  norm_var.setVal( norm_var.getValV() * scale )
      #  norm_var.setError( norm_var.getError() * scale )
      #  #norm_var.setError(0.0)
      #  #norm_var.setConstant( False )
      #  norm_var.setConstant()
        import_workspace( ws_out, pdf )

        if not self.noShapeUnc:
            full_suffix = "_".join(['MG', "M%d"%mass, 'W%s'%width, binid(ibin)])
            ## UP variation
            exprstr = "expr::cb_mass_{tag}_UP('cb_mass_{tag}*cb_mass_{tag}_shift_UP',"\
                       "cb_mass_{tag},cb_mass_{tag}_shift_UP[{maxshift}])".format(tag = full_suffix,
                                                                                  maxshift = maxshift)
            print((tPurple%exprstr))
            ws_out.factory(exprstr)

            exprstr = "RooDoubleCB::Resonance_cms_eUp(mt_res,cb_mass_{tag}_UP,cb_sigma_{tag},"\
                  "cb_cut1_{tag},cb_power1_{tag}, cb_cut2_{tag}, cb_power2_{tag})".format(tag=full_suffix)
            print((tPurple%exprstr))
            ws_out.factory(exprstr)

            # DOWN variation
            exprstr = "expr::cb_mass_{tag}_DN('cb_mass_{tag}*cb_mass_{tag}_shift_DN',"\
                       "cb_mass_{tag},cb_mass_{tag}_shift_DN[{minshift}])".format(tag = full_suffix,
                                                                            minshift = minshift)
            print((tPurple%exprstr))
            ws_out.factory(exprstr)

            exprstr = "RooDoubleCB::Resonance_cms_eDown(mt_res,cb_mass_{tag}_DN,cb_sigma_{tag},"\
                  "cb_cut1_{tag},cb_power1_{tag}, cb_cut2_{tag}, cb_power2_{tag})".format(tag=full_suffix)
            print((tPurple%exprstr))
            ws_out.factory(exprstr)

        ifile.Close()

        outputfile = '%s/%s/%s.root' %( self.outputDir, self.signame, ws_out.GetName() )
        ws_out.writeToFile( outputfile )


        ## info for generating toy data and datacard
        self.signals.update( {sigpar : {'channel': binid(ibin),
                                'file': outputfile,
                                'workspace': ws_out.GetName(),
                                #'pdf': pdf.GetName(),
                                'pdf': "$PROCESS",
                                'pdf_sys': "$PROCESS_$SYSTEMATIC",
                                'rate': rate,
                                'params': sigfitparams} }
                            )




# ---------------------------------------------------


    @f_Dumpfname
    def make_gauss_signal(self,  normvalue, ibin) :

        for mass in self.masspoints:
            for width in self.widthpoints:
                sigpar = "_".join(['Mass', str(mass), 'Width', width])

                ## one workspace/rootfile for one signal grid point
                #workspace = ROOT.RooWorkspace( 'workspace_' + self.signame +
                #'_Mass' + str(mass) + '_Width' + width )
                workspace = ROOT.RooWorkspace( "_".join(['workspace',
                    self.signame, sigpar]) )


                suffix = "_".join([sigpar, self.bins[0]['channel'], self.var,
                    self.wstag, self.bins[0]['eta']])

                if DEBUG:
                   print(suffix)

                xvar = ROOT.RooRealVar( self.xvarname, self.xvarname,
                        var['range'][0], var['range'][1] )

                mean = ROOT.RooRealVar( 'mean_%s' %suffix, 'mean', mass )
                sigma = ROOT.RooRealVar( 'sigma_%s' %suffix, 'sigma',
                        mass*Width_str2float(width)*0.01 )
                mean.setConstant()
                sigma.setConstant()

                norm = ROOT.RooRealVar( 'gauss_%s_norm' %suffix,
                        'normalization', normvalue )
                norm.setConstant()

                signal = ROOT.RooGaussian( 'gauss_%s' %suffix, 'signal', xvar,
                        mean, sigma )

                #getattr( workspace, 'import' ) ( dataset,
                #ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'gaussignal_%s' %suffix ) )
                import_workspace( workspace, [signal, norm] )

                outputfile = '%s/%s/%s.root' %( self.outputDir, self.signame,
                        workspace.GetName() )
                workspace.writeToFile( outputfile )

                self.signals.update(
                 {sigpar : {'channel':    binid(ibin), 
                            'file':       outputfile,
                            'workspace':  workspace.GetName(),
                            'pdf':        signal.GetName() } } )




# ---------------------------------------------------


    @f_Dumpfname
    def make_exp_background(self, expvalue, normvalue ) :

        workspace= ROOT.RooWorkspace( "workspace_%s"%self.bkgnames[0] )


        suffix = "%s_%s_%s_%s"%(self.bins[0]['channel'], self.var, self.wstag,
                self.bins[0]['eta'])

        if DEBUG:
           print(suffix)

        xvar = ROOT.RooRealVar( self.xvarname, self.xvarname,  var['range'][0],
                var['range'][1])

        # parameters of p.d.f must be set to constant, otherwise the combine tool would yield weird result
        power = ROOT.RooRealVar( 'power_%s' %suffix, 'power', expvalue )
        power.setConstant()

        background = ROOT.RooExponential( 'exp_%s' %suffix, 'background', xvar, power )
        norm = ROOT.RooRealVar( 'exp_%s_norm' %suffix,
                                'background normalization', normvalue )
        #norm.setError(10.0)
        norm.setError(0.0)
        norm.setConstant()

        #getattr( workspace, 'import' ) ( dataset,
        #ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'gaussignal_%s' %suffix ))
        import_workspace( workspace, [background, norm] )

        outputfile = "%s/%s/%s.root"%( self.outputDir, self.bkgnames[0],
                workspace.GetName() )
        workspace.writeToFile( outputfile )

        ## infor for generating toy data and datacard
        self.backgrounds.update(
                                 {self.bkgnames[0]: { 'channel': binid(ibin),
                                  'file':           outputfile,
                                  'workspace':      workspace.GetName(), 
                                  'pdf':            background.GetName() } }
                               )


# ---------------------------------------------------


    def get_combine_command( self, sigpar, card, log_file):

        ### essential info
        wid = sigpar.split('_W')[1].split('_')[0]
        mass = int(sigpar.split('_')[0].lstrip("M"))

        ## generate commands
        if self.method == 'AsymptoticLimits' :
            command = ""

            ## flag to limit fit range
            mtrange=" --setParameterRanges mt_res=%i,%i" %self.fitrange(mass) if self.fitrange else ""

            if self.doImpact:
                # validation (not related to impact)
                command += "ValidateDatacards.py %s\n" %card
                command += "text2workspace.py %s -m %d \n" %(card, mass)

                card = card.replace(".txt",".root")
                impactcommand = "combineTool.py -M Impacts -d %s -m %d %s" %(card, mass, mtrange)
                command += "%s --doInitialFit --robustFit 1\n" %impactcommand
                command += "%s --doFits --robustFit 1 --parallel 10\n" %impactcommand
                command += "%s -o impacts.json \n" %impactcommand
                command += "plotImpacts.py -i impacts.json -o impacts_%s\n\n" %(sigpar)

            flagstr = ""
            if self.numberOfToys is not None: flagstr+=" -t %d"  %self.numberOfToys
            if options.usedata:
                flagstr+=" --run blind "
            if self.rmin is not None: flagstr+= " --rMin %.2g" %self.rmin
            if self.rmax is not None: flagstr+= " --rMax %.2g" %self.rmax
            if self.seed is not None: flagstr+= " -s %i" %self.seed

            if self.freezeParameter is not None:
                if self.freezeParameter == "all":
                    flagstr+=" --freezeParameters 'rgx{.*}'"
                elif self.freezeParameter == "sig":
                    flagstr+=" --freezeParameters 'rgx{cb_.*_MG_M.*_W.*}'"
                elif self.freezeParameter == "bkg":
                    flagstr+=" --freezeParameters 'rgx{dijet_order.*_all_dijet}'"
                elif self.freezeParameter == "s+b":
                    flagstr+=" --freezeParameters 'rgx{cb_.*_MG_M.*_W.*},rgx{dijet_order.*_all_dijet}'"
                elif self.freezeParameter == "constrained":
                    flagstr+=" --freezeParameters allConstrainedNuisances"
                else:
                    flagstr+=" --freezeParameters %s" %self.freezeParameter

            # Use all dijet2 or use envelope --Yihui
            flagstr+= mtrange
            useenve=False
            if useenve:
                command+= 'combine -M AsymptoticLimits -m %d %s %s >& %s'%( mass, flagstr, card, log_file )
            else:
                if '2016' in log_file:
                    command+= 'combine -M AsymptoticLimits --setParameters  pdf_index_el2016=2,pdf_index_mu2016=2 --freezeParameters pdf_index_el2016,pdf_index_mu2016 -m %d %s %s >& %s'%( mass, flagstr, card, log_file )
                elif '2017' in log_file:
                    command+= 'combine -M AsymptoticLimits --setParameters  pdf_index_el2017=2,pdf_index_mu2017=2 --freezeParameters pdf_index_el2017,pdf_index_mu2017 -m %d %s %s >& %s'%( mass, flagstr, card, log_file )
                elif '2018' in log_file:
                    command+= 'combine -M AsymptoticLimits --setParameters  pdf_index_el2018=2,pdf_index_mu2018=2 --freezeParameters pdf_index_el2018,pdf_index_mu2018 -m %d %s %s >& %s'%( mass, flagstr, card, log_file )
                else:
                    command+= 'combine -M AsymptoticLimits --setParameters  pdf_index_el2016=2,pdf_index_el2017=2,pdf_index_el2018=2,pdf_index_mu2016=2,pdf_index_mu2017=2,pdf_index_mu2018=2 --freezeParameters pdf_index_el2016,pdf_index_el2017,pdf_index_el2018,pdf_index_mu2016,pdf_index_mu2017,pdf_index_mu2018 -m %d %s %s >& %s'%( mass, flagstr, card, log_file )


            #do goodness of fit -- Yihui
            if options.GoF:
                #command = '\n combineTool.py -M GoodnessOfFit --algo=KS %s -n .KS  >& %s  \n' %(card, 'goodnessdata'+log_file)
                #command += 'combineTool.py -M GoodnessOfFit --algo=KS %s -n .KS  -t 500 -s 123  >& %s \n' %(card, 'goodnesstoy'+log_file)
                #command = '\n combineTool.py -M GoodnessOfFit --algo=saturated %s -n .saturated -v 3 >& %s \n' %(card, 'goodnessdata'+log_file)
                #command += 'combineTool.py -M GoodnessOfFit --algo=saturated %s -n .saturated -v 3 -t 500 -s 1234 --toysFreq  >& %s \n' %(card, 'goodnesstoy'+log_file)
                command =''
                #for i in range(9):
                for i in [0,4,8]:
                    command += '\n combineTool.py -M GoodnessOfFit --algo=KS '+card+' -n .KS  --fixedSignalStrength=0 --setParameters  pdf_index_'+log_file[-10:-4]+'='+str(i)+' --freezeParameters pdf_index_'+log_file[-10:-4]+' -n pdf'+str(i)
                    command += '\n combineTool.py -M GoodnessOfFit --algo=KS '+card+' -n .KS  --fixedSignalStrength=0 --setParameters  pdf_index_'+log_file[-10:-4]+'='+str(i)+' --freezeParameters pdf_index_'+log_file[-10:-4]+' -n t0pdf'+str(i)+' -t 100 -s 130 '


            if options.BiasStudy:
                #directly generate and fit
                command = '\n combine -d '+ card + ' -M GenerateOnly --setParameters  pdf_index_el2016='+genindex+',pdf_index_el2017='+genindex+',pdf_index_el2018='+genindex+',pdf_index_mu2016='+genindex+',pdf_index_mu2017='+genindex+',pdf_index_mu2018='+genindex+' --freezeParameters pdf_index_el2016,pdf_index_el2017,pdf_index_el2018,pdf_index_mu2016,pdf_index_mu2017,pdf_index_mu2018 --toysFrequentist -t '+str(ntoy)+' --expectSignal '+str(injectsignal)+' --saveToys -m '+str(mass) +' -s '+str(rseed) + ' -n ' + rname
                if fitindex!='-1':
                    command += '\n combine -d '+ card + ' -M FitDiagnostics  --setParameters pdf_index_el2016='+fitindex+',pdf_index_el2017='+fitindex+',pdf_index_el2018='+fitindex+',pdf_index_mu2016='+fitindex+',pdf_index_mu2017='+fitindex+',pdf_index_mu2018='+fitindex+'  --toysFile higgsCombine'+rname+'.GenerateOnly.mH'+str(mass)+'.'+str(rseed)+'.root  -t '+str(ntoy)+' --rMin -20 --rMax 20 --freezeParameters pdf_index_el2016,pdf_index_el2017,pdf_index_el2018,pdf_index_mu2016,pdf_index_mu2017,pdf_index_mu2018  --cminDefaultMinimizerStrategy=0' + ' -s '+str(rseed) + ' -n ' + rname
                else:
                    command += '\n combine -d '+ card + ' -M FitDiagnostics  --toysFile higgsCombine'+rname+'.GenerateOnly.mH'+str(mass)+'.'+str(rseed)+'.root  -t '+str(ntoy)+' --rMin -20 --rMax 20 --cminDefaultMinimizerStrategy=0' + ' -s '+str(rseed) + ' -n ' + rname
                #Fit with enve, and generate with envelope
                #command = '\n combineTool.py -M MultiDimFit -m '+str(mass)+' -d '+ card + ' --there --robustFit 1 --cminDefaultMinimizerStrategy 0 -v 3 --saveWorkspace --noMCbonly 1 --freezeParameters r --setParameters r=0  -n Envelope \n'
                #command += '\n combineTool.py '+ 'higgsCombineEnvelope.MultiDimFit.mH'+str(mass)+'.root ' + ' -M GenerateOnly --saveToys -m '+str(mass)+' --toysFrequentist -t %s --snapshotName "MultiDimFit" --expectSignal %s  --rMin -1 --rMax 5 -s %s \n'%(ntoy, injectsignal, rseed)
                #command += '\n combine -M FitDiagnostics -m '+str(mass)+' -d '+ card +' --toysFile higgsCombine.Test.GenerateOnly.mH'+str(mass)+'.'+str(rseed)+'.root  --cminDefaultMinimizerStrategy 0  --rMin -1 --rMax 5 -n '+rname+' -t '+str(ntoy)+' \n'


        if self.method == 'AsymptoticLimitsManual' :
            command = ''
            command+='rm higgsCombine*.AsymptoticLimits.*.root\n'
            for ip in self.manualpoints:
                command += 'combine -M AsymptoticLimits -m %d --singlePoint %g -n %g'\
                        ' %s  \n'  %( mass, ip, ip, card )
            command+='rm limits.root\n'
            command+='hadd limits.root higgsCombine*.AsymptoticLimits.*\n'
            command+= 'combine -M AsymptoticLimits -m %d --getLimitFromGrid limits.root'\
                    ' %s > %s'  %( mass, card, log_file )

        if self.method == 'MaxLikelihoodFit' :
            command = 'combine -M MaxLikelihoodFit -m %d --expectSignal=1'\
                    ' %s --plots -n %s >> %s \n' %( mass, card, self.var, log_file )
        return command



# ---------------------------------------------------


    @f_Dumpfname
    def get_commands( self ) :

        commands = []
        self.output_files = {}
        self.output_files = recdd()
        #for width in self.widthpoints:
        #    self.output_files.setdefault( width, {} )

        assert  'AsymptoticLimits' in self.method or self.method == 'MaxLikelihoodFit'
        for sigpar, card in list(self.allcards.items()) :
            
            wid = sigpar.split('_W')[1].split('_')[0]
            mass = int(sigpar.split('_')[0].lstrip("M"))
            ch = sigpar.split('_')[2]
            print((sigpar, "w %s m %i ch %s" %( wid, mass, ch)))
            log_file = 'results_%s_%s.txt'  %( self.var, sigpar )
            rundir = '%s/Width%s/%s/Mass%i/' %( self.outputDir, wid, ch, mass )
            command = "cd %s;" %rundir
            command += self.get_combine_command(sigpar,os.path.basename(card), log_file)
            print((tPurple%command))
            commands.append(command)

            #self.output_files[wid].setdefault( mass, {} )
            self.output_files[wid][ch][mass] = rundir+log_file
        return commands


# ---------------------------------------------------

    def run_commands(self):
        """ limit number of processes to cpu # """
        processes = []

        i = 0
        ## get list of commands
        commands = self.get_commands()
        cnum = multiprocessing.cpu_count()

        while len(commands)>0:
            while len(processes)<cnum-1:
                c = commands.pop()
                i+=1
                print(("command #",i, c))
                ## run commands
                processes.append((i,subprocess.Popen(c, shell=True)))

            for j,p in processes:
                if p.poll() is not None:
                    print((j, " status: ", p.poll()))
                    processes.remove((j,p))
                    break
            else:
                time.sleep(10)
        return


# ---------------------------------------------------


    @f_Dumpfname
    def write_combine_files( self ) :

        jobs = []
        output_files = recdd()
        ###
        ### output_file [ width/s ][ mass/i ][ ch/s ]
        ### content: printout destination of higgscombine
        ###

        #for width in self.widthpoints:
        #    output_files.setdefault( width, {} )

        if self.method == 'AsymptoticLimits' \
          or self.method == 'AsymptoticLimitsManual' \
          or self.method == 'MaxLikelihoodFit' :

            for sigpar, card in list(self.allcards.items()) :

                wid = sigpar.split('_W')[1].split('_')[0]
                mass = int(sigpar.split('_')[0].lstrip("M"))
                ch = sigpar.split('_')[2]
                ##only run all -- Yihui
                #if ch!='all':
                #if '2017' not in ch:
                #    continue
                #print sigpar, "w %s m %i ch %s" %( wid, mass, ch)

                fname = '%s/Width%s/%s/Mass%i/run_combine_%s.sh' %( self.outputDir, wid, ch, mass, sigpar )
                rundir = '%s/Width%s/%s/Mass%i/' %( self.outputDir, wid, ch, mass )
                log_file = '%s/Width%s/%s/Mass%i/results_%s_%s.txt' \
                                            %( self.outputDir, wid, ch, mass, self.var, sigpar )
                command= self.get_combine_command(sigpar, os.path.basename(card), os.path.basename(log_file)) + "\n"
                print((tPurple %command))

                ## write shell script (for condor jobs)
                ofile = open( fname, 'w' )
                ofile.write( '#!/bin/bash\n' )
                ofile.write( 'cd %s \n' %options.combineDir )
                ofile.write( 'eval `scramv1 runtime -sh` \n' )
                ofile.write( 'cd %s \n' %rundir )

                ofile.write(command)

                output_files[wid][ch][mass] = log_file

                ofile.write( 'cd - \n' )
                ofile.write( 'echo "^.^ FINISHED ^.^" \n' )

                ofile.close()

                os.system( 'chmod 744 %s'%fname )

                jobs.append(fname )

        if self.method == 'HybridNew' :

            for pt, vardic in list(all_cards.items()) :
                for var, bindic in list(vardic.items()) :

                    fname = '%s/run_combine_%s_%d.sh' %(output_dir, var, pt)
                    log_file = '%s/results_%s_%d.txt'%( output_dir, var, pt)

                    output_files.setdefault( pt, {} )
                    output_files[pt][var] = log_file

                    jobs.append(fname )

                    if not options.noRunCombine :
                        ofile = open( fname, 'w' )
                        ofile.write( '#!/bin/bash\n' )
                        ofile.write( 'cd %s \n' %combine_dir )
                        ofile.write( 'eval `scramv1 runtime -sh` \n' )

                        ofile.write( 'combine -M HybridNew --frequentist --testStat LHC -H ProfileLikelihood --fork 1 -m %d %s > %s \n ' %( pt, card, log_file ) )

                        ofile.write( ' cd - \n' )
                        ofile.write( 'echo "^.^ FINISHED ^.^" \n' )

                        os.system( 'chmod 777 %s/run_combine.sh' %(output_dir) )

                        ofile.close()


        return ( jobs, output_files )



# ---------------------------------------------------


    @f_Dumpfname
    def get_combine_results( self ) :

        combine_results = recdd()

        for width in self.widthpoints:

            for ch, massdict in list(self.output_files[width].items()) :
                for mass, f in list(massdict.items()) :

                    xsec = self.weightMap['ResonanceMass%d'%mass]['cross_section']
                    Wlepbr = (10.71 + 10.63 + 11.38)/100.
                    xsfactor = xsec * 1000 / Wlepbr  # unit in cross_sections is pb, so now we convert it to fb
                    #Scale factor for the limit plot -- Yihui

                    result = self.process_combine_file( f, xsfactor )
                    
                    if self.method == 'AsymptoticLimits' or self.method == 'AsymptoticLimitsManual':

                        if len(result)!=6 and len(result)!=5:
                           print(("missing some limits. Skip this point Mass %d Width %s"%(mass, width)))

                        else:
                           combine_results[width][ch][mass] = result

                    if self.method == 'HybridNew' :

                        if result :
                            combine_results[var][pt] = float( result['Limit'].split('<')[1].split('+')[0] )
                        else :
                            combine_results[var][pt] = 0

        if not os.path.isdir( self.outputDir+'/Results' ) :

               print(("creating directory %s/Results"%self.outputDir))

               os.makedirs( self.outputDir+'/Results' )

        for width in self.widthpoints:
            for ch in list(self.output_files[width].keys()) :

                print(("\033[1;31m limits on the cross section for signals with %s width "\
                      "for channel %s saved to %s/Results \033[0m"%( width, ch, self.outputDir )))

                with open('%s/Results/result_%s_%s.json'\
                            %(self.outputDir, width, ch), 'w') as fp:

                     json.dump(combine_results[width][ch], fp)

        return combine_results



# ---------------------------------------------------


    @f_Dumpfname
    def process_combine_file( self, fname, xsfactor) :

        ofile = open( fname, 'r' )

        results = {}

        # http://pdg.lbl.gov/2018/tables/rpp2018-sum-gauge-higgs-bosons.pdf

        cllabeldict= { "Expected 50.0%": "exp0",
                       "Expected  2.5%": "exp-2",
                       "Expected 16.0%": "exp-1",
                       "Expected 84.0%": "exp+1",
                       "Expected 97.5%": "exp+2",
                       "Observed Limit": "obs"    }

        if self.method == 'AsymptoticLimits' or self.method == 'AsymptoticLimitsManual':

            for line in ofile :
                rvalue=-1
                if line.count(':') == 1 and ("Expected" in line or "Observed" in line):
                    clname, rvstr = line.split(':')
                    rvalue = float(rvstr.rstrip('\n').split('<')[1])
                    results[cllabeldict[clname]] = rvalue * xsfactor
                     
        if results.get("exp-2") == None:
        #if results.get("obs") == None or results.get("exp-2") == None:
            print((tRed %"No observed or expected value"))
        if results.get("obs") == None and results.get("exp0") != None:
            results["obs"] = results["exp0"]

        if self.method == 'HybridNew' :
            get_data = False
            for line in ofile :
                if line.count('-- Hybrid New -- ') :
                    get_data = True
                if get_data and line.count(':') > 0 :
                    spline = line.split(':')
                    results[spline[0]] = spline[1].rstrip('\n')

        ofile.close()

        return results

main()
