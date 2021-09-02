# setup CMSSW (without explicitly having a CMSSW release)
cd CMSSW_11_0_0/src
eval `scramv1 runtime -csh`
cd -

setenv WorkArea ${PWD}/Analysis
if( $?PYTHONPATH == 0 ) then
   setenv PYTHONPATH ${PWD}/Analysis/TreeFilter/Core/python:${PWD}/Analysis/Util/python:${PWD}/Plotting:${PWD}/CMSSW_11_0_0/src/CombineHarvester/CombinePdfs/scripts:${PWD}/CMSSW_11_0_0/src/CombineHarvester/CombineTools/scripts:${PWD}//CMSSW_11_0_0/src/HiggsAnalysis/CombinedLimit/scripts
else 
   setenv PYTHONPATH ${PWD}/Analysis/TreeFilter/Core/python:${PWD}/Analysis/Util/python:${PWD}/Plotting:${PWD}/Plotting/CMSSW_11_0_0/src/CombineHarvester/CombinePdfs/scripts:${PWD}/CMSSW_11_0_0/src/CombineHarvester/CombineTools/scripts:${PWD}//CMSSW_11_0_0/src/HiggsAnalysis/CombinedLimit/scripts:$PYTHONPATH
endif

