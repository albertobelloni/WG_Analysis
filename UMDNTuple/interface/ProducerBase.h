#ifndef PRODUCERBASE_H
#define PRODUCERBASE_H

#include <vector>
#include <string>
#include "TTree.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"


class PhotonProducer {

    private :

        typedef std::map<std::string, edm::EDGetTokenT<edm::ValueMap<Bool_t> > > TokenBoolMap;
        typedef std::map<std::string, edm::EDGetTokenT<edm::ValueMap<float> > > TokenFloatMap;

    public :
        PhotonProducer();

        //void initialize( const TTree *tree );
        void initialize( const std::string &prefix, 
                         const edm::EDGetTokenT<edm::View<pat::Photon> >&photTok, 
                         TTree *tree );
        void addUserFloat( const std::string &, const edm::EDGetTokenT<edm::ValueMap<float> > & );
        void addUserBool ( const std::string &, const edm::EDGetTokenT<edm::ValueMap<Bool_t> > & );

        void produce(const edm::Event &iEvent );


        std::string _prefix;

        std::vector<float> *ph_pt;
        std::vector<float> *ph_eta;
        std::vector<float> *ph_phi;
        std::vector<float> *ph_e;

        edm::EDGetTokenT<edm::View<pat::Photon> > _photToken;
        edm::Handle<edm::View<pat::Photon> > photons;

        std::map<std::string, std::vector<float>* > ph_user_floats;
        std::map<std::string, std::vector<Bool_t>* > ph_user_bools;

        //std::vector< edm::EDGetTokenT<edm::ValueMap<Bool_t> > > _tokens_bool;
        //std::vector< edm::EDGetTokenT<edm::ValueMap<float> > > _tokens_float;
        std::map< std::string, edm::EDGetTokenT<edm::ValueMap<Bool_t> > > _tokens_bool;
        std::map< std::string, edm::EDGetTokenT<edm::ValueMap<float> > > _tokens_float;

        TTree * _tree;

};
#endif
