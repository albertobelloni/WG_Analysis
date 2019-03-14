#include <iostream>
#include <fstream>
#include <cmath>
#include "TH1F.h"
#include "TH1.h"
#include "TString.h"
#include "TCanvas.h"
#include "TF1.h"
#include "THStack.h"
using namespace std;

void theMatrix()
{ // beginning
  
  TString datasuffix("data_mu_EB_base");
  TString mcsuffix("mc_mu_EB_base");
  
  TString plot_var("sigmaIEIE_");
  //TString plot_var("chIso_");
  //TString plot_var("phpt_");
  
  TFile* file = new TFile("Plots/Resonance/Plots_2018_10_16/WJetsWS/outfile_matrix_workspace_wjets.root","READ");

  // get histograms
  
  TString dataprefix("Data_");
  TString zjetsprefix("Z+jets_");
  TString zgamprefix("Zgamma_");
  
  vector<TString> sampleprefix;
  sampleprefix.push_back(zjetsprefix);
  sampleprefix.push_back(zgamprefix);

  vector<Color_t> colorsMC;
  colorsMC.push_back(kCyan);
  colorsMC.push_back(kOrange);
  
  
  //TString selprefix("B_");
  TString selprefix("C_");
  //TString selprefix("Al_");
  //TString selprefix("Am_");
  //TString selprefix("A_");
  //TString selprefix("incl_");
  
  
  // get data histogram
  TString datahistname = dataprefix + plot_var + selprefix + datasuffix;
  TH1F* data_hist = static_cast<TH1F*>(file->Get(datahistname)->Clone());
  //data_hist->Rebin(5);

  // legend
  TLegend* leg = new TLegend(0.4,0.5,0.8,0.9);
  leg->AddEntry(data_hist, "Data", "l");

  // get MC histograms
  THStack* stackMC = new THStack("MCstack", "MCstack");
  TString name = sampleprefix.at(0) + plot_var + selprefix + mcsuffix;
  cout << name << endl;
  TH1F* totalMC_hist = static_cast<TH1F*>(file->Get(name)->Clone());
  //totalMC_hist->Rebin(5);

  for (unsigned int i = 0; i < sampleprefix.size(); i++)
    { // loop over MC samples
      TString histname_mc = sampleprefix.at(i) + plot_var + selprefix + mcsuffix;
      TH1F* stack_hist = static_cast<TH1F*>(file->Get(histname_mc)->Clone());
      //stack_hist->Rebin(5);
      if (i != 0)
	totalMC_hist->Add(stack_hist);
      stackMC->Add(stack_hist);
      stack_hist->SetFillStyle(1001);
      stack_hist->SetFillColor(colorsMC.at(i));
      stack_hist->SetLineColor(colorsMC.at(i));
      stack_hist->SetMarkerColor(colorsMC.at(i));
      leg->AddEntry(stack_hist,sampleprefix.at(i),"lp");
    } // loop over MC samples

  cout << "Total number of data events = " << data_hist->Integral() << endl;
  cout << "Total number of MC events = " << totalMC_hist->Integral() << endl;

  TH1F* ratio_hist = static_cast<TH1F*>(data_hist->Clone());
  ratio_hist->Divide(totalMC_hist);
  ratio_hist->GetYaxis()->SetTitle("Data/MC");
  ratio_hist->GetYaxis()->SetRangeUser(0.,3.);

  TCanvas* canv = new TCanvas("dataVsMC_canv", "dataVsMC_canv", 600, 600);
  canv->cd();
  canv->Divide(1,2);
  canv->cd(1)->SetPad(0.0,0.33,1.0,1.0);
  canv->cd(2)->SetPad(0.0,0.0,1.0,0.33);
  canv->cd(1);
  stackMC->Draw("hist");
  data_hist->Draw("LPE same");
  leg->Draw();
  canv->cd(2);
  ratio_hist->Draw();  

} // end
