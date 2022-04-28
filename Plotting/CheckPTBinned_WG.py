from glob import glob
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.ROOT.EnableImplicitMT()

samples = [
    'WGToLNuG-amcatnloFXFX' ,
    'WGToLNuG_01J_5f-amcatnloFXFX' ,
    'WGToLNuG_PtG-130-amcatnloFXFX' ,
    'WGToLNuG_PtG-500-amcatnloFXFX' ,
]
colors = [
    #ROOT.kGray,
    ROOT.kRed+1, ROOT.kAzure+2, ROOT.kGreen+2, ROOT.kMagenta+2, ROOT.kOrange+1, ROOT.kOrange+3
]
paths = {
        'WGToLNuG_01J_5f-amcatnloFXFX' :"WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8",
        'WGToLNuG_PtG-130-amcatnloFXFX': "WGToLNuG_PtG-130_TuneCP5_13TeV-amcatnloFXFX-pythia8",
        'WGToLNuG_PtG-500-amcatnloFXFX': "WGToLNuG_PtG-500_TuneCP5_13TeV-amcatnloFXFX-pythia8",
}
paths2016 = {
        'WGToLNuG_01J_5f-amcatnloFXFX' :"WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
        'WGToLNuG-amcatnloFXFX' :"WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
        'WGToLNuG_PtG-130-amcatnloFXFX': "WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
        'WGToLNuG_PtG-500-amcatnloFXFX': "WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
}

sampledetails = {
        'WGToLNuG_01J_5f-amcatnloFXFX'         :{ 'n_evt' : 25296567, 'cross_section' : 190, 'gen_eff' : 1.0, 'k_factor' : 1.0 }, # cross section taken from McM (489.0) from gridpack, 8.217e+02 .  #total events = 5048470
        'WGToLNuG_PtG-130-amcatnloFXFX' :{ 'n_evt' : 841701, 'cross_section' : 1.13, 'gen_eff' : 1.0, 'k_factor' : 1.0 }, # cross section taken from McM, from gridpack, 2.563e+00 # total events = 1561571
        'WGToLNuG_PtG-500-amcatnloFXFX' :{ 'n_evt' : 827560, 'cross_section' : 0.00963, 'gen_eff' : 1.0, 'k_factor' : 1.0 }, # cross section taken from McM (0.007945) from gridpack, 2.948e-02 # total events = 1609694
        'WGToLNuG-amcatnloFXFX'         :{ 'n_evt' : 25296567, 'cross_section' : 510, 'gen_eff' : 1.0, 'k_factor' : 1.0 }, # cross section taken from McM (489.0) from gridpack, 8.217e+02 .  #total events = 5048470
}


year = 2016

if year == 2016:
    lumi = 36000.
    paths = paths2016
if year == 2017:
    lumi = 41000.
if year == 2018:
    lumi = 59000.
label = ROOT.TLatex()
label.SetNDC()
label.SetTextSize( 0.035 )
#text = '#font[132]{Year %i}' %year
text = 'Year %i' %year
label.SetText(.2, .85, text)

def create_standard_ratio_canvas() :

    #xsize = 800
    xsize = 750
    ysize = 750
    curr_canvases = dict()
    curr_canvases['base'] = ROOT.TCanvas('basecan', 'basecan', xsize, ysize)

    curr_canvases['bottom'] = ROOT.TPad('bottompad', 'bottompad', 0.01, 0.01, 0.99, 0.34)
    curr_canvases['top'] = ROOT.TPad('toppad', 'toppad', 0.01, 0.35, 0.99, 0.99)
    curr_canvases['top'].SetTopMargin(0.08)
    curr_canvases['top'].SetBottomMargin(0.08)
  # curr_canvases['top'].SetBottomMargin(0.02)
    curr_canvases['top'].SetLeftMargin(0.15)
    curr_canvases['top'].SetRightMargin(0.05)
    curr_canvases['bottom'].SetTopMargin(0.05)
   #curr_canvases['bottom'].SetTopMargin(0.00)
    curr_canvases['bottom'].SetBottomMargin(0.3)
    curr_canvases['bottom'].SetLeftMargin(0.15)
    curr_canvases['bottom'].SetRightMargin(0.05)
    curr_canvases['bottom'].SetGridy(1)
    curr_canvases['base'].cd()
    curr_canvases['bottom'].Draw()
    curr_canvases['top'].Draw()
    return curr_canvases

def getHist(samplename, color, year):
    print(('Drawing %s' % samplename))
    
    chain = ROOT.TChain('UMDNTuple/EventTree')
    
    nFiles = 0
    files = glob('/store/user/kawong/WGamma/%s/UMDNTuple_20200202_%i/*/*/*.root' % (paths[samplename], year))
    #if "WGToLNuG_PtG" in paths[samplename] and "TuneCUETP8M1" in paths[samplename]:
    if "TuneCUETP8M1" in paths[samplename] and "01J" not in paths[samplename]:
        files = glob('/store/user/kawong/WGamma2/%s/*/*/*/*.root' % (paths[samplename]))
    for f in files[:None]:
        chain.Add(f)
        nFiles += 1
    print(('Using %i of %i files' % (nFiles, len(files))))

    rdf = ROOT.RDataFrame(chain)
    rdf = rdf.Define('leppt',
        '''
        double pt = 10000.;
        for( int gidx = 0; gidx < gen_n; ++gidx ) {
            int id = gen_PID.at(gidx);
            int absid = abs(id);

            // photon
            if( absid == 11 || absid == 13 || absid == 15 ) {
                double tmppt = gen_pt.at(gidx);
                if (tmppt<pt) {pt=tmppt;}
            }
        }
        return pt;
        ''')
    rdf = rdf.Filter("leppt>15")
    rdf = rdf.Define('pt',
        '''
        double pt = -1.;
        for( int gidx = 0; gidx < gen_n; ++gidx ) {
            int id = gen_PID.at(gidx);
            int absid = abs(id);
            int mid = gen_motherPID.at(gidx);
            int absmid = abs(mid);
            int st = gen_status.at(gidx);
            int ipfs = gen_isPromptFinalState.at(gidx);

            // photon
            if( absid == 22 ) {

                if ((absmid==24&&ipfs) || st==23){
                    double pttmp = gen_pt.at( gidx );
                    if (pttmp>pt){pt=pttmp;}
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
    rdf_hist = rdf.Histo1D((samplename, ';p_{T}(#gamma)[GeV];Events (%.1f/fb)' % (lumi/1000), 100, 0, 2000), 'pt', 'NLOWeight')
    # rdf_hist = rdf_hist_resultptr.DrawCopy()
    sample = sampledetails[samplename]
    rdf_hist.Scale(lumi * sample['cross_section'] * sample['k_factor'] / rdf_hist.Integral())
    rdf_hist.SetLineColor(color)
    rdf_hist.SetLineWidth(2)
    return rdf_hist

curr_canvases =  create_standard_ratio_canvas()
hists = {}
ratio = {}
hist_denominator  = None
for i,samplename in enumerate(samples):
    if samplename not in paths:
        continue
    hists[samplename] = getHist(samplename, colors[i], year)
    #print hists[samplename], hist_denominator
    if i == 0:
        hist_denominator = hists[samplename].GetValue()
    else:
        ratio[samplename] = hists[samplename].GetValue().Clone()
        ratio[samplename].Divide(hist_denominator)
        hist_denominator = hists[samplename].GetValue()

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(ROOT.kViridis)
ROOT.TColor.InvertPalette()
ROOT.gStyle.SetTitleXOffset(1.5)
ROOT.gStyle.SetTitleYOffset(0)

c1 = curr_canvases["top"] #ROOT.TCanvas()
c1.cd()
#c.SetTopMargin(0.07)
#c.SetBottomMargin(0.13)

leg = ROOT.TLegend(0.4, 0.5, 0.9, 0.9)

firstHist = True
for samplename in samples:
    hist = hists[samplename]
    hist.GetYaxis().SetRangeUser(1e-7*lumi, 1e3*lumi)
    if firstHist:
        copy = hist.DrawCopy()
        firstHist = False
    else:
        copy = hist.DrawCopy('same')
    leg.AddEntry(copy, samplename, 'l')

leg.Draw()
label.Draw()


c = curr_canvases["bottom"]
c.cd()
firstHist=True
for samplename in samples:
    hist = ratio.get(samplename)
    if hist == None:
        continue
    hist.GetYaxis().SetRangeUser(0,2)
    hist.GetYaxis().SetTitle("Ratio to previous plot")
    hist.GetYaxis().SetTitleSize(0.06)
    hist.GetXaxis().SetTitleSize(0.06)
    hist.GetXaxis().SetLabelSize(0.06)
    hist.GetYaxis().SetLabelSize(0.06)
    if firstHist:
        copy = hist.DrawCopy()
        firstHist = False
    else:
        copy = hist.DrawCopy('same')

#hstitch = hists['WJetsToLNu-amcatnloFXFX'].Clone('hstitch')
# hstitch.SetMarkerStyle(20)
#hstitch.SetLineColor(colors[-1])
#for i in range(hstitch.GetNbinsX()+2):
#    if hstitch.GetBinCenter(i) > 100:
#        hstitch.SetBinContent(i, 0.)
#        hstitch.SetBinError(i, 0.)
#hstitch.Add(hists['WJetsToLNu_Pt-100To250'].Clone())
#hstitch.Add(hists['WJetsToLNu_Pt-250To400'].Clone())
#hstitch.Add(hists['WJetsToLNu_Pt-400To600'].Clone())
#hstitch.Add(hists['WJetsToLNu_Pt-600ToInf'].Clone())
#hstitch.Draw('same')
#leg.AddEntry(hstitch, 'WJetsToLNu_Pt stitched', 'pl')


c = curr_canvases["base"]
savedir = "~/public_html"
#c.SaveAs('%s/CheckPTBinned_%i.pdf' %(savedir,year))
c1.SetLogy()
c.SaveAs('%s/CheckPTBinned_log_%i.pdf'%(savedir,year))
c.SaveAs('%s/CheckPTBinned_log_%i.png'%(savedir,year))
c.SaveAs('%s/CheckPTBinned_%i.root' %(savedir,year))
