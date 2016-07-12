# coding=utf-8

# python scripts/parsed2redis.py cs/page-parsed.txt cs/page-redis.txt RPUSH p:

from sys import argv

if __name__ == "__main__":
    with open(argv[1]) as src:
        with open(argv[2], 'w') as out:
            for line in src:
                array = line.decode("utf8").lower().encode("utf8").split(" ")
                id = argv[4] + array[0]
                name = array[1]
                name = name[0:-1]

                out.write('*3\r\n$' + str(len(argv[3])) + '\r\n' + argv[3] + '\r\n$' + str(len(id)) + '\r\n' + id + '\r\n$' + str(len(name)) + '\r\n' + name + '\r\n')