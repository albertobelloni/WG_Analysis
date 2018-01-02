#ifndef JETPRODUCER_H
#define JETPRODUCER_H
#include <vector>
#include <string>
#include "TTree.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"


class JetProducer {

    public :
        JetProducer();

        //void initialize( const TTree *tree );
        void initialize( const std::string &prefix, 
                         const edm::EDGetTokenT<edm::View<pat::Jet> >&jetTok, 
                         TTree *tree, float minPt=20, int detail=99 );

        void produce(const edm::Event &iEvent );


    private :

        std::string _prefix;

        int jet_n;

        std::vector<float> *jet_pt;
        std::vector<float> *jet_eta;
        std::vector<float> *jet_phi;
        std::vector<float> *jet_e;
        std::vector<float> *jet_nhf;
        std::vector<float> *jet_chf;
        std::vector<float> *jet_muf;
        std::vector<float> *jet_cemf;
        std::vector<float> *jet_nemf;
        std::vector<int> *jet_cmult;
        std::vector<int> *jet_nmult;
        std::vector<int> *jet_ndaughters;
        std::vector<float> *jet_bTagCSV;
        std::vector<float> *jet_bTagCSVV1;
        std::vector<float> *jet_bTagCSVSLV1;
        std::vector<float> *jet_bTagCisvV2;
        std::vector<float> *jet_bTagJp;
        std::vector<float> *jet_bTagBjp;
        std::vector<float> *jet_bTagTche;
        std::vector<float> *jet_bTagTchp;
        std::vector<float> *jet_bTagSsvhe;
        std::vector<float> *jet_bTagSsvhp;
        std::vector<float> *jet_HFHadE;
        std::vector<float> *jet_HFEmE;

        edm::EDGetTokenT<edm::View<pat::Jet> > _jetToken;
        edm::Handle<edm::View<pat::Jet> > jets;
        int _detail;
        float _minPt;

};
#endif
