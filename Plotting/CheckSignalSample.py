from glob import glob
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.ROOT.EnableImplicitMT()

width = "0p01"
year = 2018
#generator = "MadGraph"
generator = "Pythia"
samples = [
"%sChargedResonance_WGToLNu%s_M200_width%s",
"%sChargedResonance_WGToLNu%s_M250_width%s",
"%sChargedResonance_WGToLNu%s_M300_width%s",
"%sChargedResonance_WGToLNu%s_M350_width%s",
"%sChargedResonance_WGToLNu%s_M400_width%s",
"%sChargedResonance_WGToLNu%s_M450_width%s",
"%sChargedResonance_WGToLNu%s_M500_width%s",
"%sChargedResonance_WGToLNu%s_M600_width%s",
"%sChargedResonance_WGToLNu%s_M700_width%s",
"%sChargedResonance_WGToLNu%s_M800_width%s",
"%sChargedResonance_WGToLNu%s_M900_width%s",
"%sChargedResonance_WGToLNu%s_M1000_width%s",
"%sChargedResonance_WGToLNu%s_M1200_width%s",
"%sChargedResonance_WGToLNu%s_M1400_width%s",
"%sChargedResonance_WGToLNu%s_M1600_width%s",
"%sChargedResonance_WGToLNu%s_M1800_width%s",
"%sChargedResonance_WGToLNu%s_M2000_width%s",
"%sChargedResonance_WGToLNu%s_M2400_width%s",
"%sChargedResonance_WGToLNu%s_M2600_width%s",
"%sChargedResonance_WGToLNu%s_M2800_width%s",
"%sChargedResonance_WGToLNu%s_M3000_width%s",
"%sChargedResonance_WGToLNu%s_M3500_width%s",
"%sChargedResonance_WGToLNu%s_M4000_width%s",
]

sfix = ""
if year == 2018:
    jobtag = "UMDNTuple_0915_2018"
    sfix = "G"
if year == 2016:
    jobtag = "UMDNTuple_0915_2016"

def getHist(samplename, color):
    chain = ROOT.TChain('UMDNTuple/EventTree')

    for f in glob('/store/user/kawong/WGamma2/%s/%s/*/*/*.root' %(samplename,jobtag)): #[:1]:
        chain.Add(f)
    if chain.GetEntries()<=0:
        return None

    rdf = ROOT.RDataFrame(chain)
    rdf = rdf.Define('m',
        """
        double m = 0.0;
        TLorentzVector mediator;
        for( int gidx = 0; gidx < gen_n; ++gidx ) {
            int id = gen_PID.at(gidx);
            int absid = abs(id);
            int st = gen_status.at(gidx);
            double pt  = gen_pt.at(gidx);
            double eta = gen_eta.at(gidx);
            double phi = gen_phi.at(gidx);
            double e   = gen_e.at(gidx);
            if ( absid > 90000 ) {
                mediator.SetPtEtaPhiM(pt, eta, phi, e);
                m = mediator.M();
                return m;
            }
         }
         return m;
         """)
       #     if ( absid == 24 && wboson.Pt() == 0 ){
       #         wboson.SetPtEtaPhiM(pt, eta, phi, e);
       #     }
       #     if ( absid == 22 && photon.Pt() == 0 ){
       #         photon.SetPtEtaPhiM(pt, eta, phi, e);
       #     }
       # }
       # m = (wboson + photon).M();
       # return m;
    rdf_hist = rdf.Histo1D((samplename, ';mass [GeV];Events', 300, 0, 3000), 'm')
    rdf_hist.DrawCopy()
    rdf_hist.SetLineColor(color)
    rdf_hist.SetLineWidth(2)
    return rdf_hist

hists = {}
i = 0
for sname in samples:
    samplename = sname %(generator, sfix,width)
    print('Drawing %s %i' % (samplename, (i%5)*10+2*(i/5)+51 ))
    h = getHist(samplename, i%9 +1 )
    if h:
        hists[samplename] = h
        i += 1

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(ROOT.kBird)
#ROOT.TColor.InvertPalette()
ROOT.gStyle.SetTitleXOffset(1.5)
ROOT.gStyle.SetTitleYOffset(0)

c = ROOT.TCanvas()
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)

leg = ROOT.TLegend(0.15, 0.65, 0.85, 0.9)
leg.SetBorderSize(0)
leg.SetNColumns(2)

firstHist = True
for samplename, hist in hists.iteritems():
    #hist = hists[samplename]
    hist.GetYaxis().SetRangeUser(1e-1, 2e4)
    if firstHist:
        copy = hist.DrawCopy()
        firstHist = False
    else:
        copy = hist.DrawCopy('same')
    leg.AddEntry(copy, samplename, 'l')

leg.Draw()

c.SaveAs('~/public_html/CheckSignal.pdf')
c.SaveAs('~/public_html/CheckSignal.root')

for samplename, hist in hists.iteritems():
    hist.GetYaxis().SetRangeUser(1, 1e10)
c.SetLogy()
c.SaveAs('~/public_html/CheckSignal_ln.pdf')
