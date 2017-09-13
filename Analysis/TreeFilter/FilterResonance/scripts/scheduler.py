import os
from argparse import ArgumentParser

import scheduler_base
from scheduler_base import JobConf

p = ArgumentParser()
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--clean', dest='clean', default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--batch', dest='batch', default=False, action='store_true', help='Run on batch' )
p.add_argument( '--test', dest='test', default=False, action='store_true', help='Run a test job' )
options = p.parse_args()

if not options.check :
    options.run = True
else :
    options.run = False

options.local = ( not options.batch )

base = '/data/users/jkunkle/Resonances/'
#base = '/afs/cern.ch/user/a/abelloni/work/analysis/WG_EXO/usercode/test/'

jobs = [
        ##JobConf(base, 'DoubleMuon'),
        ##JobConf(base, 'DoubleEG'),
        ##JobConf(base, 'SinglePhoton'),
        ##JobConf(base, 'JetHT'),
        #JobConf(base, 'SingleMuon', isData=True),
        #JobConf(base, 'SingleElectron', isData=True),
        #JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        #JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        #JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        #JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                         ),
        #JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                         ),
        #JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                         ),
        #JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        #JobConf(base, 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'),
        #JobConf(base, 'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'),  
        #JobConf(base, 'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'),  
        #JobConf(base, 'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'),  
        #JobConf(base, 'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'), 
        #JobConf(base, 'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'),
        #JobConf(base, 'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'), 
        #JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                         ),
        #JobConf(base, 'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'        ),
        #JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'     ),
        #JobConf(base, 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'     ),
        #JobConf(base, 'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'     ),
        #JobConf(base, 'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'     ),
        #JobConf(base, 'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8' ),
        #JobConf( base, 'GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'),
        #JobConf( base, 'GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'),
        #JobConf( base, 'GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'),
        #JobConf( base, 'GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' ),
        #JobConf( base, 'GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'),
        #JobConf( base, 'DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8'),

        ###JobConf( base, 'WWTo2L2Nu_13TeV-powheg'),
        ###JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'),
        ###JobConf(base, 'WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8'     ),
        ###JobConf(base, 'WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8'     ),

        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1000_width5'    ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1200_width5'    ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1400_width5'    ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1600_width5'    ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1800_width5'    ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2000_width5'    ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M200_width5'     ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2200_width5'    ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2400_width5'    ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M250_width5'     ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2800_width5'    ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M300_width5'     ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3500_width5'    ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M350_width5'     ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M4000_width5'    ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M400_width5'     ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M450_width5'     ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M500_width5'     ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M600_width5'     ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M700_width5'     ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M800_width5'     ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M900_width5'     ),

        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1000_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1200_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1400_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1600_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M1800_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2000_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M200_width0p01'  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2200_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2400_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M250_width0p01'  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2600_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2800_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3000_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M300_width0p01'  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M3500_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M350_width0p01'  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M4000_width0p01' ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M400_width0p01'  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M450_width0p01'  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M500_width0p01'  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M600_width0p01'  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M700_width0p01'  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M800_width0p01'  ),
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M900_width0p01'  ),

        JobConf(base,'PythiaChargedResonance_WGToLNu_M1000_width5'    ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M1200_width5'    ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M1400_width5'    ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M1600_width5'    ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M1800_width5'    ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M2000_width5'    ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M200_width5'     ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M2200_width5'    ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M2400_width5'    ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M250_width5'     ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M2800_width5'    ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M300_width5'     ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M3500_width5'    ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M350_width5'     ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M4000_width5'    ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M400_width5'     ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M450_width5'     ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M500_width5'     ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M600_width5'     ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M700_width5'     ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M800_width5'     ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M900_width5'     ),

        JobConf(base,'PythiaChargedResonance_WGToLNu_M1000_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M1200_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M1400_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M1600_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M1800_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M2000_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M200_width0p01'  ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M2200_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M2400_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M250_width0p01'  ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M2600_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M2800_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M3000_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M300_width0p01'  ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M3500_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M350_width0p01'  ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M4000_width0p01' ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M400_width0p01'  ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M450_width0p01'  ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M500_width0p01'  ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M600_width0p01'  ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M700_width0p01'  ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M800_width0p01'  ),
        JobConf(base,'PythiaChargedResonance_WGToLNu_M900_width0p01'  ),

]


options.nFilesPerJob = 1

options.nproc = 4
options.treename='tupel/EventTree'
options.exename='RunAnalysis'
options.copyInputFiles=True
options.enableKeepFilter=True
options.enableRemoveFilter=True


#input_base = 'RecoOutput_2017_04_12'
input_base = 'RecoOutput_2017_06_29'
#input_base_sig = 'RecoOutputSig_2017_01_26'

configs = [

    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_el', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'ph_id_cut' : 'None' },
    #    'input'  : input_base,
    #    'output' : base+'SingleLepNoPhID_el_2017_07_18',
    #    'dataset': 'SingleElectron',
    #    'tag'    : 'el',
    #},
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_mu', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'ph_id_cut' : 'None'  },
    #    'input'  : input_base,
    #    'output' : base+'SingleLepNoPhID_mu_2017_07_18',
    #    'dataset': 'SingleMuon',
    #    'tag'    : 'mu',
    #},
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_mumu', 'mu_pt' : ' > 30 ' },
    #    'input'  : input_base,
    #    'output' : base+'LepLep_mumu_2017_04_12',
    #    'tag'    : 'mumu',
    #    'dataset': 'SingleMuon',
    #},
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_muel', 'el_pt' : ' > 30 ' },
    #    'input'  : input_base,
    #    'output' : base+'LepLep_muel_2017_04_12',
    #    'tag'    : 'muel',
    #    'dataset': 'SingleMuon',
    #},
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_elel', 'el_pt' : ' > 30 ' },
    #    'input'  : input_base,
    #    'output' : base+'LepLep_elel_2017_04_12',
    #    'tag'    : 'elel',
    #    'dataset': 'SingleElectron',
    #},
    {
        'module' : 'Conf.py',
        'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ' },
        'input'  : input_base,
        'output' : base+'LepGamma_mug_2017_09_05',
        'tag'    : 'mug',
        'dataset': 'SingleMuon',
    },
    {
        'module' : 'Conf.py',
        'args'   : { 'function' : 'make_final_elg', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'eleVeto' : 'None'},
        'input'  : input_base,
        'output' : base+'LepGamma_elg_2017_09_05',
        'tag'    : 'elg',
        'dataset': 'SingleElectron',
    },
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 30 ', 'muphtrig' : 'True' },
    #    'input'  : input_base,
    #    'output' : base+'LepGamma_mug_ditrig_2017_03_06',
    #    'tag'    : 'mugditrig',
    #},
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'phot_vars' : 'True', 'phot_id' : 'None', 'unblind' : 'True' },
    #    'input'  : input_base,
    #    'output' : base+'LepGammaNoPhId_mug_2017_07_20',
    #    'dataset': 'SingleMuon',
    #    'tag'    : 'muglph',
    #},
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_elg', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'phot_vars' : 'True', 'phot_id' : 'None', 'unblind' : 'True' },
    #    'input'  : input_base,
    #    'output' : base+'LepGammaNoPhId_elg_2017_07_20',
    #    'dataset': 'SingleElectron',
    #    'tag'    : 'elglph',
    #},
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_mug', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'phot_vars' : 'True', 'phot_id' : 'loose', 'sec_lep_veto' : 'False' },
    #    'input'  : input_base,
    #    'output' : base+'LepGamma_mug_noseclepveto_2017_03_14',
    #    'tag'    : 'mugnslv',
    #},
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_final_elg', 'mu_pt' : ' > 10 ', 'el_pt' : ' > 10 ' , 'ph_pt' : ' > 15 ', 'phot_vars' : 'True', 'phot_id' : 'loose', 'sec_lep_veto' : 'False' },
    #    'input'  : input_base,
    #    'output' : base+'LepGamma_elg_noseclepveto_2017_03_14',
    #    'tag'    : 'elgnslv',
    #},
    #{
    #    'module' : 'Conf.py',
    #    'args'   : { 'function' : 'make_nofilt' , 'pass_lepton' : 'False'},
    #    'input'  : input_base,
    #    'output' : base+'SigNoFilt_2017_07_03',
    #    'tag'    : 'nofilt',
    #},
    ##{
    ##    'module' : 'Conf.py',
    ##    'args'   : { 'function' : 'make_final_elgjj', 'el_pt' : ' > 30 ' },
    ##    'input'  : input_base_new,
    ##    'output' : base+'LepGammaDiJet_elgjj_2017_01_03',
    ##    'tag'    : 'elgjj',
    ##},
    ##{
    ##    'module' : 'Conf.py',
    ##    'args'   : { 'function' : 'make_final_mugjj', 'mu_pt' : ' > 30 ' },
    ##    'input'  : input_base_new,
    ##    'output' : base+'LepGammaDiJet_mugjj_2017_01_03',
    ##    'tag'    : 'mugjj',
    ##},

]


scheduler_base.RunJobs( jobs, configs, options)

