Topic Estimation
================

This repository comprises an implementation of a short-text topic estimator. The novel approach utilizes Wikipedia categorization.

## Dependencies

### Python modules:

It's suggested to use **pip** in order to install those modules. **sudo** will be needed.

1) **nltk** and its libraries

2) **redis** for python

Ad 1), first install the module, then download its libraries by typing into python console:
`import nltk`

`nltk.download()`

### General dependencies:

1) Running redis server locally without password or usernames
2) Redis is fill up with data


## Insert data into redis

Go to the _wiki_db_ folder and run in terminal:
`./sql2redis_cs.bash`.
This script takes the sql dumps in wiki_db/cs as input and converts them into a redis mass insert file. Also note that for different sql dumps just change names in the bash script.  

Assuming a redis server is running. To insert a redis file into redis, run:
`cat page_redis.txt | redis-cli --pipe`

`cat categorylinks_redis.txt | redis-cli --pipe`

`cat pagelinks_redis.txt | redis-cli --pipe`

`cat redirects_redis_redis.txt | redis-cli --pipe`

Now redis includes all the data.


## How to run it

There are several task one can do with the module, however, two general ways are suggested: estimate a topic of a specific text, or run the estimator for several csv file.

For simple topic estimation of a specific text, use **get_topics.py**. This file is listed in the root folder of the module and can be executed, for example, from terminal by:
`python <dir to module>/get_topics.py "text"`
The given shell input generates lines of text that will include:
- process info
- frequencies of topics generally
- frequencies of topics per level
- tree of topics

For scanning csv files, use **analyze_csv.py** located in the root directory of the module. Although this script cannot be executed from terminal without changes, these will be essentially straight forward.
It is as easy as: open the **analyze_csv.py** and fine the __main__ part of the document in the very bottom. To walk through a csv file, use:
`compute_csv_file(<input file>, <output file>)`
Now execute the file by, for example in terminal:
`python <dir to module>/analyze_csv.py` that will create a output file with 4 new columns corresponding to:
 - proposed topics using 2 levels
 - proposed topics using 3 levels
 - pairs `<keyword>:<generated topic 1>,<generated topic 2>,...` seperated by `|` using 2 levels
 - pairs `<keyword>:<generated topic 1>,<generated topic 2>,...` seperated by `|` using 3 levels

## Detailed structure










