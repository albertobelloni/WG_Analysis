#include "UMDNTuple/UMDNTuple/interface/JetProducer.h"
#include "FWCore/Framework/interface/EDConsumerBase.h"
#include "FWCore/Framework/interface/Event.h"

JetProducer::JetProducer(  ) : 
    jet_n(0),
    jet_pt(0),
    jet_eta(0),
    jet_phi(0),
    jet_e(0),
    jet_nhf(0),
    jet_chf(0),
    jet_muf(0),
    jet_cemf(0),
    jet_nemf(0),
    jet_cmult(0),
    jet_nmult(0),
    jet_ndaughters(0),
    jet_bTagCSV(0),
    jet_bTagCSVV1(0),
    jet_bTagCSVSLV1(0),
    jet_bTagCisvV2(0),
    jet_bTagJp(0),
    jet_bTagBjp(0),
    jet_bTagTche(0),
    jet_bTagTchp(0),
    jet_bTagSsvhe(0),
    jet_bTagSsvhp(0),
    jet_HFHadE(0),
    jet_HFEmE(0),
    _detail(99)
{

}

void JetProducer::initialize( const std::string &prefix,
                                    const edm::EDGetTokenT<edm::View<pat::Jet> >&jetTok,
                                    TTree *tree, float minPt, int detail) {

    _prefix = prefix;
    _jetToken = jetTok;
    _detail = detail;
    _minPt = minPt;

    tree->Branch( (prefix + "_n" ).c_str(), &jet_n, (prefix + "_n/I" ).c_str() );

    tree->Branch( (prefix + "_pt" ).c_str(), &jet_pt );
    tree->Branch( (prefix + "_eta").c_str(), &jet_eta );
    tree->Branch( (prefix + "_phi").c_str(), &jet_phi );
    tree->Branch( (prefix + "_e"  ).c_str(), &jet_e );

    if( _detail > 0 ) {

        tree->Branch( (prefix + "_nhf" ).c_str()         , &jet_nhf);
        tree->Branch( (prefix + "_chf" ).c_str()         , &jet_chf);
        tree->Branch( (prefix + "_muf" ).c_str()         , &jet_muf);
        tree->Branch( (prefix + "_cemf" ).c_str()        , &jet_cemf);
        tree->Branch( (prefix + "_nemf" ).c_str()        , &jet_nemf);
        tree->Branch( (prefix + "_cmult" ).c_str()       , &jet_cmult);
        tree->Branch( (prefix + "_nmult" ).c_str()       , &jet_nmult);
        tree->Branch( (prefix + "_ndaughters" ).c_str()  , &jet_ndaughters);
        tree->Branch( (prefix + "_bTagCisvV2" ).c_str()  , &jet_bTagCisvV2);

        if( _detail > 1 ) {

            tree->Branch( (prefix + "_bTagCSV" ).c_str()     , &jet_bTagCSV);
            tree->Branch( (prefix + "_bTagCSVV1" ).c_str()   , &jet_bTagCSVV1);
            tree->Branch( (prefix + "_bTagCSVSLV1" ).c_str() , &jet_bTagCSVSLV1);


            tree->Branch( (prefix + "_bTagJp" ).c_str()      , &jet_bTagJp);
            tree->Branch( (prefix + "_bTagBjp" ).c_str()     , &jet_bTagBjp);
            tree->Branch( (prefix + "_bTagTche" ).c_str()    , &jet_bTagTche);
            tree->Branch( (prefix + "_bTagTchp" ).c_str()    , &jet_bTagTchp);
            tree->Branch( (prefix + "_bTagSsvhe" ).c_str()   , &jet_bTagSsvhe);
            tree->Branch( (prefix + "_bTagSsvhp" ).c_str()   , &jet_bTagSsvhp);
            tree->Branch( (prefix + "_HFHadE" ).c_str()      , &jet_HFHadE);
            tree->Branch( (prefix + "_HFEmE" ).c_str()       , &jet_HFEmE);
        }
    }
}


void JetProducer::produce(const edm::Event &iEvent ) {

    jet_n = 0;
    jet_pt->clear();
    jet_eta->clear();
    jet_phi->clear();
    jet_e->clear();
    if( _detail > 0 ) {
        jet_nhf->clear();
        jet_chf->clear();
        jet_muf->clear();
        jet_cemf->clear();
        jet_nemf->clear();
        jet_cmult->clear();
        jet_nmult->clear();
        jet_ndaughters->clear();
        jet_bTagCisvV2->clear();
        if( _detail > 1) {
            jet_bTagCSV->clear();
            jet_bTagCSVV1->clear();
            jet_bTagCSVSLV1->clear();
            jet_bTagJp->clear();
            jet_bTagBjp->clear();
            jet_bTagTche->clear();
            jet_bTagTchp->clear();
            jet_bTagSsvhe->clear();
            jet_bTagSsvhp->clear();
            jet_HFHadE->clear();
            jet_HFEmE->clear();
        }
            
    }

    iEvent.getByToken(_jetToken,jets);

    for (unsigned int j=0; j < jets->size();++j){
        edm::Ptr<pat::Jet> jet = jets->ptrAt(j);
        //const pat::Jet & jet = (*jetptr);
 
        if( jet->pt() < _minPt ) continue;

        jet_n += 1;

        jet_pt -> push_back( jet->pt() );
        jet_eta -> push_back( jet->eta() );
        jet_phi -> push_back( jet->phi() );
        jet_e -> push_back( jet->energy() );

        if( _detail > 0 ) {

            jet_nhf        -> push_back( jet->neutralHadronEnergyFraction());
            jet_chf        -> push_back( jet->chargedHadronEnergyFraction());
            jet_muf        -> push_back( jet->muonEnergyFraction());
            jet_cemf       -> push_back( jet->chargedEmEnergyFraction());
            jet_nemf       -> push_back( jet->neutralEmEnergyFraction());
            jet_cmult      -> push_back( jet->chargedMultiplicity());
            jet_nmult      -> push_back( jet->neutralMultiplicity());
            jet_ndaughters -> push_back( jet->numberOfDaughters());
            jet_bTagCisvV2  ->push_back(jet->bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"));

            if( _detail > 1 ) {

                //pfJetBProbabilityBJetTags, pfJetProbabilityBJetTags, pfTrackCountingHighEffBJetTags, pfSimpleSecondaryVertexHighEffBJetTags, pfSimpleInclusiveSecondaryVertexHighEffBJetTags, pfCombinedSecondaryVertexV2BJetTags, pfCombinedInclusiveSecondaryVertexV2BJetTags, softPFMuonBJetTags, softPFElectronBJetTags, pfCombinedMVAV2BJetTags, pfCombinedCvsLJetTags, pfCombinedCvsBJetTags, pfDeepCSVJetTags:probb, pfDeepCSVJetTags:probc, pfDeepCSVJetTags:probudsg, pfDeepCSVJetTags:probbb

                jet_bTagCSV     ->push_back(jet->bDiscriminator("combinedSecondaryVertexBJetTags"));
                jet_bTagCSVV1   ->push_back(jet->bDiscriminator("combinedSecondaryVertexV1BJetTags"));
                jet_bTagCSVSLV1 ->push_back(jet->bDiscriminator("combinedSecondaryVertexSoftPFLeptonV1BJetTags"));

                jet_bTagJp      ->push_back(jet->bDiscriminator("pfJetProbabilityBJetTags"));
                jet_bTagBjp     ->push_back(jet->bDiscriminator("pfJetBProbabilityBJetTags"));
                jet_bTagTche    ->push_back(jet->bDiscriminator("pfTrackCountingHighEffBJetTags"));
                jet_bTagTchp    ->push_back(jet->bDiscriminator("pfTrackCountingHighPurBJetTags"));
                jet_bTagSsvhe   ->push_back(jet->bDiscriminator("pfSimpleSecondaryVertexHighEffBJetTags"));
                jet_bTagSsvhp   ->push_back(jet->bDiscriminator("pfSimpleSecondaryVertexHighPurBJetTags"));

                // this would be for gen jets
                //JetAk04PartFlav_->push_back(jet.partonFlavour());
                //JetAk04HadFlav_->push_back(jet.hadronFlavour());

                jet_HFHadE->push_back(jet->HFHadronEnergy());
                jet_HFEmE->push_back(jet->HFEMEnergy());
            }
        }
    }

}



