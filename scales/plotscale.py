import os, numpy, math, copy, math
from ROOT import TLegend, TCanvas, TColor, kMagenta, kOrange, kRed, kBlue, kGray, kBlack, gROOT, gStyle, TFile, TH1F, TH2F, TLatex, TGraph, Double
from officialStyle import officialStyle
from optparse import OptionParser, OptionGroup

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

def LegendSettings(leg, ncolumn):
    leg.SetNColumns(ncolumn)
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.04)
    leg.SetTextFont(42)

    

if __name__ == '__main__':

    parser = OptionParser(usage='usage: %prog [options] ARGs',
                          description='print necessary parameters')

    parser.add_option('-m', '--mass', dest='mass', default='80', 
                      action='store',
                      help='mass')

    parser.add_option('-t', '--tanb', dest='tanb', default='30', 
                      action='store',
                      help='tanb')

    parser.add_option('-p', '--particle', dest='particle', default='h', 
                      action='store',
                      help='particle [A/H/h]')

    (options, args) = parser.parse_args()

    print 
    print '-'*80
    print 'Mass = ', options.mass
    print 'Tan(beta) = ', options.tanb
    print 'Particle = ', options.particle
    print '-'*80

    qt = TGraph()
    qb = TGraph()
    qtb = TGraph()


    _QT_ = -1.
    _QB_ = -1.
    _QTB_ = -1.

    count = 0
    for line in open('scales-higgs-mass-scan.dat', 'r'):

        mass, ht, hb, htb = line.split()
        qt.SetPoint(count, Double(mass), Double(ht))
        qb.SetPoint(count, Double(mass), Double(hb))
        qtb.SetPoint(count, Double(mass), Double(htb))

#        print mass, options.mass, type(mass), type(options.mass)
        if mass == options.mass:
#            print 'Qt = ', Double(ht)
#            print 'Qb = ', Double(hb)
#            print 'Qtb = ', Double(htb)
            _QT_ = Double(ht)
            _QB_ = Double(hb)
            _QTB_ = Double(htb)

        count += 1


    canvas = TCanvas('c1')
        
    qt.SetLineColor(kRed)
    qt.SetMarkerColor(kRed)
    qt.GetXaxis().SetTitle('mA (GeV)')
    qt.GetYaxis().SetTitle('hfact')
    qt.Draw('AL')

    qb.SetLineColor(kBlue)
    qb.SetMarkerColor(kBlue)
    qb.Draw('Lsame')

    qtb.SetLineColor(kBlack)
    qtb.SetMarkerColor(kBlack)
    qtb.Draw('Lsame')
    
    leg = TLegend(0.2,0.6,0.5,0.9)
    LegendSettings(leg, 1)
    leg.AddEntry(qt, 'Q_{t}', 'l')
    leg.AddEntry(qb, 'Q_{b}', 'l')
    leg.AddEntry(qtb, 'Q_{tb}', 'l')
    leg.Draw()

#    canvas.SaveAs('scale.gif')


    #############################################


    ct = TGraph()
    cb = TGraph()
    ctb = TGraph()
    ctb_pos = TGraph()
    ctb_neg = TGraph()
    
    dict_t = {}
    dict_b = {}

    _SIGMA_T_ = -1.
    _SIGMA_B_ = -1.
    _SIGMA_TB_ = -1.
    
#    print 'reading ... SM-b_13000_higgs_' + (options.particle).replace('H','h') + '_68cl_0_1.txt'
    
    count = 0
    for line in open('SM-b_13000_higgs_' + (options.particle).replace('H','h') + '_68cl_0_1.txt', 'r'):

        mass, cs = line.split()
        cb.SetPoint(count, Double(mass), Double(cs))
        dict_b[mass] = Double(cs)
        count += 1

    count = 0
    for line in open('SM-t_13000_higgs_' + (options.particle).replace('H','h') + '_68cl_0_1.txt', 'r'):

        mass, cs = line.split()
        ct.SetPoint(count, Double(mass), Double(cs))
        dict_t[mass] = Double(cs)
        count += 1

    count = 0
    for line in open('SM-t+b_13000_higgs_' + (options.particle).replace('H','h') + '_68cl_0_1.txt', 'r'):

        mass, cs = line.split()

        if dict_b.has_key(mass) == False or dict_t.has_key(mass) == False: 
            continue
        
        interference = Double(cs) - dict_b[mass] - dict_t[mass]

#        ctb.SetPoint(count, Double(mass), abs(interference))
        ctb.SetPoint(count, Double(mass), Double(cs))
        count += 1

        if str(int(float(mass))) == options.mass:
#            print 'sigma(t+b) = ', Double(cs)
#            print 'sigma(t) = ', dict_t[mass]
#            print 'sigma(b) = ', dict_b[mass]
#            print 'sigma(t+b) - sigma(t) - sigma(b) = ', interference

            _SIGMA_T_ = dict_t[mass]
            _SIGMA_B_ = dict_b[mass]
            _SIGMA_TB_ = Double(cs)

    count_pos = 0
    count_neg = 0
    for line in open('SM-t+b_13000_higgs_h_68cl_0_1.txt', 'r'):

        mass, cs = line.split()
       
        if dict_b.has_key(mass) == False or dict_t.has_key(mass) == False: 
            continue

        interference = Double(cs) - dict_b[mass] - dict_t[mass]

        if interference > 0:
            ctb_pos.SetPoint(count_pos, Double(mass), abs(interference))
            count_pos += 1
        else:
            ctb_neg.SetPoint(count_neg, Double(mass), abs(interference))
            count_neg += 1


    canvas2 = TCanvas('c2')
        
    ct.SetLineColor(kRed)
    ct.SetLineWidth(5)
    ct.SetMarkerColor(kRed)
    ct.GetXaxis().SetTitle('mA (GeV)')
    ct.GetYaxis().SetTitle('#sigma (pb)')
    ct.SetMarkerSize(0)
    ct.SetMaximum(1000)
    ct.SetMinimum(0.000001)
    ct.GetXaxis().SetRangeUser(0,1000)
    ct.Draw('APL')

    cb.SetLineColor(kBlue)
    cb.SetMarkerColor(kBlue)
    cb.SetMarkerSize(0)
    cb.Draw('PLsame')

    ctb.SetLineColor(kBlack)
    ctb.SetLineWidth(2)
    ctb.SetMarkerColor(kBlack)
    ctb.SetMarkerSize(0)
    ctb.Draw('PLsame')
    
#
#    ctb_pos.SetLineColor(kBlack)
#    ctb_pos.SetMarkerColor(kBlack)
#    ctb_pos.SetMarkerSize(0)
#    ctb_pos.Draw('PLsame')
#
#    ctb_neg.SetLineColor(kGray)
#    ctb_neg.SetMarkerColor(kGray)
#    ctb_neg.SetMarkerSize(0)
#    ctb_neg.Draw('PLsame')

    leg = TLegend(0.2,0.2,0.4,0.4)
    LegendSettings(leg, 1)
    leg.AddEntry(ct, '#sigma_{t}', 'l')
    leg.AddEntry(cb, '#sigma_{b}', 'l')
    leg.AddEntry(ctb, '#sigma_{t+b}', 'l')
    leg.Draw()

    canvas2.SetLogy()
#    canvas2.SaveAs('cross-section.gif')

    ################################################################

    Yt = TGraph()
    Yb = TGraph()

    count = 0
    ymax = -1.

    tdict = {}

    _YT_ = -1.
    _YB_ = -1.

    for line in open('mhmodp_13000_higgs_' + options.particle + '.txt', 'r'):

        tanB, mA, ggh, bbh, mAA, _Yt, _Yb = line.split()

        if tdict.has_key(tanB) == True:
            continue

#        print tanB, options.tanb
        if str(int(float(tanB))) == options.tanb:
#            print 'Yt(MSSM)/Yt(SM) = ', _Yt
#            print 'Yb(MSSM)/Yb(SM) = ', _Yb

            _YT_ = Double(_Yt)
            _YB_ = Double(_Yb)

        tdict[tanB] = '1'

        Yt.SetPoint(count, Double(tanB), Double(_Yt))
        Yb.SetPoint(count, Double(tanB), Double(_Yb))

        if ymax < Double(_Yt):
            ymax = Double(_Yt)*1.2
        if ymax < Double(_Yb):
            ymax = Double(_Yb)*1.2
        
        count += 1


    canvas3 = TCanvas('c3')
        
    Yt.SetLineColor(kRed)
    Yt.SetMarkerColor(kRed)
    Yt.SetMaximum(ymax)
    Yt.GetXaxis().SetTitle('tan #beta')
    Yt.GetYaxis().SetTitle('Y_{MSSM}/Y_{SM}')
    Yt.Draw('AL')

    Yb.SetLineColor(kBlue)
    Yb.SetMarkerColor(kBlue)
    Yb.Draw('Lsame')

    
    leg = TLegend(0.5,0.3,0.9,0.5)
    LegendSettings(leg, 1)
    leg.AddEntry(Yt, 'Y_{t, MSSM} / Y_{t, SM}', 'l')
    leg.AddEntry(Yb, 'Y_{b, MSSM} / Y_{b, SM}', 'l')
    leg.Draw()
    
#    canvas3.SaveAs('Yukawa_linear.gif')
    canvas3.SetLogy()
#    canvas3.SaveAs('Yukawa_log.gif')

    
    print 'Qt = ', _QT_
    print 'Qb = ', _QB_
    print 'Qtb = ', _QTB_

    print 
    print '-'*80    
    print 

    print 'Yt = ', _YT_
    print 'Yb = ', _YB_
    print 'Sigma_t = ', _SIGMA_T_
    print 'Sigma_b = ', _SIGMA_B_
    print 'Sigma_tb = ', _SIGMA_TB_

    print 
    print '-'*80    
    print 

    print 't-only = ', _YT_*_YT_*_SIGMA_T_
    print 'b-only = ', _YB_*_YB_*_SIGMA_B_
    print 'interf. t+b = ', _YT_*_YB_*_SIGMA_TB_
    print 'interf. t = ', -_YT_*_YB_*_SIGMA_T_
    print 'interf. b = ', -_YT_*_YB_*_SIGMA_B_

    print
