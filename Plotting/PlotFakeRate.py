import json
import ROOT
import os
import numpy as np

ROOT.gStyle.SetOptStat(0)

def get_param(filename, ptlist=None):
    js = json.loads(open(filename).read())
    xlist = np.array(js['ptlist'])
    sig   = np.array(js['parm']['Nsig'])
    error = np.array(js['error']['Nsig'])
    return xlist, sig, error

def quad(x1, x2):
    return np.sqrt(x1*x1+x2*x2)

def fillhist(hist, value, error, label= None):
    for i in range(len(value)):
        hist.SetBinContent(i+1, value[i])
        hist.SetBinError(i+1, error[i])
        if label:
            hist.GetXaxis().SetBinLabel(i+1, label[i])

def pair(x):
    return list(zip(x[:-1], x[1:]))

ptb=None

year =2016
#ptb    = (0, 3.1416*4, 37)
#ptbins = np.linspace(*ptb)
#ptbins = [0, 30, 40, 50, 60, 80, 2000]
#ptname = tuple(map(lambda x: str("%g" %x).replace('.','p'), ptbins))

ptname = ("normal80","badonly80","worstonly80","normal40","badonly40","worstonly40")
if year==2016: ptname = ("normal80","badonly80","normal40","badonly40")
ptsize = len(ptname)

xlist = np.zeros(ptsize)
Na,Nb,Naerr,Nberr = np.zeros(ptsize),np.zeros(ptsize),np.zeros(ptsize),np.zeros(ptsize)
Nda,Ndb,Ndaerr,Ndberr = np.zeros(ptsize),np.zeros(ptsize),np.zeros(ptsize),np.zeros(ptsize)

for i in range(ptsize):
    #data/efake/2016/parms_regD_data2016badonly40.txt
    xlist2,  Na[i],  Naerr[i]  = get_param('data/efake/%i/parms_regA%i%s.txt'       %(year,year,ptname[i]))
    xlist2,  Nb[i],  Nberr[i]  = get_param('data/efake/%i/parms_regB%i%s.txt'       %(year,year,ptname[i]))
    xlist2,  Nda[i], Ndaerr[i] = get_param('data/efake/%i/parms_regA_data%i%s.txt'  %(year,year,ptname[i]))
    xlist2,  Ndb[i], Ndberr[i] = get_param('data/efake/%i/parms_regB_data%i%s.txt'  %(year,year,ptname[i]))
    xlist[i]=xlist2[0]
#xlist,  Na, Naerr = get_param('data/parms_regA.txt')
#xlist2, Nb, Nberr = get_param('data/parms_regB.txt')
#xlistd,  Nda, Ndaerr = get_param('data/parms_regA_data.txt')
#xlistd2, Ndb, Ndberr = get_param('data/parms_regB_data.txt')

fr = Na/ Nb
frerr = fr *  quad(Naerr/Na, Nberr/Nb)

frd    = Nda/ Ndb
frderr = frd *  quad(Ndaerr/Nda, Ndberr/Ndb)

hsize = xlist.size-1
#xlabel = ["%i-%i" %r for r in pair(ptbins)]
xlabel = ptname
#xlabel = None

#make histogram
title = "Photon PixVeto transfer factor"
if ptb:
    h1= ROOT.TH1F('h1',title,ptb[2]-1,ptb[0],ptb[1])
    h2= ROOT.TH1F('h2',title,ptb[2]-1,ptb[0],ptb[1])
else:
    h1= ROOT.TH1F('h1',title,hsize+1,0,hsize+1)
    h2= ROOT.TH1F('h2',title,hsize+1,0,hsize+1)
fillhist(h1, fr, frerr, label=xlabel)
fillhist(h2, frd, frderr, label=xlabel)
c1 = ROOT.TCanvas('c1','c1')
h2.SetMarkerStyle(20)
h2.SetMarkerSize(1.1)
h2.SetMarkerColor(1)
h2.SetLineColor(1)
h2.SetLineWidth(2)
h1.SetLineColor(2)
h1.SetLineWidth(2)
h1.GetXaxis().SetLabelSize(0.05)
h1.GetXaxis().SetTitle('Photon pT [GeV]')
h2.GetYaxis().SetRangeUser(0,h2.GetMaximum()*1.4)
h2.Draw()
h1.Draw('same')
t1 = ROOT.TLegend(0.75,0.75,0.88,0.88)
t1.AddEntry(h1,"MC","L")
t1.AddEntry(h2,"Data","L")
t1.Draw()

outdir = "~/public_html"
outdir = os.path.expanduser(outdir)
c1.SaveAs("%s/fakerate%i.pdf" %(outdir, year))
c1.SaveAs("%s/fakerate%i.png" %(outdir, year))
