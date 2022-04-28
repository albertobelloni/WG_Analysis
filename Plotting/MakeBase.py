#!/usr/bin/env python
from argparse import ArgumentParser
if "parser" not in locals(): parser = ArgumentParser()
parser.add_argument('--baseDirMuG',      default=None,          help='Path to muon base directory')
parser.add_argument('--baseDirElG',      default=None,          help='Path to electron base directory')
parser.add_argument('--baseDirMuMu',     default=None,          help='Path to muon base directory')
parser.add_argument('--baseDirElEl',     default=None,          help='Path to electron base directory')
parser.add_argument('--baseDirMu',       default=None,          help='Path to muon base directory')
parser.add_argument('--baseDirEl',       default=None,          help='Path to electron base directory')
parser.add_argument('--outputDir',       default=None,          help='Output directory to write histograms')
parser.add_argument('--dataDir',         default=None,          help='IO directory to data')
parser.add_argument('--data',            action="store_true",   help='Use data or MC')
parser.add_argument('--batch',           action="store_true",   help='Supress X11 output')
parser.add_argument('--condor',          action="store_true",   help='run on condor')
parser.add_argument('--year',            default=2016,          type=int,            help='Set run year')
parser.add_argument('--quiet',           action="store_true",   help='Quiet output')
parser.add_argument('--nodataFrame',     dest='dataFrame',  action='store_false',    help='backwards compatibility for pre-2019 releases of ROOT')
#parser.add_argument('--weightHistName',     default="weighthist",  type=str ,        dest='weightHistName',         help='name of weight histogram')

## add additional argument if addparser() is defined
if "addparser" in locals(): addparser(parser)
options = parser.parse_args()

import ROOT
from itertools import product
from collections import OrderedDict,defaultdict
import numpy as np
from math import pi, sqrt
import os, sys
import pdb
import selection_defs as defs
from SampleManager import SampleManager, f_Obsolete
from FitManager import FitManager
#ROOT.PyConfig.IgnoreCommandLineOptions = True
import getpass
username = getpass.getuser()
username = 'yihuilai/WG_Merge'
recdd = lambda : defaultdict(recdd) ## define recursive defaultdict


_FILENAME = 'tree.root'
_TREENAME = 'UMDNTuple/EventTree'
#datestr   = "2021_08_27"
#datestr   = "2021_09_17"
datestr   = "2022_01_27"

lumiratio = 1.
datestrmm=datestree=datestreg=datestrmg=""
if options.year == 2016:
    _XSFILE   = 'cross_sections/photon16.py'
    _LUMI     = 36330
    _SAMPCONF = 'Modules/Resonance2016.py'
    etastr    = ""
    #etastr    = "&& !(ph_eta[0]<0 && ph_phi[0]<16*pi/18 && ph_phi[0]>13*pi/18)"
    lumiratio = 1.
    #lumiratio = 1./(1-3./72)
elif options.year == 2017:
    _SAMPCONF = 'Modules/Resonance2017.py'
    _XSFILE   = 'cross_sections/photon17.py'
    _LUMI     = 41530
    #etastr    = "&& !(ph_eta[0]>0 && ph_phi[0]>15*pi/18)"
    #lumiratio = 1./(1-3./72.)
elif options.year == 2018:
    _SAMPCONF = 'Modules/Resonance2018.py'
    _XSFILE   = 'cross_sections/photon18.py'
    _LUMI     = 59740
    #etastr    = "&& !(ph_phi[0]<5*pi/18 && ph_phi[0]>3*pi/18)"
    #lumiratio = 1./(1-1./18)
    #datestr   = "2020_02_11"
    #datestrmm = datestree   = "2020_04_25" # beta for mumu elel


filename = __file__.rstrip(".py").split("/")[-1]
if options.batch:
    ROOT.gROOT.SetBatch(True)
if options.outputDir is None :
    options.outputDir = "plots/" + filename
if options.outputDir is not None :
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )

if options.condor and not ('alt_condor' in locals() and alt_condor):
    arguments = " ".join([ a for a in sys.argv[1:] if a!="--condor"])
    working_dir = os.getcwd()
    condor_script = ['getenv=True',
                     'universe = vanilla',
                     'Executable = {workd}/{thisfile}.py',
                     'should_transfer_files = NO',
                     'Requirements = TARGET.FileSystemDomain == "privnet" && (TARGET.OpSysMajorVer == 7)',
                     'Output = {workd}/log/{thisfile}_$(cluster)_$(process).stdout',
                     'Error =  {workd}/log/{thisfile}_$(cluster)_$(process).stderr',
                     'Log =    {workd}/log/{thisfile}_$(cluster)_$(process).condor',
                     'Arguments = {}',
                     'Minute = 60',
                     'on_exit_hold =  (ExitCode != 0)',
                     'periodic_release = NumJobStarts<2 && (CurrentTime - JobCurrentStartDate) >= 10 * $(MINUTE)',
                     'Queue',]
    condor_script = "\n".join(condor_script)
    condor_script = condor_script.format(arguments, thisfile = filename, workd = working_dir)
    job_desc_file = "{workd}/log/{thisfile}.jdl".format(thisfile = filename, workd = working_dir)
    print condor_script
    with open(job_desc_file, "w") as fo:
        fo.write(condor_script)
    condor_command = "condor_submit %s" %job_desc_file
    print condor_command
    os.system(condor_command)
    sys.exit()

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(ROOT.kBird)
#ROOT.gStyle.SetOptFit(1)

tColor_Off="\033[0m"                    # Text Reset
tPurple="\033[0;35m%s"+tColor_Off       # Purple

# if no option is given, here are the default directories to read
#if options.baseDirMuG is None: options.baseDirMuG = "/data2/users/kakw/Resonances%i/LepGamma_mug_%s/WithSF/"%(options.year,datestrmg or datestr)
if options.baseDirMuG is None: options.baseDirMuG = "/data/users/%s/Resonances%i/LepGamma_mug_%s/WithSF/"%(username, options.year,datestrmg or datestr)
#if options.baseDirElG is None: options.baseDirElG = "/data2/users/kakw/Resonances%i/LepGamma_elg_%s/WithSF/"%(options.year,datestreg or datestr)
if options.baseDirElG is None: options.baseDirElG = "/data/users/%s/Resonances%i/LepGamma_elg_%s/WithSF/"%(username, options.year,datestreg or datestr)
if options.baseDirMuMu is None: options.baseDirMuMu = "/data/users/%s/Resonances%i/LepLep_mumu_%s/WithSF/"%(username, options.year,datestrmm or datestr)
if options.baseDirElEl is None: options.baseDirElEl = "/data/users/%s/Resonances%i/LepLep_elel_%s/WithSF/"%(username, options.year,datestree or datestr)
if options.baseDirMu is None: options.baseDirMu = "/data/users/%s/Resonances%i/SingleLep_mu_%s/WithSF/"%(username, options.year,datestrmm or datestr)
if options.baseDirEl is None: options.baseDirEl = "/data/users/%s/Resonances%i/SingleLep_el_%s/WithSF/"%(username, options.year,datestree or datestr)
#options.baseDirElG = "/data/users/friccita/WGammaNtuple/LepGamma_elg_2019_04_11/"

baseel = 'ph_n==1 && el_n==1 && el_pt35_n==1 && mu_n==0'
basemu = 'ph_n==1 && mu_n==1 && mu_pt30_n==1 && el_n==0'

passpix = '&& ph_hasPixSeed[0]==0'  #Pixel seed
failpix = '&& ph_hasPixSeed[0]==1'
passcsev = '&& ph_passEleVeto[0]==1' #CSEV
failcsev = '&& ph_passEleVeto[0]==0'

phptgt = "&&ph_pt[0]>%i"
phptlt = "&&ph_pt[0]<%i"
elptgt = "&&el_pt[0]>%i"
elptlt = "&&el_pt[0]<%i"
muptgt = "&&mu_pt[0]>%i"
muptlt = "&&mu_pt[0]<%i"
metgt = "&&met_pt[0]>%i"
metlt = "&&met_pt[0]<%i"

phpt50 = "&&ph_pt[0]>50"
phpt80 = "&&ph_pt[0]>80"
elpt40 = "&&el_pt[0]>40"
metlt25 = '&&met_pt<25'
metgt25 = '&&met_pt>25'
metlt40 = '&&met_pt<40'
metgt40 = '&&met_pt>40'

ph_eb =  ' && ph_IsEB[0]'
el_eb =  ' &&abs(el_eta[0])<2.1'
elaetalt =  ' &&abs(el_eta[0])<%.3g'

invZ = '&& abs(m_lep_ph-91)>20'
massZ = '&& abs(m_lep_ph-91)<20'
invzlt = '&& abs(m_lep_ph-91)>%i'
csvmed = " && jet_CSVMedium_n>1"
csvveto = " && jet_CSVMedium_n==0"

nophmatch = "&& !(ph_truthMatchPh_dr[0]<ph_truthMatchEl_dr[0])"
phmatch = "&& (ph_truthMatchPh_dr[0]<ph_truthMatchEl_dr[0])"
flatphi = "ph_phi[0]+3.1416*(1+2*(ph_eta[0]>0))"

UNBLIND = "ph_hasPixSeed[0]==1 || met_pt<40"
#weight="PUWeight*NLOWeight"
weight = defs.get_weight_str("nosf")
if options.year == 2018:
    weight = weight.replace("prefweight","1")
pie = 3.1416

## read MuG samples
sampManMuG= SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio,
                            readHists=False , weightHistName = "weighthist", dataFrame = options.dataFrame, quiet = options.quiet)

## read ElG samples
sampManElG= SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio ,
                            readHists=False , weightHistName = "weighthist", dataFrame = options.dataFrame, quiet = options.quiet)

## read MuMu samples
sampManMuMu= SampleManager( options.baseDirMuMu, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio,
                            readHists=False , weightHistName = "weighthist", dataFrame = options.dataFrame, quiet = options.quiet)

## read ElEl samples
sampManElEl= SampleManager( options.baseDirElEl, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio ,
                            readHists=False , weightHistName = "weighthist", dataFrame = options.dataFrame, quiet = options.quiet)

## read Mu samples
sampManMu= SampleManager( options.baseDirMu, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio,
                            readHists=False , weightHistName = "weighthist", dataFrame = options.dataFrame, quiet = options.quiet)

## read El samples
sampManEl= SampleManager( options.baseDirEl, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio ,
                            readHists=False , weightHistName = "weighthist", dataFrame = options.dataFrame, quiet = options.quiet)
