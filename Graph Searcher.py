"""
Sample output:

>>> graphSearch()
Reached: ['0101', '0200', '0201', '0202', '0301', '0302', '0311', '0312', '0313', '0314', '0315', '0321', '0390', '0413', '0414', '0431', '0433', '0441', '0452', '0454', '0463', '0465', '0466']
Not reached: ['0150', '0190', '0333', '0451', '0453', '0461', '0500', '0701', '0702', '1004', '1005', '1011']

"""
import queue
import urllib.request
import sys
from bs4 import BeautifulSoup


def graphSearch():
    webpage = urllib.request.urlopen("http://www.middlebury.edu/academics/cs/courses")
    
    CS_page = BeautifulSoup(webpage, "html.parser")

    coursedesc = []
    for desc in CS_page.find_all("div" , {"class" : "coursedesc"}): #get all the course descriptions from the website
        coursedesc.append(desc.text) 
    
    coursetitle = []
    for title in CS_page.find_all("h5" , {"class" : "coursetitle"}): #get all the course titles from the website
        coursetitle.append(title.text) 
    
    titles_cleaned = [] #clean up the titles
    for item in coursetitle:
        course = ""
        for char in item:
            if char.isdigit():
                course += char
        titles_cleaned.append(course)

    prereqs = [[]]
    index = 0
    words = []
    for item in coursedesc: #get prereqs from course descrition 
        prereq=""
        for index in range(len(item)): #this way I can iterate through letter by letter
            if item[index] == "(" and item[index+1:index+5] in ["CSCI", "MATH", "One ", "Appr"]: #read in only the words in parathesize because that is the prereqs are
                                                                                                  #and the second condition makes sure it is the right parathensize
                index+=1
                while item[index] != ")":   #keep adding letter by letter until you hit the end of the parathesize 
                    prereq += item[index] 
                    index+=1
                prereqs.append([prereq])
        if "no prerequisites" in item or "No prior experience" in item or "novices" in item:
            prereqs.append(["no prerequisites"])
    prereqs.remove(prereqs[0]) #had an empty index, so discarding it
 
    explored = {}
    adList = {}
    dict_classes = {} #this will be the course titles paired with their prereqs
    
    index = 0
    for course in titles_cleaned: #create the dict_classes dictionary
        dict_classes[course] = prereqs[index]
        explored[course] = 0 
        adList[course] = [] 
        index +=1 #so that I can iterate through the descriptions at the same time as the course titles
            
    #create adjacency list
    for course_num in dict_classes: 
        if 'Approval' in dict_classes[course_num][0] or 'approval' in dict_classes[course_num][0]:
            adList[course_num] = 'approval'
        elif 'one' in dict_classes[course_num][0] or 'One' in dict_classes[course_num][0]:
            adList['0101'].append(course_num)
            adList['0150'].append(course_num)
            adList['0190'].append(course_num)
        elif 'MATH' in dict_classes[course_num][0]:
            adList[course_num] = 'math needed'
        else:
            classes = dict_classes[course_num][0].split(" ") 
            for course in classes:     #this way we can look at each add this course a vertex connected to each prereq class
                if course.isdigit() and len(course)>= 4: #the length condition is explained in the next comment
                    adList[course].append(course_num)
                elif course.isdigit(): 
                    fixed_course = '0' + course #there were a few classes that were entered as 201 without the 0 so this ensures that the class will be searched as 0201 in the dictionary
                    adList[fixed_course].append(course_num)
          
    
    #graph search
    q = queue.Queue()
    s = '0101' #starting point
    q.put(s)
    explored[s] = 1
    while q.empty() == False:
        next_course = q.get()
        for connected_course in adList[next_course]: #this iterates through all the courses that a specific course in the adList is connected to
            if explored[connected_course] == 0: #if we have not looked at this course before then go ahead and look at it
                explored[connected_course] = 1
                q.put(connected_course) #add to queue so that we can look at what courses are connected to this course
    
    not_reached = []
    reached = []
    
    for course in explored: #create lists of classes not reached and reached from 0101
        if explored[course] != 1:
            not_reached.append(course)
        else:
            reached.append(course)
            
    print("Reached: " + str(reached))
    print("Not reached: " + str(not_reached))
    
