#!/bin/bash
echo "=== Building programs ==="
clang -g -o memory_debug memory_debug.c
clang -g -o memory_debug_fixed memory_debug_fixed.c

echo ""
echo "=== Running BUGGY version (expect leaks) ==="
leaks --atExit -- ./memory_debug 2>&1

echo ""
echo "=== Running FIXED version (no leaks expected) ==="
leaks --atExit -- ./memory_debug_fixed 2>&1
