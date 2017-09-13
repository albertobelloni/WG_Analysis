#include "RunAnalysis.h"

#include <bitset>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <boost/foreach.hpp>
#include <boost/algorithm/string.hpp>
#include <sys/types.h>
#include <sys/stat.h>
#include <math.h>
#include <stdlib.h>
#include <assert.h>

#include "BranchDefs.h"
#include "BranchInit.h"

#include "Util.h"

#include "TFile.h"

int main(int argc, char **argv)
{

    //TH1::AddDirectory(kFALSE);
    CmdOptions options = ParseOptions( argc, argv );

    // Parse the text file and form the configuration object
    AnaConfig ana_config = ParseConfig( options.config_file, options );
    std::cout << "Configured " << ana_config.size() << " analysis modules " << std::endl;

    RunModule runmod;
    ana_config.Run(runmod, options);

    std::cout << "^_^ Finished ^_^" << std::endl;


}

void RunModule::initialize( TChain * chain, TTree * outtree, TFile *outfile,
                            const CmdOptions & options, std::vector<ModuleConfig> &configs ) {


    std::cout << "FIX PU weighting" << std::endl;
    assert( false );

    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );
    
    // *************************
    // Set defaults for added output variables
    // *************************
    OUT::el_n                                                   = 0;
    OUT::mu_n                                                   = 0;
    OUT::ph_n                                                   = 0;
    OUT::jet_n                                                  = 0;
    OUT::jetAK08_n                                                  = 0;
    OUT::vtx_n                                                  = 0;
    OUT::trueph_n                                               = 0;
    OUT::truephIPFS_n                                           = 0;
    OUT::truelep_n                                              = 0;
    OUT::el_pt                                                  = 0;
    OUT::el_eta                                                 = 0;
    OUT::el_sceta                                               = 0;
    OUT::el_phi                                                 = 0;
    OUT::el_e                                                   = 0;
    //OUT::el_d0pv                                                = 0;
    //OUT::el_z0pv                                                = 0;
    //OUT::el_sigmaIEIE                                           = 0;
    //OUT::el_sigmaIEIEFull5x5                                    = 0;
    //OUT::el_charge                                              = 0;
    //OUT::el_ooEmooP                                             = 0;
    //OUT::el_passConvVeto                                        = 0;
    //OUT::el_chHadIso                                            = 0;
    //OUT::el_neuHadIso                                           = 0;
    //OUT::el_phoIso                                              = 0;
    //OUT::el_chHadIsoPuCorr                                      = 0;
    //OUT::el_rawIso                                              = 0;
    //OUT::el_dbIso                                               = 0;
    //OUT::el_rhoIso                                              = 0;
    OUT::el_passTight                                           = 0;
    OUT::el_passMedium                                          = 0;
    OUT::el_passLoose                                           = 0;
    OUT::el_passVeryLoose                                       = 0;
    OUT::el_passVIDTight                                        = 0;
    OUT::el_passVIDMedium                                       = 0;
    OUT::el_passVIDLoose                                        = 0;
    OUT::el_passVIDVeryLoose                                    = 0;
    OUT::el_passVIDHLT                                          = 0;
    OUT::el_passVIDHEEP                                         = 0;

    OUT::mu_pt                                                  = 0;
    OUT::mu_eta                                                 = 0;
    OUT::mu_phi                                                 = 0;
    OUT::mu_e                                                   = 0;
    //OUT::mu_isGlobal                                            = 0;
    //OUT::mu_isPF                                                = 0;
    //OUT::mu_chi2                                                = 0;
    //OUT::mu_nHits                                               = 0;
    //OUT::mu_nMuStations                                         = 0;
    //OUT::mu_nPixHits                                            = 0;
    //OUT::mu_nTrkLayers                                          = 0;
    OUT::mu_d0                                                  = 0;
    OUT::mu_z0                                                  = 0;
    //OUT::mu_pfIso_ch                                            = 0;
    //OUT::mu_pfIso_nh                                            = 0;
    //OUT::mu_pfIso_pho                                           = 0;
    //OUT::mu_rhoIso                                              = 0;
    OUT::mu_pfIso_db                                            = 0;
    //OUT::mu_corrIso                                             = 0;
    //OUT::mu_trkIso                                              = 0;
    //OUT::mu_charge                                              = 0;
    //OUT::mu_triggerMatch                                        = 0;
    //OUT::mu_triggerMatchDiMu                                    = 0;
    //OUT::mu_passLoose                                           = 0;
    //OUT::mu_passCustom                                          = 0;
    OUT::mu_passTight                                           = 0;
    OUT::mu_passMedium                                          = 0;
    OUT::mu_passLoose                                           = 0;
    //OUT::mu_passTightNoIso                                    = 0;
    //OUT::mu_passTightNoD0                                     = 0;
    //OUT::mu_passTightNoIsoNoD0                                = 0;
    OUT::mu_truthMatch_mu                                          = 0;
    OUT::mu_truthMatchMinDR_mu                                          = 0;
    OUT::mu_truthMatchPt_mu                                          = 0;

    OUT::ph_pt                                                  = 0;
    OUT::ph_eta                                                 = 0;
    OUT::ph_sceta                                               = 0;
    OUT::ph_phi                                                 = 0;
    OUT::ph_scphi                                               = 0;
    OUT::ph_e                                                   = 0;
    //OUT::ph_scE                                                 = 0;
    OUT::ph_HoverE                                              = 0;
    OUT::ph_sigmaIEIE                                           = 0;
    //OUT::ph_sigmaIEIP                                           = 0;
    //OUT::ph_r9                                                  = 0;
    //OUT::ph_E3x3                                                = 0;
    //OUT::ph_E1x5                                                = 0;
    //OUT::ph_E2x5                                                = 0;
    //OUT::ph_E5x5                                                = 0;
    //OUT::ph_E2x5Max                                           = 0;
    //OUT::ph_SCetaWidth                                          = 0;
    //OUT::ph_SCphiWidth                                          = 0;
    //OUT::ph_ESEffSigmaRR                                      = 0;
    //OUT::ph_hcalIsoDR03                                       = 0;
    //OUT::ph_trkIsoHollowDR03                                  = 0;
    //OUT::ph_chgpfIsoDR02                                      = 0;
    //OUT::ph_pfChIsoWorst                                      = 0;
    OUT::ph_chIso                                               = 0;
    OUT::ph_neuIso                                              = 0;
    OUT::ph_phoIso                                              = 0;
    OUT::ph_chIsoCorr                                           = 0;
    OUT::ph_neuIsoCorr                                          = 0;
    OUT::ph_phoIsoCorr                                          = 0;
    OUT::ph_eleVeto                                             = 0;
    OUT::ph_hasPixSeed                                          = 0;
    //OUT::ph_drToTrk                                           = 0;
    OUT::ph_isConv                                              = 0;
    OUT::ph_passTight                                           = 0;
    OUT::ph_passMedium                                          = 0;
    OUT::ph_passLoose                                           = 0;
    OUT::ph_passLooseNoSIEIE                                    = 0;
    OUT::ph_passHOverELoose                                     = 0;
    OUT::ph_passHOverEMedium                                    = 0;
    OUT::ph_passHOverETight                                     = 0;
    OUT::ph_passSIEIELoose                                      = 0;
    OUT::ph_passSIEIEMedium                                     = 0;
    OUT::ph_passSIEIETight                                      = 0;
    OUT::ph_passChIsoCorrLoose                                  = 0;
    OUT::ph_passChIsoCorrMedium                                 = 0;
    OUT::ph_passChIsoCorrTight                                  = 0;
    OUT::ph_passNeuIsoCorrLoose                                 = 0;
    OUT::ph_passNeuIsoCorrMedium                                = 0;
    OUT::ph_passNeuIsoCorrTight                                 = 0;
    OUT::ph_passPhoIsoCorrLoose                                 = 0;
    OUT::ph_passPhoIsoCorrMedium                                = 0;
    OUT::ph_passPhoIsoCorrTight                                 = 0;
    OUT::ph_truthMatch_ph                                       = 0;
    OUT::ph_truthMatchMinDR_ph                                       = 0;
    OUT::ph_truthMatchPt_ph                                     = 0;
    OUT::ph_truthMatchMotherPID_ph                              = 0;
    OUT::ph_truthMatchParentage_ph                              = 0;
    OUT::ph_truthMatch_el                                       = 0;
    OUT::ph_truthMinDR_el                                      = 0;
    OUT::ph_truthMatchPt_el                                     = 0;
    OUT::ph_truthMatch_jet                                      = 0;
    OUT::ph_truthMinDR_jet                                      = 0;
    OUT::ph_truthMatchPt_jet                                    = 0;
    OUT::ph_hasSLConv                                           = 0;
    OUT::ph_pass_mva_presel                                     = 0;
    OUT::ph_mvascore                                            = 0;
    OUT::ph_IsEB                                                = 0;
    OUT::ph_IsEE                                                = 0;
    OUT::ph_passVIDTight                                        = 0;
    OUT::ph_passVIDMedium                                       = 0;
    OUT::ph_passVIDLoose                                        = 0;

    OUT::jet_pt                                                 = 0;
    OUT::jet_eta                                                = 0;
    OUT::jet_phi                                                = 0;
    OUT::jet_e                                                  = 0;
    OUT::jet_bTagCSVV2                                          = 0;
    OUT::jet_IdLoose                                            = 0;
    OUT::jet_IdTight                                            = 0;
    OUT::jet_IdTightLep                                         = 0;

    OUT::jetAK08_pt                                             = 0;
    OUT::jetAK08_eta                                            = 0;
    OUT::jetAK08_phi                                            = 0;
    OUT::jetAK08_e                                              = 0;

    OUT::met_pt                                                 = 0;
    OUT::met_phi                                                = 0;

    OUT::PassQuality                                            = 0;
    OUT::trueph_pt                                              = 0;
    OUT::trueph_eta                                             = 0;
    OUT::trueph_phi                                             = 0;
    OUT::trueph_motherPID                                       = 0;
    OUT::trueph_status                                          = 0;
    OUT::trueph_nMatchingLep                                    = 0;

    OUT::truelep_pt                                             = 0;
    OUT::truelep_eta                                            = 0;
    OUT::truelep_phi                                            = 0;
    OUT::truelep_e                                             = 0;
    OUT::truelep_motherPID                                      = 0;
    OUT::truelep_status                                         = 0;
    OUT::truelep_Id                                             = 0;

    OUT::st3Lep_n                                               = 0;

    OUT::truechlep_n                                            = 0;
    OUT::truenu_n                                               = 0;
    OUT::truelepnu_m                                            = 0;
    OUT::truelepnuph_m                                          = 0;
    OUT::truelepph_dr                                           = 0;

    OUT::isWMuDecay                                             = 0;
    OUT::isWElDecay                                             = 0;
    OUT::isWTauDecay                                            = 0;
    OUT::isWTauElDecay                                            = 0;
    OUT::isWTauMuDecay                                            = 0;
    OUT::WIDStep                                                = 0;
    //Default triggers for TrigHltPhot
    Bool_t passTrig_HLT_Photon250_NoHE                    = 0;
    Bool_t passTrig_HLT_Photon300_NoHE                    = 0;
    Bool_t passTrig_HLT_Photon22                          = 0;
    Bool_t passTrig_HLT_Photon30                          = 0;
    Bool_t passTrig_HLT_Photon36                          = 0;
    Bool_t passTrig_HLT_Photon50                          = 0;
    Bool_t passTrig_HLT_Photon75                          = 0;
    Bool_t passTrig_HLT_Photon90                          = 0;
    Bool_t passTrig_HLT_Photon120                         = 0;
    Bool_t passTrig_HLT_Photon175                         = 0;
    Bool_t passTrig_HLT_Photon500                         = 0;
    Bool_t passTrig_HLT_Photon600                         = 0;
    Bool_t passTrig_HLT_Photon165_HE10                    = 0;
    Bool_t passTrig_HLT_Photon120_R9Id90_HE10_IsoM        = 0;
    Bool_t passTrig_HLT_Photon165_R9Id90_HE10_IsoM        = 0;
    Bool_t passTrig_HLT_Photon120_R9Id90_HE10_Iso40_EBOnly;
    Bool_t passTrig_HLT_Photon135_PFMET100_JetIdCleaned   = 0;
    //Default triggers for TrigHltMu
    Bool_t passTrig_HLT_Mu8                               = 0;
    Bool_t passTrig_HLT_Mu17                              = 0;
    Bool_t passTrig_HLT_Mu20                              = 0;
    Bool_t passTrig_HLT_Mu24                              = 0;
    Bool_t passTrig_HLT_Mu27                              = 0;
    Bool_t passTrig_HLT_Mu34                              = 0;
    Bool_t passTrig_HLT_Mu50                              = 0;
    Bool_t passTrig_HLT_Mu55                              = 0;
    Bool_t passTrig_HLT_Mu300                             = 0;
    Bool_t passTrig_HLT_Mu350                             = 0;
    Bool_t passTrig_HLT_Mu24_eta2p1                       = 0;
    Bool_t passTrig_HLT_Mu45_eta2p1                       = 0;
    Bool_t passTrig_HLT_Mu50_eta2p1                       = 0;
    Bool_t passTrig_HLT_TkMu20                            = 0;
    Bool_t passTrig_HLT_TkMu27                            = 0;
    Bool_t passTrig_HLT_TkMu24_eta2p1                     = 0;
    Bool_t passTrig_HLT_IsoMu20                           = 0;
    Bool_t passTrig_HLT_IsoMu22                           = 0;
    Bool_t passTrig_HLT_IsoMu24                           = 0;
    Bool_t passTrig_HLT_IsoMu27                           = 0;
    Bool_t passTrig_HLT_IsoMu17_eta2p1                    = 0;
    Bool_t passTrig_HLT_IsoMu20_eta2p1                    = 0;
    Bool_t passTrig_HLT_IsoMu24_eta2p1                    = 0;
    Bool_t passTrig_HLT_IsoTkMu20                         = 0;
    Bool_t passTrig_HLT_IsoTkMu22                         = 0;
    Bool_t passTrig_HLT_IsoTkMu24                         = 0;
    Bool_t passTrig_HLT_IsoTkMu27                         = 0;
    Bool_t passTrig_HLT_IsoTkMu20_eta2p1                  = 0;
    Bool_t passTrig_HLT_IsoTkMu24_eta2p1                  = 0;
    //Default triggers for TrigHltDiPhot
    //Default triggers for TrigHlt
    //Default triggers for TrigHltElMu
    Bool_t passTrig_HLT_Mu17_Photon30_CaloIdL_L1ISO       = 0;
    //Default triggers for TrigHltEl
    Bool_t passTrig_HLT_Ele22_eta2p1_WPLoose_Gsf          = 0;
    Bool_t passTrig_HLT_Ele22_eta2p1_WPTight_Gsf          = 0;
    Bool_t passTrig_HLT_Ele23_WPLoose_Gsf                 = 0;
    Bool_t passTrig_HLT_Ele24_eta2p1_WPLoose_Gsf          = 0;
    Bool_t passTrig_HLT_Ele25_WPTight_Gsf                 = 0;
    Bool_t passTrig_HLT_Ele25_eta2p1_WPLoose_Gsf          = 0;
    Bool_t passTrig_HLT_Ele25_eta2p1_WPTight_Gsf          = 0;
    Bool_t passTrig_HLT_Ele27_WPTight_Gsf                 = 0;
    Bool_t passTrig_HLT_Ele27_eta2p1_WPLoose_Gsf          = 0;
    Bool_t passTrig_HLT_Ele27_eta2p1_WPTight_Gsf          = 0;
    Bool_t passTrig_HLT_Ele32_eta2p1_WPLoose_Gsf          = 0;
    Bool_t passTrig_HLT_Ele32_eta2p1_WPTight_Gsf          = 0;
    Bool_t passTrig_HLT_Ele105_CaloIdVT_GsfTrkIdT         = 0;
    Bool_t passTrig_HLT_Ele115_CaloIdVT_GsfTrkIdT         = 0;

    //Default triggers for TrigHltDiMu
    Bool_t passTrig_HLT_Mu17_Mu8                          = 0;
    Bool_t passTrig_HLT_Mu17_Mu8_DZ                       = 0;
    Bool_t passTrig_HLT_Mu20_Mu10                         = 0;
    Bool_t passTrig_HLT_Mu20_Mu10_DZ                      = 0;
    Bool_t passTrig_HLT_Mu27_TkMu8                        = 0;
    Bool_t passTrig_HLT_Mu30_TkMu11                       = 0;
    Bool_t passTrig_HLT_Mu40_TkMu11                       = 0;

    OUT::NLOWeight                                        = 0;
    OUT::PUWeight                                         = 0;
    OUT::PUWeightUP5                                      = 0;
    OUT::PUWeightUP10                                     = 0;
    OUT::PUWeightDN5                                      = 0;
    OUT::PUWeightDN10                                     = 0;


    // *************************
    // Declare Branches
    // *************************
    outtree->Branch("el_n"                      , &OUT::el_n  , "el_n/I"          );
    outtree->Branch("mu_n"                      , &OUT::mu_n  , "mu_n/I"          );
    outtree->Branch("ph_n"                      , &OUT::ph_n , "ph_n/I"           );
    outtree->Branch("jet_n"                     , &OUT::jet_n , "jet_n/I"         );
    outtree->Branch("jetAK08_n"                 , &OUT::jet_n , "jetAK08_n/I"         );
    outtree->Branch("vtx_n"                     , &OUT::vtx_n   , "vtx_n/I"       );
    outtree->Branch("trueph_n"                  , &OUT::trueph_n, "trueph_n/I"         );
    outtree->Branch("truelep_n"                 , &OUT::truelep_n, "truelep_n/I"         );
    outtree->Branch("truephIPFS_n"              , &OUT::truephIPFS_n, "truephIPFS_n/I"         );

    outtree->Branch("el_pt"                     , &OUT::el_pt                     );
    outtree->Branch("el_eta"                    , &OUT::el_eta                    );
    outtree->Branch("el_sceta"                  , &OUT::el_sceta                  );
    outtree->Branch("el_phi"                    , &OUT::el_phi                    );
    outtree->Branch("el_e"                      , &OUT::el_e                      );
    //outtree->Branch("el_d0pv"                   , &OUT::el_d0pv                   );
    //outtree->Branch("el_z0pv"                   , &OUT::el_z0pv                   );
    //outtree->Branch("el_sigmaIEIE"              , &OUT::el_sigmaIEIE              );
    //outtree->Branch("el_sigmaIEIEFull5x5"       , &OUT::el_sigmaIEIEFull5x5       );
    //outtree->Branch("el_charge"                 , &OUT::el_charge                 );
    //outtree->Branch("el_ooEmooP"                , &OUT::el_ooEmooP                );
    //outtree->Branch("el_passConvVeto"           , &OUT::el_passConvVeto           );
    //outtree->Branch("el_chHadIso"               , &OUT::el_chHadIso               );
    //outtree->Branch("el_neuHadIso"              , &OUT::el_neuHadIso              );
    //outtree->Branch("el_phoIso"                 , &OUT::el_phoIso                 );
    //outtree->Branch("el_chHadIsoPuCorr"         , &OUT::el_chHadIsoPuCorr         );
    //outtree->Branch("el_rawIso"                 , &OUT::el_rawIso                 );
    //outtree->Branch("el_dbIso"                  , &OUT::el_dbIso                  );
    //outtree->Branch("el_rhoIso"                 , &OUT::el_rhoIso                 );
    outtree->Branch("el_passTight"              , &OUT::el_passTight              );
    outtree->Branch("el_passMedium"             , &OUT::el_passMedium             );
    outtree->Branch("el_passLoose"              , &OUT::el_passLoose              );
    outtree->Branch("el_passVeryLoose"          , &OUT::el_passVeryLoose          );
    outtree->Branch("el_passVIDTight"           , &OUT::el_passVIDTight           );
    outtree->Branch("el_passVIDMedium"          , &OUT::el_passVIDMedium          );
    outtree->Branch("el_passVIDLoose"           , &OUT::el_passVIDLoose           );
    outtree->Branch("el_passVIDVeryLoose"       , &OUT::el_passVIDVeryLoose       );
    outtree->Branch("el_passVIDHLT"             , &OUT::el_passVIDHLT       );
    outtree->Branch("el_passVIDHEEP"            , &OUT::el_passVIDHEEP       );
    //outtree->Branch("el_mva_trig"               , &OUT::el_mva_trig               );
    //outtree->Branch("el_mva_nontrig"            , &OUT::el_mva_nontrig            );
    //outtree->Branch("el_passTightTrig"          , &OUT::el_passTightTrig          );
    //outtree->Branch("el_passMvaTrig"            , &OUT::el_passMvaTrig            );
    //outtree->Branch("el_passMvaNonTrig"         , &OUT::el_passMvaNonTrig         );
    //outtree->Branch("el_passMvaTrigNoIso"       , &OUT::el_passMvaTrigNoIso       );
    //outtree->Branch("el_passMvaNonTrigNoIso"    , &OUT::el_passMvaNonTrigNoIso    );
    //outtree->Branch("el_passMvaTrigOnlyIso"     , &OUT::el_passMvaTrigOnlyIso     );
    //outtree->Branch("el_passMvaNonTrigOnlyIso"  , &OUT::el_passMvaNonTrigOnlyIso  );
    outtree->Branch("el_truthMatch_el"          , &OUT::el_truthMatch_el          );
    outtree->Branch("el_truthMatchMinDR_el"     , &OUT::el_truthMatchMinDR_el          );
    outtree->Branch("el_truthMatchPt_el"        , &OUT::el_truthMatchPt_el        );
    //outtree->Branch("el_truthMatch_ph"          , &OUT::el_truthMatch_ph          );
    //outtree->Branch("el_truthMinDR_ph"          , &OUT::el_truthMinDR_ph          );
    //outtree->Branch("el_truthMatchPt_ph"        , &OUT::el_truthMatchPt_ph        );
    //outtree->Branch("el_triggerMatch"           , &OUT::el_triggerMatch           );
    //outtree->Branch("el_hasMatchedConv"         , &OUT::el_hasMatchedConv         );
    
    outtree->Branch("mu_pt"                     , &OUT::mu_pt                     );
    outtree->Branch("mu_eta"                    , &OUT::mu_eta                    );
    outtree->Branch("mu_phi"                    , &OUT::mu_phi                    );
    outtree->Branch("mu_e"                      , &OUT::mu_e                      );
    //outtree->Branch("mu_isGlobal"               , &OUT::mu_isGlobal               );
    //outtree->Branch("mu_isPF"                   , &OUT::mu_isPF                   );
    //outtree->Branch("mu_chi2"                   , &OUT::mu_chi2                   );
    //outtree->Branch("mu_nHits"                  , &OUT::mu_nHits                  );
    //outtree->Branch("mu_nMuStations"            , &OUT::mu_nMuStations            );
    //outtree->Branch("mu_nPixHits"               , &OUT::mu_nPixHits               );
    //outtree->Branch("mu_nTrkLayers"             , &OUT::mu_nTrkLayers             );
    outtree->Branch("mu_d0"                     , &OUT::mu_d0                     );
    outtree->Branch("mu_z0"                     , &OUT::mu_z0                     );
    //outtree->Branch("mu_pfIso_ch"               , &OUT::mu_pfIso_ch               );
    //outtree->Branch("mu_pfIso_nh"               , &OUT::mu_pfIso_nh               );
    //outtree->Branch("mu_pfIso_pho"              , &OUT::mu_pfIso_pho              );
    outtree->Branch("mu_pfIso_db"               , &OUT::mu_pfIso_db               );
    //outtree->Branch("mu_rhoIso"                 , &OUT::mu_rhoIso                 );
    //outtree->Branch("mu_corrIso"                , &OUT::mu_corrIso                );
    //outtree->Branch("mu_trkIso"                 , &OUT::mu_trkIso                 );
    //outtree->Branch("mu_charge"                 , &OUT::mu_charge                 );
    //outtree->Branch("mu_triggerMatch"           , &OUT::mu_triggerMatch           );
    //outtree->Branch("mu_triggerMatchDiMu"       , &OUT::mu_triggerMatchDiMu       );
    //outtree->Branch("mu_passLoose"              , &OUT::mu_passLoose              );
    //outtree->Branch("mu_passCustom"             , &OUT::mu_passCustom             );
    outtree->Branch("mu_passTight"              , &OUT::mu_passTight              );
    outtree->Branch("mu_passMedium"              , &OUT::mu_passMedium                 );
    outtree->Branch("mu_passLoose"              , &OUT::mu_passLoose                 );
    //outtree->Branch("mu_passTightNoIso"         , &OUT::mu_passTightNoIso         );
    //outtree->Branch("mu_passTightNoD0"          , &OUT::mu_passTightNoD0          );
    //outtree->Branch("mu_passTightNoIsoNoD0"     , &OUT::mu_passTightNoIsoNoD0     );
    outtree->Branch("mu_truthMatch_mu"             , &OUT::mu_truthMatch_mu             );
    outtree->Branch("mu_truthMatchMinDR_mu"             , &OUT::mu_truthMatchMinDR_mu             );
    outtree->Branch("mu_truthMatchPt_mu"             , &OUT::mu_truthMatchPt_mu             );
    
    outtree->Branch("ph_pt"                     , &OUT::ph_pt                     );
    outtree->Branch("ph_eta"                    , &OUT::ph_eta                    );
    outtree->Branch("ph_sceta"                  , &OUT::ph_sceta                  );
    outtree->Branch("ph_phi"                    , &OUT::ph_phi                    );
    outtree->Branch("ph_scphi"                  , &OUT::ph_scphi                  );
    outtree->Branch("ph_e"                      , &OUT::ph_e                      );
    outtree->Branch("ph_IsEB"                   , &OUT::ph_IsEB                   );
    outtree->Branch("ph_IsEE"                   , &OUT::ph_IsEE                   );
    //outtree->Branch("ph_scE"                    , &OUT::ph_scE                    );
    outtree->Branch("ph_HoverE"                 , &OUT::ph_HoverE                 );
    outtree->Branch("ph_sigmaIEIE"              , &OUT::ph_sigmaIEIE              );
    //outtree->Branch("ph_sigmaIEIP"              , &OUT::ph_sigmaIEIP              );
    //outtree->Branch("ph_r9"                     , &OUT::ph_r9                     );
    //outtree->Branch("ph_E3x3"                   , &OUT::ph_E3x3                   );
    //outtree->Branch("ph_E1x5"                   , &OUT::ph_E1x5                   );
    //outtree->Branch("ph_E2x5"                   , &OUT::ph_E2x5                   );
    //outtree->Branch("ph_E5x5"                   , &OUT::ph_E5x5                   );
    //outtree->Branch("ph_E2x5Max"                , &OUT::ph_E2x5Max                );
    //outtree->Branch("ph_SCetaWidth"             , &OUT::ph_SCetaWidth             );
    //outtree->Branch("ph_SCphiWidth"             , &OUT::ph_SCphiWidth             );
    //outtree->Branch("ph_ESEffSigmaRR"           , &OUT::ph_ESEffSigmaRR           );
    //outtree->Branch("ph_hcalIsoDR03"            , &OUT::ph_hcalIsoDR03            );
    //outtree->Branch("ph_trkIsoHollowDR03"       , &OUT::ph_trkIsoHollowDR03       );
    //outtree->Branch("ph_chgpfIsoDR02"           , &OUT::ph_chgpfIsoDR02           );
    //outtree->Branch("ph_pfChIsoWorst"           , &OUT::ph_pfChIsoWorst           );
    outtree->Branch("ph_chIso"                  , &OUT::ph_chIso                  );
    outtree->Branch("ph_neuIso"                 , &OUT::ph_neuIso                 );
    outtree->Branch("ph_phoIso"                 , &OUT::ph_phoIso                 );
    outtree->Branch("ph_chIsoCorr"              , &OUT::ph_chIsoCorr              );
    outtree->Branch("ph_neuIsoCorr"             , &OUT::ph_neuIsoCorr             );
    outtree->Branch("ph_phoIsoCorr"             , &OUT::ph_phoIsoCorr             );
    outtree->Branch("ph_eleVeto"                , &OUT::ph_eleVeto                );
    outtree->Branch("ph_hasPixSeed"             , &OUT::ph_hasPixSeed             );
    //outtree->Branch("ph_drToTrk"                , &OUT::ph_drToTrk                );
    //outtree->Branch("ph_isConv"                 , &OUT::ph_isConv                 );
    outtree->Branch("ph_passTight"              , &OUT::ph_passTight              );
    outtree->Branch("ph_passMedium"             , &OUT::ph_passMedium             );
    outtree->Branch("ph_passLoose"              , &OUT::ph_passLoose              );
    outtree->Branch("ph_passLooseNoSIEIE"       , &OUT::ph_passLooseNoSIEIE       );
    outtree->Branch("ph_passHOverELoose"        , &OUT::ph_passHOverELoose        );
    outtree->Branch("ph_passHOverEMedium"       , &OUT::ph_passHOverEMedium       );
    outtree->Branch("ph_passHOverETight"        , &OUT::ph_passHOverETight        );
    outtree->Branch("ph_passSIEIELoose"         , &OUT::ph_passSIEIELoose         );
    outtree->Branch("ph_passSIEIEMedium"        , &OUT::ph_passSIEIEMedium        );
    outtree->Branch("ph_passSIEIETight"         , &OUT::ph_passSIEIETight         );
    outtree->Branch("ph_passChIsoCorrLoose"     , &OUT::ph_passChIsoCorrLoose     );
    outtree->Branch("ph_passChIsoCorrMedium"    , &OUT::ph_passChIsoCorrMedium    );
    outtree->Branch("ph_passChIsoCorrTight"     , &OUT::ph_passChIsoCorrTight     );
    outtree->Branch("ph_passNeuIsoCorrLoose"    , &OUT::ph_passNeuIsoCorrLoose    );
    outtree->Branch("ph_passNeuIsoCorrMedium"   , &OUT::ph_passNeuIsoCorrMedium   );
    outtree->Branch("ph_passNeuIsoCorrTight"    , &OUT::ph_passNeuIsoCorrTight    );
    outtree->Branch("ph_passPhoIsoCorrLoose"    , &OUT::ph_passPhoIsoCorrLoose    );
    outtree->Branch("ph_passPhoIsoCorrMedium"   , &OUT::ph_passPhoIsoCorrMedium   );
    outtree->Branch("ph_passPhoIsoCorrTight"    , &OUT::ph_passPhoIsoCorrTight    );
    //outtree->Branch("ph_truthMatch_jet"          , &OUT::ph_truthMatch_jet          );
    //outtree->Branch("ph_truthMinDR_jet"          , &OUT::ph_truthMinDR_jet          );
    //outtree->Branch("ph_truthMatchPt_jet"        , &OUT::ph_truthMatchPt_jet        );
    //outtree->Branch("ph_truthMatch_el"          , &OUT::ph_truthMatch_el          );
    //outtree->Branch("ph_truthMinDR_el"          , &OUT::ph_truthMinDR_el          );
    //outtree->Branch("ph_truthMatchPt_el"        , &OUT::ph_truthMatchPt_el        );
    outtree->Branch("ph_truthMatch_ph"          , &OUT::ph_truthMatch_ph          );
    outtree->Branch("ph_truthMatchMinDR_ph"          , &OUT::ph_truthMatchMinDR_ph          );
    outtree->Branch("ph_truthMatchPt_ph"        , &OUT::ph_truthMatchPt_ph        );
    //outtree->Branch("ph_truthMatchMotherPID_ph" , &OUT::ph_truthMatchMotherPID_ph );
    //outtree->Branch("ph_truthMatchParentage_ph" , &OUT::ph_truthMatchParentage_ph );
    outtree->Branch("ph_passVIDTight"           , &OUT::ph_passVIDTight              );
    outtree->Branch("ph_passVIDMedium"          , &OUT::ph_passVIDMedium             );
    outtree->Branch("ph_passVIDLoose"           , &OUT::ph_passVIDLoose              );

   //outtree->Branch("ph_hasSLConv"              , &OUT::ph_hasSLConv              );
    //outtree->Branch("ph_pass_mva_presel"        , &OUT::ph_pass_mva_presel        );
    //outtree->Branch("ph_mvascore"               , &OUT::ph_mvascore               );
    //
    outtree->Branch("jet_pt"                    , &OUT::jet_pt                    );
    outtree->Branch("jet_eta"                   , &OUT::jet_eta                   );
    outtree->Branch("jet_phi"                   , &OUT::jet_phi                   );
    outtree->Branch("jet_e"                     , &OUT::jet_e                     );
    outtree->Branch("jet_bTagCSVV2"             , &OUT::jet_bTagCSVV2             );
    outtree->Branch("jet_IdLoose"               , &OUT::jet_IdLoose                     );
    outtree->Branch("jet_IdTight"               , &OUT::jet_IdTight                     );
    outtree->Branch("jet_IdTightLep"            , &OUT::jet_IdTightLep                     );
    //outtree->Branch("jet_NCH"                   , &OUT::jet_NCH);
    //outtree->Branch("jet_Nconstitutents"        , &OUT::jet_Nconstitutents);
    //outtree->Branch("jet_NEF"                   , &OUT::jet_NEF);
    //outtree->Branch("jet_CEF"                   , &OUT::jet_CEF);
    //outtree->Branch("jet_CHF"                   , &OUT::jet_CHF);
    //outtree->Branch("jet_NHF"                   , &OUT::jet_NHF);
    //outtree->Branch("jet_PUIDLoose"             , &OUT::jet_PUIDLoose);
    //outtree->Branch("jet_PUIDMedium"            , &OUT::jet_PUIDMedium);
    //outtree->Branch("jet_PUIDTight"             , &OUT::jet_PUIDTight);
    //outtree->Branch("jet_CSV"                   , &OUT::jet_CSV);
    
    outtree->Branch("jetAK08_pt"               , &OUT::jetAK08_pt);
    outtree->Branch("jetAK08_eta"              , &OUT::jetAK08_eta);
    outtree->Branch("jetAK08_phi"              , &OUT::jetAK08_phi);
    outtree->Branch("jetAK08_e"                , &OUT::jetAK08_e);

    outtree->Branch("met_pt"                    , &OUT::met_pt , "met_pt/F"                   );
    outtree->Branch("met_phi"                   , &OUT::met_phi, "met_phi/F"                   );

    outtree->Branch("trueph_pt"           , &OUT::trueph_pt                        );
    outtree->Branch("trueph_eta"          , &OUT::trueph_eta                       );
    outtree->Branch("trueph_phi"          , &OUT::trueph_phi                       );
    outtree->Branch("trueph_motherPID"    , &OUT::trueph_motherPID                 );
    outtree->Branch("trueph_status"       , &OUT::trueph_status                    );
    outtree->Branch("trueph_nMatchingLep" , &OUT::trueph_nMatchingLep              );

    outtree->Branch("truelep_pt"          , &OUT::truelep_pt                       );
    outtree->Branch("truelep_eta"         , &OUT::truelep_eta                      );
    outtree->Branch("truelep_phi"         , &OUT::truelep_phi                      );
    outtree->Branch("truelep_e"           , &OUT::truelep_e                        );
    outtree->Branch("truelep_motherPID"   , &OUT::truelep_motherPID                );
    outtree->Branch("truelep_status"      , &OUT::truelep_status                   );
    outtree->Branch("truelep_Id"          , &OUT::truelep_Id                       );

    outtree->Branch("st3Lep_n"            , &OUT::st3Lep_n, "st3Lep_n/I"           );

    outtree->Branch("truechlep_n"         , &OUT::truechlep_n, "truechlep_n/I"     );
    outtree->Branch("truenu_n"            , &OUT::truenu_n, "truenu_n/I"           );

    outtree->Branch("truelepnu_m"         , &OUT::truelepnu_m, "truelepnu_m/F"     );
    outtree->Branch("truelepnuph_m"       , &OUT::truelepnuph_m, "truelepnuph_m/F" );
    outtree->Branch("truelepph_dr"        , &OUT::truelepph_dr, "truelepph_dr/F"   );

    outtree->Branch("isWMuDecay"          , &OUT::isWMuDecay, "isWMuDecay/O"       );
    outtree->Branch("isWElDecay"          , &OUT::isWElDecay, "isWElDecay/O"       );
    outtree->Branch("isWTauDecay"         , &OUT::isWTauDecay, "isWTauDecay/O"     );
    outtree->Branch("isWTauElDecay"         , &OUT::isWTauElDecay, "isWTauElDecay/O"     );
    outtree->Branch("isWTauMuDecay"         , &OUT::isWTauMuDecay, "isWTauMuDecay/O"     );
    outtree->Branch("WIDStep"             , &OUT::WIDStep    , "WIDStep/I"     );

    // Use scripts/write_trigger_code_from_ntuple.py
    // to help generate the code 

 //Set trigger branches for TrigHltPhot
    outtree->Branch("passTrig_HLT_Photon250_NoHE"                    , &OUT::passTrig_HLT_Photon250_NoHE                    , "passTrig_HLT_Photon250_NoHE/O"                     );
    outtree->Branch("passTrig_HLT_Photon300_NoHE"                    , &OUT::passTrig_HLT_Photon300_NoHE                    , "passTrig_HLT_Photon300_NoHE/O"                     );
    outtree->Branch("passTrig_HLT_Photon22"                          , &OUT::passTrig_HLT_Photon22                          , "passTrig_HLT_Photon22/O"                           );
    outtree->Branch("passTrig_HLT_Photon30"                          , &OUT::passTrig_HLT_Photon30                          , "passTrig_HLT_Photon30/O"                           );
    outtree->Branch("passTrig_HLT_Photon36"                          , &OUT::passTrig_HLT_Photon36                          , "passTrig_HLT_Photon36/O"                           );
    outtree->Branch("passTrig_HLT_Photon50"                          , &OUT::passTrig_HLT_Photon50                          , "passTrig_HLT_Photon50/O"                           );
    outtree->Branch("passTrig_HLT_Photon75"                          , &OUT::passTrig_HLT_Photon75                          , "passTrig_HLT_Photon75/O"                           );
    outtree->Branch("passTrig_HLT_Photon90"                          , &OUT::passTrig_HLT_Photon90                          , "passTrig_HLT_Photon90/O"                           );
    outtree->Branch("passTrig_HLT_Photon120"                         , &OUT::passTrig_HLT_Photon120                         , "passTrig_HLT_Photon120/O"                          );
    outtree->Branch("passTrig_HLT_Photon175"                         , &OUT::passTrig_HLT_Photon175                         , "passTrig_HLT_Photon175/O"                          );
    outtree->Branch("passTrig_HLT_Photon500"                         , &OUT::passTrig_HLT_Photon500                         , "passTrig_HLT_Photon500/O"                          );
    outtree->Branch("passTrig_HLT_Photon600"                         , &OUT::passTrig_HLT_Photon600                         , "passTrig_HLT_Photon600/O"                          );
    outtree->Branch("passTrig_HLT_Photon165_HE10"                    , &OUT::passTrig_HLT_Photon165_HE10                    , "passTrig_HLT_Photon165_HE10/O"                     );
    outtree->Branch("passTrig_HLT_Photon120_R9Id90_HE10_IsoM"        , &OUT::passTrig_HLT_Photon120_R9Id90_HE10_IsoM        , "passTrig_HLT_Photon120_R9Id90_HE10_IsoM/O"         );
    outtree->Branch("passTrig_HLT_Photon165_R9Id90_HE10_IsoM"        , &OUT::passTrig_HLT_Photon165_R9Id90_HE10_IsoM        , "passTrig_HLT_Photon165_R9Id90_HE10_IsoM/O"         );
    outtree->Branch("passTrig_HLT_Photon120_R9Id90_HE10_Iso40_EBOnly", &OUT::passTrig_HLT_Photon120_R9Id90_HE10_Iso40_EBOnly, "passTrig_HLT_Photon120_R9Id90_HE10_Iso40_EBOnly/O" );
    outtree->Branch("passTrig_HLT_Photon135_PFMET100_JetIdCleaned"   , &OUT::passTrig_HLT_Photon135_PFMET100_JetIdCleaned   , "passTrig_HLT_Photon135_PFMET100_JetIdCleaned/O"    );
 //Set trigger branches for TrigHltMu
    outtree->Branch("passTrig_HLT_Mu8"                               , &OUT::passTrig_HLT_Mu8                               , "passTrig_HLT_Mu8/O"                                );
    outtree->Branch("passTrig_HLT_Mu17"                              , &OUT::passTrig_HLT_Mu17                              , "passTrig_HLT_Mu17/O"                               );
    outtree->Branch("passTrig_HLT_Mu20"                              , &OUT::passTrig_HLT_Mu20                              , "passTrig_HLT_Mu20/O"                               );
    outtree->Branch("passTrig_HLT_Mu24"                              , &OUT::passTrig_HLT_Mu24                              , "passTrig_HLT_Mu24/O"                               );
    outtree->Branch("passTrig_HLT_Mu27"                              , &OUT::passTrig_HLT_Mu27                              , "passTrig_HLT_Mu27/O"                               );
    outtree->Branch("passTrig_HLT_Mu34"                              , &OUT::passTrig_HLT_Mu34                              , "passTrig_HLT_Mu34/O"                               );
    outtree->Branch("passTrig_HLT_Mu50"                              , &OUT::passTrig_HLT_Mu50                              , "passTrig_HLT_Mu50/O"                               );
    outtree->Branch("passTrig_HLT_Mu55"                              , &OUT::passTrig_HLT_Mu55                              , "passTrig_HLT_Mu55/O"                               );
    outtree->Branch("passTrig_HLT_Mu300"                             , &OUT::passTrig_HLT_Mu300                             , "passTrig_HLT_Mu300/O"                              );
    outtree->Branch("passTrig_HLT_Mu350"                             , &OUT::passTrig_HLT_Mu350                             , "passTrig_HLT_Mu350/O"                              );
    outtree->Branch("passTrig_HLT_Mu24_eta2p1"                       , &OUT::passTrig_HLT_Mu24_eta2p1                       , "passTrig_HLT_Mu24_eta2p1/O"                        );
    outtree->Branch("passTrig_HLT_Mu45_eta2p1"                       , &OUT::passTrig_HLT_Mu45_eta2p1                       , "passTrig_HLT_Mu45_eta2p1/O"                        );
    outtree->Branch("passTrig_HLT_Mu50_eta2p1"                       , &OUT::passTrig_HLT_Mu50_eta2p1                       , "passTrig_HLT_Mu50_eta2p1/O"                        );
    outtree->Branch("passTrig_HLT_TkMu20"                            , &OUT::passTrig_HLT_TkMu20                            , "passTrig_HLT_TkMu20/O"                             );
    outtree->Branch("passTrig_HLT_TkMu27"                            , &OUT::passTrig_HLT_TkMu27                            , "passTrig_HLT_TkMu27/O"                             );
    outtree->Branch("passTrig_HLT_TkMu24_eta2p1"                     , &OUT::passTrig_HLT_TkMu24_eta2p1                     , "passTrig_HLT_TkMu24_eta2p1/O"                      );
    outtree->Branch("passTrig_HLT_IsoMu20"                           , &OUT::passTrig_HLT_IsoMu20                           , "passTrig_HLT_IsoMu20/O"                            );
    outtree->Branch("passTrig_HLT_IsoMu22"                           , &OUT::passTrig_HLT_IsoMu22                           , "passTrig_HLT_IsoMu22/O"                            );
    outtree->Branch("passTrig_HLT_IsoMu24"                           , &OUT::passTrig_HLT_IsoMu24                           , "passTrig_HLT_IsoMu24/O"                            );
    outtree->Branch("passTrig_HLT_IsoMu27"                           , &OUT::passTrig_HLT_IsoMu27                           , "passTrig_HLT_IsoMu27/O"                            );
    outtree->Branch("passTrig_HLT_IsoMu17_eta2p1"                    , &OUT::passTrig_HLT_IsoMu17_eta2p1                    , "passTrig_HLT_IsoMu17_eta2p1/O"                     );
    outtree->Branch("passTrig_HLT_IsoMu20_eta2p1"                    , &OUT::passTrig_HLT_IsoMu20_eta2p1                    , "passTrig_HLT_IsoMu20_eta2p1/O"                     );
    outtree->Branch("passTrig_HLT_IsoMu24_eta2p1"                    , &OUT::passTrig_HLT_IsoMu24_eta2p1                    , "passTrig_HLT_IsoMu24_eta2p1/O"                     );
    outtree->Branch("passTrig_HLT_IsoTkMu20"                         , &OUT::passTrig_HLT_IsoTkMu20                         , "passTrig_HLT_IsoTkMu20/O"                          );
    outtree->Branch("passTrig_HLT_IsoTkMu22"                         , &OUT::passTrig_HLT_IsoTkMu22                         , "passTrig_HLT_IsoTkMu22/O"                          );
    outtree->Branch("passTrig_HLT_IsoTkMu24"                         , &OUT::passTrig_HLT_IsoTkMu24                         , "passTrig_HLT_IsoTkMu24/O"                          );
    outtree->Branch("passTrig_HLT_IsoTkMu27"                         , &OUT::passTrig_HLT_IsoTkMu27                         , "passTrig_HLT_IsoTkMu27/O"                          );
    outtree->Branch("passTrig_HLT_IsoTkMu20_eta2p1"                  , &OUT::passTrig_HLT_IsoTkMu20_eta2p1                  , "passTrig_HLT_IsoTkMu20_eta2p1/O"                   );
    outtree->Branch("passTrig_HLT_IsoTkMu24_eta2p1"                  , &OUT::passTrig_HLT_IsoTkMu24_eta2p1                  , "passTrig_HLT_IsoTkMu24_eta2p1/O"                   );

 //Set trigger branches for TrigHltDiPhot
 //Set trigger branches for TrigHlt
 //Set trigger branches for TrigHltElMu
    outtree->Branch("passTrig_HLT_Mu17_Photon30_CaloIdL_L1ISO"       , &OUT::passTrig_HLT_Mu17_Photon30_CaloIdL_L1ISO       , "passTrig_HLT_Mu17_Photon30_CaloIdL_L1ISO/O"        );
 //Set trigger branches for TrigHltEl
    outtree->Branch("passTrig_HLT_Ele22_eta2p1_WPLoose_Gsf"          , &OUT::passTrig_HLT_Ele22_eta2p1_WPLoose_Gsf          , "passTrig_HLT_Ele22_eta2p1_WPLoose_Gsf/O"           );
    outtree->Branch("passTrig_HLT_Ele22_eta2p1_WPTight_Gsf"          , &OUT::passTrig_HLT_Ele22_eta2p1_WPTight_Gsf          , "passTrig_HLT_Ele22_eta2p1_WPTight_Gsf/O"           );
    outtree->Branch("passTrig_HLT_Ele23_WPLoose_Gsf"                 , &OUT::passTrig_HLT_Ele23_WPLoose_Gsf                 , "passTrig_HLT_Ele23_WPLoose_Gsf/O"                  );
    outtree->Branch("passTrig_HLT_Ele24_eta2p1_WPLoose_Gsf"          , &OUT::passTrig_HLT_Ele24_eta2p1_WPLoose_Gsf          , "passTrig_HLT_Ele24_eta2p1_WPLoose_Gsf/O"           );
    outtree->Branch("passTrig_HLT_Ele25_WPTight_Gsf"                 , &OUT::passTrig_HLT_Ele25_WPTight_Gsf                 , "passTrig_HLT_Ele25_WPTight_Gsf/O"                  );
    outtree->Branch("passTrig_HLT_Ele25_eta2p1_WPLoose_Gsf"          , &OUT::passTrig_HLT_Ele25_eta2p1_WPLoose_Gsf          , "passTrig_HLT_Ele25_eta2p1_WPLoose_Gsf/O"           );
    outtree->Branch("passTrig_HLT_Ele25_eta2p1_WPTight_Gsf"          , &OUT::passTrig_HLT_Ele25_eta2p1_WPTight_Gsf          , "passTrig_HLT_Ele25_eta2p1_WPTight_Gsf/O"           );
    outtree->Branch("passTrig_HLT_Ele27_WPTight_Gsf"                 , &OUT::passTrig_HLT_Ele27_WPTight_Gsf                 , "passTrig_HLT_Ele27_WPTight_Gsf/O"                  );
    outtree->Branch("passTrig_HLT_Ele27_eta2p1_WPLoose_Gsf"          , &OUT::passTrig_HLT_Ele27_eta2p1_WPLoose_Gsf          , "passTrig_HLT_Ele27_eta2p1_WPLoose_Gsf/O"           );
    outtree->Branch("passTrig_HLT_Ele27_eta2p1_WPTight_Gsf"          , &OUT::passTrig_HLT_Ele27_eta2p1_WPTight_Gsf          , "passTrig_HLT_Ele27_eta2p1_WPTight_Gsf/O"           );
    outtree->Branch("passTrig_HLT_Ele32_eta2p1_WPLoose_Gsf"          , &OUT::passTrig_HLT_Ele32_eta2p1_WPLoose_Gsf          , "passTrig_HLT_Ele32_eta2p1_WPLoose_Gsf/O"           );
    outtree->Branch("passTrig_HLT_Ele32_eta2p1_WPTight_Gsf"          , &OUT::passTrig_HLT_Ele32_eta2p1_WPTight_Gsf          , "passTrig_HLT_Ele32_eta2p1_WPTight_Gsf/O"           );
    outtree->Branch("passTrig_HLT_Ele105_CaloIdVT_GsfTrkIdT"         , &OUT::passTrig_HLT_Ele105_CaloIdVT_GsfTrkIdT         , "passTrig_HLT_Ele105_CaloIdVT_GsfTrkIdT/O"          );
    outtree->Branch("passTrig_HLT_Ele115_CaloIdVT_GsfTrkIdT"         , &OUT::passTrig_HLT_Ele115_CaloIdVT_GsfTrkIdT         , "passTrig_HLT_Ele115_CaloIdVT_GsfTrkIdT/O"          );

 //Set trigger branches for TrigHltDiMu
    outtree->Branch("passTrig_HLT_Mu17_Mu8"                          , &OUT::passTrig_HLT_Mu17_Mu8                          , "passTrig_HLT_Mu17_Mu8/O"                           );
    outtree->Branch("passTrig_HLT_Mu17_Mu8_DZ"                       , &OUT::passTrig_HLT_Mu17_Mu8_DZ                       , "passTrig_HLT_Mu17_Mu8_DZ/O"                        );
    outtree->Branch("passTrig_HLT_Mu20_Mu10"                         , &OUT::passTrig_HLT_Mu20_Mu10                         , "passTrig_HLT_Mu20_Mu10/O"                          );
    outtree->Branch("passTrig_HLT_Mu20_Mu10_DZ"                      , &OUT::passTrig_HLT_Mu20_Mu10_DZ                      , "passTrig_HLT_Mu20_Mu10_DZ/O"                       );
    outtree->Branch("passTrig_HLT_Mu27_TkMu8"                        , &OUT::passTrig_HLT_Mu27_TkMu8                        , "passTrig_HLT_Mu27_TkMu8/O"                         );
    outtree->Branch("passTrig_HLT_Mu30_TkMu11"                       , &OUT::passTrig_HLT_Mu30_TkMu11                       , "passTrig_HLT_Mu30_TkMu11/O"                        );
    outtree->Branch("passTrig_HLT_Mu40_TkMu11"                       , &OUT::passTrig_HLT_Mu40_TkMu11                       , "passTrig_HLT_Mu40_TkMu11/O"                        );
 //Set trigger branches for TrigHltDiEl

    outtree->Branch("NLOWeight"             , &OUT::NLOWeight   , "NLOWeight/F"    );
    outtree->Branch("PassQuality"           , &OUT::PassQuality , "PassQuality/I"  );
    outtree->Branch("PUWeight"              , &OUT::PUWeight    , "PUWeight/F"     );
    outtree->Branch("PUWeightUP5"           , &OUT::PUWeightUP5 , "PUWeightUP5/F"  );
    outtree->Branch("PUWeightUP10"          , &OUT::PUWeightUP10, "PUWeightUP10/F" );
    outtree->Branch("PUWeightDN5"           , &OUT::PUWeightDN5 , "PUWeightDN5/F"  );
    outtree->Branch("PUWeightDN10"          , &OUT::PUWeightDN10, "PUWeightDN10/F" );

    eval_ph_tight  = false;
    eval_ph_medium = false;
    eval_ph_loose  = false;
    eval_mu_tight  = false;

    _needs_nlo_weght = false;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
    
        if( mod_conf.GetName() == "BuildElectron" ) { 
            std::map<std::string, std::string>::const_iterator eitr = mod_conf.GetInitData().find( "evalPID" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::string pid = eitr->second;
                if( pid == "tight"     ) eval_el_tight       = true;
                if( pid == "medium"    ) eval_el_medium      = true;
                if( pid == "loose"     ) eval_el_loose       = true;
                if( pid == "veryloose" ) eval_el_veryloose   = true;
            }
        }
        if( mod_conf.GetName() == "BuildPhoton" ) { 
            std::map<std::string, std::string>::const_iterator eitr = mod_conf.GetInitData().find( "evalPID" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::string pid = eitr->second;
                if( pid == "tight"     ) eval_ph_tight       = true;
                if( pid == "medium"    ) eval_ph_medium      = true;
                if( pid == "loose"     ) eval_ph_loose       = true;
            }
        }
        if( mod_conf.GetName() == "BuildMuon" ) { 
            std::map<std::string, std::string>::const_iterator eitr = mod_conf.GetInitData().find( "evalPID" );
            if( eitr != mod_conf.GetInitData().end() ) {
                std::string pid = eitr->second;
                if( pid == "tight"     ) eval_mu_tight       = true;
                if( pid == "medium"    ) eval_mu_medium      = true;
                if( pid == "loose"    ) eval_mu_loose      = true;
            }
        }
        if( mod_conf.GetName() == "WeightEvent" ) { 
            std::map<std::string, std::string>::const_iterator itr = mod_conf.GetInitData().find( "ApplyNLOWeight" );
            if( itr != mod_conf.GetInitData().end() ) {
                if( itr->second == "true" ) {
                    _needs_nlo_weght = true;
                }
            }
            std::string sample_filename;
            std::string data_filename;
            std::string sample_histname;
            std::string data_histname;
            std::map<std::string, std::string>::const_iterator sfitr = mod_conf.GetInitData().find( "sample_file" );
            std::map<std::string, std::string>::const_iterator dfitr = mod_conf.GetInitData().find( "data_file" );
            std::map<std::string, std::string>::const_iterator shitr = mod_conf.GetInitData().find( "sample_hist" );
            std::map<std::string, std::string>::const_iterator dhitr = mod_conf.GetInitData().find( "data_hist" );

            bool get_weight_hists = true;

            if( sfitr != mod_conf.GetInitData().end() ) {
                sample_filename = sfitr->second;
            }
            else {
                get_weight_hists = false;
            }
            if( dfitr != mod_conf.GetInitData().end() ) {
                data_filename = dfitr->second;
            }
            else {
                get_weight_hists = false;
            }
            if( shitr != mod_conf.GetInitData().end() ) {
                sample_histname = shitr->second;
            }
            else {
                get_weight_hists = false;
            }
            if( dhitr != mod_conf.GetInitData().end() ) {
                data_histname = dhitr->second;
            }
            else {
                get_weight_hists = false;
            }

            if( get_weight_hists ) {

                _puweight_sample_file = TFile::Open( sample_filename.c_str(), "READ" );
                _puweight_data_file = TFile::Open( data_filename.c_str(), "READ" );

                _puweight_sample_hist = dynamic_cast<TH1F*>(_puweight_sample_file->Get( sample_histname.c_str() ) ) ;
                _puweight_data_hist = dynamic_cast<TH1D*>(_puweight_data_file->Get( data_histname.c_str() ) );
                if( !_puweight_sample_hist ) {
                    std::cout << "Could not retrieve histogram " << sample_histname << " from " << sample_filename  << std::endl;
                }
                if( !_puweight_data_hist ) {
                    std::cout << "Could not retrieve histogram " << data_histname << " from " << data_filename << std::endl;
                }
            }
            else {
                std::cout << "WeightEvent::ERROR - Needed histogram does not exist! Will not apply PU weights!" << std::endl;
            }
            
        }
        if( mod_conf.GetName() == "FilterDataQuality" ) { 
            std::map<std::string, std::string>::const_iterator itr = mod_conf.GetInitData().find( "jsonFile" );
            if( itr != mod_conf.GetInitData().end() ) {
                std::string jsonFile = itr->second;

                std::string line;
                std::ifstream infile( jsonFile.c_str() );
                if( infile.is_open() ) {
                    while( getline( infile, line ) ) {
                        std::vector<std::string> key_val_tok = Tokenize( line, ":" );
                        std::vector<std::string> run_number_tok = Tokenize( key_val_tok[0], "\"" );
                        // find first and last brackets
                        std::string::size_type first_bracket = key_val_tok[1].find( "[" );
                        std::string::size_type last_bracket  = key_val_tok[1].rfind( "]" );

                        std::string rm_last = key_val_tok[1].substr( 0, last_bracket );
                        std::string all_vals  = rm_last.substr( first_bracket+1 );

                        int run_number;
                        std::stringstream run_number_ss( run_number_tok[1] );
                        run_number_ss >> run_number;

                        std::cout << "Run = " << run_number_tok[1] << " values = " << all_vals << std::endl;

                        std::vector<std::string> ranges_tok = Tokenize( all_vals, "[" );

                        std::vector<int> full_range;
                        for( std::vector<std::string>::const_iterator itr = ranges_tok.begin(); itr != ranges_tok.end(); ++itr ) {
                            std::string range_str = *itr;
                            std::string::size_type bracket_pos = range_str.find("]");
                            std::string range = range_str.substr( 0, bracket_pos );

                            std::vector<std::string> range_tok = Tokenize( range, "," );
                            if( range_tok.size() != 2 ) {
                                std::cout << "Expected two entries in the range.  String was " << range << std::endl;
                                continue;
                            }

                            int range_begin;
                            int range_end;

                            std::stringstream range_begin_ss( range_tok[0] );
                            std::stringstream range_end_ss  ( range_tok[1] );

                            range_begin_ss >> range_begin;
                            range_end_ss   >> range_end;

                            for( int ls = range_begin ; ls <= range_end; ++ls ) {
                                full_range.push_back(ls);
                            }

                        }
                        quality_map[run_number] = full_range;
                    }
                }
            }
        }
    }
}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // In BranchInit
    CopyInputVarsToOutput();

    // loop over configured modules
    bool save_event = true;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        save_event &= ApplyModule( mod_conf );
    }

    return save_event;

}

bool RunModule::ApplyModule( ModuleConfig & config ) const {

    bool keep_evt = true;

    if( config.GetName() == "BuildElectron" ) {
        BuildElectron( config );
    }
    if( config.GetName() == "BuildMuon" ) {
        BuildMuon( config );
    }
    if( config.GetName() == "BuildPhoton" ) {
        BuildPhoton( config );
    }
    if( config.GetName() == "BuildJet" ) {
        BuildJet( config );
    }
    if( config.GetName() == "BuildFatJet" ) {
        BuildFatJet( config );
    }
    if( config.GetName() == "BuildTruth" ) {
        BuildTruth( config );
    }
    if( config.GetName() == "BuildMET" ) {
        BuildMET( config );
    }

    if( config.GetName() == "WeightEvent" ) {
        WeightEvent( config );
    }
    if( config.GetName() == "BuildTriggerBits" ) {
        BuildTriggerBits( config );
    }

    if( config.GetName() == "FilterEvent" ) {
        keep_evt &= FilterEvent( config );
    }

    if( config.GetName() == "FilterDataQuality" ) {
        keep_evt &= FilterDataQuality( config );
    }
    //if( config.GetName() == "FilterTrigger" ) {
    //    keep_evt &= FilterTrigger( config );
    //}

    return keep_evt;
}

// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************
//

void RunModule::BuildMuon( ModuleConfig & config ) const {

    OUT::mu_pt                 -> clear();
    OUT::mu_eta                -> clear();
    OUT::mu_phi                -> clear();
    OUT::mu_e                  -> clear();
    //OUT::mu_isGlobal           -> clear();
    //OUT::mu_isPF               -> clear();
    //OUT::mu_chi2               -> clear();
    //OUT::mu_nHits              -> clear();
    //OUT::mu_nMuStations        -> clear();
    //OUT::mu_nPixHits           -> clear();
    //OUT::mu_nTrkLayers         -> clear();
    OUT::mu_d0                 -> clear();
    OUT::mu_z0                 -> clear();
    //OUT::mu_pfIso_ch           -> clear();
    //OUT::mu_pfIso_nh           -> clear();
    //OUT::mu_pfIso_pho          -> clear();
    OUT::mu_pfIso_db           -> clear();
    //OUT::mu_rhoIso             -> clear();
    //OUT::mu_corrIso            -> clear();
    //OUT::mu_trkIso             -> clear();
    //OUT::mu_charge             -> clear();
    //OUT::mu_triggerMatch       -> clear();
    //OUT::mu_triggerMatchDiMu   -> clear();
    //OUT::mu_passLoose          -> clear();
    //OUT::mu_passCustom          -> clear();
    OUT::mu_passTight          -> clear();
    OUT::mu_passMedium          -> clear();
    OUT::mu_passLoose          -> clear();
    //OUT::mu_passTightNoIso     -> clear();
    //OUT::mu_passTightNoD0      -> clear();
    //OUT::mu_passTightNoIsoNoD0 -> clear();
    OUT::mu_truthMatch_mu         -> clear();
    OUT::mu_truthMatchMinDR_mu         -> clear();
    OUT::mu_truthMatchPt_mu         -> clear();
    OUT::mu_n          = 0;


    for( unsigned int idx = 0; idx < IN::MuPt->size(); ++idx ) {
       
        float pt = IN::MuPt->at(idx);
        float eta = IN::MuEta->at(idx);
        float phi = IN::MuPhi->at(idx);
        float en = IN::MuE->at(idx);

        // MuID is filled with these bit shifts
        //kGlobMu = 1 kTkMu = 2 kPfMu = 4
        int type = IN::MuType->at(idx);

        bool isGloMu = ( ( type  &  1 ) != 0  );
        bool isTkMu  = ( ( type  &  2 ) != 0  );
        bool isPfMu  = ( ( type  &  4 ) != 0  );


        float muPFIsoDBetaCorr  = IN::MuPfIso->at(idx);
        float muPFIsoCH  = IN::MuPfIsoChHad->at(idx);
        float muPFIsoNH  = IN::MuPfIsoNeutralHad->at(idx);
        float muIsoRho   = IN::MuIsoRho->at(idx);
        float tkIso      = IN::MuIsoTkIsoAbs->at(idx);
        float d0         = IN::MuDxy->at(idx);
        float z0         = IN::MuDz->at(idx);
        float chi2       = IN::MuTkNormChi2->at(idx);

        int nMuHits          = IN::MuTkHitCnt->at(idx);
        int muStations       = IN::MuMatchedStationCnt->at(idx);
        int nPixHit          = IN::MuPixelHitCnt->at(idx);
        int nTrkLayers       = IN::MuTkLayerCnt->at(idx);

        int charge       = IN::MuCh->at(idx);

        //int muID = IN::MuId->at(idx);
        
        bool pass_tight = true;
        bool pass_loose = true;
        bool pass_medium = true;

        bool use_eval = eval_mu_tight || eval_mu_medium || eval_mu_loose;

        // loose cuts
        if( !use_eval || eval_mu_loose ) {
            if( !config.PassBool ( "cut_isPf_loose"   , isPfMu ) ) {
                pass_loose = false;
                if( eval_mu_loose) continue;
            }
            if( !config.PassBool ( "cut_isGlobalOrTk_loose"   , (isGloMu || isTkMu ) ) ) {
                pass_loose = false;
                if( eval_mu_loose) continue;
            }
        }

        // loose cuts
        if( !use_eval || eval_mu_tight ) {
            if( !config.PassBool ( "cut_isGlobal_tight"       , isGloMu     ) ) {
                pass_tight = false;
                if( eval_mu_tight ) continue;
            }
            if( !config.PassBool ( "cut_isPf_tight"       , isPfMu     ) ) {
                pass_tight = false;
                if( eval_mu_tight ) continue;
            }

            if( !config.PassFloat( "cut_chi2_tight"       , chi2           ) ) { 
                pass_tight = false;
                if( eval_mu_tight ) continue;
            }
            if( !config.PassFloat( "cut_nMuonHits_tight"  , nMuHits          ) ) { 
                pass_tight = false;
                if( eval_mu_tight ) continue;
            }
            if( !config.PassFloat( "cut_nStations_tight"  , muStations     ) ) { 
                pass_tight = false;
                if( eval_mu_tight ) continue;
            }
            if( !config.PassFloat( "cut_nPixelHits_tight" , nPixHit        ) ) { 
                pass_tight = false;
                if( eval_mu_tight ) continue;
            }
            if( !config.PassFloat( "cut_nTrkLayers_tight" , nTrkLayers     ) ) { 
                pass_tight = false;
                if( eval_mu_tight ) continue;
            }
            if( !config.PassFloat( "cut_d0_tight"         , fabs(d0)       ) ) { 
                pass_tight = false;
                if( eval_mu_tight ) continue;
            }
            if( !config.PassFloat( "cut_z0_tight"         , fabs(z0)       ) ) { 
                pass_tight = false;
                if( eval_mu_tight ) continue;
            }
            if( !config.PassFloat( "cut_trkiso_tight"     , tkIso/pt       ) ) { 
                pass_tight = false;
                if( eval_mu_tight ) continue;
            }
            if( !config.PassFloat( "cut_corriso_tight"    , muPFIsoDBetaCorr     ) ) { 
                pass_tight = false;
                if( eval_mu_tight ) continue;
            }
        }

        OUT::mu_n++;

        OUT::mu_pt                 -> push_back(pt );
        OUT::mu_eta                -> push_back(eta);
        OUT::mu_phi                -> push_back(phi);
        OUT::mu_e                  -> push_back(en );
        //OUT::mu_pfIso_ch           -> push_back(muPFIsoCH);
        //OUT::mu_pfIso_nh           -> push_back(muPFIsoNH);
        OUT::mu_pfIso_db           -> push_back(muPFIsoDBetaCorr);
        //OUT::mu_rhoIso             -> push_back(muIsoRho);
        //OUT::mu_trkIso             -> push_back(tkIso);
        OUT::mu_d0                 -> push_back(d0);
        OUT::mu_z0                 -> push_back(z0);
        //OUT::mu_chi2               -> push_back(chi2);
        //OUT::mu_charge             -> push_back(charge);
        //OUT::mu_passLoose          -> push_back((muID==0));
        //OUT::mu_passCustom         -> push_back((muID==1));

        //OUT::mu_nHits              -> push_back( nMuHits );
        //OUT::mu_nMuStations        -> push_back( muStations );
        //OUT::mu_nPixHits           -> push_back( nPixHit );
        //OUT::mu_nTrkLayers         -> push_back( nTrkLayers );
        ////OUT::mu_pfIso_pho          -> push_back(muPFIsoPho);
        ////OUT::mu_triggerMatch       -> push_back( trigMatch );
        ////OUT::mu_triggerMatchDiMu   -> push_back( trigMatchDiMu );
        OUT::mu_passTight          -> push_back( pass_tight );
        OUT::mu_passMedium          -> push_back( pass_medium );
        OUT::mu_passLoose          -> push_back( pass_loose );
        //OUT::mu_passTightNoIso     -> push_back( pass_tightNoIso );
        //OUT::mu_passTightNoD0      -> push_back( pass_tightNoD0 );
        //OUT::mu_passTightNoIsoNoD0 -> push_back( pass_tightNoIsoNoD0 );


        std::vector<int> matchPID;
        matchPID.push_back(13);
        matchPID.push_back(-13);


        TLorentzVector muonlv;
        muonlv.SetPtEtaPhiE( pt, eta, phi, en );
        
        float truthMinDR = 100.0;
        TLorentzVector matchLV;
        bool match = HasTruthMatch( muonlv, matchPID, 0.2, truthMinDR, matchLV );
        OUT::mu_truthMatch_mu->push_back( match );
        OUT::mu_truthMatchMinDR_mu->push_back( truthMinDR );
        OUT::mu_truthMatchPt_mu->push_back( matchLV.Pt() );

    }

}

void RunModule::BuildElectron( ModuleConfig & config ) const {

    OUT::el_pt                    -> clear();
    OUT::el_eta                   -> clear();
    OUT::el_sceta                 -> clear();
    OUT::el_phi                   -> clear();
    OUT::el_e                     -> clear();
    //OUT::el_d0pv                  -> clear();
    //OUT::el_z0pv                  -> clear();
    //OUT::el_sigmaIEIE             -> clear();
    //OUT::el_sigmaIEIEFull5x5      -> clear();
    //OUT::el_charge                -> clear();
    //OUT::el_ooEmooP               -> clear();
    //OUT::el_passConvVeto          -> clear();
    OUT::el_passTight             -> clear();
    OUT::el_passMedium            -> clear();
    OUT::el_passLoose             -> clear();
    OUT::el_passVeryLoose         -> clear();
    OUT::el_passVIDTight             -> clear();
    OUT::el_passVIDMedium            -> clear();
    OUT::el_passVIDLoose             -> clear();
    OUT::el_passVIDVeryLoose         -> clear();
    OUT::el_passVIDHLT         -> clear();
    OUT::el_passVIDHEEP        -> clear();
    //OUT::el_chHadIso              -> clear();
    //OUT::el_neuHadIso             -> clear();
    //OUT::el_phoIso                -> clear();
    //OUT::el_chHadIsoPuCorr        -> clear();
    //OUT::el_rawIso                -> clear();
    //OUT::el_dbIso                 -> clear();
    //OUT::el_rhoIso                -> clear();
    //OUT::el_pfiso30               -> clear();
    //OUT::el_pfiso40               -> clear();
    //OUT::el_passTightTrig         -> clear();
    //OUT::el_passMvaNonTrig        -> clear();
    //OUT::el_passMvaTrig           -> clear();
    //OUT::el_passMvaNonTrigNoIso   -> clear();
    //OUT::el_passMvaTrigNoIso      -> clear();
    //OUT::el_passMvaNonTrigOnlyIso -> clear();
    //OUT::el_passMvaTrigOnlyIso    -> clear();
    //OUT::el_triggerMatch          -> clear();
    //OUT::el_hasMatchedConv        -> clear();
    OUT::el_truthMatch_el         -> clear();
    OUT::el_truthMatchMinDR_el         -> clear();
    OUT::el_truthMatchPt_el       -> clear();
    //OUT::el_truthMatch_ph         -> clear();
    //OUT::el_truthMinDR_ph         -> clear();
    //OUT::el_truthMatchPt_ph       -> clear();
    OUT::el_n              = 0;

    for( unsigned idx = 0; idx < IN::ElOrigPt->size(); ++idx ) {

        float dEtaIn           = IN::ElDEtaTkScAtVtx->at(idx);
        float dPhiIn           = IN::ElDPhiTkScAtVtx->at(idx);
        float sigmaIEIE        = IN::ElSigmaIetaIeta->at(idx);
        float sigmaIEIEFull5x5 = IN::ElSigmaIetaIetaFull5x5->at(idx);
        float d0               = IN::ElD0->at(idx);
        float z0               = IN::ElDz->at(idx);
        float ooEmooP          = IN::ElEinvMinusPinv->at(idx);
        int   passConvVeto     = IN::ElPassConvVeto->at(idx);
        int   misshits         = IN::ElExpectedMissingInnerHitCnt->at(idx);

        float hovere           = IN::ElHoE->at(idx);
        //int   convfit          = IN::eleConvVtxFit->at(idx);
        //int   misshits         = IN::eleMissHits->at(idx);
        //float ip3d             = IN::eleIP3D->at(idx);
        //float ip3dErr          = IN::eleIP3DErr->at(idx);

        float pt               = IN::ElPt->at(idx);
        float eta              = IN::ElEta->at(idx);
        float sceta            = IN::ElEtaSc->at(idx);
        float phi              = IN::ElPhi->at(idx);
        float en               = IN::ElE->at(idx);

        float origpt               = IN::ElOrigPt->at(idx);
        float origeta              = IN::ElOrigEta->at(idx);
        float origphi              = IN::ElOrigPhi->at(idx);
        float origen               = IN::ElOrigE->at(idx);

        int   charge           = IN::ElCh->at(idx);
        //float ea               = IN::ElAEff->at(idx);

        float iso_ch           = IN::ElPfIsoChHad->at(idx);
        float iso_nh           = IN::ElPfIsoNeutralHad->at(idx);
        float iso_ph           = IN::ElPfIsoIso->at(idx);
        float iso_puch         = IN::ElPfIsoPuChHad->at(idx);
        float iso_raw          = IN::ElPfIsoRaw->at(idx);
        float iso_db           = IN::ElPfIsoDbeta->at(idx);
        float iso_rho          = IN::ElPfIsoRho->at(idx);

        bool passVIDVeryLoose = IN::ElVIDPassVeryLoose->at(idx);
        bool passVIDLoose     = IN::ElVIDPassLoose->at(idx);
        bool passVIDMedium    = IN::ElVIDPassMedium->at(idx);
        bool passVIDTight     = IN::ElVIDPassTight->at(idx);
        bool passVIDHLT       = IN::ElVIDPassHLT->at(idx);
        bool passVIDHEEP      = IN::ElVIDPassHEEP->at(idx);

        bool  pass_loose       = true;
        bool  pass_medium      = true;
        bool  pass_tight       = true;
        bool  pass_veryloose   = true;

        //float epdiff       = fabs( (1./scen) - (eoverp/scen) );
        //float mva_trig     = IN::eleIDMVATrig->at(idx);
        //float mva_nontrig  = IN::eleIDMVANonTrig->at(idx);
        //float r9           = IN::eleR9->at(idx);

        if( !config.PassFloat( "cut_pt"  , pt  ) ) continue;

        if( !config.PassFloat( "cut_abseta"         , fabs(eta) ) ) continue;
        if( !config.PassFloat( "cut_abseta_crack"   , fabs(eta) ) ) continue;
        if( !config.PassFloat( "cut_abssceta"       , fabs(sceta) ) ) continue;
        if( !config.PassFloat( "cut_abssceta_crack" , fabs(sceta) ) ) continue;

        // use versioned ID
        //bool use_eval = eval_el_tight || eval_el_medium || eval_el_loose || eval_el_veryloose || eval_el_tightTrig || eval_el_mva_nontrig || eval_el_mva_trig;
        bool use_eval = eval_el_tight || eval_el_medium || eval_el_loose || eval_el_veryloose;


        if( fabs(sceta) < 1.479 ) { // barrel

            
            // Tight cuts
            if( !use_eval || eval_el_tight ) {
                if( !config.PassFloat( "cut_absdEtaIn_barrel_tight"    , fabs(dEtaIn)       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_barrel_tight"    , fabs(dPhiIn)       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_tight" , sigmaIEIEFull5x5    ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_d0_barrel_tight"        , d0           ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_z0_barrel_tight"        , z0           ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_tight"    , hovere       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_ooEmooP_barrel_tight"    , ooEmooP       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_isoRho_barrel_tight"   , iso_rho   ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassInt( "cut_passConvVeto_barrel_tight"   , passConvVeto      ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_barrel_tight"  , misshits     ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
            }
            
            // Medium cuts
            if( !use_eval || eval_el_medium ) {
                if( !config.PassFloat( "cut_absdEtaIn_barrel_medium"    , fabs(dEtaIn)       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_barrel_medium"    , fabs(dPhiIn)       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_medium" , sigmaIEIEFull5x5    ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_d0_barrel_medium"        , d0           ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_z0_barrel_medium"        , z0           ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_medium"    , hovere       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_ooEmooP_barrel_medium"    , ooEmooP       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_isoRho_barrel_medium"   , iso_rho   ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassInt( "cut_passConvVeto_barrel_medium"   , passConvVeto      ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_barrel_medium"  , misshits     ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
            }
            
            // Loose cuts
            if( !use_eval || eval_el_loose ) {
                if( !config.PassFloat( "cut_absdEtaIn_barrel_loose"    , fabs(dEtaIn)       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_barrel_loose"    , fabs(dPhiIn)       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_loose" , sigmaIEIEFull5x5    ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_d0_barrel_loose"        , d0           ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_z0_barrel_loose"        , z0           ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_loose"    , hovere       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_ooEmooP_barrel_loose"    , ooEmooP       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_isoRho_barrel_loose"   , iso_rho ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassInt( "cut_passConvVeto_barrel_loose"   , passConvVeto      ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_barrel_loose"  , misshits     ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
            }

            // Very Loose cuts
            if( !use_eval || eval_el_veryloose ) {
                if( !config.PassFloat( "cut_absdEtaIn_barrel_veryloose"    , fabs(dEtaIn)       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_barrel_veryloose"    , fabs(dPhiIn)       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_veryloose" , sigmaIEIEFull5x5    ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_d0_barrel_veryloose"        , d0           ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_z0_barrel_veryloose"        , z0           ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_veryloose"    , hovere       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_ooEmooP_barrel_veryloose"    , ooEmooP       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_isoRho_barrel_veryloose"   , iso_rho   ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassInt( "cut_passConvVeto_barrel_veryloose"   , passConvVeto      ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_barrel_veryloose"  , misshits     ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
            }


        }
        else { // endcap

            // Tight cuts
            if( !use_eval || eval_el_tight ) {
                if( !config.PassFloat( "cut_absdEtaIn_endcap_tight"    , fabs(dEtaIn)       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_endcap_tight"    , fabs(dPhiIn)       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_tight" , sigmaIEIEFull5x5    ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_d0_endcap_tight"        , d0           ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_z0_endcap_tight"        , z0           ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_tight"    , hovere       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_ooEmooP_endcap_tight"    , ooEmooP       ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassFloat( "cut_isoRho_endcap_tight"   , iso_rho   ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }

                if( !config.PassInt( "cut_passConvVeto_endcap_tight"   , passConvVeto      ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_endcap_tight"  , misshits     ) ) {
                    pass_tight=false;
                    if( eval_el_tight ) continue;
                }
            }
            
            // Medium cuts
            if( !use_eval || eval_el_medium ) {
                if( !config.PassFloat( "cut_absdEtaIn_endcap_medium"    , fabs(dEtaIn)       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_endcap_medium"    , fabs(dPhiIn)       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_medium" , sigmaIEIEFull5x5    ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_d0_endcap_medium"        , d0           ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_z0_endcap_medium"        , z0           ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_medium"    , hovere       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_ooEmooP_endcap_medium"    , ooEmooP       ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassFloat( "cut_isoRho_endcap_medium"   , iso_rho   ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassInt( "cut_passConvVeto_endcap_medium"   , passConvVeto      ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_endcap_medium"  , misshits     ) ) {
                    pass_medium=false;
                    if( eval_el_medium ) continue;
                }
            }
            
            // Loose cuts
            if( !use_eval || eval_el_loose ) {
                if( !config.PassFloat( "cut_absdEtaIn_endcap_loose"    , fabs(dEtaIn)       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_endcap_loose"    , fabs(dPhiIn)       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_loose" , sigmaIEIEFull5x5    ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_d0_endcap_loose"        , d0           ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_z0_endcap_loose"        , z0           ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_loose"    , hovere       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_ooEmooP_endcap_loose"    , ooEmooP       ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassFloat( "cut_isoRho_endcap_loose"   , iso_rho   ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassInt( "cut_passConvVeto_endcap_loose"   , passConvVeto      ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_endcap_loose"  , misshits     ) ) {
                    pass_loose=false;
                    if( eval_el_loose ) continue;
                }
            }

            // Very Loose cuts
            if( !use_eval || eval_el_veryloose ) {
                if( !config.PassFloat( "cut_absdEtaIn_endcap_veryloose"    , fabs(dEtaIn)       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_absdPhiIn_endcap_veryloose"    , fabs(dPhiIn)       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_veryloose" , sigmaIEIEFull5x5    ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_d0_endcap_veryloose"        , d0           ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_z0_endcap_veryloose"        , z0           ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_veryloose"    , hovere       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_ooEmooP_endcap_veryloose"    , ooEmooP       ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassFloat( "cut_isoRho_endcap_veryloose"   , iso_rho   ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassInt( "cut_passConvVeto_endcap_veryloose"   , passConvVeto      ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
                if( !config.PassInt  ( "cut_misshits_endcap_veryloose"  , misshits     ) ) {
                    pass_veryloose=false;
                    if( eval_el_veryloose ) continue;
                }
            }

        }

        //if( !config.PassBool( "cut_pid_tightTrig"  , pass_tightTrig   ) ) continue;
        if( !config.PassBool( "cut_pid_tight"      , pass_tight       ) ) continue;
        if( !config.PassBool( "cut_pid_medium"     , pass_medium      ) ) continue;
        if( !config.PassBool( "cut_pid_loose"      , pass_loose       ) ) continue;
        if( !config.PassBool( "cut_pid_veryloose"  , pass_veryloose   ) ) continue;
        //if( !config.PassBool( "cut_pid_mva_trig"   , pass_mva_trig    ) ) continue;
        //if( !config.PassBool( "cut_pid_mva_nontrig", pass_mva_nontrig ) ) continue;
        //


        OUT::el_n++;

        OUT::el_pt                    -> push_back(pt);
        OUT::el_eta                   -> push_back(eta);
        OUT::el_sceta                 -> push_back(sceta);
        OUT::el_phi                   -> push_back(phi);
        OUT::el_e                     -> push_back(en);
        //OUT::el_d0pv                  -> push_back( d0 );
        //OUT::el_z0pv                  -> push_back( z0 );
        //OUT::el_sigmaIEIE             -> push_back( sigmaIEIE );
        //OUT::el_sigmaIEIEFull5x5      -> push_back( sigmaIEIEFull5x5 );
        //OUT::el_charge                -> push_back( charge );
        //OUT::el_ooEmooP               -> push_back( ooEmooP );
        //OUT::el_passConvVeto          -> push_back( passConvVeto );
        //OUT::el_chHadIso              -> push_back( iso_ch );
        //OUT::el_neuHadIso             -> push_back( iso_nh );
        //OUT::el_phoIso                -> push_back( iso_ph );
        //OUT::el_chHadIsoPuCorr        -> push_back( iso_puch );
        //OUT::el_rawIso                -> push_back( iso_raw );
        //OUT::el_dbIso                 -> push_back( iso_db );
        //OUT::el_rhoIso                -> push_back( iso_rho );
        OUT::el_passTight             -> push_back(pass_tight);
        OUT::el_passMedium            -> push_back(pass_medium);
        OUT::el_passLoose             -> push_back(pass_loose);
        OUT::el_passVeryLoose         -> push_back(pass_veryloose);

        OUT::el_passVIDVeryLoose -> push_back( passVIDVeryLoose );
        OUT::el_passVIDLoose     -> push_back( passVIDLoose     );
        OUT::el_passVIDMedium    -> push_back( passVIDMedium    );
        OUT::el_passVIDTight     -> push_back( passVIDTight     );
        OUT::el_passVIDHLT       -> push_back( passVIDHLT       );
        //OUT::el_passVIDHEEP      -> push_back( passVIDHEEP      );
        //OUT::el_mva_trig              -> push_back(mva_trig);
        //OUT::el_mva_nontrig           -> push_back(mva_nontrig);

        //OUT::el_passTightTrig         -> push_back(pass_tightTrig);
        //OUT::el_passMvaTrig           -> push_back(pass_mva_trig);
        //OUT::el_passMvaNonTrig        -> push_back(pass_mva_nontrig);
        //OUT::el_passMvaTrigNoIso      -> push_back(pass_mva_trig_noiso);
        //OUT::el_passMvaNonTrigNoIso   -> push_back(pass_mva_nontrig_noiso);
        //OUT::el_passMvaTrigOnlyIso    -> push_back(pass_mva_trig_onlyiso);
        //OUT::el_passMvaNonTrigOnlyIso -> push_back(pass_mva_nontrig_onlyiso);
        //OUT::el_triggerMatch          -> push_back( trigMatch );

        // check truth matching
        TLorentzVector ellv;
        ellv.SetPtEtaPhiE( pt, eta, phi, en );
        std::vector<int> matchPID;
        matchPID.push_back(11);
        matchPID.push_back(-11);

        float minTruthDR = 100.0;
        TLorentzVector matchLV;
        bool match = HasTruthMatch( ellv, matchPID, 0.2, minTruthDR, matchLV );
        OUT::el_truthMatch_el->push_back( match  );
        OUT::el_truthMatchMinDR_el->push_back( minTruthDR );
        OUT::el_truthMatchPt_el->push_back( matchLV.Pt() );

        //std::vector<int> matchPIDPH;
        //minTruthDR = 100.0;
        //matchLV.SetPxPyPzE(0.0, 0.0, 0.0, 0.0);
        //matchPIDPH.push_back(22);
        //match = HasTruthMatch( ellv, matchPIDPH, 0.2, minTruthDR, matchLV );
        //OUT::el_truthMatch_ph->push_back( match );
        //OUT::el_truthMinDR_ph->push_back( minTruthDR );
        //OUT::el_truthMatchPt_ph->push_back( matchLV.Pt() );

    }

}        
//
//float RunModule::get_ele_eff_area( float sceta, int cone ) const {
//
//    float ea = -1;
//
//    if( cone == 3 ) {
//        if (fabs(sceta) < 1.0 )                              ea = 0.130;
//        else if (fabs(sceta) >= 1.0 && fabs(sceta) < 1.479 ) ea = 0.137;
//        else if (fabs(sceta) >= 1.479 && fabs(sceta) < 2.0 ) ea = 0.067;
//        else if (fabs(sceta) >= 2.0 && fabs(sceta) < 2.2 )   ea = 0.089;
//        else if (fabs(sceta) >= 2.2 && fabs(sceta) < 2.3 )   ea = 0.107;
//        else if (fabs(sceta) >= 2.3 && fabs(sceta) < 2.4 )   ea = 0.110;
//        else if (fabs(sceta) >= 2.4 )                        ea = 0.138;
//        else {
//            std::cout << "Did not get Effective Area for eta " << sceta << std::endl;
//        }
//
//        //if (fabs(sceta) >= 0.0 && fabs(sceta) < 1.0 ) ea = 0.13;
//        //if (fabs(sceta) >= 1.0 && fabs(sceta) < 1.479 ) ea = 0.14;
//        //if (fabs(sceta) >= 1.479 && fabs(sceta) < 2.0 ) ea = 0.07;
//        //if (fabs(sceta) >= 2.0 && fabs(sceta) < 2.2 ) ea = 0.09;
//        //if (fabs(sceta) >= 2.2 && fabs(sceta) < 2.3 ) ea = 0.11;
//        //if (fabs(sceta) >= 2.3 && fabs(sceta) < 2.4 ) ea = 0.11;
//        //if (fabs(sceta) >= 2.4 ) ea = 0.14;
//
//    }
//    else if( cone == 4 ) {
//
//        if (fabs(sceta) < 1.0 )                              ea = 0.208;
//        else if (fabs(sceta) >= 1.0 && fabs(sceta) < 1.479 ) ea = 0.209;
//        else if (fabs(sceta) >= 1.479 && fabs(sceta) < 2.0 ) ea = 0.115;
//        else if (fabs(sceta) >= 2.0 && fabs(sceta) < 2.2 )   ea = 0.143;
//        else if (fabs(sceta) >= 2.2 && fabs(sceta) < 2.3 )   ea = 0.183;
//        else if (fabs(sceta) >= 2.3 && fabs(sceta) < 2.4 )   ea = 0.194;
//        else if (fabs(sceta) >= 2.4 )                        ea = 0.261;
//        else {
//            std::cout << "Did not get Effective Area for eta " << sceta << std::endl;
//        }
//
//    }
//    else {
//        std::cout << "Cone size must be 3 or 4" << std::endl;
//    }
//
//    return ea;
//}
//

void RunModule::BuildFatJet( ModuleConfig & config ) const {

    OUT::jetAK08_pt             -> clear();
    OUT::jetAK08_eta            -> clear();
    OUT::jetAK08_phi            -> clear();
    OUT::jetAK08_e              -> clear();
    OUT::jetAK08_n          = 0;

#ifdef EXISTS_JetAk08Pt

    for( unsigned idx = 0; idx < IN::JetAk08Pt->size(); ++idx ) {

        float pt  = IN::JetAk08Pt->at(idx);
        float eta = IN::JetAk08Eta->at(idx);
        float phi = IN::JetAk08Phi->at(idx);
        float en  = IN::JetAk08E->at(idx);

        if( !config.PassFloat( "cut_pt", pt ) ) continue;
        if( !config.PassFloat( "cut_abseta", eta ) ) continue;

        OUT::jetAK08_pt             -> push_back(pt);
        OUT::jetAK08_eta            -> push_back(eta);
        OUT::jetAK08_phi            -> push_back(phi);
        OUT::jetAK08_e              -> push_back(en);
        OUT::jetAK08_n++;
    }

#endif

}
void RunModule::BuildJet( ModuleConfig & config ) const {

    OUT::jet_pt             -> clear();
    OUT::jet_eta            -> clear();
    OUT::jet_phi            -> clear();
    OUT::jet_e              -> clear();
    OUT::jet_bTagCSVV2      -> clear();
    OUT::jet_IdLoose        -> clear();
    OUT::jet_IdTight        -> clear();
    OUT::jet_IdTightLep     -> clear();
    OUT::jet_n          = 0;


    for( unsigned idx = 0; idx < IN::JetAk04Pt->size(); ++idx ) {
        
        float pt  = IN::JetAk04Pt->at(idx);
        float eta = IN::JetAk04Eta->at(idx);
        float phi = IN::JetAk04Phi->at(idx);
        float en  = IN::JetAk04E->at(idx);


        float nhf        = 0;
        float chf        = 0;
        float muf        = 0;
        float cemf       = 0;
        float nemf       = 0;
        int   cmult      = 0;
        int   nmult      = 0;

        //float nhf        = IN::JetAk04NeuHadFrac->at(idx);
        //float chf        = IN::JetAk04ChHadFrac->at(idx);
        //float muf        = IN::JetAk04MuonFrac->at(idx);
        //float cemf       = IN::JetAk04ChEmFrac->at(idx);
        //float nemf       = IN::JetAk04NeuEmFrac->at(idx);
        //int   cmult      = IN::JetAk04ChMult->at(idx);
        //int   nmult      = IN::JetAk04NeuMult->at(idx);
        int   nconst     = cmult + nmult;

        bool pass_loose    = true;
        bool pass_tight    = true;
        bool pass_tightlep = true;

        if( fabs( eta ) < 2.7 ) {
            if( !config.PassFloat( "cut_jet_nhf_central_loose" , nhf  ) ) pass_loose = false;
            if( !config.PassFloat( "cut_jet_nemf_central_loose", nemf ) ) pass_loose = false;
            if( !config.PassInt  ( "cut_jet_nconst_central_loose", nconst ) ) pass_loose = false;

            if( !config.PassFloat( "cut_jet_nhf_central_tight" , nhf  ) ) pass_tight = false;
            if( !config.PassFloat( "cut_jet_nemf_central_tight", nemf ) ) pass_tight = false;
            if( !config.PassInt  ( "cut_jet_nconst_central_tight", nconst ) ) pass_tight = false;

            if( !config.PassFloat( "cut_jet_nhf_central_tightlep" , nhf  ) ) pass_tightlep = false;
            if( !config.PassFloat( "cut_jet_nemf_central_tightlep", nemf ) ) pass_tightlep = false;
            if( !config.PassInt  ( "cut_jet_nconst_central_tightlep", nconst ) ) pass_tightlep = false;
            if( !config.PassFloat  ( "cut_jet_muf_central_tightlep", muf ) ) pass_tightlep = false;
            if( fabs( eta ) < 2.4 ) {
                if( !config.PassFloat( "cut_jet_chf_central_loose" , chf  ) ) pass_loose = false;
                if( !config.PassInt( "cut_jet_cmult_central_loose" , cmult  ) ) pass_loose = false;
                if( !config.PassFloat( "cut_jet_cemf_central_loose" , cemf ) ) pass_loose = false;

                if( !config.PassFloat( "cut_jet_chf_central_tight" , chf  ) ) pass_tight = false;
                if( !config.PassInt( "cut_jet_cmult_central_tight" , cmult  ) ) pass_tight = false;
                if( !config.PassFloat( "cut_jet_cemf_central_tight" , cemf ) ) pass_tight = false;

                if( !config.PassFloat( "cut_jet_chf_central_tightlep" , chf  ) ) pass_tightlep = false;
                if( !config.PassInt( "cut_jet_cmult_central_tightlep" , cmult  ) ) pass_tightlep = false;
                if( !config.PassFloat( "cut_jet_cemf_central_tightlep" , cemf ) ) pass_tightlep = false;
            }

        }
        else if( fabs( eta ) < 3.0 ) {
            if( !config.PassFloat( "cut_jet_nhf_transition_loose", nhf ) ) pass_loose = false;
            if( !config.PassFloat( "cut_jet_nemf_transition_loose", nemf ) ) pass_loose = false;
            if( !config.PassInt( "cut_jet_nmult_transition_loose", nmult ) ) pass_loose = false;

            if( !config.PassFloat( "cut_jet_nhf_transition_tight", nhf ) ) pass_tight = false;
            if( !config.PassFloat( "cut_jet_nemf_transition_tight", nemf ) ) pass_tight = false;
            if( !config.PassInt( "cut_jet_nmult_transition_tight", nmult ) ) pass_tight = false;

        }
        else {
            if( !config.PassFloat( "cut_jet_nemf_forward_loose", nemf ) ) pass_loose = false;
            if( !config.PassInt( "cut_jet_nmult_forward_loose", nmult ) ) pass_loose = false;

            if( !config.PassFloat( "cut_jet_nemf_forward_tight", nemf ) ) pass_tight = false;
            if( !config.PassInt( "cut_jet_nmult_forward_tight", nmult ) ) pass_tight = false;
        }

        if( !config.PassFloat( "cut_pt", pt ) ) continue;
        if( !config.PassFloat( "cut_abseta", eta ) ) continue;
        if( !config.PassBool( "cut_idloose", pass_loose ) ) continue;

        OUT::jet_pt             -> push_back(pt);
        OUT::jet_eta            -> push_back(eta);
        OUT::jet_phi            -> push_back(phi);
        OUT::jet_e              -> push_back(en);
        OUT::jet_bTagCSVV2      -> push_back(IN::JetAk04BDiscCisvV2->at(idx) );
        OUT::jet_IdLoose        -> push_back(pass_loose );
        OUT::jet_IdTight        -> push_back(pass_tight );
        OUT::jet_IdTightLep     -> push_back(pass_tightlep );
            
        OUT::jet_n++;
    }
            
}        

void RunModule::BuildMET( ModuleConfig & config ) const {

    //use slimmedMETs
    TLorentzVector metlv;
    metlv.SetPxPyPzE( IN::METPx->at(0), IN::METPy->at(0), 0.0, IN::METPt->at(0) );
    OUT::met_pt = IN::METPt->at(0);
    OUT::met_phi = metlv.Phi();
}


void RunModule::BuildPhoton( ModuleConfig & config ) const {

    OUT::ph_pt                     -> clear();
    OUT::ph_eta                    -> clear();
    OUT::ph_sceta                  -> clear();
    OUT::ph_phi                    -> clear();
    OUT::ph_scphi                  -> clear();
    OUT::ph_e                      -> clear();
    //OUT::ph_scE                    -> clear();
    OUT::ph_HoverE                 -> clear();
    OUT::ph_sigmaIEIE              -> clear();
    //OUT::ph_sigmaIEIP              -> clear();
    //OUT::ph_r9                     -> clear();
    //OUT::ph_E3x3                   -> clear();
    //OUT::ph_E1x5                   -> clear();
    //OUT::ph_E2x5                   -> clear();
    //OUT::ph_E5x5                   -> clear();
    //OUT::ph_E2x5Max                -> clear();
    //OUT::ph_SCetaWidth             -> clear();
    //OUT::ph_SCphiWidth             -> clear();
    //OUT::ph_ESEffSigmaRR           -> clear();
    //OUT::ph_hcalIsoDR03            -> clear();
    //OUT::ph_trkIsoHollowDR03       -> clear();
    //OUT::ph_chgpfIsoDR02           -> clear();
    //OUT::ph_pfChIsoWorst           -> clear();
    OUT::ph_chIso                  -> clear();
    OUT::ph_neuIso                 -> clear();
    OUT::ph_phoIso                 -> clear();
    OUT::ph_chIsoCorr              -> clear();
    OUT::ph_neuIsoCorr             -> clear();
    OUT::ph_phoIsoCorr             -> clear();
    OUT::ph_eleVeto                -> clear();
    OUT::ph_hasPixSeed             -> clear();
    //OUT::ph_drToTrk                -> clear();
    //OUT::ph_isConv                 -> clear();
    OUT::ph_passLoose              -> clear();
    OUT::ph_passMedium             -> clear();
    OUT::ph_passTight              -> clear();
    OUT::ph_passLooseNoSIEIE       -> clear();
    OUT::ph_passHOverELoose         -> clear();
    OUT::ph_passHOverEMedium        -> clear();
    OUT::ph_passHOverETight         -> clear();
    OUT::ph_passSIEIELoose         -> clear();
    OUT::ph_passSIEIEMedium        -> clear();
    OUT::ph_passSIEIETight         -> clear();
    OUT::ph_passChIsoCorrLoose     -> clear();
    OUT::ph_passChIsoCorrMedium    -> clear();
    OUT::ph_passChIsoCorrTight     -> clear();
    OUT::ph_passNeuIsoCorrLoose    -> clear();
    OUT::ph_passNeuIsoCorrMedium   -> clear();
    OUT::ph_passNeuIsoCorrTight    -> clear();
    OUT::ph_passPhoIsoCorrLoose    -> clear();
    OUT::ph_passPhoIsoCorrMedium   -> clear();
    OUT::ph_passPhoIsoCorrTight    -> clear();
    //OUT::ph_truthMatch_el          -> clear();
    //OUT::ph_truthMinDR_el          -> clear();
    //OUT::ph_truthMatchPt_el        -> clear();
    //OUT::ph_truthMatch_jet         -> clear();
    //OUT::ph_truthMinDR_jet         -> clear();
    //OUT::ph_truthMatchPt_jet       -> clear();
    OUT::ph_truthMatch_ph          -> clear();
    OUT::ph_truthMatchMinDR_ph          -> clear();
    OUT::ph_truthMatchPt_ph        -> clear();
    OUT::ph_passVIDLoose              -> clear();
    OUT::ph_passVIDMedium             -> clear();
    OUT::ph_passVIDTight              -> clear();
    //OUT::ph_truthMatchMotherPID_ph -> clear();
    //OUT::ph_truthMatchParentage_ph -> clear();
    //OUT::ph_hasSLConv              -> clear();
    //OUT::ph_pass_mva_presel        -> clear();
    //OUT::ph_mvascore               -> clear();
    OUT::ph_IsEB                   -> clear();
    OUT::ph_IsEE                   -> clear();
    OUT::ph_n          = 0;

    for( unsigned int idx = 0; idx < IN::PhotOrigPt->size(); ++idx ) {

        float pt        = IN::PhotPt->at(idx);
        float pt_uncalib= IN::PhotOrigPt->at(idx);
        float eta       = IN::PhotEta->at(idx);
        float sceta     = IN::PhotScEta->at(idx);
        float phi       = IN::PhotPhi->at(idx);
        float scphi     = IN::PhotScPhi->at(idx);

        float rho = IN::EvtFastJetRho;

        float hovere       = IN::PhotHoE->at(idx);
        float sigmaIEIE    = IN::PhotSigmaIetaIetaFull5x5->at(idx);
        //float sigmaIEIP    = IN::PhotSigmaIEtaIPhi->at(idx);
        //float r9           = IN::PhotR9->at(idx);
        bool   eleVeto      = IN::PhotPassElVeto->at(idx);
        bool   pixseed      = IN::PhotHasPixelSeed->at(idx);
        //float drToTrk      = IN::PhotCiCdRtoTrk->at(idx);
        float E3x3         = IN::PhotE3x3->at(idx);
        float E1x5         = IN::PhotE1x5->at(idx);
        float E2x5         = IN::PhotE2x5->at(idx);
        float E5x5         = IN::PhotE5x5->at(idx);
        //float E2x5Max      = IN::PhotE2x5Max->at(dupidx);
        float SCetaWidth   = IN::PhotEtaWidth->at(idx);
        //float SCphiWidth   = IN::PhotPhiWidth->at(idx);
        //float ESEffSigmaRR = IN::PhotESEffSigmaRR_x->at(idx);

        bool iseb = false;
        bool isee = false;
        if( fabs(sceta) < 1.479 ) {
            iseb = true;
        }
        if( fabs(sceta) > 1.57 ) {
            isee = true;
        }

        //// evaluate largest isolation value
        //float phoPFChIsoWorst = 0;
        //for (unsigned k = 0; k < IN::phoCiCPF4chgpfIso03->at(idx).size(); ++k) {
        //    if (phoPFChIsoWorst < IN::phoCiCPF4chgpfIso03->at(idx)[k]) {
        //        phoPFChIsoWorst = IN::phoCiCPF4chgpfIso03->at(idx)[k];
        //    }
        //}

        //float hcalIsoDR03      = IN::phoHcalIsoDR03->at(idx);
        //float trkIsoHollowDR03 = IN::phoTrkIsoHollowDR03->at(idx);
        //float chgpfIsoDR02     = IN::phoCiCPF4chgpfIso02->at(idx).at(0);

        //float hcalIsoDR03PtCorr      = hcalIsoDR03 - 0.005 * pt;
        //float trkIsoHollowDR03PtCorr = trkIsoHollowDR03  - 0.002 * pt;

        float pfChIso     = IN::PhotPfIsoChHad->at(idx);
        float pfNeuIso    = IN::PhotPfIsoNeutralHad->at(idx);
        float pfPhoIso    = IN::PhotPfIsoPhot->at(idx);



        float pfChIsoRhoCorr = 0.0;
        float pfNeuIsoRhoCorr = 0.0;
        float pfPhoIsoRhoCorr = 0.0;
        calc_corr_iso( pfChIso, pfPhoIso, pfNeuIso, rho, sceta, pfChIsoRhoCorr, pfPhoIsoRhoCorr, pfNeuIsoRhoCorr);

        float p1_neu = 0;
        float p2_neu = 0;
        float p1_pho = 0;
        // taken from https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonIdentificationRun2#Recommended_Working_points_for_2
        // Updated Dec 2016
        if( iseb ) {
            p1_neu = 0.0148;
            p2_neu = 0.000017;
            p1_pho = 0.0047;
        }
        else {
            p1_neu = 0.0163;
            p2_neu = 0.000014;
            p1_pho = 0.0034;
        }

        float pfChIsoPtRhoCorr  = pfChIsoRhoCorr;
        float pfNeuIsoPtRhoCorr = pfNeuIsoRhoCorr-p1_neu*pt_uncalib-p2_neu*pt_uncalib*pt_uncalib;
        float pfPhoIsoPtRhoCorr = pfPhoIsoRhoCorr-p1_pho*pt_uncalib;

        //std::cout << "CutCalc : photon pt = " << pt_uncalib << " absEta = " << sceta << " Iso Val = " << pfChIso << " rho = " << rho << " EACorr = " << pfChIsoPtRhoCorr << std::endl;


        if( !config.PassFloat( "cut_pt"    , pt       ) ) continue;
        if( !config.PassFloat( "cut_abseta"    , fabs(sceta)       ) ) continue;
        if( !config.PassFloat( "cut_abseta_crack"    , fabs(sceta)       ) ) continue;

        bool passVIDLoose     = IN::PhotVIDPassLoose->at(idx);
        bool passVIDMedium    = IN::PhotVIDPassMedium->at(idx);
        bool passVIDTight     = IN::PhotVIDPassTight->at(idx);

        bool pass_loose         = true;
        bool pass_loose_nosieie = true;
        bool pass_medium        = true;
        bool pass_tight         = true;

        bool pass_sieie_loose   = true;
        bool pass_sieie_medium   = true;
        bool pass_sieie_tight   = true;

        bool pass_chIsoCorr_loose   = true;
        bool pass_chIsoCorr_medium   = true;
        bool pass_chIsoCorr_tight   = true;

        bool pass_neuIsoCorr_loose   = true;
        bool pass_neuIsoCorr_medium   = true;
        bool pass_neuIsoCorr_tight   = true;

        bool pass_phoIsoCorr_loose   = true;
        bool pass_phoIsoCorr_medium   = true;
        bool pass_phoIsoCorr_tight   = true;

        bool pass_hovere_loose   = true;
        bool pass_hovere_medium   = true;
        bool pass_hovere_tight   = true;

        bool use_eval = eval_ph_tight || eval_ph_medium || eval_ph_loose;

        if( fabs(sceta) < 1.479 ) { // barrel

            //loose 
            if( !use_eval || eval_ph_loose ) {
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_loose"   , sigmaIEIE         ) ) {
                    pass_loose=false;
                    pass_sieie_loose=false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_chIsoCorr_barrel_loose"   , pfChIsoPtRhoCorr  ) ) {
                    pass_loose=false;
                    pass_chIsoCorr_loose = false;
                    pass_loose_nosieie=false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_neuIsoCorr_barrel_loose"  , pfNeuIsoPtRhoCorr ) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_neuIsoCorr_loose = false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_phoIsoCorr_barrel_loose"  , pfPhoIsoPtRhoCorr ) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_phoIsoCorr_loose = false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_loose"  , hovere) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_hovere_loose = false;
                    if( eval_ph_loose ) continue;
                }

            }

            // medium
            if( !use_eval || eval_ph_medium ) {
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_medium"  , sigmaIEIE         ) ) {
                    pass_medium=false;
                    pass_sieie_medium=false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_chIsoCorr_barrel_medium"  , pfChIsoPtRhoCorr  ) ) {
                    pass_medium=false;
                    pass_chIsoCorr_medium = false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_neuIsoCorr_barrel_medium" , pfNeuIsoPtRhoCorr ) ) {
                    pass_medium=false;
                    pass_neuIsoCorr_medium = false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_phoIsoCorr_barrel_medium" , pfPhoIsoPtRhoCorr ) ) {
                    pass_medium=false;
                    pass_phoIsoCorr_medium = false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_medium" , hovere) ) {
                    pass_medium=false;
                    pass_hovere_medium = false;
                    if( eval_ph_medium ) continue;
                }
            }

            // tight
            if( !use_eval || eval_ph_tight ) {
                if( !config.PassFloat( "cut_sigmaIEIE_barrel_tight"   , sigmaIEIE         ) ) {
                    pass_tight=false;
                    pass_sieie_tight=false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_chIsoCorr_barrel_tight"   , pfChIsoPtRhoCorr  ) ) {
                    pass_tight=false;
                    pass_chIsoCorr_tight = false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_neuIsoCorr_barrel_tight"  , pfNeuIsoPtRhoCorr ) ) {
                    pass_tight=false;
                    pass_neuIsoCorr_tight = false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_phoIsoCorr_barrel_tight"  , pfPhoIsoPtRhoCorr ) ) {
                    pass_tight=false;
                    pass_phoIsoCorr_tight = false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_hovere_barrel_tight"  , hovere) ) {
                    pass_tight=false;
                    pass_hovere_tight = false;
                    if( eval_ph_tight ) continue;
                }
            }

        }
        else { // endcap
            // loose
            if( !use_eval || eval_ph_loose ) {
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_loose"   , sigmaIEIE         ) ) {
                    pass_loose=false;
                    pass_sieie_loose=false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_chIsoCorr_endcap_loose"   , pfChIsoPtRhoCorr  ) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_chIsoCorr_loose = false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_neuIsoCorr_endcap_loose"  , pfNeuIsoPtRhoCorr ) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_neuIsoCorr_loose = false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_phoIsoCorr_endcap_loose"  , pfPhoIsoPtRhoCorr ) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_phoIsoCorr_loose = false;
                    if( eval_ph_loose ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_loose"  , hovere) ) {
                    pass_loose=false;
                    pass_loose_nosieie=false;
                    pass_hovere_loose = false;
                    if( eval_ph_loose ) continue;
                }
            }

            // medium
            if( !use_eval || eval_ph_medium ) {
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_medium"  , sigmaIEIE         ) ) {
                    pass_medium=false;
                    pass_sieie_medium=false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_chIsoCorr_endcap_medium"  , pfChIsoPtRhoCorr  ) ) {
                    pass_medium=false;
                    pass_chIsoCorr_medium = false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_neuIsoCorr_endcap_medium" , pfNeuIsoPtRhoCorr ) ) {
                    pass_medium=false;
                    pass_neuIsoCorr_medium = false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_phoIsoCorr_endcap_medium" , pfPhoIsoPtRhoCorr ) ) {
                    pass_medium=false;
                    pass_phoIsoCorr_medium = false;
                    if( eval_ph_medium ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_medium" , hovere) ) {
                    pass_medium=false;
                    pass_hovere_medium = false;
                    if( eval_ph_medium ) continue;
                }
            }

            // tight
            if( !use_eval || eval_ph_tight ) {
                if( !config.PassFloat( "cut_sigmaIEIE_endcap_tight"   , sigmaIEIE         ) ) {
                    pass_tight=false;
                    pass_sieie_tight=false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_chIsoCorr_endcap_tight"   , pfChIsoPtRhoCorr  ) ) {
                    pass_tight=false;
                    pass_chIsoCorr_tight = false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_neuIsoCorr_endcap_tight"  , pfNeuIsoPtRhoCorr ) ) {
                    pass_tight=false;
                    pass_neuIsoCorr_tight = false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_phoIsoCorr_endcap_tight"  , pfPhoIsoPtRhoCorr ) ) {
                    pass_phoIsoCorr_tight = false;
                    pass_tight=false;
                    if( eval_ph_tight ) continue;
                }
                if( !config.PassFloat( "cut_hovere_endcap_tight"  , hovere) ) {
                    pass_hovere_tight = false;
                    pass_tight=false;
                    if( eval_ph_tight ) continue;
                }
            }
        }


        if( !config.PassBool( "cut_pid_tight"    , pass_tight     ) ) continue;
        if( !config.PassBool( "cut_pid_medium"   , pass_medium    ) ) continue;
        if( !config.PassBool( "cut_pid_loose"    , pass_loose     ) ) continue;


        OUT::ph_n++;

        OUT::ph_pt                   -> push_back(pt);
        OUT::ph_eta                  -> push_back(eta);
        OUT::ph_sceta                -> push_back(sceta);
        OUT::ph_phi                  -> push_back(phi);
        OUT::ph_scphi                -> push_back(scphi);
        OUT::ph_e                    -> push_back(pt*cosh(eta));
        //OUT::ph_scE                  -> push_back(SCRawE);
        OUT::ph_HoverE               -> push_back(hovere);
        OUT::ph_sigmaIEIE            -> push_back(sigmaIEIE);
        //OUT::ph_sigmaIEIP            -> push_back(sigmaIEIP);
        //OUT::ph_r9                   -> push_back(r9);
        //OUT::ph_E3x3                 -> push_back(E3x3);
        //OUT::ph_E1x5                 -> push_back(E1x5);
        //OUT::ph_E2x5                 -> push_back(E2x5);
        //OUT::ph_E5x5                 -> push_back(E5x5);
        //OUT::ph_E2x5Max              -> push_back(E2x5Max);
        //OUT::ph_SCetaWidth           -> push_back(SCetaWidth);
        //OUT::ph_SCphiWidth           -> push_back(SCphiWidth);
        //OUT::ph_ESEffSigmaRR         -> push_back(ESEffSigmaRR);
        //OUT::ph_hcalIsoDR03          -> push_back(hcalIsoDR03);
        //OUT::ph_trkIsoHollowDR03     -> push_back(trkIsoHollowDR03);
        //OUT::ph_chgpfIsoDR02         -> push_back(chgpfIsoDR02);
        //OUT::ph_pfChIsoWorst         -> push_back(phoPFChIsoWorst);
        OUT::ph_chIso                -> push_back(pfChIso);
        OUT::ph_neuIso               -> push_back(pfNeuIso);
        OUT::ph_phoIso               -> push_back(pfPhoIso);
        OUT::ph_chIsoCorr            -> push_back(pfChIsoPtRhoCorr);
        OUT::ph_neuIsoCorr           -> push_back(pfNeuIsoPtRhoCorr);
        OUT::ph_phoIsoCorr           -> push_back(pfPhoIsoPtRhoCorr);

        OUT::ph_passTight            -> push_back(pass_tight);
        OUT::ph_passMedium           -> push_back(pass_medium);
        OUT::ph_passLoose            -> push_back(pass_loose);
        OUT::ph_passVIDTight         -> push_back(passVIDTight);
        OUT::ph_passVIDMedium        -> push_back(passVIDMedium);
        OUT::ph_passVIDLoose         -> push_back(passVIDLoose);
        OUT::ph_passLooseNoSIEIE     -> push_back(pass_loose_nosieie);
        OUT::ph_passHOverELoose      -> push_back(pass_hovere_loose);
        OUT::ph_passHOverEMedium     -> push_back(pass_hovere_medium);
        OUT::ph_passHOverETight      -> push_back(pass_hovere_tight);
        OUT::ph_passSIEIELoose       -> push_back(pass_sieie_loose);
        OUT::ph_passSIEIEMedium      -> push_back(pass_sieie_medium);
        OUT::ph_passSIEIETight       -> push_back(pass_sieie_tight);
        OUT::ph_passChIsoCorrLoose   -> push_back(pass_chIsoCorr_loose);
        OUT::ph_passChIsoCorrMedium  -> push_back(pass_chIsoCorr_medium);
        OUT::ph_passChIsoCorrTight   -> push_back(pass_chIsoCorr_tight);
        OUT::ph_passNeuIsoCorrLoose  -> push_back(pass_neuIsoCorr_loose);
        OUT::ph_passNeuIsoCorrMedium -> push_back(pass_neuIsoCorr_medium);
        OUT::ph_passNeuIsoCorrTight  -> push_back(pass_neuIsoCorr_tight);
        OUT::ph_passPhoIsoCorrLoose  -> push_back(pass_phoIsoCorr_loose);
        OUT::ph_passPhoIsoCorrMedium -> push_back(pass_phoIsoCorr_medium);
        OUT::ph_passPhoIsoCorrTight  -> push_back(pass_phoIsoCorr_tight);
        OUT::ph_eleVeto              -> push_back(eleVeto);
        OUT::ph_hasPixSeed           -> push_back(pixseed);

        OUT::ph_IsEB -> push_back( iseb );
        OUT::ph_IsEE -> push_back( isee );

        //// fill conversion info
        //// the ntuples fill default values when the
        //// photon is not converted, so just keep that

        //OUT::ph_isConv           -> push_back(IN::phoIsConv->at(idx));
        //OUT::ph_hasSLConv        -> push_back( (IN::SingleLegConv->at(idx) > 0 ) );

        TLorentzVector phlv;
        phlv.SetPtEtaPhiM( pt, eta, phi, 0.0 );
        std::vector<int> matchPID;
        matchPID.push_back(22);

        float minTruthDR = 100.0;
        TLorentzVector matchLV;
        bool match = HasTruthMatch( phlv, matchPID, 0.2, minTruthDR, matchLV );
        OUT::ph_truthMatch_ph->push_back( match  );
        OUT::ph_truthMatchMinDR_ph->push_back( minTruthDR );
        OUT::ph_truthMatchPt_ph->push_back( matchLV.Pt() );
        //OUT::ph_truthMatchMotherPID_ph->push_back( matchMotherPID );
        //OUT::ph_truthMatchParentage_ph->push_back( matchParentage );

        //std::vector<int> matchPIDEl;
        //matchPIDEl.push_back(11);
        //matchPIDEl.push_back(-11);

        //minTruthDR = 100.0;
        //matchLV.SetPxPyPzE(0.0, 0.0, 0.0, 0.0);
        //match = HasTruthMatch( phlv, matchPIDEl, 0.2, minTruthDR, matchLV );
        //OUT::ph_truthMatch_el->push_back( match  );
        //OUT::ph_truthMinDR_el->push_back( minTruthDR );
        //OUT::ph_truthMatchPt_el->push_back( matchLV.Pt() );

        //// add gen jet matching
        //std::vector<int> matchPIDJet;   
        //// so far jets are not
        //// identified with the initial
        //// quark, so only use one PID
        //matchPIDJet.push_back(1);
        ////matchPIDJet.push_back(2);
        ////matchPIDJet.push_back(3);
        ////matchPIDJet.push_back(4);
        ////matchPIDJet.push_back(5);
        ////matchPIDJet.push_back(-1);
        ////matchPIDJet.push_back(-2);
        ////matchPIDJet.push_back(-3);
        ////matchPIDJet.push_back(-4);
        ////matchPIDJet.push_back(-5);
        //minTruthDR = 100.0;
        //matchLV.SetPxPyPzE(0.0, 0.0, 0.0, 0.0);
        //match = HasTruthMatch( phlv, matchPIDJet, 0.2, minTruthDR, matchLV );
        //OUT::ph_truthMatch_jet->push_back( match  );
        //OUT::ph_truthMinDR_jet->push_back( minTruthDR );
        //OUT::ph_truthMatchPt_jet->push_back( matchLV.Pt() );

    }
            
}        

void RunModule::BuildTruth( ModuleConfig & config ) const {

#ifdef EXISTS_GPhotPt

    OUT::trueph_pt->clear();
    OUT::trueph_eta->clear();
    OUT::trueph_phi->clear();
    OUT::trueph_motherPID->clear();
    OUT::trueph_status->clear();
    OUT::trueph_nMatchingLep->clear();

    OUT::truelep_pt->clear();
    OUT::truelep_eta->clear();
    OUT::truelep_phi->clear();
    OUT::truelep_e->clear();
    OUT::truelep_motherPID->clear();
    OUT::truelep_status->clear();
    OUT::truelep_Id->clear();

    OUT::trueph_n = 0;
    OUT::truephIPFS_n = 0;
    OUT::truelep_n = 0;

    std::vector<TLorentzVector> chleplvs;
    std::vector<TLorentzVector> nulvs;
    for( unsigned int idx = 0; idx < IN::GLepBarePt->size(); ++idx ) {

        int truelep_motherId = IN::GLepBareMomId->at(idx);
        int id = IN::GLepBareId->at(idx);

        if( fabs( truelep_motherId ) <= 25 ) {

            if( !config.PassInt( "cut_lep_mother", truelep_motherId ) ) continue;

            TLorentzVector lv;
            lv.SetPtEtaPhiE( IN::GLepBarePt->at(idx),
                             IN::GLepBareEta->at(idx),
                             IN::GLepBarePhi->at(idx),
                             IN::GLepBareE->at(idx)
                    );
            OUT::truelep_pt->push_back(lv.Pt());
            OUT::truelep_eta->push_back(lv.Eta());
            OUT::truelep_phi->push_back(lv.Phi());
            OUT::truelep_e->push_back(lv.E());
            OUT::truelep_motherPID->push_back(IN::GLepBareMomId->at(idx));
            OUT::truelep_status->push_back(IN::GLepBareSt->at(idx));
            OUT::truelep_Id->push_back(IN::GLepBareId->at(idx));
            OUT::truelep_n++;

            if( abs(id) == 11 || abs(id) == 13 || abs(id) == 15 ) {
                chleplvs.push_back( lv );
            }
            if( abs(id) == 12 || abs(id) == 14 || abs(id) == 16 ) {
                nulvs.push_back( lv );
            }
        }
    }


    // first sort by the photon pt. Apply the pt filter here
    std::vector<std::pair< float, unsigned > > sorted_photons;
    for( unsigned int idx = 0; idx < IN::GPhotPt->size(); ++idx ) {

        if( !config.PassFloat( "cut_ph_pt", IN::GPhotPt->at(idx) ) ) continue;

        sorted_photons.push_back( std::make_pair( IN::GPhotPt->at(idx), idx ) );
    }

    std::sort( sorted_photons.rbegin(), sorted_photons.rend() );
    std::vector<TLorentzVector> photlvs;

    // now fill in order
    for( std::vector<std::pair<float, unsigned > >::const_iterator itr = sorted_photons.begin(); itr != sorted_photons.end(); ++itr ) {

        unsigned idx = itr->second;

        if( !config.PassInt( "cut_ph_mother", abs(IN::GPhotMotherId->at(idx) ) ) ) continue;
        if( !config.PassInt( "cut_ph_status", IN::GPhotSt->at(idx) ) ) continue;
        if( !config.PassBool( "cut_ph_IsPromptFinalState", IN::GPhotIsPromptFinalState->at(idx) ) ) continue;
        if( !config.PassBool( "cut_ph_FromHardProcessFinalState", IN::GPhotFromHardProcessFinalState->at(idx) ) ) continue;

        TLorentzVector lv;
        lv.SetPtEtaPhiM( IN::GPhotPt->at(idx),
                         IN::GPhotEta->at(idx),
                         IN::GPhotPhi->at(idx),
                         0.0
                );

        photlvs.push_back(lv);

        OUT::trueph_pt->push_back( lv.Pt() );
        OUT::trueph_eta->push_back( lv.Eta() );
        OUT::trueph_phi->push_back( lv.Phi() );
        OUT::trueph_motherPID->push_back( IN::GPhotMotherId->at(idx) );
        OUT::trueph_status->push_back( IN::GPhotSt->at(idx) );
        OUT::trueph_n++;

        if( IN::GPhotIsPromptFinalState->at(idx) ) {
            OUT::truephIPFS_n++;
        }

        int nMatchingLep = 0;
        for( unsigned lepidx = 0; lepidx < chleplvs.size(); ++lepidx ) {

            float dr = lv.DeltaR( chleplvs[lepidx] );

            if( dr < 0.1 ) {
                nMatchingLep++;
            }
        }

        OUT::trueph_nMatchingLep->push_back(nMatchingLep);
    }
    OUT::truechlep_n = chleplvs.size();
    OUT::truenu_n = nulvs.size();
    OUT::truelepnu_m = 0.0;
    OUT::truelepnuph_m = 0.0;
    OUT::truelepph_dr = 0.0;

    if( OUT::truechlep_n == 1 ) {
        TLorentzVector wlv( chleplvs[0] );

        for( unsigned i = 0 ; i < nulvs.size(); ++i) {
            wlv = wlv + nulvs[i];
        }
        OUT::truelepnu_m = wlv.M();

        if( photlvs.size() > 0 ) {
            OUT::truelepnuph_m = (wlv + photlvs[0]).M();
            OUT::truelepph_dr =  chleplvs[0].DeltaR( photlvs[0] );
        }
    }

    OUT::st3Lep_n = IN::GLepSt3Pt->size();
    OUT::isWMuDecay = false;
    OUT::isWElDecay = false;
    OUT::isWTauDecay = false;
    OUT::isWTauElDecay = false;
    OUT::isWTauMuDecay = false;
    OUT::WIDStep = 0;
    bool found_w_mother = false;
    for( unsigned int idx = 0; idx < IN::GLepSt3Pt->size(); ++idx ) {
        if( fabs(IN::GLepSt3Mother0Id->at(idx)) == 24 ) {
            found_w_mother = true;

            int lep_id = IN::GLepSt3Id->at(idx);
            if( fabs(lep_id) == 11 || fabs(lep_id) == 12 ) {
                OUT::isWElDecay=true;
            }
            if( fabs(lep_id) == 13 || fabs(lep_id) == 14 ) {
                OUT::isWMuDecay=true;
            }
            if( fabs(lep_id) == 15 || fabs(lep_id) == 16 ) {
                OUT::isWTauDecay=true;
            }
        }
    }

    if( !found_w_mother ) {
        OUT::WIDStep++;
        for( unsigned int idx = 0; idx < IN::GLepBarePt->size(); ++idx ) {
            if( fabs(IN::GLepBareMomId->at(idx)) == 24 ) {
                found_w_mother = true;

                int lep_id = IN::GLepBareId->at(idx);
                if( fabs(lep_id) == 11 || fabs(lep_id) == 12 ) {
                    OUT::isWElDecay=true;
                }
                if( fabs(lep_id) == 13 || fabs(lep_id) == 14 ) {
                    OUT::isWMuDecay=true;
                }
                if( fabs(lep_id) == 15 || fabs(lep_id) == 16 ) {
                    OUT::isWTauDecay=true;
                }
            }
        }
    }
    if( !found_w_mother ) {
        OUT::WIDStep++;
        int n_el    = 0;
        int n_mu    = 0;
        int n_tau   = 0;
        int n_elnu  = 0;
        int n_munu  = 0;
        int n_taunu = 0;
        for( unsigned int idx = 0; idx < IN::GLepBarePt->size(); ++idx ) {

            int momId = abs(IN::GLepBareMomId->at(idx));
            int Id    = abs(IN::GLepBareId   ->at(idx));

            if( ( Id == momId) || ( momId == 15 ) ) {

                if( Id == 11 ) n_el++;
                if( Id == 12 ) n_elnu++;
                if( Id == 13 ) n_mu++;
                if( Id == 14 ) n_munu++;
                if( Id == 15 ) n_tau++;
                if( Id == 16 ) n_taunu++;

            }
        }

        // if anything tau-like is present then its a tau decay
        if( n_taunu > 0 || n_tau > 0 ) {
            found_w_mother = true;
            OUT::isWTauDecay = true;
        }
        // otherwise the final state objects should be consistent with a W decay
        else if( n_munu > 0 && n_mu > 0 ) {
            OUT::isWMuDecay = true;
        }
        // otherwise the final state objects should be consistent with a W decay
        else if( n_elnu > 0 && n_el > 0 ) {
            OUT::isWElDecay = true;
        }
    }


    if( OUT::isWTauDecay ) {
        std::vector<std::pair<float, int> > found_leptons;
        for( unsigned int idx = 0; idx < IN::GLepBarePt->size(); ++idx ) {
            if( fabs(IN::GLepBareMomId->at(idx)) == 15 && (fabs( IN::GLepBareId->at(idx)) == 11 || fabs(IN::GLepBareId->at(idx)) == 13) ) {

                found_leptons.push_back( std::make_pair( IN::GLepBarePt->at(idx), idx ) );
            }
        }
        std::sort( found_leptons.rbegin(), found_leptons.rend() );

        if( found_leptons.size() > 0 ) {
            int lep_id = IN::GLepBareId->at(found_leptons[0].second);
            if( fabs(lep_id) == 11 ) {
                OUT::isWTauElDecay=true;
            }
            if( fabs(lep_id) == 13 ) {
                OUT::isWTauMuDecay =true;
            }
        }
    }


#endif
}






bool RunModule::FilterEvent( ModuleConfig & config ) const {

    bool keep_event = true;
    if( !config.PassInt("cut_el_n", OUT::el_n ) ) keep_event = false;
    if( !config.PassInt("cut_mu_n", OUT::mu_n ) ) keep_event = false;

    return keep_event;

    
}

void RunModule::WeightEvent( ModuleConfig & config ) const {

    OUT::NLOWeight = 1.0;
    if( !IN::EvtIsRealData && _needs_nlo_weght ) {
        if( IN::EvtWeights->at(0) < 0 ) {
            OUT::NLOWeight = -1.0;
        }
    }

    if( !_puweight_data_hist || !_puweight_sample_hist ) {
        return;
    }
    float puval = -1;
    puval = IN::EvtPuCntTruth;
    //#ifdef EXISTS_nVtx
    //puval = IN::nVtx;
    //#endif

    OUT::PUWeight = calc_pu_weight( puval );

    OUT::PUWeightUP5 = calc_pu_weight( puval, 1.05 );
    OUT::PUWeightUP10 = calc_pu_weight( puval, 1.10 );

    OUT::PUWeightDN5 = calc_pu_weight( puval, 0.95 );
    OUT::PUWeightDN10 = calc_pu_weight( puval, 0.9 );
    
}

float RunModule::calc_pu_weight( float puval, float mod ) const {

    float tot_data   = _puweight_data_hist->Integral();
    float tot_sample = _puweight_sample_hist->Integral();

    int bin_sample = _puweight_sample_hist->FindBin(puval);
    int bin_data = _puweight_data_hist->FindBin(mod*puval);

    float val_data = _puweight_data_hist->GetBinContent( bin_data );
    float val_sample = _puweight_sample_hist->GetBinContent( bin_sample );

    float num = val_data*mod/tot_data;
    float den = val_sample/tot_sample;

    float weight = num/den;

    //std::cout << "puval = " << puval << " data_val = " << val_data << " sample_val = " << val_sample << " num = " << num << " den = " << den << " weight = " << weight << std::endl;

    if( weight < 0.00000005 ) {

        int bin_min_sample = _puweight_sample_hist->FindBin(puval-2.5);
        int bin_max_sample = _puweight_sample_hist->FindBin(puval+2.5);
        int bin_min_data = _puweight_data_hist->FindBin(puval*mod-2.5);
        int bin_max_data = _puweight_data_hist->FindBin(puval*mod+2.5);

        val_data = _puweight_data_hist->Integral(bin_min_data, bin_max_data);
        val_sample = _puweight_sample_hist->Integral(bin_min_sample, bin_max_sample);

        num = val_data/tot_data;
        den = val_sample/tot_sample;

        weight = num/den;

    }
    return weight;
}

//
bool RunModule::HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR ) const {
    
    float minDR = 100.0;
    TLorentzVector matchLV;
    return HasTruthMatch( objlv, matchPID, maxDR, minDR, matchLV );

}

bool RunModule::HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR ) const {
    
    TLorentzVector matchLV;
    return HasTruthMatch( objlv, matchPID, maxDR, minDR, matchLV );

}

bool RunModule::HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR, TLorentzVector &matchLV ) const {
    
    int motherPID = 0;
    int parentage = -1;
    return HasTruthMatch( objlv, matchPID, maxDR, minDR, matchLV, motherPID, parentage );

}

bool RunModule::HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float & minDR, TLorentzVector & matchLV, int &matchMotherPID, int &matchParentage  ) const {
   
    minDR = 100.0;
    matchLV.SetPxPyPzE(0.0, 0.0, 0.0, 0.0);
    bool match=false;
#ifdef EXISTS_GPhotPt
#ifdef EXISTS_GLepDr01Pt

    // store commom formats for all
    // information 
    std::vector<int> match_pid;
    std::vector<TLorentzVector> match_tlv;
    std::vector<int> match_momPID;
    std::vector<int> match_parentage;
    BOOST_FOREACH( int mpid, matchPID ) {

        // use photons
        if( mpid == 22 ) {

            for( int gidx = 0; gidx < OUT::trueph_n; ++gidx ) {

                TLorentzVector mclv;
                mclv.SetPtEtaPhiM( OUT::trueph_pt->at(gidx), 
                                   OUT::trueph_eta->at(gidx), 
                                   OUT::trueph_phi->at(gidx), 
                                   0. );

                match_pid.push_back( mpid );
                match_tlv.push_back( mclv );
                match_momPID.push_back( OUT::trueph_motherPID->at(gidx) );
                match_parentage.push_back( 0 );
            }
        }
        else if( mpid==11 || mpid==13 || mpid==-11 || mpid==-13 ) {
            for( int lidx = 0; lidx < OUT::truelep_n; ++lidx ) {

                // only use this lepton type
                if( mpid != OUT::truelep_Id->at(lidx) ) continue;

                TLorentzVector mclv;
                mclv.SetPtEtaPhiE( OUT::truelep_pt->at(lidx), 
                                   OUT::truelep_eta->at(lidx), 
                                   OUT::truelep_phi->at(lidx), 
                                   OUT::truelep_e->at(lidx) );

                match_pid.push_back( mpid );
                match_tlv.push_back( mclv );
                match_momPID.push_back( OUT::truelep_motherPID->at(lidx) );
                match_parentage.push_back( 0 );
            }
        }
        //else {
        //    for( unsigned lidx = 0; lidx < IN::GJetAk04Pt->size(); ++lidx ) {
        //        TLorentzVector mclv;
        //        mclv.SetPtEtaPhiE( IN::GJetAk04Pt->at(lidx), IN::GJetAk04Eta->at(lidx), IN::GJetAk04Phi->at(lidx), IN::GJetAk04E->at(lidx) );

        //        match_pid.push_back( mpid );
        //        match_tlv.push_back( mclv );
        //        // FIX should be filled with the originator quark/gluon
        //        match_momPID.push_back( 1 );
        //        match_parentage.push_back( 0 );
        //    }
        //}


    }

    for( unsigned idx = 0; idx < match_tlv.size(); ++idx ) {

        float dr = match_tlv[idx].DeltaR( objlv );
        //std::cout << "dr = " << dr << std::endl;
        if( dr < maxDR) {
            match = true;
            matchMotherPID = match_momPID[idx];
            matchParentage = match_parentage[idx]; 
        }
        // store the minimum delta R
        if( dr < minDR ) {
            minDR = dr;
            matchLV = match_tlv[idx];
        }
    }

#endif
#endif
    return match;

}

void RunModule::calc_corr_iso( float chIso, float phoIso, float neuIso, float rho, float eta, float &chIsoCorr, float &phoIsoCorr, float &neuIsoCorr )  const
{

    // from https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonIdentificationRun2#Selection_implementation_details
    // updated Dec 2016
    
    float ea_ch=0.0;
    float ea_pho=0.0;
    float ea_neu=0.0;

    if( fabs( eta ) < 1.0 ) {
        ea_ch = 0.0360;
        ea_neu = 0.0597;
        ea_pho = 0.1210;
    }
    else if( fabs(eta) >= 1.0 && fabs( eta ) < 1.479 ) {
        ea_ch = 0.0377;
        ea_neu = 0.0807;
        ea_pho = 0.1107;
    }
    else if( fabs(eta) >= 1.479 && fabs( eta ) < 2.0 ) {
        ea_ch = 0.0306;
        ea_neu = 0.0629;
        ea_pho = 0.0699;
    }
    else if( fabs(eta) >= 2.0 && fabs( eta ) < 2.2 ) {
        ea_ch = 0.0283;
        ea_neu = 0.0197;
        ea_pho = 0.1056;
    }
    else if( fabs(eta) >= 2.2 && fabs( eta ) < 2.3 ) {
        ea_ch = 0.0254;
        ea_neu = 0.0184;
        ea_pho = 0.1457;
    }
    else if( fabs(eta) >= 2.3 && fabs( eta ) < 2.4 ) {
        ea_ch = 0.0217;
        ea_neu = 0.0284;
        ea_pho = 0.1719;
    }
    else if( fabs(eta) >= 2.4 ) {
        ea_ch = 0.0167;
        ea_neu = 0.0591;
        ea_pho = 0.1998;
    }

    chIsoCorr  = chIso  - rho*ea_ch;
    phoIsoCorr = phoIso - rho*ea_pho;
    neuIsoCorr = neuIso - rho*ea_neu;

    if( chIsoCorr < 0 ) {
        chIsoCorr = 0;
    }
    if( phoIsoCorr < 0 ) {
        phoIsoCorr = 0;
    }
    if( neuIsoCorr < 0 ) {
        neuIsoCorr = 0;
    }

}


        



//float RunModule::GetElectronMomentumCorrection( float pt, float sceta, float eta, float r9, bool isData, int run ) {
//
//    bool isEB = (fabs(sceta) < 1.479);
//
//    if( isData ) {
//
//        if( !electron_corr_vals.size() ) {
//            std::cout << "No values loaded for data corrections " << std::endl;
//            return 1.0;
//        }
//
//        float scale = -1;
//        bool set_scale = false;
//        BOOST_FOREACH( const correctionValues & vals, electron_corr_vals ) {
//
//            if ( (run >= vals.nRunMin ) && ( run <= vals.nRunMax ) ) {
//
//                if ( isEB  && fabs(eta) < 1  && r9 <  0.94 ) scale = vals.corrCat0;
//                if ( isEB  && fabs(eta) < 1  && r9 >= 0.94 ) scale = vals.corrCat1;
//                if ( isEB  && fabs(eta) >= 1 && r9 <  0.94 ) scale = vals.corrCat2;
//                if ( isEB  && fabs(eta) >= 1 && r9 >= 0.94 ) scale = vals.corrCat3;
//                if ( !isEB && fabs(eta) < 2  && r9 <  0.94 ) scale = vals.corrCat4;
//                if ( !isEB && fabs(eta) < 2  && r9 >= 0.94 ) scale = vals.corrCat5;
//                if ( !isEB && fabs(eta) >= 2 && r9 <  0.94 ) scale = vals.corrCat6;
//                if ( !isEB && fabs(eta) >= 2 && r9 >= 0.94 ) scale = vals.corrCat7;
//
//                if( scale < 0 ) {
//                    std::cout << "Did not get a scale " << std::endl;
//                    break;
//                }
//
//                set_scale = true;
//            }
//        }
//
//        if( !set_scale ) {
//            std::cout << "Did not set a scale, check input vals " << std::endl;
//            return 1.0;
//        }
//        else {
//            return scale;
//        }
//    }
//    else {
//
//        float dsigMC = 0;
//        if ( isEB  && fabs(eta) <  1 && r9 <  0.94 ) dsigMC = 0.0099;
//        if ( isEB  && fabs(eta) <  1 && r9 >= 0.94 ) dsigMC = 0.0103;
//        if ( isEB  && fabs(eta) >= 1 && r9 <  0.94 ) dsigMC = 0.0219;
//        if ( isEB  && fabs(eta) >= 1 && r9 >= 0.94 ) dsigMC = 0.0158;
//        if ( !isEB && fabs(eta) <  2 && r9 <  0.94 ) dsigMC = 0.0222;
//        if ( !isEB && fabs(eta) <  2 && r9 >= 0.94 ) dsigMC = 0.0298;
//        if ( !isEB && fabs(eta) >= 2 && r9 <  0.94 ) dsigMC = 0.0318;
//        if ( !isEB && fabs(eta) >= 2 && r9 >= 0.94 ) dsigMC = 0.0302;   
//
//        float corr = _rand.Gaus( 1.0, dsigMC );
//        return corr; 
//    }
//
//}
//
//void RunModule::extractElectronCorrections( const std::string & filename ) {
//
//    ifstream file( filename.c_str() );
//
//    if( !file ) {
//        std::cout << "Could not open file " << filename << std::endl;
//        return;
//    }
//
//    electron_corr_vals.clear();
//
//    while( !file.eof() ) {
//
//        std::string line;
//        getline( file, line );
//        if( line.empty() ) continue;
//        std::vector<std::string> line_tok = Tokenize( line, ", " );
//        if( line_tok.size() != 10 ) {
//            std::cout << "Did not read the correct number of lines! " << std::endl;
//            continue;
//        }
//
//        correctionValues vals;
//        bool all_success = true;
//        all_success &= Utils::stringToInt(line_tok[0], vals.nRunMin);
//        all_success &= Utils::stringToInt(line_tok[1], vals.nRunMax);
//        all_success &= Utils::stringToDouble(line_tok[2], vals.corrCat0);
//        all_success &= Utils::stringToDouble(line_tok[3], vals.corrCat1);
//        all_success &= Utils::stringToDouble(line_tok[4], vals.corrCat2);
//        all_success &= Utils::stringToDouble(line_tok[5], vals.corrCat3);
//        all_success &= Utils::stringToDouble(line_tok[6], vals.corrCat4);
//        all_success &= Utils::stringToDouble(line_tok[7], vals.corrCat5);
//        all_success &= Utils::stringToDouble(line_tok[8], vals.corrCat6);
//        all_success &= Utils::stringToDouble(line_tok[9], vals.corrCat7);
//
//        if( !all_success ) {
//            std::cout << "Failed to set at least some electron correction values" << std::endl;
//        }
//
//        electron_corr_vals.push_back(vals);
//
//    }
//
//    file.close();
//
//}
//
//
//void RunModule::extractElectronLinCorrections( const std::string & filename ) {
//
//    ifstream file( filename.c_str() );
//
//    if( !file ) {
//        std::cout << "Could not open file " << filename << std::endl;
//        return;
//    }
//
//    electron_lincorr_vals.clear();
//    while( !file.eof() ) {
//
//        std::string line;
//        getline( file, line );
//        if( line.empty() ) continue;
//        std::vector<std::string> line_tok = Tokenize( line, ", " );
//        if( line_tok.size() != 8 ) {
//            std::cout << "Did not read the correct number of lines! " << std::endl;
//            continue;
//        }
//
//        linearityCorrectionValues vals;
//        bool all_success=true;
//        all_success &= Utils::stringToDouble(line_tok[0], vals.ptMin);
//        all_success &= Utils::stringToDouble(line_tok[1], vals.ptMax);
//        all_success &= Utils::stringToDouble(line_tok[2], vals.corrCat0);
//        all_success &= Utils::stringToDouble(line_tok[3], vals.corrCat1);
//        all_success &= Utils::stringToDouble(line_tok[4], vals.corrCat2);
//        all_success &= Utils::stringToDouble(line_tok[5], vals.corrCat3);
//        all_success &= Utils::stringToDouble(line_tok[6], vals.corrCat4);
//        all_success &= Utils::stringToDouble(line_tok[7], vals.corrCat5);
//
//        if( !all_success ) {
//            std::cout << "Failed to set at least some electron linear correction values" << std::endl;
//        }
//        electron_lincorr_vals.push_back(vals);
//
//    }
//
//    file.close();
//
//}
//
void RunModule::BuildTriggerBits( ModuleConfig & config ) const {

  //std::cout << std::bitset<64>(IN::TrigHltPhot) << std::endl;

    // Use scripts/write_trigger_code_from_ntuple.py
    // to help generate the code 
    //Fill trigger branches for TrigHltPhot
    OUT::passTrig_HLT_Photon250_NoHE                     = (IN::TrigHltPhot & ( ULong64_t(1) << 0 ) ) == ( ULong64_t(1) << 0 ); 
    OUT::passTrig_HLT_Photon300_NoHE                     = (IN::TrigHltPhot & ( ULong64_t(1) << 1 ) ) == ( ULong64_t(1) << 1 ); 
    OUT::passTrig_HLT_Photon22                           = (IN::TrigHltPhot & ( ULong64_t(1) << 12 ) ) == ( ULong64_t(1) << 12 ); 
    OUT::passTrig_HLT_Photon30                           = (IN::TrigHltPhot & ( ULong64_t(1) << 13 ) ) == ( ULong64_t(1) << 13 ); 
    OUT::passTrig_HLT_Photon36                           = (IN::TrigHltPhot & ( ULong64_t(1) << 14 ) ) == ( ULong64_t(1) << 14 ); 
    OUT::passTrig_HLT_Photon50                           = (IN::TrigHltPhot & ( ULong64_t(1) << 15 ) ) == ( ULong64_t(1) << 15 ); 
    OUT::passTrig_HLT_Photon75                           = (IN::TrigHltPhot & ( ULong64_t(1) << 16 ) ) == ( ULong64_t(1) << 16 ); 
    OUT::passTrig_HLT_Photon90                           = (IN::TrigHltPhot & ( ULong64_t(1) << 17 ) ) == ( ULong64_t(1) << 17 ); 
    OUT::passTrig_HLT_Photon120                          = (IN::TrigHltPhot & ( ULong64_t(1) << 18 ) ) == ( ULong64_t(1) << 18 ); 
    OUT::passTrig_HLT_Photon175                          = (IN::TrigHltPhot & ( ULong64_t(1) << 19 ) ) == ( ULong64_t(1) << 19 ); 
    OUT::passTrig_HLT_Photon500                          = (IN::TrigHltPhot & ( ULong64_t(1) << 20 ) ) == ( ULong64_t(1) << 20 ); 
    OUT::passTrig_HLT_Photon600                          = (IN::TrigHltPhot & ( ULong64_t(1) << 21 ) ) == ( ULong64_t(1) << 21 ); 
    OUT::passTrig_HLT_Photon165_HE10                     = (IN::TrigHltPhot & ( ULong64_t(1) << 22 ) ) == ( ULong64_t(1) << 22 ); 
    OUT::passTrig_HLT_Photon120_R9Id90_HE10_IsoM         = (IN::TrigHltPhot & ( ULong64_t(1) << 29 ) ) == ( ULong64_t(1) << 29 ); 
    OUT::passTrig_HLT_Photon165_R9Id90_HE10_IsoM         = (IN::TrigHltPhot & ( ULong64_t(1) << 30 ) ) == ( ULong64_t(1) << 30 ); 
    OUT::passTrig_HLT_Photon120_R9Id90_HE10_Iso40_EBOnly = (IN::TrigHltPhot & ( ULong64_t(1) << 36 ) ) == ( ULong64_t(1) << 36 ); 
    OUT::passTrig_HLT_Photon135_PFMET100_JetIdCleaned    = (IN::TrigHltPhot & ( ULong64_t(1) << 40 ) ) == ( ULong64_t(1) << 40 ); 
    //Fill trigger branches for TrigHltMu
    OUT::passTrig_HLT_Mu8                                = (IN::TrigHltMu & ( ULong64_t(1) << 0 ) ) == ( ULong64_t(1) << 0 ); 
    OUT::passTrig_HLT_Mu17                               = (IN::TrigHltMu & ( ULong64_t(1) << 1 ) ) == ( ULong64_t(1) << 1 ); 
    OUT::passTrig_HLT_Mu20                               = (IN::TrigHltMu & ( ULong64_t(1) << 2 ) ) == ( ULong64_t(1) << 2 ); 
    OUT::passTrig_HLT_Mu24                               = (IN::TrigHltMu & ( ULong64_t(1) << 3 ) ) == ( ULong64_t(1) << 3 ); 
    OUT::passTrig_HLT_Mu27                               = (IN::TrigHltMu & ( ULong64_t(1) << 4 ) ) == ( ULong64_t(1) << 4 ); 
    OUT::passTrig_HLT_Mu34                               = (IN::TrigHltMu & ( ULong64_t(1) << 5 ) ) == ( ULong64_t(1) << 5 ); 
    OUT::passTrig_HLT_Mu50                               = (IN::TrigHltMu & ( ULong64_t(1) << 6 ) ) == ( ULong64_t(1) << 6 ); 
    OUT::passTrig_HLT_Mu55                               = (IN::TrigHltMu & ( ULong64_t(1) << 7 ) ) == ( ULong64_t(1) << 7 ); 
    OUT::passTrig_HLT_Mu300                              = (IN::TrigHltMu & ( ULong64_t(1) << 8 ) ) == ( ULong64_t(1) << 8 ); 
    OUT::passTrig_HLT_Mu350                              = (IN::TrigHltMu & ( ULong64_t(1) << 9 ) ) == ( ULong64_t(1) << 9 ); 
    OUT::passTrig_HLT_Mu24_eta2p1                        = (IN::TrigHltMu & ( ULong64_t(1) << 10 ) ) == ( ULong64_t(1) << 10 ); 
    OUT::passTrig_HLT_Mu45_eta2p1                        = (IN::TrigHltMu & ( ULong64_t(1) << 11 ) ) == ( ULong64_t(1) << 11 ); 
    OUT::passTrig_HLT_Mu50_eta2p1                        = (IN::TrigHltMu & ( ULong64_t(1) << 12 ) ) == ( ULong64_t(1) << 12 ); 
    OUT::passTrig_HLT_TkMu20                             = (IN::TrigHltMu & ( ULong64_t(1) << 17 ) ) == ( ULong64_t(1) << 17 ); 
    OUT::passTrig_HLT_TkMu27                             = (IN::TrigHltMu & ( ULong64_t(1) << 18 ) ) == ( ULong64_t(1) << 18 ); 
    OUT::passTrig_HLT_TkMu24_eta2p1                      = (IN::TrigHltMu & ( ULong64_t(1) << 19 ) ) == ( ULong64_t(1) << 19 ); 
    OUT::passTrig_HLT_IsoMu20                            = (IN::TrigHltMu & ( ULong64_t(1) << 21 ) ) == ( ULong64_t(1) << 21 ); 
    OUT::passTrig_HLT_IsoMu22                            = (IN::TrigHltMu & ( ULong64_t(1) << 22 ) ) == ( ULong64_t(1) << 22 ); 
    OUT::passTrig_HLT_IsoMu24                            = (IN::TrigHltMu & ( ULong64_t(1) << 23 ) ) == ( ULong64_t(1) << 23 ); 
    OUT::passTrig_HLT_IsoMu27                            = (IN::TrigHltMu & ( ULong64_t(1) << 24 ) ) == ( ULong64_t(1) << 24 ); 
    OUT::passTrig_HLT_IsoMu17_eta2p1                     = (IN::TrigHltMu & ( ULong64_t(1) << 25 ) ) == ( ULong64_t(1) << 25 ); 
    OUT::passTrig_HLT_IsoMu20_eta2p1                     = (IN::TrigHltMu & ( ULong64_t(1) << 26 ) ) == ( ULong64_t(1) << 26 ); 
    OUT::passTrig_HLT_IsoMu24_eta2p1                     = (IN::TrigHltMu & ( ULong64_t(1) << 27 ) ) == ( ULong64_t(1) << 27 ); 
    OUT::passTrig_HLT_IsoTkMu20                          = (IN::TrigHltMu & ( ULong64_t(1) << 29 ) ) == ( ULong64_t(1) << 29 ); 
    OUT::passTrig_HLT_IsoTkMu22                          = (IN::TrigHltMu & ( ULong64_t(1) << 30 ) ) == ( ULong64_t(1) << 30 ); 
    OUT::passTrig_HLT_IsoTkMu24                          = (IN::TrigHltMu & ( ULong64_t(1) << 31 ) ) == ( ULong64_t(1) << 31 ); 
    OUT::passTrig_HLT_IsoTkMu27                          = (IN::TrigHltMu & ( ULong64_t(1) << 32 ) ) == ( ULong64_t(1) << 32 ); 
    OUT::passTrig_HLT_IsoTkMu20_eta2p1                   = (IN::TrigHltMu & ( ULong64_t(1) << 33 ) ) == ( ULong64_t(1) << 33 ); 
    OUT::passTrig_HLT_IsoTkMu24_eta2p1                   = (IN::TrigHltMu & ( ULong64_t(1) << 34 ) ) == ( ULong64_t(1) << 34 ); 
    //Fill trigger branches for TrigHltDiPhot
    //Fill trigger branches for TrigHlt
    //Fill trigger branches for TrigHltElMu
    OUT::passTrig_HLT_Mu17_Photon30_CaloIdL_L1ISO        = (IN::TrigHltElMu & ( ULong64_t(1) << 8 ) ) == ( ULong64_t(1) << 8 ); 
    //Fill trigger branches for TrigHltEl
    OUT::passTrig_HLT_Ele22_eta2p1_WPLoose_Gsf           = (IN::TrigHltEl & ( ULong64_t(1) << 0 ) ) == ( ULong64_t(1) << 0 ); 
    OUT::passTrig_HLT_Ele22_eta2p1_WPTight_Gsf           = (IN::TrigHltEl & ( ULong64_t(1) << 1 ) ) == ( ULong64_t(1) << 1 ); 
    OUT::passTrig_HLT_Ele23_WPLoose_Gsf                  = (IN::TrigHltEl & ( ULong64_t(1) << 2 ) ) == ( ULong64_t(1) << 2 ); 
    OUT::passTrig_HLT_Ele24_eta2p1_WPLoose_Gsf           = (IN::TrigHltEl & ( ULong64_t(1) << 3 ) ) == ( ULong64_t(1) << 3 ); 
    OUT::passTrig_HLT_Ele25_WPTight_Gsf                  = (IN::TrigHltEl & ( ULong64_t(1) << 4 ) ) == ( ULong64_t(1) << 4 ); 
    OUT::passTrig_HLT_Ele25_eta2p1_WPLoose_Gsf           = (IN::TrigHltEl & ( ULong64_t(1) << 5 ) ) == ( ULong64_t(1) << 5 ); 
    OUT::passTrig_HLT_Ele25_eta2p1_WPTight_Gsf           = (IN::TrigHltEl & ( ULong64_t(1) << 6 ) ) == ( ULong64_t(1) << 6 ); 
    OUT::passTrig_HLT_Ele27_WPTight_Gsf                  = (IN::TrigHltEl & ( ULong64_t(1) << 8 ) ) == ( ULong64_t(1) << 8 ); 
    OUT::passTrig_HLT_Ele27_eta2p1_WPLoose_Gsf           = (IN::TrigHltEl & ( ULong64_t(1) << 9 ) ) == ( ULong64_t(1) << 9 ); 
    OUT::passTrig_HLT_Ele27_eta2p1_WPTight_Gsf           = (IN::TrigHltEl & ( ULong64_t(1) << 10 ) ) == ( ULong64_t(1) << 10 ); 
    OUT::passTrig_HLT_Ele32_eta2p1_WPLoose_Gsf           = (IN::TrigHltEl & ( ULong64_t(1) << 11 ) ) == ( ULong64_t(1) << 11 ); 
    OUT::passTrig_HLT_Ele32_eta2p1_WPTight_Gsf           = (IN::TrigHltEl & ( ULong64_t(1) << 12 ) ) == ( ULong64_t(1) << 12 ); 
    OUT::passTrig_HLT_Ele105_CaloIdVT_GsfTrkIdT          = (IN::TrigHltEl & ( ULong64_t(1) << 15 ) ) == ( ULong64_t(1) << 15 ); 
    OUT::passTrig_HLT_Ele115_CaloIdVT_GsfTrkIdT          = (IN::TrigHltEl & ( ULong64_t(1) << 16 ) ) == ( ULong64_t(1) << 16 ); 
    //Fill trigger branches for TrigHltDiMu
    OUT::passTrig_HLT_Mu17_Mu8                           = (IN::TrigHltDiMu & ( ULong64_t(1) << 0 ) ) == ( ULong64_t(1) << 0 ); 
    OUT::passTrig_HLT_Mu17_Mu8_DZ                        = (IN::TrigHltDiMu & ( ULong64_t(1) << 1 ) ) == ( ULong64_t(1) << 1 ); 
    OUT::passTrig_HLT_Mu20_Mu10                          = (IN::TrigHltDiMu & ( ULong64_t(1) << 3 ) ) == ( ULong64_t(1) << 3 ); 
    OUT::passTrig_HLT_Mu20_Mu10_DZ                       = (IN::TrigHltDiMu & ( ULong64_t(1) << 4 ) ) == ( ULong64_t(1) << 4 ); 
    OUT::passTrig_HLT_Mu27_TkMu8                         = (IN::TrigHltDiMu & ( ULong64_t(1) << 12 ) ) == ( ULong64_t(1) << 12 ); 
    OUT::passTrig_HLT_Mu30_TkMu11                        = (IN::TrigHltDiMu & ( ULong64_t(1) << 13 ) ) == ( ULong64_t(1) << 13 ); 
    OUT::passTrig_HLT_Mu40_TkMu11                        = (IN::TrigHltDiMu & ( ULong64_t(1) << 14 ) ) == ( ULong64_t(1) << 14 ); 
    //Fill trigger branches for TrigHltDiEl


}

bool RunModule::FilterDataQuality( ModuleConfig & config) const {

    bool pass_quality = false;
    OUT::PassQuality = -1;

    bool isData = IN::EvtIsRealData;
    int run = IN::EvtRunNum;
    int ls  = IN::EvtLumiNum;

    if( quality_map.size() > 0 && isData ) {

        std::map<int, std::vector<int> >::const_iterator mitr = quality_map.find( run );
        if( mitr != quality_map.end() ) {

            std::vector<int>::const_iterator vitr = std::find( mitr->second.begin(), mitr->second.end(), ls );

            if( vitr != mitr->second.end() ) {
                pass_quality = true;
                OUT::PassQuality = 1;
            }
            else {
                pass_quality = false;
                OUT::PassQuality = 0;
            }
        }
        else {
            pass_quality = false;
            OUT::PassQuality = 0;
        }
    }
    else {
        pass_quality = true;
    }

    return pass_quality;

}

//bool RunModule::FilterTrigger( ModuleConfig & config ) const {
//    
//    bool keep_evt = false;
//    BOOST_FOREACH( const Cut & cut, config.GetCut("cut_trigger").GetCuts() ) {
//       if( IN::HLT[IN::HLTIndex[cut.val_int] ] > 0 ) keep_evt = true;
//    }
//
//    return keep_evt;
////#else 
////    return true;
////#endif
//}

RunModule::RunModule() : 
    eval_mu_loose     ( 0),
    eval_mu_medium     ( 0),
    eval_mu_tight     ( 0),
    eval_ph_tight     ( 0),
    eval_ph_medium    ( 0),
    eval_ph_loose     ( 0),
    eval_el_tight     ( 0),
    eval_el_medium    ( 0),
    eval_el_loose     ( 0),
    eval_el_veryloose ( 0),
    _needs_nlo_weght  ( 0),
    _puweight_sample_hist( 0),
    _puweight_data_hist  ( 0)
{

}
