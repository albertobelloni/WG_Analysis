#include <iostream>
#include <fstream>
#include <cmath>
#include "TH1F.h"
#include "TH1.h"
#include "TString.h"
#include "TCanvas.h"
#include "TF1.h"
#include "THStack.h"
#include "TString.h"
using namespace std;

void kplotter()
{ // beginning

  TString infilename("Plots/Resonance/Plots_2018_09_11/WJetsWS/outfile_kfactor.root");
  TFile* infile = new TFile(infilename,"READ");

  TString dataprefix("Data_");
  TString wjetsprefix("WjetsSMPIncl_");
  //TString wjetsprefix("WjetsSMPPt_");
  //TString wjetsprefix("WjetsSMPJet_");
  //TString wjetsprefix("Wjets_");
  TString wgamprefix("Wgamma_");
  TString ttbarprefix("TTbar_SingleLep_");
  TString elefakeprefix("EleFakeBackground_");

  vector<TString> sampleprefix;
  sampleprefix.push_back(wjetsprefix);
  sampleprefix.push_back(wgamprefix);
  sampleprefix.push_back(ttbarprefix);
  sampleprefix.push_back(elefakeprefix);

  //TString histsuffix("wpt_wjets_mu");
  //TString histsuffix("wmass_wjets_mu");
  //TString histsuffix("leadjetpt_wjets_mu");
  //TString histsuffix("mtmumet_wjets_mu");
  TString histsuffix("jetn_wjets_mu");


  vector<Color_t> colorsMC;
  colorsMC.push_back(kRed);
  colorsMC.push_back(kBlue);
  colorsMC.push_back(kGreen);
  colorsMC.push_back(kOrange);

  // get data histogram
  TString histname_data = dataprefix + histsuffix;
  cout << histname_data << endl;
  TH1F* histdata = static_cast<TH1F*>(infile->Get(histname_data)->Clone());
  //histdata->GetXaxis()->SetTitle("Reco W p_{T} (GeV)");
  //histdata->GetXaxis()->SetTitle("Reco W mass (GeV)");
  //histdata->GetXaxis()->SetTitle("Leading jet p_{T} (GeV)");
  //histdata->GetXaxis()->SetTitle("m_{T}(#mu,MET) (GeV)");
  histdata->GetXaxis()->SetTitle("Jet multiplicity");
  histdata->GetYaxis()->SetTitle("Events");

  // define legend
  TLegend* leg = new TLegend(0.4,0.5,0.8,0.9);
  leg->AddEntry(histdata, "Data", "l");

  // get MC histograms
  TString firstname = sampleprefix.at(0) + histsuffix;
  TH1F* histmc = static_cast<TH1F*>(infile->Get(firstname)->Clone());
  cout << "debug: first mc histo integral = " << histmc->Integral() << endl;
  THStack* stack_MC = new THStack("dataVsMC","dataVsMC");

  for (unsigned int i = 0; i < sampleprefix.size(); i++)
    { // loop over MC samples
      cout << "loop is at " << i << endl;
      TString histname_mc = sampleprefix.at(i) + histsuffix;
      TH1F* stack_hist = static_cast<TH1F*>(infile->Get(histname_mc)->Clone());
      if (i != 0)
	histmc->Add(stack_hist);

      stack_hist->SetFillStyle(1001);
      stack_hist->SetFillColor(colorsMC.at(i));
      stack_hist->SetLineColor(colorsMC.at(i));
      stack_hist->SetMarkerColor(colorsMC.at(i));
      stack_MC->Add(stack_hist);
      leg->AddEntry(stack_hist,sampleprefix.at(i),"lp");

   } // loop over MC samples

  cout << "Total data events: " << histdata->Integral() << endl;
  cout << "Total MC events: " << histmc->Integral();



  TH1F* histratio = static_cast<TH1F*>(infile->Get(histname_data)->Clone());
  histratio->Divide(histmc);
  //histratio->GetXaxis()->SetTitle("Reco W p_{T} (GeV)");
  //histratio->GetXaxis()->SetTitle("Reco W mass (GeV)");
  //histratio->GetXaxis()->SetTitle("Leading jet p_{T} (GeV)");
  //histratio->GetXaxis()->SetTitle("m_{T}(#mu,MET) (GeV)");
  histratio->GetXaxis()->SetTitle("Jet multiplicity");
  histratio->GetYaxis()->SetTitle("Data/MC");

  
  double kfactor = histdata->Integral()/histmc->Integral();
  cout << "k-factor = " << kfactor << endl;

  TCanvas* canv = new TCanvas("dataVsMC_kfactor","datavsMC_kfactor",600,600);
  canv->cd();
  canv->Divide(1,2);
  canv->cd(1)->SetPad(0.0,0.33,1.0,1.0);
  canv->cd(2)->SetPad(0.0,0.0,1.0,0.33);

  canv->cd(1);
  stack_MC->Draw("hist");
  histdata->Draw("LPE same");
  leg->Draw();
  canv->cd(2);
  histratio->Draw();

} // end
