#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Texture compression. Kakadu decides the slopes, automatically.

import os
import sys
import display
import math
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser
import logging
import io

# {{{ Logging

logging.basicConfig()
log = logging.getLogger("texture_compress__automatic") # remove __automatic (some day)
log.setLevel('INFO')

# }}}

# {{{ Arguments parsing

parser = arguments_parser(description="Compress a texture subband.")
parser.GOPs()
parser.layers()
parser.pixels_in_x()
parser.pixels_in_y()
parser.SRLs()
parser.TRLs()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
layers = int(args.layers)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
SRLs = int(args.SRLs)
TRLs = int(args.TRLs)

log.info("GOPs = {}".format(GOPs))
log.info("layers = {}".format(layers))
log.info("pixels_in_x = {}".format(pixels_in_x))
log.info("pixels_in_y = {}".format(pixels_in_y))
log.info("SRLs = {}".format(SRLs))
log.info("TRLs = {}".format(TRLs))

# }}}

MCTF_TEXTURE_CODEC   = os.environ["MCTF_TEXTURE_CODEC"]
HIGH                 = "high"
LOW                  = "low"

gop      = GOP()
GOP_size = gop.get_size(TRLs)
log.info("GOP_size = {}".format(GOP_size))

images = (GOPs - 1) * GOP_size + 1
log.info("images = {}".format(images))

# Compression of HIGH frequency temporal subbands.
subband = 1
while subband < TRLs:
    images = (images + 1) // 2
    #slopes = ','.join(str(i) for i in slope)
    command = "mctf subband_texture_compress__" + MCTF_TEXTURE_CODEC \
      + " --file="              + HIGH + "_" + str(subband) \
      + " --images="            + str(images - 1) \
      + " --pixels_in_x="       + str(pixels_in_x) \
      + " --pixels_in_y="       + str(pixels_in_y) \
      + " --layers="            + str(layers) \
      + " --SRLs="              + str(SRLs)

    log.debug("command={}".format(command))
    try:
        check_call(command, shell=True)
    except CalledProcessError:
        sys.exit(-1)

    subband += 1

# Compression of the LOW frequency temporal subband.
#slopes = ','.join(str(i) for i in slope)
command = "mctf subband_texture_compress__" + MCTF_TEXTURE_CODEC \
  + " --file="              + LOW + "_" + str(TRLs - 1) \
  + " --images="            + str(images) \
  + " --pixels_in_x="       + str(pixels_in_x) \
  + " --pixels_in_y="       + str(pixels_in_y) \
  + " --layers="            + str(layers) \
  + " --SRLs="              + str(SRLs)

log.debug(command)
try:
    check_call(command, shell=True)
except:
    sys.exit(-1)