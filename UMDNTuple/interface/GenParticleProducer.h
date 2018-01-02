#ifndef GENPARTICLEPRODUCER_H
#define GENPARTICLEPRODUCER_H
#include <vector>
#include <string>
#include "TTree.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"


class GenParticleProducer {

    public :
        GenParticleProducer();

        //void initialize( const TTree *tree );
        void initialize( const std::string &prefix, 
                         const edm::EDGetTokenT<std::vector<reco::GenParticle> >&genTok, 
                         TTree *tree, float minPt =1);

        void produce(const edm::Event &iEvent );


    private :

        std::string _prefix;

        int gen_n;

        std::vector<float> *gen_pt;
        std::vector<float> *gen_eta;
        std::vector<float> *gen_phi;
        std::vector<float> *gen_e;
        std::vector<int> *gen_PID;
        std::vector<int> *gen_status;
        std::vector<int> *gen_motherPID;
        std::vector<Bool_t> *gen_isPromptFinalState;
        std::vector<Bool_t> *gen_fromHardProcessFinalState;
        std::vector<Bool_t> *gen_fromHardProcessBeforeFSR;

        edm::EDGetTokenT<std::vector<reco::GenParticle> > _genPartToken;

        float _minPt;

};
#endif
