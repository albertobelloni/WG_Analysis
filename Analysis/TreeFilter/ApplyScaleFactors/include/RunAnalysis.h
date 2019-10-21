#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "AnalysisBase.h"
#include "include/BranchDefs.h"

#include <string>
#include <vector>


#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"
#include "TGraphAsymmErrors.h"
#include "TH2F.h"
#include "TRandom3.h"

// The RunModule inherits from RunModuleBase (an Abstract Base Class )
// defined in the Core package so that all
// RunModules present a common interface in a Run function
// This allows the code defined in this package
// to be run from the Core package to minimize
// code duplication in each module
//

struct ValWithErr {

    float val;
    float err_up;
    float err_dn;

};

class RunModule : public virtual RunModuleBase {

    public :

        RunModule() {}

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


        // Define modules below.
        // There is no restriction on the naming
        // return values, or inputs to these functions, but
        // you must of course handle them in the source file
        // Examples :
        void AddElectronSF   ( ModuleConfig & config ) const;
        void AddMuonSF       ( ModuleConfig & config ) const;
        void AddPhotonSF     ( ModuleConfig & config ) const;
        void AddPileupSF     ( ModuleConfig & config ) const;
        void AddMETUncert    ( ModuleConfig & config ) const;
        void VaryEGammaScale ( ModuleConfig & config ) const;
        void VaryMuonScale   ( ModuleConfig & config ) const;

        ValWithErr GetValsFromGraph( const TGraphAsymmErrors *, float pt, bool debug=true ) const;
        template<class HIST> ValWithErr GetVals2D( const HIST*, float pt, float eta) const;
        template<class HIST> ValWithErr PhGetVals1D( const HIST* ) const;
        template<class HIST> ValWithErr GetValsRunRange2D( const std::vector<std::pair<float, HIST*> > range_hists, float pt, float eta) const;
        float calc_pu_weight( float puval, float mod=1.0 ) const;
        float get_ele_cutid_syst( float pt, float eta) const;

        

    private :

        TFile *_sffile_mu_iso_bcdef;
        TFile *_sffile_mu_iso_gh;
        TFile *_sffile_mu_id_bcdef;
        TFile *_sffile_mu_id_gh;
        TFile *_sffile_mu_trig_bcdef;
        TFile *_sffile_mu_trig_gh;

        TFile *_sffile_pileup_data;
        TFile *_sffile_pileup_mc;

        std::vector<std::pair<float, TH2D* > > _sfhists_mu_iso;
        std::vector<std::pair<float, TH2D* > > _sfhists_mu_id;
        std::vector<std::pair<float, TH2F* > > _sfhists_mu_trig;
        std::vector<std::pair<float, TH2F* > > _effhists_mu_trig_data;
        std::vector<std::pair<float, TH2F* > > _effhists_mu_trig_mc;

        TFile *_sffile_el_id;
        TFile *_sffile_el_trig;
        TFile *_sffile_el_recohighpt;
        TFile *_sffile_el_recolowpt;

        TH2F *_sfhist_el_id;
        TH2F *_sfhist_el_recohighpt;
        TH2F *_sfhist_el_recolowpt;

        TFile *_sffile_ph_id;
        TFile *_sffile_ph_psv;
        TFile *_sffile_ph_ev;

        TH2F *_sfhist_ph_id;
        TH2D *_sfhist_ph_csev;
        TH2D *_sfhist_ph_psv;

        TH1D *_sfhist_pileup_data;
        TH1F *_sfhist_pileup_mc;

	int _year_mu;
	int _year_ph;

};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

#ifdef MODULE_AddElectronSF
    float el_trigSF;
    float el_trigSFUP;
    float el_trigSFDN;
    float el_idSF;
    float el_idSFUP;
    float el_idSFDN;
    float el_recoSF;
    float el_recoSFUP;
    float el_recoSFDN;
#endif

#ifdef MODULE_AddPhotonSF
    float ph_idSF;
    float ph_idSFUP;
    float ph_idSFDN;

    float ph_psvSF;
    float ph_psvSFUP;
    float ph_psvSFDN;

    float ph_csevSF;
    float ph_csevSFUP;
    float ph_csevSFDN;
#endif

#ifdef MODULE_AddMuonSF
    float mu_trigSF;
    float mu_trigSFUP;
    float mu_trigSFDN;

    float mu_trkSF;
    float mu_trkSFUP;
    float mu_trkSFDN;

    float mu_isoSF;
    float mu_isoSFUP;
    float mu_isoSFDN;

    float mu_idSF;
    float mu_idSFUP;
    float mu_idSFDN;

#endif


    //Examples
};

#endif
