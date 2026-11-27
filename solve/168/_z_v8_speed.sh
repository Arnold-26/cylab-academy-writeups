#!/bin/bash
# speed test: fetch 4MB range
U="https://challenge-files.cylabacademy.net/library/59e51a5b7346fe4e519eb904782d00d5f61d4dfec7dfb73838a98ee1a2fbae21/d8"
echo "--- plain range test ---"
time curl -s -r 0-4194303 -o /dev/null -w "size=%{size_download} speed=%{speed_download}\n" "$U"
echo "--- compressed full headers ---"
curl -sI "$U" | head -20
echo "--- gzip range ---"
time curl -s --compressed -r 0-4194303 -o /dev/null -w "size=%{size_download} speed=%{speed_download}\n" "$U"
