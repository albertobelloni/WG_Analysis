#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)

from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument('--channel', default='el', dest='channel', help='Channel = el/mu')
options = parser.parse_args()
channel = options.channel

file = ROOT.TFile('Plots/WCRInvIsoPlots/iso_%s.root' % channel, 'READ')
pad = file.Get('basecan').GetPrimitive('toppad')

if channel == 'el':
    data = pad.GetPrimitive('SingleElectron')
if channel == 'mu':
    data = pad.GetPrimitive('SingleMuon')
# dataBkgSub = data.Clone('dataBkgSub')

mcerrors = pad.GetPrimitive('Graph_from___AllStack__')

qcd = None
for h in pad.GetPrimitive('stack').GetHists():
    print(h.GetName(), h.Integral())
    if 'QCD' in h.GetName():
        qcd = h
    else:
        data.Add(h, -1)

scale = data.Integral()/qcd.Integral()
print('Inclusive QCD scale factor = %.3f' % scale)

qcd_scaled = qcd.Clone('qcd_scaled')
qcd_scaled.Scale(scale)

# canvas
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTitleSize(0.04, 'xyz')
ROOT.gStyle.SetTitleXOffset(1.5)
ROOT.gStyle.SetTitleYOffset(0)

c = ROOT.TCanvas('c', 'c', 500, 500)
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)
c.SetRightMargin(0.05)
c.SetLogy()

data.GetXaxis().SetTitle('PF isolation')
qcd.SetLineColor(ROOT.kCyan+1)
qcd_scaled.SetLineColor(ROOT.kMagenta+1)

data.Draw()
qcd.Draw('same')
qcd_scaled.Draw('same')

leg = ROOT.TLegend(0.5,0.7,0.9,0.9)
leg.AddEntry(data, 'Data (EW subtracted)', 'p')
leg.AddEntry(qcd, 'QCD', 'l')
leg.AddEntry(qcd_scaled, 'QCD (x %.3f)' % scale, 'l')
leg.Draw()

c.SaveAs('Plots/MakeQCDFit_%s.pdf' % channel)

# ratio = data.Clone('ratio')
# ratio.Divide(qcd)

# ratio.Draw()
# c.SaveAs('Plots/MakeQCDFit_ratio_%s.pdf' % channel)
