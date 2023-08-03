'''
Author: Kehao Chen
SID: 520305074
Unikey: kche3315
'''
import math
import os, sys
os.chdir(sys.path[0])

# find the string that need to be replaced in the file
def num_position(x: str):
    index_min = x.find("mins")  # find() method returns the index of the content in a string
    index_rep = x.find("reps")
    if index_min != -1:  # find "mins" in the string
        if x[index_min-2].isdigit() == True:  # ones place
            if x[index_min-3].isdigit() == True:  # tens place
                num = int(x[index_min-3]) * 10 + int(x[index_min-2])  # return the number needed to be replaced
            else:
                num = int(x[index_min-2])
        return num
    if index_rep != -1: # find "reps" in string
        if x[index_rep-2].isdigit() == True:
            if x[index_rep-3].isdigit() == True:
                num = int(x[index_rep-3]) * 10 + int(x[index_rep-2])
            else:
                num = int(x[index_rep-2])
        return num

# mins or reps in a line?
def min_rep(y: str):
    if "mins" in y:
        return " mins"
    elif "reps" in y:
        return " reps"
    else:
        return 0

# test letters and space in m_name
def verify_name(x: str) -> bool:
    i = 0
    while i < len(x):
        if x[i] == " " or x[i].isalpha() == True:  # is a space of letter
            i += 1
        else:
            return False
        while i == len(x):  # finish examining the string
            return True

while True:  # repeat asking input until getting right format
    m_name = input("Please enter your name: ")  # members' name
    if verify_name(m_name) == True:
        break
    else:
        print("Error: Only accept alphabetical characters and spaces for name")
        print("")
        continue
print("")  # provide a blank line between questions

while True:
    m_age = input("Please enter your age: ")  # members' age
    if m_age.isdigit() == True:  # all number in string integer?
        if int(m_age) >= 0 and int(m_age) <=110:  # only [0,110]
            break
        else:
            print("Error: The age is a number between 0 to 110")
            print("")
            continue
    else:
        print("Error: The age is a number between 0 to 110")
        print("")
        continue
m_age = int(m_age)  # change data type to integer
print("")

while True:
    m_sex = input("Please enter your biological sex (female/male): ")  # members' sex
    if (m_sex == "male") or (m_sex == "female") == True:  # m_sex must either equal to male or female excatly
        break
    else:
        print("Error: Please enter valid input")
        print("")
        continue
print("")

while True:
    print("What do you want to get out of your training? ",
          "    1. Your goal is losing weight",
          "    2. Your goal is to staying calm and relax",
          "    3. Your goal is increasing your heart rate",
          "    4. Your goal is having stronger legs",
          "    5. Your goal is having stronger ABS",
          "    6. Your goal is having stronger shoulders and arms",
          sep="\n"  # nextline after comma
          )
    m_goal = input("Choose a number between 1 to 6: ")  # members' goal
    if m_goal.isdigit() == True:
        a = int(m_goal)
        if a in (1, 2, 3, 4, 5, 6):  # choose a number
            break
        else:
            print("Error - It can only be a number between 1 to 6")
            print("")
            continue
    else:
        print("Error - It can only be a number between 1 to 6")
        print("")
        continue
m_goal = int(m_goal)
print("")

while True:
    m_traindays = input("How many days per week you can train: ")  # days per week members' can train
    if m_traindays.isdigit() == True:   
        a = int(m_traindays)
        if a in (1, 2, 3, 4, 5, 6, 7):  # choose a number
            break
        else:
            print("Error: It can only be a number between 1 to 7")
            print("")
            continue
    else:
        print("Error: It can only be a number between 1 to 7")
        print("")
        continue
m_traindays = int(m_traindays)
print("")

print("Hello ", m_name, "!", " Here is your training:", sep="")
print("-------------------------------------------------------------------------------------")  # cutting line

with open("read_me.txt") as f:  # open the file
    lines = f.readlines()  # save the lines as a list

trainday = 1  # training start from Day 1
while trainday <= m_traindays:  # recursion stop when reaching goal of training days
    print("Day", trainday)
    if trainday % 2 == 1:   # the odd days pick goals 1-6
        if m_goal == 1:  # goal 1
            i = 3   # corresponding to line 4-14 in the file
            while (i >= 3) and (i <= 13):
                if m_age <= 60:  # case 1: without any intensity reduction
                    print(lines[i], end="")  # do not type enter at the end
                elif m_age > 60 and m_age <= 65:  # case 2:  intensity reduction 0-5%
                    if min_rep(lines[i]) != 0:  # min or rep in the line
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(1-(m_age-60)*0.01)))+min_rep(lines[i])), end="")
                    else:  # min or rep not in line, means the first lines in each goal
                        print(lines[i], end="")
                elif m_age > 65 and m_age <= 75:  # case 3:  intensity reduction 5-25%
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.95-(m_age-65)*0.02)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 75 and m_age <= 80:  # case 4:  intensity reduction 25-40%
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.75-(m_age-75)*0.03)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 80:  # case 5:  intensity reduction 40-80%
                    if m_age > 90:
                        m_age = 90
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.6-(m_age-80)*0.04)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                i += 1
            print("-------------------------------------------------------------------------------------")
        elif m_goal == 2:  # goal 2
            i = 16
            while (i >= 16) and (i <= 26):
                if m_age <= 60:
                    print(lines[i], end="")
                elif m_age > 60 and m_age <= 65:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(1-(m_age-60)*0.01)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 65 and m_age <= 75:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.95-(m_age-65)*0.02)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 75 and m_age <= 80:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.75-(m_age-75)*0.03)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 80:
                    if m_age > 90:
                        m_age = 90
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.6-(m_age-80)*0.04)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                i += 1
            print("-------------------------------------------------------------------------------------")
        elif m_goal == 3:  # goal 3
            i = 29
            while (i >= 29) and (i <= 39):
                if m_age <= 60:
                    print(lines[i], end="")
                elif m_age > 60 and m_age <= 65:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(1-(m_age-60)*0.01)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 65 and m_age <= 75:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.95-(m_age-65)*0.02)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 75 and m_age <= 80:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.75-(m_age-75)*0.03)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 80:
                    if m_age > 90:
                        m_age = 90
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.6-(m_age-80)*0.04)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                i += 1
            print("-------------------------------------------------------------------------------------")
        elif m_goal == 4:  # goal 4
            i = 42
            while (i >= 42) and (i <= 51):
                if m_age <= 60:
                    print(lines[i], end="")
                elif m_age > 60 and m_age <= 65:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(1-(m_age-60)*0.01)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 65 and m_age <= 75:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.95-(m_age-65)*0.02)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 75 and m_age <= 80:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.75-(m_age-75)*0.03)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 80:
                    if m_age > 90:
                        m_age = 90
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.6-(m_age-80)*0.04)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                i += 1
            print("-------------------------------------------------------------------------------------")
        elif m_goal == 5:  # goal 5
            i = 54
            while (i >= 54) and (i <= 64):
                if m_age <= 60:
                    print(lines[i], end="")
                elif m_age > 60 and m_age <= 65:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(1-(m_age-60)*0.01)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 65 and m_age <= 75:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.95-(m_age-65)*0.02)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 75 and m_age <= 80:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.75-(m_age-75)*0.03)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 80:
                    if m_age > 90:
                        m_age = 90
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.6-(m_age-80)*0.04)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                i += 1
            print("-------------------------------------------------------------------------------------")
        elif m_goal == 6:  # goal 6
            i = 67
            while (i >= 67) and (i <= 77):
                if m_age <= 60:
                    print(lines[i], end="")
                elif m_age > 60 and m_age <= 65:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(1-(m_age-60)*0.01)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 65 and m_age <= 75:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.95-(m_age-65)*0.02)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 75 and m_age <= 80:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.75-(m_age-75)*0.03)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 80:
                    if m_age > 90:
                        m_age = 90
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.6-(m_age-80)*0.04)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                i += 1
            print("-------------------------------------------------------------------------------------")
    else:  # the odd days pick goals 7-10
        if m_sex == "male" and m_age <= 18:
            i = 80
            while (i >= 80) and (i <= 87):
                print(lines[i], end="")
                i += 1
            print("-------------------------------------------------------------------------------------")
        elif m_sex == "female" and m_age <= 18:
            i = 90
            while (i >= 90) and (i <= 97):
                print(lines[i], end="")
                i += 1
            print("-------------------------------------------------------------------------------------")
        elif m_sex == "male" and m_age >= 18:
            i = 100
            while (i >= 100) and (i <= 109):
                if m_age <= 60:
                    print(lines[i], end="")
                elif m_age > 60 and m_age <= 65:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(1-(m_age-60)*0.01)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 65 and m_age <= 75:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.95-(m_age-65)*0.02)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 75 and m_age <= 80:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.75-(m_age-75)*0.03)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 80:
                    if m_age > 90:
                        m_age = 90
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.6-(m_age-80)*0.04)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                i += 1
            print("-------------------------------------------------------------------------------------")
        elif m_sex == "female" and m_age >= 18:
            i = 112
            while (i >= 112) and (i <= 121):
                if m_age <= 60:
                    print(lines[i], end="")
                elif m_age > 60 and m_age <= 65:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(1-(m_age-60)*0.01)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 65 and m_age <= 75:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.95-(m_age-65)*0.02)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 75 and m_age <= 80:
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.75-(m_age-75)*0.03)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                elif m_age > 80:
                    if m_age > 90:
                        m_age = 90
                    if min_rep(lines[i]) != 0:
                        print(lines[i].replace(str(num_position(lines[i]))+min_rep(lines[i]), str(math.ceil(num_position(lines[i])*(0.6-(m_age-80)*0.04)))+min_rep(lines[i])), end="")
                    else:
                        print(lines[i], end="")
                i += 1
            print("-------------------------------------------------------------------------------------")
    trainday += 1  # the next day training

print("")
print("Bye", m_name + ".")