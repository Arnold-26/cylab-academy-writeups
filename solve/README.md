# solve/ - solution scripts

One folder per challenge (`solve/<id>/`) holding the script that produced the flag, plus the
helper modules and data files it actually reads.

- 163 folders, 188 files
- every script carries a header: challenge, category, event, flag, link to the writeup, usage
- the seven hardest (55, 136, 302, 441, 478, 495, 496) are annotated step by step

The scripts assume the challenge instance is already running: start it from the platform, then
pass the host and port (or the URL) as arguments.

IDs map to [`INDEX.md`](../INDEX.md). Each writeup ends with a `## Scripts` section pointing to
its folder.
