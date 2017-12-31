#include <bitset>
#include "UMDNTuple/UMDNTuple/interface/TriggerProducer.h"
#include "FWCore/Framework/interface/Event.h"

TriggerProducer::TriggerProducer(  ) 
{

}

void TriggerProducer::initialize( const std::string &prefix,
                                  const edm::EDGetTokenT<edm::TriggerResults>& trigTok,
                                  TTree *tree) {

    _prefix = prefix;
    _trigToken = trigTok;

    _tree = tree;
    
    //tree->Branch("triggerBits", &triggerBits, "triggerBits/l" );


}


void TriggerProducer::produce(const edm::Event &iEvent ) {

    iEvent.getByToken(_trigToken,triggers);

    if( !triggers.isValid() || triggers.failedToGet() ) {
        std::cout << "could not get trigger results.  Will not fill triggers!" << std::endl;
        return;
    }

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




    if( _result_map.size() == 0 ) {

        edm::RefProd<edm::TriggerNames> trigNames( &(iEvent.triggerNames( *triggers )) );

        for (unsigned i = 0; i < trigNames->size(); i++) {

            std::string trigname = trigNames->triggerName(i);

            if( trigname.substr(0,4) == "HLT_" ) {
                _result_map[i] = 0;
                _tree->Branch( trigname.c_str(), &_result_map[i], (trigname + "/O").c_str() );
            }
            //if( _result_map.size() >= 64 ) {
            //    break;
            //}

        }

    }

    for( std::map<int, bool>::iterator itr = _result_map.begin();
            itr != _result_map.end(); ++itr ) {

        itr->second = triggers->accept(itr->first);
    }

}



