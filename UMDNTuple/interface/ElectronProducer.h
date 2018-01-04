#ifndef ELECTRONPRODUCER_H
#define ELECTRONPRODUCER_H
#include <vector>
#include <string>
#include "TTree.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

enum ElectronUserVar {

    ElectronIdVeryLoose = 0,
    ElectronIdLoose = 1,
    ElectronIdMedium = 2,
    ElectronIdTight = 3,
    ElectronIdHLT = 4,
    ElectronIdHEEP = 5

};

class ElectronProducer {

    public :
        ElectronProducer();

        //void initialize( const TTree *tree );
        void initialize( const std::string &prefix, 
                         const edm::EDGetTokenT<edm::View<pat::Electron> >&elecTok, 
                         TTree *tree, float minPt=5, int detail=99 );

        void addUserBool ( ElectronUserVar , const edm::EDGetTokenT<edm::ValueMap<Bool_t> > & );

        void addConversionsToken( const edm::EDGetTokenT<reco::ConversionCollection> & );
        void addBeamSpotToken( const edm::EDGetTokenT<reco::BeamSpot> & );
        void addVertexToken( const edm::EDGetTokenT<std::vector<reco::Vertex> > & );
        void addRhoToken( const edm::EDGetTokenT<double> & );
        void addCalibratedToken( const edm::EDGetTokenT<edm::View<pat::Electron> > & );

        void produce(const edm::Event &iEvent );


    private :

        std::string _prefix;

        int el_n;

        std::vector<float> *el_pt;
        std::vector<float> *el_eta;
        std::vector<float> *el_phi;
        std::vector<float> *el_e;
        std::vector<float> *el_ptOrig;
        std::vector<float> *el_etaOrig;
        std::vector<float> *el_phiOrig;
        std::vector<float> *el_eOrig;

        std::vector<Bool_t> *el_passVIDVeryLoose;
        std::vector<Bool_t> *el_passVIDLoose;
        std::vector<Bool_t> *el_passVIDMedium;
        std::vector<Bool_t> *el_passVIDTight;
        std::vector<Bool_t> *el_passVIDHEEP;
        std::vector<Bool_t> *el_passVIDHLT;

        std::vector<float> *el_hOverE;
        std::vector<float> *el_sigmaIEIE;
        std::vector<float> *el_sigmaIEIEfull5x5;
        std::vector<float> *el_dEtaIn;
        std::vector<float> *el_dPhiIn;
        std::vector<float> *el_ooEmooP;
        std::vector<float> *el_d0;
        std::vector<float> *el_dz;

        std::vector<Bool_t> *el_passConvVeto;
        std::vector<int> *el_expectedMissingInnerHits;
        std::vector<int> *el_charge;

        std::vector<float> *el_sc_eta;
        std::vector<float> *el_dEtaClusterTrack;
        std::vector<float> *el_dPhiClusterTrack;
        std::vector<float> *el_sc_rawE;
        std::vector<float> *el_ecalIso;
        std::vector<float> *el_ecalPfIso;
        std::vector<float> *el_aeff;
        std::vector<float> *el_chIso;
        std::vector<float> *el_neuIso;
        std::vector<float> *el_phoIso;
        std::vector<float> *el_puChIso;
        std::vector<float> *el_pfIsoRaw;
        std::vector<float> *el_pfIsoDbeta;
        std::vector<float> *el_pfIsoRho;
        std::vector<float> *el_trkSumPt;
        std::vector<float> *el_ecalRecHitSumEt;
        std::vector<float> *el_hcalTowerSumEt;




        edm::EDGetTokenT<edm::View<pat::Electron> > _elecToken;
        edm::EDGetTokenT<edm::View<pat::Electron> > _elecCalibToken;

        edm::EDGetTokenT<reco::BeamSpot> _beamSpotToken;
        edm::EDGetTokenT<reco::ConversionCollection> _conversionsToken;

        edm::EDGetTokenT<edm::ValueMap<Bool_t> > _IdVeryLooseToken;
        edm::EDGetTokenT<edm::ValueMap<Bool_t> > _IdLooseToken;
        edm::EDGetTokenT<edm::ValueMap<Bool_t> > _IdMediumToken;
        edm::EDGetTokenT<edm::ValueMap<Bool_t> > _IdTightToken;
        edm::EDGetTokenT<edm::ValueMap<Bool_t> > _IdHEEPToken;
        edm::EDGetTokenT<edm::ValueMap<Bool_t> > _IdHLTToken;

        edm::EDGetTokenT<std::vector<reco::Vertex> > _vertexToken;
        edm::EDGetTokenT<double> _rhoToken;

        int _detail;
        float _minPt;

};
#endif
