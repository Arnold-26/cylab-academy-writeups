#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
cp -f 432_original.jpg 432_modified.jpg
exiftool -overwrite_original \
  -ModifyDate="1970:01:01 00:00:00" \
  -DateTimeOriginal="1970:01:01 00:00:00" \
  -CreateDate="1970:01:01 00:00:00" \
  -SubSecCreateDate="1970:01:01 00:00:00.001" \
  -SubSecDateTimeOriginal="1970:01:01 00:00:00.001" \
  -SubSecModifyDate="1970:01:01 00:00:00.001" \
  "-Samsung:TimeStamp=1970:01:01 00:00:00.001+00:00" \
  432_modified.jpg 2>&1 | tail -3
echo "=== verification ==="
exiftool 432_modified.jpg 2>/dev/null | grep -iE "Modify Date|Date/Time Original|Create Date|Sub Sec|Time Stamp" | head -10
ls -la 432_modified.jpg
