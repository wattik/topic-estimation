Topic Estimation
================

This repository comprises an implementation of a short-text topic estimator. The novel approach utilizes Wikipedia categorization.

## Dependencies

### Python modules:

It's suggested to use **pip** when installing those modules, also note that **sudo** will be needed.

1) **nltk** and its libraries

2) **redis** for python

Ad 1) First install the module, then download its libraries by typing into python console:

`import nltk`

`nltk.download()`

After a window has been poped up, select all libraries and download them. It's possible that some of them will fail, which should not cause any problems in this usage.


### General dependencies:

1) Running redis server locally without password or usernames
2) Redis is fill up with data


## Insert data into redis

Check the `wiki_db/cs` folder which shall comprise sql dumps and, optionally, ready-to-use redis import files. The latter is typically names `<table name>_redis.txt`.
In case those are included (and are up-to-date), you can skip to the step 2.

### STEP 1
If the `wiki_db/cs` folder is empty, download the sql dumps from `https://dumps.wikimedia.org/cswiki/`. It has been tested that the `latest` folder is usually incomplete, therefore, use the latest full dump named by numbers only.
Download only those tables: `categorylinks`, `page`, `pagelinks`, `redirect`. And put them into the `wiki_db/cs` folder.

Go to the _wiki_db_ folder and run in terminal: `<dir to wiki_db>/sql2redis_cs.bash`.
This script takes the sql dumps in wiki_db/cs as input and converts them into a redis mass-insert file. Also note that for different sql, dumps just change names in the bash script.  

### STEP 2

Assuming a redis server is running. To insert a redis file into redis, run:

`cat <dir to wiki_db>cs/page_redis.txt | redis-cli --pipe`

`cat <dir to wiki_db>cs/categorylinks_redis.txt | redis-cli --pipe`

`cat <dir to wiki_db>cs/pagelinks_redis.txt | redis-cli --pipe`

`cat <dir to wiki_db>cs/redirects_redis.txt | redis-cli --pipe`

`cat <dir to wiki_db>cs/lemm_redis.txt | redis-cli --pipe`

Now redis includes all data.

## How to run it

There are several tasks one require from the module, however, two general ways are suggested: estimate a topic of a specific text, or run the estimator for several csv file.

### Single text use-case

For simple topic estimation of a specific text, use **get_topics.py**. This file is listed in the root folder of the module and can be executed, for example, from terminal by:
`python <dir to module>/get_topics.py "text"`
The given shell input generates lines of text that will include:
- process info
- frequencies of topics generally
- frequencies of topics per level
- tree of topics

### CSV file use-case

For scanning csv files, use **analyze_csv.py** located in the root directory of the module. Although this script cannot be executed from terminal without changes, these will be essentially straight forward.
It is as easy as: open the **analyze_csv.py** and fine the __main__ part of the document in the very bottom. To walk through a csv file, use:
`compute_csv_file(<input file>, <output file>)`
Now execute the file by, for example in terminal:
`python <dir to module>/analyze_csv.py` that will create a output file with 4 new columns corresponding to:
 - proposed topics using 2 levels
 - proposed topics using 3 levels
 - pairs `<keyword>:<generated topic 1>,<generated topic 2>,...` separated by `|` using 2 levels
 - pairs `<keyword>:<generated topic 1>,<generated topic 2>,...` separated by `|` using 3 levels

## Detailed structure

The API of the module provides a central object working with the inside machinery. This object is called `TopicEstimator`.

### TopicEstimator
The constructor follows this schema: `TopicEstimator(<WikipediaAbstract object>, n = 3, level = 2, verbosity = 0)`
- **WikipediaAbstract object** is a redis instance handling the db connection
- **n** stands for n-grams number
- **level** stands for depth-level of search
- **verbosity**: 0 will create no process-info output, >1 will print out everything

The only method in this class is `estimate_topic(<string text>)` which returns a tuple: `<proposed topics>`, `<list of parents>`. The former is a pythonic list of all topics detected in the text.
The latter stands for a pythonic list of n-grams found in the text. Both lists comprises only `Topic` instances, i.e. an initial n-gram is considered as a topic as well.

### WikipediaAbstract and its children

The class is a Wikipedia browser. Initially, this repository included also MySQL browser and HTTP request browser which both proved to be slow.
At this stag, only `WikipediaRedis` is supported.

To create an instance, just type `wiki = WikipediaRedis()`. The `wiki` object is then inserted into the `TopicEstimator` constructor.

### Analyzer

This class is used to print or generate statistics over the found topics.

The members of the tuple returned by the `TopicEstimator`'s method `estimate_topic()` is utilized in the constructor `Analyzer(<list_of_topics>, <list_of_parents>)`. The class provides those methods:

- **get_generators(<list_of_topics>)** which returns a dictionary of a keyword (as a `Topic` instance) and a list of topics that were (a) generated by this keyword and (b) are included in the `<list_of_topics>` list. The method scans for keywords in the given text and utilizes those that generated at least one topic from the `<list_of_topics>` list.
- **print_tree()**
- **get_most_frequent()**
- **print_frequencies()**
- **print_all_topics()**
- **print_frequencies_by_levels()**
