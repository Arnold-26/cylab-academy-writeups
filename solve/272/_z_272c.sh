#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
rm -rf t272 && mkdir t272 && cd t272 || exit 1
cp ../272_vuln .
echo "academy{LOCAL_TEST_272}" > flag.txt
python3 -c "
story = 'A'*20 + '%'
print(story)
print('-11 -310')
" > in.txt
cat in.txt
echo "--- execution ---"
./272_vuln < in.txt
