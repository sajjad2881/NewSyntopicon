import nltk
from nltk.corpus import stopwords


##This creates an array, which each value being a complete book 
fileNames = []
for x in range(1,50):
    filedataVar =  ('filedata%d' %x)
    fileNames.append(filedataVar)
    
for x in range(1,50):
    bkName = ('BooksNC/Book%d.txt' % x)
    with open(bkName, 'r') as file : fileNames[x - 1]  = file.read() 


def map_book_new(hash_map, tokens):
    hash_map_current = {}
    if tokens is not None:
        for element in tokens:
            # Remove Punctuation
            word = element.replace(",","")
            word = word.replace(".","")
            word = word.replace("?","")
            word = word.replace("\"","")
            word = word.replace("/'","")
            word = word.replace("\"","")
            word = word.replace("!","")
            word = word.replace(":"," ")
            word = word.replace("*"," ")
            word = word.replace(";"," ")
            word = word.replace("(","")
            word = word.replace("_","")
            word = word.replace(")","")
            word = word.replace("'","")
            word = word.replace(" ","")
            sep1 = '['
            word = word.split(sep1, 1)[0]
            sep2 = ']'
            word = word.split(sep2, 1)[0]
            sep3 = '-'
            word = word.split(sep3, 1)[0]
            word = word.lower()
           
            if word in hash_map and word in hash_map_current:
                hash_map[word] = [hash_map[word][0] + 1, hash_map[word][1]]
            elif word in hash_map:
                hash_map_current[word] = [1,1] 
                hash_map[word] = [hash_map[word][0] + 1, hash_map[word][1] + 1]
            else:
                hash_map_current[word] = [1,1]
                hash_map[word] = [1, 1]
        return hash_map
    else:
        return None


hash_map = {}


for x in range(0, 49):
    hash_map = map_book_new(hash_map, fileNames[x].split())



listttBig = []
listttSmall = []
for x in hash_map.items():
    occourance = x[1][0]
    freq = x[1][1]
    if(occourance > 50 and freq > 5):
        listttBig.append(x)
    elif(occourance <= 50 and freq > 15):
        listttBig.append(x)
    else:
        listttSmall.append(x)


#previously was a touple connection, now a proper dict
new_dict = {}
for x in listttBig:
    new_dict[x[0]] = x[1]


new_dict_sorted = sorted(new_dict, key=lambda x: new_dict[x][0], reverse=True)


sorted_dict_final = {}
for x in new_dict_sorted:
    sorted_dict_final[x] = new_dict[x]



sw_nltk = stopwords.words('english')


listnotStop = []
for x in list(sorted_dict_final):
    if(x in sw_nltk):
        listnotStop.append(sorted_dict_final.pop(x))


f = open("BigListToNarrowV2.txt", "w")
for k in sorted_dict_final.keys():
    f.write("'{}': {} \n".format(k, sorted_dict_final[k]))
f.close()


with open('ReplacementWords.txt', 'r') as file: ReplacementWords = file.read()
with open('BigListLemmasRemovedNew.txt', 'r') as file: MasterList = file.read()

ReplacementWords = ReplacementWords.split("\n")
MasterList = MasterList.split()


MasterListSmaller = []
DiscardList = []
for x in MasterList:
    if ":" in x:
        MasterListSmaller.append(x)
    else:
        DiscardList.append(x)
        
MasterListFinal = []
for x in MasterListSmaller:
    MasterListFinal.append(x[1:-2])


Changes = []
Changes.append(("man", "man's"))
Changes.append(("men", "men’s"))
Changes.append(("god", "god’s"))
Changes.append(("arts", "art"))

for x in ReplacementWords:
    first = x.split(";")[0]
    second = x.split(";")[1]
    #print(first, second)
    if first in MasterListFinal:
        Changes.append((first, second))
    if second in MasterListFinal:
        Changes.append((second, first))


###Now, we have 2 lists, MasterListFinal and Changes 
###In MasterListFinal, replace everything, and in changes, try and see if you can add next to it, or else append it 
###The second word will be the one you look for, and replace with the first 


for x in range(1,50):
    toOpen = ('BooksNC/Book%d.txt' % x)
    toWrite = ('BooksNew/Book%d.MD' % x)
    with open(toOpen, 'r') as file:
        filedata = file.read()

    filedata = filedata.lower()

    for x in range(0, len(MasterListFinal)):
        filedata = filedata.replace(" "+ MasterListFinal[x] + " ", " [["+ MasterListFinal[x] + "]] ")
        filedata = filedata.replace(" "+ MasterListFinal[x] + ".", " [["+ MasterListFinal[x] + "]].")
        filedata = filedata.replace(" "+ MasterListFinal[x] + ",", " [["+ MasterListFinal[x] + "]],")
        filedata = filedata.replace(" "+ MasterListFinal[x] + ":", " [["+ MasterListFinal[x] + "]]:")
        filedata = filedata.replace(" "+ MasterListFinal[x] + ";", " [["+ MasterListFinal[x] + "]];")
        filedata = filedata.replace(" "+ MasterListFinal[x] + "?", " [["+ MasterListFinal[x] + "]]?")

    for x in range(0, len(Changes)):
        filedata = filedata.replace(" "+ Changes[x][1] + " ", " " + Changes[x][1] + " [[" + Changes[x][0] + "]] ")
        filedata = filedata.replace(" "+ Changes[x][1] + ".", " " + Changes[x][1] +" [[" + Changes[x][0] + "]].")
        filedata = filedata.replace(" "+ Changes[x][1] + ",", " " + Changes[x][1] +" [[" + Changes[x][0] + "]],")
        filedata = filedata.replace(" "+ Changes[x][1] + ":", " " + Changes[x][1] +" [[" + Changes[x][0] + "]]:")
        filedata = filedata.replace(" "+ Changes[x][1] + ";", " " + Changes[x][1] +" [[" + Changes[x][0] + "]];")
        filedata = filedata.replace(" "+ Changes[x][1] + "?", " " + Changes[x][1] +" [[" + Changes[x][0] + "]]?")

    with open(toWrite, 'w') as f:
        f.write(filedata)


for x in range(0, len(MasterListFinal)):
    word = MasterListFinal[x]
    toWrite = ('tempnode/%s.MD' % word)
    with open(toWrite, 'w') as f:
        f.write("Due to limiatations in Obsidian Publish, a complete list of all instances of %s cannot be displayed online. To view, you can download and host this project locally by following the instructions here:" % word)