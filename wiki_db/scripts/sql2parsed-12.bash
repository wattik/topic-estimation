#!/bin/bash


###### THE LATEST ONE SO FAR
#cat $1 | grep "INSERT INTO" | LC_ALL=C sed -e 's:INSERT INTO .* VALUES ::g' | LC_ALL=C sed -E $'s/[\,]*\(([0-9]+\,[0-9]+\,\'[^\']*\'[^\)]*)\)/\\1 \\\n/g' | LC_ALL=C tr "," ' ' | LC_ALL=C awk '{print $1 " " $3}' | LC_ALL=C sed -e $'s/\([0-9][0-9]*\) \'\(.*\)\'/\\1 \\2/g'

# cat $1 | grep "INSERT INTO" | LC_ALL=C sed -e 's:INSERT INTO .* VALUES ::g' | LC_ALL=C sed -E $'s/\(([^\)]*\')\)(\,|\;)/\\1 \\\n/g' | LC_ALL=C tr "," ' ' 
#| LC_ALL=C awk '{print $1 " " $3}' | LC_ALL=C sed -e $'s/\([0-9][0-9]*\) \'\(.*\)\'/\\1 \\2/g'

cat $1 | grep "INSERT INTO" | LC_ALL=C sed -e 's:INSERT INTO .* VALUES ::g' | LC_ALL=C sed -E $'s/[^\\]\'\)(\,|\;)/\\\n/g' | LC_ALL=C sed -E $'s/([^\,]*),(.*)/\\1 \\2/' | LC_ALL=C sed -E $'s:[\'^(\\\')]\,\': :' | LC_ALL=C awk '{print $1 " " $2}' | LC_ALL=C sed -e $'s/(\([0-9][0-9]*\) \'\(.*\)/\\1 \\2/g' | LC_ALL=C grep -E '^[0-9]+ .*'

######## JOINING
# [ ]
# echo "Joining categorylinks and pages\n"
# LC_ALL=C join -o 1.2 -o 2.2 page_sorted.txt categorylinks_sorted.txt >category_edges.txt
# LC_ALL=C sort -k1d category_edges.txt


# [ ]
# echo "Joining redirect and pages\n" 
# LC_ALL=C join -o 1.2 -o 2.2 page_sorted.txt redirect_sorted.txt >temp.txt
# LC_ALL=C sort -k2d temp.txt


# [ ]
# join -1 2 -2 1 -o 1.1 -o 2.2 temp.txt category_edges.txt >temp2.txt
# rm temp.txt


####### FINAL PARSING for REDIS

# cat category_graph_edges.txt | awk '{print "RPUSH " $2 " " $3}' > redis_import.txt

####### REDIS

# cat redis_import.txt | redis-cli --pipe






