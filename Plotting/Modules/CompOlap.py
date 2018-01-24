def config_samples(samples) :

    import ROOT

    samples.AddSample('SingleMuon'                       , path='SingleMuon'    ,  isActive=False)
    samples.AddSample('SingleElectron'                       , path='SingleElectron'    ,  isActive=False)

    samples.AddSample('DYJetsToLL_M-50', 
                      path='DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 
                      isActive=False, useXSFile=True )

    samples.AddSample('DYJetsToLL_M-50PhOlap', 
                      path='DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8PhOlap', 
                      isActive=False, useXSFile=True )

    samples.AddSample('ZGTo2LG', 
                      path='ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', 
                      isActive=False, useXSFile=True )


    # No overlap
    # NLO
    samples.AddSample('WGToLNuG_amcatnloFXFX', 
                      path='WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
                      isActive=False, useXSFile=True, XSName='WGToLNuG-amcatnloFXFX')

    samples.AddSample('WGToLNuG_PtG-130_amcatnloFXFX', 
                      path='WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
                      isActive=False, useXSFile=True, plotColor=ROOT.kViolet, XSName='WGToLNuG_PtG-130-amcatnloFXFX' )

    samples.AddSample('WGToLNuG_PtG-500_amcatnloFXFX', 
                      path='WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
                      isActive=False, useXSFile=True, plotColor=ROOT.kViolet, XSName='WGToLNuG_PtG-500-amcatnloFXFX' )

    # LO
    samples.AddSample('WGToLNuG_madgraphMLM', 
                      path='WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                      isActive=False, useXSFile=True, plotColor=ROOT.kOrange, XSName='WGToLNuG-madgraphMLM' )

    samples.AddSample('WGToLNuG_PtG-130_madgraphMLM', 
                      path='WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                      isActive=False, useXSFile=True, plotColor=ROOT.kViolet, XSName='WGToLNuG_PtG-130-madgraphMLM' )

    samples.AddSample('WGToLNuG_PtG-500_madgraphMLM',
                      path='WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                      isActive=False, useXSFile=True, plotColor=ROOT.kViolet, XSName='WGToLNuG_PtG-500-madgraphMLM' )

    # With overlap
    # NLO
    samples.AddSample('WGToLNuG_amcatnloFXFXPhCutMax', 
                      path='WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8PhCutMax', 
                      isActive=False, useXSFile=True, XSName='WGToLNuG-amcatnloFXFX')

    samples.AddSample('WGToLNuG_PtG-130_amcatnloFXFXPhCutMaxPhCutMin', 
                      path='WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8PhCutMaxPhCutMin', 
                      isActive=False, useXSFile=True, plotColor=ROOT.kViolet, XSName='WGToLNuG_PtG-130-amcatnloFXFX' )

    samples.AddSample('WGToLNuG_PtG-500_amcatnloFXFXPhCutMin', 
                      path='WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8PhCutMin', 
                      isActive=False, useXSFile=True, plotColor=ROOT.kViolet, XSName='WGToLNuG_PtG-500-amcatnloFXFX' )

    # LO
    samples.AddSample('WGToLNuG_madgraphMLMPhCutMax', 
                      path='WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8PhCutMax',
                      isActive=False, useXSFile=True, plotColor=ROOT.kOrange, XSName='WGToLNuG-madgraphMLM' )

    samples.AddSample('WGToLNuG_PtG-130_madgraphMLMPhCutMaxPhCutMin', 
                      path='WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-madgraphMLM-pythia8PhCutMaxPhCutMin',
                      isActive=False, useXSFile=True, plotColor=ROOT.kViolet, XSName='WGToLNuG_PtG-130-madgraphMLM' )

    samples.AddSample('WGToLNuG_PtG-500_madgraphMLMPhCutMin', 
                      path='WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8PhCutMin',
                      isActive=False, useXSFile=True, plotColor=ROOT.kViolet, XSName='WGToLNuG_PtG-500-madgraphMLM' )



    samples.AddSampleGroup( 'Data', legend_name='Data', 
                            input_samples = [
                                             'SingleMuon',
                                             'SingleElectron',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                          )


    samples.AddSampleGroup( 'WgNLO', 
                           input_samples = ['WGToLNuG_amcatnloFXFXPhCutMax', 
                                            'WGToLNuG_PtG-130_amcatnloFXFXPhCutMaxPhCutMin',
                                            'WGToLNuG_PtG-500_amcatnloFXFXPhCutMin',
                                           ],
                           scale=2.,
                          )

    samples.AddSampleGroup( 'WgLO', 
                           input_samples = ['WGToLNuG_madgraphMLMPhCutMax', 
                                            'WGToLNuG_PtG-130_madgraphMLMPhCutMaxPhCutMin',
                                            'WGToLNuG_PtG-500_madgraphMLMPhCutMin',
                                           ],
                           scale=2.,
                          )

    samples.AddSampleGroup(  'ZSumNoOlap', legend_name='Z+Jets',
                           input_samples = ['DYJetsToLL_M-50', 'ZGTo2LG'],
                           plotColor = ROOT.kCyan-2,
                          )

    samples.AddSampleGroup(  'ZSumWithOlap', legend_name='Z+Jets',
                           input_samples = ['DYJetsToLL_M-50PhOlap', 'ZGTo2LG'],
                           plotColor = ROOT.kCyan-2,
                          )
def print_examples() :
    pass

