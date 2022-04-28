#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H

#include "AnalysisBase.h"

#include <string>
#include <vector>


#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"

// The RunModule inherits from RunModuleBase (an Abstract Base Class )
// defined in the Core package so that all
// RunModules present a common interface in a Run function
// This allows the code defined in this package
// to be run from the Core package to minimize
// code duplication in each module
class RunModule : public virtual RunModuleBase {

    public :

        RunModule() {}

        // The run function must exist and be defined exactly as this
        // because it is defined in RunModuleBase 
        // in src/RunModule.cxx all the analysis is defind in this RunModule function
        void initialize( TChain * chain, TTree *outtree, TFile *outfile, const CmdOptions & options, std::vector<ModuleConfig> & config) ;
        bool execute( std::vector<ModuleConfig> & config ) ;
        void finalize( ) {};

        // The ApplyModule function calls any other module defined below
        // in src/RunModule.cxx.  This funciton is not strictly required
        // but its a consistent way to apply modules
        bool ApplyModule         ( ModuleConfig & config ) const;


        bool FilterPhoton        ( ModuleConfig & config ) const;
        bool FilterTrueHT        ( ModuleConfig & config ) const;
        bool FilterMTRes         ( ModuleConfig & config ) const;
        bool FilterTrueWPt       ( ModuleConfig & config ) const;
        bool ApplyTrueWPtKNeg    ( ModuleConfig & config ) const;
        bool FilterHLT           ( ModuleConfig & config ) const;

    private:
        bool printevent ;
};

// Ouput namespace 
// Declare any output variables that you'll fill here
namespace OUT {

};

#endif
