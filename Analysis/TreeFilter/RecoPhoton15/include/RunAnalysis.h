#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "AnalysisBase.h"

#include <string>
#include <vector>


#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"

// The RunModule inherits from RunModuleBase (an Abstract Base Class )
// defined in the Core package so that all
// RunModules present a common interface in a Run function
// This allows the code defined in this package
// to be run from the Core package to minimize
// code duplication in each module
class RunModule : public virtual RunModuleBase {

    public :

        RunModule();

        // The run function must exist and be defined exactly as this
        // because it is defined in RunModuleBase 
        // in src/RunModule.cxx all the analysis is defind in this RunModule function
        void initialize( TChain * chain, TTree *outtree, TFile *outfile, const CmdOptions & options, std::vector<ModuleConfig> & config) ;
        bool execute( std::vector<ModuleConfig> & config ) ;
        void finalize( ) {};

        // The ApplyModule function calls any other module defined below
        // in src/RunModule.cxx.  This funciton is not strictly required
        // but its a consistent way to apply modules
        bool ApplyModule         ( ModuleConfig & config ) const;

        void calc_corr_iso( float chIso, float phoIso, float neuIso, float rho, float eta, float &chisoCorr, float &phoIsoCorr, float &neuIsoCorr ) const;
        float calc_pu_weight( float puval, float mod=1.0) const;

        // Define modules below.
        void BuildElectron       ( ModuleConfig & config ) const;
        void BuildMuon           ( ModuleConfig & config ) const;
        void BuildPhoton         ( ModuleConfig & config ) const;
        void BuildJet            ( ModuleConfig & config ) const;
        void BuildFatJet         ( ModuleConfig & config ) const;
        void BuildMET            ( ModuleConfig & config ) const;
        void BuildTruth          ( ModuleConfig & config ) const;
        void BuildEvent          ( ModuleConfig & config ) const;
        void BuildTriggerBits    ( ModuleConfig & config ) const;
        void FilterGenPhoton     ( ModuleConfig & config ) const;
        void WeightEvent         ( ModuleConfig & config ) const;
        bool FilterElec          ( ModuleConfig & config ) const;
        bool FilterMuon          ( ModuleConfig & config ) const;
        bool FilterEvent         ( ModuleConfig & config ) const;
        bool FilterTrigger       ( ModuleConfig & config ) const;
        bool FilterDataQuality   ( ModuleConfig & config ) const;

        bool HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR ) const;
        bool HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR ) const;
        bool HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR, TLorentzVector &matchLV ) const;
        bool HasTruthMatch( const TLorentzVector & objlv, const std::vector<int> & matchPID, float maxDR, float &minDR, TLorentzVector &matchLV, int &matchMotherPID, int &matchParentage ) const;

    private :

        bool eval_mu_loose    ;
        bool eval_mu_medium   ;
        bool eval_mu_tight    ;
        bool eval_ph_tight    ;
        bool eval_ph_medium   ;
        bool eval_ph_loose    ;
        bool eval_el_tight    ;
        bool eval_el_medium   ;
        bool eval_el_loose    ;
        bool eval_el_veryloose;
        bool _needs_nlo_weght ;

        std::map<int, std::vector<int> > quality_map;

        TFile * _puweight_sample_file;
        TFile * _puweight_data_file;
        TH1F * _puweight_sample_hist;
        TH1D * _puweight_data_hist;

        
};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

    Int_t              el_n;
    Int_t              mu_n;
    Int_t              ph_n;
    Int_t              jet_n;
    Int_t              jetAK08_n;
    Int_t              vtx_n;
    Int_t              trueph_n;
    Int_t              truephIPFS_n;
    Int_t              truelep_n;


    std::vector<float> *el_pt;
    std::vector<float> *el_eta;
    std::vector<float> *el_sceta;
    std::vector<float> *el_phi;
    std::vector<float> *el_e;
    //std::vector<float> *el_d0pv;
    //std::vector<float> *el_z0pv;
    //std::vector<float> *el_sigmaIEIE;
    //std::vector<float> *el_sigmaIEIEFull5x5;
    //std::vector<float> *el_charge;
    //std::vector<float> *el_ooEmooP;
    //std::vector<int>   *el_passConvVeto;
    //std::vector<float> *el_chHadIso;
    //std::vector<float> *el_neuHadIso;
    //std::vector<float> *el_phoIso;
    //std::vector<float> *el_chHadIsoPuCorr;
    //std::vector<float> *el_rawIso;
    //std::vector<float> *el_dbIso;
    //std::vector<float> *el_rhoIso;
    std::vector<Bool_t> *el_passTight;
    std::vector<Bool_t> *el_passMedium;
    std::vector<Bool_t> *el_passLoose;
    std::vector<Bool_t> *el_passVeryLoose;
    std::vector<Bool_t> *el_passVIDTight;
    std::vector<Bool_t> *el_passVIDMedium;
    std::vector<Bool_t> *el_passVIDLoose;
    std::vector<Bool_t> *el_passVIDVeryLoose;
    std::vector<Bool_t> *el_passVIDHLT;
    std::vector<Bool_t> *el_passVIDHEEP;
    std::vector<Bool_t> *el_truthMatch_el;
    std::vector<float> *el_truthMatchMinDR_el;
    std::vector<float> *el_truthMatchPt_el;
    std::vector<Bool_t> *el_truthMatch_ph;
    std::vector<float> *el_truthMinDR_ph;
    std::vector<float> *el_truthMatchPt_ph;

    std::vector<float>  *mu_pt;
    std::vector<float>  *mu_eta;
    std::vector<float>  *mu_phi;
    std::vector<float>  *mu_e;
    //std::vector<Bool_t> *mu_isGlobal;
    //std::vector<Bool_t> *mu_isPF;
    //std::vector<float>  *mu_chi2;
    //std::vector<int>    *mu_nHits;
    //std::vector<int>    *mu_nMuStations;
    //std::vector<int>    *mu_nPixHits;
    //std::vector<int>    *mu_nTrkLayers;
    std::vector<float>  *mu_d0;
    std::vector<float>  *mu_z0;
    //std::vector<float>  *mu_pfIso_ch;
    //std::vector<float>  *mu_pfIso_nh;
    //std::vector<float>  *mu_pfIso_pho;
    std::vector<float>  *mu_rhoIso;
    std::vector<float>  *mu_pfIso_db;
    //std::vector<float>  *mu_corrIso;
    //std::vector<float>  *mu_trkIso;
    //std::vector<int>    *mu_charge;
    //std::vector<Bool_t> *mu_triggerMatch;
    //std::vector<Bool_t> *mu_triggerMatchDiMu;
    std::vector<Bool_t> *mu_passLoose;
    //std::vector<Bool_t> *mu_passCustom;
    std::vector<Bool_t> *mu_passTight;
    std::vector<Bool_t> *mu_passMedium;
    std::vector<Bool_t> *mu_truthMatch_mu;
    std::vector<float>  *mu_truthMatchMinDR_mu;
    std::vector<float>  *mu_truthMatchPt_mu;

    std::vector<float>  *ph_pt;
    std::vector<float>  *ph_eta;
    std::vector<float>  *ph_sceta;
    std::vector<float>  *ph_phi;
    std::vector<float>  *ph_scphi;
    std::vector<float>  *ph_e;
    //std::vector<float>  *ph_scE;
    std::vector<float>  *ph_HoverE;
    std::vector<float>  *ph_HoverE12;
    std::vector<float>  *ph_sigmaIEIE;
    //std::vector<float>  *ph_sigmaIEIP;
    //std::vector<float>  *ph_r9;
    //std::vector<float>  *ph_E3x3;
    //std::vector<float>  *ph_E1x5;
    //std::vector<float>  *ph_E2x5;
    //std::vector<float>  *ph_E5x5;
    //std::vector<float>  *ph_SCetaWidth;
    //std::vector<float>  *ph_SCphiWidth;
    //std::vector<float>  *ph_ESEffSigmaRR;
    //std::vector<float>  *ph_hcalIsoDR03;
    //std::vector<float>  *ph_trkIsoHollowDR03;
    //std::vector<float>  *ph_chgpfIsoDR02;
    //std::vector<float>  *ph_pfChIsoWorst;
    std::vector<float>  *ph_chIso;
    std::vector<float>  *ph_neuIso;
    std::vector<float>  *ph_phoIso;
    std::vector<float>  *ph_chIsoCorr;
    std::vector<float>  *ph_neuIsoCorr;
    std::vector<float>  *ph_phoIsoCorr;
    std::vector<Bool_t> *ph_eleVeto;
    std::vector<Bool_t> *ph_hasPixSeed;
    //std::vector<float>  *ph_drToTrk;
    std::vector<Bool_t> *ph_isConv;
    //std::vector<int>    *ph_conv_nTrk;
    //std::vector<float>  *ph_conv_vtx_x;
    //std::vector<float>  *ph_conv_vtx_y;
    //std::vector<float>  *ph_conv_vtx_z;
    //std::vector<float>  *ph_conv_ptin1;
    //std::vector<float>  *ph_conv_ptin2;
    //std::vector<float>  *ph_conv_ptout1;
    //std::vector<float>  *ph_conv_ptout2;
    std::vector<Bool_t> *ph_passTight;
    std::vector<Bool_t> *ph_passMedium;
    std::vector<Bool_t> *ph_passLoose;
    std::vector<Bool_t> *ph_passVIDTight;
    std::vector<Bool_t> *ph_passVIDMedium;
    std::vector<Bool_t> *ph_passVIDLoose;
    std::vector<Bool_t> *ph_passLooseNoSIEIE;
    std::vector<Bool_t> *ph_passHOverELoose;
    std::vector<Bool_t> *ph_passHOverEMedium;
    std::vector<Bool_t> *ph_passHOverETight;
    std::vector<Bool_t> *ph_passSIEIELoose;
    std::vector<Bool_t> *ph_passSIEIEMedium;
    std::vector<Bool_t> *ph_passSIEIETight;
    std::vector<Bool_t> *ph_passChIsoCorrLoose;
    std::vector<Bool_t> *ph_passChIsoCorrMedium;
    std::vector<Bool_t> *ph_passChIsoCorrTight;
    std::vector<Bool_t> *ph_passNeuIsoCorrLoose;
    std::vector<Bool_t> *ph_passNeuIsoCorrMedium;
    std::vector<Bool_t> *ph_passNeuIsoCorrTight;
    std::vector<Bool_t> *ph_passPhoIsoCorrLoose;
    std::vector<Bool_t> *ph_passPhoIsoCorrMedium;
    std::vector<Bool_t> *ph_passPhoIsoCorrTight;
    std::vector<Bool_t> *ph_truthMatch_el;
    std::vector<Bool_t> *ph_truthMatch_ph;
    std::vector<Bool_t> *ph_truthMatch_jet;
    std::vector<float>  *ph_truthMinDR_el;
    std::vector<float>  *ph_truthMatchMinDR_ph;
    std::vector<float>  *ph_truthMinDR_jet;
    std::vector<float>  *ph_truthMatchPt_el;
    std::vector<float>  *ph_truthMatchPt_ph;
    std::vector<float>  *ph_truthMatchPt_jet;
    std::vector<int>    *ph_truthMatchMotherPID_ph;
    std::vector<int>    *ph_truthMatchParentage_ph;
    std::vector<Bool_t> *ph_hasSLConv;
    std::vector<Bool_t> *ph_pass_mva_presel;
    std::vector<float>  *ph_mvascore;
    std::vector<Bool_t>  *ph_IsEB;
    std::vector<Bool_t>  *ph_IsEE;

    std::vector<float>  *jet_pt;
    std::vector<float>  *jet_eta;
    std::vector<float>  *jet_phi;
    std::vector<float>  *jet_e;
    std::vector<float>  *jet_bTagCSVV2;
    std::vector<Bool_t>  *jet_IdLoose;
    std::vector<Bool_t>  *jet_IdTightLep;
    std::vector<Bool_t>  *jet_IdTight;

    std::vector<float>  *jetAK08_pt;
    std::vector<float>  *jetAK08_eta;
    std::vector<float>  *jetAK08_phi;
    std::vector<float>  *jetAK08_e;

    std::vector<float>  *trueph_pt;
    std::vector<float>  *trueph_eta;
    std::vector<float>  *trueph_phi;
    std::vector<int>  *trueph_motherPID;
    std::vector<int>  *trueph_status;
    std::vector<int>  *trueph_nMatchingLep;

    std::vector<float>  *truelep_pt;
    std::vector<float>  *truelep_eta;
    std::vector<float>  *truelep_phi;
    std::vector<float>  *truelep_e;
    std::vector<int>  *truelep_motherPID;
    std::vector<int>  *truelep_status;
    std::vector<int>  *truelep_Id;

    Int_t   truechlep_n;
    Int_t   truenu_n;
    Float_t truelepnu_m;
    Float_t truelepnuph_m;
    Float_t truelepph_dr;

    Int_t st3Lep_n;
    Bool_t isWMuDecay;
    Bool_t isWElDecay;
    Bool_t isWTauDecay;
    Bool_t isWTauElDecay;
    Bool_t isWTauMuDecay;
    Int_t WIDStep;

    Float_t met_pt;
    Float_t met_phi;

    // Use scripts/write_trigger_code_from_ntuple.py
    // to help generate the code 
    //Declare triggers for TrigHltPhot
    Bool_t passTrig_HLT_Photon250_NoHE                    ;
    Bool_t passTrig_HLT_Photon300_NoHE                    ;
    Bool_t passTrig_HLT_Photon22                          ;
    Bool_t passTrig_HLT_Photon30                          ;
    Bool_t passTrig_HLT_Photon36                          ;
    Bool_t passTrig_HLT_Photon50                          ;
    Bool_t passTrig_HLT_Photon75                          ;
    Bool_t passTrig_HLT_Photon90                          ;
    Bool_t passTrig_HLT_Photon120                         ;
    Bool_t passTrig_HLT_Photon175                         ;
    Bool_t passTrig_HLT_Photon500                         ;
    Bool_t passTrig_HLT_Photon600                         ;
    Bool_t passTrig_HLT_Photon165_HE10                    ;
    Bool_t passTrig_HLT_Photon120_R9Id90_HE10_IsoM        ;
    Bool_t passTrig_HLT_Photon165_R9Id90_HE10_IsoM        ;
    Bool_t passTrig_HLT_Photon120_R9Id90_HE10_Iso40_EBOnly;
    Bool_t passTrig_HLT_Photon135_PFMET100_JetIdCleaned   ;
    //Declare triggers for TrigHltMu
    Bool_t passTrig_HLT_Mu8                               ;
    Bool_t passTrig_HLT_Mu17                              ;
    Bool_t passTrig_HLT_Mu20                              ;
    Bool_t passTrig_HLT_Mu24                              ;
    Bool_t passTrig_HLT_Mu27                              ;
    Bool_t passTrig_HLT_Mu34                              ;
    Bool_t passTrig_HLT_Mu50                              ;
    Bool_t passTrig_HLT_Mu55                              ;
    Bool_t passTrig_HLT_Mu300                             ;
    Bool_t passTrig_HLT_Mu350                             ;
    Bool_t passTrig_HLT_Mu24_eta2p1                       ;
    Bool_t passTrig_HLT_Mu45_eta2p1                       ;
    Bool_t passTrig_HLT_Mu50_eta2p1                       ;
    Bool_t passTrig_HLT_TkMu20                            ;
    Bool_t passTrig_HLT_TkMu27                            ;
    Bool_t passTrig_HLT_TkMu24_eta2p1                     ;
    Bool_t passTrig_HLT_IsoMu20                           ;
    Bool_t passTrig_HLT_IsoMu22                           ;
    Bool_t passTrig_HLT_IsoMu24                           ;
    Bool_t passTrig_HLT_IsoMu27                           ;
    Bool_t passTrig_HLT_IsoMu17_eta2p1                    ;
    Bool_t passTrig_HLT_IsoMu20_eta2p1                    ;
    Bool_t passTrig_HLT_IsoMu24_eta2p1                    ;
    Bool_t passTrig_HLT_IsoTkMu20                         ;
    Bool_t passTrig_HLT_IsoTkMu22                         ;
    Bool_t passTrig_HLT_IsoTkMu24                         ;
    Bool_t passTrig_HLT_IsoTkMu27                         ;
    Bool_t passTrig_HLT_IsoTkMu20_eta2p1                  ;
    Bool_t passTrig_HLT_IsoTkMu24_eta2p1                  ;
    //Declare triggers for TrigHltDiPhot
    //Declare triggers for TrigHlt
    //Declare triggers for TrigHltElMu
    Bool_t passTrig_HLT_Mu17_Photon30_CaloIdL_L1ISO       ;
    //Declare triggers for TrigHltEl
    Bool_t passTrig_HLT_Ele22_eta2p1_WPLoose_Gsf          ;
    Bool_t passTrig_HLT_Ele22_eta2p1_WPTight_Gsf          ;
    Bool_t passTrig_HLT_Ele23_WPLoose_Gsf                 ;
    Bool_t passTrig_HLT_Ele24_eta2p1_WPLoose_Gsf          ;
    Bool_t passTrig_HLT_Ele25_WPTight_Gsf                 ;
    Bool_t passTrig_HLT_Ele25_eta2p1_WPLoose_Gsf          ;
    Bool_t passTrig_HLT_Ele25_eta2p1_WPTight_Gsf          ;
    Bool_t passTrig_HLT_Ele27_WPTight_Gsf                 ;
    Bool_t passTrig_HLT_Ele27_eta2p1_WPLoose_Gsf          ;
    Bool_t passTrig_HLT_Ele27_eta2p1_WPTight_Gsf          ;
    Bool_t passTrig_HLT_Ele32_eta2p1_WPLoose_Gsf          ;
    Bool_t passTrig_HLT_Ele32_eta2p1_WPTight_Gsf          ;
    Bool_t passTrig_HLT_Ele105_CaloIdVT_GsfTrkIdT         ;
    Bool_t passTrig_HLT_Ele115_CaloIdVT_GsfTrkIdT         ;

    //Declare triggers for TrigHltDiMu
    Bool_t passTrig_HLT_Mu17_Mu8                          ;
    Bool_t passTrig_HLT_Mu17_Mu8_DZ                       ;
    Bool_t passTrig_HLT_Mu20_Mu10                         ;
    Bool_t passTrig_HLT_Mu20_Mu10_DZ                      ;
    Bool_t passTrig_HLT_Mu27_TkMu8                        ;
    Bool_t passTrig_HLT_Mu30_TkMu11                       ;
    Bool_t passTrig_HLT_Mu40_TkMu11                       ;
    //Declare triggers for TrigHltDiEl

    Float_t NLOWeight;
    Float_t PUWeight;
    Float_t PUWeightUP5;
    Float_t PUWeightUP10;
    Float_t PUWeightDN5;
    Float_t PUWeightDN10;
    Int_t PassQuality;
};

#endif
