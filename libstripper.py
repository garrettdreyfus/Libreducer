from string import *
import re
#gets input from user
print "Path to library to be stripped."
lib_path = str(raw_input())
print "Path to your html file"
classes_path = str(raw_input())
def strip_element(line):
    match = re.search(r'<.*?\b\w+\b', line)
    if match:
        element = match.group()
        element=element.replace('<','')
        element = element.rstrip().lstrip()
        return element
    return None
def strip_id(line):
    match = re.search(r' id.*?=.*?\"(.+?)\"',line)
    if match:
        element = match.group()
        element=element.replace(' id','').replace('=','').replace('"','').replace("'",'')
        element = element.rstrip().lstrip()
        return element
    return None
def strip_class(line):
    match = re.search(r' class.*?=.*?\"(.+?)\"',line)
    if match:
        element = match.group()
        element=element.replace(' class','').replace('=','').replace('"','').replace("'",'')
        element = element.rstrip().lstrip()
        return element
    return None
def strip_classes(classes_path):
    classes=[]
    class_file = open(classes_path).readlines()
    for line in class_file:
        if '<' in line:
            element = strip_element(line)
            if element not in classes: classes.append(element)
            if 'class' in line:
                stripped_class = strip_class(line)
                if ' ' in stripped_class:
                    stripped_class=stripped_class.split()
                    for word in stripped_class: 
                        if word not in classes: classes.append(word)
                elif stripped_class not in classes: classes.append(stripped_class)
            if 'id' in line:
                stripped_id = strip_id(line)
                if stripped_id not in classes: classes.append(stripped_id)
    return classes
def strip_library(lib_path,classes):
    output = open(lib_path[:-4]+"-stripped.css",'w')
    output.truncate()
    lib = open(lib_path).readlines()
    bracket_count=0 #balance of open and closed brackets
    initiated=False #whether or not a key word has been found, this iniates reading into the ouput file
    parsed_class = "" #the parsed class starts out as nothing
    bracket_watch = False #whether or not a bracket has been detected, this is for cases where the first open bracket
                          #is not on a seperate line
    for class_line in lib: #iterate through the library
        parsed_class = ""  #reset parsedclass
        if initiated: #if a keyword has been found
            #next two ifs add and detract from bracket balance 
            if '{' in class_line:
                bracket_count+=class_line.count('{')
                bracket_watch= True #denotes that we have a found an open bracket
            if '}' in class_line:
                bracket_count-=class_line.count('}')
            if bracket_count>=0: # if the brackets haven't been closed add it to the new file
                output.write(class_line)            
            if bracket_watch == True and bracket_count==0: #so if we have found an open bracket and the brackets are balanced we should stop writing to the file
                initiated = False
                bracket_watch == False
        else:
            for keyword in classes: #iterates through classes to see if a keywords in the line
                if keyword:
                    match = re.search(r"\b" + re.escape(keyword) + r"\b",class_line)
                    if match:
                        parsed_class = keyword
            if parsed_class: # if there is a keyword we should initiate writing and write that line
                initiated = True
                output.write(class_line)
            if '{' in class_line: # for cases like input{ where the bracket would otherwise not be detected
                bracket_count+=class_line.count('{')
                bracket_watch= True
            if '}' in class_line:
                bracket_count-=class_line.count('}')
    output.close()
    return
classes= strip_classes(classes_path)
strip_library(lib_path,classes)
