// File: B3V_line.C
// Creation date: 17/09/2017

#include <iostream>
#include <TGraphErrors.h>
#include <TCanvas.h>
#include <TAxis.h>
#include <TMath.h>


void B3V_line(){


    //nom du fichier à lire

    TString filename = "B3V_3.5.dat";


    //lit le fichier et crée des listes avec les données

    TGraphErrors *g1 = new TGraphErrors(filename, "%lg %lg");

    Double_t *u_g = g1->GetX();
    Double_t *g_r = g1->GetY();
    Int_t const nentries = g1->GetN();

    //crée une fenetre

    TCanvas *c1 = new TCanvas("c1", "c1", 600, 600);

    //prepare le fitting

    TF1 *f1 = new TF1("f1", "[0]*x+[1]");

    f1->SetParameter(0, 1.);
    f1->SetParameter(1, 0.);

    f1->SetParName(0, "a");
    f1->SetParName(1, "b");

    f1->SetRange(TMath::MinElement(nentries, g_r), TMath::MaxElement(nentries, g_r));
    f1->SetLineColor(kGreen);
    f1->SetLineWidth(3);

    gStyle->SetOptFit(1111);


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

    u_gVSg_r->Fit("f1", "R");

    u_gVSg_r->Draw("AP");

}
