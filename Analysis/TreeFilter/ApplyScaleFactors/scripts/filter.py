
#************************************************************************************
#
# filter.py
#
# Author : Josh Kunkle  (jkunkle@cern.ch)
#
# This script is called to run the analysis.  All of the heavy lifting
# is in the core package, so just import it, parse the options, and run
# The only work that is done here is to determine the package path
# so that the generated c++ files go into the correct place
#************************************************************************************
# Examples :
# Run all scale factors
# python scripts/filter.py  --filesDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalMuUnblindAll_2015_08_01/job_NLO_WAA_FSR --outputDir /afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaFinalMuUnblindAll_2015_08_01/job_NLO_WAA_FSRWithSF --outputFile tree.root --treeName ggNtuplizer/EventTree --fileKey tree.root --module scripts/Conf.py --confFileName job_NLO_WAA_FSR.txt --nFilesPerJob 1 --nproc 6 --exeName RunAnalysisMC --moduleArgs "{ 'functions' : 'get_muon_sf,get_electron_sf,get_photon_sf,get_pileup_sf', 'args' : { 'PUDistMCFile' : 'root://eoscms//eos/cms/store/user/cranelli/WGamGam/NLO_ggNtuples//job_NLO_WAA_FSR.root'  } }" 
#************************************************************************************

import os
import core

options = core.ParseArgs()

#*************************************
# get the path of this script
#*************************************
script_path = os.path.realpath(__file__)
package_name = script_path.split('/')[-3]

# run it!
core.config_and_run( options, package_name )

