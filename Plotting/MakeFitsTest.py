import ROOT
import uuid
import os
import time
import subprocess
ROOT.PyConfig.IgnoreCommandLineOptions = True
from argparse import ArgumentParser
from collections import OrderedDict
import json

from SampleInfo import SampleInfo

## need to read the xsection info
import analysis_utils

parser = ArgumentParser()

parser.add_argument( '--baseDir',  dest='baseDir', required=True, help='path to workspace directory' )
parser.add_argument( '--outputDir',  dest='outputDir', required=False, default=None, help='name of output diretory for cards' )
parser.add_argument( '--doStatTests',  dest='doStatTests', default=False, action='store_true', help='run statistical tests of WGamma background' )
parser.add_argument( '--doWJetsTests',  dest='doWJetsTests', default=False, action='store_true', help='run tests of Wjets background' )
parser.add_argument( '--doFinalFit',  dest='doFinalFit', default=False, action='store_true', help='run fit to data and background' )
parser.add_argument( '--doVarOptimization',  dest='doVarOptimization', default=False, action='store_true', help='run variable optimization' )
parser.add_argument( '--doJetOptimization',  dest='doJetOptimization', default=False, action='store_true', help='run jet veto optimization' )
parser.add_argument( '--useHistTemplates',  dest='useHistTemplates', default=False, action='store_true', help='use histogram templates' )
parser.add_argument( '--useToySignal',  dest='useToySignal', default=False, action='store_true', help='use gaussian as signal' )
parser.add_argument( '--useToyBackground',  dest='useToyBackground', default=False, action='store_true', help='use exponential as background ' )
parser.add_argument( '--noRunCombine',  dest='noRunCombine', default=False, action='store_true', help='Dont run combine, use existing results' )
parser.add_argument( '--combineDir',  dest='combineDir', default=None, help='path to combine directory' )

options = parser.parse_args()

_WLEPBR = (1.-0.6741)
_XSFILE   = 'cross_sections/photon15.py'
_LUMI     = 36000

DEBUG = 1

ROOT.gSystem.Load('My_double_CB/RooDoubleCB_cc.so')

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
                 'signal'   : SampleInfo ( pdf_prefix = 'cb_MadGraphResonance', params_prefix = [
                                                            'cb_cut1_MadGraphResonance', 'cb_cut2_MadGraphResonance', 'cb_mass_MadGraphResonance',                                                                        'cb_sigma_MadGraphResonance', 'cb_power1_MadGraphResonance', 'cb_power2_MadGraphResonance'
                                                                       ], 
                                         useLumi = True, useMET = True, usePDF = True,
                              ),
                 'WGamma'        : SampleInfo( name = 'WGamma',      useLumi = True,  useMET = False, usePDF = False, ),
                 'TTbar'         : SampleInfo( name = 'TTbar',       useLumi = False, useMET = False, usePDF = False, ),
                 'TTG'           : SampleInfo( name = 'TTG',         useLumi = False, useMET = False, usePDF = False, ),
                 'Wjets'         : SampleInfo( name = 'Wjets',       useLumi = False, useMET = False, usePDF = False, ),
                 'Zgamma'        : SampleInfo( name = 'Zgamma',      useLumi = False, useMET = False, usePDF = False, ),
                 'GammaGamma'    : SampleInfo( name = 'GammaGamma',  useLumi = False, useMET = False, usePDF = False, ),
                 'Backgrounds'   : SampleInfo( name = 'Backgrounds', useLumi = False, useMET = False, usePDF = False, ),
                 'toydata'       : {'pdf': 'toydata'},
                 'toysignal'     : {'pdf': 'gauss'},
                 'toybkg'        : {'pdf': 'exp'},
             }


    bins = [
        # mu/el channel, photons in th barrel/endcap
        {'channel' : 'mu', 'eta' : 'EB' },
        #{'channel' : 'mu', 'eta' : 'EE' },
        #{'channel' : 'el', 'eta' : 'EB' },
        #{'channel' : 'el', 'eta' : 'EE' },
    ]

    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )

    #signal_masses = [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3500, 4000]
    signal_masses = [300, 350, 400, 450, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000] 
    #signal_masses   = [900]
    signal_widths  = ['5', '0p01']

    if options.doVarOptimization:

        var_opt = {}

        kine_vars = [ 
                     #{ 'name' : 'mt_incl_lepph_z', 'color' : ROOT.kBlue},
                     #{ 'name' : 'm_incl_lepph_z' , 'color' : ROOT.kRed },
                     #{ 'name' : 'mt_rotated' , 'color' : ROOT.kRed },
                     { 'name' : 'mt_fulltrans'   , 'color' : ROOT.kBlack , 'range' : [150, 3000]},
                     #{ 'name' : 'mt_constrwmass' , 'color' : ROOT.kGreen },
                     #{ 'name' : 'ph_pt'          , 'color' : ROOT.kMagenta },
                   ]

        for var in kine_vars :
            var_opt[var['name']] = MakeLimits( 
                                              plotvar=var['name'],
                                              wskeys = ws_keys,
                                              masspoints  = signal_masses, 
                                              widthpoints = signal_widths,
                                              #backgrounds=['WGamma', 'TTG', 'TTbar', 'Wjets', 'Zgamma'],
                                              backgrounds=['WGamma'], 
                                              #backgrounds=['Backgrounds'], 
                                              baseDir=options.baseDir,
                                              bins=bins,
                                              outputDir='%s/%s/%s' %( options.outputDir, 'VarOpt', var['name'] ),
                                              useToySignal=options.useToySignal,
                                              useToyBackground=options.useToyBackground,
                                              useHistTemplates=options.useHistTemplates,
                                             )
                                                     

        for opt in var_opt.values() :
            opt.setup( kine_vars )


        combine_jobs = []
        for opt in var_opt.values() :
            combine_jobs += opt.get_combine_files() 

        if not options.noRunCombine :
            #for job in combine_jobs:
            #    os.system('bsub -q 1nh -o %s -e %s %s'%(job.replace('.sh', '_log.txt'), job.replace('.sh', '_err.txt'), job))

            #wait_for_jobs( 'yofeng')

            jdl_name = '%s/job_desc.jdl'  %( options.outputDir )
            make_jdl( combine_jobs, jdl_name )

            os.system( 'condor_submit %s' %jdl_name )

            wait_for_jobs( 'run_combine')

            results = {}
            for key, opt in var_opt.iteritems() :
                print key
                results[key] = opt.get_combine_results()

            print results

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
    file_entries.append('when_to_transfer_output = ON_EXIT_OR_EVICT')
    file_entries.append('transfer_output = True')
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
            


def Width_str2float( width ):
    widthdict = {"5": 5, "0p01": 0.01}
    try:
       fwidth = float(widthdict[width])
    except KeyError:
       print "Can not turn the width into float"
    return fwidth

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

        if n_limits == 0 :
            return
        else :
            print '%d Jobs still running' %n_limits


class MakeLimits( ) :

    def __init__(self, **kwargs) :

        self.fail=False

        self.plotvar          = kwargs.get('plotvar'    ,  None )
        self.masspoints       = kwargs.get('masspoints' ,  None )
        self.widthpoints      = kwargs.get('widthpoints',  None )
        self.baseDir          = kwargs.get('baseDir'    ,  None )
        self.outputDir        = kwargs.get('outputDir'  ,  None )
        self.bins             = kwargs.get('bins'       ,  None )
        self.bkgnames         = kwargs.get('backgrounds',  None )

        self.wskeys = kwargs.get('wskeys', None)

        self.useToySignal     = kwargs.get('useToySignal',     False )
        self.useToyBackground = kwargs.get('useToyBackground', False )

        self.useHistTemplates = kwargs.get('useHistTemplates', False )

        self.wstag = kwargs.get('wsTag', 'base' )
        self.method = kwargs.get('method', 'AsymptoticLimits' )

        self.xvarname = kwargs.get('xvarname', 'x_m')

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

        if self.plotvar == None or not isinstance( self.plotvar, str ) :
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
           self.weightMap = analysis_utils.read_xsfile( _XSFILE, _LUMI, print_values=True )


    def setup( self , kine_vars ):

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
            self.make_exp_background( kine_vars, -0.01, 200 )

        else:
            # -------------------------------------------------
            # Copy the background funcitons and set variables to constant as needed
            # -------------------------------------------------
            self.prepare_background_functions( kine_vars )

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
            self.make_gauss_signal( kine_vars, 50 )

        else:
            # -------------------------------------------------
            # Copy the signal funcitons and set variables to constant as needed
            # -------------------------------------------------
            self.prepare_signal_functions( kine_vars )

        #signal_data = {}
        if options.useHistTemplates :
            # -------------------------------------------------
            # Get the normalization info from the samples
            # -------------------------------------------------
            signal_file = '%s/%s.root' %( self.baseDir, self.signal_ws)
            signal_data = self.get_signal_data( signal_file, self.signal_ws,  self.mass_points, self.plot_var, self.bins )


        # -------------------------------------------------
        # Since we're blind, make toy data
        # -------------------------------------------------
        for ibin in self.bins :
            self.dataname = 'toydata'
            #binid = '%s_%s' %( ibin['channel'], ibin['eta'] )

            #wgamma_entry = get_workspace_entry( 'Wgamma', ibin['channel'], ibin['eta'], self.plot_var )
            #wjets_entry  = get_workspace_entry( 'wjets' , ibin['channel'], ibin['eta'], self.plot_var )

            if options.useHistTemplates :
                wgamma_entry = wgamma_entry.replace( 'dijet', 'datahist' )

            #self.generate_toy_data( kine_vars, sigpars = ['Mass_900_Width_5'], signorms = [1.0], data_norm=20.0)
            self.generate_toy_data( kine_vars ) 


        #---------------------------------------
        # Prepare the data cards for limits
        #---------------------------------------

        self.allcards = {}

        self.generate_all_cards( kine_vars )


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


    def generate_all_cards( self, kine_vars ):

        for width in self.widthpoints:
            outputdir = self.outputDir + '/' + 'Width' + width
            if not os.path.isdir( outputdir ) :
               print " creating directory", outputdir
               os.makedirs( outputdir )

            for mass in self.masspoints:

                for ibin in self.bins:

                    sigpar = "_".join( ['Mass', str(mass), 'Width', width, ibin['channel']] )

                    card_path = '%s/wgamma_test_%s_%s.txt' %(outputdir, self.plotvar, sigpar )

                    self.generate_card( card_path, sigpar, kine_vars , ibin)

                    self.allcards.setdefault(sigpar, {})
                    self.allcards[sigpar][self.plotvar] =  card_path 


    def generate_card( self, outputCard, sigpar, kine_vars, ibin, tag='base' ) :
    
        card_entries = []
    
        section_divider = '-'*100
    
        card_entries.append( 'imax %d number of bins' %len( self.bins ) )
        #card_entries.append( 'jmax %d number of backgrounds' %len( self.backgrounds) ) 
        card_entries.append( 'jmax * number of backgrounds' )
        card_entries.append( 'kmax * number of nuisance parameters' )
    
        card_entries.append( section_divider )
    
        max_name_len = max( [len(x) for x in self.bkgnames ] )
        max_path_len = max( [len(x.outputfname) for x in self.backgrounds.values() ] )
    
        all_binids = []
        #signal_norm = 1.0
        sig = self.signals[sigpar]
        #for ibin in self.bins :
        bin_id = '%s_%s' %( ibin['channel'], ibin['eta'] )
        all_binids.append(bin_id)
   
        card_entries.append( 'shapes Resonance %s %s %s:%s' %( bin_id, sig['file'], sig['workspace'], sig['pdf'] ) )
    
        for bkgname, bkg in self.backgrounds.iteritems() :
            if options.useHistTemplates :
                bkg_entry = bkg_entry.replace('dijet', 'datahist' )
            card_entries.append( 'shapes %s %s %s %s:%s' %( bkgname.ljust( max_name_len ), bin_id, bkg.outputfname.ljust( max_path_len ), bkg.GetWSName(), bkg.GetPDFName( kine_vars[0]['name'], ibin['channel'] ) ) )
    
        data = self.datas[self.dataname]
        card_entries.append( 'shapes data_obs %s %s %s:%s' %( bin_id, data['file'], data['workspace'], data['data'] ) )
    
        card_entries.append( section_divider )
    
        card_entries.append( 'bin          ' + '    '.join( all_binids ) )
        card_entries.append( 'observation  ' + '    '.join( ['-1.0']*len(self.bins) ) )
    
        card_entries.append( section_divider )
    
        rate_entries = []
        for ibin in self.bins :
            bin_id = '%s_%s' %( ibin['channel'], ibin['eta'] )
   
            # signal rate
            # use signal _norm to normalize signal distributions
            #rate_entries.append( str(1.0) )
            rate_entries.append( str(sig['rate']) )
            #for bkgdic in self.backgrounds :
            for bkgname, bkg in self.backgrounds.iteritems():
                #rate_entries.append( str(bkgdic['norm'][bin_id]) )
                rate_entries.append( str(bkg.norm[0]) )
                #bkg rate
                #rate_entries.append( str(1.0) )
    
        bin_entries = []
        for b in all_binids :
            bin_entries += [b]*(len(self.backgrounds)+1)
    
        card_entries.append( 'bin      ' + '    '.join(bin_entries )  )
        card_entries.append( 'process  ' + '    '.join( ( ['Resonance'] + [x for x in self.bkgnames])*len(self.bins) ) )
        card_entries.append( 'process  ' + '    '.join( [str(x) for x in range(0, len(self.backgrounds) +1 ) ]*len(self.bins) ) )
        #card_entries.append( 'rate     ' + '    '.join( [str(signal_norm), str(backgrounds[0]['norm']) ]*len(bins) ) )
        card_entries.append( 'rate     ' + '    '.join( rate_entries )  )
    
        card_entries.append( section_divider )
    
        #lumi_vals = ['1.05'] * (len(all_binids)*( len(self.backgrounds) + 1 ))
        lumi_vals = ['1.025'] + [ '1.025' if bkg.useLumi else '-' for bkg in self.backgrounds.values() ]
        bkg_vals = (['-'] + ['1.20']*len(self.backgrounds) )*len(all_binids)
        signal_met = ( ['1.03'] + ['-']*len(self.backgrounds) )*len( all_binids) 
        signal_pdf = ( ['1.05'] + ['-']*len(self.backgrounds) )*len( all_binids)

        card_entries.append( 'lumi       lnN    ' + '    '.join(lumi_vals   ) )
        #card_entries.append( 'bkgelse    lnN    ' + '    '.join(bkg_vals    ) )
        card_entries.append( 'met        lnN    ' + '    '.join(signal_met ) )
        card_entries.append( 'pdf        lnN    ' + '    '.join(signal_pdf ) )

        # assign 30% normalization uncertainty in all backgrounds from data-driven
        for bkgname in self.backgrounds:
            if not self.backgrounds[bkgname].useLumi:
               bkg_norms = ['-'] + ['1.30' if namebkg == bkgname else '-' for namebkg in self.backgrounds]
               card_entries.append('%s_norm lnN    '%bkgname + '    '.join( bkg_norms ))

        #parameter errors
        for iparname, iparval in self.params.iteritems():
            #card_entries.append('%s param %.2f %.2f'%(iparname, iparval[0], iparval[1]))
            card_entries.append('%s flatParam'%iparname)

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


    def generate_toy_data( self, kine_vars, sigpars=None, signorms = None, data_norm=None ) :

        if not os.path.isdir( self.outputDir+'/'+self.dataname ) :
           print " creating directory %s/%s"%(self.outputDir, self.dataname)
           os.makedirs( self.outputDir+'/'+self.dataname )

        workspace = ROOT.RooWorkspace( '_'.join(['workspace', self.dataname]) )

        for var in kine_vars :

            suffix = "%s_%s_%s_%s"%(self.bins[0]['channel'], var['name'], self.wstag, self.bins[0]['eta'])
    
            pdfs = []
            norms = []
            xvar = None

            ## background
            for bkgname, bkg in self.backgrounds.iteritems():

                #if bkgname != 'WGamma':
                #   print "[ \033[1;31mProblem running the toy data generation process. Skip %s. Only play with WGamma for now\033[0m  ]"%bkgname
                #   continue
       
                #full_path = bkg['file'] 
                #ofile = ROOT.TFile.Open( full_path )
                ofile = ROOT.TFile.Open( bkg.outputfname )
        
                #ws = ofile.Get( bkg['workspace'] )
                ws = ofile.Get( bkg.GetWSName() )
        
                if options.useHistTemplates :
                    print hist_key
                    pdfs.append(ws.data( hist_key ))
                    norms.append(pdfs[-1].sumEntries())
                else :
                    #norms.append( ws.var( '%s_norm'%bkg['pdf'] ).getVal() )
                    #pdfs.append(  ws.pdf( bkg['pdf'] ) )
                    #norms.append( ws.var('%s_norm'%bkg.GetPDFName(var['name'], self.bins[0]['channel'])).getVal() )
                    norms.append( bkg.norm[0] )
                    pdfs.append( ws.pdf( bkg.GetPDFName(var['name'], self.bins[0]['channel'])) )
        
                if xvar is None :
                    xvar = ws.var( self.xvarname )
        
                ofile.Close()
    
            ## mix into some fake signal
            if sigpars:
               print "add some fake signals for fun..."
               for sigpar, signorm in zip(sigpars, signorms):
                   try:
                       sig = self.signals[sigpar]
                       ofile = ROOT.TFile.Open( sig['file'] )
                   except:
                       print "can not open the signal workspace file: %s Please x-check self.signals collection"%self.signals[sigpar]['file']
                       raise
                   ws = ofile.Get( sig['workspace'] ) 
                   pdfs.append( ws.pdf( sig['pdf'] ) )
                   norms.append( ws.var( '%s_norm'%sig['pdf']).getVal() * signorm )
                    
            print "Normalization:: ", norms
        
            if len( pdfs ) == 1 :
                if options.useHistTemplates :
                    dataset = ROOT.RooDataHist( pdfs[0], 'toydata_%s' %suffix )
                else :
                    if data_norm is None :
                        norm = int(norms[0])
                    else :
                        norm = data_norm
                    dataset = pdfs[0].generate(ROOT.RooArgSet(xvar) , int(norm), ROOT.RooCmdArg( 'Name', 0, 0, 0, 0, 'toydata_%s' %suffix ) )
            else :
                total = sum( [int(x) for x in norms ] )
        
                fractions = [ float(x)/total for x in norms ] 
    
                print "total ", total, " fractions", fractions
        
                if options.useHistTemplates :
        
                    dataset = ROOT.RooDataHist( pdfs[0], 'toydata_%s' %suffix )
        
                    for pdf in pdfs[1:] :
                        dataset.add( pdf )
        
                else :
                    print "**** start generate toy data *****"
                    pdfList = ROOT.RooArgList()
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
                    dataset = summed.generate( ROOT.RooArgSet(xvar), int(total), ROOT.RooCmdArg( 'Name', 0, 0, 0, 0, 'toydata_%s' %suffix ) )
        
            # not clear why we have to rename here
            #getattr( out_ws, 'import' ) ( dataset, ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'toydata_%s' %suffix ) )
            getattr( workspace, 'import' ) ( dataset )

            outputfile = '%s/%s/%s.root' %( self.outputDir, self.dataname, workspace.GetName() )
    
            workspace.writeToFile( outputfile )

            self.datas.update( 
                               { self.dataname: { 'channel': "%s_%s"%(self.bins[0]['channel'], self.bins[0]['eta']), 'file': outputfile, 'workspace': workspace.GetName(), 'data': dataset.GetName() } }
                             )

    def prepare_background_functions( self, kine_vars ) :
        
        ## loop over backgrounds
        for bkgn in self.bkgnames:

            print " prepare background functions for ", bkgn

            #ofile = ROOT.TFile.Open( '%s/MCBkgWS/workspace_%s.root' %( self.baseDir, bkgn.lower() ), 'READ' )
            ofile = ROOT.TFile.Open( '%s/MCBkgWS/%s' %( self.baseDir, self.wskeys[bkgn].GetRootFileName() ), 'READ' )
    
            #ws_in = ofile.Get( "workspace_" + bkgn.lower() )
            ws_in = ofile.Get( self.wskeys[bkgn].GetWSName() )
    
            ws_out = ROOT.RooWorkspace( self.wskeys[bkgn].GetWSName() )
    
            for var in kine_vars :
                for ibin in self.bins :

                    #suffix = "_".join([bkgn, self.bins[0]['channel'], var['name'], self.wstag, self.bins[0]['eta']])

                    #ws_entry = "_".join( [self.wskeys[bkgn].pdf_prefix, suffix])

                    ws_entry = self.wskeys[bkgn].GetPDFName( var['name'], ibin['channel'] )

                    if DEBUG:
                       print ws_entry
    
                    if options.useHistTemplates :
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
                        for ipar in self.wskeys[bkgn].GetParNames( var['name'], ibin['channel'] ):
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

                        var = ws_in.var('x_m')
                        var.setBins(660)
                        getattr( ws_out, 'import' ) ( var )
    
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
            self.wskeys[bkgn].SetOutputName( self.outputDir )
            ws_out.writeToFile( self.wskeys[bkgn].outputfname )

            ## infor for generating toy data and datacard
            #self.backgrounds.update(
            #                       { bkgn: { 'channel': "%s_%s"%(self.bins[0]['channel'], self.bins[0]['eta']), 'file': outputfile, 'workspace': ws_out.GetName(), 'pdf': pdf.GetName(), 'params': params} }
            #                       )
            self.backgrounds.update( { bkgn: self.wskeys[bkgn]} )

    def prepare_signal_functions( self, kine_vars ) :
        
        for mass in self.masspoints:
            for width in self.widthpoints:
                for var in kine_vars :
                    for ibin in self.bins :

                        sigpar = "_".join(['Mass', str(mass), 'Width', width, ibin['channel']])

                        ## get the cross section and scale factor information
                        scale = self.weightMap['ResonanceMass%d'%mass]['scale']

                        ifile = ROOT.TFile.Open( '%s/SignalWS/workspace_%s_%s.root' %( self.baseDir, self.signame, sigpar ), 'READ' )

                        if DEBUG:
                           print "workspace_" + self.signame + '_' + sigpar

                        ws_in = ifile.Get( "workspace_" + self.signame + '_' + sigpar )

                        ws_out = ROOT.RooWorkspace( "workspace_" + self.signame + '_' + sigpar )

                        sigfitparams = OrderedDict()

                        suffix = "_".join([sigpar, var['name'], self.wstag, ibin['eta']])

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

                        var = ws_in.var('x_m')
                        var.setBins(660)
                        getattr( ws_out, 'import' ) ( var )

                        norm_var = ws_in.var( '%s_norm' %ws_entry )
                        rate = norm_var.getVal() * scale
                        norm_var.setVal( norm_var.getValV() * scale )
                        norm_var.setError( norm_var.getError() * scale )
                        #norm_var.setError(0.0)
                        #norm_var.setConstant( False )
                        norm_var.setConstant()
                        #getattr( ws_out, 'import' ) ( norm_var )
                        getattr( ws_out, 'import' ) ( pdf )   

                        ifile.Close()

                        outputfile = '%s/%s/%s.root' %( self.outputDir, self.signame, ws_out.GetName() )
                        ws_out.writeToFile( outputfile )

                        ## info for generating toy data and datacard
                        self.signals.update(
                                            {sigpar : {'channel': "%s_%s"%(ibin['channel'], ibin['eta']), 'file': outputfile, 'workspace': ws_out.GetName(), 'pdf': pdf.GetName(), 'rate': rate, 'params': sigfitparams} }
                                           )


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
                        binid = '%s_%s' %( ibin['channel'], ibin['eta'] )
    
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

    def make_gauss_signal(self, kine_vars, normvalue) :

        for mass in self.masspoints:
            for width in self.widthpoints:
                sigpar = "_".join(['Mass', str(mass), 'Width', width])

                ## one workspace/rootfile for one signal grid point
                #workspace = ROOT.RooWorkspace( 'workspace_' + self.signame + '_Mass' + str(mass) + '_Width' + width )
                workspace = ROOT.RooWorkspace( "_".join(['workspace', self.signame, sigpar]) )
                
                for var in kine_vars :
    
                    suffix = "_".join([sigpar, self.bins[0]['channel'], var['name'], self.wstag, self.bins[0]['eta']])

                    if DEBUG:
                       print suffix
    
                    xvar = ROOT.RooRealVar( self.xvarname, self.xvarname,  var['range'][0], var['range'][1] )
    
                    mean = ROOT.RooRealVar( 'mean_%s' %suffix, 'mean', mass )
                    sigma = ROOT.RooRealVar( 'sigma_%s' %suffix, 'sigma', mass*Width_str2float(width)*0.01 )
                    mean.setConstant()
                    sigma.setConstant()
    
                    norm = ROOT.RooRealVar( 'gauss_%s_norm' %suffix, 'normalization', normvalue )
                    norm.setConstant()
    
                    signal = ROOT.RooGaussian( 'gauss_%s' %suffix, 'signal', xvar, mean, sigma )
    
                    #getattr( workspace, 'import' ) ( dataset, ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'gaussignal_%s' %suffix ) )
                    getattr( workspace, 'import' ) ( signal )
                    getattr( workspace, 'import' ) ( norm )
   
                outputfile = '%s/%s/%s.root' %( self.outputDir, self.signame, workspace.GetName() )
                workspace.writeToFile( outputfile )

                self.signals.update( 
                                     {sigpar : {'channel': "%s_%s"%(self.bins[0]['channel'], self.bins[0]['eta']), 'file': outputfile, 'workspace': workspace.GetName(), 'pdf': signal.GetName() } } 
                                   )
    
    
    def make_exp_background(self, kine_vars, expvalue, normvalue ) :

        workspace= ROOT.RooWorkspace( "workspace_%s"%self.bkgnames[0] )

        for var in kine_vars :
    
            suffix = "%s_%s_%s_%s"%(self.bins[0]['channel'], var['name'], self.wstag, self.bins[0]['eta'])

            if DEBUG:
               print suffix

            xvar = ROOT.RooRealVar( self.xvarname, self.xvarname,  var['range'][0], var['range'][1])
    
            # parameters of p.d.f must be set to constant, otherwise the combine tool would yield weird result
            power = ROOT.RooRealVar( 'power_%s' %suffix, 'power', expvalue )
            power.setConstant()
    
            background = ROOT.RooExponential( 'exp_%s' %suffix, 'background', xvar, power )
            norm = ROOT.RooRealVar( 'exp_%s_norm' %suffix, 'background normalization', normvalue )
            #norm.setError(10.0)
            norm.setError(0.0)
            norm.setConstant()
    
            #getattr( workspace, 'import' ) ( dataset, ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'gaussignal_%s' %suffix ) )
            getattr( workspace, 'import' ) ( background )
            getattr( workspace, 'import' ) ( norm ) 

        outputfile = "%s/%s/%s.root"%( self.outputDir, self.bkgnames[0], workspace.GetName() )
        workspace.writeToFile( outputfile )

        ## infor for generating toy data and datacard
        self.backgrounds.update( 
                                   {self.bkgnames[0]: { 'channel': "%s_%s"%(self.bins[0]['channel'], self.bins[0]['eta']), 'file': outputfile, 'workspace': workspace.GetName(), 'pdf': background.GetName() } } 
                               )


    def write_combine_files( self ) :
    
        jobs = []
        output_files = {}
        for width in self.widthpoints:
            output_files.setdefault( width, {} )

        # this should be improved
        if self.method == 'AsymptoticLimits' or self.method == 'MaxLikelihoodFit' :
    
            for sigpar, vardic in self.allcards.iteritems() :

                wid = sigpar.split('Width_')[1].split('_')[0]
    
                fname = '%s/Width%s/run_combine_%s.sh' %(self.outputDir, wid, sigpar)
                #ofile = open( fname, 'w' )
                #ofile.write( '#!/bin/bash\n' )
                ofile = open( fname, 'w' )
                ofile.write( '#!/bin/tcsh\n' )
                ofile.write( 'cd %s \n' %options.combineDir )
                ofile.write( 'eval `scramv1 runtime -csh` \n' )

                mass = int(sigpar.split('_')[1])
                    
                for var, card in vardic.iteritems() :

                    print var, card
    
                    log_file = '%s/Width%s/results_%s_%s.txt'%( self.outputDir, wid, var, sigpar )
                    if self.method == 'AsymptoticLimits' :
                        ofile.write( 'combine -M AsymptoticLimits -m %d --rMin 0.01 --rMax 10 %s >& %s \n'  %( mass, card, log_file ))
                    if self.method == 'MaxLikelihoodFit' :
                        ofile.write( 'combine -M MaxLikelihoodFit -m %d --expectSignal=1 %s --plots -n %s >> %s \n' %( mass, card, var, log_file ) )
    
                    output_files[wid].setdefault( mass, {} )
                    output_files[wid][mass][var] = log_file
    
                #ofile.write( ' cd - \n' )
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
                        ofile.write( '#!/bin/tcsh\n' )
                        ofile.write( 'cd %s \n' %combine_dir ) 
                        ofile.write( 'eval `scramv1 runtime -csh` \n' ) 
                        
                        ofile.write( 'combine -M HybridNew --frequentist --testStat LHC -H ProfileLikelihood --fork 1 -m %d %s > %s \n ' %( pt, card, log_file ) )
    
                        ofile.write( ' cd - \n' )
                        ofile.write( 'echo "^.^ FINISHED ^.^" \n' )
                
                        os.system( 'chmod 777 %s/run_combine.sh' %(output_dir) )
    
                        ofile.close()
    
    
        return ( jobs, output_files )

    def get_combine_results( self ) : 
    
        combine_results = {}

        for width in self.widthpoints:
            combine_results.setdefault( width, {})

            for mass, vardic in self.output_files[width].iteritems() :
                for var, f in vardic.iteritems() :
                    result = self.process_combine_file( f, mass )
                    #combine_results.setdefault(var, {})
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
