#include "include/RunAnalysis.h"

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

#include "include/BranchDefs.h"
#include "include/BranchInit.h"
#include "include/RoccoR.h"


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

    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );
    
    // *************************
    // Set defaults for added output variables
    // *************************
#ifdef MODULE_AddElectronSF
    OUT::el_trigSF = -1;
    OUT::el_trigSFUP = -1;
    OUT::el_trigSFDN = -1;

    OUT::el_idSF = -1;
    OUT::el_idSFUP = -1;
    OUT::el_idSFDN = -1;

    OUT::el_recoSF   = -1;
    OUT::el_recoSFUP = -1;
    OUT::el_recoSFDN = -1; 
#endif

#ifdef MODULE_AddPhotonSF
    OUT::ph_idSF = -1;
    OUT::ph_idSFUP = -1;
    OUT::ph_idSFDN = -1;

    OUT::ph_psvSF = -1;
    OUT::ph_psvSFUP = -1;
    OUT::ph_psvSFDN = -1;

    OUT::ph_csevSF = -1;
    OUT::ph_csevSFUP = -1;
    OUT::ph_csevSFDN = -1;
#endif

#ifdef MODULE_AddMuonSF
    OUT::mu_trigSF = -1;
    OUT::mu_trigSFUP = -1;
    OUT::mu_trigSFDN = -1;

    OUT::mu_isoSF = -1;
    OUT::mu_isoSFUP = -1;
    OUT::mu_isoSFDN = -1;

    OUT::mu_trkSF = -1;
    OUT::mu_trkSFUP = -1;
    OUT::mu_trkSFDN = -1;

    OUT::mu_idSF = -1;
    OUT::mu_idSFUP = -1;
    OUT::mu_idSFDN = -1;

    OUT::mu_rcSF = -1;
    OUT::mu_rcSFUP = -1;
    OUT::mu_rcSFDN = -1;

#endif

    // *************************
    // Declare Branches
    // *************************

    // Examples :
#ifdef MODULE_AddElectronSF
    outtree->Branch( "el_trigSF"      ,  &OUT::el_trigSF      , "el_trigSF/F"      );
    outtree->Branch( "el_trigSFUP"    ,  &OUT::el_trigSFUP    , "el_trigSFUP/F"    );
    outtree->Branch( "el_trigSFDN"    ,  &OUT::el_trigSFDN    , "el_trigSFDN/F"    );
    outtree->Branch( "el_idSF"        ,  &OUT::el_idSF        , "el_idSF/F"        );
    outtree->Branch( "el_idSFUP"      ,  &OUT::el_idSFUP      , "el_idSFUP/F"      );
    outtree->Branch( "el_idSFDN"      ,  &OUT::el_idSFDN      , "el_idSFDN/F"      );
    outtree->Branch( "el_recoSF"      ,  &OUT::el_recoSF      , "el_recoSF/F"      );
    outtree->Branch( "el_recoSFUP"    ,  &OUT::el_recoSFUP    , "el_recoSFUP/F"    );
    outtree->Branch( "el_recoSFDN"    ,  &OUT::el_recoSFDN    , "el_recoSFDN/F"    );
#endif
   
#ifdef MODULE_AddPhotonSF
    outtree->Branch( "ph_idSF"      ,  &OUT::ph_idSF      , "ph_idSF/F"      );
    outtree->Branch( "ph_idSFUP"    ,  &OUT::ph_idSFUP    , "ph_idSFUP/F"    );
    outtree->Branch( "ph_idSFDN"    ,  &OUT::ph_idSFDN    , "ph_idSFDN/F"    );
    outtree->Branch( "ph_psvSF"     ,  &OUT::ph_psvSF     , "ph_psvSF/F"     );
    outtree->Branch( "ph_psvSFUP"   ,  &OUT::ph_psvSFUP   , "ph_psvSFUP/F"   );
    outtree->Branch( "ph_psvSFDN"   ,  &OUT::ph_psvSFDN   , "ph_psvSFDN/F"   );
    outtree->Branch( "ph_csevSF"    ,  &OUT::ph_csevSF    , "ph_csevSF/F"    );
    outtree->Branch( "ph_csevSFUP"  ,  &OUT::ph_csevSFUP  , "ph_csevSFUP/F"  );
    outtree->Branch( "ph_csevSFDN"  ,  &OUT::ph_csevSFDN  , "ph_csevSFDN/F"  );
#endif

#ifdef MODULE_AddMuonSF
    outtree->Branch( "mu_trigSF"    ,  &OUT::mu_trigSF    , "mu_trigSF/F"    );
    outtree->Branch( "mu_trigSFUP"  ,  &OUT::mu_trigSFUP  , "mu_trigSFUP/F"  );
    outtree->Branch( "mu_trigSFDN"  ,  &OUT::mu_trigSFDN  , "mu_trigSFDN/F"  );
    outtree->Branch( "mu_isoSF"     ,  &OUT::mu_isoSF     , "mu_isoSF/F"     );
    outtree->Branch( "mu_isoSFUP"   ,  &OUT::mu_isoSFUP   , "mu_isoSFUP/F"   );
    outtree->Branch( "mu_isoSFDN"   ,  &OUT::mu_isoSFDN   , "mu_isoSFDN/F"   );
    outtree->Branch( "mu_trkSF"     ,  &OUT::mu_trkSF     , "mu_trkSF/F"     );
    outtree->Branch( "mu_trkSFUP"   ,  &OUT::mu_trkSFUP   , "mu_trkSFUP/F"   );
    outtree->Branch( "mu_trkSFDN"   ,  &OUT::mu_trkSFDN   , "mu_trkSFDN/F"   );
    outtree->Branch( "mu_idSF"      ,  &OUT::mu_idSF      , "mu_idSF/F"      );
    outtree->Branch( "mu_idSFUP"    ,  &OUT::mu_idSFUP    , "mu_idSFUP/F"    );
    outtree->Branch( "mu_idSFDN"    ,  &OUT::mu_idSFDN    , "mu_idSFDN/F"    );
    outtree->Branch( "mu_rcSF"      ,  &OUT::mu_rcSF      , "mu_rcSF/F"      );
    outtree->Branch( "mu_rcSFUP"    ,  &OUT::mu_rcSFUP    , "mu_rcSFUP/F"    );
    outtree->Branch( "mu_rcSFDN"    ,  &OUT::mu_rcSFDN    , "mu_rcSFDN/F"    );
#endif


    // store the lumis for averaging
    float int_lumi_b = 5933692351.209;
    float int_lumi_c = 2761135761.229;
    float int_lumi_d = 4525903884.794;
    float int_lumi_e = 4318519409.159;
    float int_lumi_f = 3370228550.294;
    float int_lumi_g = 8015343899.163;
    float int_lumi_h = 9199511317.095;

    float int_lumi_bcdef = int_lumi_b + int_lumi_c + int_lumi_d + int_lumi_e + int_lumi_f;
    float int_lumi_gh  = int_lumi_g + int_lumi_h;

    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {

        if( mod_conf.GetName() == "AddMuonSF" ) { 
            std::map<std::string, std::string>::const_iterator itr;

            itr = mod_conf.GetInitData().find( "FilePathIsoBCDEF" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_iso_bcdef = TFile::Open( (itr->second).c_str(), "READ" );
                if( _sffile_mu_iso_bcdef->IsOpen() ) {
                    TH2D * thishist =  dynamic_cast<TH2D*>(_sffile_mu_iso_bcdef->Get( "NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt" ));
                    if( !thishist ) {
		      std::cout << "could not get hist from file " << _sffile_mu_iso_bcdef->GetName() << std::endl;
                    }
                    _sfhists_mu_iso.push_back(std::make_pair(int_lumi_bcdef,  thishist));
                }
                else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find( "FilePathIsoGH" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_iso_gh = TFile::Open( (itr->second).c_str(), "READ" );
                if( _sffile_mu_iso_gh->IsOpen() ) {
                    TH2D * thishist = dynamic_cast<TH2D*>(_sffile_mu_iso_gh->Get( "NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt" ));
                    if( !thishist ) {
                        std::cout << "could not get hist from file " << _sffile_mu_iso_gh->GetName() << std::endl;
                    }
                    _sfhists_mu_iso.push_back(std::make_pair(int_lumi_gh, thishist));
                }
                else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find( "FilePathIdBCDEF" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_id_bcdef = TFile::Open( (itr->second).c_str(), "READ" );
                if( _sffile_mu_id_bcdef->IsOpen() ) {
                    TH2D * thishist = dynamic_cast<TH2D*>(_sffile_mu_id_bcdef->Get( "NUM_TightID_DEN_genTracks_eta_pt" ) );
                    if( !thishist ) {
                        std::cout << "could not get hist from file " << _sffile_mu_id_bcdef->GetName() << std::endl;
                    }
                    _sfhists_mu_id.push_back(std::make_pair(int_lumi_bcdef, thishist) );
                }
                else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find( "FilePathIdGH" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_id_gh = TFile::Open( (itr->second).c_str(), "READ" );
                if( _sffile_mu_id_gh->IsOpen() ) {
                    TH2D * thishist = dynamic_cast<TH2D*>(_sffile_mu_id_gh->Get( "NUM_TightID_DEN_genTracks_eta_pt" ));
                    if( !thishist ) {
                        std::cout << "could not get hist from file " << _sffile_mu_id_gh->GetName() << std::endl;
                    }
                    _sfhists_mu_id.push_back(std::make_pair(int_lumi_gh, thishist));
                }
                else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find( "FilePathTrigBCDEF" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_trig_bcdef = TFile::Open( (itr->second).c_str(), "READ" );
                if( _sffile_mu_trig_bcdef->IsOpen() ) {
		  //TH2F * thishist = dynamic_cast<TH2F*>(_sffile_mu_trig_bcdef->Get( "IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio" ));
                    TH2F * thishist = dynamic_cast<TH2F*>(_sffile_mu_trig_bcdef->Get( "IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio" ));
                    if( !thishist ) {
                        std::cout << "could not get hist from file " << _sffile_mu_trig_bcdef->GetName() << std::endl;
                    }
                    _sfhists_mu_trig.push_back(std::make_pair(int_lumi_bcdef, thishist));
                }
                else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find( "FilePathTrigGH" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_mu_trig_gh = TFile::Open( (itr->second).c_str(), "READ" );
                if( _sffile_mu_trig_gh->IsOpen() ) {
		  //TH2F * thishist = dynamic_cast<TH2F*>(_sffile_mu_trig_gh->Get( "IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio" ));
                    TH2F * thishist = dynamic_cast<TH2F*>(_sffile_mu_trig_gh->Get( "IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio" ));
                    if( !thishist ) {
                        std::cout << "could not get hist from file " << _sffile_mu_trig_gh->GetName() << std::endl;
                    }
                    _sfhists_mu_trig.push_back(std::make_pair(int_lumi_gh, thishist));
                }
                else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
	    itr = mod_conf.GetInitData().find( "FilePathRochester" );
	    if( itr != mod_conf.GetInitData().end() ) {
	      rc.init((itr->second).c_str());
	    }
        }
        if( mod_conf.GetName() == "AddElectronSF" ) { 
            std::map<std::string, std::string>::const_iterator itr;

            itr = mod_conf.GetInitData().find( "FilePathCutID" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_el_id = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_el_id = dynamic_cast<TH2F*>(_sffile_el_id->Get( "EGamma_SF2D" ));
            }
            itr = mod_conf.GetInitData().find( "FilePathRecoHighPt" );
            if( itr != mod_conf.GetInitData().end() ){
                _sffile_el_recohighpt = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_el_recohighpt = dynamic_cast<TH2F*>(_sffile_el_recohighpt->Get("EGamma_SF2D"));
            }
            itr = mod_conf.GetInitData().find( "FilePathRecoLowPt" );
            if( itr != mod_conf.GetInitData().end() ){
                _sffile_el_recolowpt = TFile::Open( (itr->second).c_str(), "READ" );
                _sfhist_el_recolowpt = dynamic_cast<TH2F*>(_sffile_el_recolowpt->Get("EGamma_SF2D"));
            }
        }
        if( mod_conf.GetName() == "AddPhotonSF" ) { 
            std::map<std::string, std::string>::const_iterator itr;
            itr = mod_conf.GetInitData().find( "FilePathId" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_ph_id = TFile::Open( (itr->second).c_str(), "READ" );
                if( _sffile_ph_id->IsOpen() ) { 
                    _sfhist_ph_id   = dynamic_cast<TH2F*>(_sffile_ph_id->Get( "EGamma_SF2D" ) );
                    if( !_sfhist_ph_id ) {
                        std::cout << "could not get hist from file " << _sffile_ph_id->GetName() << std::endl;
                    }
                }
                else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find( "FilePathEveto" );
            if( itr != mod_conf.GetInitData().end() ) {
                _sffile_ph_ev   = TFile::Open( (itr->second).c_str(), "READ" );
                if( _sffile_ph_ev->IsOpen() ) { 
                    _sfhist_ph_psv  = dynamic_cast<TH2D*>(_sffile_ph_ev->Get( "Scaling_Factors_HasPix_R9 Inclusive" ) );
                    _sfhist_ph_csev = dynamic_cast<TH2D*>(_sffile_ph_ev->Get( "Scaling_Factors_CSEV_R9 Inclusive" ) );
                    if( !_sfhist_ph_psv ) std::cout << "Could not get PSV hist from file " << _sffile_ph_ev->GetName() << std::endl;
                    if( !_sfhist_ph_csev ) std::cout << "Could not get CSEV hist from file " << _sffile_ph_ev->GetName() << std::endl;
                }
                else {
                    std::cout << "Could not open file " << itr->second << std::endl;
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

    if( config.GetName() == "AddElectronSF" ) {
        AddElectronSF( config );
    }
    if( config.GetName() == "AddMuonSF" ) {
        AddMuonSF( config );
    }
    if( config.GetName() == "AddPhotonSF" ) {
        AddPhotonSF( config );
    }
    

    return keep_evt;

}

void RunModule::AddElectronSF( ModuleConfig & /*config*/ ) const {

#ifdef MODULE_AddElectronSF

    OUT::el_trigSF   = 1.0;
    OUT::el_trigSFUP = 1.0;
    OUT::el_trigSFDN = 1.0;

    OUT::el_idSF   = 1.0;
    OUT::el_idSFUP = 1.0;
    OUT::el_idSFDN = 1.0;

    OUT::el_recoSF   = 1.0;
    OUT::el_recoSFUP = 1.0;
    OUT::el_recoSFDN = 1.0;

    if( OUT::isData ) {
        return;
    }

    std::vector<float> sfs_id;
    std::vector<float> errs_id;
    std::vector<float> sfs_reco;
    std::vector<float> errs_reco;

    for( int idx = 0; idx < OUT::el_n; ++idx ) {
        /*

        if( OUT::el_triggerMatch->at(idx) ) {

            //https://twiki.cern.ch/twiki/bin/viewauth/CMS/KoPFAElectronTagAndProbe
            if( OUT::el_pt->at(idx) >= 30 && OUT::el_pt->at(idx) <= 40 ) {
                if( fabs(OUT::el_sceta->at(idx)) <= 0.8 ) {
                    OUT::el_trigSF = 0.987;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.012; 
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.017;
                }
                else if( fabs(OUT::el_sceta->at(idx)) > 0.8 && fabs( OUT::el_sceta->at(idx) ) <= 1.478 ) {
                    OUT::el_trigSF = 0.964;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.002; 
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.001;
                }
                else if( fabs(OUT::el_sceta->at(idx)) > 1.478 && fabs( OUT::el_sceta->at(idx) ) <= 2.5 ) {
                    OUT::el_trigSF = 1.004;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.006;
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.006;
                }
            }
            else if( OUT::el_pt->at(idx) > 40 && OUT::el_pt->at(idx) <= 50 ) {
                if( fabs(OUT::el_sceta->at(idx)) <= 0.8 ) {
                    OUT::el_trigSF = 0.997;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.001; 
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.001;
                }
                else if( fabs(OUT::el_sceta->at(idx)) > 0.8 && fabs( OUT::el_sceta->at(idx) ) <= 1.478 ) {
                    OUT::el_trigSF = 0.980;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.001; 
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.001;
                }
                else if( fabs(OUT::el_sceta->at(idx)) > 1.478 && fabs( OUT::el_sceta->at(idx) ) <= 2.5 ) {
                    OUT::el_trigSF = 1.033;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.007;
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.007;
                }
            }
            else if( OUT::el_pt->at(idx) > 50 ) {
                if( fabs(OUT::el_sceta->at(idx)) <= 0.8 ) {
                    OUT::el_trigSF = 0.998;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.002; 
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.002;
                }
                else if( fabs(OUT::el_sceta->at(idx)) > 0.8 && fabs( OUT::el_sceta->at(idx) ) <= 1.478 ) {
                    OUT::el_trigSF = 0.988;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.002; 
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.002;
                }
                else if( fabs(OUT::el_sceta->at(idx)) > 1.478 && fabs( OUT::el_sceta->at(idx) ) <= 2.5 ) {
                    OUT::el_trigSF = 0.976;
                    OUT::el_trigSFUP = OUT::el_trigSF + 0.015;
                    OUT::el_trigSFDN = OUT::el_trigSF - 0.012;
                }
            }
        }
        */
        // Do loose scale factors
        //

        float pt  = OUT::el_pt->at(idx);
        float eta = OUT::el_eta->at(idx);

        ValWithErr res_id   = GetVals2D( _sfhist_el_id, eta, pt );
        ValWithErr res_reco;
        if( pt<20.0 ){
            res_reco = GetVals2D( _sfhist_el_recolowpt, eta, pt ); 
        } 
        else{
            res_reco = GetVals2D( _sfhist_el_recohighpt, eta, pt );
        }

        sfs_id .push_back(res_id.val );
        errs_id.push_back(res_id.err_up);

        sfs_reco .push_back(res_reco.val );
        errs_reco.push_back(res_reco.err_up);

    }

    if( sfs_id.size() == 1 ) {
        OUT::el_idSF   = sfs_id[0];
        OUT::el_idSFUP = sfs_id[0] + errs_id[0];
        OUT::el_idSFDN = sfs_id[0] - errs_id[0];

        OUT::el_recoSF   = sfs_reco[0];
        OUT::el_recoSFUP = sfs_reco[0] + errs_reco[0];
        OUT::el_recoSFDN = sfs_reco[0] - errs_reco[0]; 
    }

    else if( sfs_id.size() > 1 ) {
        OUT::el_idSF = sfs_id[0]*sfs_id[1];
        OUT::el_idSFUP = ( sfs_id[0] + errs_id[0] ) *( sfs_id[1] + errs_id[1] );
        OUT::el_idSFDN = ( sfs_id[0] - errs_id[0] ) *( sfs_id[1] - errs_id[1] );

        OUT::el_recoSF = sfs_reco[0]*sfs_reco[1];
        OUT::el_recoSFUP = ( sfs_reco[0] + errs_reco[0] ) *( sfs_reco[1] + errs_reco[1] );
        OUT::el_recoSFDN = ( sfs_reco[0] - errs_reco[0] ) *( sfs_reco[1] - errs_reco[1] );
    }
#endif
}

float RunModule::get_ele_cutid_syst( float pt, float eta ) const {

    // Uncertainty table, from https://twiki.cern.ch/twiki/bin/view/Main/EGammaScaleFactors2012
    // pT                     10 - 15  15 - 20  20 - 30  30 - 40  40 - 50  50 - 200
    // 0.0 < abs(η) < 0.8      11.00    6.90     1.40     0.28     0.14     0.41
    // 0.8 < abs(η) < 1.442    11.00    6.90     1.40     0.28     0.14     0.41
    // 1.442 < abs(η) < 1.556  11.00    8.30     5.70     2.40     0.28     0.43
    // 1.556 < abs(η) < 2.00   12.00    4.00     2.20     0.59     0.30     0.53
    // 2.0 < abs(η) < 2.5      12.00    4.00     2.20     0.59     0.30     0.53
    //
    
    if( pt > 10 && pt <= 15 ) {
        if( fabs( eta ) <= 0.8 ) {
            return 0.11;
        }
        else if( fabs( eta ) > 0.8 && fabs( eta ) <= 1.442 ) {
            return 0.11;
        }
        else if( fabs( eta ) > 1.442 && fabs( eta ) <= 1.556 ) {
            return 0.11;
        }
        else if( fabs( eta ) > 1.556 && fabs( eta ) <= 2.0 ) {
            return 0.12;
        }
        else if( fabs( eta ) > 2.0 && fabs( eta ) <= 2.5 ) {
            return 0.12;
        }
    }
    else if( pt >15 && pt <= 20 ) {
        if( fabs( eta ) <= 0.8 ) {
            return 0.069;
        }
        else if( fabs( eta ) > 0.8 && fabs( eta ) <= 1.442 ) {
            return 0.069;
        }
        else if( fabs( eta ) > 1.442 && fabs( eta ) <= 1.556 ) {
            return 0.083;
        }
        else if( fabs( eta ) > 1.556 && fabs( eta ) <= 2.0 ) {
            return 0.04;
        }
        else if( fabs( eta ) > 2.0 && fabs( eta ) <= 2.5 ) {
            return 0.04;
        }
    }
    else if( pt > 20 && pt <= 30 ) {
        if( fabs( eta ) <= 0.8 ) {
            return 0.014;
        }
        else if( fabs( eta ) > 0.8 && fabs( eta ) <= 1.442 ) {
            return 0.014;
        }
        else if( fabs( eta ) > 1.442 && fabs( eta ) <= 1.556 ) {
            return 0.057;
        }
        else if( fabs( eta ) > 1.556 && fabs( eta ) <= 2.0 ) {
            return 0.022;
        }
        else if( fabs( eta ) > 2.0 && fabs( eta ) <= 2.5 ) {
            return 0.022;
        }
    }
    else if( pt > 30 && pt <= 40 ) {
        if( fabs( eta ) <= 0.8 ) {
            return 0.0028;
        }
        else if( fabs( eta ) > 0.8 && fabs( eta ) <= 1.442 ) {
            return 0.0028;
        }
        else if( fabs( eta ) > 1.442 && fabs( eta ) <= 1.556 ) {
            return 0.024;
        }
        else if( fabs( eta ) > 1.556 && fabs( eta ) <= 2.0 ) {
            return 0.0059;
        }
        else if( fabs( eta ) > 2.0 && fabs( eta ) <= 2.5 ) {
            return 0.0059;
        }
    }
    else if( pt > 40 && pt <= 50 ) {
        if( fabs( eta ) <= 0.8 ) {
            return 0.0014;
        }
        else if( fabs( eta ) > 0.8 && fabs( eta ) <= 1.442 ) {
            return 0.0014;
        }
        else if( fabs( eta ) > 1.442 && fabs( eta ) <= 1.556 ) {
            return 0.0028;
        }
        else if( fabs( eta ) > 1.556 && fabs( eta ) <= 2.0 ) {
            return 0.003;
        }
        else if( fabs( eta ) > 2.0 && fabs( eta ) <= 2.5 ) {
            return 0.003;
        }
    }
    else if( pt > 50 ) {
        if( fabs( eta ) <= 0.8 ) {
            return 0.0041;
        }
        else if( fabs( eta ) > 0.8 && fabs( eta ) <= 1.442 ) {
            return 0.0041;
        }
        else if( fabs( eta ) > 1.442 && fabs( eta ) <= 1.556 ) {
            return 0.0043;
        }
        else if( fabs( eta ) > 1.556 && fabs( eta ) <= 2.0 ) {
            return 0.0053;
        }
        else if( fabs( eta ) > 2.0 && fabs( eta ) <= 2.5 ) {
            return 0.0053;
        }
    }

    std::cout << "WARNING NO SF for pt = " << pt << ", eta = " << eta << std::endl;

    return -1;
}



void RunModule::AddPhotonSF( ModuleConfig & /*config*/ ) const {

#ifdef MODULE_AddPhotonSF

    OUT::ph_idSF = 1.0;
    OUT::ph_idSFUP = 1.0;
    OUT::ph_idSFDN = 1.0;
    
    OUT::ph_psvSF = 1.0;
    OUT::ph_psvSFUP = 1.0;
    OUT::ph_psvSFDN = 1.0;

    OUT::ph_csevSF = 1.0;
    OUT::ph_csevSFUP = 1.0;
    OUT::ph_csevSFDN = 1.0;

    if( OUT::isData ) {
        return;
    }
    // to check if photon pt is above histogram
    
    std::vector<float> sfs_id;
    std::vector<float> errs_id;
    std::vector<float> sfs_csev;
    std::vector<float> errs_csev;
    std::vector<float> sfs_psv;
    std::vector<float> errs_psv;
    for( int idx = 0; idx < OUT::ph_n; idx++ ) {

        // in the ID histogram, the x axis is signed eta, y is pt
        float pt = OUT::ph_pt->at(idx);
        float eta = OUT::ph_eta->at(idx);

        ValWithErr res_id   = GetVals2D( _sfhist_ph_id, eta, pt );
        ValWithErr res_psv  = GetVals2D( _sfhist_ph_psv, fabs(eta), pt );
        ValWithErr res_csev = GetVals2D( _sfhist_ph_csev, fabs(eta), pt );

        sfs_id .push_back(res_id.val );
        errs_id.push_back(res_id.err_up);

        sfs_csev .push_back(res_csev.val );
        errs_csev.push_back(res_csev.err_up);

        sfs_psv .push_back(res_psv.val );
        errs_psv.push_back(res_psv.err_up);

    }

    if( sfs_id.size() == 1 ) {
        OUT::ph_idSF = sfs_id[0];
        OUT::ph_idSFUP = sfs_id[0]+errs_id[0];
        OUT::ph_idSFDN = sfs_id[0]-errs_id[0];
        
        OUT::ph_psvSF   = sfs_psv[0];
        OUT::ph_psvSFUP = sfs_psv[0]+errs_psv[0];
        OUT::ph_psvSFDN = sfs_psv[0]-errs_psv[0];

        // Also do CSEV
        OUT::ph_csevSF   = sfs_csev[0];
        OUT::ph_csevSFUP = sfs_csev[0]+errs_csev[0];
        OUT::ph_csevSFDN = sfs_csev[0]-errs_csev[0];

    }
    else if( sfs_id.size() > 1 ) {
        OUT::ph_idSF = sfs_id[0]*sfs_id[1];
        OUT::ph_idSFUP = ( sfs_id[0] + errs_id[0] )*( sfs_id[1] + errs_id[1] );
        OUT::ph_idSFDN = ( sfs_id[0] - errs_id[0] )*( sfs_id[1] - errs_id[1] );

        OUT::ph_psvSF = sfs_psv[0]*sfs_psv[1];
        OUT::ph_psvSFUP = (sfs_psv[0]+errs_psv[0])*(sfs_psv[1]+errs_psv[1]);
        OUT::ph_psvSFDN = (sfs_psv[0]-errs_psv[0])*(sfs_psv[1]-errs_psv[1]);

        OUT::ph_csevSF = sfs_csev[0]*sfs_csev[1];
        OUT::ph_csevSFUP = (sfs_csev[0]+errs_csev[0])*(sfs_csev[1]+errs_csev[1]);
        OUT::ph_csevSFDN = (sfs_csev[0]-errs_csev[0])*(sfs_csev[1]-errs_csev[1]);
    }

#endif
}

void RunModule::AddMuonSF( ModuleConfig & /*config*/ ) const { 

#ifdef MODULE_AddMuonSF

    OUT::mu_idSF     = 1.0;
    OUT::mu_idSFUP   = 1.0;
    OUT::mu_idSFDN   = 1.0;

    OUT::mu_isoSF    = 1.0;
    OUT::mu_isoSFUP  = 1.0;
    OUT::mu_isoSFDN  = 1.0;

    OUT::mu_trigSF   = 1.0;
    OUT::mu_trigSFUP = 1.0;
    OUT::mu_trigSFDN = 1.0;

    OUT::mu_trkSF   = 1.0;
    OUT::mu_trkSFUP = 1.0;
    OUT::mu_trkSFDN = 1.0;

    OUT::mu_rcSF     = 1.0;
    OUT::mu_rcSFUP   = 1.0;
    OUT::mu_rcSFDN   = 1.0;

    if( OUT::isData) {
        return;
    }

    std::vector<float> idsfs;
    std::vector<float> iderrsup;
    std::vector<float> iderrsdn;

    std::vector<float> isosfs;
    std::vector<float> isoerrsup;
    std::vector<float> isoerrsdn;

    std::vector<float> rcsfs;
    std::vector<float> rcsfserr;

    /*
    if( OUT::mu_n == 1 )  { // our trigger SFs are only available for single muon triggers
        float feta = fabs(OUT::mu_eta->at(0));
        float pt   =      OUT::mu_pt ->at(0) ;
        if( pt > 26 && feta < 2.4 ) {

            ValWithErr entry;
            entry = GetValsRunRange2D( _sfhists_mu_trig, pt, feta );

            OUT::mu_trigSF = entry.val;
            OUT::mu_trigSFUP = entry.val + entry.err_up;
            OUT::mu_trigSFDN = entry.val - entry.err_dn;
        }
        else {
            std::cout << "AddMuonSF -- WARNING : muon pt or eta out of range " << pt << " " << feta << std::endl;
        }
    }
    */

    for( int idx = 0; idx < OUT::mu_n; ++idx ) {
        float eta =   OUT::mu_eta->at(idx);
        float pt   =   OUT::mu_pt ->at(idx) ;
	float phi = OUT::mu_phi->at(idx);
	float Q = OUT::mu_charge->at(idx);

        ValWithErr entry_id;
        ValWithErr entry_iso;
        entry_id  = GetValsRunRange2D( _sfhists_mu_id,  eta, pt );
        entry_iso = GetValsRunRange2D( _sfhists_mu_iso, eta, pt );

        idsfs.push_back( entry_id.val );
        iderrsup.push_back( entry_id.err_up );
        iderrsdn.push_back( entry_id.err_dn );

        isosfs.push_back( entry_iso.val );
        isoerrsup.push_back( entry_iso.err_up);
        isoerrsdn.push_back( entry_iso.err_dn);

        //trksfs.push_back( entry_trk.val);
        //trkerrsup.push_back( entry_trk.err_up );
        //trkerrsdn.push_back( entry_trk.err_dn );

        // tracking scale factor is 1.0
        // https://hypernews.cern.ch/HyperNews/CMS/get/muon/1425.html

	//////  Begin Rochester corrections! //////
	if( OUT::isData) {
	  double dtSF = rc.kScaleDT(Q, pt, eta, phi, 0, 0); //data, central correction
	  std::vector<double> dtSF_errs;
	  
	  //get statistical error (set 1)
	  double dtSF_statmean = 0.;
	  double dtSF_statvar = 0;
	  std::vector<double> dtSF_staterrs;
	  for (int i = 0; i < 100; i++)
	    {
	      double f = rc.kScaleDT(Q, pt, eta, phi, 1, i);
	      dtSF_staterrs.push_back(f);
	      dtSF_statmean += f;
	    }
	  dtSF_statmean = dtSF_statmean/100.;
	  for (int i = 0; i < 100; i++)
	    {
	      dtSF_statvar += pow(dtSF_staterrs.at(i) - dtSF_statmean, 2);
	    }
	  dtSF_statvar = dtSF_statvar/100.;
	  dtSF_errs.push_back(sqrt(dtSF_statvar));

	  //get systematic errors (set 2-5)
	  for (int i = 2; i < 6; i++)
	    {
	      double dtSF_witherr = rc.kScaleDT(Q, pt, eta, phi, i, 0);
	      dtSF_errs.push_back(dtSF_witherr - dtSF);
	    }

	  // total error = quadrature sum of stat and sys errors
	  double dtSFerr = 0.;
	  for (int i = 0; i < 5; i++)
	    {
	      dtSFerr += (dtSF_errs.at(i))*(dtSF_errs.at(i));
	    }
	  dtSFerr = sqrt(dtSFerr);

	  rcsfs.push_back(dtSF);
	  rcsfserr.push_back(dtSFerr);
	}
	else {
	  //double u = gRandom->Rndm();
	  float genpt   =   OUT::mu_truthMatchMu_pt ->at(idx);
	  double mcSF = rc.kSpreadMC(Q, pt, eta, phi, genpt, 0, 0); //MC scale and extra smearing with matched gen muon
	  //double mcSF = rc.kSmearMC(Q, pt, eta, phi, nl, u, 0, 0); //MC scale and extra smearing when matched gen muon is not available
	  std::vector<double> mcSF_errs;
	  
	  //get statistical error (set 1)
	  double mcSF_statmean = 0.;
	  double mcSF_statvar = 0;
	  std::vector<double> mcSF_staterrs;
	  for (int i = 0; i < 100; i++)
	    {
	      double f = rc.kSpreadMC(Q, pt, eta, phi, genpt, 1, i);
	      //double f = rc.kSmearMC(Q, pt, eta, phi, nl, u, 1, i); // matched gen muon not available
	      mcSF_staterrs.push_back(f);
	      mcSF_statmean += f;
	    }
	  mcSF_statmean = mcSF_statmean/100.;
	  for (int i = 0; i < 100; i++)
	    {
	      mcSF_statvar += pow(mcSF_staterrs.at(i) - mcSF_statmean, 2);
	    }
	  mcSF_statvar = mcSF_statvar/100.;
	  mcSF_errs.push_back(sqrt(mcSF_statvar));

	  //get systematic errors (set 2-5)
	  for (int i = 2; i < 6; i++)
	    {
	      double mcSF_witherr = rc.kSpreadMC(Q, pt, eta, phi, genpt, i, 0);
	      //mcSF_witherr = rc.kSmearMC(Q, pt, eta, phi, nl, u, i, 0); // matched gen muon not available
	      mcSF_errs.push_back(mcSF_witherr - mcSF);
	    }

	  // total error = quadrature sum of stat and sys errors
	  double mcSFerr = 0.;
	  for (int i = 0; i < 5; i++)
	    {
	      mcSFerr += (mcSF_errs.at(i))*(mcSF_errs.at(i));
	    }
	  mcSFerr = sqrt(mcSFerr);

	  rcsfs.push_back(mcSF);
	  rcsfserr.push_back(mcSFerr);
	}
	
	//////  End Rochester corrections! //////

    }

    if( OUT::mu_n == 1 ) {

        OUT::mu_idSF   = idsfs[0];
        OUT::mu_idSFUP = idsfs[0] + iderrsup[0];
        OUT::mu_idSFDN = idsfs[0] - iderrsdn[0];

        OUT::mu_isoSF   = isosfs[0];
        OUT::mu_isoSFUP = isosfs[0] + isoerrsup[0];
        OUT::mu_isoSFDN = isosfs[0] - isoerrsdn[0];

	OUT::mu_rcSF = rcsfs[0];
	OUT::mu_rcSFUP = rcsfs[0] + rcsfserr[0];
	OUT::mu_rcSFDN = rcsfs[0] - rcsfserr[0];
    }
    else if( OUT::mu_n > 1 ) {

        OUT::mu_idSF = idsfs[0]*idsfs[1];
        OUT::mu_idSFUP = ( idsfs[0] + iderrsup[0] ) *  ( idsfs[1] + iderrsup[1] );
        OUT::mu_idSFDN = ( idsfs[0] - iderrsdn[0] ) *  ( idsfs[1] - iderrsdn[1] );

        OUT::mu_isoSF = isosfs[0]*isosfs[1];
        OUT::mu_isoSFUP = ( isosfs[0] + isoerrsup[0] ) *  ( isosfs[1] + isoerrsup[1] );
        OUT::mu_isoSFDN = ( isosfs[0] - isoerrsdn[0] ) *  ( isosfs[1] - isoerrsdn[1] );

	OUT::mu_rcSF = rcsfs[0]*rcsfs[1];
	OUT::mu_rcSFUP = (rcsfs[0] + rcsfserr[0])*(rcsfs[1] + rcsfserr[1]);
	OUT::mu_rcSFDN = (rcsfs[0] - rcsfserr[0])*(rcsfs[1] - rcsfserr[1]);
    }

#endif
}

template<class HIST> ValWithErr RunModule::GetVals2D( const HIST* hist, float xvar, float yvar ) const {

    ValWithErr result;

    int nbinsX = hist->GetNbinsX();
    int nbinsY = hist->GetNbinsY();

    float min_x = hist->GetXaxis()->GetBinLowEdge(1);
    float max_x = hist->GetXaxis()->GetBinUpEdge(nbinsX);

    float min_y = hist->GetYaxis()->GetBinLowEdge(1);
    float max_y = hist->GetYaxis()->GetBinUpEdge(nbinsY);

    int bin_x = hist->GetXaxis()->FindBin( xvar );
    int bin_y = hist->GetYaxis()->FindBin( yvar );

    if( xvar < min_x ) {
        std::cout << "GetVals -- WARNING : Particle xvar of " << xvar << " exceeds minimum histogram value of " << min_x << std::endl;
        bin_x = 1;
    }
    if( xvar > max_x ) {
        if( max_x < 100 ) std::cout << "GetVals -- WARNING : Particle xvar of " << xvar << " exceeds maximum histogram value of " << max_x << std::endl;
        bin_x = nbinsX;
    }
    if( yvar < min_y ) {
        std::cout << "GetVals -- WARNING : Particle yvar of " << yvar << " exceeds minimum histogram value of " << min_y << std::endl;
        bin_y = 1;
    }
    if( yvar > max_y ) {
        if( max_y < 100 ) std::cout << "GetVals -- WARNING : Particle yvar of " << yvar << " exceeds maximum histogram value of " << max_y << std::endl;
        bin_y = nbinsY;
    }

    result.val    = hist->GetBinContent( bin_x, bin_y );
    result.err_up = hist->GetBinError( bin_x, bin_y ) ;
    result.err_dn = result.err_up;

    return result;

}



template<class HIST> ValWithErr RunModule::GetValsRunRange2D( const std::vector<std::pair<float, HIST*> > range_hists, float xvar, float yvar) const {

    ValWithErr result;

    float total_lumi = 0;
    float sum_cv = 0;
    float sum_err = 0;
    //for( std::vector<std::pair<float, TH2D*> >::const_iterator itr = range_hists.begin();
    //
    for( auto itr = range_hists.begin();
        itr != range_hists.end(); ++itr ) {
        if( !itr->second ) {
            std::cout << "GetValsRunRange2D -- ERROR : hist does not exist " << std::endl;
        }

        ValWithErr thisres = GetVals2D( itr->second, xvar, yvar );

        float this_lumi = itr->first;

        total_lumi += this_lumi;

        sum_cv += this_lumi*thisres.val;
        sum_err += this_lumi*thisres.err_up;

    }

    result.val = sum_cv / total_lumi;
    result.err_up = sum_err / total_lumi;
    result.err_dn = result.err_up;

    return result;

}


ValWithErr RunModule::GetValsFromGraph( const TGraphAsymmErrors *graph, float pt, bool debug ) const {

    ValWithErr result;

    for( int point = 0; point < graph->GetN(); ++point ) {

        double x;
        double y;

        graph->GetPoint( point, x, y );
        float xerrmin = graph->GetErrorXlow(point);
        float xerrmax = graph->GetErrorXhigh(point);

        float xmin = x - xerrmin;
        float xmax = x + xerrmax;

        if( pt >= xmin && pt < xmax )  {
            float yerrmin = graph->GetErrorYlow(point);
            float yerrmax = graph->GetErrorYhigh(point);

            result.val = y;
            result.err_up = yerrmax;
            result.err_dn = yerrmin;

            return result;

        }

    }

    // if we get here then the value wasnt
    // within the graph.  Check if its above
    // and return the last entry
    
    double x;
    double y;

    int last_point = graph->GetN()-1;
    graph->GetPoint( last_point, x, y );
    float xerrmax = graph->GetErrorXhigh(last_point);

    if( pt > ( x + xerrmax ) ) {
        result.val = y;
        result.err_up = graph->GetErrorYhigh(last_point);
        result.err_dn = graph->GetErrorYlow(last_point);

        return result;
    }

    if( debug ) {
        std::cout << "No entries for pt " << pt << " in graph " << graph->GetName() << std::endl;
    }

    result.val = -1;

    return result;

}
