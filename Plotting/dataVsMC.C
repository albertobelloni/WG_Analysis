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

void dataVsMC()
{ // beginning
  
  TString closprefix("closure_");
  TString nonclosprefix("wjets_");
  
  TString middle("mu_EB_");
  TString suffix("base");
  
  TString plot_var("mt_fulltrans_");
  
  TFile* file = new TFile("Plots/Resonance/Plots_2018_05_28/WJetsWS/outfile_workspace_wjets.root","READ");
  
  // get histograms
  
  TString dataprefix("Data_");
  TString wjetsprefix("WjetsSMP_");
  TString wgamprefix("Wgamma_");
  TString ttbarprefix("TTbar_SingleLep_");
  TString elefakeprefix("EleFakeBackground_");
  
  vector<TString> sampleprefix;
  //sampleprefix.push_back(wjetsprefix);
  //sampleprefix.push_back(wgamprefix);
  //sampleprefix.push_back(ttbarprefix);
  sampleprefix.push_back(wjetsprefix);
  sampleprefix.push_back(wgamprefix);
  sampleprefix.push_back(ttbarprefix);
  sampleprefix.push_back(elefakeprefix);

  vector<Color_t> colorsMC;
  colorsMC.push_back(kRed);
  colorsMC.push_back(kBlue);
  colorsMC.push_back(kGreen);
  colorsMC.push_back(kOrange);
  
  
  TString shapehistprefix("shapehist_");
  TString numhistprefix("numhist_");
  TString denhistprefix("denhist_");
  
  THStack* shape_DataVsMC = new THStack("dataVsMC_shape","dataVsMC_shape");
  THStack* num_DataVsMC = new THStack("dataVsMC_num","dataVsMC_num");
  THStack* den_DataVsMC = new THStack("dataVsMC_den","dataVsMC_den");
  
  // get data histograms
  TString datashapename = dataprefix + shapehistprefix + nonclosprefix + middle + plot_var + suffix;
  TString datanumname = dataprefix + numhistprefix + nonclosprefix + middle + plot_var + suffix;
  TString datadenname = dataprefix + denhistprefix + nonclosprefix + middle + plot_var + suffix;
  
  TH1F* data_shape_hist = static_cast<TH1F*>(file->Get(datashapename)->Clone());
  TH1F* data_num_hist = static_cast<TH1F*>(file->Get(datanumname)->Clone());
  TH1F* data_den_hist = static_cast<TH1F*>(file->Get(datadenname)->Clone());
  
  data_shape_hist->Rebin(4);
  data_num_hist->Rebin(4);
  data_den_hist->Rebin(4);

  double data_shape_norm = data_shape_hist->Integral(); // 14905
  double data_num_norm = data_num_hist->Integral(); // 6883
  double data_den_norm = data_den_hist->Integral(); //19471

  // legend
  TLegend* leg_shape = new TLegend(0.4,0.5,0.8,0.9);
  TLegend* leg_num = new TLegend(0.4,0.5,0.8,0.9);
  TLegend* leg_den = new TLegend(0.4,0.5,0.8,0.9);
  leg_shape->AddEntry(data_shape_hist, "Data", "l");
  leg_num->AddEntry(data_num_hist, "Data", "l");
  leg_den->AddEntry(data_den_hist, "Data", "l");
  
  
  // for calculating total MC
  TString first_shape = sampleprefix.at(0) + shapehistprefix + closprefix + middle + plot_var + suffix;
  TString first_num = sampleprefix.at(0) + numhistprefix + closprefix + middle + plot_var + suffix;
  TString first_den = sampleprefix.at(0) + denhistprefix + closprefix + middle + plot_var + suffix;

  TH1F* shape_MCTotal = static_cast<TH1F*>(file->Get(first_shape)->Clone());
  TH1F* num_MCTotal = static_cast<TH1F*>(file->Get(first_num)->Clone());
  TH1F* den_MCTotal = static_cast<TH1F*>(file->Get(first_den)->Clone());

  shape_MCTotal->Rebin(4);
  num_MCTotal->Rebin(4);
  den_MCTotal->Rebin(4);
  

  double s_normfactor = 14905./12701.3;
  double n_normfactor = 6883./3611.99;
  double d_normfactor = 19471./13352.9;


  for (unsigned int i = 0; i < sampleprefix.size(); i++)
    { // loop over MC samples
      
      TString shapename = sampleprefix.at(i) + shapehistprefix + closprefix + middle + plot_var + suffix;
      TString numname = sampleprefix.at(i) + numhistprefix + closprefix + middle + plot_var + suffix;
      TString denname = sampleprefix.at(i) + denhistprefix + closprefix + middle + plot_var + suffix;
      
      
      TH1F* shape_hist = static_cast<TH1F*>(file->Get(shapename)->Clone());
      TH1F* num_hist = static_cast<TH1F*>(file->Get(numname)->Clone());
      TH1F* den_hist = static_cast<TH1F*>(file->Get(denname)->Clone());

      shape_hist->Rebin(4);
      num_hist->Rebin(4);
      den_hist->Rebin(4);

      if (i != 0)
	{
	  shape_MCTotal->Add(shape_hist);
	  num_MCTotal->Add(num_hist);
	  den_MCTotal->Add(den_hist);
	}

      shape_hist->Scale(s_normfactor);
      num_hist->Scale(n_normfactor);
      den_hist->Scale(d_normfactor);

      shape_hist->SetFillStyle(1001);
      num_hist->SetFillStyle(1001);
      den_hist->SetFillStyle(1001);

      shape_hist->SetFillColor(colorsMC.at(i));
      num_hist->SetFillColor(colorsMC.at(i));
      den_hist->SetFillColor(colorsMC.at(i));

      shape_hist->SetLineColor(colorsMC.at(i));
      num_hist->SetLineColor(colorsMC.at(i));
      den_hist->SetLineColor(colorsMC.at(i));

      shape_hist->SetMarkerColor(colorsMC.at(i));
      num_hist->SetMarkerColor(colorsMC.at(i));
      den_hist->SetMarkerColor(colorsMC.at(i));

      shape_DataVsMC->Add(shape_hist);
      num_DataVsMC->Add(num_hist);
      den_DataVsMC->Add(den_hist);

      leg_shape->AddEntry(shape_hist,sampleprefix.at(i),"lp");
      leg_num->AddEntry(num_hist,sampleprefix.at(i),"lp");
      leg_den->AddEntry(den_hist,sampleprefix.at(i),"lp");

    } // loop over MC samples

  double MC_shape_norm = shape_MCTotal->Integral(); // 12701.3
  double MC_num_norm = num_MCTotal->Integral(); // 3611.99
  double MC_den_norm = den_MCTotal->Integral(); // 13352.9

  shape_MCTotal->Scale(s_normfactor);
  num_MCTotal->Scale(n_normfactor);
  den_MCTotal->Scale(d_normfactor);


  cout << "Getting normalization..." << endl;
  cout << "data shape events = " << data_shape_norm << " and MC shape events = " << MC_shape_norm << endl;
  cout << "data num events = " << data_num_norm << " and MC num events = " << MC_num_norm << endl;
  cout << "data den events = " << data_den_norm << " and MC den events = " << MC_den_norm << endl;
  cout << "shape normalization = " << data_shape_norm/MC_shape_norm << endl;
  cout << "num normalization = " << data_num_norm/MC_num_norm << endl;
  cout << "den normalization = " << data_den_norm/MC_den_norm << endl;


  TH1F* ratio_shape = static_cast<TH1F*>(data_shape_hist->Clone());
  TH1F* ratio_num = static_cast<TH1F*>(data_num_hist->Clone());
  TH1F* ratio_den = static_cast<TH1F*>(data_den_hist->Clone());

  ratio_shape->Add(shape_MCTotal,-1.);
  ratio_num->Add(num_MCTotal,-1.);
  ratio_den->Add(den_MCTotal,-1.);

  ratio_shape->Divide(data_shape_hist);
  ratio_num->Divide(data_num_hist);
  ratio_den->Divide(data_den_hist);

  ratio_shape->GetYaxis()->SetTitle("(Data-MC)/Data");
  ratio_num->GetYaxis()->SetTitle("(Data-MC)/Data");
  ratio_den->GetYaxis()->SetTitle("(Data-MC)/Data");
  ratio_shape->GetYaxis()->SetRangeUser(-1.5,1.5);
  ratio_num->GetYaxis()->SetRangeUser(-1.5,1.5);
  ratio_den->GetYaxis()->SetRangeUser(-1.5,1.5);

  TCanvas* canv_s = new TCanvas("dataVsMC_canv_shape", "dataVsMC_canv_shape", 600, 600);
  canv_s->cd();
  canv_s->Divide(1,2);
  canv_s->cd(1)->SetPad(0.0,0.33,1.0,1.0);
  canv_s->cd(2)->SetPad(0.0,0.0,1.0,0.33);
  canv_s->cd(1);
  shape_DataVsMC->Draw("hist");
  data_shape_hist->Draw("LPE same");
  leg_shape->Draw();
  canv_s->cd(2);
  ratio_shape->Draw();
  
  TCanvas* canv_n = new TCanvas("dataVsMC_canv_num", "dataVsMC_canv_num", 600, 600);
  canv_n->cd();
  canv_n->Divide(1,2);
  canv_n->cd(1)->SetPad(0.0,0.33,1.0,1.0);
  canv_n->cd(2)->SetPad(0.0,0.0,1.0,0.33);
  canv_n->cd(1);
  num_DataVsMC->Draw("hist");
  data_num_hist->Draw("LPE same");
  leg_num->Draw();
  canv_n->cd(2);
  ratio_num->Draw();
  
  TCanvas* canv_d = new TCanvas("dataVsMC_canv_den", "dataVsMC_canv_den", 600, 600);
  canv_d->cd();
  canv_d->Divide(1,2);
  canv_d->cd(1)->SetPad(0.0,0.33,1.0,1.0);
  canv_d->cd(2)->SetPad(0.0,0.0,1.0,0.33);
  canv_d->cd(1);
  den_DataVsMC->Draw("hist");
  data_den_hist->Draw("LPE same");
  leg_den->Draw();
  canv_d->cd(2);
  ratio_den->Draw();

} // end
