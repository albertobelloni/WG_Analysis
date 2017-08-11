#ifndef CORE_UTIL_H
#define CORE_UTIL_H

#include "TLorentzVector.h"

namespace Utils {
float calc_mt( const TLorentzVector & obj, const TLorentzVector & nu );
bool stringToDouble( const std::string &in, double &out );
bool stringToInt( const std::string &in, int &out );
}

#endif
