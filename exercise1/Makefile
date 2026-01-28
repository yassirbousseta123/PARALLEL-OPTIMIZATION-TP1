all: stride_O0 stride_O2

stride_O0: stride.c
	gcc -O0 -o stride_O0 stride.c

stride_O2: stride.c
	gcc -O2 -o stride_O2 stride.c

run: all
	./stride_O0 > results_O0.csv
	./stride_O2 > results_O2.csv

clean:
	rm -f stride_O0 stride_O2 *.csv *.png
