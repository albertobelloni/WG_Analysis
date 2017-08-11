from core import Filter
import os
import sys

def get_remove_filter() :

    return ['EvtWeights']

def get_keep_filter() :

    #return ['Evt.*', 'MET.*', 'GPdf.*', 'GPhotPt', 'GPhotEta', 'GPhotPhi', 'GPhotE' ,'GPhotSt', 'GPhotMotherId']
    return ['Evt.*', 'GPdf.*', 'GPhot.*']

def config_analysis( alg_list, args ) :

    truth_filt = Filter('BuildTruth') 
    #truth_filt.cut_ph_pt = ' > 5 '
    truth_filt.cut_ph_status = ' == 1 '
    #truth_filt.cut_ph_mother = ' <= 25 '
    truth_filt.cut_ph_IsPromptFinalState = ' == True '
    #truth_filt.cut_ph_FromHardProcessFinalState = ' == True '

    alg_list.append( truth_filt )

    alg_list.append( weight_event(args) )


def weight_event( args ) :

    filt = Filter( 'WeightEvent' )

    filt_str = args.get( 'ApplyNLOWeight', 'false' )

    filt.add_var( 'ApplyNLOWeight', filt_str )

    return filt

