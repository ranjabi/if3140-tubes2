from InputReader import *
from MVCC import *

def main():
    filename = input("Enter filename: ")
    reader = Reader()
    reader.setup(filename)
    mvcc = MVCC(reader.schedule, reader.transaction, reader.data)
    mvcc.start()


if __name__ == '__main__':
    main()