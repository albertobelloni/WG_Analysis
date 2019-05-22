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
  
  TString datasuffix("data_EB");
  TString mcsuffix("mc_EB");
  
  //TString plot_var("sigmaIEIE_real_");
  //TString plot_var("chIso_real_");
  //TString plot_var("sigmaIEIE_FR_");
  //TString plot_var("chIso_FR_");
  //TString plot_var("mll_");
  //TString plot_var("dr_");
  TString plot_var("vtxn_");
  
  TFile* file = new TFile("Plots/Resonance/Plots_2019_04_19/WJetsWS/outfile_matrix_Pt15To25_workspace_wjets.root","READ");

  // get histograms
  
  TString dataprefix("Data_");
  TString zjetsprefix("Z+jets_");
  TString zgamprefix("Zgamma_");
  
  vector<TString> sampleprefix;
  sampleprefix.push_back(zjetsprefix);
  sampleprefix.push_back(zgamprefix);

  vector<Color_t> colorsMC;
  colorsMC.push_back(kBlue-7);
  colorsMC.push_back(kOrange);
  
  TString selprefix("FR_");
  
  
  // get data histogram
  TString datahistname = dataprefix + plot_var /*+ selprefix */+ datasuffix;
  TH1F* data_hist = static_cast<TH1F*>(file->Get(datahistname)->Clone());
  data_hist->GetXaxis()->SetTitle("Number of vertices");
  data_hist->GetYaxis()->SetTitle("Events");
  //data_hist->Rebin(5);
  //data_hist->GetXaxis()->SetRangeUser(0.,0.025)

  // legend
  TLegend* leg = new TLegend(0.4,0.5,0.8,0.9);
  leg->AddEntry(data_hist, "Data", "l");

  // get MC histograms
  THStack* stackMC = new THStack("MCstack", "MCstack");
  TString name = sampleprefix.at(0) + plot_var /*+ selprefix */+ mcsuffix;
  TH1F* totalMC_hist = static_cast<TH1F*>(file->Get(name)->Clone());
  
  for (unsigned int i = 0; i < sampleprefix.size(); i++)
    { // loop over MC samples
      TString histname_mc = sampleprefix.at(i) + plot_var + mcsuffix; //+ selprefix + mcsuffix
      TH1F* stack_hist = static_cast<TH1F*>(file->Get(histname_mc)->Clone());

      cout << histname_mc << ": " << stack_hist->Integral() << " events" << endl;
      if (i != 0)
	totalMC_hist->Add(stack_hist);
      stackMC->Add(stack_hist);
      stack_hist->SetFillStyle(1001);
      stack_hist->SetFillColor(colorsMC.at(i));
      stack_hist->SetLineColor(colorsMC.at(i));
      stack_hist->SetMarkerColor(colorsMC.at(i));
      leg->AddEntry(stack_hist,sampleprefix.at(i),"lp");
    } // loop over MC samples
 
  // total mc error bars
  totalMC_hist->SetFillStyle(3352);
  totalMC_hist->SetFillColor(kRed);

  Double_t ptr_errdata;
  Double_t ptr_errMC;
  double sumdata = 0.;
  double sumMC = 0.;
  sumdata += data_hist->IntegralAndError(1, data_hist->GetSize()-1,ptr_errdata);
  sumMC += totalMC_hist->IntegralAndError(1, totalMC_hist->GetSize()-1,ptr_errMC);
  cout << "Total data = " << sumdata << " +/- " << ptr_errdata << endl;
  cout << "Total MC = " << sumMC << " +/- " << ptr_errMC << endl;

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
  totalMC_hist->Draw("same e2");
  leg->Draw();
  canv->cd(2);
  ratio_hist->Draw();  

} // end
