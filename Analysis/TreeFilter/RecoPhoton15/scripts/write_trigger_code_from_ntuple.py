import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--file', dest='file', required=True, help='path to ntuple' )
parser.add_argument( '--treeName', dest='treeName', required=True, help='name of tree' )

options = parser.parse_args()

keep_triggers = [
    'HLT_Photon22',
    'HLT_Photon30',
    'HLT_Photon36',
    'HLT_Photon50',
    'HLT_Photon75',
    'HLT_Photon90',
    'HLT_Photon120_R9Id90_HE10_Iso40_EBOnly',
    'HLT_Photon120_R9Id90_HE10_IsoM',
    'HLT_Photon120',
    'HLT_Photon135_PFMET100_JetIdCleaned',
    'HLT_Photon165_HE10',
    'HLT_Photon165_R9Id90_HE10_IsoM',
    'HLT_Photon175',
    'HLT_Photon250_NoHE',
    'HLT_Photon300_NoHE',
    'HLT_Photon500',
    'HLT_Photon600',
    'HLT_Mu8',
    'HLT_Mu17',
    'HLT_Mu20',
    'HLT_Mu24',
    'HLT_Mu27',
    'HLT_Mu34',
    'HLT_Mu50',
    'HLT_Mu55',
    'HLT_Mu300',
    'HLT_Mu350',
    'HLT_IsoMu17_eta2p1',
    'HLT_IsoMu20',
    'HLT_IsoMu20_eta2p1',
    'HLT_IsoMu24',
    'HLT_IsoMu24_eta2p1',
    'HLT_IsoMu27',
    'HLT_IsoTkMu20',
    'HLT_IsoTkMu22',
    'HLT_IsoTkMu24',
    'HLT_IsoTkMu20_eta2p1',
    'HLT_IsoTkMu24_eta2p1',
    'HLT_IsoTkMu27',
    'HLT_TkMu20',
    'HLT_Mu24_eta2p1',
    'HLT_TkMu24_eta2p1',
    'HLT_TkMu27',
    'HLT_Mu45_eta2p1',
    'HLT_Mu50_eta2p1',
    'HLT_IsoMu22',
    'HLT_Ele22_eta2p1_WPLoose_Gsf',
    'HLT_Ele22_eta2p1_WPTight_Gsf',
    'HLT_Ele23_WPLoose_Gsf',
    'HLT_Ele24_eta2p1_WPLoose_Gsf',
    'HLT_Ele25_WPTight_Gsf',
    'HLT_Ele27_WPTight_Gsf',
    'HLT_Ele25_eta2p1_WPLoose_Gsf',
    'HLT_Ele25_eta2p1_WPTight_Gsf',
    'HLT_Ele27_eta2p1_WPLoose_Gsf',
    'HLT_Ele27_eta2p1_WPTight_Gsf',
    'HLT_Ele32_eta2p1_WPLoose_Gsf',
    'HLT_Ele32_eta2p1_WPTight_Gsf',
    'HLT_Ele105_CaloIdVT_GsfTrkIdT',
    'HLT_Ele115_CaloIdVT_GsfTrkIdT',
    'HLT_Mu17_Mu8',
    'HLT_Mu17_Mu8_DZ',
    'HLT_Mu20_Mu10',
    'HLT_Mu20_Mu10_DZ',
    'HLT_Mu27_TkMu8',
    'HLT_Mu30_TkMu11',
    'HLT_Mu40_TkMu11',
    'HLT_Mu17_Photon30_CaloIdL_L1ISO',
]

def main() :

    ofile = ROOT.TFile.Open( options.file, 'READ' )

    trigtree = ofile.Get( options.treeName ) 

    print trigtree

    trig_branches = []
    other_branches = []

    for br in trigtree.GetListOfBranches() : 
        branch_name = br.GetName()

        if branch_name.count('Trig') :
            trig_branches.append( branch_name )
        else :
            other_branches.append( branch_name )

    trigger_entries = {}

    for event in trigtree : 
        for trig_br in trig_branches :
            trigger_entries.setdefault( trig_br, [] )
            obj_list = getattr( trigtree, trig_br )
            print trig_br
            for idx, entry in enumerate( obj_list ) :
                print entry
                if entry :
                    if entry in keep_triggers :
                        trigger_entries[trig_br].append( (idx+1, 'passTrig_'+entry ))

    print trigger_entries

    max_trig_length = 0

    for triggers in trigger_entries.values() :
        for idx, trig in triggers :
            trig_len = len( trig ) 
            if trig_len > max_trig_length :
                max_trig_length = trig_len

    for trig_obj, triggers in trigger_entries.iteritems() :
        print '    //Declare triggers for %s' %trig_obj
        for idx, trig in triggers :
            print '    Bool_t ' + trig.ljust( max_trig_length) + ';'

    for trig_obj, triggers in trigger_entries.iteritems() :
        print ' //Set trigger branches for %s' %trig_obj
        for idx, trig in triggers :
            print '    outtree->Branch(' + ('"' + trig + '"').ljust( max_trig_length+2) +', &OUT::' + trig.ljust(max_trig_length) + (', "' + trig + '/O"').ljust(max_trig_length+6)+' );' 

    for trig_obj, triggers in trigger_entries.iteritems() :
        print '    //Fill trigger branches for %s' %trig_obj
        for idx, trig in triggers :
            print '    OUT::' + trig.ljust( max_trig_length) + ' = (IN::%s & ( ULong64_t(1) << %d ) ) == ( ULong64_t(1) << %d ); ' %(  trig_obj, idx-1, idx-1 )


    #for obj in trigtree.GetListOfBranches() : 
    #    field_name = obj.GetName()

    #    print field_name

    #    if field_name.count('Trig') :

    #        branch = trigtree.GetBranch(field_name)
    #        print branch

    #        print branch.GetNleaves()
    #        for obj in branch.GetListOfLeaves(): 
    #            print obj.GetName()
    #        for obj in branch.GetListOfBaskets() :
    #            print obj.GetName()




main()
