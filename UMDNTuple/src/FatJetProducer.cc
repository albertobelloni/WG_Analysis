#include "UMDNTuple/UMDNTuple/interface/FatJetProducer.h"
#include "FWCore/Framework/interface/EDConsumerBase.h"
#include "FWCore/Framework/interface/Event.h"

FatJetProducer::FatJetProducer(  ) : 
    jet_ak08_prunedMass(0),
    //jet_ak08_FilteredMass(0),
    jet_ak08_SoftDropMass(0),
    jet_ak08_Puppi_SoftDropMass(0),
    jet_ak08_TrimmedMass(0),
    jet_ak08_tau1(0),
    jet_ak08_tau2(0),
    jet_ak08_tau3(0),
    jet_ak08_Puppi_tau1(0),
    jet_ak08_Puppi_tau2(0),
    jet_ak08_Puppi_tau3(0)
{

}

void FatJetProducer::initialize( const std::string &prefix,
                                 const edm::EDGetTokenT<edm::View<pat::Jet> >&jetTok,
                                 TTree *tree, float minPt) {

    _prefix = prefix;
    _jetToken = jetTok;
    _minPt = minPt;

    tree->Branch( (prefix + "_ak08_prunedMass" ).c_str(), &jet_ak08_prunedMass );
    //tree->Branch( (prefix + "_ak08_FilteredMass" ).c_str(), &jet_ak08_FilteredMass );
    tree->Branch( (prefix + "_ak08_SoftDropMass" ).c_str(), &jet_ak08_SoftDropMass );
    tree->Branch( (prefix + "_ak08_Puppi_SoftDropMass" ).c_str(), &jet_ak08_Puppi_SoftDropMass );
    tree->Branch( (prefix + "_ak08_TrimmedMass" ).c_str(), &jet_ak08_TrimmedMass );
    tree->Branch( (prefix + "_ak08_tau1" ).c_str(), &jet_ak08_tau1 );
    tree->Branch( (prefix + "_ak08_tau2" ).c_str(), &jet_ak08_tau2 );
    tree->Branch( (prefix + "_ak08_tau3" ).c_str(), &jet_ak08_tau3 );
    tree->Branch( (prefix + "_ak08_Puppi_tau1" ).c_str(), &jet_ak08_Puppi_tau1 );
    tree->Branch( (prefix + "_ak08_Puppi_tau2" ).c_str(), &jet_ak08_Puppi_tau2 );
    tree->Branch( (prefix + "_ak08_Puppi_tau3" ).c_str(), &jet_ak08_Puppi_tau3 );

    _jetProducer.initialize( prefix, jetTok, tree, 1 );



}


void FatJetProducer::produce(const edm::Event &iEvent ) {

    jet_ak08_prunedMass->clear();
    //jet_ak08_FilteredMass->clear();
    jet_ak08_SoftDropMass->clear();
    jet_ak08_Puppi_SoftDropMass->clear();
    jet_ak08_TrimmedMass->clear();
    jet_ak08_tau1->clear();
    jet_ak08_tau2->clear();
    jet_ak08_tau3->clear();
    jet_ak08_Puppi_tau1->clear();
    jet_ak08_Puppi_tau2->clear();
    jet_ak08_Puppi_tau3->clear();

    _jetProducer.produce( iEvent );

    iEvent.getByToken(_jetToken,jets);

    for (unsigned int j=0; j < jets->size();++j){
        edm::Ptr<pat::Jet> jet = jets->ptrAt(j);
 
        if( jet->pt() < _minPt ) continue;

        //jet_ak08_prunedMass -> push_back( jet->userFloat("ak8PFJetsCHSValueMap:ak8PFJetsCHSPrunedMass") );
        jet_ak08_prunedMass -> push_back( jet->userFloat("ak8PFJetsCHSPrunedMass") );


//Available user floats : 
//NjettinessAK8Puppi:tau1 
//NjettinessAK8Puppi:tau2 
//NjettinessAK8Puppi:tau3 
//ak8PFJetsCHSValueMap:NjettinessAK8CHSTau1 
//ak8PFJetsCHSValueMap:NjettinessAK8CHSTau2 
//ak8PFJetsCHSValueMap:NjettinessAK8CHSTau3 
//ak8PFJetsCHSValueMap:ak8PFJetsCHSPrunedMass 
//ak8PFJetsCHSValueMap:ak8PFJetsCHSSoftDropMass 
//ak8PFJetsCHSValueMap:eta 
//ak8PFJetsCHSValueMap:mass 
//ak8PFJetsCHSValueMap:phi 
//ak8PFJetsCHSValueMap:pt 
//ak8PFJetsPuppiSoftDropMass 


        //jet_ak08_FilteredMass->push_back(jet->userFloat("ak8PFJetsCHSFilteredMass"));
        jet_ak08_SoftDropMass->push_back(jet->userFloat("ak8PFJetsCHSSoftDropMass"));
        //jet_ak08_Puppi_SoftDropMass->push_back(jet->userFloat("ak8PFJetsPuppiSoftDropMass"));
        //jet_ak08_TrimmedMass->push_back(jet->userFloat("ak8PFJetsCHSTrimmedMass"));
        jet_ak08_tau1->push_back(jet->userFloat("NjettinessAK8:tau1"));
        jet_ak08_tau2->push_back(jet->userFloat("NjettinessAK8:tau2"));
        jet_ak08_tau3->push_back(jet->userFloat("NjettinessAK8:tau3"));
        jet_ak08_Puppi_tau1->push_back(jet->userFloat("ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau1"));
        jet_ak08_Puppi_tau2->push_back(jet->userFloat("ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau2"));
        jet_ak08_Puppi_tau3->push_back(jet->userFloat("ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau3"));
    }

}

