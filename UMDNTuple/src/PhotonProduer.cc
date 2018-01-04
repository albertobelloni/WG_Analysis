#include "UMDNTuple/UMDNTuple/interface/PhotonProducer.h"
#include "FWCore/Framework/interface/EDConsumerBase.h"
#include "FWCore/Framework/interface/Event.h"

PhotonProducer::PhotonProducer(  ) : 
    ph_n(0),
    ph_pt(0),
    ph_eta(0),
    ph_phi(0),
    ph_e(0),
    ph_ptOrig(0),
    ph_etaOrig(0),
    ph_phiOrig(0),
    ph_eOrig(0),
    ph_passVIDLoose(0),
    ph_passVIDMedium(0),
    ph_passVIDTight(0),
    ph_chIso(0),
    ph_neuIso(0),
    ph_phoIso(0),
    ph_sc_eta(0),
    ph_sc_phi(0),
    ph_hOverE(0),
    ph_sigmaIEIE(0),
    ph_sigmaIEIEFull5x5(0),
    ph_r9(0),
    ph_r9Full5x5(0),
    ph_etaWidth(0),
    ph_phiWidth(0),
    ph_passEleVeto(0),
    ph_hasPixSeed(0),
    ph_sc_rawE(0),
    ph_ecalIso(0),
    ph_hcalIso(0),
    ph_trkIso(0),
    ph_pfIsoPUChHad(0),
    ph_pfIsoEcal(0),
    ph_pfIsoHcal(0),
    ph_E3x3(0),
    ph_E1x5(0),
    ph_E2x5(0),
    ph_E5x5(0),
    //ph_sigmaIetaIphi(0),
    //ph_sigmaIphiIphi(0),
    ph_E1x5Full5x5(0),
    ph_E2x5Full5x5(0),
    ph_E3x3Full5x5(0),
    ph_E5x5Full5x5(0),
    _detail(0),
    _tree(0)
{

}

void PhotonProducer::initialize( const std::string &prefix,
                                 const edm::EDGetTokenT<edm::View<pat::Photon> >&photTok,
                                 TTree *tree, float minPt, int detail) {

    _prefix = prefix;
    _photToken = photTok;
    _detail = detail;
    _tree = tree;
    _minPt = minPt;

    tree->Branch( (prefix + "_n" ).c_str(), &ph_n,(prefix + "_n/I" ).c_str()  );

    tree->Branch( (prefix + "_pt" ).c_str(), &ph_pt );
    tree->Branch( (prefix + "_eta").c_str(), &ph_eta );
    tree->Branch( (prefix + "_phi").c_str(), &ph_phi );
    tree->Branch( (prefix + "_e"  ).c_str(), &ph_e );
    tree->Branch( (prefix + "_ptOrig" ).c_str(), &ph_ptOrig );
    tree->Branch( (prefix + "_etaOrig").c_str(), &ph_etaOrig );
    tree->Branch( (prefix + "_phiOrig").c_str(), &ph_phiOrig );
    tree->Branch( (prefix + "_eOrig"  ).c_str(), &ph_eOrig );

    if( detail > 0 ) {

        tree->Branch( (prefix + "_passVIDLoose").c_str(), &ph_passVIDLoose );
        tree->Branch( (prefix + "_passVIDMedium").c_str(), &ph_passVIDMedium );
        tree->Branch( (prefix + "_passVIDTight").c_str(), &ph_passVIDTight );

        tree->Branch( (prefix + "_chIso").c_str(), &ph_chIso );
        tree->Branch( (prefix + "_neuIso").c_str(), &ph_neuIso );
        tree->Branch( (prefix + "_phoIso").c_str(), &ph_phoIso );

        tree->Branch( (prefix + "_sc_eta").c_str(), &ph_sc_eta );
        tree->Branch( (prefix + "_sc_phi").c_str(), &ph_sc_phi );

        tree->Branch( (prefix + "_hOverE").c_str(), &ph_hOverE );
        tree->Branch( (prefix + "_sigmaIEIE").c_str(), &ph_sigmaIEIE );
        tree->Branch( (prefix + "_sigmaIEIEFull5x5").c_str(), &ph_sigmaIEIEFull5x5 );
        tree->Branch( (prefix + "_r9").c_str(), &ph_r9 );
        tree->Branch( (prefix + "_r9Full5x5").c_str(), &ph_r9Full5x5 );
        tree->Branch( (prefix + "_etaWidth").c_str(), &ph_etaWidth );
        tree->Branch( (prefix + "_phiWidth").c_str(), &ph_phiWidth );

        tree->Branch( (prefix + "_passEleVeto").c_str(), &ph_passEleVeto  );
        tree->Branch( (prefix + "_hasPixSeed").c_str(), &ph_hasPixSeed  );

        if( detail > 1 ) {

            tree->Branch( (prefix + "_sc_rawE").c_str(), &ph_sc_rawE );

            tree->Branch( (prefix + "_ecalIso").c_str(), &ph_ecalIso );
            tree->Branch( (prefix + "_hcalIso").c_str(), &ph_hcalIso );
            tree->Branch( (prefix + "_trkIso").c_str(), &ph_trkIso );
            tree->Branch( (prefix + "_pfIsoPUChHad").c_str(), &ph_pfIsoPUChHad );
            tree->Branch( (prefix + "_pfIsoEcal").c_str(), &ph_pfIsoEcal );
            tree->Branch( (prefix + "_pfIsoHcal").c_str(), &ph_pfIsoHcal );
            tree->Branch( (prefix + "_E3x3").c_str(), &ph_E3x3 );
            tree->Branch( (prefix + "_E1x5").c_str(), &ph_E1x5 );
            tree->Branch( (prefix + "_E2x5").c_str(), &ph_E2x5 );
            tree->Branch( (prefix + "_E5x5").c_str(), &ph_E5x5 );
            //tree->Branch( (prefix + "_sigmaIetaIphi").c_str(), &ph_sigmaIetaIphi );
            //tree->Branch( (prefix + "_sigmaIphiIphi").c_str(), &ph_sigmaIphiIphi );

            tree->Branch( (prefix + "_E1x5Full5x5").c_str(), &ph_E1x5Full5x5 );
            tree->Branch( (prefix + "_E2x5Full5x5").c_str(), &ph_E2x5Full5x5 );
            tree->Branch( (prefix + "_E3x3Full5x5").c_str(), &ph_E3x3Full5x5 );
            tree->Branch( (prefix + "_E5x5Full5x5").c_str(), &ph_E5x5Full5x5 );
        }
    }

}

//void PhotonProducer::addUserFloat( const std::string &name, const edm::EDGetTokenT<edm::ValueMap<float> > &userFloat ) {
//
//    if( !_tree ) {
//        std::cout << "PhotonProducer::addUserFloats -- ERROR : Must call initialize before adding user floats" << std::endl;
//        return;
//    }
//
//    //_tokens_float.push_back( userFloat );
//    _tokens_float[name] = userFloat;
//
//    //ph_user_floats.push_back(0);
//    ph_user_floats[name] = 0;
//
//    //_tree->Branch( (_prefix + "_" + name).c_str(), &(ph_user_floats.back()) );
//    _tree->Branch( (_prefix + "_" + name).c_str(), &(ph_user_floats[name]) );
//
//}
//
//void PhotonProducer::addUserBool( const std::string &name, const edm::EDGetTokenT<edm::ValueMap<Bool_t> > &userBool ) {
//
//    if( !_tree ) {
//        std::cout << "PhotonProducer::addUserBool -- ERROR : Must call initialize before adding user bools" << std::endl;
//        return;
//    }
//
//    //_tokens_bool.push_back( userBool );
//    _tokens_bool[name] =  userBool;
//
//    //ph_user_bools.push_back(0);
//    ph_user_bools[name] = 0;
//
//    //_tree->Branch( (_prefix + "_" + name).c_str(), &(ph_user_bools.back()) );
//    _tree->Branch( (_prefix + "_" + name).c_str(), &(ph_user_bools[name]) );
//
//}

void PhotonProducer::addUserBool( PhotonUserVar type, const edm::EDGetTokenT<edm::ValueMap<Bool_t> > &userBool ) {

    if( type == PhotonVIDLoose ) {
        _VIDLooseToken = userBool;
    }
    if( type == PhotonVIDMedium ) {
        _VIDMediumToken = userBool;
    }
    if( type == PhotonVIDTight ) {
        _VIDTightToken = userBool;
    }

}
        
void PhotonProducer::addUserFloat( PhotonUserVar type, const edm::EDGetTokenT<edm::ValueMap<float> > &userFloat) {

    if( type == PhotonChIso) {
        _ChIsoToken = userFloat;
    }
    if( type == PhotonNeuIso ) {
        _NeuIsoToken = userFloat;
    }
    if( type == PhotonPhoIso) {
        _PhoIsoToken = userFloat;
    }

}
        
void PhotonProducer::addConversionsToken( const edm::EDGetTokenT<reco::ConversionCollection> & tok) {
    _ConversionsToken = tok;
}
void PhotonProducer::addBeamSpotToken( const edm::EDGetTokenT<reco::BeamSpot> & tok) {
    _beamSpotToken= tok;
}
void PhotonProducer::addElectronsToken( const edm::EDGetTokenT<edm::View<pat::Electron> > & tok) {
    _ElectronsToken = tok;
}
void PhotonProducer::addCalibratedToken( const edm::EDGetTokenT<edm::View<pat::Photon> > & tok) {
    _photCalibToken = tok;
}

void PhotonProducer::produce(const edm::Event &iEvent ) {

    ph_n=0;
    ph_pt->clear();
    ph_eta->clear();
    ph_phi->clear();
    ph_e->clear();
    ph_ptOrig->clear();
    ph_etaOrig->clear();
    ph_phiOrig->clear();
    ph_eOrig->clear();

    if( _detail > 0 ) {

        ph_passVIDLoose->clear();
        ph_passVIDMedium->clear();
        ph_passVIDTight->clear();

        ph_chIso->clear();
        ph_neuIso->clear();
        ph_phoIso->clear();

        ph_sc_eta ->clear();
        ph_sc_phi ->clear();

        ph_hOverE->clear();
        ph_sigmaIEIE->clear();
        ph_sigmaIEIEFull5x5->clear();
        ph_r9->clear();
        ph_r9Full5x5->clear();
        ph_etaWidth->clear();
        ph_phiWidth->clear();

        ph_passEleVeto ->clear();
        ph_hasPixSeed ->clear();

        if( _detail > 1 ) {
            ph_sc_rawE->clear();

            ph_ecalIso->clear();
            ph_hcalIso->clear();
            ph_trkIso->clear();
            ph_pfIsoPUChHad->clear();
            ph_pfIsoEcal->clear();
            ph_pfIsoHcal->clear();
            ph_E3x3->clear();
            ph_E1x5->clear();
            ph_E2x5->clear();
            ph_E5x5->clear();
            //ph_sigmaIetaIphi->clear();
            //ph_sigmaIphiIphi->clear();

            ph_E1x5Full5x5->clear();
            ph_E2x5Full5x5->clear();
            ph_E3x3Full5x5->clear();
            ph_E5x5Full5x5->clear();
        }
    }

    edm::Handle<edm::View<pat::Photon> > photons;
    iEvent.getByToken(_photToken,photons);

    edm::Handle<edm::View<pat::Photon> > calibPhotons;
    iEvent.getByToken(_photCalibToken,calibPhotons);

    edm::Handle<edm::ValueMap<Bool_t> > ph_passVIDLoose_h;
    edm::Handle<edm::ValueMap<Bool_t> > ph_passVIDMedium_h;
    edm::Handle<edm::ValueMap<Bool_t> > ph_passVIDTight_h;

    iEvent.getByToken( _VIDLooseToken , ph_passVIDLoose_h );
    iEvent.getByToken( _VIDMediumToken, ph_passVIDMedium_h );
    iEvent.getByToken( _VIDTightToken , ph_passVIDTight_h );

    edm::Handle<edm::ValueMap<float> > ph_chIso_h;
    edm::Handle<edm::ValueMap<float> > ph_neuIso_h;
    edm::Handle<edm::ValueMap<float> > ph_phoIso_h;

    iEvent.getByToken( _ChIsoToken  , ph_chIso_h );
    iEvent.getByToken( _NeuIsoToken , ph_neuIso_h );
    iEvent.getByToken( _PhoIsoToken , ph_phoIso_h );

    edm::Handle<edm::View<pat::Electron> > electrons_h;
    iEvent.getByToken(_ElectronsToken, electrons_h);

    edm::Handle<reco::ConversionCollection> conversions_h;
    iEvent.getByToken(_ConversionsToken, conversions_h);

    edm::Handle<reco::BeamSpot> beamSpot_h;
    iEvent.getByToken(_beamSpotToken, beamSpot_h);

    // needed for a few shower shape variables
    // do not use for now
    //EcalClusterLazyTools lazyTool(iEvent, iSetup, ecalHitEBToken_, ecalHitEEToken_, ecalHitESToken_ );

    for (unsigned int j=0; j < photons->size();++j){
        edm::Ptr<pat::Photon> ph = photons->ptrAt(j);
        edm::Ptr<pat::Photon> calibPh = calibPhotons->ptrAt(j);
        // Need to implemnet calibrations
        //edm::Ptr<pat::Photon> calib_phptr = calibrated_photons->ptrAt(j);
 
        if( ph->pt() < _minPt ) continue;
        // should be added with calibration
        //if( isnan(calib_phptr->pt() ) ) continue;

        ph_n += 1;

        ph_pt      -> push_back( calibPh->pt() );
        ph_eta     -> push_back( calibPh->eta() );
        ph_phi     -> push_back( calibPh->phi() );
        ph_e       -> push_back( calibPh->energy() );
        ph_ptOrig  -> push_back( ph->pt() );
        ph_etaOrig -> push_back( ph->eta() );
        ph_phiOrig -> push_back( ph->phi() );
        ph_eOrig   -> push_back( ph->energy() );

        if( _detail > 0 ) {

            ph_passVIDLoose -> push_back( (*ph_passVIDLoose_h)[ph] );
            ph_passVIDMedium -> push_back( (*ph_passVIDMedium_h)[ph] );
            ph_passVIDTight -> push_back( (*ph_passVIDTight_h)[ph] );

            ph_chIso -> push_back( (*ph_chIso_h)[ph] );
            ph_neuIso -> push_back( (*ph_neuIso_h)[ph] );
            ph_phoIso -> push_back( (*ph_phoIso_h)[ph] );

            ph_sc_eta ->push_back(ph->superCluster()->eta());
            ph_sc_phi ->push_back(ph->superCluster()->phi());

            ph_hOverE->push_back(ph->hadTowOverEm());
            ph_sigmaIEIE->push_back(ph->sigmaIetaIeta());
            ph_sigmaIEIEFull5x5->push_back(ph->full5x5_sigmaIetaIeta());
            ph_r9->push_back(ph->r9());
            ph_r9Full5x5->push_back(ph->full5x5_r9());   
            ph_etaWidth->push_back(ph->superCluster()->etaWidth());
            ph_phiWidth->push_back(ph->superCluster()->phiWidth());

            ph_passEleVeto -> push_back (ph->passElectronVeto());
            ph_hasPixSeed -> push_back( ph->hasPixelSeed());

            if( _detail > 1 ) {

                ph_sc_rawE->push_back(ph->superCluster()->rawEnergy());

                ph_ecalIso->push_back(ph->ecalIso());
                ph_hcalIso->push_back(ph->hcalIso());
                ph_trkIso->push_back(ph->trackIso());
                ph_pfIsoPUChHad->push_back(ph->puChargedHadronIso());
                ph_pfIsoEcal->push_back(ph->ecalPFClusterIso());
                ph_pfIsoHcal->push_back(ph->hcalPFClusterIso());

                // requires implementation fo lazy tools
                //const reco::CaloClusterPtr  seed_clu = photon.superCluster()->seed();
                //ph_E1x3->push_back( lazyTool.e1x3( *seed_clu ) );
                //ph_E2x2->push_back( lazyTool.e2x2( *seed_clu ) );
                //ph_S4->push_back( lazyTool.e2x2( *seed_clu ) / lazyTool.e5x5( *seed_clu ) );
                ////photon cluster shape
                ph_E3x3->push_back(ph->e3x3());
                ph_E1x5->push_back(ph->e1x5());
                ph_E2x5->push_back(ph->e2x5());
                ph_E5x5->push_back(ph->e5x5());
                //ph_sigmaIetaIphi->push_back(ph->sigmaIetaIphi());
                //ph_sigmaIphiIphi->push_back(ph->sigmaIphiIphi());

                ph_E1x5Full5x5->push_back(ph->full5x5_e1x5());    
                ph_E2x5Full5x5->push_back(ph->full5x5_e2x5());
                ph_E3x3Full5x5->push_back(ph->full5x5_e3x3());
                ph_E5x5Full5x5->push_back(ph->full5x5_e5x5());
            }
        }
    }
}
    //for( std::map< std::string, edm::EDGetTokenT<edm::ValueMap<Bool_t> > >::const_iterator itr = _tokens_bool.begin(); itr != _tokens_bool.end(); ++itr ) {

    //    ph_user_bools[itr->first]->clear();

    //    edm::Handle<edm::ValueMap<Bool_t> > bool_val;

    //    iEvent.getByToken( itr->second, bool_val );

    //    for (unsigned int j=0; j < photons->size();++j){
    //        edm::Ptr<pat::Photon> ph = photons->ptrAt(j);

    //        ph_user_bools[itr->first]->push_back( (*bool_val)[ph] );

    //    }
    //}

    //for( std::map< std::string, edm::EDGetTokenT<edm::ValueMap<float> > >::const_iterator itr = _tokens_float.begin(); itr != _tokens_float.end(); ++itr ) {

    //    edm::Handle<edm::ValueMap<Float_t> > float_val;

    //    iEvent.getByToken( itr->second, float_val );

    //    for (unsigned int j=0; j < photons->size();++j){
    //        edm::Ptr<pat::Photon> ph = photons->ptrAt(j);

    //        ph_user_floats[itr->first]->push_back( (*float_val)[ph] );

    //    }
    //}



