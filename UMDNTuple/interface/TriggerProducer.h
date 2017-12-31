#ifndef TRIGGERPRODUCER_H
#define TRIGGERPRODUCER_H
#include <vector>
#include <string>
#include "TTree.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
//#include "PhysicsTools/PatUtils/interface/TriggerHelper.h"
#include "FWCore/Common/interface/TriggerNames.h"


class TriggerProducer {

    public :
        TriggerProducer();

        //void initialize( const TTree *tree );
        void initialize( const std::string &prefix, 
                         const edm::EDGetTokenT<edm::TriggerResults >&trigTok, 
                         TTree *tree );

        void produce(const edm::Event &iEvent );


    private :

        std::string _prefix;

        std::vector<std::string> _name_list;
        std::map<int, bool> _result_map;

        std::vector<int> _trigger_indices;

        //ULong64_t triggerBits;

        edm::EDGetTokenT<edm::TriggerResults> _trigToken;
        edm::Handle<edm::TriggerResults> triggers;

        TTree * _tree;

};
#endif
