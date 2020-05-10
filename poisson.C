// To be able to compile the above code, insert the following preprocessor directives:
// #include "Math/QuantFuncMathCore.h"
// #include "TMath.h"
// #include "TGraphAsymmErrors.h"
// - Thanks Guillelmo Gomez-Ceballos for these.
#include <iostream>

{
  //const double CL = 0.6827;
  const double CL = 0.950;
  const double alpha = 1 - CL;
  std::cout << "CL: " << CL << std::endl;

  TH1D * h1 = new TH1D("h1","h1",50,-4,4);
  h1->FillRandom("gaus",100);
  
  TGraphAsymmErrors * g = new TGraphAsymmErrors(h1);
  g->SetMarkerSize(0.5);
  g->SetMarkerStyle (20);
  
  for (int i = 0; i < g->GetN(); ++i) {
    int N = g->GetY()[i];
    double L =  (N==0) ? 0  : (ROOT::Math::gamma_quantile(alpha/2,N,1.));
    double U =  ROOT::Math::gamma_quantile_c(alpha/2,N+1,1) ;
    g->SetPointEYlow(i, N-L);
    g->SetPointEYhigh(i, U-N);
    std::cout << "i: " << i 
	      << " N: " << N
	      << " L: " << L
	      << " U: " << U
	      << " N-L: " << N-L
	      << " U-N: " << U-N
	      << std::endl; 
  }
  g->Draw("AP");
}

