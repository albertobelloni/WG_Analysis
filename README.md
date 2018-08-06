The analysis part is based on ntuples made from 

   https://github.com/albertobelloni/UMDNTuple

To run the analyzer, first do 

   **git clone https://github.com/albertobelloni/WG_Analysis.git**

   **cd WG_Analysis/**

If you are on bash:

   **source setup.sh**

or if you are on tcsh:

   **source setup.csh**


If this is your first time to run the analysis, compile the core first:

   **cd Analysis/TreeFilter/Core**

   **make**

Then modify the script in RecoResonance:

   **cd ../RecoResonance/scripts/**

change the base, output_base, and options.PUPath if necessary

   **cd ..**

   **python scripts/scheduler.py**

If you want your jobs to run locally, do

   **python scripts/scheduler.py --local**

After finishing, check if all events in the input files have been processed by

   **python scripts/scheduler.py --check**

More information on the Twiki:

    https://twiki.cern.ch/twiki/bin/view/CMS/WGToLNuGResonance

Try search 'how to process ntuples'

For the MET filter, it's under 

    WG_Analysis/Analysis/TreeFilter/RecoResonance/scripts/Conf.py

Line 211-213 or Line 263-265

The three lines will pass the cut ids to FilterMET and select events passing these 7 flags, recommended by the MET group:

    https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2

The filter id and name map can be found in the ntuples from UMDNTuple/FilterInfoTree

If you need to apply the MET filter, simply copy these three lines to the pre-selection function, like in make_final_elg or make_final_mug.

After processing, your new ntuples should contain about 20 branches, such as Flag_BadPFMuonFilter, and if everything is correct, the 7 flags should always be 1 in the new ntuples, i.e.,

    Flag_HBHENoiseFilter

    Flag_HBHENoiseIsoFilter

    Flag_globalSuperTightHalo2016Filter

    Flag_EcalDeadCellTriggerPrimit

    Flag_goodVertices

    Flag_BadChargedCandidateFilter

    Flag_BadPFMuonFilter


After finishing the above, please be careful if you are using inclusive and binned MC samples, you might need to run FilterOverlap to remove overlapping between different MC samples, 

  **cd WG_Analysis/Analysis/TreeFilter/FilterOverlap/scripts/**

and modify the base to the your output

  **cd ..**

  **python scripts/scheduler.py**

In theory the cuts should be the same so you don't need to change other settings.
