from string import *
import re
import optparse
def strip_element(line):
    #uses regex to strip element
    match = re.search(r'<.*?\b\w+\b', line)
    if match:
        element = match.group()
        element=element.replace('<','')
        element = element.rstrip().lstrip()
        return element
    return None
def strip_id(line):
    #uses regex to strip id
    match = re.search(r' id.*?=.*?\"(.+?)\"',line)
    if match:
        element = match.group()
        element=element.replace(' id','').replace('=','').replace('"','').replace("'",'')
        element = element.rstrip().lstrip()
        return element
    return None
def strip_class(line):
    #uses regex to strip id
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
            if element not in classes: classes.append(element) #to deal with dupes
            if 'class' in line:
                stripped_class = strip_class(line)
                if ' ' in stripped_class:
                    #if the lines in the form of class="alert alert-danger" for instance
                    stripped_class=stripped_class.split()
                    for word in stripped_class: 
                        if word not in classes: classes.append(word) #to deal with dupes
                elif stripped_class not in classes: classes.append(stripped_class)
            if 'id' in line:
                stripped_id = strip_id(line)
                if stripped_id not in classes: classes.append(stripped_id) #to deal with dupes

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
def consolidate(list_of_lists):
    #consolidates a list_of_lists into a list
    classes = []
    classes = set(classes)
    for lis in list_of_lists:
        lis = set(lis)
        classes = classes.union(lis)
    return list(classes)
def main():
    optionparser = optparse.OptionParser()    
    optionparser.add_option('--html')    
    optionparser.add_option('--css')    
    optionparser.add_option('--dir')    
    options, arguments = optionparser.parse_args()
    if options.html and options.css and not options.dir:
        if options.html[-4:] == 'html' and options.css[-3:] == 'css':
            classes= strip_classes(options.html)
            strip_library(options.css,classes)
            print "success"
            return
        else: 
            print "Your file path was invalid"
            return

    if options.dir and options.css and not options.html:
        import os
        directory = options.dir
        list_of_classes = []
        for root, dirs, filenames in os.walk(directory):
            for f in filenames:
                if f[-4:]=='html':
                    if directory[-1] == '/': list_of_classes.append(strip_classes(directory+f))
                    else: list_of_classes.append(strip_classes(directory+'/'+f))
        strip_library(options.css,consolidate(list_of_classes))
        return
        
    else:
        if options.html and options.css and options.dir:
            print "You must either have html and css specified, or dir and css specified. Not both."
            return
        else: 
            print "You must either have html and css specified, or dir and css specified."
            return
if __name__ == '__main__':
    main()
