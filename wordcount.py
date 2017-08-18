import sys

def makedict(file):
    dict= {}
    file = open(file)
# following coverts the file in a string and load everything in the RAM
    fh= file.read()
    str= fh.lower()
    str = str.split()
    #print str
    for item in str:
        if item in dict:
            dict[item] +=1
        else:
           dict[item] = 1
    return dict


def print_words(file):
	dict= makedict(file)
        words = sorted(dict.keys()) 
        #print words   
        for i in words:
            print i,'->', dict[i]   

def get_count(word_count_tuple):
    return word_count_tuple[1]


def print_top(file):
    topcount= makedict(file)
    #topcount= topcount.items()
   #print sorted(topcount)
    count= sorted(topcount.items(),key=get_count, reverse=True)

    for item in count[:20]:
        key= item[0]
        value= item[1]
        #value= sorted(value)
        print key, value

###

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
    if len(sys.argv) != 3:
        print 'usage: ./wordcount.py {--count | --topcount} file'
        sys.exit(1)

    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print 'unknown option: ' + option
        sys.exit(1)

if __name__ == '__main__':
  main()
