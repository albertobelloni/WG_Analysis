#!/usr/bin/env bash 

cd /home/kakw/efake/WG_Analysis/Plotting/data/higgs/
rm limits$2.root higgsCombine*.AsymptoticLimits.*mH$2*.root
combine -M AsymptoticLimits -m $2 $1 --singlePoint 0.1 -n 0.1
combine -M AsymptoticLimits -m $2 $1 --singlePoint 0.2 -n 0.2
combine -M AsymptoticLimits -m $2 $1 --singlePoint 0.3 -n 0.3
combine -M AsymptoticLimits -m $2 $1 --singlePoint 0.5 -n 0.5
combine -M AsymptoticLimits -m $2 $1 --singlePoint 1. -n 1.
combine -M AsymptoticLimits -m $2 $1 --singlePoint 1.5 -n 1.5
combine -M AsymptoticLimits -m $2 $1 --singlePoint 2. -n 2.
combine -M AsymptoticLimits -m $2 $1 --singlePoint 2.3 -n 2.3
combine -M AsymptoticLimits -m $2 $1 --singlePoint 2.6 -n 2.6
combine -M AsymptoticLimits -m $2 $1 --singlePoint 3. -n 3.
combine -M AsymptoticLimits -m $2 $1 --singlePoint 3.3 -n 3.3
combine -M AsymptoticLimits -m $2 $1 --singlePoint 3.6 -n 3.6
combine -M AsymptoticLimits -m $2 $1 --singlePoint 4. -n 4.
hadd limits$2.root higgsCombine*.AsymptoticLimits.*$2*
combine -M AsymptoticLimits -m $2 $1 --getLimitFromGrid limits$2.root >& $3 # /home/kakw/efake/WG_Analysis/Plotting/data/higgs//Width5/results_mt_res_M350_W5_mu2016.txt

echo "run: python MakeFits.py --doVarOpt --noRunCombine" 
