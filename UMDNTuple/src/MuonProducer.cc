#include "UMDNTuple/UMDNTuple/interface/MuonProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

MuonProducer::MuonProducer(  ) : 
    mu_n(0),
    mu_pt(0),
    mu_eta(0),
    mu_phi(0),
    mu_e(0),
    mu_isGlobal(0),
    mu_isTracker(0),
    mu_isPf(0),
    mu_pfIso(0),
    mu_trkIso(0),
    mu_dz(0),
    mu_charge(0),
    mu_d0(0),
    mu_chi2(0),
    mu_nHits(0),
    mu_nMuStations(0),
    mu_nPixHits(0),
    mu_nTrkLayers(0),
    mu_vtx_z(0),
    mu_rhoIso(0),
    mu_chHadIso(0),
    mu_neuHadIso(0),
    mu_ecalIso(0),
    mu_hcalIso(0),
    mu_sumPtIso(0),
    mu_besttrk_pt(0),
    mu_besttrk_pterr(0),
    _detail(99)
{

}

void MuonProducer::initialize( const std::string &prefix,
                               const edm::EDGetTokenT<edm::View<pat::Muon> >&muonTok,
                               TTree *tree, float minPt, int detail) {

    _prefix = prefix;
    _muonToken = muonTok;
    _detail = detail;
    _minPt = minPt;

    tree->Branch( (prefix + "_n" ).c_str() , &mu_n,(prefix + "_n/I" ).c_str()  );
    tree->Branch( (prefix + "_pt" ).c_str()           , &mu_pt );
    tree->Branch( (prefix + "_eta").c_str()           , &mu_eta );
    tree->Branch( (prefix + "_phi").c_str()           , &mu_phi );
    tree->Branch( (prefix + "_e"  ).c_str()           , &mu_e );
    tree->Branch( (prefix + "_isGlobal").c_str()      , &mu_isGlobal );
    tree->Branch( (prefix + "_isTracker").c_str()     , &mu_isTracker );
    tree->Branch( (prefix + "_isPf").c_str()          , &mu_isPf );
    if( detail > 0 ) {
        tree->Branch( (prefix + "_pfIso").c_str()         , &mu_pfIso );
        tree->Branch( (prefix + "_trkIso").c_str()        , &mu_trkIso );
        tree->Branch( (prefix + "_dz").c_str()            , &mu_dz );
        tree->Branch( (prefix + "_charge").c_str()        , &mu_charge );
        tree->Branch( (prefix + "_d0").c_str()            , &mu_d0 );
        tree->Branch( (prefix + "_chi2").c_str()          , &mu_chi2 );
        tree->Branch( (prefix + "_nHits").c_str()         , &mu_nHits );
        tree->Branch( (prefix + "_nMuStations").c_str()   , &mu_nMuStations );
        tree->Branch( (prefix + "_nPixHits").c_str()      , &mu_nPixHits );
        tree->Branch( (prefix + "_nTrkLayers").c_str()    , &mu_nTrkLayers );
        if( detail > 1 ) { 
            tree->Branch( (prefix + "_vtx_z").c_str()         , &mu_vtx_z );
            tree->Branch( (prefix + "_rhoIso").c_str()        , &mu_rhoIso );
            tree->Branch( (prefix + "_chHadIso").c_str()      , &mu_chHadIso );
            tree->Branch( (prefix + "_neuHadIso").c_str()     , &mu_neuHadIso );
            tree->Branch( (prefix + "_ecalIso").c_str()       , &mu_ecalIso );
            tree->Branch( (prefix + "_hcalIso").c_str()       , &mu_hcalIso );
            tree->Branch( (prefix + "_sumPtIso").c_str()      , &mu_sumPtIso );
            tree->Branch( (prefix + "_besttrk_pt").c_str()    , &mu_besttrk_pt );
            tree->Branch( (prefix + "_besttrk_pterr").c_str() , &mu_besttrk_pterr );
        }
    }

}

void MuonProducer::addVertexToken( const edm::EDGetTokenT<std::vector<reco::Vertex> > & tok) {
    _vertexToken = tok;
}

void MuonProducer::addRhoToken( const edm::EDGetTokenT<double> & tok) {
    _rhoToken = tok;
}
        
void MuonProducer::produce(const edm::Event &iEvent ) {

    mu_n = 0;
    mu_pt            -> clear();
    mu_eta           -> clear();
    mu_phi           -> clear();
    mu_e             -> clear();
    mu_isGlobal      -> clear();
    mu_isTracker     -> clear();
    mu_isPf          -> clear();
    if( _detail > 0 ) {
        mu_pfIso         -> clear();
        mu_trkIso        -> clear();
        mu_dz            -> clear();
        mu_charge        -> clear();
        mu_d0            -> clear();
        mu_chi2          -> clear();
        mu_nHits         -> clear();
        mu_nMuStations   -> clear();
        mu_nPixHits      -> clear();
        mu_nTrkLayers    -> clear();

        if( _detail > 1 ) {
            mu_vtx_z         -> clear();
            mu_rhoIso        -> clear();
            mu_chHadIso      -> clear();
            mu_neuHadIso     -> clear();
            mu_ecalIso       -> clear();
            mu_hcalIso       -> clear();
            mu_sumPtIso      -> clear();
            mu_besttrk_pt    -> clear();
            mu_besttrk_pterr -> clear();
        }
    }


    iEvent.getByToken(_muonToken,muons);

    edm::Handle<std::vector<reco::Vertex> > vertices_h;
    iEvent.getByToken( _vertexToken, vertices_h );

    edm::Handle<double> rho_h;
    iEvent.getByToken( _rhoToken, rho_h );


    for (unsigned int j=0; j < muons->size();++j){
        edm::Ptr<pat::Muon> mu = muons->ptrAt(j);
 
        if( mu->pt() < _minPt ) continue;

        mu_n += 1;

        mu_pt -> push_back( mu->pt() );
        mu_eta -> push_back( mu->eta() );
        mu_phi -> push_back( mu->phi() );
        mu_e -> push_back( mu->energy() );

        bool isTracker =mu->isTrackerMuon();
        bool isGlobal =mu->isGlobalMuon();
        bool isPf = mu->isPFMuon();
        mu_isGlobal -> push_back( isGlobal );
        mu_isTracker -> push_back( isTracker );
        mu_isPf -> push_back( isPf );

        if( _detail > 0 ) {
            // pf Isolation variables
            double chHadIso   = mu->pfIsolationR04().sumChargedHadronPt;
            double chHadIsoPU = mu->pfIsolationR04().sumPUPt;
            double neuHadIso   = mu->pfIsolationR04().sumNeutralHadronEt;
            double phoIso          = mu->pfIsolationR04().sumPhotonEt;
            // OPTION 1: DeltaBeta corrections for iosolation
            float pfisodb = (chHadIso + std::max(phoIso+neuHadIso - 0.5*chHadIsoPU,0.))/std::max(0.5, mu->pt());
            mu_pfIso->push_back(pfisodb);

            mu_trkIso->push_back(mu->isolationR03().sumPt);

            double dZ = -999;
            if( !vertices_h->empty() && !vertices_h->front().isFake() ) {
                const reco::Vertex &vtx = vertices_h->front();
                dZ = mu->muonBestTrack()->dz(vtx.position());
 	    }
            mu_dz->push_back(dZ);

            double trkLayers = -999;
            double pixelHits = -999;
            double muonHits  = -999;
            double nMatches  = -999;
            double normChi2  = -999;
            if(isTracker && isGlobal ){
	        trkLayers     = mu->innerTrack()->hitPattern().trackerLayersWithMeasurement();
	        pixelHits     = mu->innerTrack()->hitPattern().numberOfValidPixelHits();
	        muonHits      = mu->globalTrack()->hitPattern().numberOfValidMuonHits();
	        nMatches      = mu->numberOfMatchedStations();
	        normChi2      = mu->globalTrack()->normalizedChi2();
            }
            mu_charge -> push_back(mu->charge());
            mu_d0->push_back(mu->dB());
            mu_chi2->push_back(normChi2);
            mu_nHits->push_back(muonHits);
            mu_nMuStations -> push_back(nMatches);
            mu_nPixHits->push_back(pixelHits);
            mu_nTrkLayers->push_back(trkLayers);

            if( _detail > 1 ) {
            
                mu_vtx_z->push_back(mu->vz());

                float Aecal=0.041; // initiallize with EE value
                float Ahcal=0.032; // initiallize with HE value
                if (fabs(mu->eta())<1.48) {
                  Aecal = 0.074;   // substitute EB value
                  Ahcal = 0.023;   // substitute EE value
                }
                float muonIsoRho = mu->isolationR03().sumPt + std::max(0.,(mu->isolationR03().emEt -Aecal*(*rho_h))) + std::max(0.,(mu->isolationR03().hadEt-Ahcal*(*rho_h)));
                double dbeta = muonIsoRho/mu->pt();
                mu_rhoIso->push_back(dbeta);
                mu_chHadIso->push_back(mu->pfIsolationR03().sumChargedHadronPt);
                mu_neuHadIso->push_back(mu->pfIsolationR03().sumNeutralHadronEt);
                mu_ecalIso ->push_back(mu->isolationR03().emEt);
                mu_hcalIso ->push_back(mu->isolationR03().hadEt);
                mu_sumPtIso ->push_back(mu->isolationR03().sumPt);

                mu_besttrk_pt -> push_back( mu->muonBestTrack()->pt() );
                mu_besttrk_pterr->push_back( mu->muonBestTrack()->ptError() );
            }
        }
    }
}



