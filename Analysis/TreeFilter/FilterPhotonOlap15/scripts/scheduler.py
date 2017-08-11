import os
import scheduler_base
from scheduler_base import JobConf

from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument( '--run', dest='run', default=False, action='store_true', help='Run filtering' )
p.add_argument( '--check', dest='check', default=False, action='store_true', help='Run check of completion' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--batch', dest='batch', default=False, action='store_true', help='Run on batch, not locally ' )
options = p.parse_args()

if not options.check :
    options.run = True
else :
    options.run = False

options.local = ( not options.batch )


base = '/data/users/jkunkle/Resonances'

# ----------------------------
# The suffix that appears on the 
# end of the output jobs
# ----------------------------

jobs_ht = [
    JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', suffix='GenHTOlap', genht_cut=' < 100 ' ),
]

jobs_ph = [
    JobConf(base, 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'   , suffix = 'PhOlap', pt_cut = ' > 10 ', nph_cut = ' == 0' ),
    JobConf(base, 'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' , suffix = 'PhOlap', pt_cut = ' > 10 ', nph_cut = ' == 0' ),
    JobConf(base, 'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'   , suffix = 'PhOlap', pt_cut = ' > 10 ', nph_cut = ' == 0' ),
    JobConf(base, 'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'  , suffix = 'PhOlap', pt_cut = ' > 10 ', nph_cut = ' == 0' ),
    JobConf(base, 'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'   , suffix = 'PhOlap', pt_cut = ' > 10 ', nph_cut = ' == 0' ),
    JobConf(base, 'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'   , suffix = 'PhOlap', pt_cut = ' > 10 ', nph_cut = ' == 0' ),
    JobConf(base, 'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'  , suffix = 'PhOlap', pt_cut = ' > 10 ', nph_cut = ' == 0' ),
    JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'               , suffix = 'PhOlap', pt_cut = ' > 10 ', nph_cut = ' == 0' ),
    JobConf(base, 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8GenHTOlap'      , suffix = 'PhOlap', pt_cut = ' > 10 ', nph_cut = ' == 0' ),
    JobConf(base, 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'          , suffix = 'PhOlap', pt_cut = ' > 10 ', nph_cut = ' == 0' ),
    JobConf(base, 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'            , suffix = 'PhOlap', pt_cut = ' > 10', nph_cut = ' == 0' ),
    JobConf(base, 'TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', suffix = 'PhOlap', pt_cut = ' > 10', nph_cut = ' == 0' ),
    JobConf(base, 'TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'   , suffix = 'PhOlap', pt_cut = ' > 10', nph_cut = ' == 0' ),
    JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                , suffix = 'PhCutMax', pt_cut = ' > 160 ', nph_cut = ' == 0' ),
    JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                 , suffix = 'PhCutMax', pt_cut = ' > 160 ', nph_cut = ' == 0' ),
    JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'        , suffix = 'PhCutMax', pt_cut = ' > 530 ', nph_cut = ' == 0' ),
    JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'         , suffix = 'PhCutMax', pt_cut = ' > 530 ', nph_cut = ' == 0' ),
    JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8PhCutMax', suffix = 'PhCutMin', pt_cut = ' > 160 ', nph_cut = ' > 0' ),
    JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-madgraphMLM-pythia8PhCutMax' , suffix = 'PhCutMin', pt_cut = ' > 160 ', nph_cut = ' > 0' ),
    JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'        , suffix = 'PhCutMin', pt_cut = ' > 530 ', nph_cut = ' > 0' ),
    JobConf(base, 'WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'         , suffix = 'PhCutMin', pt_cut = ' > 530 ', nph_cut = ' > 0' ),
]

jobs_mtres = [
    JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8PhCutMax'                , suffix = 'MTResCut', mtres_cut = ' < 600 '),
    JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8PhCutMaxPhCutMin', suffix = 'MTResCut', mtres_cut = ' < 1300 '),
    JobConf(base, 'WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8PhCutMax'                 , suffix = 'MTResCut', mtres_cut= ' < 500 '),
    JobConf(base, 'WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-madgraphMLM-pythia8PhCutMaxPhCutMin' , suffix = 'MTResCut', mtres_cut= ' < 1300 '),
]

options.nFilesPerJob = 1
options.nproc = 2
options.treename='tupel/EventTree'
options.exename='RunAnalysis'
options.copyInputFiles=True
options.enableKeepFilter=False

#input_dirs = ['SingleLepNoPhID_el_2017_02_03', 'SingleLepNoPhID_mu_2017_02_03']
#input_dirs = ['SingleLepNoPhID_mu_2017_04_12', 'SingleLepNoPhID_el_2017_04_12','LepGamma_mug_2017_04_12', 'LepGamma_elg_2017_04_12', 'LepLep_mumu_2017_04_12', 'LepLep_elel_2017_04_12', 'LepLep_muel_2017_04_12']
input_dirs = ['LepGammaNoPhId_elg_2017_07_20', 'LepGammaNoPhId_mug_2017_07_20']
module = 'Conf.py'

for input_dir in input_dirs :
    for job in jobs_ht :
        config_ht = { 
                        'module' : module,
                        'args'   : { 'function' : 'filter_genht', 'genht_cut' : getattr(job, 'genht_cut', None) },
                        'input'  : input_dir,
                        'output' : base + '/' + input_dir,
                        'tag'    : 'genhtolap',
        }

        scheduler_base.RunJobs( job, config_ht, options)

    for job in jobs_ph :
    
        config_ph = { 
                        'module' : module,
                        'args'   : { 'function' : 'filter_photon', 'pt_cut' : getattr(job, 'pt_cut', None), 'nph_cut' :  getattr(job, 'nph_cut', None) },
                        'input'  : input_dir,
                        'output' : base + '/' + input_dir,
                        'tag'    : 'phcut',
        }
    
        scheduler_base.RunJobs( job, config_ph, options)

    for job in jobs_mtres :
    
        config_ph = { 
                        'module' : module,
                        'args'   : { 'function' : 'filter_mtres', 'mtres_cut' : getattr(job, 'mtres_cut', None) },
                        'input'  : input_dir,
                        'output' : base + '/' + input_dir,
                        'tag'    : 'mtrescut',
        }
    
        scheduler_base.RunJobs( job, config_ph, options)

    
