### ATTENTION: Set OUTPUTMAIN to the folder in your Plotting directory where you want to save your output
OUTPUTMAIN=/home/kakw/efake/WG_Analysis_hcombinetest/WG_Analysis/Plotting/tmp
### ATTENTION: Make sure that these DIR_* strings specify the directories containing the processed ntuples that you want to run over
DIR_MUG=/data/users/friccita/WGammaNtuple/LepGamma_mug_2019_04_11/WithSF
DIR_ELG=/data/users/friccita/WGammaNtuple/LepGamma_elg_2019_04_11/WithSF
#DIR_MUGNoId=/data/users/friccita/WGammaNtuple/LepGammaNoPhId_mug_2019_03_17/WithSF
#DIR_ELGNoId=/data/users/friccita/WGammaNtuple/LepGammaNoPhId_elg_2019_03_17/WithSF
DIR_MUGNoId=/data/users/friccita/WGammaNtuple/LepGammaNoPhId_mug_2019_07_12/WithSF
DIR_ELGNoId=/data/users/friccita/WGammaNtuple/LepGammaNoPhId_elg_2019_07_12/WithSF
DIR_MU=/data/users/friccita/WGammaNtuple/SingleLepNoPhId_mu_2019_04_11/WithSF
DIR_EL=/data/users/friccita/WGammaNtuple/SingleLepNoPhId_el_2019_04_11/WithSF
#DIR_MUMU=/data/users/friccita/WGammaNtuple/LepLep_mumu_2019_07_12/WithSF
#DIR_MUMU=/data/users/kakw/Resonances2016/LepLep_mumu_2019_08_05
DIR_MUMU=/data/users/friccita/WGammaNtuple/LepGammaNoPhId_mug_2019_08_14/WithSF
DIR_ELEL=/data/users/friccita/WGammaNtuple/LepLep_elel_2019_04_11/WithSF

DIR_MUG=/data2/users/kakw/Resonances2016/LepGamma_mug_2019_09_15
DIR_ELG=/data2/users/kakw/Resonances2016/LepGamma_elg_2019_09_15
#DIR_MUGNoId=/data2/users/kakw/Resonances2016/LepGammaNoPhId_mug_2019_06_11b
#DIR_ELGNoId=/data2/users/kakw/Resonances2016/LepGammaNoPhId_elg_2019_06_11b
#DIR_MU=/data2/users/kakw/Resonances2016/LepGammaNoPhId_mug_2019_06_11b
#DIR_EL=/data2/users/kakw/Resonances2016/LepGammaNoPhId_elg_2019_06_11b
#DIR_MUMU=/data2/users/kakw/Resonances2016/LepLep_mumu_2019_06_11b
#DIR_ELEL=/data2/users/kakw/Resonances2016/LepLep_elel_2019_06_11

DIR_SIGTruth=/data/users/friccita/WGammaNtuple/SigNoFilt_2019_04_15/WithSF

#DIR_Combine=/data/users/fengyb/CMSSW_8_1_0/src
DIR_Combine=/home/kakw/efake/WG_Analysis_hcombinetest/CMSSW_8_1_0/src


all : plots workspaces limits

plots :
	python MakePlots.py --baseDirMu ${DIR_MU} --baseDirEl ${DIR_EL} --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG}  --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --baseDirMuMu ${DIR_MUMU} --baseDirElEl ${DIR_ELEL} --baseDirNoFilt ${DIR_SIGTruth} --makeSR --outputDir ${OUTPUTMAIN}/Plots
	#python MakePlots.py --baseDirMu ${DIR_MU} --baseDirEl ${DIR_EL} --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG}  --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --baseDirMuMu ${DIR_MUMU} --baseDirElEl ${DIR_ELEL} --baseDirNoFilt ${DIR_SIGTruth} --baseDirReco ${DIR_MU} --makeBkgTruth --outputDir ${OUTPUTMAIN}/Plots

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
	python MakeMCBkgWS.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --outputDir ${OUTPUTMAIN}/MCBkgWS  --doAllTop --doZGamma --doWJets --doWGamma --doGammaGamma --doAll
	#python MakeMCBkgWS.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --outputDir ${OUTPUTMAIN}/MCBkgWS --doWGamma

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
	#python MakeFitsTest.py --baseDir ${OUTPUTMAIN} --combineDir /home/kakw/efake/WG_Analysis_hcombinetest/CMSSW_8_1_0/src/HiggsAnalysis/CombinedLimit --outputDir /home/kakw/efake/WG_Analysis_hcombinetest/WG_Analysis/Plotting/HiggsAnalysis/output/	--doVarOptimization

signalfits : 
	python MakeResSignalFits.py --baseDirMu  ${DIR_MUG} --baseDirEl ${DIR_ELG} --outputDir ${OUTPUTMAIN}/SignalFits
