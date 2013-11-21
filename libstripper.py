#gets input from user
print "Path to library to stripped."
lib_path = str(raw_input())
print "Path to text file of classes used."
classes_path = str(raw_input())
classes = []
output = open(lib_path[:-4]+"-stripped.css",'w')
# get a list of things we want to preserve from the css file
with open(classes_path) as ClassesFile:
    for class_line in ClassesFile:
        if class_line != '\n':
            classes.append(class_line.replace("\n",''))
# Get work done
lib = open(lib_path).readlines()
bracket_count=0
initiated=False
parsed_class = False
bracket_watch = False
for class_line in lib:
    parsed_class = False
    if initiated:
        if '{' in class_line:
            bracket_count+=class_line.count('{')
            bracket_watch= True
        if '}' in class_line:
            bracket_count-=class_line.count('}')
        if bracket_count>=0:
            output.write(class_line)            
        if bracket_watch == True and bracket_count==0:
            initiated = False
            bracket_watch == False
    else:
        for i in classes: 
            if i in class_line: 
                parsed_class = i
        if parsed_class:
            initiated = True
            output.write(class_line)
        if '{' in class_line:
            bracket_count+=class_line.count('{')
            bracket_watch= True
        if '}' in class_line:
            bracket_count-=class_line.count('}')
        
output.close()
