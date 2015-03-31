# Auto generated configuration file
# using:
# Revision: 1.20
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: Configuration/GenProduction/python/ThirteenTeV/WH_ZH_HToTauTau_M_125_TuneZ2star_13TeV_pythia6_cff.py --fileout file:HIG-Fall13-00001.root --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions POSTLS162_V1::All --step GEN,SIM --magField 38T_PostLS1 --geometry Extended2015 --python_filename HIG-Fall13-00001_1_cfg.py --no_exec -n 29
import FWCore.ParameterSet.Config as cms

process = cms.Process('SIM')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2015_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100000)
)

# Input source

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
		"file:MCDBtoEDM_NONE.root"
	  )
)



process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    annotation = cms.untracked.string('PYTHIA6 WH/ZH, H->2tau mH=125GeV with TAUOLA at 13TeV'),
    name = cms.untracked.string('$Source: /cvs/CMSSW/CMSSW/Configuration/GenProduction/python/ThirteenTeV/WH_ZH_HToTauTau_M_125_TuneZ2star_13TeV_pythia6_cff.py,v $')
)

# Output definition
ofile = 'EDM2GEN_PY8.root'

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string(ofile),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_71_V1::All', '')

from Configuration.Generator.PythiaUEZ2starSettings_cfi import *
#from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *


process.generator = cms.EDFilter("Pythia8HadronizerFilter",
#    ExternalDecays = cms.PSet(
#        Tauola = cms.untracked.PSet(
#            UseTauolaPolarization = cms.bool(True),
#            InputCards = cms.PSet(
#                mdtau = cms.int32(240),
#                pjak2 = cms.int32(0),
#                pjak1 = cms.int32(0)
#            ),
#        ),
#        parameterSets = cms.vstring('Tauola'),
#    ),
    maxEventsToPrint = cms.untracked.int32(2),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.0),
    UseExternalGenerators = cms.untracked.bool(True),
    #jetMatching = cms.untracked.PSet(
        #MEMAIN_nqmatch = cms.int32(5),
        #MEMAIN_showerkt = cms.double(0),
        #MEMAIN_minjets = cms.int32(-1),
        #MEMAIN_qcut = cms.double(-1),
        #MEMAIN_excres = cms.string(''),
        #MEMAIN_etaclmax = cms.double(-1),
        #outTree_flag = cms.int32(0),
        #scheme = cms.string('Madgraph'),
        #MEMAIN_maxjets = cms.int32(-1),
        #mode = cms.string('auto')
    #),
#    SLHATableForPythia8 = cms.string('%s' % SLHA_TABLE),
    PythiaParameters = cms.PSet(
            processParameters = cms.vstring(
				'Main:timesAllowErrors    = 10000',
				'ParticleDecays:limitTau0 = on',
				'ParticleDecays:tau0Max = 10',
				'Tune:ee 3',
				'Tune:pp 5',
				'SpaceShower:pTmaxMatch = 1',
				'SpaceShower:pTmaxFudge = 1',
				'SpaceShower:MEcorrections = off',
				'TimeShower:pTmaxMatch = 1',
				'TimeShower:pTmaxFudge = 1',
				'TimeShower:MEcorrections = off',
				'TimeShower:globalRecoil = on',
				'TimeShower:limitPTmaxGlobal = on',
				'TimeShower:nMaxGlobalRecoil = 1',
				'TimeShower:globalRecoilMode = 2',
				'TimeShower:nMaxGlobalBranch = 1',
				'SLHA:keepSM = on',
				'SLHA:minMassSM = 1000.', #reset masses/widths/branching ratios for W/Z/top to match internal madgraph/madspin values
				'Check:epTolErr = 0.01',
				'25:onMode = off',    # turn OFF all H decays
				'25:onIfAny = 15',    # turn ON H->tautau
				),
	    parameterSets = cms.vstring('processParameters')
	    )
)




# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
#process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.endjob_step,process.RAWSIMoutput_step)

process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.RAWSIMoutput_step)


# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)

# End of customisation functions
