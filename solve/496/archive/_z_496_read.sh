#!/bin/bash
cd ./_z_496 || exit 1
for f in main.py util.py admin_bot.py db.py init.py model.py template.jinja2 docker-compose.yml Dockerfile requirements.txt; do
  echo "########## $f ##########"
  cat "$f"
  echo
done
echo "########## frontend tree ##########"
find frontend -type f | head -40
