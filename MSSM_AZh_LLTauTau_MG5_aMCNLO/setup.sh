#!/bin/bash
DIRECTORY=$CMSSW_BASE/src/MSSM_AZh_LLTauTau_MG5_aMCNLO/madgraph5
echo 'check if madgraph is installed'
if [ ! -d "$DIRECTORY" ]; then
    echo 'nope, it isn\'t, let\'s do it'
    bzr branch lp:madgraph5
fi
echo 'yep, it\'s already here'
echo 'initialising'
source /afs/cern.ch/cms/slc5_amd64_gcc462/external/python/2.6.4-cms/etc/profile.d/init.sh
echo 'to generate LHE files with MadGraph5 just type mg5 from anywhere or type mg5_aMC if you want MadGraph5 and aMC@NLO'
echo 'for the hadronisation steps just cmsRun MCDBtoEDM_NONE.py ; cmsRun EDM2GEN_cfg_PY8.py'
echo 'executables and configs are linked in bin directory and added to your PATH'
PATH=$PATH:$CMSSW_BASE/src/MSSM_AZh_LLTauTau_MG5_aMCNLO/bin:./bin:bin

