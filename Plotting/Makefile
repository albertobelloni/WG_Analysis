OUTPUTMAIN=~/Plots/Resonance/Plots_2017_09_13

DIR_MUG=/data/users/jkunkle/Resonances/LepGamma_mug_2017_09_05/
DIR_ELG=/data/users/jkunkle/Resonances/LepGamma_elg_2017_09_05/ 
DIR_MUGNoId=/data/users/jkunkle/Resonances/LepGammaNoPhId_mug_2017_07_20/
DIR_ELGNoId=/data/users/jkunkle/Resonances/LepGammaNoPhId_elg_2017_07_20/
DIR_MU=/data/users/jkunkle/Resonances/SingleLepNoPhID_mu_2017_07_18/
DIR_EL=/data/users/jkunkle/Resonances/SingleLepNoPhID_el_2017_07_18/  
DIR_MUMU=/data/users/jkunkle/Resonances/LepLep_mumu_2017_04_12/
DIR_ELEL=/data/users/jkunkle/Resonances/LepLep_elel_2017_04_12/
DIR_SIGTruth=/data/users/jkunkle/Resonances/SigNoFilt_2017_07_03


all : plots fits

plots :
	python MakeResonancePlots --baseDirMu ${DIR_MU} --baseDirEl ${DIR_EL} --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG}  --baseDirMuGNoId ${DIR_MUGNoId} --baseDirELGNoId ${DIR_ElGNoId} --baseDirMuMu ${DIR_MUMU} --baseDirELEL ${DIR_ELEL} --baseDirNoFilt ${DIR_SIGTruth} --makeZCR --makeWCR --makeSR --makeJetBkg --makeJetBkg --makeEleBkg --outputDir ${OUTPUTMAIN}/Plots

fits :
	python MakeResWJetsBkg.py --baseDirMuG ${DIR_MUG} --baseDirElG ${DIR_ELG} --baseDirMuGNoId ${DIR_MUGNoId} --baseDirElGNoId ${DIR_ELGNoId} --doSignal --doWGamma --doWJets --doEleFake --doClosure --outputDir ${OUTPUTMAIN}/Workspaces

