#include "include/RunAnalysis.h"

#include <math.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <boost/algorithm/string.hpp>
#include <boost/foreach.hpp>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>

#include "include/BranchDefs.h"
#include "include/BranchInit.h"
#include "BTagCalibrationStandalone.cxx"

#include "Util.h"

#include "TFile.h"

int main(int argc, char **argv) {
    // TH1::AddDirectory(kFALSE);
    CmdOptions options = ParseOptions(argc, argv);

    // Parse the text file and form the configuration object
    AnaConfig ana_config = ParseConfig(options.config_file, options);
    std::cout << "Configured " << ana_config.size() << " analysis modules "
              << std::endl;

    RunModule runmod;
    ana_config.Run(runmod, options);

    std::cout << "^_^ Finished ^_^" << std::endl;
}

void RunModule::initialize(TChain *chain, TTree *outtree, TFile *outfile,
                           const CmdOptions &options,
                           std::vector<ModuleConfig> &configs) {
    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree(outtree);

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

    OUT::el_recoSF = -1;
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

#endif

#ifdef MODULE_AddBJetSF
    OUT::jet_btagSF = -1;
    OUT::jet_btagSFUP = -1;
    OUT::jet_btagSFDN = -1;
#endif

    // *************************
    // Declare Branches
    // *************************

    // Examples :
#ifdef MODULE_AddElectronSF
    outtree->Branch("el_trigSF", &OUT::el_trigSF, "el_trigSF/F");
    outtree->Branch("el_trigSFUP", &OUT::el_trigSFUP, "el_trigSFUP/F");
    outtree->Branch("el_trigSFDN", &OUT::el_trigSFDN, "el_trigSFDN/F");
    outtree->Branch("el_idSF", &OUT::el_idSF, "el_idSF/F");
    outtree->Branch("el_idSFUP", &OUT::el_idSFUP, "el_idSFUP/F");
    outtree->Branch("el_idSFDN", &OUT::el_idSFDN, "el_idSFDN/F");
    outtree->Branch("el_recoSF", &OUT::el_recoSF, "el_recoSF/F");
    outtree->Branch("el_recoSFUP", &OUT::el_recoSFUP, "el_recoSFUP/F");
    outtree->Branch("el_recoSFDN", &OUT::el_recoSFDN, "el_recoSFDN/F");
#endif

#ifdef MODULE_AddPhotonSF
    outtree->Branch("ph_idSF", &OUT::ph_idSF, "ph_idSF/F");
    outtree->Branch("ph_idSFUP", &OUT::ph_idSFUP, "ph_idSFUP/F");
    outtree->Branch("ph_idSFDN", &OUT::ph_idSFDN, "ph_idSFDN/F");
    outtree->Branch("ph_psvSF", &OUT::ph_psvSF, "ph_psvSF/F");
    outtree->Branch("ph_psvSFUP", &OUT::ph_psvSFUP, "ph_psvSFUP/F");
    outtree->Branch("ph_psvSFDN", &OUT::ph_psvSFDN, "ph_psvSFDN/F");
    outtree->Branch("ph_csevSF", &OUT::ph_csevSF, "ph_csevSF/F");
    outtree->Branch("ph_csevSFUP", &OUT::ph_csevSFUP, "ph_csevSFUP/F");
    outtree->Branch("ph_csevSFDN", &OUT::ph_csevSFDN, "ph_csevSFDN/F");
#endif

#ifdef MODULE_AddMuonSF
    outtree->Branch("mu_trigSF", &OUT::mu_trigSF, "mu_trigSF/F");
    outtree->Branch("mu_trigSFUP", &OUT::mu_trigSFUP, "mu_trigSFUP/F");
    outtree->Branch("mu_trigSFDN", &OUT::mu_trigSFDN, "mu_trigSFDN/F");
    outtree->Branch("mu_isoSF", &OUT::mu_isoSF, "mu_isoSF/F");
    outtree->Branch("mu_isoSFUP", &OUT::mu_isoSFUP, "mu_isoSFUP/F");
    outtree->Branch("mu_isoSFDN", &OUT::mu_isoSFDN, "mu_isoSFDN/F");
    outtree->Branch("mu_trkSF", &OUT::mu_trkSF, "mu_trkSF/F");
    outtree->Branch("mu_trkSFUP", &OUT::mu_trkSFUP, "mu_trkSFUP/F");
    outtree->Branch("mu_trkSFDN", &OUT::mu_trkSFDN, "mu_trkSFDN/F");
    outtree->Branch("mu_idSF", &OUT::mu_idSF, "mu_idSF/F");
    outtree->Branch("mu_idSFUP", &OUT::mu_idSFUP, "mu_idSFUP/F");
    outtree->Branch("mu_idSFDN", &OUT::mu_idSFDN, "mu_idSFDN/F");
#endif

#ifdef MODULE_AddBJetSF
    outtree->Branch("jet_btagSF",   &OUT::jet_btagSF,   "jet_btagSF/F");
    outtree->Branch("jet_btagSFUP", &OUT::jet_btagSFUP, "jet_btagSFUP/F");
    outtree->Branch("jet_btagSFDN", &OUT::jet_btagSFDN, "jet_btagSFDN/F");
#endif
    // store the lumis for averaging
    /*float int_lumi_b = 5933692351.209;
  float int_lumi_c = 2761135761.229;
  float int_lumi_d = 4525903884.794;
  float int_lumi_e = 4318519409.159;
  float int_lumi_f = 3370228550.294;
  float int_lumi_g = 8015343899.163;
  float int_lumi_h = 9199511317.095;

  float int_lumi_bcdef = int_lumi_b + int_lumi_c + int_lumi_d + int_lumi_e +
  int_lumi_f; float int_lumi_gh  = int_lumi_g + int_lumi_h;
  */
    BOOST_FOREACH (ModuleConfig &mod_conf, configs) {
        std::cout << "Module: " << mod_conf.GetName() << std::endl;
        if (mod_conf.GetName() == "AddMuonSF") {
            std::map<std::string, std::string>::const_iterator muyear =
                mod_conf.GetInitData().find("year");
            if (muyear != mod_conf.GetInitData().end()) {
                _year_mu = std::stoi(muyear->second);
                std::cout << "year = " << _year_mu << std::endl;
            }

            std::map<std::string, std::string>::const_iterator bcdef;
            std::map<std::string, std::string>::const_iterator gh;
            bcdef = mod_conf.GetInitData().find("LumiBCDEF");
            gh = mod_conf.GetInitData().find("LumiGH");
            float lumi_bcdef = 0.;
            float lumi_gh = 0.;
            if (bcdef != mod_conf.GetInitData().end()) {
                lumi_bcdef = std::stof(bcdef->second);
                std::cout << "lumi bcdef = " << lumi_bcdef << std::endl;
            } else {
                std::cout << "Warning: could not get integrated luminosity for BCDEF!"
                          << std::endl;
            }
            if (gh != mod_conf.GetInitData().end()) {
                lumi_gh = std::stof(gh->second);
                std::cout << "lumi gh = " << lumi_gh << std::endl;
            } else {
                std::cout << "Warning: could not get integrated luminosity for GH!"
                          << std::endl;
            }

            std::map<std::string, std::string>::const_iterator itr;
            std::map<std::string, std::string>::const_iterator hname;

            itr = mod_conf.GetInitData().find("FilePathIsoBCDEF");
            hname = mod_conf.GetInitData().find("HistIsoBCDEF");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_mu_iso_bcdef = TFile::Open((itr->second).c_str(), "READ");
                if (_sffile_mu_iso_bcdef->IsOpen()) {
                    TH2D *thishist = dynamic_cast<TH2D *>(
                        _sffile_mu_iso_bcdef->Get((hname->second).c_str()));
                    if (!thishist) {
                        std::cout << "could not get hist from file "
                                  << _sffile_mu_iso_bcdef->GetName() << std::endl;
                    }
                    _sfhists_mu_iso.push_back(std::make_pair(lumi_bcdef, thishist));
                } else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find("FilePathIsoGH");
            hname = mod_conf.GetInitData().find("HistIsoGH");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_mu_iso_gh = TFile::Open((itr->second).c_str(), "READ");
                if (_sffile_mu_iso_gh->IsOpen()) {
                    TH2D *thishist = dynamic_cast<TH2D *>(
                        _sffile_mu_iso_gh->Get((hname->second).c_str()));
                    if (!thishist) {
                        std::cout << "could not get hist from file "
                                  << _sffile_mu_iso_gh->GetName() << std::endl;
                    }
                    _sfhists_mu_iso.push_back(std::make_pair(lumi_gh, thishist));
                } else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find("FilePathIdBCDEF");
            hname = mod_conf.GetInitData().find("HistIdBCDEF");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_mu_id_bcdef = TFile::Open((itr->second).c_str(), "READ");
                if (_sffile_mu_id_bcdef->IsOpen()) {
                    TH2D *thishist = dynamic_cast<TH2D *>(
                        _sffile_mu_id_bcdef->Get((hname->second).c_str()));
                    if (!thishist) {
                        std::cout << "could not get hist from file "
                                  << _sffile_mu_id_bcdef->GetName() << std::endl;
                    }
                    _sfhists_mu_id.push_back(std::make_pair(lumi_bcdef, thishist));
                } else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find("FilePathIdGH");
            hname = mod_conf.GetInitData().find("HistIdGH");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_mu_id_gh = TFile::Open((itr->second).c_str(), "READ");
                if (_sffile_mu_id_gh->IsOpen()) {
                    TH2D *thishist = dynamic_cast<TH2D *>(
                        _sffile_mu_id_gh->Get((hname->second).c_str()));
                    if (!thishist) {
                        std::cout << "could not get hist from file "
                                  << _sffile_mu_id_gh->GetName() << std::endl;
                    }
                    _sfhists_mu_id.push_back(std::make_pair(lumi_gh, thishist));
                } else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find("FilePathTrigBCDEF");
            hname = mod_conf.GetInitData().find("HistTrigBCDEF");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_mu_trig_bcdef = TFile::Open((itr->second).c_str(), "READ");
                if (_sffile_mu_trig_bcdef->IsOpen()) {
                    TH2F *thishist = dynamic_cast<TH2F *>(
                        _sffile_mu_trig_bcdef->Get((hname->second).c_str()));
                    if (!thishist) {
                        std::cout << "could not get hist from file "
                                  << _sffile_mu_trig_bcdef->GetName() << std::endl;
                    }
                    _sfhists_mu_trig.push_back(std::make_pair(lumi_bcdef, thishist));
                    hname = mod_conf.GetInitData().find("HistTrigBCDEFdata");
                    thishist = dynamic_cast<TH2F *>(
                        _sffile_mu_trig_bcdef->Get((hname->second).c_str()));
                    if (!thishist) {
                        std::cout << "could not get hist from file "
                                  << _sffile_mu_trig_bcdef->GetName() << std::endl;
                    }
                    _effhists_mu_trig_data.push_back(
                        std::make_pair(lumi_bcdef, thishist));
                    hname = mod_conf.GetInitData().find("HistTrigBCDEFmc");
                    thishist = dynamic_cast<TH2F *>(
                        _sffile_mu_trig_bcdef->Get((hname->second).c_str()));
                    if (!thishist) {
                        std::cout << "could not get hist from file "
                                  << _sffile_mu_trig_bcdef->GetName() << std::endl;
                    }
                    _effhists_mu_trig_mc.push_back(std::make_pair(lumi_bcdef, thishist));
                } else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find("FilePathTrigGH");
            hname = mod_conf.GetInitData().find("HistTrigGH");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_mu_trig_gh = TFile::Open((itr->second).c_str(), "READ");
                if (_sffile_mu_trig_gh->IsOpen()) {
                    TH2F *thishist = dynamic_cast<TH2F *>(
                        _sffile_mu_trig_gh->Get((hname->second).c_str()));
                    if (!thishist) {
                        std::cout << "could not get hist from file "
                                  << _sffile_mu_trig_gh->GetName() << std::endl;
                    }
                    _sfhists_mu_trig.push_back(std::make_pair(lumi_gh, thishist));
                    hname = mod_conf.GetInitData().find("HistTrigGHdata");
                    thishist = dynamic_cast<TH2F *>(
                        _sffile_mu_trig_gh->Get((hname->second).c_str()));
                    if (!thishist) {
                        std::cout << "could not get hist from file "
                                  << _sffile_mu_trig_gh->GetName() << std::endl;
                    }
                    _effhists_mu_trig_data.push_back(std::make_pair(lumi_gh, thishist));
                    hname = mod_conf.GetInitData().find("HistTrigGHmc");
                    thishist = dynamic_cast<TH2F *>(
                        _sffile_mu_trig_gh->Get((hname->second).c_str()));
                    if (!thishist) {
                        std::cout << "could not get hist from file "
                                  << _sffile_mu_trig_gh->GetName() << std::endl;
                    }
                    _effhists_mu_trig_mc.push_back(std::make_pair(lumi_gh, thishist));
                } else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
        }
        if (mod_conf.GetName() == "AddElectronSF") {
            std::map<std::string, std::string>::const_iterator elyear =
                mod_conf.GetInitData().find("year");
            if (elyear != mod_conf.GetInitData().end()) {
                _year_el = std::stoi(elyear->second);
                std::cout << "year = " << _year_el << std::endl;
            }
            std::map<std::string, std::string>::const_iterator itr;
            std::map<std::string, std::string>::const_iterator hname;

            itr = mod_conf.GetInitData().find("FilePathCutID");
            hname = mod_conf.GetInitData().find("HistCutID");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_el_id = TFile::Open((itr->second).c_str(), "READ");
                _sfhist_el_id =
                    dynamic_cast<TH2F *>(_sffile_el_id->Get((hname->second).c_str()));
            }
            itr = mod_conf.GetInitData().find("FilePathRecoHighPt");
            hname = mod_conf.GetInitData().find("HistRecoHighPt");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_el_recohighpt = TFile::Open((itr->second).c_str(), "READ");
                _sfhist_el_recohighpt = dynamic_cast<TH2F *>(
                    _sffile_el_recohighpt->Get((hname->second).c_str()));
            }
            itr = mod_conf.GetInitData().find("FilePathRecoLowPt");
            hname = mod_conf.GetInitData().find("HistRecoLowPt");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_el_recolowpt = TFile::Open((itr->second).c_str(), "READ");
                _sfhist_el_recolowpt = dynamic_cast<TH2F *>(
                    _sffile_el_recolowpt->Get((hname->second).c_str()));
            }
            itr = mod_conf.GetInitData().find("FilePathTrigEl");
            hname = mod_conf.GetInitData().find("HistTrigEl");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_el_trig = TFile::Open((itr->second).c_str(), "READ");
                if (_sffile_el_trig->IsOpen()) {
                    _sfhist_el_trig = dynamic_cast<TH2F *>(
                        _sffile_el_trig->Get((hname->second).c_str()));
                    if (!_sfhist_el_trig) {
                        std::cout << "could not get hist from file "
                                  << _sffile_el_trig->GetName() << std::endl;
                    }
                    hname = mod_conf.GetInitData().find("HistTrigElData");
                    _effhist_el_trig_data = dynamic_cast<TH2F *>(
                        _sffile_el_trig->Get((hname->second).c_str()));
                    if (!_effhist_el_trig_data) {
                        std::cout << "could not get hist from file "
                                  << _sffile_el_trig->GetName() << std::endl;
                    }
                    hname = mod_conf.GetInitData().find("HistTrigElMC");
                    _effhist_el_trig_mc = dynamic_cast<TH2F *>(
                        _sffile_el_trig->Get((hname->second).c_str()));
                    if (!_effhist_el_trig_mc) {
                        std::cout << "could not get hist from file "
                                  << _sffile_el_trig->GetName() << std::endl;
                    }
                } else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
        }
        if (mod_conf.GetName() == "AddBJetSF") {

            std::map<std::string, std::string>::const_iterator itr;
            std::map<std::string, std::string>::const_iterator hname;

            itr = mod_conf.GetInitData().find("FilePath");
            if (itr != mod_conf.GetInitData().end()) {
              calib =  new BTagCalibration("csvv1", (itr->second).c_str());

              BTagEntry::OperatingPoint cutpoint = BTagEntry::OP_LOOSE;
              itr = mod_conf.GetInitData().find("CutPoint");
              if (itr != mod_conf.GetInitData().end()) {
                if (itr->second == "tight")  cutpoint = BTagEntry::OP_TIGHT;
                if (itr->second == "medium") cutpoint = BTagEntry::OP_MEDIUM;
                if (itr->second == "loose")  cutpoint = BTagEntry::OP_LOOSE;
              }
              reader = new BTagCalibrationReader(cutpoint,  // operating poin
                                           "central",             // central sys type
                                           {"up", "down"});      // other sys types

              reader->load(*calib,                // calibration instance
                          BTagEntry::FLAV_B,    // btag flavour
                          "comb");               // measurement type

              reader->load(*calib,                // calibration instance
                          BTagEntry::FLAV_C,    // btag flavour
                          "comb");               // measurement type

              reader->load(*calib,                // calibration instance
                          BTagEntry::FLAV_UDSG,    // btag flavour
                          "incl");               // measurement type 
            }

            itr = mod_conf.GetInitData().find("HistPath");
            if (itr != mod_conf.GetInitData().end()) {
              _efffile_jet = TFile::Open((itr->second).c_str(),"READ");
              if (_efffile_jet->IsOpen()) {

                hname = mod_conf.GetInitData().find("HistBJetEff");
                if (hname != mod_conf.GetInitData().end()) {
                    _effhist_jet_b = dynamic_cast<TH2F*>(_efffile_jet->Get((hname->second).c_str()));
                }
                hname = mod_conf.GetInitData().find("HistCJetEff");
                if (hname != mod_conf.GetInitData().end()) {
                    _effhist_jet_c = dynamic_cast<TH2F*>(_efffile_jet->Get((hname->second).c_str()));
                }
                hname = mod_conf.GetInitData().find("HistLJetEff");
                if (hname != mod_conf.GetInitData().end()) {
                    _effhist_jet_l = dynamic_cast<TH2F*>(_efffile_jet->Get((hname->second).c_str()));
                }
              }
            
            }

        }
        if (mod_conf.GetName() == "AddPhotonSF") {
            std::map<std::string, std::string>::const_iterator phyear =
                mod_conf.GetInitData().find("year");
            if (phyear != mod_conf.GetInitData().end()) {
                _year_ph = std::stoi(phyear->second);
            }

            std::map<std::string, std::string>::const_iterator itr;

            itr = mod_conf.GetInitData().find("HiPtId_inner_const");
            if (itr != mod_conf.GetInitData().end())
                _HiPtId_inner_const = std::stod(itr->second);
            itr = mod_conf.GetInitData().find("HiPtId_inner_cov00");
            if (itr != mod_conf.GetInitData().end())
                _HiPtId_inner_cov00 = std::stod(itr->second);
            itr = mod_conf.GetInitData().find("HiPtId_inner_cov01");
            if (itr != mod_conf.GetInitData().end())
                _HiPtId_inner_cov01 = std::stod(itr->second);
            itr = mod_conf.GetInitData().find("HiPtId_inner_cov11");
            if (itr != mod_conf.GetInitData().end())
                _HiPtId_inner_cov11 = std::stod(itr->second);
            itr = mod_conf.GetInitData().find("HiPtId_outer_const");
            if (itr != mod_conf.GetInitData().end())
                _HiPtId_outer_const = std::stod(itr->second);
            itr = mod_conf.GetInitData().find("HiPtId_outer_cov00");
            if (itr != mod_conf.GetInitData().end())
                _HiPtId_outer_cov00 = std::stod(itr->second);
            itr = mod_conf.GetInitData().find("HiPtId_outer_cov01");
            if (itr != mod_conf.GetInitData().end())
                _HiPtId_outer_cov01 = std::stod(itr->second);
            itr = mod_conf.GetInitData().find("HiPtId_outer_cov11");
            if (itr != mod_conf.GetInitData().end())
                _HiPtId_outer_cov11 = std::stod(itr->second);

            std::map<std::string, std::string>::const_iterator hname;

            itr = mod_conf.GetInitData().find("FilePathId");
            hname = mod_conf.GetInitData().find("HistId");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_ph_id = TFile::Open((itr->second).c_str(), "READ");
                if (_sffile_ph_id->IsOpen()) {
                    _sfhist_ph_id =
                        dynamic_cast<TH2F *>(_sffile_ph_id->Get((hname->second).c_str()));
                    if (!_sfhist_ph_id) {
                        std::cout << "could not get hist from file "
                                  << _sffile_ph_id->GetName() << std::endl;
                    }
                } else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find("FilePathPSveto");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_ph_psv = TFile::Open((itr->second).c_str(), "READ");
                if (_sffile_ph_psv->IsOpen()) {
                    hname = mod_conf.GetInitData().find("HistPSveto");
                    if (_year_ph == 2016) {
                        _sfhist_ph_psv = dynamic_cast<TH2D *>(
                            _sffile_ph_psv->Get((hname->second).c_str()));
                        if (!_sfhist_ph_psv)
                            std::cout << "Could not get PSV hist from file "
                                      << _sffile_ph_psv->GetName() << std::endl;
                    }
                    if (_year_ph == 2017) {
                        _sfhist_ph_psv_2017 = dynamic_cast<TH1F *>(
                            _sffile_ph_psv->Get((hname->second).c_str()));
                        if (!_sfhist_ph_psv_2017)
                            std::cout << "Could not get PSV hist from file "
                                      << _sffile_ph_psv->GetName() << std::endl;
                    }
                    if (_year_ph == 2018) {
                        _sfhist_ph_psv_2018 = dynamic_cast<TH2F *>(
                            _sffile_ph_psv->Get((hname->second).c_str()));
                        if (!_sfhist_ph_psv_2018)
                            std::cout << "Could not get PSV hist from file "
                                      << _sffile_ph_psv->GetName() << std::endl;
                        hname = mod_conf.GetInitData().find("HistPSveto_err");
                        _sfhist_ph_psv_2018_err = dynamic_cast<TH2F *>(
                            _sffile_ph_psv->Get((hname->second).c_str()));
                        if (!_sfhist_ph_psv_2018_err)
                            std::cout << "Could not get PSV err hist from file "
                                      << _sffile_ph_psv->GetName() << std::endl;
                    }
                } else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
            itr = mod_conf.GetInitData().find("FilePathEveto");
            if (itr != mod_conf.GetInitData().end()) {
                _sffile_ph_ev = TFile::Open((itr->second).c_str(), "READ");
                if (_sffile_ph_ev->IsOpen()) {
                    hname = mod_conf.GetInitData().find("HistCSEveto");
                    if (_year_ph == 2016) {
                        _sfhist_ph_csev =
                            dynamic_cast<TH2D *>(_sffile_ph_ev->Get((hname->second).c_str()));
                        if (!_sfhist_ph_csev)
                            std::cout << "Could not get CSEV 2D hist from file "
                                      << _sffile_ph_ev->GetName() << std::endl;
                    }
                    if (_year_ph == 2017) {
                        _sfhist_ph_csev_2017 =
                            dynamic_cast<TH1F *>(_sffile_ph_ev->Get((hname->second).c_str()));
                        if (!_sfhist_ph_csev_2017)
                            std::cout << "Could not get CSEV 2D hist from file "
                                      << _sffile_ph_ev->GetName() << std::endl;
                    }
                    if (_year_ph == 2018) {
                        _sfhist_ph_csev_2018 =
                            dynamic_cast<TH2F *>(_sffile_ph_ev->Get((hname->second).c_str()));
                        if (!_sfhist_ph_csev_2018)
                            std::cout << "Could not get CSEV 2D hist from file "
                                      << _sffile_ph_ev->GetName() << std::endl;
                        hname = mod_conf.GetInitData().find("HistCSEveto_err");
                        _sfhist_ph_csev_2018_err = dynamic_cast<TH2F *>(
                            _sffile_ph_ev->Get((hname->second).c_str()));
                        if (!_sfhist_ph_csev_2018_err)
                            std::cout << "Could not get CSEV err hist from file "
                                      << _sffile_ph_ev->GetName() << std::endl;
                    }
                } else {
                    std::cout << "Could not open file " << itr->second << std::endl;
                }
            }
        }
    }
}

bool RunModule::execute(std::vector<ModuleConfig> &configs) {
    // In BranchInit
    CopyInputVarsToOutput();

    // loop over configured modules
    bool save_event = true;
    BOOST_FOREACH (ModuleConfig &mod_conf, configs) {
        save_event &= ApplyModule(mod_conf);
    }

    return save_event;
}

bool RunModule::ApplyModule(ModuleConfig &config) const {
    bool keep_evt = true;

    if (config.GetName() == "AddElectronSF") {
        AddElectronSF(config);
    }
    if (config.GetName() == "AddMuonSF") {
        AddMuonSF(config);
    }
    if (config.GetName() == "AddPhotonSF") {
        AddPhotonSF(config);
    }
    if (config.GetName() == "AddBJetSF") {
        AddBJetSF(config);
    }

    return keep_evt;
}

void RunModule::AddElectronSF(ModuleConfig & /*config*/) const {
#ifdef MODULE_AddElectronSF

    OUT::el_trigSF = 1.0;
    OUT::el_trigSFUP = 1.0;
    OUT::el_trigSFDN = 1.0;

    OUT::el_idSF = 1.0;
    OUT::el_idSFUP = 1.0;
    OUT::el_idSFDN = 1.0;

    OUT::el_recoSF = 1.0;
    OUT::el_recoSFUP = 1.0;
    OUT::el_recoSFDN = 1.0;

    if (OUT::isData) {
        return;
    }

    std::vector<float> trsfs;
    std::vector<float> trerrs;
    std::vector<float> treffs_data;
    std::vector<float> trerrs_data;
    std::vector<float> treffs_mc;
    std::vector<float> trerrs_mc;

    for (int idx = 0; idx < OUT::el_n; ++idx) {
        float eta = OUT::el_eta->at(idx);
        float pt = OUT::el_pt->at(idx);

        float ptcut = -999.;
        if (_year_el == 2016)
            ptcut = 35.;
        else if (_year_el == 2017)
            ptcut = 40.;
        else if (_year_el == 2018)
            ptcut = 35.;
        else
            std::cout << "ERROR AddElectronSF: year not recognized!" << std::endl;

        if (!(pt > ptcut && fabs(eta) < 2.4)) {
            std::cout << "AddElectronSF -- WARNING : electron pt or eta out of range "
                      << pt << " " << eta << std::endl;
        }

        ValWithErr entry;
        ValWithErr entry_data;
        ValWithErr entry_mc;
        entry = GetVals2D(_sfhist_el_trig, eta, pt);
        entry_data = GetVals2D(_effhist_el_trig_data, eta, pt);
        entry_mc = GetVals2D(_effhist_el_trig_mc, eta, pt);

        trsfs.push_back(entry.val);
        trerrs.push_back(entry.err_up);
        treffs_data.push_back(entry_data.val);
        trerrs_data.push_back(entry_data.err_up);
        treffs_mc.push_back(entry_mc.val);
        trerrs_mc.push_back(entry_mc.err_up);
    }

    if (OUT::el_n == 1) {
        OUT::el_trigSF = trsfs[0];
        OUT::el_trigSFUP = trsfs[0] + trerrs[0];
        OUT::el_trigSFDN = trsfs[0] - trerrs[0];
    } else if (OUT::el_n > 1) {
        double eff_data = 1 - (1 - treffs_data[0]) * (1 - treffs_data[1]);
        double eff_mc = 1 - (1 - treffs_mc[0]) * (1 - treffs_mc[1]);

        double err_data = sqrt(pow(trerrs_data[0] / treffs_data[0], 2) +
                               pow(trerrs_data[1] / treffs_data[1], 2));
        double err_mc = sqrt(pow(trerrs_mc[0] / treffs_mc[0], 2) +
                             pow(trerrs_mc[1] / treffs_mc[1], 2));

        double sf_val = eff_data / eff_mc;
        double sf_err = sqrt(pow(err_data / eff_data, 2) + pow(err_mc / eff_mc, 2));

        OUT::el_trigSF = sf_val;
        OUT::el_trigSFUP = sf_val + sf_err;
        OUT::el_trigSFDN = sf_val - sf_err;
    }

    std::vector<float> sfs_id;
    std::vector<float> errs_id;
    std::vector<float> sfs_reco;
    std::vector<float> errs_reco;

    for (int idx = 0; idx < OUT::el_n; ++idx) {
        /*

    if( OUT::el_triggerMatch->at(idx) ) {

        //https://twiki.cern.ch/twiki/bin/viewauth/CMS/KoPFAElectronTagAndProbe
        if( OUT::el_pt->at(idx) >= 30 && OUT::el_pt->at(idx) <= 40 ) {
            if( fabs(OUT::el_sceta->at(idx)) <= 0.8 ) {
                OUT::el_trigSF = 0.987;
                OUT::el_trigSFUP = OUT::el_trigSF + 0.012;
                OUT::el_trigSFDN = OUT::el_trigSF - 0.017;
            }
            else if( fabs(OUT::el_sceta->at(idx)) > 0.8 && fabs(
    OUT::el_sceta->at(idx) ) <= 1.478 ) { OUT::el_trigSF = 0.964;
                OUT::el_trigSFUP = OUT::el_trigSF + 0.002;
                OUT::el_trigSFDN = OUT::el_trigSF - 0.001;
            }
            else if( fabs(OUT::el_sceta->at(idx)) > 1.478 && fabs(
    OUT::el_sceta->at(idx) ) <= 2.5 ) { OUT::el_trigSF = 1.004; OUT::el_trigSFUP
    = OUT::el_trigSF + 0.006; OUT::el_trigSFDN = OUT::el_trigSF - 0.006;
            }
        }
        else if( OUT::el_pt->at(idx) > 40 && OUT::el_pt->at(idx) <= 50 ) {
            if( fabs(OUT::el_sceta->at(idx)) <= 0.8 ) {
                OUT::el_trigSF = 0.997;
                OUT::el_trigSFUP = OUT::el_trigSF + 0.001;
                OUT::el_trigSFDN = OUT::el_trigSF - 0.001;
            }
            else if( fabs(OUT::el_sceta->at(idx)) > 0.8 && fabs(
    OUT::el_sceta->at(idx) ) <= 1.478 ) { OUT::el_trigSF = 0.980;
                OUT::el_trigSFUP = OUT::el_trigSF + 0.001;
                OUT::el_trigSFDN = OUT::el_trigSF - 0.001;
            }
            else if( fabs(OUT::el_sceta->at(idx)) > 1.478 && fabs(
    OUT::el_sceta->at(idx) ) <= 2.5 ) { OUT::el_trigSF = 1.033; OUT::el_trigSFUP
    = OUT::el_trigSF + 0.007; OUT::el_trigSFDN = OUT::el_trigSF - 0.007;
            }
        }
        else if( OUT::el_pt->at(idx) > 50 ) {
            if( fabs(OUT::el_sceta->at(idx)) <= 0.8 ) {
                OUT::el_trigSF = 0.998;
                OUT::el_trigSFUP = OUT::el_trigSF + 0.002;
                OUT::el_trigSFDN = OUT::el_trigSF - 0.002;
            }
            else if( fabs(OUT::el_sceta->at(idx)) > 0.8 && fabs(
    OUT::el_sceta->at(idx) ) <= 1.478 ) { OUT::el_trigSF = 0.988;
                OUT::el_trigSFUP = OUT::el_trigSF + 0.002;
                OUT::el_trigSFDN = OUT::el_trigSF - 0.002;
            }
            else if( fabs(OUT::el_sceta->at(idx)) > 1.478 && fabs(
    OUT::el_sceta->at(idx) ) <= 2.5 ) { OUT::el_trigSF = 0.976; OUT::el_trigSFUP
    = OUT::el_trigSF + 0.015; OUT::el_trigSFDN = OUT::el_trigSF - 0.012;
            }
        }
    }
    */
        // Do loose scale factors
        //

        float pt = OUT::el_pt->at(idx);
        float eta = OUT::el_eta->at(idx);

        ValWithErr res_id = GetVals2D(_sfhist_el_id, eta, pt);
        ValWithErr res_reco;
        if (pt < 20.0) {
            res_reco = GetVals2D(_sfhist_el_recolowpt, eta, pt);
        } else {
            res_reco = GetVals2D(_sfhist_el_recohighpt, eta, pt);
        }

        sfs_id.push_back(res_id.val);
        errs_id.push_back(res_id.err_up);

        sfs_reco.push_back(res_reco.val);
        errs_reco.push_back(res_reco.err_up);
    }

    if (sfs_id.size() == 1) {
        OUT::el_idSF = sfs_id[0];
        OUT::el_idSFUP = sfs_id[0] + errs_id[0];
        OUT::el_idSFDN = sfs_id[0] - errs_id[0];

        OUT::el_recoSF = sfs_reco[0];
        OUT::el_recoSFUP = sfs_reco[0] + errs_reco[0];
        OUT::el_recoSFDN = sfs_reco[0] - errs_reco[0];
    }

    else if (sfs_id.size() > 1) {
        OUT::el_idSF = sfs_id[0] * sfs_id[1];
        OUT::el_idSFUP = (sfs_id[0] + errs_id[0]) * (sfs_id[1] + errs_id[1]);
        OUT::el_idSFDN = (sfs_id[0] - errs_id[0]) * (sfs_id[1] - errs_id[1]);

        OUT::el_recoSF = sfs_reco[0] * sfs_reco[1];
        OUT::el_recoSFUP =
            (sfs_reco[0] + errs_reco[0]) * (sfs_reco[1] + errs_reco[1]);
        OUT::el_recoSFDN =
            (sfs_reco[0] - errs_reco[0]) * (sfs_reco[1] - errs_reco[1]);
    }
#endif
}

float RunModule::get_ele_cutid_syst(float pt, float eta) const {
    // Uncertainty table, from
    // https://twiki.cern.ch/twiki/bin/view/Main/EGammaScaleFactors2012 pT 10 - 15
    // 15 - 20  20 - 30  30 - 40  40 - 50  50 - 200 0.0 < abs(η) < 0.8      11.00
    // 6.90     1.40     0.28     0.14     0.41 0.8 < abs(η) < 1.442    11.00 6.90
    // 1.40     0.28     0.14     0.41 1.442 < abs(η) < 1.556  11.00    8.30 5.70
    // 2.40     0.28     0.43 1.556 < abs(η) < 2.00   12.00    4.00     2.20 0.59
    // 0.30     0.53 2.0 < abs(η) < 2.5      12.00    4.00     2.20     0.59 0.30
    // 0.53
    //

    if (pt > 10 && pt <= 15) {
        if (fabs(eta) <= 0.8) {
            return 0.11;
        } else if (fabs(eta) > 0.8 && fabs(eta) <= 1.442) {
            return 0.11;
        } else if (fabs(eta) > 1.442 && fabs(eta) <= 1.556) {
            return 0.11;
        } else if (fabs(eta) > 1.556 && fabs(eta) <= 2.0) {
            return 0.12;
        } else if (fabs(eta) > 2.0 && fabs(eta) <= 2.5) {
            return 0.12;
        }
    } else if (pt > 15 && pt <= 20) {
        if (fabs(eta) <= 0.8) {
            return 0.069;
        } else if (fabs(eta) > 0.8 && fabs(eta) <= 1.442) {
            return 0.069;
        } else if (fabs(eta) > 1.442 && fabs(eta) <= 1.556) {
            return 0.083;
        } else if (fabs(eta) > 1.556 && fabs(eta) <= 2.0) {
            return 0.04;
        } else if (fabs(eta) > 2.0 && fabs(eta) <= 2.5) {
            return 0.04;
        }
    } else if (pt > 20 && pt <= 30) {
        if (fabs(eta) <= 0.8) {
            return 0.014;
        } else if (fabs(eta) > 0.8 && fabs(eta) <= 1.442) {
            return 0.014;
        } else if (fabs(eta) > 1.442 && fabs(eta) <= 1.556) {
            return 0.057;
        } else if (fabs(eta) > 1.556 && fabs(eta) <= 2.0) {
            return 0.022;
        } else if (fabs(eta) > 2.0 && fabs(eta) <= 2.5) {
            return 0.022;
        }
    } else if (pt > 30 && pt <= 40) {
        if (fabs(eta) <= 0.8) {
            return 0.0028;
        } else if (fabs(eta) > 0.8 && fabs(eta) <= 1.442) {
            return 0.0028;
        } else if (fabs(eta) > 1.442 && fabs(eta) <= 1.556) {
            return 0.024;
        } else if (fabs(eta) > 1.556 && fabs(eta) <= 2.0) {
            return 0.0059;
        } else if (fabs(eta) > 2.0 && fabs(eta) <= 2.5) {
            return 0.0059;
        }
    } else if (pt > 40 && pt <= 50) {
        if (fabs(eta) <= 0.8) {
            return 0.0014;
        } else if (fabs(eta) > 0.8 && fabs(eta) <= 1.442) {
            return 0.0014;
        } else if (fabs(eta) > 1.442 && fabs(eta) <= 1.556) {
            return 0.0028;
        } else if (fabs(eta) > 1.556 && fabs(eta) <= 2.0) {
            return 0.003;
        } else if (fabs(eta) > 2.0 && fabs(eta) <= 2.5) {
            return 0.003;
        }
    } else if (pt > 50) {
        if (fabs(eta) <= 0.8) {
            return 0.0041;
        } else if (fabs(eta) > 0.8 && fabs(eta) <= 1.442) {
            return 0.0041;
        } else if (fabs(eta) > 1.442 && fabs(eta) <= 1.556) {
            return 0.0043;
        } else if (fabs(eta) > 1.556 && fabs(eta) <= 2.0) {
            return 0.0053;
        } else if (fabs(eta) > 2.0 && fabs(eta) <= 2.5) {
            return 0.0053;
        }
    }

    std::cout << "WARNING NO SF for pt = " << pt << ", eta = " << eta
              << std::endl;

    return -1;
}


void RunModule::AddBJetSF(ModuleConfig & /*config*/) const {
#ifdef MODULE_AddBJetSF
    OUT::jet_btagSF = 1.0;
    OUT::jet_btagSFUP = 1.0;
    OUT::jet_btagSFDN = 1.0;
    
    ValWithErr effval;
    double jet_scalefactor=1;
    double jet_scalefactor_up=1;
    double jet_scalefactor_do=1;


  for (int idx; idx<OUT::jet_n; idx++) {
      std::cout<< "pt  "<< OUT::jet_pt->at(idx)
               << "eta "<< OUT::jet_eta->at(idx)
               << "flav"<< OUT::jet_flav->at(idx)
               << "tag "<< OUT::jet_btagged->at(idx)
               <<std::endl; 

      if (abs(OUT::jet_flav->at(idx))==5) {
          jet_scalefactor    = reader->eval_auto_bounds(
              "central", BTagEntry::FLAV_B, 
              fabs(OUT::jet_eta->at(idx)), // absolute value of eta
              OUT::jet_pt->at(idx)
          ); 
          jet_scalefactor_up = reader->eval_auto_bounds(
              "up", BTagEntry::FLAV_B, 
              fabs(OUT::jet_eta->at(idx)), // absolute value of eta
              OUT::jet_pt->at(idx)
          );
          jet_scalefactor_do = reader->eval_auto_bounds(
              "down", BTagEntry::FLAV_B,
              fabs(OUT::jet_eta->at(idx)), 
              OUT::jet_pt->at(idx)
          );

          // get efficiency from histogram
          effval = GetVals2D( _effhist_jet_b, OUT::jet_pt->at(idx), fabs(OUT::jet_eta->at(idx)));
      }
      else if (abs(OUT::jet_flav->at(idx))==4) {
          jet_scalefactor    = reader->eval_auto_bounds(
              "central", BTagEntry::FLAV_C, 
              fabs(OUT::jet_eta->at(idx)), // absolute value of eta
              OUT::jet_pt->at(idx)
          ); 
          jet_scalefactor_up = reader->eval_auto_bounds(
              "up", BTagEntry::FLAV_C, 
              fabs(OUT::jet_eta->at(idx)), // absolute value of eta
              OUT::jet_pt->at(idx)
          );
          jet_scalefactor_do = reader->eval_auto_bounds(
              "down", BTagEntry::FLAV_C,
              fabs(OUT::jet_eta->at(idx)), 
              OUT::jet_pt->at(idx)
          );

          // get efficiency from histogram
          effval = GetVals2D( _effhist_jet_c, OUT::jet_pt->at(idx), fabs(OUT::jet_eta->at(idx)));
      }
      else if (abs(OUT::jet_flav->at(idx))==0) {
          jet_scalefactor    = reader->eval_auto_bounds(
              "central", BTagEntry::FLAV_UDSG, 
              fabs(OUT::jet_eta->at(idx)), // absolute value of eta
              OUT::jet_pt->at(idx)
          ); 
          jet_scalefactor_up = reader->eval_auto_bounds(
              "up", BTagEntry::FLAV_UDSG, 
              fabs(OUT::jet_eta->at(idx)), // absolute value of eta
              OUT::jet_pt->at(idx)
          );
          jet_scalefactor_do = reader->eval_auto_bounds(
              "down", BTagEntry::FLAV_UDSG,
              fabs(OUT::jet_eta->at(idx)), 
              OUT::jet_pt->at(idx)
          );

          // get efficiency from histogram
          effval = GetVals2D( _effhist_jet_l, OUT::jet_pt->at(idx), fabs(OUT::jet_eta->at(idx)));
      }

      // calculate event scale factor
      if (OUT::jet_btagged->at(idx)) {
          OUT::jet_btagSF   = OUT::jet_btagSF*jet_scalefactor;
          OUT::jet_btagSFUP = OUT::jet_btagSFDN*jet_scalefactor_up;
          OUT::jet_btagSFDN = OUT::jet_btagSFDN*jet_scalefactor_do;
          std::cout<< "accepted: "<< jet_scalefactor << " " <<OUT::jet_btagSF <<std::endl; 
      } else {
          // FIXME: uncertainty from SF and eff are independent
          OUT::jet_btagSF   = OUT::jet_btagSF*(1-effval.val * jet_scalefactor) / (1-effval.val);
          OUT::jet_btagSFUP = OUT::jet_btagSFUP*(1-(effval.val+effval.err_up) * jet_scalefactor_up) / (1- (effval.val+effval.err_up));
          OUT::jet_btagSFDN = OUT::jet_btagSFDN*(1-(effval.val-effval.err_dn) * jet_scalefactor_do) / (1- (effval.val-effval.err_dn));
          std::cout<< "rejected: "<< effval.val<< " "<<jet_scalefactor << " "<< (1-effval.val * jet_scalefactor) / (1-effval.val) <<" "<<OUT::jet_btagSF<<std::endl; 
      }


  }

#endif
}


void RunModule::AddPhotonSF(ModuleConfig & /*config*/) const {
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

    if (OUT::isData) {
        return;
    }
    // to check if photon pt is above histogram

    std::vector<float> sfs_id;
    std::vector<float> errs_id;
    std::vector<float> sfs_csev;
    std::vector<float> errs_csev;
    std::vector<float> sfs_psv;
    std::vector<float> errs_psv;
    for (int idx = 0; idx < OUT::ph_n; idx++) {
        // in the ID histogram, the x axis is signed eta, y is pt
        float pt = OUT::ph_pt->at(idx);
        float eta = OUT::ph_eta->at(idx);

        if (pt < 100 || fabs(eta) > 1.44) {
            ValWithErr res_id = GetVals2D(_sfhist_ph_id, eta, pt);
            sfs_id.push_back(res_id.val);
            errs_id.push_back(res_id.err_up);
        }
        else {
            // high-pt photon ID fit: https://indico.cern.ch/event/879936/#3-high-pt-photon-sfs-for-wgamm
            double const_fit, cov00, cov01, cov11;
            
            if (fabs(eta) < 0.8) {
                const_fit = _HiPtId_inner_const;
                cov00     = _HiPtId_inner_cov00;
                cov01     = _HiPtId_inner_cov01;
                cov11     = _HiPtId_inner_cov11;
            }
            else {
                const_fit = _HiPtId_outer_const;
                cov00     = _HiPtId_outer_cov00;
                cov01     = _HiPtId_outer_cov01;
                cov11     = _HiPtId_outer_cov11;
            }
            
            // central value from constant fit
            sfs_id.push_back(const_fit);
            
            // uncertainty from linear fit
            double dp0 = 1.;
            double dp1 = pt - 150.;
            double err2 = dp0*cov00*dp0 + 2*dp0*cov01*dp1 + dp1*cov11*dp1;
            errs_id.push_back(sqrt(err2));
        }

        if (_year_ph == 2016) {

            ValWithErr res_psv = GetVals2D(_sfhist_ph_psv, fabs(eta), pt);
            ValWithErr res_csev = GetVals2D(_sfhist_ph_csev, fabs(eta), pt);

            sfs_csev.push_back(res_csev.val);
            errs_csev.push_back(res_csev.err_up);

            sfs_psv.push_back(res_psv.val);
            errs_psv.push_back(res_psv.err_up);

        } else if (_year_ph == 2017) {

            ValWithErr res_psv = PhGetVals1D(_sfhist_ph_psv_2017);
            ValWithErr res_csev = PhGetVals1D(_sfhist_ph_csev_2017);

            sfs_csev.push_back(res_csev.val);
            errs_csev.push_back(res_csev.err_up);

            sfs_psv.push_back(res_psv.val);
            errs_psv.push_back(res_psv.err_up);

        } else if (_year_ph == 2018) {

            ValWithErr res_psv = GetVals2D(_sfhist_ph_psv_2018, pt, fabs(eta));
            ValWithErr err_psv = GetVals2D(_sfhist_ph_psv_2018_err, pt, fabs(eta));
            ValWithErr res_csev = GetVals2D(_sfhist_ph_csev_2018, pt, fabs(eta));
            ValWithErr err_csev = GetVals2D(_sfhist_ph_csev_2018_err, pt, fabs(eta));

            sfs_csev.push_back(res_csev.val);
            errs_csev.push_back(err_csev.val);

            sfs_psv.push_back(res_psv.val);
            errs_psv.push_back(err_psv.val);
        } else
            std::cout << "ERROR AddPhotonSF: year not recognized!" << std::endl;
    }

    if (sfs_id.size() == 1) {
        OUT::ph_idSF = sfs_id[0];
        OUT::ph_idSFUP = sfs_id[0] + errs_id[0];
        OUT::ph_idSFDN = sfs_id[0] - errs_id[0];

        OUT::ph_psvSF = sfs_psv[0];
        OUT::ph_psvSFUP = sfs_psv[0] + errs_psv[0];
        OUT::ph_psvSFDN = sfs_psv[0] - errs_psv[0];

        // Also do CSEV
        OUT::ph_csevSF = sfs_csev[0];
        OUT::ph_csevSFUP = sfs_csev[0] + errs_csev[0];
        OUT::ph_csevSFDN = sfs_csev[0] - errs_csev[0];
    } else if (sfs_id.size() > 1) {
        OUT::ph_idSF = sfs_id[0] * sfs_id[1];
        OUT::ph_idSFUP = (sfs_id[0] + errs_id[0]) * (sfs_id[1] + errs_id[1]);
        OUT::ph_idSFDN = (sfs_id[0] - errs_id[0]) * (sfs_id[1] - errs_id[1]);

        OUT::ph_psvSF = sfs_psv[0] * sfs_psv[1];
        OUT::ph_psvSFUP = (sfs_psv[0] + errs_psv[0]) * (sfs_psv[1] + errs_psv[1]);
        OUT::ph_psvSFDN = (sfs_psv[0] - errs_psv[0]) * (sfs_psv[1] - errs_psv[1]);

        OUT::ph_csevSF = sfs_csev[0] * sfs_csev[1];
        OUT::ph_csevSFUP =
            (sfs_csev[0] + errs_csev[0]) * (sfs_csev[1] + errs_csev[1]);
        OUT::ph_csevSFDN =
            (sfs_csev[0] - errs_csev[0]) * (sfs_csev[1] - errs_csev[1]);
    }

#endif
}

void RunModule::AddMuonSF(ModuleConfig & /*config*/) const {
#ifdef MODULE_AddMuonSF

    OUT::mu_idSF = 1.0;
    OUT::mu_idSFUP = 1.0;
    OUT::mu_idSFDN = 1.0;

    OUT::mu_isoSF = 1.0;
    OUT::mu_isoSFUP = 1.0;
    OUT::mu_isoSFDN = 1.0;

    OUT::mu_trigSF = 1.0;
    OUT::mu_trigSFUP = 1.0;
    OUT::mu_trigSFDN = 1.0;

    OUT::mu_trkSF = 1.0;
    OUT::mu_trkSFUP = 1.0;
    OUT::mu_trkSFDN = 1.0;

    if (OUT::isData) {
        return;
    }

    std::vector<float> trsfs;
    std::vector<float> trerrs;
    std::vector<float> treffs_data;
    std::vector<float> trerrs_data;
    std::vector<float> treffs_mc;
    std::vector<float> trerrs_mc;

    std::vector<float> idsfs;
    std::vector<float> iderrsup;
    std::vector<float> iderrsdn;

    std::vector<float> isosfs;
    std::vector<float> isoerrsup;
    std::vector<float> isoerrsdn;

    for (int idx = 0; idx < OUT::mu_n; ++idx) {
        float feta = fabs(OUT::mu_eta->at(idx));
        float pt = OUT::mu_pt_rc->at(idx);

        float ptcut = -999.;
        if (_year_mu == 2016)
            ptcut = 26.;
        else if (_year_mu == 2017)
            ptcut = 29.;
        else if (_year_mu == 2018)
            ptcut = 26.;
        else
            std::cout << "ERROR AddMuonSF: year not recognized!" << std::endl;

        if (!(pt > ptcut && feta < 2.4)) {
            std::cout << "AddMuonSF -- WARNING : muon pt or eta out of range " << pt
                      << " " << feta << std::endl;
        }

        ValWithErr entry;
        ValWithErr entry_data;
        ValWithErr entry_mc;
        entry = GetValsRunRange2D(_sfhists_mu_trig, pt, feta);
        entry_data = GetValsRunRange2D(_effhists_mu_trig_data, pt, feta);
        entry_mc = GetValsRunRange2D(_effhists_mu_trig_mc, pt, feta);

        trsfs.push_back(entry.val);
        trerrs.push_back(entry.err_up);
        treffs_data.push_back(entry_data.val);
        trerrs_data.push_back(entry_data.err_up);
        treffs_mc.push_back(entry_mc.val);
        trerrs_mc.push_back(entry_mc.err_up);
    }

    if (OUT::mu_n == 1) {
        OUT::mu_trigSF = trsfs[0];
        OUT::mu_trigSFUP = trsfs[0] + trerrs[0];
        OUT::mu_trigSFDN = trsfs[0] - trerrs[0];
    } else if (OUT::mu_n > 1) {
        double eff_data = 1 - (1 - treffs_data[0]) * (1 - treffs_data[1]);
        double eff_mc = 1 - (1 - treffs_mc[0]) * (1 - treffs_mc[1]);

        double err_data = sqrt(pow(trerrs_data[0] / treffs_data[0], 2) +
                               pow(trerrs_data[1] / treffs_data[1], 2));
        double err_mc = sqrt(pow(trerrs_mc[0] / treffs_mc[0], 2) +
                             pow(trerrs_mc[1] / treffs_mc[1], 2));

        double sf_val = eff_data / eff_mc;
        double sf_err = sqrt(pow(err_data / eff_data, 2) + pow(err_mc / eff_mc, 2));

        OUT::mu_trigSF = sf_val;
        OUT::mu_trigSFUP = sf_val + sf_err;
        OUT::mu_trigSFDN = sf_val - sf_err;
    }

    for (int idx = 0; idx < OUT::mu_n; ++idx) {
        float eta = OUT::mu_eta->at(idx);
        float pt = OUT::mu_pt_rc->at(idx);
        //float phi = OUT::mu_phi->at(idx);
        //float Q = OUT::mu_charge->at(idx);
        float feta = fabs(eta);

        ValWithErr entry_id;
        ValWithErr entry_iso;
        if (_year_mu == 2016) {  // 2016
            entry_id = GetValsRunRange2D(_sfhists_mu_id, eta, pt);
            entry_iso = GetValsRunRange2D(_sfhists_mu_iso, eta, pt);
        }                             // 2016
        else if (_year_mu == 2017) {  // 2017
            entry_id = GetValsRunRange2D(_sfhists_mu_id, pt, feta);
            entry_iso = GetValsRunRange2D(_sfhists_mu_iso, pt, feta);
        }                             // 2017
        else if (_year_mu == 2018) {  // 2018
            entry_id = GetValsRunRange2D(_sfhists_mu_id, pt, feta);
            entry_iso = GetValsRunRange2D(_sfhists_mu_iso, pt, feta);
        }  // 2018
        else
            std::cout << "Error AddMuonSF: year not recognized!" << std::endl;

        idsfs.push_back(entry_id.val);
        iderrsup.push_back(entry_id.err_up);
        iderrsdn.push_back(entry_id.err_dn);

        isosfs.push_back(entry_iso.val);
        isoerrsup.push_back(entry_iso.err_up);
        isoerrsdn.push_back(entry_iso.err_dn);

        // Tracking sf's are not needed anymore!
        // trksfs.push_back( entry_trk.val);
        // trkerrsup.push_back( entry_trk.err_up );
        // trkerrsdn.push_back( entry_trk.err_dn );

        // tracking scale factor is 1.0
        // https://hypernews.cern.ch/HyperNews/CMS/get/muon/1425.html
    }

    if (OUT::mu_n == 1) {
        OUT::mu_idSF = idsfs[0];
        OUT::mu_idSFUP = idsfs[0] + iderrsup[0];
        OUT::mu_idSFDN = idsfs[0] - iderrsdn[0];

        OUT::mu_isoSF = isosfs[0];
        OUT::mu_isoSFUP = isosfs[0] + isoerrsup[0];
        OUT::mu_isoSFDN = isosfs[0] - isoerrsdn[0];
    } else if (OUT::mu_n > 1) {
        OUT::mu_idSF = idsfs[0] * idsfs[1];
        OUT::mu_idSFUP = (idsfs[0] + iderrsup[0]) * (idsfs[1] + iderrsup[1]);
        OUT::mu_idSFDN = (idsfs[0] - iderrsdn[0]) * (idsfs[1] - iderrsdn[1]);

        OUT::mu_isoSF = isosfs[0] * isosfs[1];
        OUT::mu_isoSFUP = (isosfs[0] + isoerrsup[0]) * (isosfs[1] + isoerrsup[1]);
        OUT::mu_isoSFDN = (isosfs[0] - isoerrsdn[0]) * (isosfs[1] - isoerrsdn[1]);
    }

#endif
}

template <class HIST>
ValWithErr RunModule::PhGetVals1D(const HIST *hist) const {
    ValWithErr result;
    //int nbinsX = hist->GetNbinsX();

    // Assumes only EB photons!
    result.val = hist->GetBinContent(1);
    result.err_up = hist->GetBinError(1);
    result.err_dn = result.err_up;

    return result;
}

template <class HIST>
ValWithErr RunModule::GetVals2D(const HIST *hist, float xvar,
                                float yvar) const {
    ValWithErr result;

    int nbinsX = hist->GetNbinsX();
    int nbinsY = hist->GetNbinsY();

    float min_x = hist->GetXaxis()->GetBinLowEdge(1);
    float max_x = hist->GetXaxis()->GetBinUpEdge(nbinsX);

    float min_y = hist->GetYaxis()->GetBinLowEdge(1);
    float max_y = hist->GetYaxis()->GetBinUpEdge(nbinsY);

    int bin_x = hist->GetXaxis()->FindBin(xvar);
    int bin_y = hist->GetYaxis()->FindBin(yvar);

    if (xvar < min_x) {
        std::cout << "GetVals -- WARNING : Particle xvar of " << xvar
                  << " exceeds minimum histogram value of " << min_x << std::endl;
        bin_x = 1;
    }
    if (xvar > max_x) {
        if (max_x < 100)
            std::cout << "GetVals -- WARNING : Particle xvar of " << xvar
                      << " exceeds maximum histogram value of " << max_x << std::endl;
        bin_x = nbinsX;
    }
    if (yvar < min_y) {
        std::cout << "GetVals -- WARNING : Particle yvar of " << yvar
                  << " exceeds minimum histogram value of " << min_y << std::endl;
        bin_y = 1;
    }
    if (yvar > max_y) {
        if (max_y < 100)
            std::cout << "GetVals -- WARNING : Particle yvar of " << yvar
                      << " exceeds maximum histogram value of " << max_y << std::endl;
        bin_y = nbinsY;
    }

    result.val = hist->GetBinContent(bin_x, bin_y);
    result.err_up = hist->GetBinError(bin_x, bin_y);
    result.err_dn = result.err_up;

    return result;
}

template <class HIST>
ValWithErr RunModule::GetValsRunRange2D(
    const std::vector<std::pair<float, HIST *>> range_hists, float xvar,
    float yvar) const {
    ValWithErr result;

    float total_lumi = 0;
    float sum_cv = 0;
    float sum_err = 0;
    // for( std::vector<std::pair<float, TH2D*> >::const_iterator itr =
    // range_hists.begin();
    //
    for (auto itr = range_hists.begin(); itr != range_hists.end(); ++itr) {
        if (!itr->second) {
            std::cout << "GetValsRunRange2D -- ERROR : hist does not exist "
                      << std::endl;
        }

        ValWithErr thisres = GetVals2D(itr->second, xvar, yvar);

        float this_lumi = itr->first;

        total_lumi += this_lumi;

        sum_cv += this_lumi * thisres.val;
        sum_err += this_lumi * thisres.err_up;
    }

    result.val = sum_cv / total_lumi;
    result.err_up = sum_err / total_lumi;
    result.err_dn = result.err_up;

    return result;
}

ValWithErr RunModule::GetValsFromGraph(const TGraphAsymmErrors *graph, float pt,
                                       bool debug) const {
    ValWithErr result;

    for (int point = 0; point < graph->GetN(); ++point) {
        double x;
        double y;

        graph->GetPoint(point, x, y);
        float xerrmin = graph->GetErrorXlow(point);
        float xerrmax = graph->GetErrorXhigh(point);

        float xmin = x - xerrmin;
        float xmax = x + xerrmax;

        if (pt >= xmin && pt < xmax) {
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

    int last_point = graph->GetN() - 1;
    graph->GetPoint(last_point, x, y);
    float xerrmax = graph->GetErrorXhigh(last_point);

    if (pt > (x + xerrmax)) {
        result.val = y;
        result.err_up = graph->GetErrorYhigh(last_point);
        result.err_dn = graph->GetErrorYlow(last_point);

        return result;
    }

    if (debug) {
        std::cout << "No entries for pt " << pt << " in graph " << graph->GetName()
                  << std::endl;
    }

    result.val = -1;

    return result;
}
