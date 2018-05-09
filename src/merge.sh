#!/bin/bash

low="low_0/"
even="even_1/"
odd="odd_1/"
images=33

usage() {
    echo $0
    echo "Forward Lazzy wavelet transform over the time domain"
    echo "  [-e even images ($even)]"
    echo "  [-o odd images ($odd)]"
    echo "  [-l low images ($low)]"
    echo "  [-i images ($images)]"
    echo "  [-? (help)]"
}

(echo $0 $@ 1>&2)

while getopts "e:o:l:i:?" opt; do
    case ${opt} in
	e)
	    even="${OPTARG}"
	    echo even=$even
	    ;;
	o)
	    odd="${OPTARG}"
	    echo odd=$odd
	    ;;
	l)
	    low="${OPTARG}"
	    echo low=$low
	    ;;
	i)
	    images="${OPTARG}"
	    echo images=$images
	    ;;
	?)
            usage
            exit 0
            ;;
        \?)
            echo "Invalid option: -${OPTARG}" >&2
            usage
            exit 1
            ;;
        :)
            echo "Option -${OPTARG} requires an argument." >&2
	    usage
            exit 1
            ;;
    esac
done

set -x

mkdir $low

ln -s ../${even}"0000_Y" $low
ln -s ../${even}"0000_U" $low
ln -s ../${even}"0000_V" $low

image=0
images_2=`echo $images/2 | bc`
while [ $image -le $images_2 ]
do
    _odd=`echo $image*2+1 | bc`
    ln -s ../$odd$(printf "%04d.Y.pgm" $image) $low/$(printf "%04d.Y.pgm" $_odd)
    ln -s ../$odd$(printf "%04d.U.pgm" $image) $low/$(printf "%04d.U.pgm" $_odd)
    ln -s ../$odd$(printf "%04d.V.pgm" $image) $low/$(printf "%04d.V.pgm" $_odd)

    _even=`echo $image*2+2 | bc`
    ln -s ../$even$(printf "%04d.Y.pgm" $image) $low/$(printf "%04d.Y.pgm" $_even)
    ln -s ../$even$(printf "%04d.U.pgm" $image) $low/$(printf "%04d.U.pgm" $_even)
    ln -s ../$even$(printf "%04d.V.pgm" $image) $low/$(printf "%04d.V.pgm" $_even)

    ((image++))
done
