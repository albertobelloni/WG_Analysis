from core import Filter
import inspect
import sys

def get_remove_filter() :
    """ Define list of regex strings to filter input branches to remove from the output.
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableRemoveFilter on the command line.
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return []

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
    nph_cut = args.get('nph_cut' , ' == 0 ' )

    filter_event = Filter('FilterPhoton')
    filter_event.cut_genph_pt = pt_cut
    filter_event.cut_n_gen_phot = nph_cut

    alg_list.append( filter_event )

def filter_genht( alg_list, args ) :

    genht_cut = args.get('genht_cut', None )

    if genht_cut is not None :

        filter_event = Filter('FilterGenHT')
        filter_event.cut_genht = genht_cut

        alg_list.append( filter_event )

def filter_mtres( alg_list, args ) :

    mtres_cut = args.get('mtres_cut', None )

    if mtres_cut is not None :

        filter_event = Filter('FilterMTRes')
        filter_event.cut_mtres = mtres_cut

        alg_list.append( filter_event )


