from glob import glob
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.ROOT.EnableImplicitMT()

samples = [
    'WJetsToLNu-madgraphMLM'  ,
    'WJetsToLNu-amcatnloFXFX' ,
    'WJetsToLNu_HT-100To200'  ,
    'WJetsToLNu_HT-200To400'  ,
    'WJetsToLNu_HT-400To600'  ,
    'WJetsToLNu_HT-600To800'  ,
    'WJetsToLNu_HT-800To1200' ,
    'WJetsToLNu_HT-1200To2500',
    'WJetsToLNu_HT-2500ToInf' ,
]
paths = {
    'WJetsToLNu-madgraphMLM'   : 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu-amcatnloFXFX'  : 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
    'WJetsToLNu_HT-100To200'   : 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu_HT-200To400'   : 'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu_HT-400To600'   : 'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu_HT-600To800'   : 'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu_HT-800To1200'  : 'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu_HT-1200To2500' : 'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu_HT-2500ToInf'  : 'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
}
sampledetails = {
    'WJetsToLNu-madgraphMLM'   : { 'n_evt' : 29514020, 'cross_section' : 20508.9*3, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },# NNLO cross section # 61526.7 in SummaryTable1G25ns
    'WJetsToLNu-amcatnloFXFX'  : { 'n_evt' : 16410910, 'cross_section' : 20508.9*3, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }, 
    'WJetsToLNu_HT-100To200'   : { 'n_evt' : 9945478, 'cross_section' :  1345,   'gen_eff' : 1.0 , 'k_factor' : 1.21 }, ## 1346 in XSDB #from SummaryTable1G25ns twiki
    'WJetsToLNu_HT-200To400'   : { 'n_evt' : 4963240, 'cross_section' :  359.7, 'gen_eff' : 1.0 , 'k_factor' : 1.21 },
    'WJetsToLNu_HT-400To600'   : { 'n_evt' : 1963464, 'cross_section' :  48.91, 'gen_eff' : 1.0 , 'k_factor' : 1.21 },
    'WJetsToLNu_HT-600To800'   : { 'n_evt' : 3779141, 'cross_section' :  12.05, 'gen_eff' : 1.0 , 'k_factor' : 1.21 },
    'WJetsToLNu_HT-800To1200'  : { 'n_evt' : 1544513, 'cross_section' :  5.501, 'gen_eff' : 1.0 , 'k_factor' : 1.21 },
    'WJetsToLNu_HT-1200To2500' : { 'n_evt' : 244532,  'cross_section' :  1.329, 'gen_eff' : 1.0 , 'k_factor' : 1.21 },
    'WJetsToLNu_HT-2500ToInf'  : { 'n_evt' : 253561, 'cross_section' :  0.03216, 'gen_eff' : 1.0 , 'k_factor' : 1.21 },
}

def getHist(samplename, color):
    chain = ROOT.TChain('UMDNTuple/EventTree')
    
    for file in glob('/store/user/mseidel/WGamma/%s/UMDNTuple_1129_2016/*/*/*.root' % paths[samplename]): #[:1]:
        chain.Add(file)
    print chain.GetEntries()

    rdf = ROOT.RDataFrame(chain)
    rdf = rdf.Define('ht',
        '''
        double ht = 0.0;
        for( int gidx = 0; gidx < gen_n; ++gidx ) {
            int id = gen_PID.at(gidx);
            int absid = abs(id);
            int st = gen_status.at(gidx);

            // calculate HT at truth level
            if( ( absid < 6 || id == 21 )  && st == 23 ) {
                ht += gen_pt.at(gidx);
            }
        }
        return ht;
        ''')
    rdf = rdf.Define('NLOWeight',
        '''
        double NLOWeight = 1.0;
        if( EventWeights.at(0) < 0 ) {
            NLOWeight = -1.0;
        }
        return NLOWeight;
        ''')
    rdf_hist = rdf.Histo1D((samplename, ';HT [GeV];Events', 500, 0, 5000), 'ht', 'NLOWeight')
    # rdf_hist = rdf_hist_resultptr.DrawCopy()
    sample = sampledetails[samplename]
    rdf_hist.Scale(sample['cross_section'] * sample['k_factor'] / rdf_hist.Integral())
    rdf_hist.SetLineColor(color)
    rdf_hist.SetLineWidth(2)
    return rdf_hist

hists = {}
i = 1
for samplename in samples:
    print('Drawing %s' % samplename)
    hists[samplename] = getHist(samplename, i)
    i += 1

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(ROOT.kViridis)
ROOT.TColor.InvertPalette()
ROOT.gStyle.SetTitleXOffset(1.5)
ROOT.gStyle.SetTitleYOffset(0)

c = ROOT.TCanvas()
c.SetTopMargin(0.07)
c.SetBottomMargin(0.13)

leg = ROOT.TLegend(0.5, 0.5, 0.9, 0.9)

firstHist = True
for samplename in samples:
    hist = hists[samplename]
    hist.GetYaxis().SetRangeUser(1e-5, 1e5)
    if firstHist:
        copy = hist.DrawCopy()
        firstHist = False
    else:
        copy = hist.DrawCopy('same')
    leg.AddEntry(copy, samplename, 'l')

leg.Draw()

c.SaveAs('Plots/CheckHTBinned.pdf')
c.SaveAs('Plots/CheckHTBinned.root')
c.SetLogy()
c.SaveAs('Plots/CheckHTBinned_log.pdf')
