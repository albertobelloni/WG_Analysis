import ROOT
from uncertainties import ufloat
import uuid

from ROOT import gSystem, gROOT
#gSystem.Load('My_double_CB/My_double_CB_cxx')
gROOT.LoadMacro('My_double_CB/My_double_CB.cxx')
from ROOT import My_double_CB

class FitManager : 
    """ Aim to collect all fitting machinery here """

    def __init__(self, typename, norders, sampname, hist, plot_var, ieta, xvar, label, useRooFit, sample_params={}) :

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
        self.fit_params = {}

        self.roofitresult = None

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
 

    def MakeROOTObj( self, root_obj, *args ) :
        """ Generic function for making ROOT objects."""  

        try :
            thisobj = getattr(ROOT, root_obj)( *args )
            ROOT.SetOwnership( thisobj, False )
            return thisobj

        except TypeError :
            print '***********************************************************'
            print 'FitManager.MakeROOTObj -- Failed to create a %s.  Please check the arguments :'%root_obj
            print args
            print 'Exception is below'
            print '***********************************************************'
            raise


    def Integral( self ) :

        err = ROOT.Double()
        val = self.hist.IntegralAndError( self.hist.FindBin( self.xvar.getMin() ), self.hist.FindBin( self.xvar.getMax() ), err )

        return ufloat( val, err )


    def set_vals(self, name, order, vals ) :

        self.defs.setdefault( name, {} )
        self.defs[name][order] = vals

    def get_vals( self, name, order ) :

        return self.defs[name][order]

    def add_vars( self, arg_list) :

        if self.func_name == 'dijet' : 
            for i in range( 1, self.func_norders+1 ) :
                short_name = 'power' 
                if i > 1 :
                    short_name = 'logcoef%d' %(i-1)

                long_name = '%s_order%d_%s' %( self.func_name, i, self.label )
                this_def = self.get_vals( self.func_name, i )
                var = ROOT.RooRealVar( long_name, long_name, this_def[0], this_def[1], this_def[2] )
                ROOT.SetOwnership(var, False)
                arg_list.add( var  ) 
                self.fit_params[short_name] = var

        # These need to be modified to match the format above
        #if self.func_name == 'atlas' : 
        #    def_num_power = self.get_vals( self.func_name+'_num_power', 1 )
        #    def_den_power = self.get_vals( self.func_name+'_den_power', 1 )

        #    var_num_power = ROOT.RooRealVar( 'num_power', 'num_power', def_num_power[0], def_num_power[1], def_num_power[2] )
        #    var_den_power = ROOT.RooRealVar( 'den_power', 'den_power', def_den_power[0], def_den_power[1], def_den_power[2] )
        #    ROOT.SetOwnership(var_num_power, False)
        #    ROOT.SetOwnership(var_den_power, False)
        #    arg_list.add( var_num_power )
        #    arg_list.add( var_den_power )
        #    for i in range( 1, self.func_norders+1 ) :
        #        def_den_logcoef = self.get_vals( self.func_name+'_den_logcoef', i )
        #        var_den_locoef  = ROOT.RooRealVar( 'den_logcoef_order%d' %i, 'den_logcoef_order%d' %i, def_den_logcoef[0], def_den_logcoef[1], def_den_logcoef[2] )
        #        ROOT.SetOwnership(var_den_locoef, False)
        #        #var.SetName( '%s_order%d' %( self.func_name, i ) )
        #        arg_list.add( var_den_locoef  ) 

        if self.func_name == 'power' : 
            for i in range( 1, self.func_norders +1 ) :
                if i!= self.func_norders:
                   # the last one does not have coefficient  coef1 * exp( -x /pow1) + .... + ( 1- coef1 - ....) exp( -x/pown) 
                   this_def_coef = self.get_vals( self.func_name+'_coef', i )
                   var_coef = ROOT.RooRealVar( 'coef%d' %i, 'coef%d'%i, this_def_coef[0], this_def_coef[1], this_def_coef[2] )
                   ROOT.SetOwnership(var_coef, False)
                   arg_list.add( var_coef )
                   self.fit_params['power_coef%d'%i] = var_coef

                this_def_pow  = self.get_vals( self.func_name+'_pow', i )
                var_pow = ROOT.RooRealVar( 'pow%d' %i, 'pow%d'%i, this_def_pow[0], this_def_pow[1], this_def_pow[2] )
                ROOT.SetOwnership(var_pow, False)

                arg_list.add( var_pow )
                self.fit_params['power_pow%d'%i] = var_pow


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
            coef_final = '1'
            for i in range( 0, self.func_norders-1) :
                order_entries.append( '@%d*TMath::Exp( - @0 / @%d )'  %( i*2+1, i*2+2 ) )
                coef_final += '-@%d'%(i*2+1) 

            function = '+'.join( order_entries )
            function += ' + (' + coef_final + ') * TMath::Exp( - @0 / @%d)'%(self.func_norders*2-1)

        if self.useRooFit or forceUseRooFit :
            print "function: %s"%function
            return function
        else :
            mod_function = function.replace( '@0', 'x' )
            mod_function = '[0]*' + mod_function
            for i in range( 0, 9 ) :
                mod_function = mod_function.replace( '@%d' %i, '[%d]' %i )
            return mod_function


    def make_func_pdf( self ):

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
                #if bw_width < 2  :
                #    bw_width = 2

                #bw_m = self.MakeROOTObj( 'RooRealVar', 'bw_mass_%s' %self.label, 'Resonance  Mass', mass, xmin, xmax, 'GeV' )
                #bw_w = self.MakeROOTObj('RooRealVar', 'bw_width_%s' %self.label, 'Breit-Wigner width',bw_width, 0, 200,'GeV')
                bw_m = self.MakeROOTObj( 'RooRealVar', 'bw_mass_%s' %self.label, 'Resonance  Mass', mass, mass, mass, 'GeV' )
                bw_w = self.MakeROOTObj( 'RooRealVar', 'bw_width_%s'%self.label, 'Breit-Wigner width',bw_width, bw_width, bw_width,'GeV')
                #bw_m.setConstant()
                #bw_w.setConstant()
                bw_m.setError(50.0)
                bw_w.setError(1.0)
                bw = self.MakeROOTObj('RooBreitWigner','bw_%s' %self.label, 'A Breit-Wigner Distribution', self.xvar, bw_m,bw_w)

                #------------------------------
                # crystal ball, has four parameters
                #------------------------------
                cut1_vals   = self.defs['cb_cut1'][mass] 
                sigma_vals = self.defs['cb_sigma'][mass]
                power1_vals = self.defs['cb_power1'][mass]
                mass_vals  = self.defs['cb_mass'][mass]
                cut2_vals = self.defs['cb_cut2'][mass]
                power2_vals = self.defs['cb_power2'][mass]
                
                #cb_cut   = self.MakeROOTObj('RooRealVar','cb_cut_%s' %self.label, 'Cut'  , 0.5, 0.5, 0.50 , '')
                cb_cut1   = self.MakeROOTObj('RooRealVar','cb_cut1_%s' %self.label,   'Cut'  ,  cut1_vals[0],   cut1_vals[1],   cut1_vals[2],   '')
                cb_sigma  = self.MakeROOTObj('RooRealVar','cb_sigma_%s' %self.label, 'Width',  sigma_vals[0], sigma_vals[1], sigma_vals[2], 'GeV')
                cb_power1 = self.MakeROOTObj('RooRealVar','cb_power1_%s' %self.label, 'Power',  power1_vals[0], power1_vals[1], power1_vals[2], '')
                cb_m0     = self.MakeROOTObj('RooRealVar','cb_mass_%s' %self.label,  'mass' ,  mass_vals[0],  mass_vals[1],  mass_vals[2],  'GeV')
                cb_cut2   = self.MakeROOTObj('RooRealVar','cb_cut2_%s' %self.label,   'Cut'  ,  cut2_vals[0],   cut2_vals[1],   cut2_vals[2],   '')
                cb_power2 = self.MakeROOTObj('RooRealVar','cb_power2_%s' %self.label, 'Power',  power2_vals[0], power2_vals[1], power2_vals[2], '')
                

                cb_cut2.setConstant()
                cb_cut2.setError(0.0)
                
                cb_power2.setConstant()
                cb_power2.setError(0.0)

                cb_power1.setConstant() 
                cb_power1.setError(0.0)

                #cb_cut1.setError( 0.05 )
                #cb_sigma.setError( 0.5 )
                #cb_power1.setError( 1. )
                #cb_m0.setError( 1. )

                #cb = self.MakeROOTObj('RooCBShape','cb_%s' %self.label, 'A  Crystal Ball Lineshape', self.xvar, cb_m0, cb_sigma,cb_cut,cb_power)
                #self.func_pdf = self.MakeROOTObj('RooCBShape','sig_model_%s'%self.label, 'A  Crystal Ball Lineshape', self.xvar, cb_m0, cb_sigma,cb_cut,cb_power)
                self.func_pdf = self.MakeROOTObj('My_double_CB', 'cb_%s'%self.label, 'Double Sided Crystal Ball Lineshape', self.xvar, cb_m0, cb_sigma, cb_cut1, cb_power1, cb_cut2, cb_power2)

                #self.func_pdf = self.MakeROOTObj('RooFFTConvPdf','sig_model_%s' %self.label,'Convolution', self.xvar, bw, cb)

                self.fit_params['cb_cut1'] = cb_cut1
                self.fit_params['cb_sigma'] = cb_sigma
                self.fit_params['cb_power1'] = cb_power1
                self.fit_params['cb_mass'] = cb_m0
                self.fit_params['cb_cut2'] = cb_cut2
                self.fit_params['cb_power2'] = cb_power2

                
            else :
                self.func_pdf = self.MakeROOTObj('RooGenericPdf', '%s_%s' %(self.func_name, self.label), self.func_name, func_str, arg_list)

    def fit_histogram( self, workspace=None ) :
        if self.useRooFit:
           self.run_roofit()
        else:
          # use Fit in ROOT and then build RooGenericPdf from TF1
          self.run_tf1fit()
          self.calculate_func_pdf()
        print "*******************************************"
        print "finished fitting"
        print "*******************************************"
        return self.get_results( workspace )

    def run_roofit( self ):      
        xmin = self.xvar.getMin()
        xmax = self.xvar.getMax()

        ll = ROOT.RooLinkedList()
        arg1 = ROOT.RooFit.Save()
        arg2 = ROOT.RooFit.Range( xmin, xmax)
        #arg3 = ROOT.RooFit.SumW2Error(True)
        ll.Add( arg1 )
        ll.Add( arg2 )
        #ll.Add( arg3 )
        self.roofitresult = self.func_pdf.chi2FitTo( self.datahist, ll)
        #self.roofitresult = self.func_pdf.fitTo( self.datahist, ROOT.RooFit.Save(), ROOT.RooFit.Range( xmin, xmax),ROOT.RooFit.SumW2Error(True), ROOT.RooCmdArg( 'Strategy', 3 ) )
        #self.func_pdf.fitTo( self.datahist, ROOT.RooFit.Save(), ROOT.RooFit.Range( xmin, xmax),ROOT.RooFit.SumW2Error(True), ROOT.RooCmdArg( 'Strategy', 3 ) )
        #self.roofitresult = self.func_pdf.fitTo( self.datahist, ROOT.RooFit.Save(), ROOT.RooFit.Range( xmin, xmax), ROOT.RooFit.SumW2Error(True), ROOT.RooFit.Minimizer('Minuit', "Hesse")) 
        #self.func_pdf.fitTo( self.datahist, ROOT.RooFit.Save())
        print "\n**************************"
        print "***** finished fitTo******"
        print "*********************\n"

        '''
        nll = self.func_pdf.createNLL(self.datahist) ;
        m = ROOT.RooMinimizer(nll) 
        #m.setStrategy(2)
        #raw_input('cont2')
        ##// Activate verbose logging of MINUIT parameter space stepping
        #m.setVerbose(ROOT.kTRUE) 
        #raw_input('cont3')
        ##// Call MIGRAD to minimize the likelihood
        #m.simplex() 
        #raw_input('cont3.5')
        m.migrad() 
        print "\n*************************************"
        print "************ finished MIGRAD ****************"
        print "***************************************\n"
        #raw_input('cont4')
        ##// Print values of all parameters, that reflect values (and error estimates)
        ##// that are back propagated from MINUIT
        #self.func_pdf.getParameters(ROOT.RooArgSet(self.xvar)).Print("s") 
        #raw_input('cont5')
        ##// Disable verbose logging
        #m.setVerbose(ROOT.kFALSE) 
        #raw_input('cont6')
        ##// Run HESSE to calculate errors from d2L/dp2
        m.hesse() 
        print "\n*************************************"
        print "************ finished HESSE *****************"
        print "***************************************\n"
        m.minos()
        print "\n*************************************"
        print "************ finished MINOS *****************"
        print "***************************************\n"
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

        self.roofitresult = m.save()
        '''

        #return self.func_pdf

    def run_tf1fit( self ): 
        xmin = self.xvar.getMin()
        xmax = self.xvar.getMax()

        func_str = self.get_fit_function( ) 

        self.func = self.MakeROOTObj( 'TF1', 'tf1_%s' %self.label, func_str, xmin, xmax )

        if self.func_name == 'dijet' : 

            self.func.SetParameter( 0, 0.0000001)
            param = 1
            for i in range( 1, self.func_norders+1 ) :
                this_def = self.get_vals( self.func_name, i )
                self.func.SetParameter( param, this_def[0] )
                param += 1
        
        self.fitresult = self.hist.Fit( self.func, 'R' )

        return self.func

    def calculate_func_pdf( self ) :

        if self.func_pdf is not None : 
            print 'The PDF Function already exists.  It will be overwritten'
        
        if self.func_name == 'dijet' :
            for i in range( 1, self.func_norders+1 ) :
                fitted_result = self.func.GetParameter(i)
                fitted_error = self.func.GetParError(i)

                self.defs['dijet'][i] = ( fitted_result, fitted_result - fitted_error, fitted_result + fitted_error )

            arg_list = self.MakeROOTObj( 'RooArgList' )
            arg_list.add( self.xvar )
            self.add_vars( arg_list )

            for i in range( 1, arg_list.getSize() )  :
                fitted_error = self.func.GetParError(i)
                arg_list[i].setError( fitted_error )

            func_str = self.get_fit_function( forceUseRooFit=True) 

            self.func_pdf = self.MakeROOTObj( 'RooGenericPdf', '%s_%s' %( self.func_name, self.label), self.func_name, func_str, arg_list)


    def save_fit( self, sampMan=None, workspace = None, logy=False, stats_pos='right' ) :

        if sampMan is not None :

            for name, param in self.fit_params.iteritems() : 
                param.SetName( name) 

            #
            # define plot styles
            #
            uid = str(uuid.uuid4())
            can = ROOT.TCanvas( uid, '', 500, 500)
            pad1 = self.MakeROOTObj( 'TPad', "pad1"+self.label, 'pad1'+self.label, 0, 0.25, 1, 1.0 ); pad1.Draw(); pad1.SetBottomMargin(0.0);
            pad2 = self.MakeROOTObj( 'TPad', "pad2"+self.label, 'pad2'+self.label, 0, 0.00, 1, 0.25); pad2.Draw(); 
            pad2.SetTopMargin(0.10);   pad2.SetBottomMargin(0.30); pad2.SetGridy()

            pad1.cd()
            frame = self.xvar.frame() 
            frame.SetName("%s"%self.label)
            frame.SetTitle("%s"%self.label)
            frame.SetTitleSize(0.04, "Y")
            frame.SetLabelSize(0.03, "XYZ")
            frame.SetTitleOffset(0.9,  "Y")
            frame.GetXaxis().SetLabelSize(0.0)
            frame.GetXaxis().SetTitleSize(0.0)

            self.datahist.plotOn(frame, ROOT.RooFit.Name("hist"))
            #self.func_pdf.plotOn( frame,ROOT.RooFit.VisualizeError(self.roofitresult ,1, False), ROOT.RooFit.DrawOption("L"), ROOT.RooFit.LineWidth(5), ROOT.RooFit.LineColor(ROOT.kYellow)) ;
            self.func_pdf.plotOn( frame, ROOT.RooFit.Name("cbpdf"))
            self.normchi2 = frame.chiSquare(2)
           
            print "Start bulid RooChi2Var" 
            Chi2var = self.MakeROOTObj('RooChi2Var', 'Chi2var'+self.label, 'Chi2var'+self.label, self.func_pdf, self.datahist)
            self.chi2 = Chi2var.getVal()
            print "normalized chi2 %.2f chi2: %.2f"%(self.normchi2, self.chi2)
            str1 = ROOT.TString()
            if stats_pos == 'left' : 
                plabel = self.MakeROOTObj( 'TPaveText', 0.1, 0.35, 0.3, 0.55, "NBNDC")
                self.func_pdf.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.1,0.5,0.89), ROOT.RooFit.Format("NBNEU"), ROOT.RooFit.LineWidth(0))
                ## Warning! Might be dangerous to do this. But currently can't find a way to change the border size
                frame.findObject("%s_paramBox"%self.func_pdf.GetName()).SetBorderSize(0)
            if stats_pos == 'right' :
                plabel = self.MakeROOTObj( 'TPaveText', 0.65, 0.35, 0.85, 0.55, "NBNDC")
                self.func_pdf.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.7,0.5,0.89), ROOT.RooFit.Format("NBNEU",ROOT.RooFit.FixedPrecision(2)))
                frame.findObject("%s_paramBox"%self.func_pdf.GetName()).SetBorderSize(0)

            plabel.SetTextSize(0.03)
            plabel.AddText(ROOT.Form("#chi^{2}=%.2f"%self.chi2))
            plabel.AddText(ROOT.Form("#chi^{2}/ndof=%.2f"%self.normchi2))
            #plabel.AddText(ROOT.Form("%.2f cal %2.f"%(int(round(self.chi2/self.normchi2)), self.datahist.numEntries())))
            #plabel.AddText(ROOT.Form("#chi^{2} Prob=%.6f"%ROOT.TMath.Prob(self.chi2, int(round(self.chi2/self.normchi2)))))
            print self.datahist.numEntries()
            plabel.AddText(ROOT.Form("#chi^{2} Prob=%.6f"%ROOT.TMath.Prob(self.normchi2 * (self.datahist.numEntries()-2), self.datahist.numEntries()-2)))
            plabel.SetFillColor(0)
            #plabel.SetBorderSize(0)
            plabel.Draw()
            frame.addObject(plabel)
            frame.Draw()
            #pad1.Update()

            pad2.cd()
            frame2 = self.xvar.frame()
            frame2.SetName("%s_2"%self.label)
            frame2.SetTitle("")
            frame2.GetYaxis().SetTitle("pull")
            frame2.SetTitleSize(0.12, "XYZ")
            frame2.SetLabelSize(0.09, "X")
            frame2.SetLabelSize(0.06, "Y")
            frame2.SetTitleOffset(0.3, "Y")
            frame2.GetXaxis().SetTitle("m_{T}/GeV")
            frame2.addPlotable( frame.pullHist(), "p")
            frame2.GetYaxis().SetRangeUser(-5.0, 5.0)
            frame2.Draw()
            pad2.Update()

            if logy :
                ymax = frame.GetMaximum()
                frame.SetMinimum( 0.0001 )
                frame.SetMaximum( ymax*10 )
                pad1.SetLogy()
                #pad1.SetLogx()
                #pad2.SetLogx()
             
            can.Update()
            can.SaveAs("plots/%s.pdf"%self.label)
            sampMan.outputs[self.label] = can

            if self.useRooFit:
               sampMan.fitresults[self.label] = self.roofitresult
            sampMan.chi2[self.label] = self.chi2

    def get_results( self, workspace = None) :


        results = {}
        for param in self.fit_params.values() :
            results[param.GetName()] = ufloat( param.getValV(), param.getErrorHi() )


        #power_res = ufloat( power.getValV(), power.getErrorHi() )
        #log_res   = ufloat( logcoef.getValV(), logcoef.getErrorHi())
        #int_res   = ufloat( integral, math.sqrt( integral ) )


        results['integral'] = self.Integral( )
        integral_var = ROOT.RooRealVar('dijet_%s_norm' %( self.label ), 'normalization', results['integral'].n )
        integral_var.setError( results['integral'].s )

        if workspace is not None :
            getattr( workspace , 'import' ) ( self.datahist )
            getattr( workspace , 'import' ) ( self.func_pdf )
            getattr( workspace , 'import' ) ( integral_var )

        return results


    def get_defaults( self, sample, var, ieta ) :
    
        #self.set_vals('dijet', 1, ( -10.0, -20, 0 ) )
        #self.set_vals('dijet', 2, (-2.0, -20., -1.0 ))
        #self.set_vals('dijet', 3, ( 0.0, -10, 10) )
        #self.set_vals('dijet', 1, (-14.0,  -20.0,  -10.0))
        #self.set_vals('dijet', 2, (-7.0,   -9.0,  -5.0))
        #self.set_vals('dijet', 3, (-2.0,   -5.0,  -1.0))
        self.set_vals('dijet', 1, (-15.0,  -20.0,  -10.0))
        self.set_vals('dijet', 2, (-7.0,   -9.0,  -5.0))
        self.set_vals('dijet', 3, (-2.0,   -5.0,  -1.0))
        self.set_vals('dijet', 4, (0.0, -10 ,10 ) )
        self.set_vals('dijet', 5, (0.0, -10 ,10 ) )
    
        self.set_vals('power_coef', 1, ( 0.75, 0.1, 0.9 ) )
        #self.set_vals('power_coef', 2, (1000, 0, 100000000) )
        self.set_vals('power_coef', 2, ( 0.1,  0.0, 1.0 ) )
        self.set_vals('power_coef', 3, ( 0.0,  0.0, 0.01 ) )
        self.set_vals('power_coef', 4, (0.0, 0 ,10 ) )
        self.set_vals('power_coef', 5, (0.0, 0 ,10 ) )
    
        self.set_vals('power_pow', 1, (  50.0,    0.,  100 ) )
        self.set_vals('power_pow', 2, ( 150.0,  100.,  300 ) )
        self.set_vals('power_pow', 3, ( 250.0,  250., 1000 ) )
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
    
        '''
        self.set_vals('cb_sigma', 500, ( 28., 1., 100. ) )
        self.set_vals('cb_power', 500, ( 2.15, 0., 10. ) )
        self.set_vals('cb_mass',  500, ( -18, -100, 0 ) )
       
        self.set_vals('cb_cut',   450, ( 0.5, 0., 1.0 ) ) 
        self.set_vals('cb_sigma', 450, ( 28., 1., 100. ) )
        self.set_vals('cb_power', 450, ( 2.15, 0., 10. ) )
        #self.set_vals('cb_mass',  450, ( -18, -100, 0 ) )
        self.set_vals('cb_mass',  450, (450, 200, 600))
        
        self.set_vals('cb_sigma', 400, ( 28., 1., 100. ) )
        self.set_vals('cb_power', 400, ( 2.15, 0., 10. ) )
        self.set_vals('cb_mass',  400, ( -18, -100, 0 ) )
        '''
        for imass in [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3500, 4000]:
            self.set_vals('cb_cut1',   imass,  (  0.3,       0.1,     0.6 ) )
            #self.set_vals('cb_power',  imass, (    2.15,      0.,    10. ) )
            if 'width' in self.sample_params:
               if self.sample_params['width'] == 1e-4:
                  self.set_vals('cb_power1', imass, ( 2.0,        1.4,       4.6 ) )
               else:
                  self.set_vals('cb_power1', imass, ( 3.0,        2.4,       4.0 ) )
            self.set_vals('cb_mass',   imass,  (imass, 0.5*imass, 1.1*imass) )
            self.set_vals('cb_sigma',  imass,  (  28.,       1.,      200. ) )
            self.set_vals('cb_cut2',   imass,  (  1.5,       1.,      2.5  ) )
            self.set_vals('cb_power2', imass,  (  4.0,       0.,      5.0  ) )
    
    


