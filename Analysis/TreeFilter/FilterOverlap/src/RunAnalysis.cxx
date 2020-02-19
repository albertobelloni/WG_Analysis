#include "RunAnalysis.h"

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

#include "BranchDefs.h"
#include "BranchInit.h"

#include "Util.h"

#include "TFile.h"
#include "TLorentzVector.h"

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

    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );
    
    // *************************
    // Set defaults for added output variables
    // *************************

    // *************************
    // Declare Branches
    // *************************

}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // In BranchInit
    CopyInputVarsToOutput();

    // print event
    printevent = false;
    //printevent = true;
    if( IN::eventNumber%100 == 42  ) printevent = true;
    if( printevent ) std::cout << " eventNumber " << IN::eventNumber; //<< std::endl;

    // loop over configured modules
    bool save_event = true;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        save_event &= ApplyModule( mod_conf );
    }

    return save_event;

}

bool RunModule::ApplyModule( ModuleConfig & config ) const {

    // This bool is used for filtering
    // If a module implements an event filter
    // update this variable and return it
    // to apply the filter
    bool keep_evt = true;

    // Example :
    if( config.GetName() == "FilterPhoton" ) {
        keep_evt &= FilterPhoton( config );
    }
    if( config.GetName() == "FilterTrueHT" ) {
        keep_evt &= FilterTrueHT( config );
    }
    if( config.GetName() == "FilterMTRes" ) {
        keep_evt &= FilterMTRes( config );
    }
    if( config.GetName() == "FilterTrueWPt" ) {
        keep_evt &= FilterTrueWPt( config );
    }
    if( config.GetName() == "ApplyTrueWPtKNeg" ) {
        keep_evt &= ApplyTrueWPtKNeg( config );
    }

    return keep_evt;

}

// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************
//

bool RunModule::FilterTrueHT( ModuleConfig & config ) const {

    bool keep_event = true;

    if(!config.PassFloat( "cut_trueht", OUT::trueht) ) keep_event = false;

    return keep_event;
}

bool RunModule::FilterMTRes( ModuleConfig & config ) const {

    bool keep_event = true;

    if(!config.PassFloat( "cut_mtres", OUT::mt_res ) ) keep_event = false;

    return keep_event;
}

bool RunModule::FilterTrueWPt( ModuleConfig & config ) const {

    bool keep_event = true;
    
    // Just accept events without on-shell W bosons
    if (OUT::trueW_n == 0) {
        return keep_event;
    }

    if(!config.PassFloat( "cut_truewpt", OUT::trueW_pt->at(0) ) ) keep_event = false;

    return keep_event;
}

bool RunModule::ApplyTrueWPtKNeg( ModuleConfig & config ) const {

    bool keep_event = true;
    
    double truewpt_bound_lo = -99.;
    double truewpt_bound_hi = -99.;
    double truewpt_kneg_lo  = -99.;
    double truewpt_kneg_hi  = -99.;
    
    std::map<std::string, std::string>::const_iterator eitr;
    eitr = config.GetInitData().find( "truewpt_bound_lo" );
    if( eitr != config.GetInitData().end() ) Utils::stringToDouble(eitr->second, truewpt_bound_lo);
    else std::cout << "Warning: ApplyTrueWPtKNeg truewpt_bound_lo unset, output will be invalid." << std::endl;
    
    eitr = config.GetInitData().find( "truewpt_bound_hi" );
    if( eitr != config.GetInitData().end() ) Utils::stringToDouble(eitr->second, truewpt_bound_hi);
    else  std::cout << "Warning: ApplyTrueWPtKNeg truewpt_bound_hi unset, output will be invalid." << std::endl;
    
    eitr = config.GetInitData().find( "truewpt_kneg_lo" );
    if( eitr != config.GetInitData().end() ) Utils::stringToDouble(eitr->second, truewpt_kneg_lo);
    else std::cout << "Warning: ApplyTrueWPtKNeg truewpt_kneg_lo  unset, output will be invalid." << std::endl;
    
    eitr = config.GetInitData().find( "truewpt_kneg_hi" );
    if( eitr != config.GetInitData().end() ) Utils::stringToDouble(eitr->second, truewpt_kneg_hi);
    else std::cout << "Warning: ApplyTrueWPtKNeg truewpt_kneg_hi  unset, output will be invalid." << std::endl;
    
    double trueW_pt;
    if (OUT::trueW_n > 0) {
        trueW_pt = OUT::trueW_pt->at(0);
    }
    else {
        return keep_event;
    }
    double NLOWeight = 1.0;
    if( OUT::EventWeights->at(0) < 0 ) {
        NLOWeight = -1.0;
    }
    
    if (NLOWeight < 0) {
        if (trueW_pt < truewpt_bound_lo) {
            if (printevent) std::cout << "Modified NLOWeight -> " << NLOWeight * truewpt_kneg_lo << std::endl;
            OUT::NLOWeight = NLOWeight * truewpt_kneg_lo;
        }
        if (trueW_pt > truewpt_bound_hi) {
            if (printevent) std::cout << "Modified NLOWeight -> " << NLOWeight * truewpt_kneg_hi << std::endl;
            OUT::NLOWeight = NLOWeight * truewpt_kneg_hi;
        }
    }
    
    return keep_event;
}

bool RunModule::FilterPhoton( ModuleConfig & config ) const {

    bool keep_event = true;

    std::vector<TLorentzVector> gen_phot;
    for( int i = 0; i < OUT::trueph_n ; i++ ) {

        float phot_pt = OUT::trueph_pt->at(i);
        float phot_eta = OUT::trueph_eta->at(i);
        float phot_phi = OUT::trueph_phi->at(i);
        float phot_dr = OUT::trueph_lep_dr->at(i);
      	int phot_mother = OUT::trueph_motherPID->at(i);
      	int phot_status = OUT::trueph_status->at(i);

#ifdef EXISTS_trueph_isPromptFS
	      int phot_isPromptFS = OUT::trueph_isPromptFS->at(i);
#endif
#ifdef EXISTS_trueph_FHPFS
      	int phot_FHPFS = OUT::trueph_FHPFS->at(i);
#endif
//bool phot_isStable = (phot_status == 1);
//bool phot_correctMother = (fabs(phot_mother) == 1) || (fabs(phot_mother) == 2) || (fabs(phot_mother) == 3) || (fabs(phot_mother) == 4) || (fabs(phot_mother) == 5) || (fabs(phot_mother) == 11) || (fabs(phot_mother) == 13) || (fabs(phot_mother) == 15) || (fabs(phot_mother) == 21) || (fabs(phot_mother) == 2212); // gen photon must come from quark, lepton, gluon, or proton

#ifdef EXISTS_trueph_isPromptFS
      if (printevent) {std::cout<<std::endl << phot_pt<< " "<< phot_eta<<" "<< phot_mother<<" status "<<phot_status<<" isPrompt "<<phot_isPromptFS<<" FHPFS "<<phot_FHPFS<<" "<<phot_dr; }
#endif
        if( !config.PassFloat( "cut_genph_pt", phot_pt ) ) continue;
        if( !config.PassFloat( "cut_genph_aeta", fabs(phot_eta) ) ) continue;
        if( !config.PassFloat( "cut_genph_dr", phot_dr ) ) continue;
#ifdef EXISTS_trueph_isPromptFS
        if( !config.PassBool( "cut_genph_isPromptFS", phot_isPromptFS ) ) continue;
        bool wgcut = (phot_status==23)||(abs(phot_mother)==24 && phot_isPromptFS)
        if( !config.PassBool( "cut_genph_wg", wg ) ) continue;
#endif
#ifdef EXISTS_trueph_FHPFS
        if( !config.PassBool( "cut_genph_FHPFS", phot_FHPFS ) ) continue;
#endif
        bool isr = abs(phot_mother) < 11 || abs(phot_mother) > 16;
        if( !config.PassBool( "cut_genph_isr", isr ) ) continue;


        if (printevent) std::cout<< " pass";
        TLorentzVector phlv;
        phlv.SetPtEtaPhiM( phot_pt, phot_eta, phot_phi, 0.0 );

        gen_phot.push_back(phlv);

    }

    if (printevent) {
        //std::cout<< std::endl; 
        //for (unsigned i=0;i<gen_phot.size() ;i++) {std::cout<<i<<" pt "<<gen_phot.at(i).Pt();}
        std::cout<< std::endl; 
    }
    if( !config.PassInt( "cut_n_gen_phot", gen_phot.size() ) ) keep_event=false;
    if( !config.PassFloat( "cut_lead_genph_pt", gen_phot.size() ? gen_phot[0].Pt() : -1 ) ) keep_event=false;

    return keep_event;
    
}

