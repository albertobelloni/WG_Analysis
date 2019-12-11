import json
import ROOT
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
    return zip(x[:-1], x[1:])

ptb=None

#ptb    = (0, 3.1416*4, 37)
#ptbins = np.linspace(*ptb)
ptbins = [0, 30, 40, 50, 60, 80, 2000]
ptname = tuple(map(lambda x: str("%g" %x).replace('.','p'), ptbins))
ptsize = len(ptname)-1

xlist = np.zeros(ptsize)
Na,Nb,Naerr,Nberr = np.zeros(ptsize),np.zeros(ptsize),np.zeros(ptsize),np.zeros(ptsize)
Nda,Ndb,Ndaerr,Ndberr = np.zeros(ptsize),np.zeros(ptsize),np.zeros(ptsize),np.zeros(ptsize)

for i in range(ptsize):
    xlist2, Na[i], Naerr[i] = get_param('data/parms_regA%s.txt' %ptname[i])
    xlist2,   Nb[i], Nberr[i] = get_param('data/parms_regB%s.txt' %ptname[i])
    xlist2,  Nda[i], Ndaerr[i] = get_param('data/parms_regA_data%s.txt' %ptname[i])
    xlist2,  Ndb[i], Ndberr[i] = get_param('data/parms_regB_data%s.txt' %ptname[i])
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
xlabel = ["%i-%i" %r for r in pair(ptbins)]
#xlabel = None

#make histogram
if ptb:
    h1= ROOT.TH1F('h1','Photon Pixel Seed Veto Passing Rate',ptb[2]-1,ptb[0],ptb[1])
    h2= ROOT.TH1F('h2','Photon Pixel Seed Veto Passing Rate',ptb[2]-1,ptb[0],ptb[1])
else:
    h1= ROOT.TH1F('h1','Photon Pixel Seed Veto Passing Rate',hsize+1,0,hsize+1)
    h2= ROOT.TH1F('h2','Photon Pixel Seed Veto Passing Rate',hsize+1,0,hsize+1)
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
h1.Draw()
h2.Draw('same')
t1 = ROOT.TLegend(0.75,0.75,0.88,0.88)
t1.AddEntry(h1,"MC","L")
t1.AddEntry(h2,"Data","L")
t1.Draw()

