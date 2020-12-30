class SampleInfo() :

   """ used to load workspace and provide necessary information to make data card """

   def __init__(self, **kwargs ):

       # basic information

       self.name           = kwargs.get( 'name'              ,  'WGamma' )
       self.isSignal       = kwargs.get( 'isSignal'          ,  False    )

       # name / prefix of the analytical function
       self.pdf_prefix     = kwargs.get( 'pdf_prefix'        ,  'dijet'  )

       # parameters of the analytical function
       #self.params_prefix  = kwargs.get( 'params_prefix'     ,  ['dijet_order1', 'dijet_order2', 'dijet_order3'])
       self.params_prefix  = kwargs.get( 'params_prefix'     ,  ['dijet_order1', 'dijet_order2'])
       assert isinstance( self.params_prefix, list),  "Input parames_prefix must be a list!!!"

       self.outputfname = None
       # (val, err)
       self.norm = {"-1": ( 1.0, 0.0 )}

       # analysis channel: muon for default
       #self.channel = kwargs.get('channel', 'mu')

       # analysis eta region: EB (probably never changed.)
       #self.eta     = kwargs.get('eta',     'EB')
       #self.wstag   = kwargs.get('wstag',   'base')

       # analysis variable
       #self.var     = kwargs.get('var',     'mt_fulltrans')

       # for signals only, default 1000 GeV and 5% width
       self.sigpar  = kwargs.get('sigpar',  '1000_5')


       # for systematic uncertainties

       # whether has systematics from lumi
       self.useLumi = kwargs.get( 'useLumi',  True  )
       # whether has systematics from MET
       self.useMET  = kwargs.get( 'useMET' ,  False )
       # whether has systematcis from PDF
       self.usePDF  = kwargs.get( 'usePDF' ,  False )



       ## variables calculated
   def GetRootFileName( self ):
       return self.GetWSName() + ".root"

   def GetWSName( self ):
       if self.isSignal:
          return "workspace_%s_%s"%(self.name, self.sigpar)
       else:
          #return "workspace_%s_%s"%(self.name.lower(),self.pdf_prefix)
          return "workspace_%s"%(self.name.lower())

   def GetPDFNamesList( self, var, cutsettag = "ABC" ,channel="mu", year = 2016 ):
       ## FIXME may be deleted
       namelist = []
       for tag in cutsettag:
            namelist.append(self.GetPDFName( var, channel+tag , year ))
       return namelist

   def GetPDFName( self, var, channel="mu", year = 2016 ):
       if self.isSignal:
          tmp =  "_".join( [ self.pdf_prefix, self.sigpar, channel+str(year), var ] )
          print "pdfname:",tmp
          return tmp
       else:
          return "_".join( [ self.pdf_prefix, channel+str(year), self.name.lower(), self.pdf_prefix] )

   def GetParNames( self, channel ="mu", year = 2016):
       parlist = []
       for ipar_prefix in self.params_prefix:
           if self.isSignal:
              parlist.append( "_".join( [ ipar_prefix, self.sigpar, channel+str(year), var ] ) )
           else:
              parlist.append( "_".join( [ ipar_prefix,
                  channel+str(year), self.name.lower(), self.pdf_prefix] ) )
       return parlist


   def GetOutputName( self, outputDir , channel = "mu", year = 2016):
       return outputDir + '/' + self.name + '/' + channel+str(year)+self.GetRootFileName()

   def SetNorm( self, norm, err, cuttag = "-1" ):
       self.norm[cuttag] = ( norm, err )

