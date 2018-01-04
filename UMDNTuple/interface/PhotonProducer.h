#ifndef PHOTONPRODUCER_H
#define PHOTONPRODUCER_H

#include <vector>
#include <string>
#include "TTree.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

enum PhotonUserVar {

    PhotonVIDLoose = 0,
    PhotonVIDMedium = 1,
    PhotonVIDTight = 2,
    PhotonChIso = 3,
    PhotonNeuIso = 4,
    PhotonPhoIso = 5

};



class PhotonProducer {

    private :

        typedef std::map<std::string, edm::EDGetTokenT<edm::ValueMap<Bool_t> > > TokenBoolMap;
        typedef std::map<std::string, edm::EDGetTokenT<edm::ValueMap<float> > > TokenFloatMap;

    public :
        PhotonProducer();

        //void initialize( const TTree *tree );
        void initialize( const std::string &prefix, 
                         const edm::EDGetTokenT<edm::View<pat::Photon> >&photTok, 
                         TTree *tree, float minPt=5, int detail=99 );
        //void addUserFloat( const std::string &, const edm::EDGetTokenT<edm::ValueMap<float> > & );
        void addUserBool ( PhotonUserVar , const edm::EDGetTokenT<edm::ValueMap<Bool_t> > & );
        void addUserFloat( PhotonUserVar , const edm::EDGetTokenT<edm::ValueMap<float> > & );
        
        void addElectronsToken( const edm::EDGetTokenT<edm::View<pat::Electron> > &);
        void addConversionsToken( const edm::EDGetTokenT<reco::ConversionCollection> &);
        void addBeamSpotToken( const edm::EDGetTokenT<reco::BeamSpot> &);
        void addCalibratedToken( const edm::EDGetTokenT<edm::View<pat::Photon> > &);
        
        void produce(const edm::Event &iEvent );


        std::string _prefix;

        int ph_n;
        std::vector<float> *ph_pt;
        std::vector<float> *ph_eta;
        std::vector<float> *ph_phi;
        std::vector<float> *ph_e;
        std::vector<float> *ph_ptOrig;
        std::vector<float> *ph_etaOrig;
        std::vector<float> *ph_phiOrig;
        std::vector<float> *ph_eOrig;
        std::vector<Bool_t> *ph_passVIDLoose;
        std::vector<Bool_t> *ph_passVIDMedium;
        std::vector<Bool_t> *ph_passVIDTight;
        std::vector<float> *ph_chIso;
        std::vector<float> *ph_neuIso;
        std::vector<float> *ph_phoIso;

        std::vector<float> *ph_sc_eta;
        std::vector<float> *ph_sc_phi;
        std::vector<float> *ph_hOverE;
        std::vector<float> *ph_sigmaIEIE;
        std::vector<float> *ph_sigmaIEIEFull5x5;
        std::vector<float> *ph_r9;
        std::vector<float> *ph_r9Full5x5;
        std::vector<float> *ph_etaWidth;
        std::vector<float> *ph_phiWidth;
        std::vector<Bool_t> *ph_passEleVeto;
        std::vector<Bool_t> *ph_hasPixSeed;
        std::vector<float> *ph_sc_rawE;
        std::vector<float> *ph_ecalIso;
        std::vector<float> *ph_hcalIso;
        std::vector<float> *ph_trkIso;
        std::vector<float> *ph_pfIsoPUChHad;
        std::vector<float> *ph_pfIsoEcal;
        std::vector<float> *ph_pfIsoHcal;
        std::vector<float> *ph_E3x3;
        std::vector<float> *ph_E1x5;
        std::vector<float> *ph_E2x5;
        std::vector<float> *ph_E5x5;
        //std::vector<float> *ph_sigmaIetaIphi;
        //std::vector<float> *ph_sigmaIphiIphi;
        std::vector<float> *ph_E1x5Full5x5;
        std::vector<float> *ph_E2x5Full5x5;
        std::vector<float> *ph_E3x3Full5x5;
        std::vector<float> *ph_E5x5Full5x5;

        edm::EDGetTokenT<edm::View<pat::Photon> > _photToken;
        edm::EDGetTokenT<edm::View<pat::Photon> > _photCalibToken;

        //std::map<std::string, std::vector<float>* > ph_user_floats;
        //std::map<std::string, std::vector<Bool_t>* > ph_user_bools;

        //std::map< std::string, edm::EDGetTokenT<edm::ValueMap<Bool_t> > > _tokens_bool;
        //std::map< std::string, edm::EDGetTokenT<edm::ValueMap<float> > > _tokens_float;

        edm::EDGetTokenT<edm::ValueMap<Bool_t> > _VIDLooseToken;
        edm::EDGetTokenT<edm::ValueMap<Bool_t> > _VIDMediumToken;
        edm::EDGetTokenT<edm::ValueMap<Bool_t> > _VIDTightToken;

        edm::EDGetTokenT<edm::ValueMap<float> > _ChIsoToken;
        edm::EDGetTokenT<edm::ValueMap<float> > _NeuIsoToken;
        edm::EDGetTokenT<edm::ValueMap<float> > _PhoIsoToken;

        edm::EDGetTokenT<edm::View<pat::Electron> > _ElectronsToken;
        edm::EDGetTokenT<reco::ConversionCollection> _ConversionsToken;
        edm::EDGetTokenT<reco::BeamSpot> _beamSpotToken;

        //edm::EDGetTokenT<edm::ValueMap<float> > 
        int _detail;
        TTree * _tree;
        float _minPt;

};
#endif
