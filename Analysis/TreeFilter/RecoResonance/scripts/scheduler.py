#!/usr/bin/env python
import os
from argparse import ArgumentParser
import getpass
username = getpass.getuser()

import scheduler_base
from scheduler_base import JobConf

p = ArgumentParser()
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--clean', dest='clean', default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local', dest='local', default=False, action='store_true', help='Run locally' )
p.add_argument( '--test', dest='test', default=False, action='store_true', help='Run a test job' )
p.add_argument( '--year', dest='year', default=2016, type=int, help='run year' )
options = p.parse_args()

if not options.check :
    options.run = True
else :
    options.run = False

options.batch = ( not options.local )

### ATTENTION! Here you specify the directory containing the raw ntuples that you want to process further.
### Also specify the version number of the raw ntuples with the version_* variables below.
base = '/store/group/WGAMMA'
baseqcd = '/store/user/mseidel/WGamma'
options.nFilesPerJob = 10

options.nproc = 1
options.treename='UMDNTuple/EventTree'
options.exename='RunAnalysis'
options.copyInputFiles=False
options.enableKeepFilter=True
options.enableRemoveFilter=False
options.filekey = 'ntuple'
options.PUPath='/data/users/%s/Resonances%i/pileup_full/' % (username, options.year)
# REMINDER: PU histos created with, e.g.:
# python make_pileup_histos.py --condor --skipDone --outputDir /data/users/mseidel/Resonances2017/pileup_full --year 2017

if options.test :
    options.nproc = 1
    options.nFilesPerJob = 1
    options.totalEvents = 50001
    options.nJobs = 1
    options.batch = False
    options.local = True

### ATTENTION! Specify the output directory where the processed ntuple output will be saved.

output_base='/data/users/%s/Resonances%i/' % (username, options.year)
jobtag = '_2022_01_27'
if options.test:
    jobtag += '_test'

version2016 = 'UMDNTuple_0902_2016'
version2017 = 'UMDNTuple_211210_2017'
version2018 = 'UMDNTuple_0902_2018'

version2016data = 'UMDNTuple_0902_2016'
version2017data = 'UMDNTuple_211210_2017'
version2018data = 'UMDNTuple_0902_2018'

jobs2018 = [
        #--------------------------

        JobConf(base,'EGamma',    version=version2018data, year=2018, isData=True),
        JobConf(base,'SingleMuon',version=version2018data, year=2018, isData=True),
        JobConf(base,'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf(base,'GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf(base,'TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf(base,'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8',version=version2018,year=2018, tags=['NLO']),
        ##JobConf(base,'TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2018,year=2018, tags=['NLO']),
        ##JobConf(base,'TTJets_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf(base,'WGToLNuG_PtG-130_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf(base,'WGToLNuG_PtG-500_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf(base,'WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'WWG_TuneCP5_13TeV-amcatnlo-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf(base,'WZG_TuneCP5_13TeV-amcatnlo-pythia8',version=version2018,year=2018, tags=['NLO']),
        ##JobConf(base,'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8',version=version2018,year=2018),
        ##JobConf(base,'WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf(base,'ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf(base, 'DiPhotonJets_MGG-80toInf_TuneCP5_13TeV-amcatnloFXFX-pythia8', tags=['NLO'], year=2018,version=version2018),
        JobConf(base, 'ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8', version=version2018, year=2018),
        JobConf(base, 'ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8', version=version2018, year=2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M200_width0p01'  ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M200_width5'     ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M250_width0p01'  ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M250_width5'     ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M300_width0p01'  ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M300_width5'     ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M350_width0p01'  ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M350_width5'     ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M400_width0p01'  ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M400_width5'     ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M450_width0p01'  ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M450_width5'     ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M500_width0p01'  ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M500_width5'     ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M600_width0p01'  ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M600_width5'     ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M700_width0p01'  ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M700_width5'     ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M800_width0p01'  ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M800_width5'     ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M900_width0p01'  ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M900_width5'     ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M900_width5'     ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1000_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1000_width5'    ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1200_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1200_width5'    ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1400_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1400_width5'    ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1600_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1600_width5'    ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1800_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1800_width5'    ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2000_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2000_width5'    ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2200_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2200_width5'    ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2400_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2400_width5'    ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2600_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2600_width5'    ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2800_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2800_width5'    ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M3000_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M3000_width5'    ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M3500_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M3500_width5'    ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M4000_width0p01' ,year=2018, version = version2018),
        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M4000_width5'    ,year=2018, version = version2018),

        JobConf(baseqcd, 'QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        JobConf(baseqcd, 'QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2018, year=2018),
        ]

jobs2017 = [
        #--------------------------
        JobConf(base, 'WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8',        version=version2017, year=2017),
        JobConf(base, 'WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8', version=version2017, year=2017, tags=['NLO']),
        JobConf(base, 'WGToLNuG_PtG-130_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2017,year=2017, tags=['NLO']),
        JobConf(base, 'WGToLNuG_PtG-500_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2017,year=2017, tags=['NLO']),
        JobConf(base, 'ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8', version=version2017, year=2017 ,tags=['NLO']),
        JobConf(base, 'DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8', version=version2017, tags=['NLO'], year=2017),
        JobConf(base, 'SingleMuon', isData=True, version=version2017, year=2017),
        JobConf(base, 'SingleElectron', isData=True, version=version2017, year=2017),
        JobConf(base, 'SinglePhoton', isData=True, version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2017 , year=2017 ,tags=['NLO']),
        ##JobConf(base, 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017 , year=2017                        ),
        JobConf(base, 'WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        #JobConf(base, 'TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017            ,nfiles=5 ),
        #JobConf(base, 'TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017,nfiles=5     ),
        #JobConf(base, 'TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8' , version=version2017, year=2017  ,nfiles=5  ),
        JobConf(base, 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8', version=version2017, year=2017),
        JobConf(base, 'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8', version=version2017, year=2017),
        JobConf(base, 'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8', version=version2017, year=2017, tags=['NLO'] ),
        JobConf(base, 'GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017 ),
        JobConf(base, 'GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8', version=version2017, year=2017),
        JobConf(base, 'ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8', version=version2017, year=2017),
        JobConf(base,'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8',version=version2017,year=2017),
        JobConf(base, 'WWG_TuneCP5_13TeV-amcatnlo-pythia8', version=version2017, year=2017, tags=['NLO']     ),
        JobConf(base, 'WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8', version=version2017, year=2017, tags=['NLO']     ),
        JobConf(base, 'WZG_TuneCP5_13TeV-amcatnlo-pythia8', version=version2017, year=2017, tags=['NLO']     ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M200_width0p01',  version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M200_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M250_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M250_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M300_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M300_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M350_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M350_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M400_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M400_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M450_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M450_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M500_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M500_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M600_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M600_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M700_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M700_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M800_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M800_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M900_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M900_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1000_width0p01', version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1000_width5',    version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1200_width0p01', version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1200_width5',    version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1400_width0p01', version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1400_width5',    version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1600_width0p01', version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1600_width5',    version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1800_width0p01', version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1800_width5',    version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2000_width0p01', version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2000_width5',    version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2200_width0p01', version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2200_width5',    version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2400_width0p01', version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2400_width5',    version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2600_width0p01', version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2600_width5',    version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2800_width0p01', version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2800_width5',    version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M3000_width0p01', version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M3000_width5',    version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M3500_width0p01', version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M3500_width5',    version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M4000_width0p01', version=version2017, year=2017 ),
        #JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M4000_width5',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8', version=version2017, year=2017),
        JobConf( base, 'QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
        JobConf( base, 'QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8',    version=version2017, year=2017 ),
]


jobs2016 = [
        JobConf(base, 'SingleMuon', isData=True, version=version2016, year=2016),
        JobConf(base, 'SingleElectron', isData=True, version=version2016, year=2016),
        JobConf(base, 'SinglePhoton', isData=True, version=version2016, year=2016),
        #JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016                     ),
        #JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016                         ),
        #JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016                         ),
        JobConf(base, 'WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016, tags=['NLO']                        ),
        JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016, tags=['NLO']                        ),
        JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016, tags=['NLO']                         ),
        JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016, tags=['NLO']      ),
        JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016, tags=['NLO']),
        JobConf(base, 'DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8', version=version2016, year=2016, tags=['NLO']),
        JobConf(base, 'ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1', version=version2016, year=2016),
        JobConf(base, 'ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1', version=version2016, year=2016),
        JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016                         ),
        JobConf(base, 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
        JobConf(base, 'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
        JobConf(base, 'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
        JobConf(base, 'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
        JobConf(base, 'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
        JobConf(base, 'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
        JobConf(base, 'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
        JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016                ),
        JobConf(base, 'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' , version=version2016, year=2016, tags=['NLO']  ),
        JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016, tags=['NLO']     ),
        JobConf(base, 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016               ),
        JobConf(base, 'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016     ),
        JobConf(base, 'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , version=version2016, year=2016    ),
        JobConf(base, 'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8', version=version2016, year=2016, tags=['NLO'] ),
        JobConf(base, 'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8', version=version2016, year=2016, tags=['NLO'] ),
        JobConf(base, 'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8', version=version2016, year=2016, tags=['NLO'] ),
        JobConf(base, 'GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
        JobConf(base, 'GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
        JobConf(base, 'GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
        JobConf(base, 'GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016 ),
        JobConf(base, 'GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
        JobConf(base, 'WWTo2L2Nu_13TeV-powheg', version=version2016, year=2016),
        JobConf(base, 'WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8', version=version2016, year=2016, tags=['NLO']     ),
        JobConf(base, 'WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8', version=version2016, year=2016, tags=['NLO']     ),


        ###### signal stuff ######
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M200_width0p01' , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M200_width5'    , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M250_width0p01' , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M250_width5'    , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M300_width0p01' , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M300_width5'    , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M350_width0p01' , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M350_width5'    , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M400_width0p01' , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M400_width5'    , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M450_width0p01' , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M450_width5'    , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M500_width0p01' , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M500_width5'    , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M600_width0p01' , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M600_width5'    , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M700_width0p01' , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M700_width5'    , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M800_width0p01' , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M800_width5'    , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M900_width0p01' , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M900_width5'    , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1000_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1000_width5'   , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1200_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1200_width5'   , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1400_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1400_width5'   , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1600_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1600_width5'   , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1800_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1800_width5'   , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2000_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2000_width5'   , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2200_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2200_width5'   , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2400_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2400_width5'   , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2600_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2600_width5'   , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2800_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2800_width5'   , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3000_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3000_width5'   , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3500_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3500_width5'   , version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M4000_width0p01', version=version2016 , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M4000_width5'   , version=version2016 , year=2016  ),

        JobConf(baseqcd, 'QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(base,    'QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(base,    'QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(base,    'QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(base,    'QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        JobConf(baseqcd, 'QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version=version2016, year=2016 ),
        ]

if options.year==2016: jobs=jobs2016
if options.year==2017: jobs=jobs2017
if options.year==2018: jobs=jobs2018

if options.test:
    if options.year==2016: jobs=JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016, tags=['NLO'])
    if options.year==2017: jobs=JobConf(base, 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8', version=version2017, year=2017, tags=['NLO'])
    if options.year==2018: jobs=JobConf(base, 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8', version=version2018, year=2018, tags=['NLO'])

args_nlo = { 'ApplyNLOWeight' : 'true' }#, 'doFHPFS' : 'true' }
### ATTENTION! Choose (uncomment and modify as necessary) the type of ntuple you want to make. Single lepton, dilepton, single lepton plus gamma, etc.
configs = [

   {
        'module' : 'Conf%i.py' %options.year,
        'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'phot_vars' : 'True' },
        'args_tag_NLO' : args_nlo,
        'input'  : '',
        'output' : output_base+'LepGamma_mug'+jobtag,
        'tag'    : 'mug%i'%options.year,
        'dataset': 'SingleMuon',
    },

    {
        'module' : 'Conf%i.py' %options.year,
        'args'   : { 'function' : 'make_final_elg', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'eleVeto' : 'None', 'phot_vars' : 'True'},
        'args_tag_NLO' : args_nlo,
        'input'  : '' ,
        'output' : output_base+'LepGamma_elg'+jobtag,
        'tag'    : 'elg%i'%options.year,
        'dataset': ['SingleElectron', 'SinglePhoton'] if options.year!=2018 else 'EGamma',
    },
#   {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'phot_vars' : 'True' , 'phot_id': 'almostmedium'},
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'LepGamma_mug_AlmostMediumPhoton'+jobtag,
#        'tag'    : 'mug%i'%options.year,
#        'dataset': 'SingleMuon',
#    },
#
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_elg', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'eleVeto' : 'None', 'phot_vars' : 'True', 'phot_id': 'almostmedium'},
#        'args_tag_NLO' : args_nlo,
#        'input'  : '' ,
#        'output' : output_base+'LepGamma_elg_AlmostMediumPhoton'+jobtag,
#        'tag'    : 'elg%i'%options.year,
#        'dataset': 'SingleElectron' if options.year!=2018 else 'EGamma',
#    },
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_mumu', 'mu_pt' : ' > 30 ' },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'LepLep_mumu'+jobtag,
#        'tag'    : 'mumu%i' %options.year ,
#     #    'keepSelection': 'tight',
#        'dataset': 'SingleMuon',
#    },
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_elel', 'el_pt' : ' > 35 ' },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'LepLep_elel'+jobtag,
#        'tag'    : 'elel%i' %options.year,
#     #    'keepSelection': 'tight',
#        'dataset': 'SingleElectron' if options.year!=2018 else 'EGamma',
#    },
#    { ## NOTE for jet fake
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 30 ' , "ph_id": "None" },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'LepLep_mug_NoPhID'+jobtag,
#        'tag'    : 'mug%i' %options.year ,
#        #'keepSelection': 'tight',
#        'dataset': 'SingleMuon',
#    },
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_mumu', 'mu_pt' : ' > 30 ' , "ph_id": "None" },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'LepLep_mumu_NoPhID'+jobtag,
#        'tag'    : 'mumu%i' %options.year ,
#        #'keepSelection': 'tight',
#        'dataset': 'SingleMuon',
#    },
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_mu', 'mu_pt' : ' > 30 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'phot_vars' : 'False' },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'SingleLep_mu'+jobtag,
#        'tag'    : 'mu%i'%options.year,
#        'dataset': 'SingleMuon',
#    },
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_el', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 35 ' , 'ph_pt' : ' > 10 ', 'eleVeto' : 'None', 'phot_vars' : 'False'},
#        'args_tag_NLO' : args_nlo,
#        'input'  : '' ,
#        'output' : output_base+'SingleLep_el'+jobtag,
#        'tag'    : 'el%i'%options.year,
#        'dataset': 'SingleElectron',
#    },
    #{
    #    'module' : 'Conf%i.py' %options.year,
    #    'args'   : { 'function' : 'make_final_mu', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'phot_vars' : 'False', 'invertIso' : True },
    #    'args_tag_NLO' : args_nlo,
    #    'input'  : '',
    #    'output' : output_base+'SingleLepInvIso_mu'+jobtag,
    #    'tag'    : 'mu%i'%options.year,
    #    'dataset': 'SingleMuon',
    #},
    #{
    #    'module' : 'Conf%i.py' %options.year,
    #    'args'   : { 'function' : 'make_final_el', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'eleVeto' : 'None', 'phot_vars' : 'False', 'invertIso' : True },
    #    'args_tag_NLO' : args_nlo,
    #    'input'  : '' ,
    #    'output' : output_base+'SingleLepInvIso_el'+jobtag,
    #    'tag'    : 'el%i'%options.year,
    #    'dataset': 'SingleElectron',
    #},
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_mu', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'phot_vars' : 'False', 'cut_pfiso_tight': ' > 0.15 ' },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'SingleLepNoIso_mu'+jobtag,
#        'tag'    : 'munoiso%i'%options.year,
#        'dataset': 'SingleMuon',
#    },
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_el', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'eleVeto' : 'None', 'phot_vars' : 'False', 'cut_pfiso_tight': ' > 0.15 ' },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '' ,
#        'output' : output_base+'SingleLepNoIso_el'+jobtag,
#        'tag'    : 'elnoiso%i'%options.year,
#        'dataset': 'SingleElectron',
#    },
    #{
    #    'module' : 'Conf%i.py' %options.year,
    #    'args'   : { 'function' : 'make_final_muel', 'el_pt' : ' > 30 ' },
    #    'args_tag_NLO' : args_nlo,
    #    'input'  : '',
    #    'output' : output_base+'LepLep_muel_2018_03_28',
    #    'tag'    : 'muel%i'%options.year,
    #    'keepSelection': 'tight',
    #    'dataset': 'SingleMuon',
    #},
    #{
    #    'module' : 'Conf%i.py' %options.year,
    #    'args'   : { 'function' : 'make_final_elg', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'eleVeto' : 'None', 'phot_vars' : 'True', 'eleOlap' : 'False'},
    #    'args_tag_NLO' : args_nlo,
    #    'input'  : '' ,
    #    'output' : output_base+'LepGammaNoEleOlapMod_elg_2018_06_11',
    #    'tag'    : 'elgnov%i'%options.year,
    #    'dataset': 'SingleElectron',
    #},
   # {
   #     'module' : 'Conf%i.py' %options.year,
   #     'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'phot_vars' : 'true', 'phot_id' : 'None'},#, 'unblind' : 'True' },
   #     'args_tag_NLO' : args_nlo,
   #     'input'  : '',
   #     'output' : output_base+'LepGammaNoPhId_mug'+jobtag,
   #     'dataset': 'SingleMuon',
   #     'tag'    : 'muglph%i'%options.year,
   # },
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_elg', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'phot_vars' : 'True', 'phot_id' : 'None',},# 'unblind' : 'True' },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'LepGammaNoPhId_elg'+jobtag,
#        'dataset': 'SingleElectron',
#        'tag'    : 'elglph%i'%options.year,
#    },




### old configs
    #{
    #    'module' : 'Conf%i.py' %options.year,
    #    'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 30 ', 'muphtrig' : 'True' },
    #    'args_tag_NLO' : args_nlo,
    #    'input'  : input_base,
    #    'output' : base+'LepGamma_mug_ditrig_2017_03_06',
    #    'tag'    : 'mugditrig',
    #},
    #{
    #    'module' : 'Conf%i.py' %options.year,
    #    'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'phot_vars' : 'True', 'phot_id' : 'loose', 'sec_lep_veto' : 'False' },
    #    'input'  : input_base,
    #    'output' : base+'LepGamma_mug_noseclepveto_2017_03_14',
    #    'tag'    : 'mugnslv',
    #},
    #{
    #    'module' : 'Conf%i.py' %options.year,
    #    'args'   : { 'function' : 'make_final_elg', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'phot_vars' : 'True', 'phot_id' : 'loose', 'sec_lep_veto' : 'False' },
    #    'input'  : input_base,
    #    'output' : base+'LepGamma_elg_noseclepveto_2017_03_14',
    #    'tag'    : 'elgnslv',
    #},
    #{
    #    'module' : 'Conf%i.py' %options.year,
    #    'args'   : { 'function' : 'make_nofilt' , 'pass_lepton' : 'True'},
    #    'input'  : '',
    #    'output' : output_base+'nofilt'+jobtag,
    #    'tag'    : 'nofilt',
    #    'args_tag_NLO' : args_nlo,
    #},
    ##{
    ##    'module' : 'Conf%i.py' %options.year,
    ##    'args'   : { 'function' : 'make_final_elgjj', 'el_pt' : ' > 30 ' },
    ##    'input'  : input_base_new,
    ##    'output' : base+'LepGammaDiJet_elgjj_2017_01_03',
    ##    'tag'    : 'elgjj',
    ##},
    ##{
    ##    'module' : 'Conf%i.py' %options.year,
    ##    'args'   : { 'function' : 'make_final_mugjj', 'mu_pt' : ' > 30 ' },
    ##    'input'  : input_base_new,
    ##    'output' : base+'LepGammaDiJet_mugjj_2017_01_03',
    ##    'tag'    : 'mugjj',
    ##},

]


scheduler_base.RunJobs( jobs, configs, options)

