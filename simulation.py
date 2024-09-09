import random
import pandas as pd

#print(random.uniform(1, 10))
# Duration 60-180
# download 10-20
# swtiching 10-240

N = 10
word = 5
alpha = random.uniform(0, 0.2)
acc = 0.8878

data_pre0 = []
data_pre1 = []
data_post0 = []
data_post1 = []
data_t0 = []
data_t1 = []

S = 100
# 处理组
print('处理组')
for n in range(S):
    s = list([0]*N )
    for ii in range(N ):
        for jj in range(word):
            if random.uniform(0, 1)<alpha:
                s[ii] += 1
    #print('s   :', s)    
    s0 = sum(s)


    wifi = list([0]*N )
    for ii in range(N ):
        if random.uniform(0, 1)<0.8:
            wifi[ii] = 1
    #print('wifi:', wifi)

    pred = list([0]*N )
    for ii in range(N ):
        if random.uniform(0, 1)<acc:
            pred[ii] = 1
    #print('pred:', pred)


    Ts = list([0]*N )
    for ii in range(N ):
        Ts[ii] = round(random.uniform(60, 240))
    #print('Ts:', Ts)


    down = list([0]*N)
    for ii in range(N):
        down[ii] = round(random.uniform(10, 20))
    #print('down:', down)


    Dur = list([0]*N )
    for ii in range(N ):
        Dur[ii] = round(random.uniform(60, 180))
    #print('Dur:', Dur)

    study_time = list([0]*N)
    for ii in range(N ):
        if pred[ii] == 1:
            s[ii] = 5
            study_time[ii] = Dur[ii]
        else:
            if wifi[ii] == 1:
                s[ii] = 5
                study_time[ii] = Dur[ii] - min(down[ii], Ts[ii])
                study_time[ii] = max(study_time[ii], 0)
                
    #print('s   :', s)
    s1 = sum(s)
    # print('s0:', s0, 's1:',s1, 'time:',sum(study_time))
    data_pre1.append([n+1, 1, s0, ''])
    data_post1.append([n+1, 1, s1, ''])
    data_t1.append([n+1, 1, sum(study_time), ''])


# 对照组
print('对照')
for n in range(S):
    s = list([0]*N )
    for ii in range(N ):
        for jj in range(word):
            if random.uniform(0, 1)<alpha:
                s[ii] += 1
    #print('s   :', s)    
    s0 = sum(s)


    wifi = list([0]*N )
    for ii in range(N ):
        if random.uniform(0, 1)<0.8:
            wifi[ii] = 1
    #print('wifi:', wifi)



    Ts = list([0]*N )
    for ii in range(N ):
        Ts[ii] = round(random.uniform(60, 240))
    #print('Ts:', Ts)


    down = list([0]*N)
    for ii in range(N):
        down[ii] = round(random.uniform(10, 20))
    #print('down:', down)


    Dur = list([0]*N )
    for ii in range(N ):
        Dur[ii] = round(random.uniform(60, 180))
    #print('Dur:', Dur)

    study_time = list([0]*N)
    for ii in range(N ):
        if wifi[ii] == 1:
            s[ii] = 5
            study_time[ii] = Dur[ii] - min(down[ii], Ts[ii])
            study_time[ii] = max(study_time[ii], 0)

    s1 = sum(s)           
    #print('s   :', s)
    # print('s0:', s0, 's1:',s1, 'time:',sum(study_time))
    data_pre0.append([S+n+1, 0, '', s0])
    data_post0.append([S+n+1, 0, '', s1 ])
    data_t0.append([S+n+1, 0, '', sum(study_time)])

print('pre0:',data_pre0)
print('pre1:',data_pre1)
print('post0:',data_post0)
print('post1:',data_post1)
print('t0:',data_t0)
print('t1:',data_t1)



# Sample list
#data = [[1, 'Alice', 50.0], [2, 'Bob', 60.0], [3, 'Charlie', 70.0]]

# 前测
df_pre = pd.DataFrame(data_pre1+data_pre0, columns=['Num', 'D', 'S1', 'S0'])
df_pre.to_excel('知识点前测.xlsx', index=False)

# 后测
df_post = pd.DataFrame(data_post1+data_post0, columns=['Num', 'D', 'S1', 'S0'])
df_post.to_excel('知识点后测.xlsx', index=False)

# 时间后测
df_t = pd.DataFrame(data_t1+data_t0, columns=['Num', 'D', 'T1', 'T0'])
df_t.to_excel('学习时间后测.xlsx', index=False)
