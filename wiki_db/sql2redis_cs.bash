#!/bin/bash

# HOW TO USE IT: ./sql2redis_cs.bash

# categorylinks
./scripts/sql2parsed-12.bash cs/cswiki-20160701-categorylinks.txt > cs/categorylinks-parsed.txt
python scripts/parsed2redis.py cs/categorylinks-parsed.txt cs/categorylinks-redis.txt RPUSH c:
rm cs/categorylinks-parsed.txt

# page
./scripts/sql2parsed-13.bash cs/cswiki-20160701-page.txt | LC_ALL=C awk '{print $2 " " $1}' > cs/page-parsed.txt
python scripts/parsed2redis.py cs/page-parsed.txt cs/page-redis.txt RPUSH p:
rm cs/page-parsed.txt

# pagelinks
./scripts/sql2parsed-13nula.bash cs/cswiki-20160701-pagelinks.txt > cs/pagelinks-parsed.txt
python scripts/parsed2redis.py cs/pagelinks-parsed.txt cs/pagelinks-redis.txt RPUSH l:
rm cs/pagelinks-parsed.txt

# pagelinks
./scripts/sql2parsed-13nula.bash cs/cswiki-20160701-redirect.txt > cs/redirect-parsed.txt
python scripts/parsed2redis.py cs/redirect-parsed.txt cs/redirect-redis.txt SET r:
rm cs/redirect-parsed.txt