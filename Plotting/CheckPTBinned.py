from glob import glob
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.ROOT.EnableImplicitMT()

samples = [
    # 'WJetsToLNu-madgraphMLM'  ,
    'WJetsToLNu-amcatnloFXFX' ,
    'WJetsToLNu_Pt-100To250'  ,
    'WJetsToLNu_Pt-250To400'  ,
    'WJetsToLNu_Pt-400To600'  ,
    'WJetsToLNu_Pt-600ToInf'  ,
]
colors = [
    ROOT.kGray, ROOT.kRed+1, ROOT.kAzure+2, ROOT.kGreen+2, ROOT.kMagenta+2, ROOT.kOrange+1, ROOT.kOrange+3
]
paths = {
    'WJetsToLNu-madgraphMLM'   : 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
    'WJetsToLNu-amcatnloFXFX'  : 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
    'WJetsToLNu_Pt-100To250'   : 'WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
    'WJetsToLNu_Pt-250To400'   : 'WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
    'WJetsToLNu_Pt-400To600'   : 'WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
    'WJetsToLNu_Pt-600ToInf'   : 'WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
}
sampledetails = {
    'WJetsToLNu-madgraphMLM'   : { 'n_evt' : 29514020, 'cross_section' : 20508.9*3, 'gen_eff' : 1.0 , 'k_factor' : 1.0 },# NNLO cross section # 61526.7 in SummaryTable1G25ns
    'WJetsToLNu-amcatnloFXFX'  : { 'n_evt' : 16410910, 'cross_section' : 20508.9*3, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }, 
    'WJetsToLNu_Pt-100To250'   : { 'n_evt' : 1, 'cross_section' : 689.749632 , 'gen_eff' : 1.0 , 'k_factor' : 1. },
    'WJetsToLNu_Pt-250To400'   : { 'n_evt' : 1, 'cross_section' : 24.5069015 , 'gen_eff' : 1.0 , 'k_factor' : 1. },
    'WJetsToLNu_Pt-400To600'   : { 'n_evt' : 1, 'cross_section' : 3.110130566 , 'gen_eff' : 1.0 , 'k_factor' : 1. },
    'WJetsToLNu_Pt-600ToInf'   : { 'n_evt' : 1, 'cross_section' : 0.4683178368 , 'gen_eff' : 1.0 , 'k_factor' : 1. },
}

lumi = 35900.

def getHist(samplename, color):
    print(('Drawing %s' % samplename))
    
    chain = ROOT.TChain('UMDNTuple/EventTree')
    
    nFiles = 0
    files = glob('/store/user/mseidel/WGamma/%s/UMDNTuple_1129_2016/*/*/*.root' % paths[samplename])
    for file in files[:None]:
        chain.Add(file)
        nFiles += 1
    print(('Using %i of %i files' % (nFiles, len(files))))

    rdf = ROOT.RDataFrame(chain)
    rdf = rdf.Define('pt',
        '''
        double pt = -1.;
        for( int gidx = 0; gidx < gen_n; ++gidx ) {
            int id = gen_PID.at(gidx);
            int absid = abs(id);
            int st = gen_status.at(gidx);

            // W boson
            if( absid == 24 ) {
                bool pass_W_cuts = true;

                if( gen_motherPID.at(gidx) == id ) pass_W_cuts = false;
                if( pass_W_cuts ){
                    pt = gen_pt.at( gidx );
                }
            }
        }
        return pt;
        ''')
    rdf = rdf.Define('NLOWeight',
        '''
        double NLOWeight = 1.0;
        if( EventWeights.at(0) < 0 ) {
            NLOWeight = -1.0;
        }
        return NLOWeight;
        ''')
    rdf_hist = rdf.Histo1D((samplename, ';W p_{T} [GeV];Events (%.1f/fb)' % (lumi/1000), 400, 0, 2000), 'pt', 'NLOWeight')
    # rdf_hist = rdf_hist_resultptr.DrawCopy()
    sample = sampledetails[samplename]
    rdf_hist.Scale(lumi * sample['cross_section'] * sample['k_factor'] / rdf_hist.Integral())
    rdf_hist.SetLineColor(color)
    rdf_hist.SetLineWidth(2)
    return rdf_hist

hists = {}
for i,samplename in enumerate(samples):
    hists[samplename] = getHist(samplename, colors[i])

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
    hist.GetYaxis().SetRangeUser(1e-5*lumi, 1e5*lumi)
    if firstHist:
        copy = hist.DrawCopy()
        firstHist = False
    else:
        copy = hist.DrawCopy('same')
    leg.AddEntry(copy, samplename, 'l')

hstitch = hists['WJetsToLNu-amcatnloFXFX'].Clone('hstitch')
# hstitch.SetMarkerStyle(20)
hstitch.SetLineColor(colors[-1])
for i in range(hstitch.GetNbinsX()+2):
    if hstitch.GetBinCenter(i) > 100:
        hstitch.SetBinContent(i, 0.)
        hstitch.SetBinError(i, 0.)
hstitch.Add(hists['WJetsToLNu_Pt-100To250'].Clone())
hstitch.Add(hists['WJetsToLNu_Pt-250To400'].Clone())
hstitch.Add(hists['WJetsToLNu_Pt-400To600'].Clone())
hstitch.Add(hists['WJetsToLNu_Pt-600ToInf'].Clone())
hstitch.Draw('same')
leg.AddEntry(hstitch, 'WJetsToLNu_Pt stitched', 'pl')

leg.Draw()

c.SaveAs('Plots/CheckPTBinned.pdf')
c.SaveAs('Plots/CheckPTBinned.root')
c.SetLogy()
c.SaveAs('Plots/CheckPTBinned_log.pdf')
