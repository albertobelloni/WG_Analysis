#!/usr/bin/env python
import os
from argparse import ArgumentParser

import scheduler_base
from scheduler_base import JobConf

p = ArgumentParser()
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--clean', dest='clean', default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local', dest='local', default=False, action='store_true', help='Run locally' )
p.add_argument( '--test', dest='test', default=False, action='store_true', help='Run a test job' )
p.add_argument( '--year', dest='year', default=None, type=int, help='run year' )
options = p.parse_args()

if not options.check :
    options.run = True
else :
    options.run = False

options.batch = ( not options.local )

### ATTENTION! Here you specify the directory containing the raw ntuples that you want to process further.
### Also specify the version number of the raw ntuples with the version_* variables below.
#base = '/store/user/jkunkle'
#base = '/store/user/yofeng/WGamma'
base = '/store/user/kawong/WGamma2'
baseqcd = '/store/user/mseidel/WGamma'
#base = 'root://eoscms.cern.ch:1094///store/group/phys_exotica/Wgamma'
#base = '/eos/cms/store/group/phys_exotica/Wgamma'
options.nFilesPerJob = 10

options.nproc = 1
options.treename='UMDNTuple/EventTree'
options.exename='RunAnalysis'
options.copyInputFiles=False
options.enableKeepFilter=True
options.enableRemoveFilter=False
options.filekey = 'ntuple'
if options.year == None: options.year = 2016
#options.PUPath='/data/users/jkunkle/Resonances/PileupHistograms'
#options.PUPath='/data/users/friccita/WGammaNtuple/Pileup'
#options.PUPath='/data/users/kakw/Resonances2017/pileuptest/' ## testonly
#options.PUPath='/data/users/kakw/Resonances2017/pileup3'
#if options.year==2018: options.PUPath='/afs/cern.ch/work/k/kawong/Resonances2018/pileup'
options.PUPath='/data2/users/kakw/Resonances%i/pileup/' %options.year
if options.year == 2016:
    options.PUPath='/data/users/mseidel/Resonances%i/pileup/' %options.year
#options.PUPath='/afs/cern.ch/work/k/kawong/Resonances%i/pileup' %options.year
#options.usexrd = True

if options.test :
    options.nproc = 1
    options.nFilesPerJob = 1
    options.totalEvents = 50001
    options.nJobs = 1
    options.batch = False
    options.local = True

### ATTENTION! Specify the output directory where the processed ntuple output will be saved.

output_base = '/data2/users/kakw/Resonances%i/' %options.year
#output_base = '/afs/cern.ch/work/k/kawong/Resonances%i/' %options.year
jobtag = '_2020_01_30'

#version = 'UMDNTuple_0620'
version2016sig = 'UMDNTuple_0915_2016' # 2016 signal
version = 'UMDNTuple_0503'
version2016 = 'UMDNTuple_0506_2016'
version2017 = 'UMDNTuple_0506_2017'
version2018 = 'UMDNTuple_0506_2018'
version2018signal = 'UMDNTuple_0915_2018'
#version_py = 'UMDNTuple_20190329testc'
#version_data = 'UMDNTuple_0506'
#version_madgraph = 'UMDNTuple_20190329test'
#version_g = 'UMDNTuple_20190329testg'
#version_reminiAOD=''

jobs2018 = [
        #--------------------------

        JobConf(base,'EGamma',version=version2018,year=2018, isData=True),
        JobConf(base,'SingleMuon',version=version2018,year=2018, isData=True),
        JobConf(base,'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',version="UMDNTuple_0911",year=2018, tags=['NLO']),
        JobConf(base,'GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf(base,'TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf(base,'TTJets_TuneCP5_13TeV-madgraphMLM-pythia8',version=version2018,year=2018),
        JobConf(base,'WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2018,year=2018, tags=['NLO']),
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
        JobConf(base,'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8',version=version2018,year=2018),
        JobConf(base,'WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf(base,'ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2018,year=2018, tags=['NLO']),
        JobConf( base, 'DiPhotonJets_MGG-80toInf_TuneCP5_13TeV-amcatnloFXFX-pythia8', tags=['NLO'], year=2018,version="UMDNTuple_0909"),
        JobConf( base, 'ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8', version="UMDNTuple_2018_1003", year=2018),
        JobConf( base, 'ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8', version="UMDNTuple_2018_1003", year=2018),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1000_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1000_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1200_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1200_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1400_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1400_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1600_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1600_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1800_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M1800_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2000_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2000_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M200_width0p01'  ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M200_width5'     ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2200_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2200_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2400_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2400_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M250_width0p01'  ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M250_width5'     ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2600_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2600_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2800_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M2800_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M3000_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M3000_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M300_width0p01'  ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M300_width5'     ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M3500_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M3500_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M350_width0p01'  ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M350_width5'     ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M4000_width0p01' ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M4000_width5'    ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M400_width0p01'  ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M400_width5'     ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M450_width5'     ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M500_width0p01'  ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M500_width5'     ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M600_width0p01'  ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M600_width5'     ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M700_width0p01'  ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M700_width5'     ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M800_width0p01'  ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M800_width5'     ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M900_width0p01'  ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M900_width5'     ,year=2018, version = version2018signal),
#        JobConf(base,'MadGraphChargedResonance_WGToLNuG_M900_width5'     ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1000_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1000_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1000_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1200_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1200_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1400_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1400_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1600_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1600_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1800_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1800_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2000_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2000_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M200_width0p01'    ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M200_width5'       ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2200_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2200_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2400_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2400_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M250_width0p01'    ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M250_width5'       ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2600_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2600_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2800_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2800_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M3000_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M300_width0p01'    ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M300_width5'       ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M3500_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M3500_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M350_width0p01'    ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M350_width5'       ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M4000_width0p01'   ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M4000_width5'      ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M400_width0p01'    ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M400_width5'       ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M450_width0p01'    ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M450_width5'       ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M500_width0p01'    ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M500_width5'       ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M600_width0p01'    ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M600_width5'       ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M700_width0p01'    ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M700_width5'       ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M800_width0p01'    ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M800_width5'       ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M900_width0p01'    ,year=2018, version = version2018signal),
#        JobConf(base,'PythiaChargedResonance_WGToLNuG_M900_width5'       ,year=2018, version = version2018signal),
        ]

jobs2017 = [
        #--------------------------
        JobConf(base, 'WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8', version=version2017, year=2017, tags=['NLO']                        ),
        JobConf( base, 'ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8', version=version2017, year=2017 ,tags=['NLO']),
        JobConf( base, 'DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8', version=version2017, tags=['NLO'], year=2017),
        JobConf(base, 'SingleMuon', isData=True, version=version2017, year=2017),
        JobConf(base, 'SingleElectron', isData=True, version=version2017, year=2017),

        JobConf(base, 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017                         ),
       JobConf( base, 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',version=version2017 , year=2017 ,tags=['NLO']),
        JobConf(base, 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017 , year=2017                        ),
        JobConf(base, 'WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf(base, 'TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017            ,nfiles=5 ),
        JobConf(base, 'TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017,nfiles=5     ),
        JobConf(base, 'TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8' , version=version2017, year=2017  ,nfiles=5  ),
        JobConf(base, 'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8', version=version2017, year=2017, tags=['NLO'] ),
        JobConf( base, 'GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf( base, 'GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf( base, 'GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf( base, 'GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017 ),
        JobConf( base, 'GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8', version=version2017, year=2017),
        JobConf( base, 'ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8', version="UMDNTuple_2017_1003", year=2017),
        JobConf( base, 'ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8', version="UMDNTuple_2017_1003", year=2017),
#        #JobConf( base, 'WTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8', version=version2017, year=2017),
#        #JobConf(base, 'WWG_TuneCP5_13TeV-amcatnlo-pythia8', version=version2017, year=2017, tags=['NLO']     ),
#        #JobConf(base, 'WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8', version=version2017, year=2017, tags=['NLO']     ),
#        #JobConf(base, 'WZG_TuneCP5_13TeV-amcatnlo-pythia8', version=version2017, year=2017, tags=['NLO']     ),
#
##        JobConf( base, 'WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8',        version=version2017, year=2017),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M900_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M900_width0p01',  version=version2017, year=2017),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M800_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M800_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M700_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M500_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M450_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M400_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M4000_width5',    version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M350_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M3500_width5',    version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M300_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2800_width0p01', version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2600_width0p01', version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M250_width5',     version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2200_width5',    version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2200_width0p01', version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M200_width0p01',  version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2000_width5',    version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M2000_width0p01', version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1800_width5',    version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1400_width5',    version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1400_width0p01', version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1200_width0p01', version=version2017, year=2017 ),
        JobConf( base, 'MadGraphChargedResonance_WGToLNuG_M1000_width0p01', version=version2017, year=2017 ),


        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1000_width5'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1200_width5'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1400_width0p01'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1800_width0p01'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M1800_width5'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2000_width0p01'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M200_width0p01'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2200_width5'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2400_width0p01'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M250_width0p01'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M2600_width0p01'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M300_width0p01'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M300_width5'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M3500_width0p01'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M3500_width5'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M350_width0p01'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M4000_width5'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M450_width0p01'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M450_width5'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M500_width0p01'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M500_width5'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M600_width5'  , version=version2017, year=2017 ),
        JobConf(base,'PythiaChargedResonance_WGToLNuG_M800_width0p01'  , version=version2017, year=2017 ),


]

jobs2016 = [
#        JobConf(base, 'SingleMuon', isData=True, version=version2016, year=2016),
#        JobConf(base, 'SingleElectron', isData=True, version=version2016, year=2016),
#        JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016                     ),
#        JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016                         ),
#        JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016                         ),
#        JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016, tags=['NLO']                        ),
#        JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016, tags=['NLO']                         ),
#        JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version="UMDNTuple_0814_2016", year=2016, tags=['NLO']      ),
#        JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016, tags=['NLO'], nfiles = options.nFilesPerJob*2),
#        JobConf(base, 'DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8', version=version2016, year=2016, tags=['NLO']),
#        JobConf(base, 'ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1', version="UMDNTuple_2016_1003", year=2016),
#        JobConf(base, 'ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1', version="UMDNTuple_2016_1003", year=2016),
#        JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016                         ),
#        JobConf(base, 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
#        JobConf(base, 'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
#        JobConf(base, 'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
#        JobConf(base, 'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
#        JobConf(base, 'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
#        JobConf(base, 'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
#        JobConf(base, 'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
#        JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016                ),
#        JobConf(base, 'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' , version=version2016, year=2016, tags=['NLO']   , nfiles = options.nFilesPerJob/3    ),
#        JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016, tags=['NLO']     ),
#        JobConf(base, 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016            ,nfiles=5    ),
#        JobConf(base, 'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016,nfiles=5     ),
#        JobConf(base, 'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , version=version2016, year=2016  ,nfiles=5  ),
#        JobConf(base, 'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8', version=version2016, year=2016, tags=['NLO'] ),
#        JobConf( base, 'GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
#        JobConf( base, 'GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
#        JobConf( base, 'GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
#        JobConf( base, 'GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016 ),
#        JobConf( base, 'GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version2016, year=2016),
        #JobConf( base, 'WWTo2L2Nu_13TeV-powheg', version=version2016, year=2016),
        #JobConf(base, 'WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8', version=version2016, year=2016, tags=['NLO']     ),
        #JobConf(base, 'WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8', version=version2016, year=2016, tags=['NLO']     ),

        JobConf( base, 'WJetsToLNu_Wpt-0To50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016),
        JobConf( base, 'WJetsToLNu_Wpt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016),
        JobConf( base, 'WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016),
        JobConf( base, 'WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016),
        JobConf( base, 'WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016),
        JobConf( base, 'WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016),
        JobConf( base, 'WToLNu_0J_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016),
        JobConf( base, 'WToLNu_1J_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016),
        JobConf( base, 'WToLNu_2J_13TeV-amcatnloFXFX-pythia8', version=version2016, year=2016),
        JobConf( baseqcd, 'WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version='UMDNTuple_1129_2016', year=2016 ),

        JobConf( baseqcd, 'QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),
        JobConf( baseqcd, 'QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8', version='UMDNTuple_1129_2016', year=2016 ),


        ###### signal stuff ######
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1000_width5'   , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1200_width5'   , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1400_width5'   , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1600_width5'   , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1800_width5'   , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2000_width5'   , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M200_width5'    , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2200_width5'   , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2400_width5'   , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M250_width5'    , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2800_width5'   , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M300_width5'    , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3500_width5'   , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M350_width5'    , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M4000_width5'   , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M400_width5'    , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M450_width5'    , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M500_width5'    , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M600_width5'    , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M700_width5'    , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M800_width5'    , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M900_width5'    , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1000_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1200_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1400_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1600_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1800_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2000_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M200_width0p01' , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2200_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2400_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M250_width0p01' , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2600_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2800_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3000_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M300_width0p01' , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3500_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M350_width0p01' , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M4000_width0p01', version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M400_width0p01' , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M450_width0p01' , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M500_width0p01' , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M600_width0p01' , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M700_width0p01' , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M800_width0p01' , version=version2016sig , year=2016  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M900_width0p01' , version=version2016sig , year=2016  ),


        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1000_width5' , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1200_width5' , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1400_width5' , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1600_width5' , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1800_width5' , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2000_width5' , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M200_width5'  , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2200_width5' , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2400_width5' , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M250_width5'  , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2800_width5' , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M300_width5'  , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M3500_width5' , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M350_width5'  , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M4000_width5' , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M400_width5'  , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M450_width5'  , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M500_width5'  , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M600_width5'  , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M700_width5'  , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M800_width5'  , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M900_width5'  , version=version_py   ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1000_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1200_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1400_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1600_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1800_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2000_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M200_width0p01' , version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2200_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2400_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M250_width0p01' , version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2600_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2800_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M3000_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M300_width0p01' , version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M3500_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M350_width0p01' , version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M4000_width0p01', version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M400_width0p01' , version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M450_width0p01' , version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M500_width0p01' , version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M600_width0p01' , version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M700_width0p01' , version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M800_width0p01' , version=version_py ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M900_width0p01' , version=version_py ),
        ]

if options.year==2016: jobs=jobs2016
if options.year==2017: jobs=jobs2017
if options.year==2018: jobs=jobs2018


args_nlo = { 'ApplyNLOWeight' : 'true' }#, 'doFHPFS' : 'true' }
### ATTENTION! Choose (uncomment and modify as necessary) the type of ntuple you want to make. Single lepton, dilepton, single lepton plus gamma, etc.
configs = [

#   {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'phot_vars' : 'True' },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'LepGamma_mug'+jobtag,
#        'tag'    : 'mug',
#        'dataset': 'SingleMuon',
#    },
#
    {
        'module' : 'Conf%i.py' %options.year,
        'args'   : { 'function' : 'make_final_elg', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'eleVeto' : 'None', 'phot_vars' : 'True'},
        'args_tag_NLO' : args_nlo,
        'input'  : '' ,
        'output' : output_base+'LepGamma_elg'+jobtag,
        'tag'    : 'elg',
        'dataset': 'SingleElectron' if options.year!=2018 else 'EGamma',
    },
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_mumu', 'mu_pt' : ' > 30 ' },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'LepLep_mumu'+jobtag,
#        'tag'    : 'mumu',
#        'keepSelection': 'tight',
#        'dataset': 'SingleMuon',
#    },
    {
        'module' : 'Conf%i.py' %options.year,
        'args'   : { 'function' : 'make_final_elel', 'el_pt' : ' > 30 ' },
        'args_tag_NLO' : args_nlo,
        'input'  : '',
        'output' : output_base+'LepLep_elel'+jobtag,
        'tag'    : 'elel',
        'keepSelection': 'tight',
        'dataset': 'SingleElectron' if options.year!=2018 else 'EGamma',
    },
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_mu', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'phot_vars' : 'False' },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'SingleLep_mu'+jobtag,
#        'tag'    : 'mu',
#        'dataset': 'SingleMuon',
#    },
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_el', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'eleVeto' : 'None', 'phot_vars' : 'False'},
#        'args_tag_NLO' : args_nlo,
#        'input'  : '' ,
#        'output' : output_base+'SingleLep_el'+jobtag,
#        'tag'    : 'el',
#        'dataset': 'SingleElectron',
#    },
    #{
    #    'module' : 'Conf%i.py' %options.year,
    #    'args'   : { 'function' : 'make_final_mu', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'phot_vars' : 'False', 'invertIso' : True },
    #    'args_tag_NLO' : args_nlo,
    #    'input'  : '',
    #    'output' : output_base+'SingleLepInvIso_mu'+jobtag,
    #    'tag'    : 'mu',
    #    'dataset': 'SingleMuon',
    #},
    #{
    #    'module' : 'Conf%i.py' %options.year,
    #    'args'   : { 'function' : 'make_final_el', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'eleVeto' : 'None', 'phot_vars' : 'False', 'invertIso' : True },
    #    'args_tag_NLO' : args_nlo,
    #    'input'  : '' ,
    #    'output' : output_base+'SingleLepInvIso_el'+jobtag,
    #    'tag'    : 'el',
    #    'dataset': 'SingleElectron',
    #},
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_mu', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'phot_vars' : 'False', 'cut_pfiso_tight': ' > 0.15 ' },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'SingleLepNoIso_mu'+jobtag,
#        'tag'    : 'munoiso',
#        'dataset': 'SingleMuon',
#    },
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_el', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'eleVeto' : 'None', 'phot_vars' : 'False', 'cut_pfiso_tight': ' > 0.15 ' },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '' ,
#        'output' : output_base+'SingleLepNoIso_el'+jobtag,
#        'tag'    : 'elnoiso',
#        'dataset': 'SingleElectron',
#    },
    #{
    #    'module' : 'Conf%i.py' %options.year,
    #    'args'   : { 'function' : 'make_final_muel', 'el_pt' : ' > 30 ' },
    #    'args_tag_NLO' : args_nlo,
    #    'input'  : '',
    #    'output' : output_base+'LepLep_muel_2018_03_28',
    #    'tag'    : 'muel',
    #    'keepSelection': 'tight',
    #    'dataset': 'SingleMuon',
    #},
    #{
    #    'module' : 'Conf%i.py' %options.year,
    #    'args'   : { 'function' : 'make_final_elg', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'eleVeto' : 'None', 'phot_vars' : 'True', 'eleOlap' : 'False'},
    #    'args_tag_NLO' : args_nlo,
    #    'input'  : '' ,
    #    'output' : output_base+'LepGammaNoEleOlapMod_elg_2018_06_11',
    #    'tag'    : 'elgnov',
    #    'dataset': 'SingleElectron',
    #},
   # {
   #     'module' : 'Conf%i.py' %options.year,
   #     'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'phot_vars' : 'true', 'phot_id' : 'None'},#, 'unblind' : 'True' },
   #     'args_tag_NLO' : args_nlo,
   #     'input'  : '',
   #     'output' : output_base+'LepGammaNoPhId_mug'+jobtag,
   #     'dataset': 'SingleMuon',
   #     'tag'    : 'muglph',
   # },
#    {
#        'module' : 'Conf%i.py' %options.year,
#        'args'   : { 'function' : 'make_final_elg', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 10 ', 'phot_vars' : 'True', 'phot_id' : 'None',},# 'unblind' : 'True' },
#        'args_tag_NLO' : args_nlo,
#        'input'  : '',
#        'output' : output_base+'LepGammaNoPhId_elg'+jobtag,
#        'dataset': 'SingleElectron',
#        'tag'    : 'elglph',
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
    #    'args'   : { 'function' : 'make_nofilt' , 'pass_lepton' : 'true'},
    #    'input'  : '',
    #    'output' : output_base+'SigNoFilt_2018_07_03',
    #    'tag'    : 'nofilt',
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

