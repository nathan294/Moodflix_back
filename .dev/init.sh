#!/bin/bash

cd /app/workspace

poetry install --with dev
# git init
git config --global --add safe.directory /app/workspace
poetry run pre-commit install -f --hook-type pre-commit
# poetry run pre-commit autoupdate

# echo "Listing files in /docker-entrypoint-initdb.d/"
# ls -la /docker-entrypoint-initdb.d/

# for f in /docker-entrypoint-initdb.d/*; do
#   case "$f" in
#     *.sh)
#       if [ -x "$f" ]; then
#         echo "$0: running $f"
#         "$f"
#       else
#         echo "$0: sourcing $f"
#         . "$f"
#       fi
#       ;;
#     *.sql)    echo "$0: running $f"; "${psql[@]}" -f "$f"; echo ;;
#     *.sql.gz) echo "$0: running $f"; gunzip -c "$f" | "${psql[@]}"; echo ;;
#     *)        echo "$0: ignoring $f" ;;
#   esac
#   echo
# done

echo "###### READY TO ROCK !"
sleep infinity