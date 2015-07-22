import ROOT
import os
from cmsTitle import CMS_header
from style    import PlotStyle
from utils    import cosmetics
from copy import deepcopy as dc

ROOT.TH1.SetDefaultSumw2()

class comparer(object):
    '''
    Compares distributions stored in different files.
    Make sure the file structure is constant.
    '''
    
    def __init__(self, files, extraTitle):
        self.files = {}
        for file in files:
            self.files[file[1]] = (ROOT.TFile.Open(file[0], 'r'), file[2])
        self._iniStyle()
        self.header = CMS_header(extraTitle)
        try:
           os.mkdir('comparison')
        except:
           pass
           
    def plot(self):
        
        first_file = self.files.values()[0][0]
        first_file.cd()
        names = [key.GetName() for key in first_file.GetListOfKeys()]

        c1 = ROOT.TCanvas('', '', 700, 1000)
        c1.cd()
        c1.Draw()
        
        stackPad = ROOT.TPad('stackPad', 'stackPad', 0.,  .3, 1., 1.  , 0, 0)  
        ratioPad = ROOT.TPad('ratioPad', 'ratioPad', 0., 0. , 1.,  .38, 0, 0)  

#         c1.cd()
        stackPad.Draw()
#         c1.cd()
        ratioPad.Draw()
                
        l1 = ROOT.TLegend(0.45, 0.8, 0.94, 0.92)
        l1.SetFillColor(0)
        l1.SetBorderSize(0)
        
        for name in names:
                
            l1.Clear()
                        
            options = 'HISTE'

            stackPad.cd()
            for k, v in self.files.items():
                v[0].cd()
                histo = v[0].FindObjectAny(name)
                histo.SetMaximum( histo.GetMaximum()*1.7 )
#                 histo.GetXaxis().SetLabelSize(0.000001)
#                 histo.GetXaxis().SetTitleSize(0.000001)
                histo.GetXaxis().SetLabelOffset(2.)
                histo.GetXaxis().SetTitleOffset(2.)
                histo.GetYaxis().SetTitle('a.u.')
                cosmetics(self.header)
                l1.AddEntry(histo, k + '\t mean %.2f RMS %.2f' %(histo.GetMean(), histo.GetRMS()), 'l')
                self._histoStyle(histo, v[1])
                histo.DrawNormalized(options)
                if 'SAME' not in options:
                    options += 'SAME'

            l1.Draw('sameAEPZ')
            denominator = dc( self.files.items()[0][1][0].FindObjectAny(name) )
            options = 'E2'
            
            for k, v in self.files.items()[1:]:
                histo = v[0].FindObjectAny(name)
                ratioPad.cd()
                ratioPad.SetGridy(True)
                ratioPad.SetBottomMargin(0.2)
                ROOT.gStyle.SetOptStat(0)
                numerator = dc(histo)
                numerator.SetStats(0)
                
                numerator.Divide(denominator)
                
                for bin in range(numerator.GetNbinsX()+1):
                    numerator.SetBinContent( bin, numerator.GetBinContent(bin) - 1.)

#                     num = numerator.GetBinContent(bin)
#                     den = max(0.00001, denominator.GetBinContent(bin))
#                     diff = num / den -1.                    
#                     numerator.SetBinContent( bin, diff )
#                 numerator.Divide(denominator)
                self._histoStyle(numerator, v[1])
                numerator.SetTitle('')
                numerator.GetYaxis().SetRangeUser(-.5,.5)
                numerator.GetYaxis().SetNdivisions(6)
                numerator.GetYaxis().SetTitle('diff over '+ self.files.items()[0][0])

                numerator.GetYaxis().SetLabelSize(0.06)
                numerator.GetXaxis().SetLabelSize(0.06)

#                 numerator.SetMarkerColor(numerator.GetLineColor())

                numerator.GetYaxis().SetTitleSize(0.05)
                numerator.GetXaxis().SetTitleSize(0.07)

                numerator.GetYaxis().SetTitleOffset(1.)
                numerator.GetXaxis().SetTitleOffset(1.)

                numerator.GetXaxis().SetLabelOffset(0.005)
                numerator.Draw(options)          
                if 'SAME' not in options:
                    import pdb ; pdb.set_trace()
                    options += 'SAME'
            c1.Print('comparison/'+name+'.pdf')
            
            ROOT.SetOwnership(c1      , False)
            ROOT.SetOwnership(stackPad, False)
            ROOT.SetOwnership(ratioPad, False)

    def _iniStyle(self):
        ROOT.gROOT.SetBatch()
        ROOT.gROOT.SetStyle('Plain')
        PlotStyle()
        ROOT.gStyle.SetOptStat(0)
        
    def _histoStyle(self, histo, color = ROOT.kRed):
        histo.SetLineColor(color)
        histo.SetLineWidth(2)
        histo.SetFillColor(0)
        histo.SetFillStyle(0)

if __name__ == '__main__':
    mycomp = comparer(
        [#('mA300_MG5_2HDM/histos.root'    , 'MG5_aMC 2HDM4MG5 model', ROOT.kBlue + 4 ),
         ('mA300_PY8/histos.root'         , 'PYTHIA 8 + SLHA'       , ROOT.kBlue - 9 ),
         ('mA300_aMCSusHi_PY8/histos.root', 'MG5_aMC + SusHi'       , ROOT.kBlue     )],
        extraTitle = 'A#rightarrowZh, h#rightarrow#tau#tau, m_{A}= 300 GeV, tan#beta = 2',
    )
        
    mycomp.plot()    
        
