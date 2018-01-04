import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.VarParsing as VarParsing
import re

process = cms.Process("UMDNTuple")

# setup 'analysis'  options
opt = VarParsing.VarParsing ('analysis')

opt.register('isMC', -1, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, 'Flag indicating if the input samples are from MC (1) or from the detector (0).')
opt.register('nEvents', 1000, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, 'Number of events to analyze')

#input files. Can be changed on the command line with the option inputFiles=...
opt.inputFiles = [
    #'file:/data/users/jkunkle/Samples/aQGC_WWW_SingleLepton_LO/Job_0000/MakeMINIAOD/aQGC_WWW_SingleLepton_LO_MINIAOD.root',
    #'file:/data/users/jkunkle/Samples/WGamma/02FE572F-88DA-E611-8CAB-001E67792884.root',
    'file:/data/users/jkunkle/Samples/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAOD/08F5FD50-23BC-E611-A4C2-00259073E3DA.root',
    #'root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/004A7893-A990-E611-B29F-002590E7DE36.root'
    #'root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleElectron/MINIAOD/03Feb2017-v1/50000/004A75AB-B2EA-E611-B000-24BE05CEFDF1.root',
]


#default number of exvents
opt.nEvents = 1000

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
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

#------------------------------------
#Condition DB tag
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
dataGlobalTag = '80X_dataRun2_2016SeptRepro_v7'
#mcGlobalTag = '80X_mcRun2_asymptotic_2016_miniAODv2_v3'
#mcGlobalTag = '80X_mcRun2_asymptotic_2016_TrancheIV_v6'
mcGlobalTag= '80X_mcRun2_asymptotic_2016_TrancheIV_v8'

if opt.isMC == 1:
  process.GlobalTag = GlobalTag(process.GlobalTag, mcGlobalTag, '')
else:
  process.GlobalTag = GlobalTag(process.GlobalTag, dataGlobalTag, '')

process.source = cms.Source("PoolSource",
                            fileNames =  cms.untracked.vstring(opt.inputFiles))

#------------------------------------

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(opt.nEvents))
#process.source.skipEvents = cms.untracked.uint32(1000)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck') 

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('ntuple.root' )
)

# try to determine if its data or MC based on the name
# otherwise request the user to provide isMC=
if opt.isMC < 0 and len(process.source.fileNames) > 0:
  if re.match(r'.*/(MINI)?AODSIM/.*', process.source.fileNames[0]):
    print "MC dataset detected."
    opt.isMC = 1
  elif re.match(r'.*/(MINI)?AOD/.*', process.source.fileNames[0]):
    print "Real data dataset detected."
    opt.isMC = 0

if opt.isMC < 0:
  raise Exception("Failed to detect data type. Data type need to be specify with the isMC cmsRun command line option")

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

#eg_corr_phot_file = "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Moriond17_23Jan_ele"
#eg_corr_el_file   = "EgammaAnalysis/ElectronTools/data/ScalesSmearings/Moriond17_23Jan_ele"
eg_corr_phot_file = "EgammaAnalysis/ElectronTools/data/ScalesSmearings/80X_ichepV2_2016_pho"
eg_corr_el_file   = "EgammaAnalysis/ElectronTools/data/ScalesSmearings/80X_ichepV1_2016_ele"

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
                                                #electrons = cms.InputTag('selectedElectrons'),
                                                #gbrForestName = cms.vstring('electron_eb_ECALTRK_lowpt', 
                                                #                    'electron_eb_ECALTRK',
                                                #                    'electron_ee_ECALTRK_lowpt', 
                                                #                    'electron_ee_ECALTRK',
                                                #                    'electron_eb_ECALTRK_lowpt_var', 
                                                #                    'electron_eb_ECALTRK_var',
                                                #                    'electron_ee_ECALTRK_lowpt_var', 
                                                #                    'electron_ee_ECALTRK_var'
                                                #                   ),
                                                gbrForestName = cms.string("gedelectron_p4combination_25ns"),
                                                #gbrForestName = cms.vstring("GEDelectron_EBCorrection_80X_EGM_v4"),
                                                #gbrForestName = cms.vstring(""),
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

#--------------------------------------------
# define the triggers that we want to save
trigger_map = cms.untracked.vstring( 
    # Muon triggers
    '0:HLT_Mu8',
    '1:HLT_Mu17',
    '2:HLT_Mu20',
    '3:HLT_Mu24',
    '4:HLT_Mu27',
    '5:HLT_Mu34',
    '6:HLT_Mu50',
    '7:HLT_Mu55',
    '8:HLT_Mu300',
    '9:HLT_Mu350',
    '10:HLT_Mu24_eta2p1',
    '11:HLT_Mu45_eta2p1',
    '12:HLT_Mu50_eta2p1',
    '13:HLT_Mu8_TrkIsoVVL',
    '14:HLT_Mu17_TrkIsoVVL',
    '15:HLT_Mu24_TrkIsoVVL',
    '16:HLT_Mu34_TrkIsoVVL',
    '17:HLT_TkMu20',
    '18:HLT_TkMu27',
    '19:HLT_TkMu24_eta2p1',
    '20:HLT_IsoMu18',
    '21:HLT_IsoMu20',
    '22:HLT_IsoMu22',
    '23:HLT_IsoMu24',
    '24:HLT_IsoMu27',
    '25:HLT_IsoMu17_eta2p1',
    '26:HLT_IsoMu20_eta2p1',
    '27:HLT_IsoMu24_eta2p1',
    '28:HLT_IsoTkMu18',
    '29:HLT_IsoTkMu20',
    '30:HLT_IsoTkMu22',
    '31:HLT_IsoTkMu24',
    '32:HLT_IsoTkMu27',
    '33:HLT_IsoTkMu20_eta2p1',
    '34:HLT_IsoTkMu24_eta2p1',
    '35:HLT_Mu16_eta2p1_CaloMET30',
    '36:HLT_IsoMu16_eta2p1_CaloMET30',
    # Electron triggers
    '50:HLT_Ele22_eta2p1_WPLoose_Gsf',
    '51:HLT_Ele22_eta2p1_WPTight_Gsf',
    '52:HLT_Ele23_WPLoose_Gsf',
    '53:HLT_Ele24_eta2p1_WPLoose_Gsf',
    '54:HLT_Ele25_WPTight_Gsf',
    '55:HLT_Ele25_eta2p1_WPLoose_Gsf',
    '56:HLT_Ele25_eta2p1_WPTight_Gsf',
    '57:HLT_Ele27_WPLoose_Gsf',
    '58:HLT_Ele27_WPTight_Gsf',
    '59:HLT_Ele27_eta2p1_WPLoose_Gsf',
    '60:HLT_Ele27_eta2p1_WPTight_Gsf',
    '61:HLT_Ele32_eta2p1_WPLoose_Gsf',
    '62:HLT_Ele32_eta2p1_WPTight_Gsf',
    '63:HLT_Ele35_WPLoose_Gsf',
    '64:HLT_Ele45_WPLoose_Gsf',
    '65:HLT_Ele105_CaloIdVT_GsfTrkIdT',
    '66:HLT_Ele115_CaloIdVT_GsfTrkIdT',
    '67:HLT_Ele12_CaloIdL_TrackIdL_IsoVL',
    '68:HLT_Ele17_CaloIdL_GsfTrkIdVL',
    '69:HLT_Ele17_CaloIdL_TrackIdL_IsoVL',
    '70:HLT_Ele23_CaloIdL_TrackIdL_IsoVL',
    # Photon triggers
    '100:HLT_Photon250_NoHE',
    '101:HLT_Photon300_NoHE',
    '102:HLT_Photon22',
    '103:HLT_Photon30',
    '104:HLT_Photon36',
    '105:HLT_Photon50',
    '106:HLT_Photon75',
    '107:HLT_Photon90',
    '108:HLT_Photon120',
    '109:HLT_Photon175',
    '110:HLT_Photon500',
    '111:HLT_Photon600',
    '112:HLT_Photon165_HE10',
    '113:HLT_Photon22_R9Id90_HE10_IsoM',
    '114:HLT_Photon30_R9Id90_HE10_IsoM',
    '115:HLT_Photon36_R9Id90_HE10_IsoM',
    '116:HLT_Photon50_R9Id90_HE10_IsoM',
    '117:HLT_Photon75_R9Id90_HE10_IsoM',
    '118:HLT_Photon90_R9Id90_HE10_IsoM',
    '119:HLT_Photon120_R9Id90_HE10_IsoM',
    '120:HLT_Photon165_R9Id90_HE10_IsoM',
    '121:HLT_Photon22_R9Id90_HE10_Iso40_EBOnly',
    '122:HLT_Photon36_R9Id90_HE10_Iso40_EBOnly',
    '123:HLT_Photon50_R9Id90_HE10_Iso40_EBOnly',
    '124:HLT_Photon75_R9Id90_HE10_Iso40_EBOnly',
    '125:HLT_Photon90_R9Id90_HE10_Iso40_EBOnly',
    '126:HLT_Photon120_R9Id90_HE10_Iso40_EBOnly',
    #DiMuon triggers
    '150:HLT_Mu17_Mu8',
    '151:HLT_Mu17_Mu8_DZ',
    '152:HLT_Mu17_Mu8_SameSign_DZ',
    '153:HLT_Mu20_Mu10',
    '154:HLT_Mu20_Mu10_DZ',
    '155:HLT_Mu20_Mu10_SameSign_DZ',
    '156:HLT_Mu17_TkMu8_DZ',
    '157:HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',
    '158:HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
    '159:HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL',
    '160:HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
    '161:HLT_Mu27_TkMu8',
    '162:HLT_Mu30_TkMu11',
    '163:HLT_Mu40_TkMu11',
    '164:HLT_DoubleIsoMu17_eta2p1',
    '165:HLT_DoubleIsoMu17_eta2p1_noDzCut',
    #DiElectron triggers
    '200:HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf',
    '201:HLT_DoubleEle25_CaloIdL_GsfTrkIdVL',
    '202:HLT_DoubleEle33_CaloIdL',
    '203:HLT_DoubleEle33_CaloIdL_MW',
    '204:HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_MW',
    '205:HLT_DoubleEle33_CaloIdL_GsfTrkIdVL',
    '206:HLT_DoubleEle37_Ele27_CaloIdL_GsfTrkIdVL',
    '207:HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
    '208:HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
    '209:HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL',
    '210:HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL',
    '211:HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL',
    # muon + egamma triggers
    '212:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',
    '213:HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL',
    '214:HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL',
    '215:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
    '216:HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
    '217:HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL',
    '218:HLT_Mu37_Ele27_CaloIdL_GsfTrkIdVL',
    '219:HLT_Mu27_Ele37_CaloIdL_GsfTrkIdVL',
    '220:HLT_Mu17_Photon30_CaloIdL_L1ISO',
    #DiPhoton triggers
    '250:HLT_DoublePhoton40',
    '251:HLT_DoublePhoton50',
    '252:HLT_DoublePhoton60',
    '253:HLT_DoublePhoton85',
    '254:HLT_Photon26_R9Id85_OR_CaloId24b40e_Iso50T80L_Photon16_AND_HE10_R9Id65_Eta2_Mass60',
    '255:HLT_Photon36_R9Id85_OR_CaloId24b40e_Iso50T80L_Photon22_AND_HE10_R9Id65_Eta2_Mass15',
    '256:HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90',
    '257:HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelSeedMatch_Mass70',
    '258:HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55',
    '259:HLT_Diphoton30_18_Solid_R9Id_AND_IsoCaloId_AND_HE_R9Id_Mass55',
    '260:HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95',
    '261:HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55',
    '262:HLT_Photon42_R9Id85_OR_CaloId24b40e_Iso50T80L_Photon25_AND_HE10_R9Id65_Eta2_Mass15',
    ) 


process.UMDNTuple = cms.EDAnalyzer("UMDNTuple",
    electronTag = cms.untracked.InputTag('slimmedElectrons'),
    electronCalibTag = cms.untracked.InputTag('calibratedPatElectrons'),
        elecIdVeryLooseTag = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto"),
        elecIdLooseTag     = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose"),
        elecIdMediumTag    = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium"),
        elecIdTightTag     = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight"),
        elecIdHLTTag       = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronHLTPreselection-Summer16-V1"),
        elecIdHEEPTag      = cms.untracked.InputTag("egmGsfElectronIDs:heepElectronID-HEEPV70"),
    muonTag     = cms.untracked.InputTag('slimmedMuons'),
    photonTag   = cms.untracked.InputTag('slimmedPhotons'),
    photonCalibTag   = cms.untracked.InputTag('calibratedPatPhotons'),
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
    triggerObjTag = cms.untracked.InputTag('selectedPatTrigger'),
    triggerMap = trigger_map,

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
    isMC = cms.untracked.int32( opt.isMC ),

    prefix_el   = cms.untracked.string("el"),
    prefix_mu   = cms.untracked.string("mu"),
    prefix_ph   = cms.untracked.string("ph"),
    prefix_jet  = cms.untracked.string("jet"),
    prefix_fjet = cms.untracked.string("fjet"),
    prefix_trig = cms.untracked.string("passTrig"),
    prefix_gen  = cms.untracked.string("gen"),
    prefix_met  = cms.untracked.string("met"),
                                   
    electronMinPt = cms.untracked.double( 10 ),
    muonMinPt = cms.untracked.double( 10 ),
    photonMinPt = cms.untracked.double( 20 ),
    jetMinPt = cms.untracked.double( 30 ),
    fjetMinPt = cms.untracked.double( 200 ),
    genMinPt = cms.untracked.double( 5 ),


)
    

process.p = cms.Path()

#process.p += process.selectedElectrons
process.p += process.calibratedPatPhotons
process.p += process.calibratedPatElectrons
process.p += process.photonIDValueMapProducer
process.p += process.egmGsfElectronIDSequence
process.p += process.egmPhotonIDSequence

process.p += process.UMDNTuple

