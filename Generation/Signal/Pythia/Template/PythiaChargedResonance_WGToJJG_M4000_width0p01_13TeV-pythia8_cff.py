import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            "37:onMode = off", 
            "37:addChannel = 1 0.00001 101 24 22", 
            "37:onIfMatch = 24 22", 
            "37:m0 = 4000", 
            "37:doForceWidth = on", 
            "37:mWidth = 0.400000", 
            "24:onMode = off", 
            "24:onIfAny = 1 2 3 4 5", 
            "Higgs:useBSM = on", 
            "HiggsBSM:ffbar2H+- = on"),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)
