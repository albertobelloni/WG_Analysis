

def config_samples(samples) :

    import ROOT
    samples.AddSample('Data'                           , path='job_summer12_WgTest'          ,  isActive=True, useXSFile=True, plotColor=ROOT.kBlack, isData=True, XSName='Wg' )
    #samples.AddSample('WgPt0-20'                   , path='job_summer12_WgPt0-20'          ,  isActive=True, useXSFile=True, plotColor=ROOT.kYellow+2, XSName='Wg' )
    #samples.AddSample('WgPt20-30'                   , path='job_summer12_WgPt20-30'          ,  isActive=True, useXSFile=True, plotColor=ROOT.kRed, scale=5.3 )
    #samples.AddSample('WgPt30-50'                   , path='job_summer12_WgPt30-50'          ,  isActive=True, useXSFile=True, plotColor=ROOT.kBlue, scale=5.16 )
    #samples.AddSample('WgPt50-130'                   , path='job_summer12_WgPt50-130'          ,  isActive=True, useXSFile=True, plotColor=ROOT.kGreen, scale=4.21 )
    #samples.AddSample('WgPt130'                   , path='job_summer12_WgPt130'          ,  isActive=True, useXSFile=True, plotColor=ROOT.kMagenta, scale=1.45 )

    samples.AddSample('WgPt20-30'                   , path='job_summer12_WgPt20-30Test'      ,  isActive=False, useXSFile=True, plotColor=ROOT.kRed, )
    samples.AddSample('WgPt30-50'                   , path='job_summer12_WgPt30-50Test'      ,  isActive=False, useXSFile=True, plotColor=ROOT.kBlue, )
    samples.AddSample('WgPt50-130'                   , path='job_summer12_WgPt50-130New'    ,  isActive=False, useXSFile=True, plotColor=ROOT.kGreen,)
    samples.AddSample('WgPt130'                   , path='job_summer12_WgPt130Test'          ,  isActive=False, useXSFile=True, plotColor=ROOT.kMagenta,)

    samples.AddSampleGroup( 'WgComb', 
                           input_samples = [
                                            'WgPt20-30',
                                            'WgPt30-50',
                                            'WgPt50-130',
                                            'WgPt130',
                           ],
                           plotColor=ROOT.kOrange,
                          )

def print_examples() :
    pass
