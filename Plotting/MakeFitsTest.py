from functools import wraps
import sys
import ROOT
import uuid
import os
import time
import subprocess
ROOT.PyConfig.IgnoreCommandLineOptions = True
from argparse import ArgumentParser
from collections import OrderedDict
import json

from SampleInfo2 import SampleInfo

## need to read the xsection info
import analysis_utils

parser = ArgumentParser()

parser.add_argument( '--baseDir', help='path to workspace directory' )
parser.add_argument( '--outputDir', default=None, help='name of output diretory for cards')
#parser.add_argument( '--doStatTests', action='store_true', help='run statistical tests of WGamma background')
#parser.add_argument( '--doWJetsTests', action='store_true', help='run tests of Wjets background' )
#parser.add_argument( '--doFinalFit',  action='store_true', help='run fit to data and background' )
parser.add_argument( '--doVarOpt',     action='store_true', help='run variable optimization' )
#parser.add_argument( '--doJetOpt',      action='store_true', help='run jet veto optimization' )
parser.add_argument( '--useHistTemp', action='store_true', help='use histogram templates' )
parser.add_argument( '--useToySignal', action='store_true', help='use gaussian as signal' )
parser.add_argument( '--useToyBackground',  action='store_true', help='use exponential as background ' )
parser.add_argument( '--noRunCombine',     action='store_true', help='Dont run combine, use existing results' )
parser.add_argument( '--combineDir',      default=None,        help='path to combine directory' )
parser.add_argument( '--condor',  action='store_true', help='run condor jobs' )

options = parser.parse_args()

_WLEPBR = (1.-0.6741)
_XSFILE   = 'cross_sections/photon16_smallsig2.py'
_LUMI     = 36000

DEBUG = 1

ROOT.gSystem.Load('My_double_CB/RooDoubleCB_cc.so')

tColor_Off="\033[0m"                    # Text Reset
tPurple="\033[0;35m%s"+tColor_Off       # Purple

def f_Obsolete(f):
        @wraps(f)
        def f_wrapper(*args, **kws):
                print f.__name__,": This method is obsolete"
                return f(*args,**kws)
        return f_wrapper



# ---------------------------------------------------


def f_Dumpfname(func):
    """ decorator to show function name and caller name """
    @wraps(func)
    def echo_func(*func_args, **func_kwargs):
        print('func \033[1;31m {}()\033[0m called by \033[1;31m{}() \033[0m'.format(func.__name__,sys._getframe(1).f_code.co_name))
        return func(*func_args, **func_kwargs)
    return echo_func

def main() :

    #ws_keys = {
    #            'Wgamma'   : 'workspace_wgamma',
    #            'top'      : 'workspace_top',
    #            'signal'   : 'workspace_signal',
    #            'wjets'    : 'workspace_wjets',
    #            'data'     : 'workspace_data',
    #            ## toy model
    #            'toysignal': 'workspace_toy_signal',
    #            'toybkg'   : 'workspace_toy_background',
    #            ## toy data
    #            'toydata'  : 'workspace_toy_data',
    #          }
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
                 'WGamma'        : SampleInfo( name = 'WGamma',      useLumi = True,
                                                 useMET = False, usePDF = False, ),
                 'TTbar'         : SampleInfo( name = 'TTbar',       useLumi = False,
                                                 useMET = False, usePDF = False, ),
                 'TTG'           : SampleInfo( name = 'TTG',         useLumi = False,
                                                 useMET = False, usePDF = False, ),
                 'Wjets'         : SampleInfo( name = 'Wjets',       useLumi = False,
                                                 useMET = False, usePDF = False, ),
                 'Zgamma'        : SampleInfo( name = 'Zgamma',      useLumi = False,
                                                 useMET = False, usePDF = False, ),
                 'GammaGamma'    : SampleInfo( name = 'GammaGamma',  useLumi = False,
                                                 useMET = False, usePDF = False, ),
                 'Backgrounds'   : SampleInfo( name = 'Backgrounds', useLumi = False,
                                                 useMET = False, usePDF = False, ),
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
    def binid(ibin): return "".join(map(str,ibin.values()))

    if options.outputDir is None :
        options.outputDir = "/home/kakw/efake/WG_Analysis/Plotting/data/higgs/"
    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )

    if options.baseDir is None :
        options.baseDir = "/home/kakw/efake/WG_Analysis/Plotting/data/"

    if options.combineDir == None:
        options.combineDir == "/home/kakw/efake/WG_Analysis/Plotting/CMSSW_10_2_13/src/"

    #signal_masses   = [900]
    #signal_masses   = [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400,
    #                   1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3500, 4000]
    signal_masses    = [300, 350, 400, 450, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
    signal_widths    = ['5', '0p01']

    if options.doVarOpt:

#        var_opt = {}

#        kine_vars = {
#                      'name' : 'mt_res'   , 'color' : ROOT.kBlack , 'range' : [150, 3000]
#                     #{ 'name' : 'mt_incl_lepph_z', 'color' : ROOT.kBlue},
#                     #{ 'name' : 'm_incl_lepph_z' , 'color' : ROOT.kRed },
#                     #{ 'name' : 'mt_rotated' , 'color' : ROOT.kRed },
#                     #{ 'name' : 'mt_constrwmass' , 'color' : ROOT.kGreen },
#                     #{ 'name' : 'ph_pt'          , 'color' : ROOT.kMagenta },
#                   }

        var_opt = MakeLimits(  var=  "mt_res" ,
                               wskeys = ws_keys,
                               masspoints  = signal_masses,
                               widthpoints = signal_widths,
                               #backgrounds=['WGamma', 'TTG', 'TTbar', 'Wjets', 'Zgamma'],
                               backgrounds=['WGamma'],
                               #backgrounds=['Backgrounds'],
                               baseDir=options.baseDir,
                               bins=bins,
                               #outputDir='%s/%s/%s' %( options.outputDir, 'VarOpt', var['name'] ),
                               outputDir=options.outputDir,
                               useToySignal=options.useToySignal,
                               useToyBackground=options.useToyBackground,
                             )

        var_opt.setup()

        combine_jobs = var_opt.get_combine_files()

        if not options.noRunCombine :

            if options.condor:
                jdl_name = '%s/job_desc.jdl'  %( options.outputDir )
                make_jdl( combine_jobs, jdl_name )

                os.system( 'condor_submit %s' %jdl_name )

                #wait_for_jobs( 'run_combine')
                wait_for_jobs( 'kakw') ### FIXME extremely error prone
            else:
                var_opt.run_commands()

        raw_input("continue")

        #results = {}
        #for key, opt in var_opt.iteritems() :
        #    print key
        results = var_opt.get_combine_results()

        print results

    else: ## run test sequence
        var_opt = MakeLimits( useToySignal = True )
        var_opt.run_commands()


# ---------------------------------------------------


@f_Dumpfname
def make_jdl( exe_list, output_file ) :

    base_dir = os.path.dirname( output_file )

    file_entries = []
    file_entries.append('#Use only the vanilla universe')
    file_entries.append('universe = vanilla')
    file_entries.append('# This is the executable to run.  If a script,')
    file_entries.append('#   be sure to mark it "#!<path to interp>" on the first line.')
    file_entries.append('# Filename for stdout, otherwise it is lost')
    file_entries.append('# Copy the submittor environment variables.  Usually required.')
    file_entries.append('getenv = True')
    file_entries.append('# Copy output files when done.  REQUIRED to run in a protected directory')
    file_entries.append('Requirements = (TARGET.OpSysMajorVer == 7)')

    file_entries.append('when_to_transfer_output = ON_EXIT_OR_EVICT')
    #file_entries.append('transfer_output = True')
    file_entries.append('priority=0')

    for exe in exe_list :

        file_entries.append('output = %s'%exe.replace('.sh', '_out.txt'))
        file_entries.append('error = %s'%exe.replace('.sh', '_err.txt'))

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
       print "Can not turn the width into float"
    return fwidth



# ---------------------------------------------------


def wait_for_jobs( job_tag ) :

    #while 1 :
    #    status = subprocess.Popen( ['bjobs'], stdout=subprocess.PIPE).communicate()[0]

    #    n_limits = 0

    #    for line in status.split('\n') :
    #        if line.count(job_tag ) :
    #            n_limits += 1

    #    if n_limits == 0 :
    #        return
    #    else :
    #        print '%d Jobs still running' %n_limits
    #    time.sleep( 1.0 * 60 )

    while 1 :
        time.sleep(20)
        status = subprocess.Popen( ['condor_q'], stdout=subprocess.PIPE).communicate()[0]

        n_limits = 0

        for line in status.split('\n') :
            if line.count(job_tag ) :
                n_limits += 1

        if n_limits == 1 :
            return
        else :
            print '%d Jobs still running' %(n_limits-1)




# ---------------------------------------------------


class MakeLimits( ) :

    def __init__(self, **kwargs) :

        self.fail=False

        self.var              = kwargs.get('var'        ,  None )
        self.masspoints       = kwargs.get('masspoints' ,  None )
        self.widthpoints      = kwargs.get('widthpoints',  None )
        self.baseDir          = kwargs.get('baseDir'    ,  None )
        self.outputDir        = kwargs.get('outputDir'  ,  None )
        self.bins             = kwargs.get('bins'       ,  None )
        self.bkgnames         = kwargs.get('backgrounds',  None )

        self.wskeys = kwargs.get('wskeys', None)

        self.useToySignal     = kwargs.get('useToySignal',     False )
        self.useToyBackground = kwargs.get('useToyBackground', False )


        self.wstag = kwargs.get('wsTag', 'base' )
        self.method = kwargs.get('method', 'AsymptoticLimits' )

        self.xvarname = kwargs.get('xvarname', 'mt_res')

        self.signals = OrderedDict()
        self.backgrounds = OrderedDict()
        self.datas = OrderedDict()

        self.params = OrderedDict()

        ## format checks
        if self.masspoints == None or not isinstance( self.masspoints, list ) :
            print 'Must provide a list of mass points'
            self.fail = True;

        if self.widthpoints == None or not isinstance( self.widthpoints, list):
            print 'Must provide a list of width points'
            self.fail = True;

        if self.var == None or not isinstance( self.var, str ) :
            print 'Must provide a plot var as a string'
            self.fail = True

        if self.bins == None or not isinstance( self.bins, list ) :
            print 'Must provide a list of bins '
            self.fail = True

        if self.wskeys == None or not isinstance( self.wskeys, dict) :
            print "Must provide a dictionary of workspace names"
            self.fail = True

        if self.baseDir == None or not isinstance( self.baseDir, str ) :
            print 'Must provide a base directory'
            self.fail = True

        #--------------------

        if self.useToyBackground :
            print "use exponential toy background. Will ignore the input backgrounds..."
            self.bkgnames = ['toybkg']

        if self.useToySignal :
            print "use gaussian toy signal. Will ignore the input signals..."
            self.signame = 'toysignal'
        else:
            self.signame = 'signal'

        if not self.useToySignal:
           print "have to load cross sections for signals for normalization. :( "
           self.weightMap,_ = analysis_utils.read_xsfile( _XSFILE, _LUMI, print_values=True )



# ---------------------------------------------------






# ---------------------------------------------------


    @f_Dumpfname
    def setup( self ):

        if self.fail :
            print 'Initialzation failed, will not setup'
            return

        # -------------------------------------------------
        # Prepare workspaces
        # -------------------------------------------------

        # -------------------------------------------------
        # background
        # -------------------------------------------------

        for bkgn in self.bkgnames:
            if not os.path.isdir( self.outputDir+'/'+bkgn ) :
               print "creating directory %s/%s"%(self.outputDir, bkgn )
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
           print " creating directory %s/%s"%(self.outputDir, self.signame)
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
        # Prepare the data cards for limits
        #---------------------------------------

        self.allcards = {}

        self.generate_all_cards( )




# ---------------------------------------------------


    @f_Dumpfname
    def get_combine_files( self ) :

        if self.fail :
            print 'Initialzation failed, will not setup'
            return []

        print "all cards: ",  self.allcards
        print "method: ",     self.method
        print "outputDir: ",  self.outputDir

        jobs, output_files = self.write_combine_files()

        self.output_files = output_files

        return jobs




# ---------------------------------------------------


    @f_Dumpfname
    def generate_all_cards( self ):

        for width in self.widthpoints:
            outputdir = self.outputDir + '/' + 'Width' + width
            if not os.path.isdir( outputdir ) :
               print " creating directory", outputdir
               os.makedirs( outputdir )

            for mass in self.masspoints:

                sigpar = "_".join( ['M'+ str(mass), 'W'+width] )

                card_path = '%s/wgamma_test_%s_%s.txt' %(outputdir, self.var, sigpar )

                self.generate_card( card_path, sigpar )

                self.allcards[sigpar] =  card_path




# ---------------------------------------------------


    @f_Dumpfname
    def generate_card( self, outputCard, sigpar,  tag='base' ) :
        """

            generates card
            input:
                outputCard      output card?
                sigpar          list of signal parameters
                tag             tag (still used?)
            output:
                none

        """

        card_entries = []
        viablebins , viablesig= [], []

        section_divider = '-'*100

        ## check if signal channel exists
        for ibin in self.bins :
            sig = self.signals.get(sigpar+"_"+ibin['channel']+str(ibin['year']))
            if not sig: ## model not exist: exclude them for now
                print "WARNING MODEL NOT EXIST: ", sigpar, ibin
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
        max_path_len = max( [len(x.GetOutputName(self.outputDir, **ibin)) for x in self.backgrounds.values() for ibin in self.bins] )

        all_binids = []
        #signal_norm = 1.0

        ############################################
        ##  shape decaration 
        ##  num of lines: (SIG+BKG+DATA=1)XCH
        ##
        ##  shapes Resonance mu_2016 /sigfit/2016/wssignal_M350_W5_mu.root wssignal_M350_W5_mu:cb_MG_M350_W5_mu2016
        ##  shapes Resonance el_2016 /sigfit/2016/wssignal_M350_W5_el.root wssignal_M350_W5_el:cb_MG_M350_W5_el2016
        ##  shapes Resonance mu_2018 /sigfit/2018/wssignal_M350_W5_mu.root wssignal_M350_W5_mu:cb_MG_M350_W5_mu2018
        ##  shapes Resonance el_2018 /sigfit/2018/wssignal_M350_W5_el.root wssignal_M350_W5_el:cb_MG_M350_W5_el2018
        ##  shapes WGamma el_2018    /higgs/WGamma/mu2016workspace_wgamma_dijet.root workspace_wgamma_dijet:dijet_mu2016_wgamma
        ##  shapes data_obs el_2018  /higgs/toydata/wtoydata.root workspace_toydata:toydata_mu_2016_mt_res_base
        ##  shapes data_obs el_2018  /higgs/toydata/wtoydata.root workspace_toydata:toydata_mu_2016_mt_res_base
        ############################################



        for ibin, sig in viablesig:
            bin_id = binid(ibin) 
            all_binids.append(bin_id)
            card_entries.append( 'shapes Resonance %s %s %s:%s' %( bin_id, sig['file'], sig['workspace'], sig['pdf'] ) )

        for ibin in viablebins:
            bin_id = binid(ibin)
            for bkgname, bkg in self.backgrounds.iteritems() :
                ### BKG X CH
                if options.useHistTemp :
                    bkg_entry = bkg_entry.replace('dijet', 'datahist' )
                card_entries.append( 'shapes %s %s %s %s:%s' %( bkgname.ljust( max_name_len ),
                    bin_id, bkg.GetOutputName(options.outputDir,**ibin).ljust( max_path_len ), bkg.GetWSName(),
                    bkg.GetPDFName( self.var , ibin['channel'], ibin['year']) ) )

        for ibin in viablebins:
            bin_id = binid(ibin)
            ###  DATA (=1) X CH
            data = self.datas[self.dataname+binid(ibin)]
            card_entries.append( 'shapes data_obs %s %s %s:%s' %( bin_id, data['file'], data['workspace'], data['data'] ) )

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
            for bkgname, bkg in self.backgrounds.iteritems():
                #rate_entries.append( str(bkgdic['norm'][bin_id]) )
                rate_entries.append( bkg.norm[0] )
                #bkg rate
                #rate_entries.append( str(1.0) )

        bin_entries = []
        for b in all_binids :
            bin_entries += [b]*(len(self.backgrounds)+1)

        card_entries.append( 'bin         ' + listformat(bin_entries )  )
        card_entries.append( 'process     ' + listformat((['Resonance'] + [x for x in self.bkgnames])*len(viablebins) ) )
        card_entries.append( 'process     ' + listformat( range(len(self.backgrounds) +1)*len(viablebins), form = "%-14d" ) )
        #card_entries.append( 'rate     ' + '    '.join( [str(signal_norm), str(backgrounds[0]['norm']) ]*len(bins) ) )
        card_entries.append( 'rate        ' + listformat( rate_entries,"%-13g " )  )

        card_entries.append( section_divider )
        ############################################
        ##  systematics declaration
        ##
        ##  lumi       lnN    1.025    1.0250
        ##  met        lnN    1.03    -    1.03    -    1.03    -    1.03    -
        ##  pdf        lnN    1.05    -    1.05    -    1.05    -    1.05    -
        ##  dijet_order1_el2018_wgamma flatParam
        ##  dijet_order2_el2018_wgamma flatParam
        ##  cb_cut1_MG_M350_W5_mu2016 param 0.60000 0.00005
        ##  cb_mass_MG_M350_W5_mu2016 param 329.58155 0.06551
        ############################################

        lumi_vals = ["%-13g "%1.025] * (len(all_binids)*( len(self.backgrounds) + 1 ))
        #lumi_vals = ['1.025'] + [ '1.025' if bkg.useLumi else '-' for bkg in self.backgrounds.values() ]
        bkg_vals = (['       -     '] + ["%-13g " %1.20]*len(self.backgrounds) )*len(all_binids)
        signal_met = ( ["%-13g " %1.03] + ['       -     ']*len(self.backgrounds) )*len( all_binids)
        signal_pdf = ( ["%-13g " %1.05] + ['       -     ']*len(self.backgrounds) )*len( all_binids)

        card_entries.append( 'lumi  lnN   ' + ''.join(lumi_vals) )
        #card_entries.append( 'bkgelse   lnN    ' + '    '.join(bkg_vals    ) )
        card_entries.append( 'met   lnN   ' + ''.join(signal_met) )
        card_entries.append( 'pdf   lnN   ' + ''.join(signal_pdf) )

        # assign 30% normalization uncertainty in all backgrounds from data-driven
        for bkgname in self.backgrounds:
            if not self.backgrounds[bkgname].useLumi:
               bkg_norms = ['-'] + ['1.30' if namebkg == bkgname else '-' for namebkg in self.backgrounds]
               card_entries.append('%s_norm lnN    '%bkgname + '    '.join( bkg_norms ))

        #parameter errors
        for iparname, iparval in self.params.iteritems():
            ## FIXME stopgap measure 
            if any([ibin['channel']+str(ibin['year']) in iparname for ibin in viablebins]):
                #card_entries.append('%s param %.2f %.2f'%(iparname, iparval[0], iparval[1]))
                card_entries.append('%s flatParam'%iparname)

        for ibin, sig in viablesig:
            #sig = self.signals.get(sigpar+"_"+ibin['channel']+str(ibin['year']))
            #if not sig: ## model not exist
            #    continue
            for iparname, iparval in sig['params'].iteritems():
                if iparval[1] != 0:
                   card_entries.append('%s param %.5f %.5f'%(iparname, iparval[0], iparval[1]))

        card_entries.append( section_divider )

        #for ibin in bins :
        #    card_entries.append( 'logcoef_dijet_Wgamma_%s flatParam' %( ibin ) )
        #    card_entries.append( 'power_dijet_Wgamma_%s flatParam' %( ibin ) )

        if outputCard is not None :
            print 'Write file ', outputCard
            ofile = open( outputCard, 'w' )
            for line in card_entries :
                ofile.write( line + '\n' )
            ofile.close()
        else :
            for ent in card_entries :
                print ent




# ---------------------------------------------------


    @f_Dumpfname
    def generate_toy_data( self,  sigpars=None, signorms = None, data_norm=None ) :

        if not os.path.isdir( self.outputDir+'/'+self.dataname ) :
           print " creating directory %s/%s"%(self.outputDir, self.dataname)
           os.makedirs( self.outputDir+'/'+self.dataname )


        ##loop over bins
        for ibin in self.bins :
            ## background
            for bkgname, bkg in self.backgrounds.iteritems():
                self.generate_toy_data_helper( ibin, bkgname, bkg,
                                        sigpars, signorms, data_norm)



# ---------------------------------------------------


    def generate_toy_data_helper( self, ibin, bkgname, bkg,
                                  sigpars=None, signorms = None, data_norm=None ) :

       workspace = ROOT.RooWorkspace( '_'.join(['workspace', self.dataname, binid(ibin)]) )


       suffix = "%s_%s_%s"%(binid(ibin), self.var, self.wstag)

       pdfs = []
       norms = []
       xvar = None
       #if bkgname != 'WGamma':
       #   print "[ \033[1;31mProblem running the toy data generation process. Skip %s. Only play with WGamma for now\033[0m  ]"%bkgname
       #   continue

       #full_path = bkg['file']
       #ofile = ROOT.TFile.Open( full_path )
       # FIXME print "bkg.outputfname", bkg.outputfname
       ofile = ROOT.TFile.Open( bkg.GetOutputName( self.outputDir ,**ibin) )

       #ws = ofile.Get( bkg['workspace'] )
       ws = ofile.Get( bkg.GetWSName() )

       if options.useHistTemp :
           print hist_key
           pdfs.append(ws.data( hist_key ))
           norms.append(pdfs[-1].sumEntries())
       else :
           #norms.append( ws.var( '%s_norm'%bkg['pdf'] ).getVal() )
           #pdfs.append(  ws.pdf( bkg['pdf'] ) )
           #norms.append( ws.var('%s_norm'%bkg.GetPDFName(self.var, self.bins[0]['channel'])).getVal() )
           norms.append( bkg.norm[0] )
           pdfs.append( ws.pdf( bkg.GetPDFName(self.var, **ibin)) )

       if xvar is None :
           xvar = ws.var( self.xvarname )

       ofile.Close()

       ## mix into some fake signal
       if sigpars:
          print "add some fake signals for fun..."
          for sigpar, signorm in zip(sigpars, signorms):
              try:
                  sig = self.signals[sigpar+str(ibin['year'])]
                  print "sig: ", sig
                  ofile = ROOT.TFile.Open( sig['file'] )
              except:
                  print self.signals.keys()
                  print "can not open the signal workspace file: "\
                        "%s Please x-check self.signals collection"\
                            %self.signals[sigpar]['file']
                  raise
              print sigpar, sig['file'], sig['pdf']
              ws = ofile.Get( sig['workspace'] )
              pdfs.append( ws.pdf( sig['pdf'] ) )
              #norms.append( ws.var( '%s_norm'%sig['pdf']).getVal() * signorm )
              norms.append( sig['rate']*signorm)

       print "Normalization:: ", norms

       if len( pdfs ) == 1 :
           ### there is only 1 pdf. save toy data
           if options.useHistTemp :
               dataset = ROOT.RooDataHist( pdfs[0], 'toydata_%s' %suffix )
           else :
               if data_norm is None :
                   norm = int(norms[0])
               else :
                   norm = data_norm
               dataset = pdfs[0].generate(ROOT.RooArgSet(xvar) , int(norm),
                         ROOT.RooCmdArg( 'Name', 0, 0, 0, 0, 'toydata_%s' %suffix ) )
       else :
           if DEBUG: print "norms: ", norms
           total = sum( [int(x) for x in norms ] )

           fractions = [ float(x)/total for x in norms ]

           print "total ", total, " fractions", fractions

           if options.useHistTemp :

               dataset = ROOT.RooDataHist( pdfs[0], 'toydata_%s' %suffix )

               for pdf in pdfs[1:] :
                   dataset.add( pdf )

           else :
               print "**** start generate toy data *****"
               pdfList = ROOT.RooArgList()
               print pdfs
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
               print fracList
               summed = ROOT.RooAddPdf( 'summed' ,'summed', pdfList , fracList )
               dataset = summed.generate( ROOT.RooArgSet(xvar), int(total),
                            ROOT.RooCmdArg( 'Name', 0, 0, 0, 0, 'toydata_%s' %suffix ) )

       # not clear why we have to rename here
       #getattr( out_ws, 'import' ) ( dataset, ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'toydata_%s' %suffix ) )
       getattr( workspace, 'import' ) ( dataset )

       outputfile = '%s/%s/%s.root' %( self.outputDir, self.dataname, workspace.GetName() )
       print outputfile, "718"

       workspace.writeToFile( outputfile )

       self.datas.update(
                          { self.dataname+binid(ibin): { 'channel':
                              binid(ibin), 'file': outputfile, 'workspace':
                              workspace.GetName(), 'data': dataset.GetName() }
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
        print " prepare background functions for ", bkgn

        #ofile = ROOT.TFile.Open( '%s/MCBkgWS/workspace_%s.root' %( self.baseDir, bkgn.lower() ), 'READ' )
        print  '%s/bkgfit/%i/%s' %( self.baseDir, ibin['year'],self.wskeys[bkgn].GetRootFileName() )
        ofile = ROOT.TFile.Open( '%s/bkgfit/%i/%s' %( self.baseDir, ibin['year'], 
                        self.wskeys[bkgn].GetRootFileName() ), 'READ' )

        #ws_in = ofile.Get( "workspace_" + bkgn.lower() )
        ws_in = ofile.Get( self.wskeys[bkgn].GetWSName() )

        ws_out = ROOT.RooWorkspace( self.wskeys[bkgn].GetWSName() )

        #suffix = "_".join([bkgn, self.bins[0]['channel'], self.var, self.wstag, self.bins[0]['eta']])

        #ws_entry = "_".join( [self.wskeys[bkgn].pdf_prefix, suffix])

        ws_entry = self.wskeys[bkgn].GetPDFName( self.var, **ibin)

        if DEBUG:
           print ws_entry

        if options.useHistTemp :
            datahist = ws_in.data(ws_entry.replace('dijet', 'datahist') )
            getattr( ws_out, 'import' ) ( datahist )
        else :
            pdf = ws_in.pdf( ws_entry )
            #power_var = ws_in.var( 'power_%s' %ws_entry )
            #logcoef_var = ws_in.var( 'logcoef_%s' %ws_entry )

            #power_var.setConstant()
            #logcoef_var.setConstant()
            # pars

            #for ipar in self.wskeys[bkgn].params_prefix:
            for ipar in self.wskeys[bkgn].GetParNames( **ibin):
                if DEBUG:
                   print ipar
                oldvar = ws_in.var( ipar )
                if 'order1' in ipar:
                    varrange = (-50.0, 0.0)
                elif 'order2' in ipar:
                    varrange = (-10.0, 0.0)
                elif 'order3' in ipar:
                    print "order 3............................"
                    varrange = (-5.0, 0.0)

                var =  ROOT.RooRealVar( ipar, ipar,  oldvar.getVal(), varrange[0], varrange[1] )
                print var
                # save the value and errors of the fit parameters, to be used for card generation
                self.params.update( {ipar: (oldvar.getVal(), oldvar.getError())} )
                #var.setError(0.0)
                #var.setConstant()
                #if 'order1' in ipar: var.setRange(-50.0, 0.0 )
                #else: var.setRange(-10.0, 0.0 )

                getattr( ws_out, 'import' ) ( var )

            var = ws_in.var("mt_res") ##FIXME
            var.setBins(660)
            getattr( ws_out, 'import' ) ( var )

            print "%s_norm" %ws_entry
            norm_var = ws_in.var( '%s_norm' %ws_entry )
            self.wskeys[bkgn].SetNorm( norm_var.getVal(), norm_var.getError() )
            #norm_var.setError( 0.3*norm_var.getValV() )
            #norm_var.setVal( norm_var.getValV() )
            #norm_var.setError( 0.0 )
            #norm_var.setConstant()
            #getattr( ws_out, 'import' ) ( norm_var )
            getattr( ws_out, 'import' ) ( pdf )

        ofile.Close()

        #outputfile = '%s/%s/%s.root' %( self.outputDir, bkgn, ws_out.GetName() )
        #ws_out.writeToFile( outputfile )
        outputname = self.wskeys[bkgn].GetOutputName( self.outputDir , **ibin)
        ws_out.writeToFile( outputname )

        ## infor for generating toy data and datacard
        #self.backgrounds.update(
        #                       { bkgn: { 'channel': "%s_%s"%(self.bins[0]['channel'], self.bins[0]['eta']), 'file': outputfile, 'workspace': ws_out.GetName(), 'pdf': pdf.GetName(), 'params': params} }
        #                       )
        self.backgrounds.update( { bkgn: self.wskeys[bkgn]} )
        print "BACKGROUND: ",self.backgrounds



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
        scale = self.weightMap['ResonanceMass%d'%mass]['scale']

        fname= '%s/sigfit/%i/ws%s_%s.root' %( self.baseDir, ibin['year'], self.signame, inpar )
        wsname = "ws" + self.signame + '_' + inpar
        if DEBUG:
            print fname, " : ", wsname
        ifile = ROOT.TFile.Open( fname, 'READ' )
        if not ifile:
            print "skipping ", fname
            return


        ws_in = ifile.Get( wsname )

        ws_out = ROOT.RooWorkspace( "workspace_" + self.signame + '_' + sigpar )

        sigfitparams = OrderedDict()

        suffix = sigpar#+str(ibin["year"] )#"_".join([sigpar, "2016"]) ##FIXME
        ws_entry = "_".join([self.wskeys[self.signame].pdf_prefix, suffix])

        if DEBUG:
           print ws_entry

        pdf = ws_in.pdf( ws_entry )

        for ipar in self.wskeys[self.signame].params_prefix:
            if DEBUG:
               print ipar+ '_' + suffix
            var = ws_in.var( ipar  + '_' + suffix )
            sigfitparams.update( {ipar + '_' + suffix: (var.getVal(), var.getError())} )
            #var.setError(0.0)
            #var.setConstant()
            getattr( ws_out, 'import' ) ( var )

        var = ws_in.var('mt_res')##FIXME
        var.setBins(660)
        getattr( ws_out, 'import' ) ( var )

        norm_var = ws_in.var( '%s_norm' %ws_entry )
        rate = norm_var.getVal() * scale ## FIXME double counting?
        print tPurple%("norm %g scale %g rate %g" \
                                   %(norm_var.getVal(),scale,rate))
        norm_var.setVal( norm_var.getValV() * scale )
        norm_var.setError( norm_var.getError() * scale )
        #norm_var.setError(0.0)
        #norm_var.setConstant( False )
        norm_var.setConstant()
        #getattr( ws_out, 'import' ) ( norm_var )
        getattr( ws_out, 'import' ) ( pdf )

        ifile.Close()

        outputfile = '%s/%s/%s.root' %( self.outputDir, self.signame, ws_out.GetName() )
        print outputfile, "885"
        ws_out.writeToFile( outputfile )

#        ## info for generating toy data and datacard
#        self.signals.update(
#                    {sigpar) : {'channel': binid(ibin),
#                               'file': fname,
#                               'workspace': wsname,
#                               'pdf': ws_entry, #pdf.GetName(),
#                               'rate': rate,
#                               'params': sigfitparams} }
#                           )

        ## info for generating toy data and datacard
        self.signals.update( {sigpar : {'channel': binid(ibin),
                                'file': outputfile,
                                'workspace': ws_out.GetName(),
                                'pdf': pdf.GetName(),
                                'rate': rate,
                                'params': sigfitparams} }
                            )




# ---------------------------------------------------


    @f_Dumpfname
    @f_Obsolete
    def get_signal_data( self, signal_file, ws_key, signal_points, plot_var, bins ) :
        '''
         currently this function is not used
        '''

        signal_data = {}

        ofile = ROOT.TFile.Open( signal_file, 'READ'  )

        signal_ws = ofile.Get( ws_key )

        if plot_var.count('pt') :
            xvar = signal_ws.var( 'x_pt' )
        else :
            xvar = signal_ws.var( 'x_m' )

        for gen in ['MadGraph', 'Pythia'] :
            for width in ['width5', 'width0p01'] :
                for sig_pt in signal_points :

                    signal_base = 'srhist_%sResonanceMass%d_%s' %(gen, sig_pt, width )
                    signal_data.setdefault( signal_base, {} )
                    signal_data[signal_base].setdefault( plot_var, {} )
                    for ibin in bins :
                        binid= binid(ibin)

                        signal_entry = get_workspace_entry( signal_base, ibin['channel'], ibin['eta'], plot_var)

                        dist = signal_ws.data( signal_entry )

                        if not dist :
                            continue

                        reco_events   = signal_ws.var( '%s_norm' %signal_entry ).getValV()
                        scale         = signal_ws.var(signal_entry.replace('srhist', 'scale' )).getValV()
                        total_events  = signal_ws.var(signal_entry.replace('srhist', 'total_events')).getValV()
                        cross_section = signal_ws.var(signal_entry.replace('srhist', 'cross_section')).getValV()

                        efficiency = reco_events / ( scale * total_events )
                        signal_data[signal_base][plot_var].setdefault(binid,  {} )
                        signal_data[signal_base][plot_var][binid]['norm'] = dist.sumEntries()
                        signal_data[signal_base][plot_var][binid]['efficiency'] = efficiency
                        signal_data[signal_base][plot_var][binid]['cross_section'] = cross_section

        ofile.Close()
        return signal_data



# ---------------------------------------------------


    @f_Dumpfname
    def make_gauss_signal(self,  normvalue) :

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
                   print suffix

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
                getattr( workspace, 'import' ) ( signal )
                getattr( workspace, 'import' ) ( norm )

                outputfile = '%s/%s/%s.root' %( self.outputDir, self.signame,
                        workspace.GetName() )
                print outputfile, "982"
                workspace.writeToFile( outputfile )

                self.signals.update(
                                     {sigpar : {'channel':
                                         "%s_%s"%(self.bins[0]['channel'],
                                             self.bins[0]['eta']), 'file':
                                         outputfile, 'workspace':
                                         workspace.GetName(), 'pdf':
                                         signal.GetName() } }
                                   )




# ---------------------------------------------------


    @f_Dumpfname
    def make_exp_background(self, expvalue, normvalue ) :

        workspace= ROOT.RooWorkspace( "workspace_%s"%self.bkgnames[0] )


        suffix = "%s_%s_%s_%s"%(self.bins[0]['channel'], self.var, self.wstag,
                self.bins[0]['eta'])

        if DEBUG:
           print suffix

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
        getattr( workspace, 'import' ) ( background )
        getattr( workspace, 'import' ) ( norm )

        outputfile = "%s/%s/%s.root"%( self.outputDir, self.bkgnames[0],
                workspace.GetName() )
        print outputfile, "1019"
        workspace.writeToFile( outputfile )

        ## infor for generating toy data and datacard
        self.backgrounds.update(
                                   {self.bkgnames[0]: { 'channel':
                                       "%s_%s"%(self.bins[0]['channel'],
                                           self.bins[0]['eta']), 'file':
                                       outputfile, 'workspace':
                                       workspace.GetName(), 'pdf':
                                       background.GetName() } }
                               )


# ---------------------------------------------------


    def get_combine_command( self, sigpar, card, log_file):

        ### essential info
        wid = sigpar.split('_W')[1].split('_')[0] ## FIXME repeated
        mass = int(sigpar.split('_')[0].lstrip("M"))

        ## generate commands
        if self.method == 'AsymptoticLimits' :
            command = 'combine -M AsymptoticLimits -m %d --rMin 0.01'\
                    ' --rMax 10 %s >& %s'  %( mass, card, log_file )
        if self.method == 'MaxLikelihoodFit' :
            command = 'combine -M MaxLikelihoodFit -m %d --expectSignal=1'\
                    ' %s --plots -n %s >> %s \n' %( mass, card, self.var, log_file )
        return command



# ---------------------------------------------------


    @f_Dumpfname
    def get_commands( self ) :

        commands = []
        self.output_files = {}
        for width in self.widthpoints:
            self.output_files.setdefault( width, {} )

        assert self.method == 'AsymptoticLimits' or self.method == 'MaxLikelihoodFit'

        for sigpar, card in self.allcards.iteritems() :

            print sigpar
            wid = sigpar.split('_W')[1].split('_')[0]
            mass = int(sigpar.split('_')[0].lstrip("M"))

            log_file = '%s/Width%s/results_%s_%s.txt' \
                                 %( self.outputDir, wid, self.var, sigpar )
            command= self.get_combine_command(sigpar, card, log_file)
            print tPurple%command
            commands.append(command)

            self.output_files[wid].setdefault( mass, {} )
            self.output_files[wid][mass] = log_file
        return commands


# ---------------------------------------------------


    def run_commands(self):
        processes = []
        doneset = set()

        ## get list of commands
        commands = self.get_commands()
        ## FIXME for testing
        #commands = [ ['sleep','%i'%i] for i in range(0,30,5)]

        ## run command
        for i,c in enumerate(commands):
            print "command #",i, c
            processes.append(subprocess.Popen(c, shell=True))

        ## check command state
        while any([p.poll() == None for p in processes]):
            time.sleep(10)
            for i, p in enumerate(processes):
                status = p.poll()
                if status == None:
                    continue
                elif status == 0:
                    if i not in doneset:
                        doneset.add(i)
                        print "FINISHED", i
                else:
                    if i not in doneset:
                        doneset.add(i)
                    print "ERROR", i
        return


# ---------------------------------------------------


    @f_Dumpfname
    def write_combine_files( self ) :

        jobs = []
        output_files = {}
        for width in self.widthpoints:
            output_files.setdefault( width, {} )

        # FIXME this should be improved
        if self.method == 'AsymptoticLimits' or self.method == 'MaxLikelihoodFit' :

            for sigpar, card in self.allcards.iteritems() :

                print sigpar
                wid = sigpar.split('_W')[1].split('_')[0]
                mass = int(sigpar.split('_')[0].lstrip("M"))

                fname = '%s/Width%s/run_combine_%s.sh' %( self.outputDir, wid, sigpar )
                log_file = '%s/Width%s/results_%s_%s.txt' \
                                             %( self.outputDir, wid, self.var, sigpar )
                command= self.get_combine_command(sigpar, card, log_file) + "\n"

                ## write shell script (for condor jobs)
                ofile = open( fname, 'w' )
                ofile.write( '#!/bin/bash\n' )
                ofile.write( 'cd %s \n' %options.combineDir )
                ofile.write( 'eval `scramv1 runtime -sh` \n' )

                ofile.write(command)

        #        if self.method == 'AsymptoticLimits' :
        #            ofile.write( 'combine -M AsymptoticLimits -m %d --rMin 0.01 --rMax 10 %s >& %s \n'  %( mass, card, log_file ))
        #        if self.method == 'MaxLikelihoodFit' :
        #            ofile.write( 'combine -M MaxLikelihoodFit -m %d --expectSignal=1 %s --plots -n %s >> %s \n' %( mass, card, var, log_file ) )

                output_files[wid][mass] = log_file

                ofile.write( ' cd - \n' )
                ofile.write( 'echo "^.^ FINISHED ^.^" \n' )

                ofile.close()

                os.system( 'chmod 744 %s'%fname )

                jobs.append(fname )

        if self.method == 'HybridNew' :

            for pt, vardic in all_cards.iteritems() :
                for var, bindic in vardic.iteritems() :

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

        combine_results = {}

        for width in self.widthpoints:
            combine_results.setdefault( width, {})

            for mass, f in self.output_files[width].iteritems() :
                result = self.process_combine_file( f, mass )
                if self.method == 'AsymptoticLimits' :
                    #combine_results[var][mass] = float( result[key].split('<')[1] )
                    if len(result)!=6:
                       print "missing some limits. Skip this point Mass %d Width %s"%(mass, width)
                    else:
                       combine_results[width][mass] = result

                if self.method == 'HybridNew' :
                    if result :
                        combine_results[var][pt] = float( result['Limit'].split('<')[1].split('+')[0] )
                    else :
                        combine_results[var][pt] = 0

        if not os.path.isdir( self.outputDir+'/Results' ) :
               print "creating directory %s/Results"%self.outputDir
               os.makedirs( self.outputDir+'/Results' )

        for width in self.widthpoints:
            print "\033[1;31m limits on the cross section for signals with %s width saved to %s/Results \033[0m"%( width, self.outputDir )
            with open('%s/Results/result_%s_%s.json'%(self.outputDir, width, self.bins[0]['channel']), 'w') as fp:
                 json.dump(combine_results[width], fp)

        return combine_results



# ---------------------------------------------------


    @f_Dumpfname
    def process_combine_file( self, fname, mass) :

        ofile = open( fname, 'r' )

        xsec = self.weightMap['ResonanceMass%d'%mass]['cross_section']

        results = {}

        # http://pdg.lbl.gov/2018/tables/rpp2018-sum-gauge-higgs-bosons.pdf

        Wlepbr = 10.71 + 10.63 + 11.38

        if self.method == 'AsymptoticLimits' :
            for line in ofile :
                if line.count(':') > 0 :
                    spline = line.split(':')
                    #results[spline[0]] = spline[1].rstrip('\n')
                    if "Expected 50.0%" in spline[0]:
                       results["exp0"] = float(spline[1].rstrip('\n').split('<')[1]) * xsec * 1000.0  * 100.0/Wlepbr
                    elif "Expected  2.5%" in spline[0]:
                       results["exp-2"] = float(spline[1].rstrip('\n').split('<')[1]) * xsec * 1000.0 * 100.0/Wlepbr
                    elif "Expected 16.0%" in spline[0]:
                       results["exp-1"] = float(spline[1].rstrip('\n').split('<')[1]) * xsec * 1000.0 * 100.0/Wlepbr
                    elif "Expected 84.0%" in spline[0]:
                       results["exp+1"] = float(spline[1].rstrip('\n').split('<')[1]) * xsec * 1000.0 * 100.0/Wlepbr
                    elif "Expected 97.5%" in spline[0]:
                       results["exp+2"] = float(spline[1].rstrip('\n').split('<')[1]) * xsec * 1000.0 * 100.0/Wlepbr
                    elif "Observed" in spline[0]:
                       results["obs"] = float(spline[1].rstrip('\n').split('<')[1]) * xsec * 1000.0   * 100.0/Wlepbr


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
