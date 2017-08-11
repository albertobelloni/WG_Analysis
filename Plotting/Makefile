OUTPUTMAIN=~/Plots/ZggPlotsOneBin_2015_12_01
SYSTFILE=$(OUTPUTMAIN)/JetFakeTemplatePlots/systematics.pickle
PLOTDIR=PlotsUnblind

JETFITVARS=sigmaIEIE chIsoCorr
JETFFCORRINPUTS=veryloose
MODULE=Modules/JetFakeFit.py
all : plots syst jet ele background evetosf
	@echo "^_^ FINISHED ^_^"

#-----------------------------
# Single photon binning
SINGLEPTBINS = 15,25,40,70,1000000

jet :
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels muhighmt --ptbins $(PTBINSJET) $(SUBLSTR)
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels mulowmt --ptbins $(PTBINSJET) $(SUBLSTR)
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels ellooselowmt --ptbins $(PTBINSJET) $(SUBLSTR)
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels ellooseinvpixleadlowmt --ptbins $(PTBINSJET) $(SUBLSTR)
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels ellooseinvpixsubllowmt --ptbins $(PTBINSJET) $(SUBLSTR)
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfullhighmt --ptbins $(PTBINSJET) $(SUBLSTR)
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfullinvpixleadhighmt --ptbins $(PTBINSJET) $(SUBLSTR)
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfullinvpixsublhighmt --ptbins $(PTBINSJET) $(SUBLSTR)
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfulllowmt --ptbins $(PTBINSJET) $(SUBLSTR)
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfullinvpixleadlowmt --ptbins $(PTBINSJET) $(SUBLSTR)
	python RunMatrixFit.py --samplesConf Modules/JetFakeFit.py --fileName tree.root --samplesConfGG Modules/JetFakeFit.py --treeName ggNtuplizer/EventTree --xsFile cross_sections/wgamgam.py --lumi 19400 --outputDir $(OUTPUTMAIN) --syst_file   $(SYSTFILE) --channels elfullinvpixsubllowmt --ptbins $(PTBINSJET) $(SUBLSTR)

ele :
	python FitElectronFakes.py --baseDir /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/ --dirNom LepGammaNoPhID_2015_11_09 --dirInv  LepGammaMediumPhIDNoTrigElOlapRmDupInvPSV_2016_03_10 --treeName ggNtuplizer/EventTree --fileName tree.root --lumi 19400 --samplesConf Modules/ElectronFake.py --outputDir $(OUTPUTMAIN) --ndkeys_cms_fine 

backupele :
	python MakeBackupEleBkgEstimate.py --baseDir $(OUTPUTMAIN)
tandp :
	#python FitTagAndProbe.py  --photon --outputDir ~/Plots/WggPlots_2015_01_10

evetosf :
	python DoPhotonEvetoEfficiency.py  --outputDir $(OUTPUTMAIN)

syst :
	python CollectSystUncertanities.py --baseDir $(OUTPUTMAIN) --save

plots :
	python MakeWggHists.py --xsFile cross_sections/wgamgam.py --makeEvent --makeEleFake --makeJetFakeTemplate --makeJetFakeSyst --makeLepGamma --makeLepLepGamma --lumi 19400 --outputDir $(OUTPUTMAIN)  --save

background :
	python MakeBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --ptbins 15,1000000 --plotDir $(PLOTDIR) --zgg

singlebackground :
	python MakeSingleBackgroundEstimates.py --baseDir $(OUTPUTMAIN) --plotDir PlotsNom --ptbins 15,25,40,70,150 --wcr

finalplots :
	python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR)  --outputDir $(OUTPUTMAIN)/FinalPlotsOneBin --zgg
	python MakeFinalHists.py  --baseDir $(OUTPUTMAIN)/BackgroundEstimates/$(PLOTDIR)/Summed  --outputDir $(OUTPUTMAIN)/MoneyPlots --money --zgg

finalplotssingle :
	python MakeFinalSingleHists.py  --baseDir $(OUTPUTMAIN)/SinglePhotonWCRBackgroundEstimates/SigmaIEIEFits/PlotsMCNDCoarse     --outputDir $(OUTPUTMAIN)/FinalPlotsEValid --doRatio  --evalid

singlephjet : 
	for var in $(JETFITVARS) ; do \
	    #python RunSinglePhotonFit.py --fitPath /afs/cern.ch/work/j/jkunkle/public/CMS/Wgamgam/Output/LepLepGammaNoPhID_2015_10_01/ --samplesConf Modules/JetFakeFit.py --fileName tree.root --treeName ggNtuplizer/EventTree   --xsFile cross_sections/wgamgam.py  --lumi 19400 --channel muzpeak_eff_medium --ptbins $(SINGLEPTBINS) --outputDir $(OUTPUTMAIN) --fitvar $$var; \
	done
