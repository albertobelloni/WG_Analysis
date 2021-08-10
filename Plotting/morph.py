
import ROOT
from ROOT import gROOT, gSystem, RooIntegralMorph
from ROOT import RooRealVar, RooDataHist,RooAbsReal
from ROOT import RooFit as rf
from uncertainties import ufloat
import uuid
import re
import random
import sys
from collections import namedtuple, OrderedDict
from functools import wraps
from DrawConfig import DrawConfig
gSystem.Load("My_double_CB/RooDoubleCB_cc.so")


inputDir = "/data/users/yihuilai/WG_Analysis/Plotting/data/sigfit/2018/"
outputDir = "./"


def extrapolate_ws( ws1, ws2 , massLow=0, massHigh=1000, targetMass=500):
    """ extrapolate signal """

    ifile1 = ROOT.TFile.Open( inputDir+ws1+'.root', 'READ' )
    ifile2 = ROOT.TFile.Open( inputDir+ws2+'.root', 'READ' )
    if not ifile1 or not ifile2:
       print "skipping ", ws1+'.root', ws2+'.root' 
       exit()
    ws_in1 = ifile1.Get( ws1 )
    ws_in2 = ifile2.Get( ws2 )
    ws_outname = ws1.replace("M"+str(massLow), "M"+str(targetMass))
    ws_out = ROOT.RooWorkspace( ws_outname )
    print("extrapolate ", ws_outname ," from ", ws1, ws2)
    sigModel={}
    
    for ipdf1, ipdf2 in zip(ws_in1.allPdfs(),ws_in2.allPdfs()):
        print('pdf:', ipdf1.GetName(), ipdf2.GetName())
        #continue
        mAlpha = 1.0 - float(targetMass-massLow)/float(massHigh-massLow)
        alpha_morph = RooRealVar("alpha_morph", "#alpha_{morph}", mAlpha, 0., 1.)
        alpha_morph.setBins(10,"cache") ;
        va = RooRealVar("mt_res", "mt_res", ws_in1.var("mt_res").getMin(), ws_in2.var("mt_res").getMax())
        pdf_name = ipdf1.GetName().replace("M"+str(massLow), "M"+str(targetMass))
        print("new pdf", pdf_name)
        sigModel[pdf_name] = RooIntegralMorph(pdf_name, pdf_name, ipdf1, ipdf2 , va, alpha_morph)
        getattr( ws_out, "import" ) ( sigModel[pdf_name] )
        outputfile = outputDir+ws_outname+".root"
        debug = False #True
        if (debug):
            from ROOT import gPad, RooFit, kRed, kBlue, kViolet
            c=ROOT.TCanvas()
            frame = va.frame()
            ipdf1.plotOn(frame, RooFit.LineColor(kRed+1),RooFit.LineStyle(2))
            ipdf2.plotOn(frame, RooFit.LineColor(kBlue+1),RooFit.LineStyle(2))
            sigModel[pdf_name].plotOn(frame, RooFit.LineColor(kViolet+1),RooFit.LineStyle(9))
            frame.Draw()
            c.SaveAs(pdf_name+'.pdf')
    ws_out.writeToFile( outputfile )


wsname1 = 'wssignal_M300_W5_el'
wsname2 = 'wssignal_M350_W5_el'
extrapolate_ws(wsname1, wsname2, 300, 350, 325)

exit()


#allData()
#allPdfs()
#allVars()




