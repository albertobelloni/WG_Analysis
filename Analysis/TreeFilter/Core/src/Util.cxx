#include "Util.h"
#include <math.h>
#include <sstream>
#include <iostream>

namespace Utils {

float calc_mt( const TLorentzVector & obj, const TLorentzVector & nu ) {

    return sqrt( 2*obj.Pt()*nu.Pt() * ( 1 - cos( obj.DeltaPhi(nu) ) ) );

}

bool stringToDouble( const std::string & in, double & out ) {

    std::stringstream ss;
    double val = 0;
    ss.str(in);
    ss >> val;
    if( ss.bad() || ss.fail() ) {// check if the conversion was successful
        return false;
    }
    else {
        out = val;
        return true;
    }
}

bool stringToInt( const std::string & in, int & out ) {

    std::stringstream ss;
    int val = 0;
    ss.str(in);
    ss >> val;
    if( ss.bad() || ss.fail() ) {// check if the conversion was successful
        return false;
    }
    else {
        out = val;
        return true;
    }
}

}

