# setup CMSSW (without explicitly having a CMSSW release)
cd /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_25/src
eval `scramv1 runtime -sh`
cd -
# add paths within this package
export WorkArea=$PWD/Analysis
# pip2 install --user uncertainties
export PYTHONPATH=$PYTHONPATH:${PWD}/Analysis/TreeFilter/Core/python:${PWD}/Analysis/Util/python:${PWD}/Plotting:~/.local/lib/python2.6/site-packages/
