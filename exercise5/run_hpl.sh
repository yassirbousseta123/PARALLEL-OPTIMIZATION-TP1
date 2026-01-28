#!/bin/bash

HPL_DIR="hpl-2.3/bin/MacOS"
RESULTS_FILE="hpl_results.csv"

if [ ! -f "$HPL_DIR/xhpl" ]; then
    echo "HPL not built. Run ./build_hpl.sh first"
    exit 1
fi

echo "N,NB,Time_s,GFLOPS" > $RESULTS_FILE

# Matrix sizes and block sizes to test
SIZES="1000 5000 10000"
BLOCKS="32 64 128 256"

for N in $SIZES; do
    for NB in $BLOCKS; do
        echo "Testing N=$N, NB=$NB..."

        # Create HPL.dat for this configuration
        cat > $HPL_DIR/HPL.dat << EOF
HPLinpack benchmark input file
Test run
HPL.out      output file name
6            device out
1            # of problems sizes (N)
$N           Ns
1            # of NBs
$NB          NBs
0            PMAP process mapping
1            # of process grids (P x Q)
1            Ps
1            Qs
16.0         threshold
1            # of panel fact
2            PFACTs
1            # of recursive stopping criterium
4            NBMINs
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1            RFACTs
1            # of broadcast
1            BCASTs
1            # of lookahead depth
1            DEPTHs
2            SWAP
64           swapping threshold
0            L1 in transposed form
0            U  in transposed form
1            Equilibration
8            memory alignment
EOF

        # Run HPL and capture output
        cd $HPL_DIR
        OUTPUT=$(mpirun -np 1 ./xhpl 2>&1)
        cd - > /dev/null

        # Parse results (extract time and GFLOPS from WR line)
        RESULT=$(echo "$OUTPUT" | grep "WR" | tail -1 | awk '{print $6","$7}')

        if [ -n "$RESULT" ]; then
            echo "$N,$NB,$RESULT" >> $RESULTS_FILE
            echo "  -> $RESULT"
        else
            echo "  -> FAILED"
        fi
    done
done

echo ""
echo "Results saved to $RESULTS_FILE"
