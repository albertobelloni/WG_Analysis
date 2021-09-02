#!/usr/bin/env python
import sys, os
import ROOT
from CombineHarvester.CombineTools.plotting import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

# Style and pads
ModTDRStyle()
graphs = StandardLimitsFromJSONFile(sys.argv[1])
name = os.path.basename(sys.argv[1])
fname = {}
fgraphs = {}
if (len(sys.argv)%2!=1):
    print("give me correct argument!! :")
    print(sys.argv)
    exit()

for i in range((len(sys.argv)+1)/2):
    if i ==0: continue
    fgraphs[i] = StandardLimitsFromJSONFile(sys.argv[i])
    fname[i] = sys.argv[i+len(sys.argv)/2]
    print(fgraphs, fname)

sname = name.replace(".json","")
print sname
canv = ROOT.TCanvas(sname, sname)
pads = OnePad()

x = ROOT.Double(0.)
y = ROOT.Double(0.)
for i in range((len(sys.argv)+1)/2):
    if i ==0: continue
    fgraphs[i].values()[2].GetPoint(0, x, y)
    print(x,y)
print("\n")
for i in range((len(sys.argv)+1)/2):
    if i ==0: continue
    fgraphs[i].values()[2].GetPoint(1, x, y)
    print(x,y)
for i in range((len(sys.argv)+1)/2):
    if i ==0: continue
    #fgraphs[i].values()[2].GetPoint(10, x, y)
    #print(x,y)

# Get limit TGraphs as a dictionary

# Create an empty TH1 from the first TGraph to serve as the pad axis and frame
axis = CreateAxisHist(graphs.values()[0])
axis.GetXaxis().SetTitle('m_{res} (GeV)')
axis.GetYaxis().SetTitle('95% CL limit #sigma (fb)')
pads[0].cd()
pads[0].SetLogy()
axis.Draw('axis')

# Create a legend in the top left
legend = PositionedLegend(0.3, 0.2, 3, 0.015)

# Set the standard green and yellow colors and draw
#StyleLimitBand(graphs)
#DrawLimitBand(pads[0], graphs, legend=legend)
#legend.Draw()

# Re-draw the frame and tick marks
pads[0].RedrawAxis()
pads[0].GetFrame().Draw()

# Adjust the y-axis range such that the maximum graph value sits 25% below
# the top of the frame. Fix the minimum to zero.
FixBothRanges(pads[0], 0, 0, GetPadYMax(pads[0]), 0.25)

if "5_all" in sys.argv[1]:
    text = "width = 5%"
if "0p01_all" in sys.argv[1]:
    text = "width = 0.01%"
text2=None
if "mu" in  sname or "el" in sname:
    ch = sname.split("_")[-1][:2]
    year = int(sname.split("_")[-1][2:])
    ch2 = "Electron" if ch=="el" else "Muon"
    text2 = "%s Channel %i" %(ch2,year)
    print text2
l = ROOT.TLatex()
l.SetNDC()
l.SetTextSize(0.04)
l.SetTextFont(72)
l.DrawLatex(0.38,.78, "W#gamma#rightarrow l#gamma#nu")
l.DrawLatex(0.38,.73, text)
if text2: l.DrawLatex(0.5,.55, text2)

hmax = axis.GetMaximum()
hmin = axis.GetMinimum()
def oneline(xval):
    ln = ROOT.TLine(xval,hmax,xval,hmin)
    ln.SetLineStyle(3)
    ln.SetLineWidth(2)
    ln.Draw()
    return ln
#ln = oneline(625)
#ln2 = oneline(425)

#plt atlas
from array import array

fgraph={}

color = [ ROOT.kCyan,ROOT.kBlue,ROOT.kOrange,ROOT.kRed, ROOT.kBlack, ROOT.kGreen]
if len(sys.argv)/2 > 6:
    for j in range(20):
        color[j] = ROOT.kRainbow+2*j
for i in range((len(sys.argv)+1)/2):
    if i ==0: continue
    fgraphs[i].values()[2].GetPoint(8, x, y)
    fgraph[i] = fgraphs[i].values()[2]
    fgraph[i].SetLineColor( color[i-1] )
    fgraph[i].SetLineWidth( 2 )
    fgraph[i].SetLineStyle( 9 )
    fgraph[i].Draw()
leg1 = ROOT.TLegend(0.45,0.5,0.66,0.7);
leg1.SetFillColor(ROOT.kWhite);
leg1.SetLineColor(ROOT.kWhite);
for i in range((len(sys.argv)+1)/2):
    if i ==0: continue
    entry = leg1.AddEntry(fgraph[i], fname[i],"L")
    entry.SetFillStyle(1001)
    entry.SetLineStyle(2)
    entry.SetLineWidth(1)
    entry.SetTextFont(42)
    entry.SetTextSize(0.04)
    entry.SetLineColor(color[i-1])

leg1.Draw()

# Standard CMS logo
DrawCMSLogo(pads[0], 'CMS', 'Simulation Preliminary', 11, 0.200, 0.035, 1.2, '', 0.8)

canv.Print('.pdf')
canv.Print('.png')
