# Run Analysis

## RecoResonance

The analysis part is based on ntuples made from 

   [https://github.com/albertobelloni/UMDNTuple](https://github.com/albertobelloni/UMDNTuple)

To run the analyzer, first do 
   ```
   git clone https://github.com/albertobelloni/WG_Analysis.git
   cd WG_Analysis/
   ```
If you are on bash:
   ```
   source setup.sh
   ```
or if you are on tcsh:
   ```
   source setup.csh
   ```

If this is your first time to run the analysis, compile the core first:
   ```
   cd Analysis/TreeFilter/Core
   make
   ```

Then modify the script in RecoResonance:
   ```
   cd ../RecoResonance/scripts/
   ```
change the base, output_base, and options.PUPath in scheduler.py if necessary. (By default the base should be already pointed to the correct ntuples. And the PU files should be correct as well. So in principle you only need to modify the output_base to your directory.)

Also change the preselections if needed. Here the make_final_mug is called in Line 243-251. Comment out these lines and uncomment other preselections you want. 

After setting up the config file
   ```
   cd ..
   ```

If you want to submit jobs, do
   ```
   python scripts/scheduler.py
   ```

If you want your jobs to run locally, do
   ```
   python scripts/scheduler.py --local
   ```

After finishing, check if all events in the input files have been processed by
   ```
   python scripts/scheduler.py --check
   ```

More information on the [Twiki](https://twiki.cern.ch/twiki/bin/view/CMS/WGToLNuGResonance). Try search 'how to process ntuples'

## MET filter

For the MET filter, it's under 

    WG_Analysis/Analysis/TreeFilter/RecoResonance/scripts/Conf.py

Line 211-213 or Line 263-265

The three lines will pass the cut ids to FilterMET and select events passing these 7 flags, recommended by the MET group ([Twiki](https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2)).

The filter id and name map can be found in the ntuples from UMDNTuple/FilterInfoTree

If you need to apply the MET filter, simply copy these three lines to the pre-selection function, like in make_final_elg or make_final_mug.

After processing, your new ntuples should contain about 20 branches, such as Flag_BadPFMuonFilter, and if everything is correct, the 7 flags should always be 1 in the new ntuples, i.e.,

    Flag_HBHENoiseFilter

    Flag_HBHENoiseIsoFilter

    Flag_globalSuperTightHalo2016Filter

    Flag_EcalDeadCellTriggerPrimitiveFilter

    Flag_goodVertices

    Flag_BadChargedCandidateFilter

    Flag_BadPFMuonFilter

## FilterOverlap

After finishing the above, please be careful if you are using inclusive and binned MC samples, you might need to run FilterOverlap to remove overlapping between different MC samples, 
   ```
   cd WG_Analysis/Analysis/TreeFilter/FilterOverlap/scripts/
   ```
and modify the base in `scheduler.py` to the your output. 

If this is your first time to run FilterOverlap, please
   ```
   cd WG_Analysis/Analysis/TreeFilter/FilterOverlap/
   mkdir obj
   ```
Otherwise it would go into problem when compiling. Finally,
   ```
   cd ..
   python scripts/scheduler.py
   ```
In theory the cuts should be the same so you don't need to change other settings.

## To play with the Plots and limits

Go to the Plotting directory first. Do
```
root -l My_double_CB/RooDoubleCB.cc+
```
to compile Double Crystal Ball

```
make signal
```
to fit the signal templates with double sided crystal ball function and save the fit results (pdfs, vars and norms) into the workspace. After this, a new directory will be created with some root files under:

```
~/WGamma/WG_Analysis/Plotting/Plots/Resonance/Plots_2019_02_15
```

After the signal part, you can do
```
make mcbkg
```
to prepare the bkg templates for different backgrounds. The default is WGamma only. One could change this in the Makefile. New root files with workspaces for backgrounds will be created in the above directory as well.

When the signal and bkg are all done, if you want to run the limit settings, first you have to get the Higgs Combine code compiled first.
Follow the instructions from 

[https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/)

( For now we are using the CMSSW_8_1_X version. So you could follow the instructions starting from 

[https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#slc6cc7-release-cmssw_8_1_x](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#slc6cc7-release-cmssw_8_1_x)

) 

After compiled the HiggsCombine code, change the `DIR_Combine` in the Makefile to the src location of the CMSSW_8_1_X you just set. Then do
```
make fits
```
This will generate the datacard and the code to run combine, and submit the jobs to condor. It might take one minute to finish, and finally you will get the limit on the signal strength.
