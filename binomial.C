// To be able to compile the above code, insert the following preprocessor directives:
// #include "Math/QuantFuncMathCore.h"
// #include "TMath.h"
// #include "TGraphAsymmErrors.h"
// - Thanks Guillelmo Gomez-Ceballos for these.
#include <iostream>
#include <TEfficiency.h>

{
  //const double CL = 0.6827;
  const double CL = 0.950;
  const double alpha = 1. - CL;
  
  const double trials = 138.*(12597./919.);
  const double successes = 7.;

  std::cout << "CL: " << CL
	    << " trials: " << trials
	    << " successes: " << successes
	    << " prob: " << successes/trials
	    << " lower: " <<  TEfficiency::ClopperPearson(trials,successes,CL,false)
	    << " upper: " << TEfficiency::ClopperPearson(trials,successes,CL,true)
	    << std::endl;
  
}

