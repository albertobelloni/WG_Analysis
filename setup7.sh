# setup CMSSW (without explicitly having a CMSSW release)
cd /cvmfs/cms.cern.ch/slc7_amd64_gcc820/cms/cmssw/CMSSW_11_0_0
eval `scramv1 runtime -sh`
cd -
# add paths within this package
export WorkArea=$PWD/Analysis
# pip2 install --user uncertainties
export PYTHONPATH=$PYTHONPATH:${PWD}/Analysis/TreeFilter/Core/python:${PWD}/Analysis/Util/python:${PWD}/Plotting:~/.local/lib/python2.6/site-packages/
