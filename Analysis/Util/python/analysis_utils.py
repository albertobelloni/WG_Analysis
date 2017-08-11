import os

class Printer() :

    def __init__ (self) :
        self.entries = []

    def AddLine( self, line ) :
        self.entries.append( line )

    def Print(self) :

        # get number of columns
        max_cols = max( [len(line) for line in self.entries ] )
        colwidths = [0]*max_cols

        # collect max length of each column
        for line in self.entries :
            for idx, col in enumerate(line) :
                if len(col) > colwidths[idx] :
                    colwidths[idx] = len(col)

        for line in self.entries :
            print ' '.join( [col.ljust(colwidths[idx]) for idx, col in enumerate(line) ] )

def read_xsfile( file, lumi, print_values=False ) :
    print '-------------------------------------'
    print ' LOAD CROSS SECTION INFO'
    print '-------------------------------------'
    weightMap = {}
    if file is None :
        return weightMap
    if lumi is None :
        print 'Cannot calculate weights without a luminosity'
        return weightMap
    if not os.path.isfile( file ) :
        print 'Could not locate cross section file.  No values will be loaded.'
        return weightMap

    ofile = open( file )
    xsdict = eval( ofile.read() )
    xs_printer = Printer()
    for name, values in xsdict.iteritems() :

        lumi_sample_den = values['cross_section']*values['gen_eff']*values['k_factor']
        if lumi_sample_den == 0 :
            print 'Cannot calculate cross section for %s.  It will receive a weight of 1.' %name
            lumi_sample = lumi
            xs_printer.AddLine( ['Sample %s ' %name, 'cross section : %f pb' %values['cross_section'], 'N Events : %d' %(values['n_evt']), 'sample lumi : %f' %(lumi_sample), 'Scale : ERROR' ] )
        else :
            lumi_sample = values['n_evt']/float(lumi_sample_den)

        lumi_scale = float(lumi)/lumi_sample;
        xs_printer.AddLine( ['Sample %s ' %name, 'cross section : %f pb' %values['cross_section'], 'N Events : %d' %(values['n_evt']), 'sample lumi : %f' %(lumi_sample), 'Scale : %f' %lumi_scale ] )

        weightMap[name] = {}  
        weightMap[name]['scale'] = lumi_scale
        weightMap[name]['cross_section'] = values['cross_section']

    if print_values :
        xs_printer.Print()

    return weightMap

