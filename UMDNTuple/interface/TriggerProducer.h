#ifndef TRIGGERPRODUCER_H
#define TRIGGERPRODUCER_H
#include <vector>
#include <string>
#include "TTree.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
//#include "PhysicsTools/PatUtils/interface/TriggerHelper.h"
#include "FWCore/Common/interface/TriggerNames.h"


class TriggerProducer {

    public :
        TriggerProducer();

        //void initialize( const TTree *tree );
        void initialize( const std::string &prefix, 
                         const edm::EDGetTokenT<edm::TriggerResults >&, 
                         const edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection>&, 
                         const std::vector<std::string> &,
                         TTree *, TTree* );

        void produce(const edm::Event &iEvent );
        void endRun( );


    private :

        std::string _prefix;

        //std::vector<std::string> _name_list;
        //std::map<int, bool> _result_map;

        //std::vector<int> _trigger_indices;
        std::map<std::string, int> _trigger_map;
        std::vector<std::pair<int, int> > _trigger_idx_map;

        std::vector<int> *_passing_triggers;

        int HLTObj_n;
        std::vector<float> *HLTObj_pt;
        std::vector<float> *HLTObj_eta;
        std::vector<float> *HLTObj_phi;
        std::vector<float> *HLTObj_e;
        std::vector<std::vector< int > > *HLTObj_passTriggers;

        //ULong64_t triggerBits;

        edm::EDGetTokenT<edm::TriggerResults> _trigToken;
        edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> _trigObjToken;

        TTree *_infoTree;


};
#endif
