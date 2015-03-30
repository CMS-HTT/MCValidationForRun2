#!/bin/bash
source  /afs/cern.ch/cms/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc481
if [ -r CMSSW_7_1_13/src ] ; then
 echo release CMSSW_7_1_13 already exists
else
scram p CMSSW CMSSW_7_1_13
fi
cd CMSSW_7_1_13/src
eval `scram runtime -sh`

curl -s --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/HIG-RunIIWinter15GS-00003 --retry 2 --create-dirs -o Configuration/GenProduction/python/HIG-RunIIWinter15GS-00003-fragment.py
[ -s Configuration/GenProduction/python/HIG-RunIIWinter15GS-00003-fragment.py ] || exit $?;

scram b
cd ../../
cmsDriver.py Configuration/GenProduction/python/HIG-RunIIWinter15GS-00003-fragment.py --fileout file:HIG-RunIIWinter15GS-00003.root --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot NominalCollision2015 --step GEN,SIM --magField 38T_PostLS1 --python_filename HIG-RunIIWinter15GS-00003_1_cfg.py --no_exec -n 100 || exit $? ;



echo "nothing" ;cmsDriver.py Configuration/GenProduction/python/HIG-RunIIWinter15GS-00003-fragment.py --fileout file:HIG-RunIIWinter15GS-00003.root --mc --eventcontent DQM --datatier DQM --conditions MCRUN2_71_V1::All --beamspot NominalCollision2015 --step GEN,VALIDATION:genvalid_all --magField 38T_PostLS1  --fileout file:HIG-RunIIWinter15GS-00003_genvalid.root --mc -n 100 --python_filename HIG-RunIIWinter15GS-00003_genvalid.py  --no_exec || exit $? ;

cmsDriver.py step2 --filein file:HIG-RunIIWinter15GS-00003_genvalid.root --conditions MCRUN2_71_V1::All --mc -s HARVESTING:genHarvesting --harvesting AtJobEnd --python_filename HIG-RunIIWinter15GS-00003_genvalid_harvesting.py --no_exec || exit $? ;

