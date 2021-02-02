import matplotlib.pyplot as plt
import numpy as np

# input for Bisc type of cooking
array_input = [ [100, 1], [100, 1], [550, 3], [650, 1], [950, 3]]

# input for Galze type of cooking
#array_input = [ [100, 1], [100, 1], [1220, 6],[1220, 20.0/60]]

# input for Galze via Bisc type of cooking
#array_input = [ [100, 1], [100, 1], [550, 3], [650, 1], [1220, 5], [1220, 20.0/60]]

def update_line(hl, new_data):
    hl.set_xdata(np.append(hl.get_xdata(), new_data))
    hl.set_ydata(np.append(hl.get_ydata(), new_data))
    plt.draw()

def time_to_str(t):
    if t - int(t) > 0:
        diff = t - int(t)
        t = t - diff
        return  "%u:%u" % ( int(t), int(60*diff))
    else:
        return  "%u" % ( int(t))

def PreparePlot(TempratureAndTimeList):
    t = [0]
    for line in array_input:
        currTime = line[1]
        t.append(t[len(t)-1] + currTime)
    temprature = [0]
    temprature = temprature + [ line[0] for line in array_input]
    return (t, temprature)

def ConvertFromTempratureAndTime2TempratureRate(StartingTemprature, GoalTemprature, TimeToGetThere):
    TempratureRate = (1.0*(GoalTemprature - StartingTemprature))/TimeToGetThere
    return TempratureRate

def ConvertFromTempratureAndTimeList2TempratureRateAndGoalTempratureAndHoldtime(TempratureAndTimeList):
    def _print(_list):
        for line in _list:
            print("TempratureRateline " + str(line[0]) + ", GoalTemprature " + str(line[1]) + ", HoldTime " + str(line[2]))

    prev_goal_temprature = 0
    output = []
    for line in array_input:
        GoalTemprature = line[0]
        TimeToGetThere = line[1]
        if(prev_goal_temprature == GoalTemprature):
            if len(output) != 0:
                output[len(output) - 1][2] = TimeToGetThere
            else:
                raise "len must be greater than zero"
        else:
            OutTempratureRate = ConvertFromTempratureAndTime2TempratureRate(prev_goal_temprature, GoalTemprature, TimeToGetThere)
            output.append([OutTempratureRate, GoalTemprature, 0])        
        prev_goal_temprature = GoalTemprature
    _print(output)
    return output

output = ConvertFromTempratureAndTimeList2TempratureRateAndGoalTempratureAndHoldtime(array_input)
plt.figure(1)
plt.title('Bisc')
(timeList, tempratureList) = PreparePlot(array_input)
plt.plot(timeList, tempratureList)
plt.xlabel('t (hr)')
plt.ylabel('Temprature (C)')
plt.yticks(tempratureList, [str(c) for c in tempratureList])
x = [ time_to_str(c) for c in timeList]
plt.xticks(timeList, x)

prevTemprature = None
for temprature in tempratureList:
    if prevTemprature != temprature and temprature != 0:
        plt.axhline(temprature, color='gray', linewidth=0.5)

prevTime = None
for t in timeList:
    if prevTime != t and t != 0:
        plt.axvline(t, color='gray', linewidth=0.5)

columns = ('Rate', 'GoalTemprature', 'HoldTime')
cell_text = []
for line in output:
    row_text = []
    row_text.append(str(line[0]))
    row_text.append(str(line[1]))
    if line[2] < 1 and not line[2] == 0:
        minutes = line[2]*60
        row_text.append(str(minutes) + " [min]")
    else:
        row_text.append(str(line[2]) + " [h]")
    cell_text.append(row_text) 
# Add a table at the bottom of the axes
the_table = plt.table(cellText=cell_text,
                      colLabels=columns,
                      loc='bottom',
                      bbox=[0, -0.6, 0.7, 0.4])

plt.subplots_adjust(left=0.2, bottom=0.4)
plt.show()


