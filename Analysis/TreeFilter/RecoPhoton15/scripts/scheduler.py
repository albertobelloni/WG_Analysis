import os
from argparse import ArgumentParser

import scheduler_base
from scheduler_base import JobConf

p = ArgumentParser()
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local', dest='local', default=False, action='store_true', help='Run locally' )
p.add_argument( '--test', dest='test', default=False, action='store_true', help='Run a local test job' )
options = p.parse_args()

if not options.check :
    options.run = True
else :
    options.run = False

options.batch = ( not options.local )


#base = '/data/users/jkunkle/Baobabs/'
base = '/store/user/jkunkle/'
#base_signal = '/data/users/jkunkle/Samples/SignalMoriond/'
version = 'Resonances_v10'
version11 = 'Resonances_v11'

jobs = [
        #JobConf(base, 'SingleMuon', version=version, isData=True ),
        #JobConf(base, 'SingleElectron', version=version11, isData=True),
        ###JobConf(base, 'SinglePhoton', version=version, isData=True),
        #JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        #JobConf(base, 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        #JobConf(base, 'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),  
        #JobConf(base, 'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),  
        #JobConf(base, 'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),  
        #JobConf(base, 'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version), 
        #JobConf(base, 'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        #JobConf(base, 'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version), 
        #JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version), 
        #JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version), 
        #JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version), 
        #JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        #JobConf(base, 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        #JobConf(base, 'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        #JobConf(base, 'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        #JobConf( base, 'GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        #JobConf( base, 'GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        #JobConf( base, 'GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        #JobConf( base, 'GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),
        #JobConf( base, 'GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', version=version),

        #JobConf( base, 'WWTo2L2Nu_13TeV-powheg', version=version),

        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1000_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1000_width5'   , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1200_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1200_width5'   , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1400_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1400_width5'   , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1600_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1600_width5'   , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1800_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1800_width5'   , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2000_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2000_width5'   , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M200_width0p01' , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M200_width5'    , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2200_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2200_width5'   , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2400_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2400_width5'   , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M250_width0p01' , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M250_width5'    , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2600_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2800_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2800_width5'   , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3000_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M300_width0p01' , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M300_width5'    , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3500_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3500_width5'   , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M350_width0p01' , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M350_width5'    , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M4000_width0p01', version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M4000_width5'   , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M400_width0p01' , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M400_width5'    , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M450_width0p01' , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M450_width5'    , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M500_width0p01' , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M500_width5'    , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M600_width0p01' , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M600_width5'    , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M700_width0p01' , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M700_width5'    , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M800_width0p01' , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M800_width5'    , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M900_width0p01' , version=version ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M900_width5'    , version=version ),

        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1000_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1000_width5'   , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1200_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1200_width5'   , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1400_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1400_width5'   , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1600_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1600_width5'   , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1800_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M1800_width5'   , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2000_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2000_width5'   , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M200_width0p01' , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M200_width5'    , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2200_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2200_width5'   , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2400_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2400_width5'   , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M250_width0p01' , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M250_width5'    , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2600_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2800_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M2800_width5'   , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M3000_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M300_width0p01' , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M300_width5'    , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M3500_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M3500_width5'   , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M350_width0p01' , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M350_width5'    , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M4000_width0p01', version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M4000_width5'   , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M400_width0p01' , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M400_width5'    , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M450_width0p01' , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M450_width5'    , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M500_width0p01' , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M500_width5'    , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M600_width0p01' , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M600_width5'    , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M700_width0p01' , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M700_width5'    , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M800_width0p01' , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M800_width5'    , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M900_width0p01' , version=version ),
        #JobConf(base,'PythiaChargedResonance_WGToLNu_M900_width5'    , version=version ),



]

jobs_nlo = [
        #JobConf(base, 'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version),
        #JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version),
        #JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'        , version=version),
        #JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', version=version), 
        #JobConf(base, 'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8'        , version=version),
        #JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' , version=version),
        #JobConf(base, 'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         , version=version),
        #JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'      , version=version),
        #JobConf(base, 'WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                 , version=version),
        #JobConf(base, 'WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                 , version=version),
        #JobConf( base, 'DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8', version=version),
]

options.filekey = 'ntuple'
options.nFilesPerJob = 1
options.nproc = 6
options.treename='tupel/EventTree'
options.exename='RunAnalysis'
options.copyInputFiles=False
options.enableKeepFilter=True
options.enableRemoveFilter=True
options.PUPath='/data/users/jkunkle/Resonances/PileupHistograms/'

module = 'ConfPhotonReco.py'
#module = 'ConfTruthPhotonReco.py'

out_base = '/data/users/jkunkle/Resonances/'
configs = [ 
    {
        'module' : module,
        'args'   : { },
        'input'  : '',
        'output' : out_base+'RecoOutput_2017_06_29',
        'tag'    : 'reco',
    },
]

configs_nlo = [
    {
        'module' : module,
        'args'   : { 'ApplyNLOWeight' : 'true', 'doFHPFS' : 'true'  },
        'input'  : '',
        'output' : out_base+'RecoOutput_2017_06_29',
        'tag'    : 'nloreco',
    },
]

scheduler_base.RunJobs( jobs, configs, options)
scheduler_base.RunJobs( jobs_nlo, configs_nlo, options)

