import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.VarParsing as VarParsing
import re

process = cms.Process("UMDNTuple")

# setup 'analysis'  options
opt = VarParsing.VarParsing ('analysis')
# Addition options.
# Note: if you add an option, update the code which write the values 
# in the configuration dump, you can find at the end of this file.
opt.register('minRun', 1, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, 'Gives an indication on the minimum run number included in the input samples.')
opt.register('maxRun', 999999, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, 'Gives an indication on the maximum run number include in the input samples.')
opt.register('prodEra', '', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, 'Production run era. Label used to identify a run period whose data are processed together.')
opt.register('recoTag', '', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, 'Tag of the recontruction.')
opt.register('dataTier', '', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, 'Data tier of input dataset, typically AOD, AODSIM, MINIAOD or MINIAODSIM')
opt.register('isMC',    -1, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, 'Flag indicating if the input samples are from MC (1) or from the detector (0).')
opt.register('makeEdm', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, 'Switch for EDM output production. Use 0 (default) to disable it, 1 to enable it.')

#input files. Can be changed on the command line with the option inputFiles=...
opt.inputFiles = [
    #'file:/data/users/jkunkle/Samples/aQGC_WWW_SingleLepton_LO/Job_0000/MakeMINIAOD/aQGC_WWW_SingleLepton_LO_MINIAOD.root',
    #'file:/data/users/jkunkle/Samples/WGamma/02FE572F-88DA-E611-8CAB-001E67792884.root',
    'file:/data/users/jkunkle/Samples/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAOD/08F5FD50-23BC-E611-A4C2-00259073E3DA.root',
]


#max number of events. #input files. Can be changed on the command line with the option maxEvents=...
opt.maxEvents = 1000

opt.parseArguments()



#-----------------------------------------------------
# Configure message logger
#-----------------------------------------------------
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
#process.MessageLogger.suppressWarning = cms.untracked.vstring('ecalLaserCorrFilter','manystripclus53X','toomanystripclus53X')
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
#process.options.allowUnscheduled = cms.untracked.bool(True)
#-----------------------------------------------------

# Load the standard set of configuration modules
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
#process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi");
#process.load("Geometry.CaloEventSetup.CaloGeometry_cfi");
#process.load("Geometry.CaloEventSetup.CaloTopology_cfi");
# need the first one?
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

#------------------------------------
#Condition DB tag
dataGlobalTag = '80X_dataRun2_2016SeptRepro_v4'
#mcGlobalTag = '80X_mcRun2_asymptotic_2016_miniAODv2_v3'
mcGlobalTag = '80X_mcRun2_asymptotic_2016_TrancheIV_v6'
triggerMenu = '2016'
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag

if opt.isMC == 1:
  process.GlobalTag = GlobalTag(process.GlobalTag, mcGlobalTag, '')
else:
  process.GlobalTag = GlobalTag(process.GlobalTag, dataGlobalTag, '')

process.source = cms.Source("PoolSource",
                            fileNames =  cms.untracked.vstring(opt.inputFiles))

#------------------------------------

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(opt.maxEvents))
#process.source.skipEvents = cms.untracked.uint32(381000)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck') 

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('ntuple.root' )
)

if opt.isMC < 0 and len(process.source.fileNames) > 0:
  if re.match(r'.*/(MINI)?AODSIM/.*', process.source.fileNames[0]):
    print "MC dataset detected."
    opt.isMC = 1
  elif re.match(r'.*/(MINI)?AOD/.*', process.source.fileNames[0]):
    print "Real data dataset detected."
    opt.isMC = 0
  #endif
#endif

if opt.isMC < 0:
  raise Exception("Failed to detect data type. Data type need to be specify with the isMC cmsRun command line option")
#endif


reapply_jec = False
eg_corr = True
eg_corr_phot_file = "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Moriond17_23Jan_ele"
eg_corr_el_file   = "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Moriond17_23Jan_ele"

include_ak08 = False #switch to include anti-kt R=0.8 jets. ak(a) fatjet
mcGlobalTag = '92X_upgrade2017_TSG_For90XSamples_V1'
eg_corr = False


# Photon and electron correction
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
  calibratedPatElectrons = cms.PSet(
      initialSeed = cms.untracked.uint32(757132),
      engineName = cms.untracked.string('TRandom3')
  ),
  calibratedPatPhotons = cms.PSet(
      initialSeed = cms.untracked.uint32(1294),
      engineName = cms.untracked.string('TRandom3')
  ),
)

eg_corr_phot_file = "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Moriond17_74x_pho"
eg_corr_el_file   = "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Moriond17_23Jan_ele"

# copied from  EgammaAnalysis/ElectronTools/python/calibratedPatPhotonsRun2_cfi.py:
process.calibratedPatPhotons = cms.EDProducer("CalibratedPatPhotonProducerRun2",
                                              # input collections
                                              photons = cms.InputTag('slimmedPhotons'),# data or MC corrections
                                              # if isMC is false, data corrections are applied
                                              isMC = cms.bool(opt.isMC != 0),
                                              # set to True to get special "fake" smearing for synchronization. Use JUST in case of synchronization
                                              isSynchronization = cms.bool(False),
                                              correctionFile = cms.string(eg_corr_phot_file),
                                              recHitCollectionEB = cms.InputTag('reducedEgamma:reducedEBRecHits'),
                                              recHitCollectionEE = cms.InputTag('reducedEgamma:reducedEERecHits'),
                                              )

#copied from  EgammaAnalysis/ElectronTools/python/calibratedPatElectronsRun2_cfi.py'
process.calibratedPatElectrons = cms.EDProducer("CalibratedPatElectronProducerRun2", 
                                                # input collections
                                                electrons = cms.InputTag('slimmedElectrons'),
                                        #gbrForestName = cms.vstring('electron_eb_ECALTRK_lowpt', 'electron_eb_ECALTRK',
                                        #                            'electron_ee_ECALTRK_lowpt', 'electron_ee_ECALTRK',
                                        #                            'electron_eb_ECALTRK_lowpt_var', 'electron_eb_ECALTRK_var',
                                        #                            'electron_ee_ECALTRK_lowpt_var', 'electron_ee_ECALTRK_var'),
                                                #gbrForestName = cms.vstring("gedelectron_p4combination_25ns"),
                                                gbrForestName = cms.vstring("GEDelectron_EBCorrection_80X_EGM_v4"),
                                                # data or MC corrections
                                                # if isMC is false, data corrections are applied
                                                isMC = cms.bool(opt.isMC != 0),
                                                # set to True to get special "fake" smearing for synchronization. Use JUST in case of synchronization
                                                isSynchronization = cms.bool(False),
                                                correctionFile = cms.string(eg_corr_el_file),
                                                recHitCollectionEB = cms.InputTag('reducedEgamma:reducedEBRecHits'),
                                                recHitCollectionEE = cms.InputTag('reducedEgamma:reducedEERecHits'),
                                                )
#--------------------------------------------

#from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
#process.load('Configuration.StandardSequences.MagneticField_38T_cff')

##default configuration for miniAOD reprocessing, change the isData flag to run on data
##for a full met computation, remove the pfCandColl input
#runMetCorAndUncFromMiniAOD(process,
#    isData = not opt.isMC,
#)

#--------------------------------------------
# Electron and photon VID
#--------------------------------------------
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
switchOnVIDPhotonIdProducer(process, DataFormat.MiniAOD)

# define which IDs we want to produce
my_eleid_modules = [
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronHLTPreselecition_Summer16_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV70_cff',
        ]

#add them to the VID producer
for idmod in my_eleid_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

setupAllVIDIdsInModule(process,'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Spring16_V2p2_cff',setupVIDPhotonSelection)
#--------------------------------------------

#electronSrc = "calibratedPatElectrons"
#photonSrc   = "calibratedPatPhotons"
process.UMDNTuple = cms.EDAnalyzer("UMDNTuple",
    electronTag = cms.untracked.InputTag('slimmedElectrons'),
        elecIdVeryLooseTag = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto"),
        elecIdLooseTag     = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose"),
        elecIdMediumTag    = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium"),
        elecIdTightTag     = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight"),
        elecIdHLTTag       = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronHLTPreselection-Summer16-V1"),
        elecIdHEEPTag      = cms.untracked.InputTag("egmGsfElectronIDs:heepElectronID-HEEPV70"),
    muonTag     = cms.untracked.InputTag('slimmedMuons'),
    photonTag   = cms.untracked.InputTag('slimmedPhotons'),
        phoChIsoTag    = cms.untracked.InputTag("photonIDValueMapProducer:phoChargedIsolation"),
        phoNeuIsoTag   = cms.untracked.InputTag("photonIDValueMapProducer:phoNeutralHadronIsolation"),
        phoPhoIsoTag   = cms.untracked.InputTag("photonIDValueMapProducer:phoPhotonIsolation"),
        phoIdLooseTag  = cms.untracked.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-loose"),
        phoIdMediumTag = cms.untracked.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-medium"),
        phoIdTightTag  = cms.untracked.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-tight"),
    jetTag     = cms.untracked.InputTag('slimmedJets'),
    fatjetTag     = cms.untracked.InputTag('slimmedJetsAK8'),
    metTag     = cms.untracked.InputTag('slimmedMETs'),
    triggerTag  = cms.untracked.InputTag('TriggerResults', '', 'HLT'), 
    beamSpotTag = cms.untracked.InputTag('offlineBeamSpot'),
    conversionsTag = cms.untracked.InputTag('reducedEgamma', 'reducedConversions' ),
    #conversionsTag = cms.untracked.InputTag('allConversions' ),
    verticesTag  = cms.untracked.InputTag('offlineSlimmedPrimaryVertices'),
    rhoTag  = cms.untracked.InputTag('fixedGridRhoFastjetAll'),
    puTag   = cms.untracked.InputTag('slimmedAddPileupInfo'),
    lheEventTag  = cms.untracked.InputTag('externalLHEProducer'),
    lheRunTag  = cms.untracked.InputTag('externalLHEProducer'),
    generatorTag = cms.untracked.InputTag('generator'),
    genParticleTag = cms.untracked.InputTag('prunedGenParticles'),

    electronDetailLevel = cms.untracked.int32( 1 ),
    photonDetailLevel = cms.untracked.int32( 1 ),
    muonDetailLevel = cms.untracked.int32( 1 ),
    jetDetailLevel = cms.untracked.int32( 1 ),

                                   


)
    

process.p = cms.Path()

process.p += process.calibratedPatPhotons
process.p += process.calibratedPatElectrons
process.p += process.photonIDValueMapProducer
process.p += process.egmGsfElectronIDSequence
process.p += process.egmPhotonIDSequence

process.p += process.UMDNTuple

