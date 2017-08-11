

def config_samples(samples) :

    import ROOT
    samples.AddSample('_SinglePhoton'   , path='SinglePhoton'    ,  isActive=False, isData=False, scale=1.0 )
    samples.AddSample('_JetHT'   , path='JetHT'    ,  isActive=False, isData=False, scale=1.0 )


    samples.AddSample('DiPhoton_M40_80', path='DiPhotonJetsBox_M40_80-Sherpa', isActive=False, useXSFile=True )
    samples.AddSample('DiPhoton_M80toInf', path='DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa', isActive=False, useXSFile=True)

    samples.AddSample('GJet_Pt-15ToInf', path='GJet_Pt-15ToInf_TuneCUETP8M1_13TeV-pythia8', isActive=False )

    samples.AddSample('QCD_Pt_10to15', path='QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8', isActive=False, useXSFile=True  )
    samples.AddSample('QCD_Pt_15to30', path='QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8', isActive=False )
    samples.AddSample('QCD_Pt_30to50', path='QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8', isActive=False )
    samples.AddSample('QCD_Pt_50to80', path='QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8', isActive=False )
    samples.AddSample('QCD_Pt_80to120', path='QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8', isActive=False )
    samples.AddSample('QCD_Pt_120to170', path='QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8', isActive=False )
    samples.AddSample('QCD_Pt_170to300', path='QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8', isActive=False )

    samples.AddSample('QCD_Pt-15to20_EMEnriched', path='QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8', isActive=False )
    samples.AddSample('QCD_Pt-20to30_EMEnriched', path='QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8', isActive=False )
    samples.AddSample('QCD_Pt-30to50_EMEnriched', path='QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8', isActive=False )
    samples.AddSample('QCD_Pt-50to80_EMEnriched', path='QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8', isActive=False )
    samples.AddSample('QCD_Pt-80to120_EMEnriched', path='QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8', isActive=False )
    samples.AddSample('QCD_Pt-120to170_EMEnriched', path='QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8', isActive=False )
    samples.AddSample('QCD_Pt-170to300_EMEnriched', path='QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8', isActive=False )
    samples.AddSample('QCD_Pt-300toInf_EMEnriched', path='QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8', isActive=False )

    samples.AddSample('DYJetsToLL', path='DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', isActive=False, useXSFile=True  )
    samples.AddSample('WJetsToLNu', path='WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8', isActive=False, useXSFile=True  )

    samples.AddSample('MultiJet', path='job_MultiJet_2012a_Jan22rereco', isActive=True )


    samples.AddSampleGroup( 'Data', legend_name='Single Photon Data', 
                            input_samples = [
                                             '_SinglePhoton',
                                            ],
                           isData = True,
                          )

    samples.AddSampleGroup( 'GJet', legend_name='#gamma + jet', 
                            input_samples = [
                                             'GJet_Pt-15ToInf',
                                            ],
                           plotColor=ROOT.kYellow-2,
                          )

    samples.AddSampleGroup( 'DiPhoton', legend_name='#gamma #gamma', 
                            input_samples = [
                                             'DiPhoton_M40_80',
                                             'DiPhoton_M80toInf',
                                            ],
                           plotColor=ROOT.kBlue+7,
                           isActive=True,
                          )

    samples.AddSampleGroup( 'QCD', legend_name='QCD', 
                            input_samples = [
                                              'QCD_Pt_10to15',
                                              'QCD_Pt_15to30',
                                              'QCD_Pt_30to50',
                                              'QCD_Pt_50to80',
                                              'QCD_Pt_80to120',
                                              'QCD_Pt_120to170',
                                              'QCD_Pt_170to300',
                                            ],
                           plotColor=ROOT.kRed-2,
                          )

    samples.AddSampleGroup( 'QCDEMEnriched', legend_name='QCD, EM Enriched', 
                            input_samples = [
                                             'QCD_Pt-15to20_EMEnriched',
                                             'QCD_Pt-20to30_EMEnriched',
                                             'QCD_Pt-30to50_EMEnriched',
                                             'QCD_Pt-50to80_EMEnriched',
                                             'QCD_Pt-80to120_EMEnriched',
                                             'QCD_Pt-120to170_EMEnriched',
                                             'QCD_Pt-170to300_EMEnriched',
                                             'QCD_Pt-300toInf_EMEnriched',
                                            ],
                           plotColor=ROOT.kRed-5,
                          )


    samples.AddSampleGroup( 'SinglePhoton', legend_name='Single Photon',
                      input_samples = [
                                        '_SinglePhoton',
                      ],
                      isData=False,
                           isActive=False,
                     )

    samples.AddSampleGroup( 'JetHT', legend_name='JetHT',
                      input_samples = [
                                        '_JetHT',
                      ],
                      isData=False, isActive=False ,
                     )


    samples.AddSampleGroup( 'Zgammastar', legend_name='Z', 
                      input_samples=['DYJetsToLL'], isActive=False )

    samples.AddSampleGroup( 'WJets', legend_name='W', 
                      input_samples=['WJetsToLNu'], isActive=False  )




def print_examples() :
    pass
