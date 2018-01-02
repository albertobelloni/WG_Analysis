#ifndef MUONPRODUCER_H
#define MUONPRODUCER_H
#include <vector>
#include <string>
#include "TTree.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"


class MuonProducer {

    public :
        MuonProducer();

        //void initialize( const TTree *tree );
        void initialize( const std::string &prefix, 
                         const edm::EDGetTokenT<edm::View<pat::Muon> >&muonTok, 
                         TTree *tree, float minPt = 5, int detail=99 );

        void addVertexToken( const edm::EDGetTokenT<std::vector<reco::Vertex> > & );
        void addRhoToken( const edm::EDGetTokenT<double> & );

        void produce(const edm::Event &iEvent );


    private :

        std::string _prefix;

        int mu_n;
        std::vector<float> *mu_pt;
        std::vector<float> *mu_eta;
        std::vector<float> *mu_phi;
        std::vector<float> *mu_e;
        std::vector<Bool_t> *mu_isGlobal;
        std::vector<Bool_t> *mu_isTracker;
        std::vector<Bool_t> *mu_isPf;
        std::vector<float> *mu_pfIso;
        std::vector<float> *mu_trkIso;
        std::vector<float> *mu_dz;
        std::vector<int> *mu_charge;
        std::vector<float> *mu_d0;
        std::vector<float> *mu_chi2;
        std::vector<int> *mu_nHits;
        std::vector<int> *mu_nMuStations;
        std::vector<int> *mu_nPixHits;
        std::vector<int> *mu_nTrkLayers;
        std::vector<float> *mu_vtx_z;
        std::vector<float> *mu_rhoIso;
        std::vector<float> *mu_chHadIso;
        std::vector<float> *mu_neuHadIso;
        std::vector<float> *mu_ecalIso;
        std::vector<float> *mu_hcalIso;
        std::vector<float> *mu_sumPtIso;
        std::vector<float> *mu_besttrk_pt;
        std::vector<float> *mu_besttrk_pterr;

        edm::EDGetTokenT<edm::View<pat::Muon> > _muonToken;
        edm::Handle<edm::View<pat::Muon> > muons;
        edm::EDGetTokenT<std::vector<reco::Vertex> > _vertexToken;
        edm::EDGetTokenT<double> _rhoToken;
         
        int _detail;
        float _minPt;

};
#endif
