// File: find_hot_stars.C
// Creation date: 17/09/2017

#include <iostream>
#include <TGraphErrors.h>
#include <TCanvas.h>
#include <TAxis.h>
#include <TMath.h>


void find_hot_stars(){


    //nom du fichier à lire

    TString filename = "data_modifie.txt";


    //ligne B3V au dessus de laquelle on veut recuperer les points, de la forme ax+b

    Double_t a = 0.9909;
    Double_t b = -0.8901;


    //lit le fichier et crée des listes avec les données

    TGraphErrors *g1 = new TGraphErrors(filename, "%*lg %*lg %*lg %*lg %*lg %lg %lg %*lg %*lg %*lg %*lg %*lg %*lg %*lg %*lg %*lg %*lg %*lg", "\t|");

    Double_t *u_g = g1->GetX();
    Double_t *g_r = g1->GetY();
    Int_t const nentries = g1->GetN();

    //crée une fenetre

    TCanvas *c1 = new TCanvas("c1", "c1", 600, 600);

    //prepare ligne B3V

    TF1 *f = new TF1("f", "[0]*x+[1]", TMath::MinElement(nentries, u_g), TMath::MaxElement(nentries, u_g));

    f->SetParameter(0, a);
    f->SetParameter(1, b);


    //crée le graphique

    TGraphErrors *u_gVSg_r = new TGraphErrors(nentries, g_r, u_g);

    //trace le graphique u-g vs g-r

    u_gVSg_r->SetMarkerStyle(2);
    u_gVSg_r->SetMarkerSize(0.5);
    u_gVSg_r->SetTitle("u-g vs g-r");
    u_gVSg_r->GetXaxis()->SetTitle("g - r");
    u_gVSg_r->GetYaxis()->SetTitle("u - g");
    u_gVSg_r->GetXaxis()->CenterTitle();
    u_gVSg_r->GetYaxis()->CenterTitle();

    c1->cd();

    u_gVSg_r->Draw("AP");
    f->Draw("SAME");

}
