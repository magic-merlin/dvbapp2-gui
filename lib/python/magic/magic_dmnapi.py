#!/usr/bin/python
# -*- coding: utf-8 -*-
# napiprojekt.pl API is used with napiproject administration consent

import sys
sys.path.append('/usr/lib/enigma2/python/magic')
import magic_dmnapim

magic_dmnapim.lets_go(sys.argv[1],sys.argv[2])
