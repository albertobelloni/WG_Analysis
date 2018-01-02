#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "UMDNTuple/UMDNTuple/interface/UMDNTuple.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

UMDNTuple::UMDNTuple( const edm::ParameterSet & iConfig ) :
    _produceEvent(true),
    _produceElecs(true),
    _produceMuons(true),
    _producePhots(true),
    _produceJets(true),
    _produceFJets(true),
    _produceGen(true),
    _isMC( -1 )
{
    edm::Service<TFileService> fs;

    // Create tree to store event data
    _myTree = fs->make<TTree>( "EventTree", "EventTree" );
    // Create tree to store metadata
    _infoTree = fs->make<TTree>( "InfoTree", "InfoTree" );

    // Get config flags
    if( !iConfig.exists( "isMC" ) ) {
        throw cms::Exception("CorruptData")
        << "Must provide isMC flag so we can handle the data/MC properly";
    }

    _isMC = iConfig.getUntrackedParameter<int>("isMC");

    // get the detail levels from the configuration
    int elecDetail = 99;
    int muonDetail = 99;
    int photDetail = 99;
    int jetDetail  = 99;
    if( iConfig.exists("electronDetailLevel") ) {  
        elecDetail = iConfig.getUntrackedParameter<int>("electronDetailLevel"); 
    }
    if( iConfig.exists("muonDetailLevel") ) {
        muonDetail   = iConfig.getUntrackedParameter<int>("muonDetailLevel"); 
    }
    if( iConfig.exists("photonDetailLevel") ) {
        photDetail = iConfig.getUntrackedParameter<int>("photonDetailLevel"); 
    }
    if( iConfig.exists("jetDetailLevel") ) {
        jetDetail    = iConfig.getUntrackedParameter<int>("jetDetailLevel"); 
    }

    // get pt cut from the configuration
    float elecMinPt = 0;
    float muonMinPt = 0;
    float photMinPt = 0;
    float jetMinPt  = 0;
    float fjetMinPt = 0;
    float genMinPt  = 0;

    if( iConfig.exists("electronMinPt") ) {
        elecMinPt = iConfig.getUntrackedParameter<double>("electronMinPt");
    }
    if( iConfig.exists("muonMinPt") ) {
        muonMinPt = iConfig.getUntrackedParameter<double>("muonMinPt");
    }
    if( iConfig.exists("photonMinPt") ) {
        photMinPt = iConfig.getUntrackedParameter<double>("photonMinPt");
    }
    if( iConfig.exists("jetMinPt") ) {
        jetMinPt  = iConfig.getUntrackedParameter<double>("jetMinPt");
    }
    if( iConfig.exists("fjetMinPt") ) {
        fjetMinPt = iConfig.getUntrackedParameter<double>("fjetMinPt");
    }
    if( iConfig.exists("genMinPt") ) {
        genMinPt  = iConfig.getUntrackedParameter<double>("genMinPt");
    }

    // prefix for object branches
    // defaults
    std::string prefix_el   = "el";
    std::string prefix_mu   = "mu";
    std::string prefix_ph   = "ph";
    std::string prefix_jet  = "jet";
    std::string prefix_fjet = "fjet";
    std::string prefix_trig = "passTrig";
    std::string prefix_gen  = "gen";
    std::string prefix_met  = "met";

    if( iConfig.exists(prefix_el) ) {
        prefix_el = iConfig.getUntrackedParameter<std::string>("prefix_el");
    }
    if( iConfig.exists(prefix_mu) ) {
        prefix_mu = iConfig.getUntrackedParameter<std::string>("prefix_mu");
    }
    if( iConfig.exists(prefix_ph) ) {
        prefix_ph = iConfig.getUntrackedParameter<std::string>("prefix_ph");
    }
    if( iConfig.exists(prefix_jet) ) {
        prefix_jet = iConfig.getUntrackedParameter<std::string>("prefix_jet");
    }
    if( iConfig.exists(prefix_fjet) ) {
        prefix_fjet = iConfig.getUntrackedParameter<std::string>("prefix_fjet");
    }
    if( iConfig.exists(prefix_trig) ) {
        prefix_trig = iConfig.getUntrackedParameter<std::string>("prefix_trig");
    }
    if( iConfig.exists(prefix_gen) ) {
        prefix_gen = iConfig.getUntrackedParameter<std::string>("prefix_gen");
    }
    if( iConfig.exists(prefix_met) ) {
        prefix_met = iConfig.getUntrackedParameter<std::string>("prefix_met");
    }


    edm::EDGetTokenT<reco::BeamSpot> beamSpotToken;
    edm::EDGetTokenT<reco::ConversionCollection> conversionsToken;
    edm::EDGetTokenT<std::vector<reco::Vertex> > verticesToken;
    edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puToken;
    edm::EDGetTokenT<GenEventInfoProduct> generatorToken;
    edm::EDGetTokenT<double> rhoToken;
    edm::EDGetTokenT<LHEEventProduct> lheEventToken;
    edm::EDGetTokenT<LHERunInfoProduct> lheRunToken;

    if( iConfig.exists("beamSpotTag" ) ) {
        beamSpotToken = consumes<reco::BeamSpot>(
                        iConfig.getUntrackedParameter<edm::InputTag>("beamSpotTag"));
    }
    if( iConfig.exists("conversionsTag") ) {
        conversionsToken = consumes<reco::ConversionCollection>(
                 iConfig.getUntrackedParameter<edm::InputTag>("conversionsTag"));
    }
    if( iConfig.exists("verticesTag") ) {
        verticesToken = consumes<std::vector<reco::Vertex> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("verticesTag"));
    }
    if( iConfig.exists("puTag") ) {
        puToken = consumes<std::vector<PileupSummaryInfo> >(
                 iConfig.getUntrackedParameter<edm::InputTag>("puTag"));
    }
    if( iConfig.exists("generatorTag") ) {
        generatorToken = consumes<GenEventInfoProduct>(
                 iConfig.getUntrackedParameter<edm::InputTag>("generatorTag"));
    }
    if( iConfig.exists("rhoTag") ) {
        rhoToken = consumes<double>(
                 iConfig.getUntrackedParameter<edm::InputTag>("rhoTag"));
    }
    if( iConfig.exists("lheEventTag") ) {
        lheEventToken = consumes<LHEEventProduct>(
                 iConfig.getUntrackedParameter<edm::InputTag>("lheEventTag"));
    }
    if( iConfig.exists("lheRunTag") ) {
        lheRunToken = consumes<LHERunInfoProduct, edm::InRun>(
                 iConfig.getUntrackedParameter<edm::InputTag>("lheRunTag"));
    }

    // flags to enable or disable production
    // of objects based on the provided tags
    _produceJets  = iConfig.exists( "jetTag" );
    _produceFJets = iConfig.exists( "fatjetTag" );
    _produceElecs = iConfig.exists( "electronTag" );
    _produceMuons = iConfig.exists( "muonTag" );
    _producePhots = iConfig.exists( "photonTag" );
    _produceMET   = iConfig.exists( "metTag" );
    _produceTrig  = iConfig.exists( "triggerTag" );
    _produceGen   = iConfig.exists( "genParticleTag" );

    if( !_isMC ) _produceGen = false;

    // delcare object tokens
    edm::EDGetTokenT<edm::View<pat::Jet> >            jetToken;
    edm::EDGetTokenT<edm::View<pat::Jet> >            fjetToken;
    edm::EDGetTokenT<edm::View<pat::Electron> >       elecToken;
    edm::EDGetTokenT<edm::View<pat::Muon> >           muonToken;
    edm::EDGetTokenT<edm::View<pat::Photon> >         photToken;
    edm::EDGetTokenT<edm::View<pat::MET> >            metToken;
    edm::EDGetTokenT<edm::TriggerResults>             trigToken;
    edm::EDGetTokenT<std::vector<reco::GenParticle> > genToken;


    // Event information
    _eventProducer.initialize( verticesToken, puToken, 
                               generatorToken, lheEventToken, lheRunToken,
                               rhoToken, _myTree, _infoTree, _isMC );

    // Electrons
    if( _produceElecs ) {
        elecToken =  consumes<edm::View<pat::Electron> >(
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

        _elecProducer.initialize( prefix_el  , elecToken, _myTree, elecMinPt, elecDetail );
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
    }

    if( _produceMuons ) { 

        muonToken = consumes<edm::View<pat::Muon> >(
                    iConfig.getUntrackedParameter<edm::InputTag>("muonTag"));

        _muonProducer.initialize( prefix_mu       , muonToken, _myTree, muonMinPt, muonDetail );
        _muonProducer.addVertexToken( verticesToken );
        _muonProducer.addRhoToken( rhoToken );
    }

    if( _producePhots ) {

        photToken = consumes<edm::View<pat::Photon> >(
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

        _photProducer.initialize( prefix_ph       , photToken, _myTree, photMinPt, photDetail );
        _photProducer.addUserFloat( PhotonChIso        , phoChIsoToken );
        _photProducer.addUserFloat( PhotonNeuIso       , phoNeuIsoToken );
        _photProducer.addUserFloat( PhotonPhoIso       , phoPhoIsoToken );
        _photProducer.addUserBool( PhotonVIDLoose      , phoIdLooseToken );
        _photProducer.addUserBool( PhotonVIDMedium     , phoIdMediumToken );
        _photProducer.addUserBool( PhotonVIDTight      , phoIdTightToken );

        _photProducer.addElectronsToken( elecToken );
        _photProducer.addConversionsToken( conversionsToken );
        _photProducer.addBeamSpotToken( beamSpotToken );
    }

    if( _produceJets ) {
        jetToken = consumes<edm::View<pat::Jet> >(
                   iConfig.getUntrackedParameter<edm::InputTag>("jetTag"));
        _jetProducer .initialize( prefix_jet   , jetToken , _myTree, jetMinPt, jetDetail );
    }

    if( _produceFJets ) {

        fjetToken =  consumes<edm::View<pat::Jet> >(
                     iConfig.getUntrackedParameter<edm::InputTag>("fatjetTag"));

        _fjetProducer.initialize( prefix_fjet     , fjetToken, _myTree, fjetMinPt );
    }

    if( _produceMET ) {
        metToken  = consumes<edm::View<pat::MET> >(
                    iConfig.getUntrackedParameter<edm::InputTag>("metTag"));

        _metProducer .initialize( prefix_met      , metToken , _myTree );
    }
    if( _produceTrig ) {
        trigToken = consumes<edm::TriggerResults>(
                    iConfig.getUntrackedParameter<edm::InputTag>("triggerTag"));

        _trigProducer.initialize( prefix_trig    , trigToken, _myTree );

    }
    if( _produceGen ) {
        genToken = consumes<std::vector<reco::GenParticle> >(
                   iConfig.getUntrackedParameter<edm::InputTag>("genParticleTag"));

        _genProducer.initialize( prefix_gen       , genToken, _myTree, genMinPt );
    }


}

void UMDNTuple::beginJob() {


}

void UMDNTuple::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) {

    _eventProducer.produce( iEvent );
    if( _produceElecs ) _elecProducer.produce( iEvent );
    if( _produceMuons ) _muonProducer.produce( iEvent );
    if( _producePhots ) _photProducer.produce( iEvent );
    if( _produceJets  ) _jetProducer .produce( iEvent );
    if( _produceFJets ) _fjetProducer.produce( iEvent );
    if( _produceMET   ) _metProducer .produce( iEvent );
    if( _produceTrig  ) _trigProducer.produce( iEvent );
    if( _produceGen   ) _genProducer .produce( iEvent );

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
