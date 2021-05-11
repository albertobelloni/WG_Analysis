# setup CMSSW (without explicitly having a CMSSW release)
#source /cvmfs/cms.cern.ch/cmsset_default.sh
#cd /cvmfs/cms.cern.ch/slc7_amd64_gcc820/cms/cmssw/CMSSW_11_0_0
cd Plotting/CMSSW_11_0_0/src
eval `scramv1 runtime -csh`
cd -

setenv WorkArea ${PWD}/Analysis
if( $?PYTHONPATH == 0 ) then
   setenv PYTHONPATH ${PWD}/Analysis/TreeFilter/Core/python:${PWD}/Analysis/Util/python:${PWD}/Plotting:${PWD}/Plotting/CMSSW_11_0_0/src/CombineHarvester/CombinePdfs/scripts:${PWD}/Plotting/CMSSW_11_0_0/src/CombineHarvester/CombineTools/scripts:${PWD}/Plotting/CMSSW_11_0_0/src/HiggsAnalysis/CombinedLimit/scripts
else 
   setenv PYTHONPATH ${PWD}/Analysis/TreeFilter/Core/python:${PWD}/Analysis/Util/python:${PWD}/Plotting:${PWD}/Plotting/CMSSW_11_0_0/src/CombineHarvester/CombinePdfs/scripts:${PWD}/Plotting/CMSSW_11_0_0/src/CombineHarvester/CombineTools/scripts:${PWD}/Plotting/CMSSW_11_0_0/src/HiggsAnalysis/CombinedLimit/scripts:$PYTHONPATH
endif

