from core import Filter
import inspect
import sys
import os

def get_remove_filter() :
    """ Define list of regex strings to filter input branches to remove from the output.
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableRemoveFilter on the command line.
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return ['']

def get_keep_filter() :
    """ Define list of regex strings to filter input branches to retain in the output.  
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableKeepFilter on the command line
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return []

def config_analysis( alg_list, args ) :
    """ Configure analysis modules. Order is preserved """

    # run on the function provided through
    # the args
    for s in inspect.getmembers(sys.modules[__name__]) :
        if s[0] == args['function'] :
            print '*********************************'
            print 'RUN %s' %( args['function'] )
            print '*********************************'
            s[1]( alg_list, args )

def filter_photon( alg_list, args ) :

    pt_cut = args.get('pt_cut' , ' > 10 ' )
    leadpt_cut = args.get('leadpt_cut' , None )
    aeta_cut = args.get('aeta_cut' , None )
    dr_cut = args.get('dr_cut' , None )
    nph_cut = args.get('nph_cut' , ' == 0 ' )
    isPromptFS_cut = args.get('isPromptFS_cut', None )
    fhpfs_cut = args.get('fhpfs_cut', None)
    isr_cut = args.get('isr_cut' , None)
    wg_cut = args.get('wg_cut', None)

    filter_event = Filter('FilterPhoton')
    filter_event.cut_genph_pt = pt_cut
    if wg_cut:
        filter_event.cut_genph_wg = wg_cut
    if leadpt_cut:
        filter_event.cut_lead_genph_pt = leadpt_cut
    if aeta_cut:
        filter_event.cut_genph_aeta = aeta_cut
    if dr_cut:
        filter_event.cut_genph_dr = dr_cut
    filter_event.cut_n_gen_phot = nph_cut
    if isPromptFS_cut:
        filter_event.cut_genph_isPromptFS = isPromptFS_cut
    if fhpfs_cut:
        filter_event.cut_genph_FHPFS = fhpfs_cut
    if isr_cut:
        filter_event.cut_genph_isr = isr_cut

    alg_list.append( filter_event )

def filter_genht( alg_list, args ) :

    trueht_cut = args.get('trueht_cut', None )

    if trueht_cut is not None :

        filter_event = Filter('FilterTrueHT')
        filter_event.cut_trueht = trueht_cut

        alg_list.append( filter_event )

def filter_mtres( alg_list, args ) :

    mtres_cut = args.get('mtres_cut', None )

    if mtres_cut is not None :

        filter_event = Filter('FilterMTRes')
        filter_event.cut_mtres = mtres_cut

        alg_list.append( filter_event )

def filter_wpt( alg_list, args ) :

    truewpt_cut = args.get('truewpt_cut', None )

    if truewpt_cut is not None :

        filter_event = Filter('FilterTrueWPt')
        filter_event.cut_truewpt = truewpt_cut

        alg_list.append( filter_event )

def apply_wpt_kneg( alg_list, args ) :
    
    truewpt_bound_lo = args.get('truewpt_bound_lo', 0. )
    truewpt_bound_hi = args.get('truewpt_bound_hi', 13000. )
    truewpt_kneg_lo  = args.get('truewpt_kneg_lo',  1. )
    truewpt_kneg_hi  = args.get('truewpt_kneg_hi',  1. )

    if (truewpt_kneg_lo != 1. or 
        truewpt_kneg_hi != 1.):

        filter_event = Filter('ApplyTrueWPtKNeg')
        filter_event.add_var( 'truewpt_bound_lo', truewpt_bound_lo )
        filter_event.add_var( 'truewpt_bound_hi', truewpt_bound_hi )
        filter_event.add_var( 'truewpt_kneg_lo',  truewpt_kneg_lo  )
        filter_event.add_var( 'truewpt_kneg_hi',  truewpt_kneg_hi  )

        alg_list.append( filter_event )

def filter_combined( alg_list, args ) :
    
    filter_photon( alg_list, args )
    filter_genht( alg_list, args )
    filter_mtres( alg_list, args )
    filter_wpt( alg_list, args )
    apply_wpt_kneg( alg_list, args )
