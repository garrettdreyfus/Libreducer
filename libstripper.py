from string import *
import re
import sys
import optparse


def strip_element(line):
    #uses regex to strip element
    match = re.search(r'<.*?\b\w+\b', line)
    if match:
        element = match.group()
        element = element.replace('<', '')
        element = element.rstrip().lstrip()
        return element
    return None


def strip_id(line):
    #uses regex to strip id
    match = re.search(r' id.*?=.*?\"(.+?)\"', line)
    if match:
        element = match.group()
        element = element.replace(' id', '').replace('=', '')
        element = element.replace('"', '').replace("'", '')
        element = element.rstrip().lstrip()
        return element
    return None


def strip_class(line):
    #uses regex to strip id
    match = re.search(r' class.*?=.*?\"(.+?)\"', line)
    if match:
        element = match.group()
        element = element.replace(' class', '').replace('=', '')
        element = element.replace('"', '').replace("'", '')
        element = element.rstrip().lstrip()
        return element
    return None


def strip_classes(classes_path):
    classes = []
    class_file = open(classes_path).readlines()
    for line in class_file:
        if '<' in line:
            element = strip_element(line)
            if element not in classes:
                #to deal with dupe
                classes.append(elements)
            if 'class' in line:
                stripped_class = strip_class(line)
                if ' ' in stripped_class:
                    #if the lines in the form of class="alert alert-danger" for instance
                    stripped_class = stripped_class.split()
                    for word in stripped_class:
                        if word not in classes:
                            #to deal with dupes
                            classes.append(word) 
                elif stripped_class not in classes:
                    classes.append(stripped_class)
            if 'id' in line:
                stripped_id = strip_id(line)
                if stripped_id not in classes:
                    classes.append(stripped_id) 
                    #to deal with dupes

    return classes


def strip_library(lib_path, classes):
    output = open(lib_path[:-4]+"-stripped.css", 'w')
    output.truncate()
    lib = open(lib_path).readlines()
    #balance of open and closed brackets
    bracket_count = 0
    #whether or not a key word has been found, this iniates reading into the ouput file
    initiated = False
    #the parsed class starts out as nothing
    parsed_class = ""
    #whether or not a bracket has been detected, this is for cases where the first open bracket
    #is not on a seperate line
    bracket_watch = False
    #iterate through the library
    for class_line in lib:
        #reset parsedclass
        parsed_class = ""
        #if a keyword has been found
        if initiated:
            #next two ifs add and detract from bracket balance 
            if '{' in class_line:
                bracket_count += class_line.count('{')
                #denotes that we have a found an open bracket
                bracket_watch = True 
            if '}' in class_line:
                bracket_count -= class_line.count('}')
                # if the brackets haven't been closed add it to the new file
            if bracket_count >= 0:
                output.write(class_line)
                #so if we have found an open bracket and the brackets are balanced we should stop writing to the file
            if bracket_watch and bracket_count == 0:
                initiated = False
                bracket_watch = False
        else:
            #iterates through classes to see if a keywords in the line
            for keyword in classes:
                if keyword:
                    match = re.search(r"\b" + re.escape(keyword) + r"\b", class_line)
                    if match:
                        parsed_class = keyword
            # if there is a keyword we should initiate writing and write that line
            if parsed_class:
                initiated = True
                output.write(class_line)
            # for cases like input{ where the bracket would otherwise not be detected
            if '{' in class_line: 
                bracket_count += class_line.count('{')
                bracket_watch = True
            if '}' in class_line:
                bracket_count -= class_line.count('}')
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


def min(path):
    #This is code from http://stackoverflow.com/questions/222581/python-script-for-minifying-css
    css_file = open(path, 'r+b')
    css = css_file.read()
# remove comments - this will break a lot of hacks :-P
    css = re.sub(r'\s*/\*\s*\*/', "$$HACK1$$", css) # preserve IE<6 comment hack
    css = re.sub(r'/\*[\s\S]*?\*/', "", css)
    css = css.replace("$$HACK1$$", '/**/') # preserve IE<6 comment hack
# url() doesn't need quotes
    css = re.sub(r'url\((["\'])([^)]*)\1\)', r'url(\2)', css)
# spaces may be safely collapsed as generated content will collapse them anyway
    css = re.sub(r'\s+', ' ', css)
# shorten collapsable colors: #aabbcc to #abc
    css = re.sub(r'#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3(\s|;)', r'#\1\2\3\4', css)
# fragment values can loose zeros
    css = re.sub(r':\s*0(\.\d+([cm]m|e[mx]|in|p[ctx]))\s*;', r':\1;', css)
    for rule in re.findall(r'([^{]+){([^}]*)}', css):
       # we don't need spaces around operators
        selectors = [re.sub(r'(?<=[\[\(>+=])\s+|\s+(?=[=~^$*|>+\]\)])', r'', selector.strip()) for selector in rule[0].split(',')]
       # order is important, but we still want to discard repetitions
        properties = {}
        porder = []
        for prop in re.findall('(.*?):(.*?)(;|$)', rule[1]):
            key = prop[0].strip().lower()
            if key not in porder:
                porder.append(key)
            properties[key] = prop[1].strip()
       # output rule if it contains any declarations
    css_file.seek(0)
    css_file.truncate()
    css_file.write(css)
    css_file.close()


def main():
    optionparser = optparse.OptionParser()
    optionparser.add_option('--html', help="path to your html file")
    optionparser.add_option('--css', help="path to your css library")
    optionparser.add_option('--dir', help="path to directory of your html files")
    optionparser.add_option('--min', help="minify afterwords")
    options, arguments = optionparser.parse_args()
    if options.html and options.css and not options.dir:
        if options.html[-4:] == 'html' and options.css[-3:] == 'css':
            classes = strip_classes(options.html)
            strip_library(options.css, classes)
            print "success"
            if options.min:
                print options.css[:-4]+'-stripped.css'
                min(options.css[:-4]+'-stripped.css')
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
                if f[-4:] == 'html':
                    if directory[-1] == '/':
                        list_of_classes.append(strip_classes(directory+f))
                    else:
                        list_of_classes.append(strip_classes(directory+'/'+f))
        strip_library(options.css, consolidate(list_of_classes))
        if options.min:
            min(options.css[:-4]+'-stripped.css')
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
