### ATTENTION: Set OUTPUTMAIN to the folder in your Plotting directory where you want to save your output
### ATTENTION: Make sure that these DIR_* strings specify the directories containing the processed ntuples that you want to run over
DIR_MUG=/data/users/friccita/WGammaNtuple/LepGamma_mug_2019_04_11/WithSF
DIR_ELG=/data/users/friccita/WGammaNtuple/LepGamma_elg_2019_04_11/WithSF
DIR_MUGNoId=/data/users/friccita/WGammaNtuple/LepGammaNoPhId_mug_2019_07_12/WithSF
DIR_ELGNoId=/data/users/friccita/WGammaNtuple/LepGammaNoPhId_elg_2019_07_12/WithSF
DIR_MU=/data/users/friccita/WGammaNtuple/SingleLepNoPhId_mu_2019_04_11/WithSF
DIR_EL=/data/users/friccita/WGammaNtuple/SingleLepNoPhId_el_2019_04_11/WithSF
DIR_MUMU=/data/users/friccita/WGammaNtuple/LepGammaNoPhId_mug_2019_09_04/WithSF
DIR_ELEL=/data/users/friccita/WGammaNtuple/LepLep_elel_2019_04_11/WithSF

DIR_MUG=/data2/users/kakw/Resonances2016/LepGamma_mug_2019_10_04
DIR_ELG=/data2/users/kakw/Resonances2016/LepGamma_elg_2019_10_04
DIR_Combine=/home/kakw/efake/WG_Analysis_hcombinetest/CMSSW_8_1_0/src

OUTPUTMAIN=/data/users/yihuilai/test_code/WG_Analysis/Plotting/data
OUTPUTMAIN=data

all : plots workspaces limits

plots :
	python MakePlots.py --baseDirMu ${DIR_MU} --baseDirEl ${DIR_EL} --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG}  --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --baseDirMuMu ${DIR_MUMU} --baseDirElEl ${DIR_ELEL} --baseDirNoFilt ${DIR_SIGTruth} --makeSR --outputDir ${OUTPUTMAIN}/Plots

zcr:
	nohup nice python3 -u MakePlots.py --makeZCR --year 2016 > makeZCR2016.out 2>&1 &
	nohup nice python3 -u MakePlots.py --makeZCR --year 2017 > makeZCR2017.out 2>&1 &
	nohup nice python3 -u MakePlots.py --makeZCR --year 2018 > makeZCR2018.out 2>&1 &

wcr:
	nohup nice python3 -u MakePlots.py --makeWCR --year 2016 > makeWCR2016.out 2>&1 &
	nohup nice python3 -u MakePlots.py --makeWCR --year 2017 > makeWCR2017.out 2>&1 &
	nohup nice python3 -u MakePlots.py --makeWCR --year 2018 > makeWCR2018.out 2>&1 &

control:
	make zcr
	make wcr

wjets : 

	python MakeWJetsWS.py --baseDirMuNoG ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --doClosure  --outputDir ${OUTPUTMAIN}/WJetsWS
	#python MakeWJetsWS.py --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --outputDir ${OUTPUTMAIN}/WJetsWS

kfactor:

	python KFactorWS.py --baseDirMuNoG ${DIR_MU} --baseDirElNoG ${DIR_EL} --outputDir ${OUTPUTMAIN}/WJetsWS

matrix:

	python MatrixWJetsWS.py --baseDirMuMu ${DIR_MUMU} --baseDirElEl ${DIR_ELEL} --outputDir ${OUTPUTMAIN}/WJetsWS


beff:

	./MakeBEff.py --year 2016 --ch mu --batch --condor
	./MakeBEff.py --year 2017 --ch mu --batch --condor
	./MakeBEff.py --year 2018 --ch mu --batch --condor
	./MakeBEff.py --year 2016 --ch el --batch --condor
	./MakeBEff.py --year 2017 --ch el --batch --condor
	./MakeBEff.py --year 2018 --ch el --batch --condor

fit:

	#python MakeFits.py --BiasStudy --NoBKGUnc --condor --usedata # --GoF--noRunCombine
	python MakeFits.py --NoBKGUnc --condor --usedata --paramodel # --GoF--noRunCombine
	#python MakeFits.py --usedata --NoBKGUnc --condor #--noRunCombine

nofit:

	python MakeFits.py --NoBKGUnc  --noRunCombine --usedata --paramodel



limit:

	./limitplot.py data_1015_afterbias_study/higgs/Results/result_0p01_all.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_5_all.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_0p01_el2016.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_0p01_mu2016.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_5_el2016.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_5_mu2016.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_0p01_el2017.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_0p01_el2018.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_0p01_mu2017.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_0p01_mu2018.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_5_el2017.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_5_el2018.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_5_mu2017.json
	./limitplot.py data_1015_afterbias_study/higgs/Results/result_5_mu2018.json

syspdf:	

	python MakeSystematics.py --batch --year 2016 --ch mu --condor --Onlypdf --pdfstart 0 --pdfend 20
	python MakeSystematics.py --batch --year 2016 --ch mu --condor --Onlypdf --pdfstart 21 --pdfend 40
	python MakeSystematics.py --batch --year 2016 --ch mu --condor --Onlypdf --pdfstart 41 --pdfend 60
	python MakeSystematics.py --batch --year 2016 --ch mu --condor --Onlypdf --pdfstart 61 --pdfend 80
	python MakeSystematics.py --batch --year 2016 --ch mu --condor --Onlypdf --pdfstart 81 --pdfend 100

	python MakeSystematics.py --batch --year 2016 --ch el --condor --Onlypdf --pdfstart 0 --pdfend 20
	python MakeSystematics.py --batch --year 2016 --ch el --condor --Onlypdf --pdfstart 21 --pdfend 40
	python MakeSystematics.py --batch --year 2016 --ch el --condor --Onlypdf --pdfstart 41 --pdfend 60
	python MakeSystematics.py --batch --year 2016 --ch el --condor --Onlypdf --pdfstart 61 --pdfend 80
	python MakeSystematics.py --batch --year 2016 --ch el --condor --Onlypdf --pdfstart 81 --pdfend 100

	python MakeSystematics.py --batch --year 2017 --ch mu --condor --Onlypdf --pdfstart 0 --pdfend 20
	python MakeSystematics.py --batch --year 2017 --ch mu --condor --Onlypdf --pdfstart 21 --pdfend 40
	python MakeSystematics.py --batch --year 2017 --ch mu --condor --Onlypdf --pdfstart 41 --pdfend 60
	python MakeSystematics.py --batch --year 2017 --ch mu --condor --Onlypdf --pdfstart 61 --pdfend 80
	python MakeSystematics.py --batch --year 2017 --ch mu --condor --Onlypdf --pdfstart 81 --pdfend 100

	python MakeSystematics.py --batch --year 2017 --ch el --condor --Onlypdf --pdfstart 0 --pdfend 20
	python MakeSystematics.py --batch --year 2017 --ch el --condor --Onlypdf --pdfstart 21 --pdfend 40
	python MakeSystematics.py --batch --year 2017 --ch el --condor --Onlypdf --pdfstart 41 --pdfend 60
	python MakeSystematics.py --batch --year 2017 --ch el --condor --Onlypdf --pdfstart 61 --pdfend 80
	python MakeSystematics.py --batch --year 2017 --ch el --condor --Onlypdf --pdfstart 81 --pdfend 100

	python MakeSystematics.py --batch --year 2018 --ch mu --condor --Onlypdf --pdfstart 0 --pdfend 20
	python MakeSystematics.py --batch --year 2018 --ch mu --condor --Onlypdf --pdfstart 21 --pdfend 40
	python MakeSystematics.py --batch --year 2018 --ch mu --condor --Onlypdf --pdfstart 41 --pdfend 60
	python MakeSystematics.py --batch --year 2018 --ch mu --condor --Onlypdf --pdfstart 61 --pdfend 80
	python MakeSystematics.py --batch --year 2018 --ch mu --condor --Onlypdf --pdfstart 81 --pdfend 100

	python MakeSystematics.py --batch --year 2018 --ch el --condor --Onlypdf --pdfstart 0 --pdfend 20
	python MakeSystematics.py --batch --year 2018 --ch el --condor --Onlypdf --pdfstart 21 --pdfend 40
	python MakeSystematics.py --batch --year 2018 --ch el --condor --Onlypdf --pdfstart 41 --pdfend 60
	python MakeSystematics.py --batch --year 2018 --ch el --condor --Onlypdf --pdfstart 61 --pdfend 80
	python MakeSystematics.py --batch --year 2018 --ch el --condor --Onlypdf --pdfstart 81 --pdfend 100

sys:

	python MakeSystematics.py --batch --year 2016 --ch mu --condor
	python MakeSystematics.py --batch --year 2017 --ch mu --condor
	python MakeSystematics.py --batch --year 2018 --ch mu --condor
	python MakeSystematics.py --batch --year 2016 --ch el --condor
	python MakeSystematics.py --batch --year 2017 --ch el --condor
	python MakeSystematics.py --batch --year 2018 --ch el --condor

llvalid : 

	python MakeMuValidPlot.py --batch --year 2016 --condor
	python MakeMuValidPlot.py --batch --year 2017 --condor
	python MakeMuValidPlot.py --batch --year 2018 --condor
	python MakeEGValidPlot.py --batch --year 2016 --condor
	python MakeEGValidPlot.py --batch --year 2017 --condor
	python MakeEGValidPlot.py --batch --year 2018 --condor

lgvalid : 

	python MakeElGValidPlot.py --batch --year 2016 --condor
	python MakeElGValidPlot.py --batch --year 2017 --condor
	python MakeElGValidPlot.py --batch --year 2018 --condor
	python MakeMuGValidPlot.py --batch --year 2016 --condor
	python MakeMuGValidPlot.py --batch --year 2017 --condor
	python MakeMuGValidPlot.py --batch --year 2018 --condor

money : 

	python MakeMoneyPlot.py --batch --year 2016 --condor
	python MakeMoneyPlot.py --batch --year 2017 --condor
	python MakeMoneyPlot.py --batch --year 2018 --condor

signal : 

	python MakeSignalWS.py --batch --condor --year 2016 --dataDir ${OUTPUTMAIN}/sigfit
	python MakeSignalWS.py --batch --condor --year 2017 --dataDir ${OUTPUTMAIN}/sigfit
	python MakeSignalWS.py --batch --condor --year 2018 --dataDir ${OUTPUTMAIN}/sigfit

bkg : 

	python MakeMCBkgWS.py --process All --batch --year 2016 --condor --dataDir ${OUTPUTMAIN}/bkgfit
	python MakeMCBkgWS.py --process All --batch --year 2017 --condor --dataDir ${OUTPUTMAIN}/bkgfit
	python MakeMCBkgWS.py --process All --batch --year 2018 --condor --dataDir ${OUTPUTMAIN}/bkgfit

efake : 

	python MakeEFakeWS.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --outputDir ${OUTPUTMAIN}/EFakeWS


workspaces :
	#python MakeWorkspaces.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --doSignal --doWGamma --doTop --doZGamma --doWJets --doEleFake --doClosure --outputDir ${OUTPUTMAIN}/Workspaces
	#python MakeWorkspaces.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId}  --doSignal --doWGamma --doTop --doZGamma  --outputDir ${OUTPUTMAIN}/Workspaces
	#python MakeWorkspaces.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --doWJets --doEleFake --doClosure  --outputDir ${OUTPUTMAIN}/Workspaces
	#python MakeWorkspaces.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --doWGamma --outputDir ${OUTPUTMAIN}/Workspaces
	python MakeSignalWS.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --doSignal --outputDir ${OUTPUTMAIN}/Workspaces

signalfits : 
	python MakeResSignalFits.py --baseDirMu  ${DIR_MUG} --baseDirEl ${DIR_ELG} --outputDir ${OUTPUTMAIN}/SignalFits
