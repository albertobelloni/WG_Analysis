'''
 Make the cutflow table for muon and electron channels with specific mass and width
 Prepare the acceptance vs gen mass distribution and plot it
'''

import pickle
import math
from uncertainties import ufloat
import ROOT
import sys
sys.path.append('/data/users/fengyb/CMSPLOTS')
from Plotter.myFunction import DrawGraphs

ROOT.gROOT.SetBatch(True)

cut_efficiencies = pickle.load( open('acceptance.pickle', "rb"))

def main():
    width = 5
    mass = 1000
    # make cutflow tables for sample with mass and width
    MakeCutflow(width, mass, 'muon')
    MakeCutflow(width, mass, 'electron')

    # make the acceptance distribution, as a function of gen signal mass
    MakeAcceptance()
    PlotAcceptance()

def MakeCutflow(width, mass, channel):
    
    if channel == 'muon':
       tauchannel = 'taumu'
    elif channel == 'electron':
       tauchannel = 'tauel'
    
    outf = open('acceptance_%s.tex'%channel, "wb")
   
    print "\n\n\n"
    print channel
    outf.write("\n\n\n")
    outf.write("%% %s\n"%channel)
    
    ## look at the specific channel
    cut_count = cut_efficiencies[width][mass][channel]['counts']
    cut_efficiency = cut_efficiencies[width][mass][channel]['eff']
    cut_acceptance = cut_efficiencies[width][mass][channel]['effwithtau']
    for icut in cut_count[channel]:
        if icut!= 'denominator':
           print icut, cut_count[channel][icut], cut_efficiency[channel][icut]*100.0, cut_count[tauchannel][icut], cut_efficiency[tauchannel][icut]*100.0
           outf.write("%s & %d & %.2f $\pm$ %.2f & %d & %.2f $\pm$ %.2f \\\\ \n"%(icut, cut_count[channel][icut], cut_efficiency[channel][icut].n*100.0, cut_efficiency[channel][icut].s*100.0, cut_count[tauchannel][icut], cut_efficiency[tauchannel][icut].n*100.0, cut_efficiency[tauchannel][icut].s*100.0))
        else:
           print icut, cut_count[channel][icut], "-", cut_count[tauchannel][icut], "-"
           outf.write("Total & %d & \\multicolumn{1}{c}{-} & %d & \\multicolumn{1}{c}{-} \\\\ \n"%(cut_count[channel][icut], cut_count[tauchannel][icut]))
    
   
    print "\n\n\n" 
    outf.write("\n\n\n")
    
    # calculate the total acceptance
    acceptance = {}
    ntot_v = cut_count[channel]['denominator'] + cut_count[tauchannel]['denominator'] 
    outf.write("Total & %d & \\multicolumn{1}{c}{-} \\\\ \n"%ntot_v)
    for icut, icount in cut_count[channel].iteritems():
        if icut!= 'denominator':
           npass1_v = icount  
           npass2_v = cut_count[tauchannel][icut]
           npass_v = npass1_v + npass2_v
    
           nfail_v = ntot_v - npass_v
    
           npass = ufloat( npass_v, math.sqrt(npass_v ) )
           nfail = ufloat( nfail_v, math.sqrt(nfail_v ) )
       
           acceptance[icut]  = npass / ( npass + nfail)
           ## the value should be the same as cut_acceptance[channel][icut]
           print icut, ntot_v, npass_v, acceptance[icut], cut_acceptance[channel][icut]
           outf.write("%s & %d & %.2f $\pm$ %.2f \\\\ \n"%(icut, npass.n, acceptance[icut].n*100.0, acceptance[icut].s*100.0))
    
    outf.close()

def MakeAcceptance():
    channels = ['muon', 'electron']

    GColor = {}
    GColor["muon"]  = 2
    GColor["electron"]  = 3

    GMStyle = {}
    GMStyle["muon"] = 21
    GMStyle["electron"]    = 22

    ofile = ROOT.TFile.Open("acceptance.root", "RECREATE")

    for iwidth in cut_efficiencies:
        for ichan in channels:
            gacp = ROOT.TGraphErrors( 40 )
            gacp.SetName('acceptance_Madgraph_%s_%s'%(iwidth, ichan))
            gacp.SetTitle('acceptance_Madgraph_%s_%s'%(iwidth, ichan))
           
            idx = 0 
            for imass in cut_efficiencies[iwidth]:
                print cut_efficiencies[iwidth][imass][ichan]['effwithtau'][ichan].items()[-1][0]
                acp = cut_efficiencies[iwidth][imass][ichan]['effwithtau'][ichan].items()[-1][1]
                gacp.SetPoint( idx, imass, acp.n)
                gacp.SetPointError( idx, 0, acp.s)
                idx+=1
          
            gacp.SetLineColor(int(GColor[ichan]))
            gacp.SetMarkerColor(int(GColor[ichan]))
            gacp.SetMarkerStyle(int(GMStyle[ichan]))
            gacp.SetMarkerSize(1)
            gacp.Write()

    ofile.Write()
    ofile.Close()

def PlotAcceptance():
    channels = ['muon', 'electron']

    ifile = ROOT.TFile.Open("acceptance.root")
    # Draw graph
    Gacp = {}
    for iwidth in cut_efficiencies:
        Gacp[iwidth] = []
        for ichan in channels:
            print "acceptance_Madgraph_%s_%s"%(iwidth, ichan)
            Gacp[iwidth].append( ifile.Get("acceptance_Madgraph_%s_%s"%(iwidth, ichan)) )
        if iwidth ==0:
           actwidth = "width=0.01%"
        else:
           actwidth = "width=5%"
        DrawGraphs(Gacp[iwidth], channels, 100, 4200, "gen_mass[GeV]", 0.1, 0.8, "Acceptance", "acceptance_%s"%iwidth, dology = False, lheader=actwidth)

main()
