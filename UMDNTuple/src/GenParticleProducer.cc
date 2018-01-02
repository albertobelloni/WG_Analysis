#include "UMDNTuple/UMDNTuple/interface/GenParticleProducer.h"
#include "FWCore/Framework/interface/EDConsumerBase.h"
#include "FWCore/Framework/interface/Event.h"

GenParticleProducer::GenParticleProducer(  ) : 
    gen_n(0),
    gen_pt(0),
    gen_eta(0),
    gen_phi(0),
    gen_e(0),
    gen_PID(0),
    gen_status(0),
    gen_motherPID(0),
    gen_isPromptFinalState(0),
    gen_fromHardProcessFinalState(0),
    gen_fromHardProcessBeforeFSR(0)
{

}

void GenParticleProducer::initialize( const std::string &prefix,
                          const edm::EDGetTokenT<std::vector<reco::GenParticle> >&genTok,
                          TTree *tree, float minPt) {

    _prefix = prefix;
    _genPartToken = genTok;
    _minPt = minPt;


    tree->Branch( (prefix + "_n" ).c_str(), &gen_n, (prefix + "_n/I" ).c_str() );

    tree->Branch( (prefix + "_pt" ).c_str(), &gen_pt );
    tree->Branch( (prefix + "_eta").c_str(), &gen_eta );
    tree->Branch( (prefix + "_phi").c_str(), &gen_phi );
    tree->Branch( (prefix + "_e"  ).c_str(), &gen_e );
    tree->Branch( (prefix + "_PID" ).c_str(), &gen_PID);
    tree->Branch( (prefix + "_status" ).c_str(), &gen_status);
    tree->Branch( (prefix + "_motherPID" ).c_str(), &gen_motherPID);
    tree->Branch( (prefix + "_isPromptFinalState" ).c_str(), &gen_isPromptFinalState);
    tree->Branch( (prefix + "_fromHardProcessFinalState" ).c_str(), &gen_fromHardProcessFinalState);
    tree->Branch( (prefix + "_fromHardProcessBeforeFSR" ).c_str(), &gen_fromHardProcessBeforeFSR);
}


void GenParticleProducer::produce(const edm::Event &iEvent ) {

    gen_n = 0;

    gen_pt->clear();
    gen_eta->clear();
    gen_phi->clear();
    gen_e->clear();
    gen_PID->clear();
    gen_status->clear();
    gen_motherPID->clear();
    gen_isPromptFinalState->clear();
    gen_fromHardProcessFinalState->clear();
    gen_fromHardProcessBeforeFSR->clear();

    edm::Handle<std::vector<reco::GenParticle> > genParticles;

    iEvent.getByToken(_genPartToken,genParticles);

    for (unsigned int j=0; j < genParticles->size();++j){
        reco::GenParticle gen = genParticles->at(j);
 
        if( gen.pt() < _minPt ) continue;

        gen_n++;

        // kinematics
        gen_pt -> push_back( gen.pt() );
        gen_eta -> push_back( gen.eta() );
        gen_phi -> push_back( gen.phi() );
        gen_e -> push_back( gen.energy() );

        gen_PID -> push_back( gen.pdgId() );
        gen_status -> push_back( gen.status() );

        int motherId = 0;
        if( gen.numberOfMothers() > 0 ) motherId = gen.mother()->pdgId();
        gen_motherPID -> push_back( motherId );

        gen_isPromptFinalState -> push_back( gen.isPromptFinalState() );
        gen_fromHardProcessFinalState-> push_back( gen.fromHardProcessFinalState() );
        gen_fromHardProcessBeforeFSR-> push_back( gen.fromHardProcessBeforeFSR() );



    }

}



