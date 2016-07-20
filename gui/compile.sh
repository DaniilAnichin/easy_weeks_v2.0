#!/usr/bin/env bash

cd prev
rm *.py
cd ..

cd drawing
mv ./__init__.py ./in.it
mv *.py ../prev
mv ./in.it ./__init__.py

for i in $(ls *.ui)
 do pyuic4 ${i} -o ${i%.ui}.py
 done

