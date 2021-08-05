
""" usage: echo qq | python scanTFileContent.py /[path].root | less -S  """

import ROOT
import sys
f = ROOT.TFile(sys.argv[1])
t=f.Get("UMDNTuple/EventTree")
#t.Print("toponly")
#t.Print("pref*")
lbranch = t.GetListOfBranches()
lb = [lbranch.At(i).GetName() for i in range(lbranch.GetEntries())]
#print lb
lb = [b for b in lb if b != "EventWeights"]
excludes  = ["Flag","EventWeights","ph_pass"]
includes  = ["EventWeights[0]",]
for exclu in excludes:
    lb = [b for b in lb if b.find(exclu)==-1]
lb+=includes
print lb
t.Scan(":".join(lb))#,'Entry$<10')
