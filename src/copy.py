#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Copy MCTF structure to a different place.

import sys
import io
from GOP import GOP
from arguments_parser import arguments_parser
from colorlog import log
import traceback
from shell import Shell as shell

parser = arguments_parser(description="Copy MCTF structure.")
parser.GOPs()
parser.TRLs()
parser.add_argument("--destination",
                    help="destination directory (must exist)",
                    default="/tmp")

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
TRLs = int(args.TRLs)
destination = args.destination

gop = GOP()
GOP_size = gop.get_size(TRLs)
pictures = GOP_size*(GOPs-1)+1

sys.stdout.write("\n" + sys.argv[0] + ":\n\n")
sys.stdout.write("TRLs           = " + str(TRLs) + " temporal resolution levels\n")
sys.stdout.write("Pictures       = " + str(pictures) + " pictures\n")
sys.stdout.write("GOP size       = " + str(GOP_size) + " pictures\n")
sys.stdout.write("Number of GOPs = " + str(GOPs) + " groups of pictures\n")

# Frame types
shell.run("cp frame_types_* " + destination) 

# low_<TRLs-1>
shell.run("mkdir " + destination + "/low_" +  str(TRLs - 1))
shell.run("cp low_" + str(TRLs - 1) + "/" + "*.jp2 " + destination + "/low_" +  str(TRLs - 1))

for subband in range(TRLs-1, 0, -1):
    # motion_residue_<subband>
    shell.run("mkdir " + destination + "/motion_residue_" + str(subband))
    shell.run("cp motion_residue_" + str(subband) + "/*.j2c " + destination + "/motion_residue_" + str(subband))
    # high_<subband>
    shell.run("mkdir " + destination + "/high_" + str(subband))
    shell.run("cp high_" + str(subband) + "/*.jp2 " + destination + "/high_" + str(subband))