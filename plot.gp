set terminal pdf enhanced fname "Helvetica" fsize 5 size 2.5,2.5
set output "scan.pdf"
# set lmargin 0
# set rmargin 0
# set ytics nomirror

w = -121529.686236

print "Plotting ./Scan/propanol/0-1-6-10-11/RIMP2/scanw.txt"
#==================#
#| Begin Trickery |#
#==================#
reset
set xrange[-180:180]
set yrange[-180:180]
set dgrid3d 35, 35 splines
set table 'gp.dat'
splot './Scan/propanol/0-1-6-10-11/RIMP2/scanw.txt' u 1:2:($3-w)
unset table
set contour base
set cntrparam levels discrete 1, 2, 3, 5, 7.5, 10, 12.5, 15, 20, 30, 40, 50
unset surf
set dgrid3d 281, 281 splines
set table 'contour.dat'
splot './Scan/propanol/0-1-6-10-11/RIMP2/scanw.txt' u 1:2:($3-w)
unset table
#=================#
#|  End Trickery |#
#=================#

reset
unset key
set cbrange[0:20]
set zrange[0:20]
set xrange[-180:180]
set yrange[-180:180]
set xtics 30
set ytics 30

set dgrid3d 35, 35 splines

set palette rgbformulae 22,13,-31
#33,13,10

set title "Dihedral Scan"
set xlabel "Torsion 1 (degrees)"
set ylabel "Torsion 2 (degrees)"
l '<sh contour.sh contour.dat 0 6 1'

plot 'gp.dat' w ima, \
     '<sh contour.sh contour.dat 1 6 1' w l lt -1 lw 1.5

