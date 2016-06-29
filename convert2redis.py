# coding=utf-8

from sys import argv

if __name__ == "__main__":
    with open(argv[1]) as src:
        with open(argv[2], 'w') as out:
            for line in src:
                array = line.lower().split(" ")
                id = argv[4] + array[0]
                name = array[1]
                name = name[0:-1]

                out.write("*3\r\n$" + str(len(argv[3])) + "\r\n" + argv[3] + "\r\n$" + str(len(id)) +"\r\n" + id + "\r\n$" + str(len(name)) + "\r\n" + name +"\r\n")