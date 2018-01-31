import ROOT
from uncertainties import ufloat
import uuid

class FitManager : 
    """ Aim to collect all fitting machinery here """

    def __init__(self, typename, sampname, norders, hist, plot_var, ieta, xvar, label, useRooFit, sample_params={}) :

        self.defs = {}

        self.func_name = typename
        self.func_norders = norders

        self.plot_var = plot_var

        self.ieta = ieta

        self.hist = hist
        self.xvar = xvar

        self.label = label

        self.func = None
        self.func_pdf = None

        self.useRooFit = useRooFit

        self.sample_params = sample_params

        self.hist.SetLineColor( ROOT.kBlack )
        self.hist.SetMarkerColor( ROOT.kBlack )
        self.hist.SetMarkerStyle( 20 )
        self.hist.SetMarkerSize( 1.0 )

        self.datahist = ROOT.RooDataHist( 'datahist_%s' %self.label, 'data', ROOT.RooArgList(self.xvar), self.hist )
        ROOT.SetOwnership( self.datahist, False )
        
        self.get_defaults( sampname, plot_var, ieta )

        self.objs = []

    def MakeROOTObj( self, root_obj, name, *args ) :
        """ Generic function for making ROOT objects."""  

        all_args = ( name, ) + args

        try :
            thisobj = getattr(ROOT, root_obj)( *all_args )
            ROOT.SetOwnership( thisobj, False )
            setattr( self, name, thisobj )

            #self.objs.append( thisobj )
            return thisobj
        except TypeError :
            print '***********************************************************'
            print 'FitManager.MakeROOTObj -- Failed to create a %s.  Please check the arguments :'%name
            print args
            print 'Exception is below'
            print '***********************************************************'
            raise


    def Integral( self ) :

        return self.hist.Integral( self.hist.FindBin( self.xvar.getMin() ), self.hist.FindBin( self.xvar.getMax() ) )

    def set_vals(self, name, order, vals ) :

        self.defs.setdefault( name, {} )
        self.defs[name][order] = vals

    def get_vals( self, name, order ) :

        return self.defs[name][order]

    def add_vars( self, arg_list) :

        if self.func_name == 'dijet' : 
            for i in range( 1, self.func_norders+1 ) :
                this_def = self.get_vals( self.func_name, i )
                var = ROOT.RooRealVar( 'order%d' %i, 'order%d' %i, this_def[0], this_def[1], this_def[2] )
                ROOT.SetOwnership(var, False)
                var.SetName( '%s_order%d' %( self.func_name, i ) )
                arg_list.add( var  ) 

        if self.func_name == 'atlas' : 
            def_num_power = self.get_vals( self.func_name+'_num_power', 1 )
            def_den_power = self.get_vals( self.func_name+'_den_power', 1 )

            var_num_power = ROOT.RooRealVar( 'num_power', 'num_power', def_num_power[0], def_num_power[1], def_num_power[2] )
            var_den_power = ROOT.RooRealVar( 'den_power', 'den_power', def_den_power[0], def_den_power[1], def_den_power[2] )
            ROOT.SetOwnership(var_num_power, False)
            ROOT.SetOwnership(var_den_power, False)
            arg_list.add( var_num_power )
            arg_list.add( var_den_power )
            for i in range( 1, self.func_norders+1 ) :
                def_den_logcoef = self.get_vals( self.func_name+'_den_logcoef', i )
                var_den_locoef  = ROOT.RooRealVar( 'den_logcoef_order%d' %i, 'den_logcoef_order%d' %i, def_den_logcoef[0], def_den_logcoef[1], def_den_logcoef[2] )
                ROOT.SetOwnership(var_den_locoef, False)
                #var.SetName( '%s_order%d' %( self.func_name, i ) )
                arg_list.add( var_den_locoef  ) 

        if self.func_name == 'power' : 
            for i in range( 1, self.func_norders+1 ) :
                this_def_coef = self.get_vals( self.func_name+'_coef', i )
                this_def_pow  = self.get_vals( self.func_name+'_pow', i )

                var_coef = ROOT.RooRealVar( 'coef%d' %i, 'coef%d'%i, this_def_coef[0], this_def_coef[1], this_def_coef[2] )
                ROOT.SetOwnership(var_coef, False)
                var_pow = ROOT.RooRealVar( 'pow%d' %i, 'pow%d'%i, this_def_pow[0], this_def_pow[1], this_def_pow[2] )
                ROOT.SetOwnership(var_pow, False)

                arg_list.add( var_coef )
                arg_list.add( var_pow )


    def get_fit_function( self, forceUseRooFit=False ) :

        function = ''

        if self.func_name == 'dijet' : 
            order_entries = []

            log_str = 'TMath::Log10(@0/13000)'
            for i in range( 1, self.func_norders) :
                order_entries.append('@'+str(i+1)+'*' + '*'.join( [log_str]*i))
            
            function = 'TMath::Power( @0/13000., @1 + ' + '+'.join( order_entries) + ')'


        if self.func_name == 'atlas' : 

            function = 'TMath::Power( (1-(@0/13000.)), @1 ) / ( TMath::Power( @0/13000. , @2+ '
            order_entries = []
            for i in range( 0, self.func_norders ) :
                order_entries.append( '@%d*TMath::Log10( @0/13000.)'  %( i+3 ) )

            function += ' + '.join( order_entries )
            function += ' ) )'

        if self.func_name == 'power' : 

            order_entries = []
            for i in range( 0, self.func_norders ) :
                order_entries.append( '@%d*TMath::Power( @0, @%d )'  %( i*2+1, i*2+2 ) )

            function = '+'.join( order_entries )

        if self.useRooFit or forceUseRooFit :
            return function
        else :
            mod_function = function.replace( '@0', 'x' )
            mod_function = '[0]*' + mod_function
            for i in range( 0, 9 ) :
                mod_function = mod_function.replace( '@%d' %i, '[%d]' %i )
            return mod_function

    def fit_histogram( self, workspace=None ) :

        self.run_fit()
        self.calculate_func_pdf()
        return self.get_results( workspace )


    def run_fit(self ) : 

        xmin = self.xvar.getMin()
        xmax = self.xvar.getMax()
    
        if self.useRooFit :

            arg_list = ROOT.RooArgList()
            ROOT.SetOwnership(arg_list, False)
            
            arg_list.add( self.xvar )
            self.add_vars( arg_list)

            func_str = self.get_fit_function() 

            if self.func_name == 'bwxcb'  :

                mass = self.sample_params['mass']
                width = self.sample_params['width']

                bw_width = mass*width
                if bw_width < 2  :
                    bw_width = 2

                bw_m = self.MakeROOTObj( 'RooRealVar', 'bw_mass' , 'Resonance  Mass', mass, xmin, xmax, 'GeV' )
                bw_w = self.MakeROOTObj('RooRealVar', 'bw_width', 'Breit-Wigner width',bw_width, 0, 200,'GeV')
                #bw_m.setConstant()
                #bw_w.setConstant()
                bw = self.MakeROOTObj('RooBreitWigner', 'bw' ,'A Breit-Wigner Distribution', self.xvar, bw_m,bw_w)

                #------------------------------
                # crystal ball, has four parameters
                #------------------------------
                sigma_vals = self.defs['cb_sigma'][mass]
                power_vals = self.defs['cb_power'][mass]
                mass_vals  = self.defs['cb_mass'][mass]
                cb_cut   = self.MakeROOTObj('RooRealVar','cb_cut'   , 'Cut'  , 0.5, 0.5, 0.50 , '')
                cb_sigma = self.MakeROOTObj('RooRealVar','cb_sigma' , 'Width', sigma_vals[0], sigma_vals[1], sigma_vals[2], 'GeV')
                cb_power = self.MakeROOTObj('RooRealVar','cb_power' , 'Power', power_vals[0], power_vals[1], power_vals[2], '')
                cb_m0    = self.MakeROOTObj('RooRealVar','cb_mass'  , 'mass' , mass_vals[0], mass_vals[1], mass_vals[2],'GeV')

                cb_cut.setConstant()
                #cb_power.setConstant()
                #cb_m0.setConstant()

                cb_cut.setError( 0.05 )
                cb_sigma.setError( 0.5 )
                cb_power.setError( 1. )
                cb_m0.setError( 1. )

                cb = self.MakeROOTObj('RooCBShape','cb', 'A  Crystal Ball Lineshape', self.xvar, cb_m0, cb_sigma,cb_cut,cb_power)

                self.func_pdf = self.MakeROOTObj('RooFFTConvPdf','sig_model','Convolution', self.xvar, bw, cb)
                
            else :
                self.func_pdf = self.MakeROOTObj('RooGenericPdf','%s_%s' %(self.func_name, self.label), self.func_name, func_str, arg_list)

            self.func_pdf.fitTo( self.datahist, ROOT.RooFit.Range( xmin, xmax),ROOT.RooFit.SumW2Error(True), ROOT.RooCmdArg( 'Strategy', 3 ) )

            #nll = self.func_pdf.createNLL(self.datahist) ;
            #m = ROOT.RooMinimizer(nll) 
            #m.setStrategy(2)
            #raw_input('cont2')
            ##// Activate verbose logging of MINUIT parameter space stepping
            #m.setVerbose(ROOT.kTRUE) 
            #raw_input('cont3')
            ##// Call MIGRAD to minimize the likelihood
            #m.simplex() 
            #raw_input('cont3.5')
            #m.migrad() 
            #raw_input('cont4')
            ##// Print values of all parameters, that reflect values (and error estimates)
            ##// that are back propagated from MINUIT
            #self.func_pdf.getParameters(ROOT.RooArgSet(self.xvar)).Print("s") 
            #raw_input('cont5')
            ##// Disable verbose logging
            #m.setVerbose(ROOT.kFALSE) 
            #raw_input('cont6')
            ##// Run HESSE to calculate errors from d2L/dp2
            #m.hesse() 
            #raw_input('cont7')
            ##// Print value (and error) of sigma_g2 parameter, that reflects
            ##// value and error back propagated from MINUIT
            ##cb_cut.Print()
            ##raw_input('cont10')
            #self.cb_sigma.Print()
            ##raw_input('cont11')
            ##cb_power.Print()
            ##raw_input('cont12')
            ##cb_m0.Print()
            #raw_input('cont13')
            ##// Run MINOS on sigma_g2 parameter only
            #m.minos(ROOT.RooArgSet(self.cb_sigma)) 
            #raw_input('cont14')
            #self.cb_sigma.Print()
            #raw_input('cont15')
            ##// Print value (and error) of sigma_g2 parameter, that reflects
            ##// value and error back propagated from MINUIT
            ##sigma_g2.Print() ;

            return self.func_pdf
        else :

            func_str = self.get_fit_function( ) 

            self.func = ROOT.TF1( 'tf1_%s' %self.label, func_str, xmin, xmax )

            if self.func_name == 'dijet' : 

                self.func.SetParameter( 0, 0.0000001)
                param = 1
                for i in range( 1, self.func_norders+1 ) :
                    this_def = self.get_vals( self.func_name, i )
                    self.func.SetParameter( param, this_def[0] )
                    param += 1
            
            self.hist.Fit( self.func, 'R' )

            return self.func

    def calculate_func_pdf( self ) :

        if self.func_pdf is not None : 
            print 'The PDF Function already exists.  It will be overwritten'
        
        if self.func_name == 'dijet' :
            for i in range( 1, self.func_norders+1 ) :
                fitted_result = self.func.GetParameter(i)
                fitted_error = self.func.GetParError(i)

                self.defs['dijet'][i] = ( fitted_result, fitted_result - fitted_error, fitted_result + fitted_error )

            arg_list = ROOT.RooArgList()
            ROOT.SetOwnership(arg_list, False)
            arg_list.add( self.xvar )
            self.add_vars( arg_list )

            for i in range( 1, arg_list.getSize() )  :
                fitted_error = self.func.GetParError(i)
                arg_list[i].setError( fitted_error )


            func_str = self.get_fit_function( forceUseRooFit=True) 

            self.func_pdf = ROOT.RooGenericPdf('%s_%s' %(self.func_name, self.label), self.func_name, func_str, arg_list)
            ROOT.SetOwnership(self.func_pdf, False)


    def save_fit( self, sampMan=None, workspace = None, logy=False, stats_pos='right' ) :

        if sampMan is not None :

            can = ROOT.TCanvas( str(uuid.uuid4()), '' )
            frame = self.xvar.frame() 
            self.datahist.plotOn(frame)
            self.func_pdf.plotOn( frame )
            if stats_pos == 'left' : 
                self.func_pdf.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.1,0.5,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(3)));
            if stats_pos == 'right' :
                self.func_pdf.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
            frame.Draw()
            if logy :
                ymax = frame.GetMaximum()
                frame.SetMinimum( 0.001 )
                frame.SetMaximum( ymax*10 )
                can.SetLogy()
                can.SetLogx()

            sampMan.outputs[self.label] = can

    def get_results( self, workspace = None) :

        integral = self.Integral( )

        #power_res = ufloat( power.getValV(), power.getErrorHi() )
        #log_res   = ufloat( logcoef.getValV(), logcoef.getErrorHi())
        #int_res   = ufloat( integral, math.sqrt( integral ) )

        power_res = ufloat( 0, 0 )
        log_res   = ufloat( 0,0)
        int_res   = ufloat( 0, 0)

        integral_var = ROOT.RooRealVar('dijet_%s_norm' %( self.label ), 'normalization', integral )

        #power.SetName( power_name )
        #logcoef.SetName( logcoef_name )

        if workspace is not None :
            getattr( workspace , 'import' ) ( self.datahist )
            getattr( workspace , 'import' ) ( self.func_pdf )
            getattr( workspace , 'import' ) ( integral_var )


        return {'power' : power_res, 'logcoef' : log_res, 'integral' : int_res, 'function_str' : self.get_fit_function(), 'object' : self.func_pdf }


    def get_defaults( self, sample, var, ieta ) :
    
        self.set_vals('dijet', 1, ( -10.5, -20, 0 ) )
        self.set_vals('dijet', 2, (-2.03, -10, 0) )
        self.set_vals('dijet', 3, ( 0.0, -10, 10) )
        self.set_vals('dijet', 4, (0.0, -10 ,10 ) )
        self.set_vals('dijet', 5, (0.0, -10 ,10 ) )
    
        self.set_vals('power_coef', 1, ( 1000, 0, 10000000 ) )
        self.set_vals('power_coef', 2, (1000, 0, 100000000) )
        self.set_vals('power_coef', 3, ( 0.0, 0, 10) )
        self.set_vals('power_coef', 4, (0.0, 0 ,10 ) )
        self.set_vals('power_coef', 5, (0.0, 0 ,10 ) )
    
        self.set_vals('power_pow', 1, ( -9.9, -100, 100 ) )
        self.set_vals('power_pow', 2, (-0.85, -10, 10) )
        self.set_vals('power_pow', 3, ( 0.0, -10, 10) )
        self.set_vals('power_pow', 4, (0.0, -10 ,10 ) )
        self.set_vals('power_pow', 5, (0.0, -10 ,10 ) )
    
        self.set_vals('atlas_num_power', 1, ( -9.9, -100, 100 ) )
        self.set_vals('atlas_den_power', 1, ( -9.9, -100, 100 ) )
        self.set_vals('atlas_den_logcoef', 1, ( -9.9, -100, 100 ) )
        self.set_vals('atlas_den_logcoef', 2, ( -9.9, -100, 100 ) )

        #self.set_vals('cb_sigma', 450, ( 26.41, 15., 35. ) )
        #self.set_vals('cb_power', 450, ( 2.15, 1., 4. ) )
        #self.set_vals('cb_mass',  450, ( -18.1, -30., -10. ) )
        
        #self.set_vals('cb_sigma', 450, ( 28., 1., 100. ) )
        #self.set_vals('cb_power', 450, ( 30., 0., 130. ) )
        #self.set_vals('cb_mass',  450, ( -18, -100, 0 ) )
    
        self.set_vals('cb_sigma', 500, ( 28., 1., 100. ) )
        self.set_vals('cb_power', 500, ( 2.15, 0., 10. ) )
        self.set_vals('cb_mass',  500, ( -18, -100, 0 ) )
        
        self.set_vals('cb_sigma', 450, ( 28., 1., 100. ) )
        self.set_vals('cb_power', 450, ( 2.15, 0., 10. ) )
        self.set_vals('cb_mass',  450, ( -18, -100, 0 ) )
        
        self.set_vals('cb_sigma', 400, ( 28., 1., 100. ) )
        self.set_vals('cb_power', 400, ( 2.15, 0., 10. ) )
        self.set_vals('cb_mass',  400, ( -18, -100, 0 ) )
        
    
    


