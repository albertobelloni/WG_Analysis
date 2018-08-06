#ifndef ROODOUBLECBPDF
#define ROODOUBLECBPDF

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"

class RooDoubleCB : public RooAbsPdf {
public:
  RooDoubleCB();
  RooDoubleCB(const char *name, const char *title,
	      RooAbsReal& _x,
	      RooAbsReal& _mean,
	      RooAbsReal& _width,
	      RooAbsReal& _alpha1,
	      RooAbsReal& _n1,
	      RooAbsReal& _alpha2,
	      RooAbsReal& _n2
	   );
  RooDoubleCB(const char *name, const char *title,
        RooAbsReal& _x,
        RooAbsReal& _xp,
        RooAbsReal& _mean,
        RooAbsReal& _width,
        RooAbsReal& _alpha1,
        RooAbsReal& _n1,
        RooAbsReal& _alpha2,
        RooAbsReal& _n2
  );
  RooDoubleCB(const RooDoubleCB& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new RooDoubleCB(*this,newname); }
  inline virtual ~RooDoubleCB() { }
  Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
  Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;

protected:

  RooRealProxy x;
  RooRealProxy xp;
  RooRealProxy mean;
  RooRealProxy width;
  RooRealProxy alpha1;
  RooRealProxy n1;
  RooRealProxy alpha2;
  RooRealProxy n2;
  
  Double_t evaluate() const ;

private:

  ClassDef(RooDoubleCB,2)
};
 
#endif
