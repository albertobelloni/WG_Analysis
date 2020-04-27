#!/bin/bash

START_TIME=`/bin/date`
echo "started at $START_TIME"
pwd

STEP=$1
BINLOW=$2
BINHIGH=$3
REGION=$4
EXTRA=$5

BASE=/home/kakw/efake/WG_Analysis
cd $BASE
VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/
source $VO_CMS_SW_DIR/cmsset_default.sh
#cd /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_25/src
cd /cvmfs/cms.cern.ch/slc7_amd64_gcc820/cms/cmssw/CMSSW_11_0_0/src
#cd /cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_9_3_3/src 
eval `scramv1 runtime -sh`
cd -
# add python to path
#export PATH=$PYTHONDIR/bin:$PATH
# add paths within this package
#export WorkArea=$PWD/Analysis
#export PYTHONPATH=$PYTHONPATH:${BASE}/Analysis/TreeFilter/Core/python:${BASE}/Analysis/Util/python:${BASE}/Plotting
export PYTHONPATH=$PYTHONPATH:${PWD}/Analysis/TreeFilter/Core/python:${PWD}/Analysis/Util/python:${PWD}/Plotting:~/.local/lib/python2.6/site-packages/
cd Plotting


echo "./MakeZFit.py --step $STEP --binlow $BINLOW --binhigh $BINHIGH --region $REGION $EXTRA"
./MakeZFit.py --step $STEP --binlow $BINLOW --binhigh $BINHIGH --region $REGION $EXTRA
exitcode=$?
echo $exitcode


echo ""
END_TIME=`/bin/date`
echo "finished at $END_TIME"
exit $exitcode
