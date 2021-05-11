#!/usr/bin/env python
execfile("MakeBase.py")
from uncertainties import ufloat

###
### This script makes N-1/ final selection distribution plots
###

year = options.year

ch = "el"
if ch=="el":
    sampManElG.ReadSamples( _SAMPCONF )
    samples = sampManElG
else:
    sampManMuG.ReadSamples( _SAMPCONF )
    samples = sampManMuG

sel, weight =  defs.makeselstring( ch = ch, phpt = 40, leppt = 25, met = 0 )
masscut  = "&& mt_res>900"
#selection = "%s_n==1 && ph_n==1 && %s" %(ch, masscut)
sel += masscut
sf = samples.SetFilter(sel).SetDefine("weight",weight)
counterdict={}


setuparray = [ (ch,),
          #( 50, 80, 100, 120, 150, 180, 200, 220, 250, 300), ## phpt
          ( 30, 200, 250, 300, 400,  500), ## phpt
          ( 35, 50,  150), #leppt
          (  40, 60, 100,  300), #metpt
        ]
#setuparray = [ (ch,),
#          ( 30, 150, 200, 250, 300, 500),
#          ( 25, 40, 60, 150),
#          ( 20, 30, 50),
#        ]

setups = product(*setuparray)
## you might want to rescale to 1/N_total but for comparison between same signal model, this has no effect
#signalname = "MadGraphResonanceMass300_width5"
signalname = "MadGraphResonanceMass800_width5"
samples.activate_sample(signalname)
samples.deactivate_sample("MadGraphResonanceMass300_width5")
samples.deactivate_sample("MadGraphResonanceMass250_width5")
samples.deactivate_sample("MadGraphResonanceMass450_width5")
samples.deactivate_sample("MadGraphResonanceMass600_width0p01")
signalnames= [s.name for s in samples.get_samples(isSignal=True,isActive=True)]
samples.deactivate_all_samples()
samples.activate_sample(signalnames)
samples.activate_sample("WGamma")



for setup in setups:
    sel, w =  defs.makeselstring( *setup )
    print "%s ph %g lep %g met %g" %setup, sel
    hf = sf.SetFilter(sel).SetCount()
    counterdict[setup] = hf

sgslist = {}
for signalname in signalnames:
    print
    print signalname
    print
    sgslist[signalname] = []
    for setup, hf in counterdict.iteritems():
        counts = hf.ShowCount()
        sig = counts[signalname]
        bkg = counts["TOTAL"]
        sgf = sig[0]/sqrt(bkg[0])
        print sig, bkg, sgf
        sgslist[signalname].append((setup,ufloat(*sig),ufloat(*bkg),sgf))

    sgslist[signalname].sort(key=lambda x: -x[-1])

for signalname in signalnames:
    print
    print signalname
    print
    for s in sgslist[signalname][:10]:
         print "%s ph %g lep %g met %g "%s[0], "sig %s bkg %s S/sqrt(B) %g" %s[1:]
