

def config_samples(samples) :

    import ROOT
    samples.AddSample('DoubleMuon'   , path='DoubleMuon'    ,  isActive=False, scale=1.0 )
    samples.AddSample('DoubleEG'   , path='DoubleEG'    ,  isActive=False, scale=1.0 )

    samples.AddSample('DYJetsToLL'        , path='DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         ,  isActive=False, useXSFile=True )
    samples.AddSample('Zg'                , path='ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         ,  isActive=False, useXSFile=True )
    samples.AddSample('WJets'             , path='WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         ,  isActive=False, useXSFile=True )
    samples.AddSample('TTbar'             , path='TT_TuneCUETP8M1_13TeV-powheg-pythia8'         ,  isActive=False, useXSFile=True )

    samples.AddSample('_WW'                , path='WWTo2L2Nu_13TeV-powheg'         ,  isActive=False, useXSFile=True, XSName='WW' )
    samples.AddSample('WZ3LNLO'           , path='WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         ,  isActive=False, useXSFile=True )
    samples.AddSample('_ZZ'                , path='ZZ_TuneCUETP8M1_13TeV-pythia8'         ,  isActive=False, useXSFile=True, XSName='ZZ' )
    samples.AddSample('ST_TW'             , path='ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1'         ,  isActive=False, useXSFile=True )
    samples.AddSample('ST_TbarW'          , path='ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1'         ,  isActive=False, useXSFile=True )
    samples.AddSample('STsCh'             , path='ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1'         ,  isActive=False, useXSFile=True )

    #samples.AddSample('MultiJet', path='job_MultiJet_2012a_Jan22rereco', isActive=True )

    samples.AddSampleGroup( 'Muon', legend_name='Muon', 
                            input_samples = [
                                             'DoubleMuon',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=False,
                           isActive=False
                          )

    samples.AddSampleGroup( 'Electron', legend_name='Electron', 
                            input_samples = [
                                             'DoubleEG',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=False,
                           isActive=False
                          )

    samples.AddSampleGroup( 'Data', legend_name='Data', 
                            input_samples = [
                                             'DoubleMuon',
                                             'DoubleEG',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                          )

    samples.AddSampleGroup( 'Zgammastar', legend_name='Z/#gamma * ', 
                            input_samples = [
                                             'DYJetsToLL'
                                            ],
                           plotColor=ROOT.kCyan,
                          )
    samples.AddSampleGroup( 'Zgamma', legend_name='Z#gamma', 
                           input_samples = [
                                            'Zg',
                           ],
                           plotColor=ROOT.kOrange-4,
                           isSignal=False,
                          )
    samples.AddSampleGroup( 'Top', legend_name='Top', 
                           input_samples = [
                                            'TTbar',
                           ],
                           plotColor=ROOT.kGreen-2,
                           isSignal=False,
                          )
    samples.AddSampleGroup( 'SingleTop', legend_name='Single Top', 
                           input_samples = [
                                            'ST_TW',
                                            'ST_TbarW',
                                            'STsCh',
                           ],
                           plotColor=ROOT.kGreen-4,
                          )

    samples.AddSampleGroup( 'WW', legend_name='WW', 
                           input_samples = [
                                            '_WW',
                           ],
                           plotColor=ROOT.kBlue-10,
                          )

    samples.AddSampleGroup( 'WWWZ', legend_name='WZ/ZZ', 
                           input_samples = [
                                            'WZ3LNLO',
                                            '_ZZ',
                           ],
                           plotColor=ROOT.kGray,
                           ) 

    samples.AddSampleGroup( 'InclusiveW', legend_name='Inclusive W', 
                           input_samples = [
                                            'WJets',
                           ],
                           plotColor=ROOT.kMagenta-4,
                           isSignal=False,
                          )





def print_examples() :
    pass
