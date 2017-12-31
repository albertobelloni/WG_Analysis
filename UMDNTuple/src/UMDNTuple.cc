#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "UMDNTuple/UMDNTuple/interface/UMDNTuple.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

UMDNTuple::UMDNTuple( const edm::ParameterSet & iConfig )
{
    edm::Service<TFileService> fs;

    _myTree = fs->make<TTree>( "EventTree", "EventTree" );
    _infoTree = fs->make<TTree>( "InfoTree", "InfoTree" );

    edm::EDGetTokenT<edm::View<pat::Electron> > elecToken = 
                 consumes<edm::View<pat::Electron> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("electronTag"));
    edm::EDGetTokenT<edm::ValueMap<Bool_t> > elecIdVeryLooseToken = 
                 consumes<edm::ValueMap<Bool_t> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("elecIdVeryLooseTag"));
    edm::EDGetTokenT<edm::ValueMap<Bool_t> > elecIdLooseToken = 
                 consumes<edm::ValueMap<Bool_t> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("elecIdLooseTag"));
    edm::EDGetTokenT<edm::ValueMap<Bool_t> > elecIdMediumToken = 
                 consumes<edm::ValueMap<Bool_t> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("elecIdMediumTag"));
    edm::EDGetTokenT<edm::ValueMap<Bool_t> > elecIdTightToken = 
                 consumes<edm::ValueMap<Bool_t> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("elecIdTightTag"));
    edm::EDGetTokenT<edm::ValueMap<Bool_t> > elecIdHLTToken = 
                 consumes<edm::ValueMap<Bool_t> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("elecIdHLTTag"));
    edm::EDGetTokenT<edm::ValueMap<Bool_t> > elecIdHEEPToken =  
                 consumes<edm::ValueMap<Bool_t> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("elecIdHEEPTag"));

    edm::EDGetTokenT<edm::View<pat::Muon> > muonToken = 
                 consumes<edm::View<pat::Muon> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("muonTag"));
    edm::EDGetTokenT<edm::View<pat::Photon> > photToken = 
                  consumes<edm::View<pat::Photon> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("photonTag"));
    edm::EDGetTokenT<edm::ValueMap<float> > phoChIsoToken = 
                 consumes<edm::ValueMap<float> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("phoChIsoTag"));
    edm::EDGetTokenT<edm::ValueMap<float> > phoNeuIsoToken = 
                 consumes<edm::ValueMap<float> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("phoNeuIsoTag"));
    edm::EDGetTokenT<edm::ValueMap<float> > phoPhoIsoToken = 
                 consumes<edm::ValueMap<float> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("phoPhoIsoTag"));
    edm::EDGetTokenT<edm::ValueMap<Bool_t> > phoIdLooseToken = 
                 consumes<edm::ValueMap<Bool_t> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("phoIdLooseTag"));
    edm::EDGetTokenT<edm::ValueMap<Bool_t> > phoIdMediumToken = 
                 consumes<edm::ValueMap<Bool_t> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("phoIdMediumTag"));
    edm::EDGetTokenT<edm::ValueMap<Bool_t> > phoIdTightToken = 
                 consumes<edm::ValueMap<Bool_t> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("phoIdTightTag"));

    edm::EDGetTokenT<edm::View<pat::Jet> > jetToken  = 
                 consumes<edm::View<pat::Jet> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("jetTag"));
    edm::EDGetTokenT<edm::View<pat::Jet> > fjetToken = 
                 consumes<edm::View<pat::Jet> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("fatjetTag"));
    edm::EDGetTokenT<edm::View<pat::MET> > metToken  = 
                 consumes<edm::View<pat::MET> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("metTag"));
    edm::EDGetTokenT<edm::TriggerResults> trigToken = 
                 consumes<edm::TriggerResults>(
                 iConfig.getUntrackedParameter<edm::InputTag>("triggerTag"));

    edm::EDGetTokenT<std::vector<reco::GenParticle> > genToken = 
                 consumes<std::vector<reco::GenParticle> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("genParticleTag"));

    edm::EDGetTokenT<reco::BeamSpot> beamSpotToken = 
                 consumes<reco::BeamSpot>(
                 iConfig.getUntrackedParameter<edm::InputTag>("beamSpotTag"));
    edm::EDGetTokenT<reco::ConversionCollection> conversionsToken = 
                 consumes<reco::ConversionCollection>(
                 iConfig.getUntrackedParameter<edm::InputTag>("conversionsTag"));
    edm::EDGetTokenT<std::vector<reco::Vertex> > verticesToken = 
                 consumes<std::vector<reco::Vertex> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("verticesTag"));
    edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puToken = 
                 consumes<std::vector<PileupSummaryInfo> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("puTag"));
    edm::EDGetTokenT<GenEventInfoProduct> generatorToken = 
                 consumes<GenEventInfoProduct>(
                 iConfig.getUntrackedParameter<edm::InputTag>("generatorTag"));
    edm::EDGetTokenT<double> rhoToken = 
                 consumes<double>(
                 iConfig.getUntrackedParameter<edm::InputTag>("rhoTag"));
    edm::EDGetTokenT<LHEEventProduct> lheEventToken = 
                 consumes<LHEEventProduct>(
                 iConfig.getUntrackedParameter<edm::InputTag>("lheEventTag"));
    edm::EDGetTokenT<LHERunInfoProduct> lheRunToken = 
                 consumes<LHERunInfoProduct, edm::InRun>(
                 iConfig.getUntrackedParameter<edm::InputTag>("lheRunTag"));


    int electronDetail = iConfig.getUntrackedParameter<int>("electronDetailLevel"); 
    int muonDetail = iConfig.getUntrackedParameter<int>("muonDetailLevel"); 
    int photonDetail = iConfig.getUntrackedParameter<int>("photonDetailLevel"); 
    int jetDetail = iConfig.getUntrackedParameter<int>("jetDetailLevel"); 

    _eventProducer.initialize( verticesToken, puToken, 
                               generatorToken, lheEventToken, lheRunToken,
                               rhoToken, _myTree, _infoTree );
    _elecProducer.initialize( "el"       , elecToken, _myTree, electronDetail );
    _muonProducer.initialize( "mu"       , muonToken, _myTree, muonDetail );
    _photProducer.initialize( "ph"       , photToken, _myTree, photonDetail );
    _jetProducer .initialize( "jet"      , jetToken , _myTree, jetDetail );
    _fjetProducer.initialize( "fjet"     , fjetToken, _myTree );
    _metProducer .initialize( "met"      , metToken , _myTree );
    _trigProducer.initialize( "passTrig" , trigToken, _myTree );
    _genProducer.initialize( "gen"       , genToken, _myTree );

    _photProducer.addUserFloat( PhotonChIso        , phoChIsoToken );
    _photProducer.addUserFloat( PhotonNeuIso       , phoNeuIsoToken );
    _photProducer.addUserFloat( PhotonPhoIso       , phoPhoIsoToken );
    _photProducer.addUserBool( PhotonVIDLoose      , phoIdLooseToken );
    _photProducer.addUserBool( PhotonVIDMedium     , phoIdMediumToken );
    _photProducer.addUserBool( PhotonVIDTight      , phoIdTightToken );

    _photProducer.addElectronsToken( elecToken );
    _photProducer.addConversionsToken( conversionsToken );
    _photProducer.addBeamSpotToken( beamSpotToken );

    _elecProducer.addUserBool( ElectronIdVeryLoose , elecIdVeryLooseToken);
    _elecProducer.addUserBool( ElectronIdLoose     , elecIdLooseToken);
    _elecProducer.addUserBool( ElectronIdMedium    , elecIdMediumToken);
    _elecProducer.addUserBool( ElectronIdTight     , elecIdTightToken);
    _elecProducer.addUserBool( ElectronIdHLT       , elecIdHLTToken);
    _elecProducer.addUserBool( ElectronIdHEEP      , elecIdHEEPToken);

    _elecProducer.addConversionsToken( conversionsToken );
    _elecProducer.addBeamSpotToken( beamSpotToken );
    _elecProducer.addVertexToken( verticesToken );
    _elecProducer.addRhoToken( rhoToken );

    _muonProducer.addVertexToken( verticesToken );
    _muonProducer.addRhoToken( rhoToken );
}

void UMDNTuple::beginJob() {


}

void UMDNTuple::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) {

    _eventProducer.produce( iEvent );
    _elecProducer.produce( iEvent );
    _muonProducer.produce( iEvent );
    _photProducer.produce( iEvent );
    _jetProducer .produce( iEvent );
    _fjetProducer.produce( iEvent );
    _metProducer .produce( iEvent );

    _trigProducer.produce( iEvent );

    _genProducer.produce( iEvent );

    _myTree->Fill();

}

void UMDNTuple::endJob() {

    //_myTree->Write();

}

void UMDNTuple::endRun( edm::Run const& iRun, edm::EventSetup const&) {

  _eventProducer.endRun( iRun );


}

UMDNTuple::~UMDNTuple() {

};


DEFINE_FWK_MODULE(UMDNTuple);
