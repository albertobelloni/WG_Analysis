import re
import os

def find_version_dir(config_file, version_key ):
    """Find the version of the results used from the latex config file"""

    output = None

    # open the file
    try :
        input_conf_file = open( config_file, 'r' )
    except IOError :
        print 'Could not open file, %s' %config_file
        return output

    # loop over the file, find the matching key
    for line in input_conf_file :
        match_str = r'\\newcommand{\\%s}{(\w+)' %version_key
        res = re.match( match_str, line )
        if res is not None : #found the key, store it
            output = res.group(1)

    input_conf_file.close()

    return output

def run_funcs_on_files( base_dirs, file_key, funcs, args={}) : 

    if not isinstance( funcs, list ) :
        funcs = [funcs]

    for base_dir in base_dirs :

        input_files = find_files( base_dir, file_key )

        func_args = []
        for f in input_files :
            arg_dic = {'input_file' : f}
            for inkey, inval in args.iteritems() :
                arg_dic[inkey] = inval
            func_args.append( arg_dic )

        for f in funcs :
            try :
                map( f , func_args )
            except :
                print 'FAILED TO RUN FUNC, %s'%( f.__name__,  )
                raise

def find_files( base_dir, file_key ) :

    input_files = []
    for top, dirs, files in os.walk( base_dir ) :

        for f in files :
            res = re.match( file_key, f )
            if res is not None :
                input_files.append( top + '/' + f )

    return input_files

def find_files_with_res( base_dir, file_key ) :

    input_files = []
    for top, dirs, files in os.walk( base_dir ) :

        for f in files :
            res = re.match( file_key, f )
            if res is not None :
                input_files.append( ( top + '/' + f, res ) )

    return input_files



class latex_table :
    def __init__(self, in_tab=None) :

        self.header =''
        self.columns = []
        self.rows = []
        self.dividers = []
        self.table = []
        self.row_postfix = {}
        self.footer = ''

        if in_tab is not None :
            self.header  = in_tab.header
            self.columns = in_tab.columns
            self.table   = in_tab.table 
            self.footer  = in_tab.footer

    #def getColumn( self, colname ) :
    #    for tcol in self.table.keys() :
    #        if tcol.count(colname) :
    #            return self.table[tcol]

    #def replaceColumn( self, colname, newcol ) :
    #    for tcol in self.table.keys() :
    #        if tcol.count(colname) :
    #            self.table[tcol] = newcol

    def write( self, fname ) :
        ofile = open( fname, 'w' )

        print 'Write table %s '%fname

        ofile.write( self.get_header_str())
        #ofile.write( self.get_column_str())
        ofile.write( self.get_table_str() )
        ofile.write( self.get_footer_str())

        ofile.close()

    def parse_file( self, fname ) :
        if not os.path.isfile( fname ) :
            print 'Input file does not exist'
            return 

        ofile = open( fname, 'r' )

        last_sline=''
        for idx, line in enumerate(ofile) :
            sline = line.rstrip('\n')
            last_sline=sline
            if idx == 0 :
                self.header = sline
                continue
            elif idx == 1 :
                self.columns = sline.split( '&' )
                continue
            else :

                if sline.count('&') :
                    entries = sline.split('&')
                    
                    for entry, col in zip(entries, self.columns ) :
                        self.table.append( (col, entry,None ) )

            self.footer=last_sline

        ofile.close()

    def Print(self) :
        print self.get_header_str()
        print self.get_column_str()
        print self.get_table_str()
        print self.get_footer_str()

    def get_table_str( self ) :

        row_entries = []
        for idx, (lab, entries, postfix) in enumerate(self.table) :
            row_str = ''
            row_str += ( lab )
            if entries :
                row_str += ' & '
            row_str += ' & '.join( entries )
            row_str += r' \\ '
            if postfix is not None :
                row_str += postfix

            if idx in self.dividers :
                row_str += ' \hline '

            row_entries.append(row_str)

        row_entries[-1] += ' \hline '
        return ' \n '.join(row_entries )


    #def get_table_str( self ) :
    #    row_entries = []
    #    nlines = len( self.table.values()[0] )
    #    for line in range(0, nlines ) :
    #        line_entries = []
    #        for col in self.columns :
    #            line_entries.append( self.table[col][line] )

    #        row_entries.append(' & '.join(line_entries) + r'  \\')
    #    return '\n'.join(row_entries) + '\n'

    def get_header_str(self) :
        return self.header + '\n'

    def get_column_str(self) :
        return ' & '.join(self.columns) + r'  \\ \hline' + '\n'

    def get_footer_str(self) :
        return '\n' + self.footer + '\n'

    #def add_column( self, col, entries ) :
    #    self.columns.append( col )
    #    self.table[col] = entries

    def add_row( self, row, entries, postfix=None ) :
        self.table.append( ( row, entries, postfix ) )

    def add_divider( self ) :
        self.dividers.append( len(self.table)-1 )

    def show_latex_table( self ) :

        if not os.path.isdir( 'tmp' ) :
            os.mkdir( 'tmp' )

        self.write( 'tmp/tmp.tex' )
        ftable = open( 'tmp/table.tex', 'w' )

        ftable.write( r'\documentclass[12pt]{article}' + '\n' )
        ftable.write( r'\usepackage{pbox}'  + '\n' )
        ftable.write( r'\begin{document}' + '\n' )
        ftable.write( r'\begin{table}' + '\n' )
        ftable.write( r'\tiny' + '\n' )
        ftable.write( r'\input{tmp.tex}' + '\n' )
        ftable.write( r'\end{table}' + '\n' )
        ftable.write( r'\end{document}' + '\n' )

        print ( 'latex -output-directory ${PWD}/tmp ${PWD}/tmp/table.tex; dvipdf ${PWD}/tmp/table.dvi ${PWD}/tmp/table.pdf ; acroread ${PWD}/tmp/table.pdf &' )


