#!/usr/bin/env python
''' Reads config file and executes CTMP

    json formatted config

'''

import sys
import json
from subprocess import *

def ctmp_commandline(cfg_d):
    ''' gets arguments from cfg_d

        CTMPs binary calculate_likelihood takes 19-22 arguments
        depending on the analysis.

    '''

    ctmp_args = [
                cfg_d['seq_type'],
                cfg_d['anal_type'],
                cfg_d['left_phy'],
                cfg_d['right_phy'],
                cfg_d['left_tre'],
                cfg_d['right_tre'],
                cfg_d['spec_names'],
                cfg_d['spec_tre'],
                cfg_d['left_seq2spec'],
                cfg_d['right_seq2spec'],  
                cfg_d['prior'],       # use included aa_prior.txt
                cfg_d['ratmat'],      # use included aa_ratemat.txt
                cfg_d['penalty'],     # 0.1 default?
                cfg_d['maxgap'],      # .25 --> (75% ungapped)
                cfg_d['maxcons'],     # set to 1 to analyze all pairs
                cfg_d['minnonovlp'],  # set to 0 to analyze all pairs
                cfg_d['loglikerat'],  # set negative? to report all scores
                cfg_d['output'],
                cfg_d['scanmode']  # 0: all pairs, 1: single pair
                ]
    if cfg_d['anal_type'] == 1:
        ctmp_args += [cfg_d['seqpairs']]
    if len(cfg_d) > 20:
        ctmp_args += [
                cfg_d['leftcol'],   # only valid if scanmod is 0
                cfg_d['rightcol']   # ditto
                ]

    ctmp_args = map(str, ctmp_args)  # args must be strings
    cmd = ['calculate_likelihood'] + ctmp_args
    return cmd

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >>sys.stderr, "Usage: %s config.json" % sys.argv[0]
        sys.exit(1)

    cfg = sys.argv[1]
    cfg_d = json.load(open(cfg, 'r'))
    cmd = ctmp_commandline(cfg_d)
    #print >>sys.stderr, "running %s" % ' '.join(cmd)
    Popen(cmd, stdout=PIPE).communicate()
