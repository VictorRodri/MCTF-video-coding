ln -s ~/Videos/container_352x288x30x420x300.yuv low_0
mctf compress --GOPs=9 --TRLs=6
mctf info --GOPs=9 --TRLs=6
mkdir tmp
cd tmp
cp ../*.j2c .
cp ../slopes.tx .
cp ../*type* .
mctf expand --GOPs=9 --TRLs=6
mctf show
