from officialStyle import officialStyle
from basic import *
from ROOT import TFile, TH1F, TTree, gStyle, TH2F, kYellow
import sys, math

#gStyle.SetOptStat(11111)
officialStyle(gStyle)
gROOT.SetBatch(True)
gStyle.SetPadRightMargin(0.22)
gStyle.SetStatY(0.92)
    
def makeCompareVars(tree, var, sel, nbin, xmin, xmax, xtitle, ytitle, directory='', header='', name='', adjustable=True):
   
#    c = TCanvas()
#    hist = TH1F(header, header, nbin, xmin, xmax)
#    hist.SetTitle(name)
#    hist.GetXaxis().SetTitle(xtitle)
#    hist.GetYaxis().SetTitle(ytitle)
#    hist.GetYaxis().SetNdivisions(507)
#    hist.Sumw2()


    _hist_ = TH1F(header + '_tmp', header + '_tmp', 11000, -1000, 10000)
    tree.Project(_hist_.GetName(), var, sel)
#    _xmin_ = xmin
#    _xmax_ = xmax

    _xmin_ = 10000
    _xmax_ = -1000

    for ibin in range(1, _hist_.GetXaxis().GetNbins()+1):
        if _hist_.GetBinContent(ibin)==0: continue

        _val_ = _hist_.GetBinCenter(ibin) - _hist_.GetBinWidth(ibin)*0.5
        if _xmin_ > _val_:
            _xmin_ = _val_
        if _xmax_ < _val_:
            _xmax_ = _val_
        
    del _hist_

    c = TCanvas()
    
    if adjustable:
        print 'adjusted ! ', header, nbin, _xmin_, _xmax_
        if _xmin_ == _xmax_:
            print 'Force adjusted ...'
            _xmin_ -= 1
            _xmax_ += 1
        if header.find('mass')!=-1:
            _xmin_ -= 10
            _xmax_ += 10

        if header.find('phi')!=-1:
            _xmin_ = - math.pi
            _xmax_ = math.pi

        if header.find('eta')!=-1:
            _xmin_ = -7
            _xmax_ = 7

        hist = TH1F(header, header, nbin, _xmin_, _xmax_)
    else:
        hist = TH1F(header, header, nbin, xmin, xmax)

    hist.SetTitle(name)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetYaxis().SetNdivisions(507)

    tree.Project(hist.GetName(), var, sel)
        
    hist.SetLineWidth(3)
    hist.SetMarkerSize(0)
    hist.SetMinimum(0)
    hist.SetFillStyle(1)
    hist.SetFillColor(kYellow)
    hist.Draw()

    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle(ytitle)
    hist.GetXaxis().SetLabelSize(0.05)
    hist.GetYaxis().SetLabelSize(0.05)
    hist.GetXaxis().SetTitleSize(0.05)
    hist.GetYaxis().SetTitleSize(0.05)       
    hist.SetLineWidth(3)

    if hist.GetEntries()!=0:
#        save(c, 'plots/' + header)
        save(c, directory + '/ValPlots_' + directory + '/' + header)
    else:
        print 'No entries for ', hist.GetName(), ' ... avoid'


def Save2Canvas(h, xtitle, ytitle, header=''):

    c = TCanvas()
    h.GetXaxis().SetTitle(xtitle)
    h.GetYaxis().SetTitle(ytitle)
    h.GetXaxis().SetLabelSize(0.05)
    h.GetYaxis().SetLabelSize(0.05)
    h.GetXaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleSize(0.05)       
    h.GetYaxis().SetTitleOffset(1.4)
    h.SetFillColor(kYellow)
    h.SetLineColor(1)
    h.SetLineWidth(3)
    
    h.Draw()
#    save(c, header + '/' + h.GetName())
#    save(c, 'plots/' + header + '_' + h.GetName())
    save(c, header + '/ValPlots_' + header + '/' + h.GetName())

if __name__ == '__main__':   

    argvs = sys.argv
    argc = len(argvs)

    if argc != 2:
        print 'Please specify the ID : python YutaTest.py <e.g. : HIG-RunIIWinter15GS-00006>'
        sys.exit(0)

    ensureDir(argvs[1] + '/ValPlots_' + argvs[1])

    fname = argvs[1] + '/ValidationTest_' + argvs[1] + '.root'
    rfile = TFile(fname)

#    fname = argvs[1]
#    rfile = TFile(fname)

    hdict = {
        'A':{'hist':'h_decayA', 'label':'A', 'pdgId':36, 'xtitle':'pdg ID', 'ytitle':'entries'},
        'H':{'hist':'h_decayH', 'label':'H', 'pdgId':35, 'xtitle':'pdg ID', 'ytitle':'entries'},
        'h':{'hist':'h_decayh', 'label':'h', 'pdgId':25, 'xtitle':'pdg ID', 'ytitle':'entries'},
        'Z':{'hist':'h_decayZ', 'label':'Z', 'pdgId':23, 'xtitle':'pdg ID', 'ytitle':'entries'},
    }

    mtree = rfile.Get('per_mother')
    mdict = {
        'pt':{'label':'mother_pt', 'xtitle':'pT', 'ytitle':'entries', 'nbin':30, 'min':0, 'max':200},
        'eta':{'label':'mother_eta', 'xtitle':'eta', 'ytitle':'entries', 'nbin':30, 'min':-7., 'max':7.},
        'phi':{'label':'mother_phi', 'xtitle':'phi', 'ytitle':'entries', 'nbin':30, 'min':-math.pi, 'max':math.pi},
#        'invmass':{'label':'mother_inv', 'xtitle':'di#tau mass', 'ytitle':'entries', 'nbin':30, 'min':0, 'max':200},
        'mass':{'label':'mother_mass', 'xtitle':'mass', 'ytitle':'entries', 'nbin':30, 'min':0, 'max':200},
    }


    for key, val in hdict.iteritems():

        h = rfile.Get(val['hist'])
        if h.GetEntries()==0: continue
        
        h.SetTitle(val['label'] + ': decay')
        Save2Canvas(h, val['xtitle'], val['ytitle'], argvs[1])


        for mkey, mval in mdict.iteritems():
            makeCompareVars(mtree, mval['label'], 'mother_pdg == ' + str(val['pdgId']), mval['nbin'], mval['min'], mval['max'], mval['xtitle'], mval['ytitle'], argvs[1], val['label'] + '_' + mkey, val['label'] + ' : ' + mval['label'].replace('_',' '), True)






    etree = rfile.Get('per_event')
    edict = {
        'njet':{'label':'event_njet','xtitle':'Njets (pT > 30, #eta < 5)', 'ytitle':'entries', 'nbin':10, 'min':0, 'max':10, 'adj':False},
        'nbjet':{'label':'event_nb','xtitle':'Nbjets (pT > 20, #eta < 2.5, status=71)', 'ytitle':'entries', 'nbin':10, 'min':0, 'max':10, 'adj':False},
        'nbgenjet':{'label':'event_nbgen','xtitle':'Nbjets (status=71)', 'ytitle':'entries', 'nbin':10, 'min':0, 'max':10, 'adj':False},
        'met':{'label':'event_met', 'xtitle':'missing ET', 'ytitle':'entries', 'nbin':30, 'min':0, 'max':200, 'adj':True},
        'ljet':{'label':'event_ljet', 'xtitle':'leading jet pT', 'ytitle':'entries', 'nbin':30, 'min':0, 'max':200, 'adj':True},
        'sljet':{'label':'event_sljet', 'xtitle':'sub-leading jet pT', 'ytitle':'entries', 'nbin':30, 'min':0, 'max':200, 'adj':True},
    }

    for ekey, val in edict.iteritems():
        makeCompareVars(etree, val['label'], '', val['nbin'], val['min'], val['max'], val['xtitle'], val['ytitle'], argvs[1], ekey, ekey, val['adj'])


    jtree = rfile.Get('per_jet')
    jdict = {
        'jet_pt':{'label':'jet_pt','xtitle':'jet pT (pT > 30, #eta < 5)', 'ytitle':'entries', 'nbin':30, 'min':0, 'max':200},
        'jet_eta':{'label':'jet_eta','xtitle':'jet eta (pT > 30, #eta < 5)', 'ytitle':'entries', 'nbin':30, 'min':-7, 'max':7},
        'jet_phi':{'label':'jet_phi','xtitle':'jet phi (pT > 30, #eta < 5)', 'ytitle':'entries', 'nbin':30, 'min':-math.pi, 'max':math.pi},
    }

    for jkey, val in jdict.iteritems():
        makeCompareVars(jtree, val['label'], '', val['nbin'], val['min'], val['max'], val['xtitle'], val['ytitle'], argvs[1], jkey, jkey, True)


    dtree = rfile.Get('per_decay')
    ddict = {
#        'decay_pt':{'label':'decay_pt','xtitle':'decay pT (m_{A}-m_{A,input} < 100GeV)', 'ytitle':'entries', 'nbin':30, 'min':0, 'max':200},
#        'decay_eta':{'label':'decay_eta','xtitle':'decay eta (m_{A}-m_{A,input} < 100GeV)', 'ytitle':'entries', 'nbin':30, 'min':-7, 'max':7},
#        'decay_phi':{'label':'decay_phi','xtitle':'decay phi (m_{A}-m_{A,input} < 100GeV)', 'ytitle':'entries', 'nbin':30, 'min':-math.pi, 'max':math.pi},
        'decay_pt':{'label':'decay_pt','xtitle':'decay pT', 'ytitle':'entries', 'nbin':30, 'min':0, 'max':200},
        'decay_eta':{'label':'decay_eta','xtitle':'decay eta', 'ytitle':'entries', 'nbin':30, 'min':-7, 'max':7},
        'decay_phi':{'label':'decay_phi','xtitle':'decay phi', 'ytitle':'entries', 'nbin':30, 'min':-math.pi, 'max':math.pi},
    }


    pdict = {
        'tau':{'label':'tau', 'pdgId':15},
        'b':{'label':'b', 'pdgId':5},
        'e':{'label':'e', 'pdgId':11},
        'muon':{'label':'muon', 'pdgId':13},
    }

    for pkey, pval in pdict.iteritems():
        for dkey, dval in ddict.iteritems():
            makeCompareVars(dtree, dval['label'], 'abs(decay_pdgId)==' + str(pval['pdgId']), dval['nbin'], dval['min'], dval['max'], dval['xtitle'], dval['ytitle'], argvs[1], pkey + '_' + dkey, pval['label'] + ' : ' + dval['label'].replace('_', ' '), True)
