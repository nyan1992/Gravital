inputfile = open('rawtext.txt', encoding="utf8")#change name as needed
outputfile = open('dataset.txt', encoding="utf8", mode="x")

for line in inputfile.readlines():
    if not line.startswith(("[", "\n", "{", "=====", "Guild:", "Channel:", "Topic:", "http")):
        outputfile.write(line)