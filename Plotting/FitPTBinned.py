#!/usr/bin/env python3
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument('-b', '--boundary', default=250, dest='boundary', help='Boundary for fitting', type=int)
options = parser.parse_args()

ob = options.boundary

boundaries = [100, 250, 400, 600, 'Inf']
if not ob in boundaries[1:-1]:
    import sys
    sys.exit('Exit: invalid boundary')
ib = boundaries.index(ob)

samples = {
    'incl' : 'WJetsToLNu-amcatnloFXFX' ,
    'below' : 'WJetsToLNu_Pt-' + str(boundaries[ib-1]) + 'To' + str(boundaries[ib]),
    'above' : 'WJetsToLNu_Pt-' + str(boundaries[ib]) + 'To' + str(boundaries[ib+1]),
    'stitch' : 'hstitch',
}

def splitHist(hist, boundary):
    hup = hist.Clone(hist.GetName()+'_up')
    hdn = hist.Clone(hist.GetName()+'_dn')
    for i in range(hist.GetNbinsX()+2):
        if hist.GetBinCenter(i) < boundary:
            hup.SetBinContent(i, 0.)
            hup.SetBinError(i, 0.)
        if hist.GetBinCenter(i) > boundary:
            hdn.SetBinContent(i, 0.)
            hdn.SetBinError(i, 0.)
    return hup,hdn

file = ROOT.TFile('Plots/CheckPTBinned.root', 'READ')
c1 = file.Get('c1')

# get histos and split
hists = {}
for key,name in list(samples.items()):
    nameInFile = name
    if name != 'hstitch':
        nameInFile = name + '_copy'
    hists[key] = c1.GetPrimitive(nameInFile)
    hists[key].SetMaximum()
    hists[key].SetMinimum()
    hists[key+'_up'],hists[key+'_dn'] = splitHist(hists[key], ob)

# scale histos
x_dn_total = 1.
x_up_total = 1.
fitrange = ob*0.2

fit = []
for iteration in range(10):
    # stitch together
    hists['stitch_new'] = hists['stitch'].Clone('stitch_new_%i' % iteration)
    hists['stitch_new'].Reset()
    hists['stitch_new'].Add(hists['below_up'])
    hists['stitch_new'].Add(hists['below_dn'])
    hists['stitch_new'].Add(hists['above_up'])
    hists['stitch_new'].Add(hists['above_dn'])
    
    fit.append(ROOT.TF1('fit_%i' % iteration, 'pol3', ob-fitrange, ob+fitrange))
    hists['stitch_new'].Fit(fit[iteration], 'WQ0', '', ob-fitrange, ob+fitrange)

    val = ob - 2.5
    bin = hists['incl'].FindBin(val)
    sumfit,sum1,sum2 = 0., 0., 0.
    for i in range(1):
        sumfit += fit[iteration].Eval(val-5*i)
        sum1 += hists['below_dn'].GetBinContent(bin-1*i)
        sum2 += hists['above_dn'].GetBinContent(bin-1*i)
    x_dn = (sumfit - sum1) / sum2
    hists['above_dn'].Scale(x_dn)

    val = ob + 2.5
    bin = hists['incl'].FindBin(val)
    sumfit,sum1,sum2 = 0., 0., 0.
    for i in range(1):
        sumfit += fit[iteration].Eval(val+5*i)
        sum1 += hists['above_up'].GetBinContent(bin+1*i)
        sum2 += hists['below_up'].GetBinContent(bin+1*i)
    x_up = (sumfit - sum1) / sum2
    hists['below_up'].Scale(x_up)
    
    print(('k factors in iteration, above_dn, below_up', iteration, x_dn, x_up))
    
    x_dn_total *= x_dn
    x_up_total *= x_up

print(('TOTAL k factors above_dn / below_up', x_dn_total, x_up_total))

c = ROOT.TCanvas()
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)
c.SetLeftMargin(0.13)
c.cd()

leg = ROOT.TLegend(0.5, 0.6, 0.9, 0.9)
leg.AddEntry(hists['incl'], samples['incl'], 'l')
leg.AddEntry(hists['below'], samples['below'], 'l')
leg.AddEntry(hists['above'], samples['above'], 'l')
leg.AddEntry(hists['stitch'], 'Stiched OLD', 'l')
leg.AddEntry(hists['stitch_new'], 'Stiched NEW, k = %.3f, %.3f' % (x_dn_total, x_up_total), 'l')

hists['incl'].GetXaxis().SetRangeUser(ob-fitrange, ob+fitrange)
hists['incl'].GetYaxis().SetRangeUser(hists['above'].GetMinimum()*2, hists['above'].GetMaximum()*4)
hists['incl'].Draw()
hists['stitch'].Draw('same')
hists['below_up'].Draw('same')
hists['below_dn'].Draw('same')
hists['above_up'].Draw('same')
hists['above_dn'].Draw('same')
fit[-1].Draw('lsame')
hists['stitch_new'].SetLineColor(ROOT.kBlack)
hists['stitch_new'].Draw('same')
leg.Draw()

c.SaveAs('Plots/FitPTBinned%i.pdf' % ob)
