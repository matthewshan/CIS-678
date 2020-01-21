#!/bin/bash
for i in $(seq 25 200); do
        echo "Retrieving $i"
        curl -X GET "http://www.gutenberg.org/cache/epub/$i/pg$i.txt" -H "Accept-Charset: utf-8" > Input/$i.txt
done
