#!/bin/bash
cd ./_z_302
echo "===== solve.o sections"
readelf -SW solve.o
echo "===== solve.o symbols"
readelf -sW solve.o
echo "===== solve.o relocations"
readelf -rW solve.o
echo "===== solfire.so dynamic"
readelf -dW solfire/solfire.so
echo "===== solfire.so dynsym"
readelf -sW --dyn-syms solfire/solfire.so
echo "===== solfire.so .rel.dyn"
readelf -rW solfire/solfire.so
