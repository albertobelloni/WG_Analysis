#include <bitset>
#include <sstream>
#include "UMDNTuple/UMDNTuple/interface/TriggerProducer.h"
#include "FWCore/Framework/interface/Event.h"

TriggerProducer::TriggerProducer(  )  :
    _passing_triggers(0),
    HLTObj_n(0),
    HLTObj_pt(0),
    HLTObj_eta(0),
    HLTObj_phi(0),
    HLTObj_e(0),
    HLTObj_passTriggers(0)
{

}

void TriggerProducer::initialize( const std::string &prefix,
            const edm::EDGetTokenT<edm::TriggerResults>& trigTok,
            const edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection>& trigObjTok,
            const std::vector<std::string> &trigMap,
            TTree *tree, TTree *infoTree) {

    _prefix = prefix;
    _trigToken = trigTok;
    _trigObjToken = trigObjTok;
    _infoTree = infoTree;

    //tree->Branch("triggerBits", &triggerBits, "triggerBits/l" );
    tree->Branch("passedTriggers", &_passing_triggers );

    tree->Branch("HLTObj_n"  , &HLTObj_n, "HLTObj_n/I");
    tree->Branch("HLTObj_pt" , &HLTObj_pt );
    tree->Branch("HLTObj_eta", &HLTObj_eta );
    tree->Branch("HLTObj_phi", &HLTObj_phi );
    tree->Branch("HLTObj_e"  , &HLTObj_e );
    tree->Branch("HLTObj_passTriggers"  , &HLTObj_passTriggers );

    for( std::vector<std::string>::const_iterator itr = trigMap.begin();
            itr != trigMap.end(); ++itr ) {
        int trig_idx;

        std::string::size_type sep_pos = itr->find(":");
        std::string idx_str = itr->substr(0, sep_pos );
        std::string trig_name = itr->substr(sep_pos+1, itr->size() );

        std::stringstream idx_ss(idx_str);

        idx_ss >> trig_idx;

        _trigger_map[trig_name] = trig_idx;

    }

}


void TriggerProducer::produce(const edm::Event &iEvent ) {

    edm::Handle<edm::TriggerResults> triggers;
    iEvent.getByToken(_trigToken,triggers);

    edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
    iEvent.getByToken(_trigObjToken,triggerObjects);

    if( !triggers.isValid() || triggers.failedToGet() ) {
        std::cout << "could not get trigger results.  Will not fill triggers!" << std::endl;
        return;
    }

    _passing_triggers->clear();

    HLTObj_n=0;
    HLTObj_pt->clear();
    HLTObj_eta->clear();
    HLTObj_phi->clear();
    HLTObj_e->clear();
    HLTObj_passTriggers->clear();

    const edm::TriggerNames trigNames( iEvent.triggerNames( *triggers ) );

    if( _trigger_idx_map.size() == 0 ) {

        for (unsigned i = 0; i < trigNames.size(); i++) {

            std::string trigname = trigNames.triggerName(i);

            std::string::size_type version_pos = trigname.find_last_of("_");

            std::string trigname_mod = trigname.substr( 0, version_pos );

            std::map<std::string, int>::const_iterator mitr = _trigger_map.find(trigname_mod);

            if( mitr != _trigger_map.end() ) {
                _trigger_idx_map.push_back( std::make_pair(i, mitr->second) );
            }
        }
    }

    for( std::vector<std::pair<int,int> >::const_iterator mitr = _trigger_idx_map.begin();
            mitr != _trigger_idx_map.end(); ++mitr ) {
        if( triggers->accept( mitr->first ) ) {
            _passing_triggers->push_back( mitr->second );
        }
    }
    for (unsigned j=0; j < triggerObjects->size();++j){
        pat::TriggerObjectStandAlone obj = triggerObjects->at(j);
    
        obj.unpackPathNames(trigNames);
        
        std::vector<std::string> pathNamesLast = obj.pathNames(true);

        std::vector<int> passed_trigs;

        for( unsigned i = 0; i < pathNamesLast.size(); ++i ) {
            std::string pathname = pathNamesLast[i];
            if( pathname.substr(0,4) != "HLT_" ) continue; // ignore non "HLT" triggers

            std::string::size_type version_pos = pathname.find_last_of("_");

            std::string pathname_mod = pathname.substr(0, version_pos);

            std::map<std::string, int>::const_iterator mitr = 
                _trigger_map.find(pathname_mod);

            if( mitr != _trigger_map.end() ) {
                passed_trigs.push_back( mitr->second );
            }
        }

        if( passed_trigs.size() > 0 ) {

            HLTObj_n++;
            HLTObj_pt->push_back( obj.pt() );
            HLTObj_eta->push_back( obj.eta() );
            HLTObj_phi->push_back( obj.phi() );
            HLTObj_e->push_back( obj.energy() );
            HLTObj_passTriggers->push_back(passed_trigs);
        }

    }
        //std::vector<std::string> pathNamesAll = obj.pathNames(false);


    //triggerBits = 0;

    //if( _trigger_indices.size() == 0 ) {

    //    edm::RefProd<edm::TriggerNames> trigNames( &(iEvent.triggerNames( *triggers )) );

    //    unsigned itrig = 0;
    //    for (unsigned i = 0; i < trigNames->size(); i++) {

    //        std::string trigname = trigNames->triggerName(i);
    //        if( trigname.substr(0,4) != "HLT_" ) continue;

    //        _trigger_indices.push_back( i );

    //        std::cout << trigname << std::endl;

    //        if( _trigger_indices.size() >= 64 ) break;

    //    }

    //}

    //std::cout << "Event" << std::endl;
    //for( unsigned idx = 0; idx < _trigger_indices.size(); ++idx ) {

    //    if( triggers->accept(_trigger_indices[idx]) ) {
    //        std::cout << "Accept " << idx << std::endl;
    //        std::cout << std::bitset<64>(1 << idx) << std::endl;

    //        triggerBits |= (1 << idx);
    //    }
    //}

    //std::cout << std::bitset<64>(triggerBits) << std::endl;




    //if( _result_map.size() == 0 ) {

    //    edm::RefProd<edm::TriggerNames> trigNames( &(iEvent.triggerNames( *triggers )) );

    //    for (unsigned i = 0; i < trigNames->size(); i++) {

    //        std::string trigname = trigNames->triggerName(i);

    //        if( trigname.substr(0,4) == "HLT_" ) {
    //            _result_map[i] = 0;
    //            _tree->Branch( trigname.c_str(), &_result_map[i], (trigname + "/O").c_str() );
    //        }
    //        //if( _result_map.size() >= 64 ) {
    //        //    break;
    //        //}

    //    }

    //}

    //for( std::map<int, bool>::iterator itr = _result_map.begin();
    //        itr != _result_map.end(); ++itr ) {

    //    itr->second = triggers->accept(itr->first);
    //}

}

void TriggerProducer::endRun() {

    int trigger_ids = 0;
    std::vector<char*> descriptions;
    descriptions.push_back(new char[1024]);

    _infoTree->Branch( "trigger_ids", &trigger_ids, "trigger_ids/I" );
    _infoTree->Branch( "trigger_names", descriptions.back(), "trigger_names/C");

    for( std::map<std::string, int>::const_iterator itr = _trigger_map.begin();
            itr != _trigger_map.end(); ++itr ) {

        trigger_ids = itr->second;
        strcpy( descriptions.back(), itr->first.c_str() );

        _infoTree->Fill();
    }

}


