with open("students.txt", 'r') as file:
    next(file)
    x =[line.strip().split(',') for line in file]
for line in x:
    stid,name = line
