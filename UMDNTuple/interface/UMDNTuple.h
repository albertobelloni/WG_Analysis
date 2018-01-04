#ifndef UMDNTUPLE_H
#define UMDNTUPLE_H
#include <vector>
#include <string>
#include "TTree.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include "UMDNTuple/UMDNTuple/interface/EventInfoProducer.h"
#include "UMDNTuple/UMDNTuple/interface/ElectronProducer.h"
#include "UMDNTuple/UMDNTuple/interface/GenParticleProducer.h"
#include "UMDNTuple/UMDNTuple/interface/MuonProducer.h"
#include "UMDNTuple/UMDNTuple/interface/PhotonProducer.h"
#include "UMDNTuple/UMDNTuple/interface/JetProducer.h"
#include "UMDNTuple/UMDNTuple/interface/FatJetProducer.h"
#include "UMDNTuple/UMDNTuple/interface/METProducer.h"
#include "UMDNTuple/UMDNTuple/interface/TriggerProducer.h"


class UMDNTuple : public edm::EDAnalyzer {

public:
  /// default constructor
  explicit UMDNTuple(const edm::ParameterSet&);
  /// default destructor
  ~UMDNTuple(); 

private:
  /// everything that needs to be done before the event loop
  virtual void beginJob() ;
  /// everything that needs to be done during the event loop
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  /// everything that needs to be done after the event loop

  virtual void endJob();

  virtual void endRun(edm::Run const& iRun, edm::EventSetup const&);

  
private :
  
  TTree *_myTree;
  TTree *_weightInfoTree;
  TTree *_trigInfoTree;

  EventInfoProducer  _eventProducer;
  GenParticleProducer  _genProducer;
  ElectronProducer _elecProducer;
  MuonProducer     _muonProducer;
  PhotonProducer   _photProducer;
  JetProducer      _jetProducer;
  FatJetProducer   _fjetProducer;
  METProducer      _metProducer;
  TriggerProducer  _trigProducer;
  
  bool _produceEvent;
  bool _produceElecs;
  bool _produceMuons;
  bool _producePhots;
  bool _produceJets;
  bool _produceFJets;
  bool _produceMET;
  bool _produceTrig;
  bool _produceGen;

  int _isMC;

};
#endif
