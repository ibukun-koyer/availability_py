#import the random generator library
import random
#import np
import numpy as np
#create random name stream
names = ["tonya","william", "samuel", "matt", "johnny", "cage", "lucas","will","jake","mary","olivia", "mike","rice","indigo","justin","blake", "red","black","lucas","tran","alex","judy","alex","violet","singh","khan","daniella","bruce","kent","leon"]
#create days list
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#this value is used to change the number of busy time a person can have per day
max_schedule = 20
#this value is used to set the number of users 
number_of_users = 10   

#create a random first and last name duo
def random_name():
    return f"{random.choice(names)} {random.choice(names)}"

#create a random schedule for each user
def random_schedule():
    #create a schedule
    schedule = []
    #create random times for all days of the week
    for i in days:

        string = f"{i}=>"
        random_amount = random.random() *  max_schedule 
        curr = 0
        postfix = "am"

        for j in range(int(random_amount)):
            #random time
            curr = int((random.random() * 12) + curr)
            if curr >= 12:
                postfix = "pm"
            if curr >= 23:
                string = string[0:-2]
                break
            #start time
            if j+1 == int(random_amount):
                new_time = f"{curr}:00{postfix}-"
                if curr >= 12:
                     postfix = "pm"
                new_time+=f"{curr+1}:00{postfix}"
            #end time
            else:
                new_time = f"{curr}:00{postfix}-"
                if curr >= 12:
                     postfix = "pm"
                new_time+=f"{curr+1}:00{postfix}, "

            string+=new_time
            curr+=1
        schedule.append(string)
    #return created schedule
    return schedule

#minutes must be divisible by 15
def create_chart(min, arr):
    #error checking
    if min == None:
        raise "Minutes cannot be None"
    #numbers indivisible by 15 result in invalid indexes
    if min % 15 != 0:
        raise "Minutes must be an divisible by 15"
    if min <= 0:
        raise "Minutes must be a positive number"
    #create a zeroed array
    board = np.zeros(int((60/min) * 24), dtype=np.int8)
    #index increment
    index_inc = min/60
    
    for i in arr:
        for j in i:
            #get the start and end busy time and fill in 1 in busy periods
            start = int(j["start"] / index_inc)
            end = int(j["end"] / index_inc)
            while (start <= end):
                board[start] = 1
                start+=1
    #convert back to 24-hour time representation

    #note, we could make use of board array but it is just a  bit representation and maybe unreadable to the user
    str = []
    closed = True
    curr_index = 0
    print(board)
    for i in range(len(board)):
        if board[i] == 0 and closed ==True:
            if i == 0:
                str.append({"start":0.0})
            else:
                str.append({"start": (i * index_inc)-index_inc}) 
            closed = False

        elif board[i] == 1 and closed == False:
            str[curr_index]["end"] = i * index_inc
            curr_index+=1
            closed = True

    try:
        if str[-1]["end"] == None:
            pass
    except:
        try:
            str[-1]["end"] = 0.0
        except:
            return str
    return str

    #start = arr[decimal_number/index_inc]
#THIS IS THE FUNCTION THAT ACTUALLY CHECKS FOR THE FREE SLOTS
def find_free_slots(arr):
    print("========================STAGE 3(CALCULATING FREE SPOTS)===============================")
    output_arr = []
    for i in range(7):
        print(days[i] + ": ")
        by_days = []
        for user in arr:
            by_days.append(user[i]["times"])
        #output_arr is a well formatted array that stores the free times along with its days
        output_arr.append({"day":days[i], "availability":create_chart(60, by_days)})
    return output_arr
#a user class
class user:
    #constructor
    def __init__(self):
        self.user_name = random_name()
        self.schedule = random_schedule()
    #convert time to float representation for easier reading and analysis
    def convert_to_float(self, type):
        new_array = []
        for i in range(len(self.schedule)):
            output = 0
            without = self.schedule[i].split("=>")
            times = without[1].split(",")
            out = []
            for j in times:
                new_out = j.split("-")
                index = 1
                dic = {}
                for k in new_out:
                    digits = k.split(":")
                    try:
                        if digits[1].__contains__("a") == True:
                            output = float(digits[0]) + (((float(digits[1].split("a")[0]) * 100) / 60) / 100)
                        elif digits[1].__contains__("p") == True:
                            if type == 24:
                                output = float(digits[0]) + (((float(digits[1].split("p")[0]) * 100) / 60) / 100)
                            elif type == 12:
                                output = float(digits[0]) + (((float(digits[1].split("p")[0]) * 100) / 60) / 100) + 12
                        if index == 1:
                            dic["start"] = output
                        elif index == 2:
                            dic["end"] = output
                            out.append(dic)
                        index = index + 1 
                    except:
                        continue

            new_array.append({"day": without[0], "times":out})
        return new_array

#main program
if __name__ == "__main__":
    
    users = []
    schd = []
    for i in range(number_of_users):
        #creating a random user
        newuser = user()
        users.append(newuser)
        print("==============================STAGE 1(RAW SCHEDULE)==================")
        print(users[i].user_name)
        print("--------------")
        for s in users[i].schedule:
            print(s + "\n")
        print("===============STAGE 2(CONVERT TO FLOAT REPRESENTATION)===============")
        
        schd.append(users[i].convert_to_float(24))
        #print the float representation of the schedule
        print(users[i].user_name + ":")
        print("--------------\n")
        for l in range(len(schd[i])):
            print("\t"+schd[i][l]["day"] + ":")
            for j in schd[i][l]["times"]:
                print(f"\t\t{j['start']} to {j['end']}")

    available = find_free_slots(schd)
    #the time can easily be changed from float to time, it currently is but the decimal point has been converted to a 1.0 instead of 0.6 from actual 
        #time. Also think of the float as 24 hour representations.
    print("===============STAGE 4(THE ACTUAL FREE TIME, OUTPUT IN FLOAT FORM WHICH IS CLOSE TO ACTUAL FORM)===============")
    for i in available:
        print(i["day"])
        for j in i["availability"]:
            print(f"\t{j['start']} to {j['end']}")
    
