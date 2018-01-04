#include "UMDNTuple/UMDNTuple/interface/EventInfoProducer.h"
#include "FWCore/Framework/interface/EDConsumerBase.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"

EventInfoProducer::EventInfoProducer(  ) : 
    isData(0),
    eventNumber(0),
    lumiSection(0),
    runNumber(0),
    bxNumber(0),
    vtx_n(0),
    pu_n(0),
    truepu_n(0),
    EventWeights(0),
    rho(0),
    _infoTree(0),
    _isMC(0)

{

}

void EventInfoProducer::initialize( 
                        const edm::EDGetTokenT<std::vector<reco::Vertex> > & vtxTok, 
                        const edm::EDGetTokenT<std::vector<PileupSummaryInfo> > & puTok,
                        const edm::EDGetTokenT<GenEventInfoProduct> & genTok,
                        const edm::EDGetTokenT<LHEEventProduct> & lheEventTok, 
                        const edm::EDGetTokenT<LHERunInfoProduct> & lheRunTok, 
                        const edm::EDGetTokenT<double> & rhoTok, 
                        TTree *tree, TTree *infoTree, bool isMC) {

    _vertexToken = vtxTok;
    _puToken = puTok;
    _generatorToken = genTok;
    _lheEventToken = lheEventTok;
    _lheRunToken = lheRunTok;
    _rhoToken = rhoTok;
    _isMC = isMC;


    tree -> Branch( "isData", &isData, "isData/O" );
    tree -> Branch( "eventNumber", &eventNumber, "eventNumber/I");
    tree -> Branch( "lumiSection", &lumiSection, "lumiSection/I");
    tree -> Branch( "runNumber", &runNumber, "runNumber/I");
    tree -> Branch( "bxNumber", &bxNumber, "bxNumber/I");
    tree -> Branch( "vtx_n", &vtx_n, "vtx_n/I");
    tree -> Branch( "pu_n", &pu_n, "pu_n/I");
    tree -> Branch( "rho", &rho, "rho/F");

    if( _isMC ) {
        tree -> Branch( "truepu_n", &truepu_n, "truepu_n/I");
        tree -> Branch( "EventWeights", &EventWeights);
        tree -> Branch( "pdf_id1", &pdf_id1, "pdf_id1/F");
        tree -> Branch( "pdf_id2", &pdf_id2, "pdf_id2/F");
        tree -> Branch( "pdf_x1", &pdf_x1, "pdf_x1/F");
        tree -> Branch( "pdf_x2", &pdf_x2, "pdf_x2/F");
        tree -> Branch( "pdf_scale", &pdf_scale, "pdf_scale/F");
    }

    _infoTree = infoTree;
}


void EventInfoProducer::produce(const edm::Event &iEvent ) {

    vtx_n = 0;
    pu_n = 0;

    if( _isMC ) {

        truepu_n = 0;

        pdf_id1 = 0;
        pdf_id2 = 0;
        pdf_x1 = 0;
        pdf_x2 = 0;
        pdf_scale = 0;
        EventWeights->clear();
    }

    edm::Handle<std::vector<reco::Vertex> > vertices_h;
    iEvent.getByToken(_vertexToken, vertices_h);


    edm::Handle<double>   rho_h;
    iEvent.getByToken(_rhoToken, rho_h);

    eventNumber      = iEvent.id().event();
    runNumber     = iEvent.id().run();
    lumiSection   = iEvent.luminosityBlock();
    bxNumber     = iEvent.bunchCrossing();
    isData      = iEvent.isRealData();


    for (std::vector<reco::Vertex>::const_iterator vtx = vertices_h->begin(); vtx != vertices_h->end(); ++vtx){
        if (vtx->isValid() && !vtx->isFake()) vtx_n++;
    }

    rho = (*rho_h);

    if( _isMC ) {
        edm::Handle<std::vector< PileupSummaryInfo > >  pileup_h;
        iEvent.getByToken(_puToken, pileup_h);

        edm::Handle<GenEventInfoProduct> generator_h;
        iEvent.getByToken(_generatorToken, generator_h);

        edm::Handle<LHEEventProduct>   lheevent_h;
        iEvent.getByToken(_lheEventToken, lheevent_h);

        std::vector<PileupSummaryInfo>::const_iterator PVI;
        float nputrue=-1.;
        float npu=-1.;

        for(std::vector<PileupSummaryInfo>::const_iterator pidx = pileup_h->begin(); 
                pidx != pileup_h->end(); ++pidx) {

          if( pidx->getBunchCrossing() == 0) {
              nputrue = pidx->getTrueNumInteractions();
              npu = pidx->getPU_NumInteractions();
          }
        }

        pu_n     = npu;
        truepu_n = nputrue;

        for(unsigned iw = 0; iw < lheevent_h->weights().size(); ++iw){
            EventWeights->push_back(lheevent_h->weights()[iw].wgt);
        }

        if (generator_h->pdf()) {
           pdf_id1 = generator_h->pdf()->id.first;
           pdf_id2 = generator_h->pdf()->id.second;
           pdf_x1 = generator_h->pdf()->x.first;
           pdf_x2 = generator_h->pdf()->x.second;
           pdf_scale = generator_h->pdf()->scalePDF;
        }
    }
  

}

void EventInfoProducer::endRun( const edm::Run & iRun ) {

    if( !_isMC ) return;

    edm::Handle<LHERunInfoProduct>   lherun_h;
    iRun.getByToken(_lheRunToken, lherun_h);
   
    std::vector<char*> descriptions;
    descriptions.push_back(new char[1024]);
    strcpy( descriptions.back(), "Null" );

    _infoTree->Branch("weightInfo",descriptions.back(), "weightInfo/C");
    for( std::vector<LHERunInfoProduct::Header>::const_iterator itr = lherun_h->headers_begin() ; itr != lherun_h->headers_end(); ++itr ) {

        std::string weight_group;
        if(  itr->tag() == "initrwgt" ) {
	    for(std::vector<std::string>::const_iterator it = itr->begin();
	        it != itr->end(); ++it){

                if( it->find( "weightgroup" ) != std::string::npos ) {
                    std::string::size_type type_pos = it->find( "type=" );
                    if( type_pos != std::string::npos ) {
                        std::string::size_type end_pos = it->find( ">" );
                        weight_group = it->substr( type_pos+6, end_pos - type_pos - 7 );
                    }
                }
                std::string::size_type weightid_pos = it->find( "weight id");
                if( weightid_pos != std::string::npos ) {
                    std::string::size_type idend = it->find_first_of( '>' );
                    std::string idnum = it->substr( weightid_pos+11, idend-weightid_pos-12 );
                    std::string::size_type nameend = it->find( "</weight>" );
                    std::string weightname = it->substr( idend +1, nameend-idend-1 );
                    strcpy(descriptions.back(),(weight_group + ":" + weightname).c_str( ));
                    _infoTree->Fill();
                }
            }
        }
    }

}
