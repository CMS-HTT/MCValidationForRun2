from optparse import OptionParser

parser = OptionParser()
parser.usage = '''To be written.'''

parser.add_option('-M', '--mass'       , dest = 'mass'       ,  help = 'Choose the mass of the A boson.'  )
parser.add_option('-P', '--path'       , dest = 'path'       ,  help = 'Path to files. Either EOS or AFS' )
parser.add_option('-T', '--title'      , dest = 'title'      ,  help = 'pattern to look for in sample directory. Default diTau'          , default = 'diTau'   )
parser.add_option('-E', '--edmintcheck', dest = 'edmintcheck',  help = 'run edmIntegrityCheck.py. Default False'                         , default = False     )
parser.add_option('-P', '--publish'    , dest = 'publish'    ,  help = 'publish.py dataset if it is fine. Default False'                 , default = False     )
parser.add_option('-L', '--logger'     , dest = 'logger'     ,  help = 'compress and cmsStage the Logger file to eos. Default False'     , default = False     )

(options,args) = parser.parse_args()

try:
  fname = args[0]
except:
  print 'provide the list of samples to check'
  print 'usage: resubmitter.py samples_pub.txt queue'
  sys.exit(0)



    analyzer = genAnalyzerMSSM_AZh(mass = 300,
        pathToFiles = '/afs/cern.ch/work/m/manzoni/mc-generation/CMSSW_7_1_13/src/MSSM_AZh_LLTauTau_MG5_aMCNLO_2HDM4MG5/madgraph5/PROC_ggAZhlltt_HEFT/Events/run_01/EDM2GEN_PY8.root',
        #pathToFiles = '../MSSM_AZh_LLTauTau_PY8/300/first2k_*/HIG-RunIIWinter15GS-00003*.root',
        extraTitle = 'MG5_aMC A#rightarrowZh, h#rightarrow#tau#tau, m_{A}= 300 GeV, tan#beta = 2',
        maxEvents = 2000)
    analyzer.loop()
    analyzer.saveHistos()

