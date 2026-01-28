CC = gcc
CFLAGS = -O2

mxm: mxm.c
	$(CC) $(CFLAGS) -o mxm mxm.c

run: mxm
	rm -f results.csv
	for n in 500 1000 1500 2000; do \
		./mxm $$n ijk >> results.csv; \
		./mxm $$n ikj >> results.csv; \
	done

plot: run
	python3 plot_mxm.py

clean:
	rm -f mxm results.csv *.png

.PHONY: run plot clean
