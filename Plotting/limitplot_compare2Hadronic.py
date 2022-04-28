#!/usr/bin/env python3
import sys, os
import ROOT
from CombineHarvester.CombineTools.plotting import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

# Style and pads
ModTDRStyle()
graphs = StandardLimitsFromJSONFile(sys.argv[1])
name = os.path.basename(sys.argv[1])

sname = name.replace(".json","")
print(sname)
canv = ROOT.TCanvas(sname, sname)
pads = OnePad()

#print(graphs.values()[2].GetN())
#x = ROOT.Double(0.)
#y = ROOT.Double(0.)
#print(graphs.values())
#graphs.values()[2].GetPoint(10, x, y)
#print(x,y)
#exit()

# Get limit TGraphs as a dictionary

# Create an empty TH1 from the first TGraph to serve as the pad axis and frame
axis = CreateAxisHist(list(graphs.values())[0])
axis.GetXaxis().SetTitle('m_{X} (GeV)')
axis.GetYaxis().SetTitle('95% CL limit #sigma (fb)')
pads[0].cd()
pads[0].SetLogy()
axis.Draw('axis')

# Create a legend in the top left
legend = PositionedLegend(0.3, 0.2, 3, 0.015)

# Set the standard green and yellow colors and draw
StyleLimitBand(graphs)
DrawLimitBand(pads[0], graphs, legend=legend)
legend.Draw()

# Re-draw the frame and tick marks
pads[0].RedrawAxis()
pads[0].GetFrame().Draw()

# Adjust the y-axis range such that the maximum graph value sits 25% below
# the top of the frame. Fix the minimum to zero.
FixBothRanges(pads[0], 0, 0, GetPadYMax(pads[0]), 0.25)

if "0p01" in sys.argv[1]:
    text = "width = 0.01%"
if "5" in sys.argv[1]:
    text = "width = 5%"
text2=None
if "mu" in  sname or "el" in sname:
    ch = sname.split("_")[-1][:2]
    year = int(sname.split("_")[-1][2:])
    ch2 = "Electron" if ch=="el" else "Muon"
    text2 = "%s Channel %i" %(ch2,year)
    print(text2)
l = ROOT.TLatex()
l.SetNDC()
l.SetTextSize(0.04)
l.SetTextFont(72)
l.DrawLatex(0.38,.78, "W#gamma#rightarrow l#gamma#nu")
l.DrawLatex(0.38,.73, text)
if text2: l.DrawLatex(0.5,.55, text2)

ll = ROOT.TLatex()
ll.SetNDC()
ll.SetTextSize(0.04)
ll.SetTextFont(42)
ll.DrawLatex(0.7,.95, "13TeV, 137 fb^{-1}")

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

xatlas_lep, yatlas_lep = array( 'd',[304.97	,338.56	,374.51	,424.86	,472.81	,515.95	,549.51	,626.21	,678.92	,729.25	,784.36	,827.49	,875.41	,928.1	,976.02	,1050.3	,1122.17	,1186.85	,1244.34	,1304.23	,1349.75	,1400.05	,1450.36	,1505.45	,1553.35	,1603.65	]), array( 'd',[5.9078	,4.8497	,4.2518	,3.4903	,2.8651	,2.5119	,2.2022	,1.7207	,1.5086	,1.3226	,1.15954	,1.03344	,0.93633	,0.87671	,0.78137	,0.66287	,0.57167	,0.5095	,0.46162	,0.42518	,0.37894	,0.35481	,0.32147	,0.301	,0.28184	,0.26389	])
xatlas_had, yatlas_had = array( 'd', [1010.16	,1081.3	,1213.41	,1376.02	,1579.27	,1752.03	,1924.8	,2117.89	,2260.16	,2432.93	,2666.67	,2900.41	,3113.82	,3347.56	,3571.14	,3784.55	,4069.11	,4241.87	,4485.77	,4760.16	,5004.07	,5247.97	,5461.38	,5684.96	,5918.7	,6203.25	,6406.5	,6609.76	,6762.2]	), array( 'd',[8.4569	,6.9405	,5.0591	,3.6155	,2.4352	,1.8466	,1.4003	,1.0831	,0.90659	,0.78947	,0.64791	,0.52133	,0.44509	,0.40322	,0.37257	,0.31809	,0.30576	,0.28253	,0.26626	,0.25094	,0.23649	,0.22288	,0.20594	,0.19796	,0.18291	,0.17583	,0.16901	,0.16901	,0.15928	])
#narrow
xcms, ycms = array( 'd',[694.74	,751.58	,865.26	,1016.84	,1196.84	,1367.37	,1528.42	,1680	,1860	,2040	,2248.42	,2456.84	,2712.63	,2977.89	,3318.95	,3660	,3887.37	,4114.74	,4351.58	,4522.11	,4683.16	,4882.11	,5081.05	,5242.11	,5488.42	,5640	,5810.53	,5952.63	] ), array( 'd',[11.043	,7.7155	,5.1793	,3.8401	,2.5772	,1.7999	,1.3345	,0.98944	,0.73353	,0.57728	,0.45426	,0.37945	,0.32329	,0.27542	,0.23929	,0.21635	,0.21617	,0.20756	,0.20329	,0.19916	,0.19127	,0.18367	,0.18354	,0.17981	,0.17264	,0.16914	,0.16903	,0.168] )
#broad
xcms_b, ycms_b = array( 'd',[721.72	,876.64	,1009.43	,1153.28	,1330.33	,1485.25	,1595.9	,1772.95	,2005.33	,2149.18	,2370.49	,2613.93	,2923.77	,3200.41	,3521.31	,3930.74	,4384.43	,4738.52	,5225.41	,5634.84	,5922.54	,] ) , array( 'd',[14.85	,7.7426	,5.9948	,4.4306	,2.848	,2.257	,1.7475	,1.2619	,0.8902	,0.77426	,0.64281	,0.5214	,0.4132	,0.36784	,0.31993	,0.29151	,0.26561	,0.26561	,0.2595	,0.25354	,0.2595	,] )

gr = ROOT.TGraph( len(xatlas_lep), xatlas_lep, yatlas_lep )
gr.SetLineColor( ROOT.kBlue )
gr.SetLineWidth( 2 )
gr.SetLineStyle( 9 )
#gr.Draw()
gr1 = ROOT.TGraph( len(xatlas_had), xatlas_had, yatlas_had )
gr1.SetLineColor( ROOT.kCyan )
gr1.SetLineWidth( 2 )
gr1.SetLineStyle( 9 )
gr1.Draw()
if "0p01" in sys.argv[1]:
    gr2 = ROOT.TGraph( len(xcms), xcms, ycms )
else:
    gr2 = ROOT.TGraph( len(xcms_b), xcms_b, ycms_b )
gr2.SetLineColor( ROOT.kBlue )
gr2.SetLineWidth( 2 )
gr2.SetLineStyle( 9 )
gr2.Draw()

leg1 = ROOT.TLegend(0.65,0.57,0.86,0.7);
leg1.SetFillColor(ROOT.kWhite);
leg1.SetLineColor(ROOT.kWhite);
#entry = leg1.AddEntry(gr,"ATLAS Lep","L")
#entry.SetFillStyle(1001)
#entry.SetLineStyle(2)
#entry.SetLineWidth(1)
#entry.SetTextFont(42)
#entry.SetTextSize(0.04)
#entry.SetLineColor(ROOT.kBlue)
entry = leg1.AddEntry(gr1,"ATLAS Hadron","L")
entry.SetFillStyle(1001)
entry.SetLineStyle(2)
entry.SetLineWidth(1)
entry.SetTextFont(42)
entry.SetTextSize(0.04)
entry.SetLineColor(ROOT.kCyan)
entry = leg1.AddEntry(gr2,"CMS Hadron","L")
entry.SetFillStyle(1001)
entry.SetLineStyle(2)
entry.SetLineWidth(1)
entry.SetTextFont(42)
entry.SetTextSize(0.04)
entry.SetLineColor(ROOT.kBlue)
leg1.Draw();


# Standard CMS logo
DrawCMSLogo(pads[0], 'CMS', 'Simulation Preliminary', 11, 0.200, 0.035, 1.2, '', 0.8)



canv.Print('.pdf')
canv.Print('.png')
canv.Print('.C')
