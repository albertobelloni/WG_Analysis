

def config_samples(samples) :

    import ROOT
    samples.AddSample('SingleMuon'   , path='SingleMuon'    ,  isActive=False, scale=1.0 )
    samples.AddSample('SingleElectron'   , path='SingleElectron'    ,  isActive=False, scale=1.0 )

    samples.AddSample('WJets'             , path='WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         ,  isActive=False, useXSFile=True )
    samples.AddSample('Wg'                , path='WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         ,  isActive=False, useXSFile=True )
    samples.AddSample('DYJetsToLL'        , path='DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         ,  isActive=False, useXSFile=True )
    samples.AddSample('Zg'                , path='ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         ,  isActive=False, useXSFile=True )
    samples.AddSample('TTbar'             , path='TT_TuneCUETP8M1_13TeV-powheg-pythia8'         ,  isActive=False, useXSFile=True )
    samples.AddSample('WW'                , path='WWTo2L2Nu_13TeV-powheg'         ,  isActive=False, useXSFile=True )
    samples.AddSample('WZ3LNLO'           , path='WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'         ,  isActive=False, useXSFile=True )
    samples.AddSample('ZZ'                , path='ZZ_TuneCUETP8M1_13TeV-pythia8'         ,  isActive=False, useXSFile=True )
    samples.AddSample('ST_TW'             , path='ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1'         ,  isActive=False, useXSFile=True )
    samples.AddSample('ST_TbarW'          , path='ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1'         ,  isActive=False, useXSFile=True )
    samples.AddSample('STsCh'             , path='ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1'         ,  isActive=False, useXSFile=True )


    #samples.AddSample('MultiJet', path='job_MultiJet_2012a_Jan22rereco', isActive=True )

    samples.AddSampleGroup( 'Data', legend_name='Data', 
                            input_samples = [
                                             'SingleMuon',
                                             'SingleElectron',
                                            ],
                           plotColor=ROOT.kBlack,
                           isData=True,
                          )

    samples.AddSampleGroup( 'InclusiveW', legend_name='Inclusive W', 
                           input_samples = [
                                            'WJets',
                           ],
                           plotColor=ROOT.kMagenta-4,
                          )

    samples.AddSampleGroup( 'Wgamma', legend_name='W#gamma', 
                           input_samples = [
                                            'Wg',
                           ],
                           plotColor=ROOT.kBlue-6,
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
                          )
    samples.AddSampleGroup( 'Top', legend_name='Top', 
                           input_samples = [
                                            'TTbar',
                           ],
                           plotColor=ROOT.kGreen-2,
                          )

    samples.AddSampleGroup( 'SingleTop', legend_name='Single Top', 
                           input_samples = [
                                            'ST_TW',
                                            'ST_TbarW',
                                            'STsCh',
                           ],
                           plotColor=ROOT.kGreen-4,
                          )

    samples.AddSampleGroup( 'MultiBoson', legend_name='Multi Boson', 
                           input_samples = [
                                            'WW',
                                            'WZ3LNLO',
                                            'ZZ',
                           ],
                           plotColor=ROOT.kBlue-10,
                          )





def print_examples() :
    pass
