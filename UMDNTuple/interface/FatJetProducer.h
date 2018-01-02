#ifndef FATJETPRODUCER_H
#define FATJETPRODUCER_H
#include <vector>
#include <string>
#include "TTree.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "UMDNTuple/UMDNTuple/interface/JetProducer.h"


class FatJetProducer {

    public :
        FatJetProducer();

        //void initialize( const TTree *tree );
        void initialize( const std::string &prefix, 
                         const edm::EDGetTokenT<edm::View<pat::Jet> >&jetTok, 
                         TTree *tree, float minPt = 200 );

        void produce(const edm::Event &iEvent );


    private :

        std::string _prefix;

        std::vector<float> *jet_ak08_prunedMass;
        //std::vector<float> *jet_ak08_FilteredMass;
        std::vector<float> *jet_ak08_SoftDropMass;
        std::vector<float> *jet_ak08_Puppi_SoftDropMass;
        std::vector<float> *jet_ak08_TrimmedMass;
        std::vector<float> *jet_ak08_tau1;
        std::vector<float> *jet_ak08_tau2;
        std::vector<float> *jet_ak08_tau3;
        std::vector<float> *jet_ak08_Puppi_tau1;
        std::vector<float> *jet_ak08_Puppi_tau2;
        std::vector<float> *jet_ak08_Puppi_tau3;

        edm::EDGetTokenT<edm::View<pat::Jet> > _jetToken;
        edm::Handle<edm::View<pat::Jet> > jets;
        JetProducer _jetProducer;

        float _minPt;

};
#endif
