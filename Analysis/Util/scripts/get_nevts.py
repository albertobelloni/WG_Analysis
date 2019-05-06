import ROOT

base = '/eos/cms/store/group/phys_smp/ggNtuples/data'
job_conf = [
           'job_electron_2012a_Jan22rereco',
           'job_electron_2012b_Jan22rereco',
           'job_electron_2012c_Jan2012rereco',
           'job_electron_2012d_Jan22rereco',
           'job_muon_2012a_Jan22rereco',
           'job_muon_2012b_Jan22rereco',
           'job_muon_2012c_Jan22rereco',
           'job_muon_2012d_Jan22rereco',

]

for i in job_conf :

    #file = ROOT.TFile.Open('root://eoscms.cern.ch/%s/%s/histograms.root' %(base, i))
    file = ROOT.TFile.Open('root://eoscms.cern.ch/%s/%s.root' %(base, i))
    hist = file.Get('ggNtuplizer/hEvents')
    nevt = hist.GetBinContent(1)

    print '%s : %d' %( i, nevt )
