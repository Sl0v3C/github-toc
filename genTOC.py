import os, re, sys, shutil

FIRST = re.compile('^# ')
SECOND = re.compile('^## ')
THIRD = re.compile('^### ')
FOURTH = re.compile('^#### ')
FIFTH = re.compile('^##### ')
SIXTH = re.compile('^###### ')

DELETE = re.compile('\.|\(|\)|\/')
SPACE = re.compile(' ')
DELSPACE = re.compile('^ *| *$')
NEWLINE = re.compile('\n')
ICON = re.compile(' \[.*$')
MD = re.compile('<.*?>|<\/.*?>')

LEVEL1 = "["
LEVEL2 = "　"
LEVEL3 = "　　"
LEVEL4 = "　　　　"
LEVEL5 = "　　　　　　"
LEVEL6 = "　　　　　　　　"

content = []
each = []
origin = []
org_each = []

count_dict = {}

def enqueue(Q, e):
    Q.insert(len(Q), e)

def dequeue(Q):
    return Q.pop(0)

def backup():
    try:
        if not os.path.exists("README.md.bak"):
            shutil.copy("README.md", "README.md.bak")
    except:
        print("Cannot backup the file")

def findTitle(NO, string, LEVEL):
    global each, org_each
    if re.search(NO, string):
        if re.search(ICON, string):
            string = re.sub(ICON, '', string)
            string = string + '-'
        title = re.sub(NO, '', string)
        title = re.sub(DELSPACE, '', title)
        title = re.sub(NEWLINE, '', title)
        org_dict = {}
        org_dict[LEVEL] = re.sub('-$', '', title)
        enqueue(org_each, org_dict)
        
        title = re.sub(MD, '', title)
        title = re.sub(SPACE, '-', title)
        title = re.sub(DELETE, '', title)

        if title not in count_dict.keys():
            count_dict[title] = 1
        else:
            new = title + "-" + str(count_dict[title])
            count_dict[title] += 1
            title = new

        title_dict = {}
        title_dict[LEVEL] = title.lower()
        enqueue(each, title_dict)

def genTOC(content, org):
    string = "# Content  \n"
    count_list = [0, 0, 0, 0, 0,]
    for i, v in enumerate(content):
        if list(v.keys())[0] == 1:
            string += LEVEL1 + list(org[i].values())[0] + '](#' + list(v.values())[0] + ')' + "  \n"
        elif list(v.keys())[0] == 2:
            count_list[0] += 1
            count_list[1] = 0
            string += LEVEL2 + str(count_list[0]) + ". ["  + list(org[i].values())[0] + '](#' + list(v.values())[0] + ')' + "  \n"
        elif list(v.keys())[0] == 3:
            count_list[1] += 1
            count_list[2] = 0
            string += LEVEL3 + str(count_list[0]) + "." + str(count_list[1]) + " [" + list(org[i].values())[0] + '](#' + \
                      list(v.values())[0] + ')' + "  \n"
        elif list(v.keys())[0] == 4:
            count_list[2] += 1
            count_list[3] = 0
            string += LEVEL4 + str(count_list[0]) + "." + str(count_list[1]) + "." + str(count_list[2]) + " [" + \
                      list(org[i].values())[0] + '](#' + list(v.values())[0] + ')' + "  \n"
        elif list(v.keys())[0] == 5:
            count_list[3] += 1
            count_list[4] = 0
            string += LEVEL5 + str(count_list[0]) + "." + str(count_list[1]) + "." + str(count_list[2]) + "." + \
                      str(count_list[3]) + " [" + list(org[i].values())[0] + '](#' + list(v.values())[0] + ')' + "  \n"
        elif list(v.keys())[0] == 6:
            count_list[4] += 1
            string += LEVEL6 + str(count_list[0]) + "." + str(count_list[1]) + "." + str(count_list[2]) + "." + \
                      str(count_list[3]) + "." + str(count_list[4]) + " [" + list(org[i].values())[0] + '](#' + list(v.values())[0] + ')' + "  \n"

    return string

def getTitles():
    global each, org_each
    contentStr = ""
    try:
        with open("README.md", "r", encoding='UTF-8') as f:
            for line in f.readlines():
                if re.search(FIRST, line):
                    if each:
                        content.append(each)
                        origin.append(org_each)
                        each = []
                        org_each = []
                findTitle(FIRST, line, 1)
                findTitle(SECOND, line, 2)
                findTitle(THIRD, line, 3)
                findTitle(FOURTH, line, 4)
                findTitle(FIFTH, line, 5)
                findTitle(SIXTH, line, 6)
        if each:
            content.append(each)
        if org_each:
            origin.append(org_each)

        for i, v in enumerate(content):
            contentStr += genTOC(v, origin[i])

        return contentStr
    except:
        print(sys.exc_info())
        sys.exit()

def writeContent(string):
    string += "  \n"
    try:
        with open("README.md", "w", encoding='UTF-8') as f:
            f.write(string)
            with open("README.md.bak", "r", encoding='UTF-8') as read:
                for i in read.readlines():
                    f.write(i)

    except:
        print(sys.exc_info())
        sys.exit()

backup()
string = getTitles()
writeContent(string)

