#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# The MCTF project has been supported by the Junta de Andaluc�a through
# the Proyecto Motriz "Codificaci�n de V�deo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

## @file compress.py
#  Compression of a sequence of images (motion vectors and textures).
#  The compression consists of three major steps:\n
#  - Temporal analysis of image sequence. Temporal decorrelation.
#  - Compress the fields of motion. A layer quality is used without loss.
#  - Compressed textures. Quality layers are used, with loss.
#
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.
#
#  @example compress.py
#
#  - Show default parameters.\n
#  mcj2k compress --help
#
#  - Compress using the default parameters.\n
#  mcj2k compress
#
#  - Using a GOP_size=8.\n
#  mcj2k compress --TRLs=3
#
#  - Controlling quantization.
#  mcj2k compress --quantization=45000
#
#  - Example of use.\n 
#  compress --update_factor=0 --texture_layers=16
#  --quantization_texture=42000 --GOPs=10 --TRLs=5 --SRLs=5
#  --block_size=32 --min_block_size=32 --search_range=4
#  --pixels_in_x=352 --pixels_in_y=288

## @package compress
#  Compression of a sequence of images (motion vectors and textures).
#  The compression consists of three major steps:\n
#  - Temporal analysis of image sequence. Temporal decorrelation.
#  - Compress the fields of motion. A layer quality is used without loss.
#  - Compressed textures. Quality layers are used, with loss.

import sys
import getopt
import os
import array
import display
import string
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser

parser = arguments_parser(description="Encodes a sequence of pictures.")
parser.pixels_in_x()
parser.pixels_in_y()
parser.always_B()
parser.block_overlaping()
parser.block_size()
parser.min_block_size()
parser.border_size()
parser.GOPs()
parser.motion_layers()
parser.quantization_step()
parser.quantization_motion()
parser.quantization_texture()
parser.search_range()
parser.subpixel_accuracy()
parser.TRLs()
parser.SRLs()
parser.texture_layers()
parser.update_factor()
parser.using_gains()

args = parser.parse_known_args()[0]

always_B = int(args.always_B)
block_overlaping = int(args.block_overlaping)
block_size = int(args.block_size)
min_block_size = int(args.min_block_size)
border_size = int(args.border_size)
GOPs = int(args.GOPs)
motion_layers = str(args.motion_layers)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
quantization_step = args.quantization_step
quantization_motion = str(args.quantization_motion)
quantization_texture = str(args.quantization_texture)
search_range = int(args.search_range)
subpixel_accuracy = int(args.subpixel_accuracy)
TRLs = int(args.TRLs)
SRLs = int(args.SRLs)
texture_layers = int(args.texture_layers)
update_factor = float(args.update_factor)
using_gains = str(args.using_gains)

# Default block_size as pixels_in_xy
resolution_FHD = 1920 * 1080
if pixels_in_x * pixels_in_y < resolution_FHD:
    block_size = min_block_size = 32
else:
    block_size = min_block_size = 64

if TRLs > 1:
    try:
        # Temporal analysis of image sequence. Temporal decorrelation.
        check_call("mctf analyze"
                   + " --always_B="          + str(always_B)
                   + " --block_overlaping="  + str(block_overlaping)
                   + " --block_size="        + str(block_size)
                   + " --min_block_size="    + str(min_block_size)
                   + " --border_size="       + str(border_size)
                   + " --GOPs="              + str(GOPs)
                   + " --pixels_in_x="       + str(pixels_in_x)
                   + " --pixels_in_y="       + str(pixels_in_y)
                   + " --search_range="      + str(search_range)
                   + " --subpixel_accuracy=" + str(subpixel_accuracy)
                   + " --TRLs="              + str(TRLs)
                   + " --update_factor="     + str(update_factor)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        # Compress the fields of motion. A layer quality is used without loss.
        check_call("mctf motion_compress"
                   + " --block_size="     + str(block_size)
                   + " --GOPs="           + str(GOPs)
                   + " --min_block_size=" + str(min_block_size)
                   + " --motion_layers=\""+ str(motion_layers) + "\""
                   + " --pixels_in_x="    + str(pixels_in_x)
                   + " --pixels_in_y="    + str(pixels_in_y)
                   + " --quantization=\"" + str(quantization_motion) + "\""
                   + " --SRLs="           + str(SRLs)
                   + " --TRLs="           + str(TRLs)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

try:
    # Compressed textures. Quality layers are used, with loss.
    check_call("mctf texture_compress"
               + " --GOPs="                + str(GOPs)
               + " --pixels_in_x="         + str(pixels_in_x)
               + " --pixels_in_y="         + str(pixels_in_y)
               + " --quantization=\""      + str(quantization_texture) + "\""
               + " --quantization_step="   + str(quantization_step)
               + " --SRLs="                + str(SRLs)
               + " --TRLs="                + str(TRLs)
               + " --texture_layers="      + str(texture_layers)
               + " --using_gains="         + str(using_gains)
               , shell=True)
except CalledProcessError:
    sys.exit(-1)
