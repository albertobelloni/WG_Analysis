

def config_samples(samples) :

    import ROOT
    samples.AddSample('Data'    , path='Data'    ,legend_name='Data',   isActive=True, plotColor=ROOT.kBlack, isData=True )
    samples.AddSample('Wgamma'     , path='Wg'     ,legend_name='W#gamma',   isActive=True, plotColor=ROOT.kRed+1 )
    samples.AddSample('Zgamma'     , path='Zg'     ,legend_name='Z#gamma',   isActive=True, plotColor=ROOT.kOrange+1, displayErrBand=True )
    #samples.AddSample('ZJets'     , path='ZJets'     ,legend_name='Z + jets',   isActive=True, plotColor=ROOT.kOrange+1, displayErrBand=True )
    samples.AddSample('EleFake' , path='EleFake' ,legend_name='Electron fake estimate',   isActive=True, plotColor=ROOT.kGreen+1 )
    samples.AddSample('JetFake' , path='JetFake' ,legend_name='Jet fake estimate',   isActive=True, plotColor=ROOT.kBlue-7, displayErrBand=True )
    #samples.AddSample('MCBkg'   , path='MCBkg'   ,legend_name='MC background',   isActive=True, isSignal=True, plotColor=ROOT.kGray+2 )

def print_examples() :
    pass
