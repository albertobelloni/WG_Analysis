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
        bool ApplyModule         ( ModuleConfig & config ) ;


        // Define modules below.
        // There is no restriction on the naming
        // return values, or inputs to these functions, but
        // you must of course handle them in the source file
        // Examples :
        void FilterMuon         ( ModuleConfig & config );
        void FilterElectron     ( ModuleConfig & config );
        void FilterPhoton       ( ModuleConfig & config );
        void FilterJet          ( ModuleConfig & config ) const;
        bool FilterEvent        ( ModuleConfig & config ) const;
        bool FilterBlind        ( ModuleConfig & config ) const;
        void BuildEventVars     ( ModuleConfig & config ) const;
        void MakePhotonCountVars( ModuleConfig & config ) const;
        void BuildTruth         ( ModuleConfig & config ) const;


        bool get_constriained_nu_pz( const TLorentzVector lepton, TLorentzVector & metlv ) const ;
        bool calc_constrained_nu_momentum( const TLorentzVector lepton, const TLorentzVector metlv, float &result ) const ;
        bool solve_quadratic( float Aval, float Bval, float Cval, float & solution1, float &solution2 ) const; 


    private :
        float _m_w;
        bool _isData;
        std::vector<TLorentzVector> _selectedMuons;
        std::vector<TLorentzVector> _selectedElectrons;
        std::vector<TLorentzVector> _selectedPhotons;

        std::vector<int> _muonTrigMatchBits;
        std::vector<int> _electronTrigMatchBits;

        TH1D * _puHist;


};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {


    Int_t jet_CSVLoose_n;
    Int_t jet_CSVMedium_n;
    Int_t jet_CSVTight_n;

    Int_t el_pt30_n;
    Int_t mu_pt20_n;
    Int_t mu_pt30_n;

    Float_t m_lep_ph;
    Float_t m_lep_met_ph;
    Float_t m_mt_lep_met_ph;
    Float_t m_mt_lep_met_ph_forcewmass;
    Float_t mt_w;
    Float_t mt_res;
    Float_t mt_lep_ph;
    Float_t dphi_lep_ph;
    Float_t dr_lep_ph;
    Float_t m_lep_met;
    Float_t mt_lep_met;
    Float_t pt_lep_met;
    Float_t dphi_lep_met;
    Float_t mt_lep_met_ph;
    Float_t mt_lep_met_ph_inv;
    Float_t dphi_ph_w;
    Float_t pt_lep_met_ph;
    Float_t RecoWMass;
    Float_t recoM_lep_nu_ph;
    Float_t recoMet_eta;
    Float_t recoW_pt;
    Float_t recoW_eta;
    Float_t recoW_phi;
    Float_t m_ll;

    Float_t truemt_res;
    Float_t truemt_lep_met_ph;

    Bool_t nu_z_solution_success;
    Bool_t isBlinded;

    Float_t SampleWeight;

    std::vector<Bool_t>  *ph_hasTruthMatchPh;
    std::vector<Float_t> *ph_truthMatchPh_dr;
    std::vector<Float_t> *ph_truthMatchPh_pt;

    std::vector<Bool_t>  *mu_hasTruthMatchMu;
    std::vector<Float_t> *mu_truthMatchMu_dr;
    std::vector<Float_t> *mu_truthMatchMu_pt;

    std::vector<Bool_t>  *el_hasTruthMatchEl;
    std::vector<Float_t> *el_truthMatchEl_dr;
    std::vector<Float_t> *el_truthMatchEl_pt;

    std::vector<Bool_t>  *mu_hasTrigMatch;
    std::vector<Float_t> *mu_trigMatchMinDr;

    std::vector<Bool_t>  *el_hasTrigMatch;
    std::vector<Float_t> *el_trigMatchMinDr;

    Float_t leadjet_pt;
    Float_t subljet_pt;
    Float_t leaddijet_m;
    Float_t leaddijet_pt;
    Float_t massdijet_m;
    Float_t massdijet_pt;
 
    Int_t ph_loose_n;
    Int_t ph_medium_n;
    Int_t ph_tight_n;

    Int_t ph_mediumPassPSV_n;
    Int_t ph_mediumFailPSV_n;
    Int_t ph_mediumPassCSEV_n;
    Int_t ph_mediumFailCSEV_n;

    Int_t ph_mediumNoSIEIE_n;
    Int_t ph_mediumNoChIso_n;
    Int_t ph_mediumNoNeuIso_n;
    Int_t ph_mediumNoPhoIso_n;

    Int_t ph_mediumNoSIEIENoChIso_n;
    Int_t ph_mediumNoSIEIENoNeuIso_n;
    Int_t ph_mediumNoSIEIENoPhoIso_n;
    Int_t ph_mediumNoChIsoNoPhoIso_n;
    Int_t ph_mediumNoChIsoNoNeuIso_n;
    Int_t ph_mediumNoPhoIsoNoNeuIso_n;

    Int_t ph_mediumNoSIEIEPassPSV_n;
    Int_t ph_mediumNoChIsoPassPSV_n;
    Int_t ph_mediumNoNeuIsoPassPSV_n;
    Int_t ph_mediumNoPhoIsoPassPSV_n;

    Int_t ph_mediumNoSIEIEFailPSV_n;
    Int_t ph_mediumNoChIsoFailPSV_n;
    Int_t ph_mediumNoNeuIsoFailPSV_n;
    Int_t ph_mediumNoPhoIsoFailPSV_n;

    Int_t ph_mediumNoSIEIEPassCSEV_n;
    Int_t ph_mediumNoChIsoPassCSEV_n;
    Int_t ph_mediumNoNeuIsoPassCSEV_n;
    Int_t ph_mediumNoPhoIsoPassCSEV_n;

    Int_t ph_mediumNoSIEIEFailCSEV_n;
    Int_t ph_mediumNoChIsoFailCSEV_n;
    Int_t ph_mediumNoNeuIsoFailCSEV_n;
    Int_t ph_mediumNoPhoIsoFailCSEV_n;

    std::vector<int> *ptSorted_ph_loose_idx;
    std::vector<int> *ptSorted_ph_medium_idx;
    std::vector<int> *ptSorted_ph_tight_idx;

    std::vector<int> *ptSorted_ph_mediumPassPSV_idx;
    std::vector<int> *ptSorted_ph_mediumFailPSV_idx;
    std::vector<int> *ptSorted_ph_mediumPassCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumFailCSEV_idx;

    std::vector<int> *ptSorted_ph_mediumNoSIEIE_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIso_idx;
    std::vector<int> *ptSorted_ph_mediumNoNeuIso_idx;
    std::vector<int> *ptSorted_ph_mediumNoPhoIso_idx;

    std::vector<int> *ptSorted_ph_mediumNoSIEIENoChIso_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoNeuIso_idx;
    std::vector<int> *ptSorted_ph_mediumNoSIEIENoPhoIso_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoNoPhoIso_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoNoNeuIso_idx;
    std::vector<int> *ptSorted_ph_mediumNoPhoIsoNoNeuIso_idx;

    std::vector<int> *ptSorted_ph_mediumNoSIEIEPassPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoPassPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoNeuIsoPassPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoPhoIsoPassPSV_idx;

    std::vector<int> *ptSorted_ph_mediumNoSIEIEFailPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoFailPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoNeuIsoFailPSV_idx;
    std::vector<int> *ptSorted_ph_mediumNoPhoIsoFailPSV_idx;

    std::vector<int> *ptSorted_ph_mediumNoSIEIEPassCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoPassCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoNeuIsoPassCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoPhoIsoPassCSEV_idx;

    std::vector<int> *ptSorted_ph_mediumNoSIEIEFailCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoChIsoFailCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoNeuIsoFailCSEV_idx;
    std::vector<int> *ptSorted_ph_mediumNoPhoIsoFailCSEV_idx;


};

#endif
