### ATTENTION: Set OUTPUTMAIN to the folder in your Plotting directory where you want to save your output
OUTPUTMAIN=/home/kakw/efake/WG_Analysis/Plotting/Plots/Resonance/
### ATTENTION: Make sure that these DIR_* strings specify the directories containing the processed ntuples that you want to run over
DIR_MUG=/data/users/fengyb/WGammaNtuple/Legacy2016/LepGamma_mug_2018_10_11
DIR_ELG=/data/users/fengyb/WGammaNtuple/Legacy2016/LepGamma_elg_2018_10_11
DIR_MUGNoId=/data/users/friccita/WGammaNtuple/LepGammaNoPhId_mug_2019_03_17/WithSF
DIR_ELGNoId=/data/users/friccita/WGammaNtuple/LepGammaNoPhId_mug_2019_03_17/WithSF
#DIR_MU=/data/users/jkunkle/Resonances/SingleLepNoPhID_mu_2018_03_28
DIR_MU=/data/users/friccita/WGammaNtuple/SingleLepNoPhId_mu_2019_03_17/WithSF
DIR_EL=/data/users/friccita/WGammaNtuple/SingleLepNoPhId_mu_2019_03_17/WithSF
DIR_MUMU=/data/users/friccita/WGammaNtuple/LepLep_mumu_2018_11_30/WithSF
DIR_ELEL=/data/users/friccita/WGammaNtuple/LepLep_elel_2018_08_13

DIR_SIGTruth=/data/users/friccita/WGamma/WG_Analysis/Resonances/SigNoFilt_2018_02_02

DIR_Combine=/data/users/fengyb/CMSSW_8_1_0/src


all : plots workspaces limits

plots :
	#python MakePlots.py --baseDirMu ${DIR_MU} --baseDirEl ${DIR_EL} --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG}  --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --baseDirMuMu ${DIR_MUMU} --baseDirElEl ${DIR_ELEL} --baseDirNoFilt ${DIR_SIGTruth} --makeZCR --makeWCR --makeSR --makeJetBkg --makeEleBkg --outputDir ${OUTPUTMAIN}/Plots
	python MakePlots.py --baseDirMu ${DIR_MU} --baseDirEl ${DIR_EL} --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG}  --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --baseDirMuMu ${DIR_MUMU} --baseDirElEl ${DIR_ELEL} --baseDirNoFilt ${DIR_SIGTruth} --makeJetBkg --outputDir ${OUTPUTMAIN}/Plots
	#python MakePlots.py --baseDirMu ${DIR_MU} --baseDirEl ${DIR_EL} --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG}  --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --baseDirMuMu ${DIR_MUMU} --baseDirElEl ${DIR_ELEL} --baseDirNoFilt ${DIR_SIGTruth} --makeSR --outputDir ${OUTPUTMAIN}/Plots

wjets : 

	python MakeWJetsWS.py --baseDirMuNoG ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --doClosure  --outputDir ${OUTPUTMAIN}/WJetsWS
	#python MakeWJetsWS.py --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --outputDir ${OUTPUTMAIN}/WJetsWS

kfactor:

	python KFactorWS.py --baseDirMuNoG ${DIR_MU} --baseDirElNoG ${DIR_EL} --outputDir ${OUTPUTMAIN}/WJetsWS

matrix:
	python MatrixWJetsWS.py --baseDirMuMu ${DIR_MUMU} --baseDirElEl ${DIR_ELEL} --outputDir ${OUTPUTMAIN}/WJetsWS

signal : 

	python MakeSignalWS.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --outputDir ${OUTPUTMAIN}/SignalWS

mcbkg : 

	#python MakeMCBkgWS.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --outputDir ${OUTPUTMAIN}/MCBkgWS
	#python MakeMCBkgWS.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --outputDir ${OUTPUTMAIN}/MCBkgWS --doTopGamma --doTop --doZGamma --doWJets --doWGamma --doGammaGamma --doAll
	python MakeMCBkgWS.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --outputDir ${OUTPUTMAIN}/MCBkgWS --doWGamma

efake : 

	python MakeEFakeWS.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --outputDir ${OUTPUTMAIN}/EFakeWS


workspaces :
	#python MakeWorkspaces.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --doSignal --doWGamma --doTop --doZGamma --doWJets --doEleFake --doClosure --outputDir ${OUTPUTMAIN}/Workspaces
	#python MakeWorkspaces.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId}  --doSignal --doWGamma --doTop --doZGamma  --outputDir ${OUTPUTMAIN}/Workspaces
	#python MakeWorkspaces.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --doWJets --doEleFake --doClosure  --outputDir ${OUTPUTMAIN}/Workspaces
	#python MakeWorkspaces.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --doWGamma --outputDir ${OUTPUTMAIN}/Workspaces
	python MakeSignalWS.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --doSignal --outputDir ${OUTPUTMAIN}/Workspaces

fits :
	#python MakeFits.py --baseDir ${OUTPUTMAIN}/Workspaces/ --combineDir /home/friccita/WGamma/WG_Analysis/CMSSW_8_1_0 --outputDir ${OUTPUTMAIN} --doVarOptimization   --useHistTemplate  --noRunCombine
	python MakeFitsTest.py --baseDir ${OUTPUTMAIN} --combineDir ${DIR_Combine}/HiggsAnalysis/CombinedLimit --outputDir ${DIR_Combine}/TEST --doVarOptimization

signalfits : 
	python MakeResSignalFits.py --baseDirMu  ${DIR_MUG} --baseDirEl ${DIR_ELG} --outputDir ${OUTPUTMAIN}/SignalFits
