#ifndef METPRODUCER_H
#define METPRODUCER_H
#include <vector>
#include <string>
#include "TTree.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"


class METProducer {

    public :
        METProducer();

        //void initialize( const TTree *tree );
        void initialize( const std::string &prefix, 
                         const edm::EDGetTokenT<edm::View<pat::MET> >&metTok, 
                         TTree *tree );

        void produce(const edm::Event &iEvent );


    private :

        std::string _prefix;

        float met_pt;
        float met_phi;

        float met_JetResUp_pt;
        float met_JetResUp_phi;
        float met_JetResDown_pt;
        float met_JetResDown_phi;

        float met_JetEnUp_pt;
        float met_JetEnUp_phi;
        float met_JetEnDown_pt;
        float met_JetEnDown_phi;

        float met_MuonEnUp_pt;
        float met_MuonEnUp_phi;
        float met_MuonEnDown_pt;
        float met_MuonEnDown_phi;
       
        float met_ElectronEnUp_pt;
        float met_ElectronEnUp_phi;
        float met_ElectronEnDown_pt;
        float met_ElectronEnDown_phi;

        float met_PhotonEnUp_pt;
        float met_PhotonEnUp_phi;
        float met_PhotonEnDown_pt;
        float met_PhotonEnDown_phi;

        float met_UnclusteredEnUp_pt;
        float met_UnclusteredEnUp_phi;
        float met_UnclusteredEnDown_pt;
        float met_UnclusteredEnDown_phi;


        edm::EDGetTokenT<edm::View<pat::MET> > _metToken;
        edm::Handle<edm::View<pat::MET> > mets;

};
#endif
