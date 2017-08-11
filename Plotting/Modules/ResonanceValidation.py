

def config_samples(samples) :

    import ROOT
    samples.AddSample('ChargedResonance_WGToLNu_M200_width1'   , path='ChargedResonance_WGToLNu_M1000_width1'    ,  isActive=True, isSignal=True, sigLineStyle=1, plotColor=ROOT.kRed )
    samples.AddSample('ChargedResonance_WGToLNu_M200_width10'   , path='ChargedResonance_WGToLNu_M1000_width10'    ,  isActive=True, isSignal=True, sigLineStyle=1, plotColor=ROOT.kBlue )
    samples.AddSample('ChargedResonance_WGToLNu_M200_width20'   , path='ChargedResonance_WGToLNu_M1000_width20'    ,  isActive=True, isSignal=True, sigLineStyle=1, plotColor=ROOT.kGreen  )



def print_examples() :
    pass
