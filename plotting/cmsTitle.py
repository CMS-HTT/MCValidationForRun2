import ROOT as rt

# CMS_lumi
#   Initiated by: Gautier Hamel de Monchenault (Saclay)
#   Translated in Python by: Joshua Hardenbrook (Princeton)
#

class CMS_header( object ):
    def __init__(self, lumitext = '', extraText = 'Simulation', drawLogo = False):
        self.cmsText              = 'CMS'
        self.cmsTextFont          = 61
        self.writeExtraText       = True
        self.extraText            = extraText
        self.extraTextFont        = 52
        self.lumiTextSize         = 0.5
        self.lumiTextOffset       = 0.3
        self.cmsTextSize          = 0.8
        self.cmsTextOffset        = 0.1
        self.relPosX              = 0.120
        self.relPosY              = 0.025
        self.relExtraDY           = 1.2
        self.extraOverCmsTextSize = 0.75
        self.drawLogo             = drawLogo
        self.lumi_13TeV           = '20.1 fb^{-1}'
        self.lumi_8TeV            = '19.7 fb^{-1}'
        self.lumi_7TeV            = '5.1 fb^{-1}'
        if len(lumitext):
            self.lumi_13TeV = lumitext
            self.lumi_8TeV  = lumitext
            self.lumi_7TeV  = lumitext

    def CMS_lumi(self, pad,  iPeriod,  iPosX):
        outOfFrame    = False
        if(iPosX/10==0 ): outOfFrame = True

        alignY_=3
        alignX_=2
        if( iPosX/10==0 ): alignX_=1
        if( iPosX==0    ): alignY_=1
        if( iPosX/10==1 ): alignX_=1
        if( iPosX/10==2 ): alignX_=2
        if( iPosX/10==3 ): alignX_=3
        align_ = 10*alignX_ + alignY_

        H = pad.GetWh()
        W = pad.GetWw()
        l = pad.GetLeftMargin()
        t = pad.GetTopMargin()
        r = pad.GetRightMargin()
        b = pad.GetBottomMargin()
        e = 0.025

        pad.cd()

        lumiText = ''
        if( iPeriod==1 ):
            lumiText += self.lumi_7TeV
            lumiText += ' (7 TeV)'
        elif ( iPeriod==2 ):
            lumiText += self.lumi_8TeV
            lumiText += ' (8 TeV)'

        elif( iPeriod==3 ):
            lumiText = self.lumi_8TeV
            lumiText += ' (8 TeV)'
            lumiText += ' + '
            lumiText += self.lumi_7TeV
            lumiText += ' (7 TeV)'
        elif ( iPeriod==4 ):
            lumiText += self.lumi_13TeV
            lumiText += ' (13 TeV)'
        elif ( iPeriod==7 ):
            if( outOfFrame ):lumiText += '#scale[0.85]{'
            lumiText += self.lumi_13TeV
            lumiText += ' (13 TeV)'
            lumiText += ' + '
            lumiText += self.lumi_8TeV
            lumiText += ' (8 TeV)'
            lumiText += ' + '
            lumiText += self.lumi_7TeV
            lumiText += ' (7 TeV)'
            if( outOfFrame): lumiText += '}'
        elif ( iPeriod==12 ):
            lumiText += '8 TeV'

        print lumiText

        latex = rt.TLatex()
        latex.SetNDC()
        latex.SetTextAngle(0)
        latex.SetTextColor(rt.kBlack)

        extraTextSize = self.extraOverCmsTextSize*self.cmsTextSize

        latex.SetTextFont(42)
        latex.SetTextAlign(31)
        latex.SetTextSize(self.lumiTextSize*t)

        latex.DrawLatex(1-r,1-t+self.lumiTextOffset*t,lumiText)

        if( outOfFrame ):
            latex.SetTextFont(self.cmsTextFont)
            latex.SetTextAlign(11)
            latex.SetTextSize(self.cmsTextSize*t)
            latex.DrawLatex(l,1-t+self.lumiTextOffset*t,self.cmsText)

        pad.cd()

        posX_ = 0
        if( iPosX%10<=1 ):
            posX_ =   l + self.relPosX*(1-l-r)
        elif( iPosX%10==2 ):
            posX_ =  l + 0.5*(1-l-r)
        elif( iPosX%10==3 ):
            posX_ =  1-r - self.relPosX*(1-l-r)

        posY_ = 1-t - self.relPosY*(1-t-b)

        if( not outOfFrame ):
            if( self.drawLogo ):
                posX_ =   l + 0.045*(1-l-r)*W/H
                posY_ = 1-t - 0.045*(1-t-b)
                xl_0 = posX_
                yl_0 = posY_ - 0.15
                xl_1 = posX_ + 0.15*H/W
                yl_1 = posY_
                CMS_logo = rt.TASImage('CMS-BW-label.png')
                pad_logo =  rt.TPad('logo','logo', xl_0, yl_0, xl_1, yl_1 )
                pad_logo.Draw()
                pad_logo.cd()
                CMS_logo.Draw('X')
                pad_logo.Modified()
                pad.cd()
            else:
                latex.SetTextFont(self.cmsTextFont)
                latex.SetTextSize(self.cmsTextSize*t)
                latex.SetTextAlign(align_)
                latex.DrawLatex(posX_, posY_, self.cmsText)
                if( self.writeExtraText ) :
                    latex.SetTextFont(extraTextFont)
                    latex.SetTextAlign(align_)
                    latex.SetTextSize(extraTextSize*t)
                    latex.DrawLatex(posX_, posY_- self.relExtraDY*self.cmsTextSize*t, self.extraText)
        elif( self.writeExtraText ):
            if( iPosX==0):
                posX_ =   l +  self.relPosX*(1-l-r)
                posY_ =   1-t+self.lumiTextOffset*t

            latex.SetTextFont(self.extraTextFont)
            latex.SetTextSize(extraTextSize*t)
            latex.SetTextAlign(align_)
            latex.DrawLatex(posX_, posY_, self.extraText)

        pad.Update()
