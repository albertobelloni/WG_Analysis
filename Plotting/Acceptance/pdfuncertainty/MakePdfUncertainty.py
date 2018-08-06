import os
import re
import uuid
from SampleManager import SampleManager
import ROOT
import sys
sys.path.append('/data/users/fengyb/CMSPLOTS')
from Plotter.myFunction import DrawGraphs

_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = '/data/users/fengyb/WGToLNuG/WG_Analysis/Plotting/cross_sections/photon15.py'
_LUMI     = 36000
_SAMPCONF = '/data/users/fengyb/WGToLNuG/WG_Analysis/Plotting/Modules/Resonance.py'

ROOT.gROOT.SetBatch(True)

def main():

    BaseDir = "/data/users/fengyb/WGammaNtuple/SigNoFilt_2018_05_11"
    sampManNoFilt = SampleManager( BaseDir, _TREENAME, filename=_FILENAME, quiet=True)
    sampManNoFilt.ReadSamples( _SAMPCONF )

    GColor = {}
    GColor["0p01"]  = 2
    GColor["5"]     = 3

    GMStyle = {}
    GMStyle["0p01"] = 21
    GMStyle["5"]    = 22

    gerr = {}
    for ichan in ["muon", "electron"]:
        gerr[ichan] = {}
        for iwidth in ["5", "0p01"]:
            gerr[ichan][iwidth] = ROOT.TGraphErrors( 40 )
            gerr[ichan][iwidth].SetName( "pdf_uncertainty_%s_width%s"%(ichan, iwidth))
            gerr[ichan][iwidth].SetTitle( "pdf_uncertainty_%s_width%s"%(ichan, iwidth))
            print gerr[ichan][iwidth].GetName()

    ipoint = 0

    for samp in sampManNoFilt.get_samples() :

        print 'Sample = ', samp.name

        #res = re.match( '(MadGraph|Pythia)ResonanceMass(\d+)_width(\d+)', samp.name )
        res = re.match( 'MadGraphResonanceMass(\d+)_width(\d+)', samp.name)

        if res is not None :

            mass  = int(res.group(1))
            if samp.name.count( 'width0p01' ):
               width = "0p01"
            else:
               width  = "5"
             
            print width, mass

            PdfRootFile = "/data/users/fengyb/WGToLNuG/WG_Analysis/Plotting/Acceptance/pdfuncertainty/root"

            ifile = ROOT.TFile("%s/pdf_%s.root"%(PdfRootFile, samp.name))

            for ichan in ["muon", "electron"]:
                (accpt, unc) = GetPdfUncertainty( ifile, "hacceptance_%s"%ichan, samp.name)
                gerr[ichan][width].SetPoint( ipoint, mass, unc/accpt )
                gerr[ichan][width].SetPointError( ipoint, 0.,   0. )
                print accpt, unc, unc/accpt

            ipoint += 1
            ifile.Close()


    ofile = ROOT.TFile.Open( "pdfuncertainty.root", 'RECREATE')

    for ichan in ["muon", "electron"]:
        for iwidth in ["5", "0p01"]:
            gerr[ichan][iwidth].SetLineColor(int(GColor[iwidth]))
            gerr[ichan][iwidth].SetMarkerColor(int(GColor[iwidth]))
            gerr[ichan][iwidth].SetMarkerStyle(int(GMStyle[iwidth]))
            gerr[ichan][iwidth].SetMarkerSize(1)
            print gerr[ichan][iwidth].GetName()
            #gerr[ichan][width].SetDirectory(ofile)
            gerr[ichan][iwidth].Write()    

    DrawGraphs([gerr["muon"]["0p01"], gerr["muon"]["5"]], ["muon width0p01", "muon width5"], 100, 4500, "gen_mass", 0, 0.08, "p.d.f uncertainty", "pdf_uncertainty_pythia_muon", dology = False)
    DrawGraphs([gerr["electron"]["0p01"], gerr["electron"]["5"]], ["electron width0p01", "electron width5"], 100, 4500, "gen_mass", 0, 0.08, "p.d.f uncertainty", "pdf_uncertainty_pythia_electron", dology = False)


def GetPdfUncertainty( rootfile, histoname, sampname) :

    ## Get the smeared acceptance distribution
    haccpt = rootfile.Get( histoname )
    mean_mu = haccpt.GetMean()
    std_mu =  haccpt.GetRMS()

    haccpt.Rebin(4)
    haccpt.GetXaxis().SetRangeUser( mean_mu - 4* std_mu, mean_mu + 4 * std_mu )

    haccpt.Fit("gaus")
    fgaus = haccpt.GetFunction("gaus")

    uid = str(uuid.uuid4())
    can = ROOT.TCanvas( uid, '', 500, 500)
    haccpt.SetTitle("%s_%s"%(haccpt.GetTitle(), sampname))
    haccpt.Draw()

    print " printing histogram"
    can.Print("plots/%s_%s.pdf"%(histoname, sampname))
    print " finished printing histogram"

    return ( fgaus.GetParameter(1), fgaus.GetParameter(2) )
    

main()
