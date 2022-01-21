import math,copy
import itertools

# we denote the plant by 1,2,3,4,then we let 0,1 represent the existence of plants such as 0001 means only plant 4 exists,1110 means only plant 4 not exists.
# edge cost from customer to each plant
edge_cost = {1:[(1,4),(2,6),(3,9)],2:[(1,5),(2,4),(3,7)],3:[(1,6),(2,3),(3,4)],4:[(1,8),(2,5),(3,3)],5:[(1,10),(2,8),(3,4)]}

customer_demand = [[1,8],[2,27],[3,25],[4,16],[5,18]]
#[capacity,open fee]
plant = {1:[50,100],2:[50,100],3:[50,100]}

def enumerate_plant(factory_list):

    total_f = []
    for i in range(1,int(math.pow(2,len(factory_list)))):
        total_f.append(bin(i).lstrip('0b').zfill(len(factory_list)))
    return total_f

def calculate_open_and_cap(plant_com):
    
    open_cost = 0
    capacity = 0
    for i in range(len(plant_com)):
        open_cost += plant[i+1][1]*int(plant_com[i])
        capacity += plant[i+1][0]*int(plant_com[i])

    return [open_cost,capacity]
def enumerate_allocate(demand,p_num):

    return filter(lambda x:sum(x) == demand,itertools.product(range(0,demand+1),repeat = p_num))

def enumerate_all_allocate(customer_list,p_num):

    return [enumerate_allocate(i[1],p_num) for i in customer_list]

def reform_cost(p_com):
    new_cost = []
    for m in range(1,6):
        temp = []
        for i in range(len(p_com)):
            if p_com[i] == '1':
                temp.append(edge_cost[m][i][1])
        new_cost.append(temp)
    return new_cost

def reform_cap(p_com):

    new_cap = []
    for m in range(len(p_com)):
        if p_com[m] == '1':
            new_cap.append(plant[m+1][0])
    return new_cap

def min_edge_cost(demand,p_com):

    p_int = [int(i) for i in p_com]
    alpha_index = [ i for i in range(len(p_com)) if p_com[i] == '1']
    all_p = enumerate_all_allocate(demand,sum(p_int))
    total_cost_old = 100000000000000
    new_form_cap = reform_cap(p_com)
    new_cost = reform_cost(p_com)
    final_path = ''
    for i in itertools.product(*all_p):
        count = 0
        for j in range(sum(p_int)):
            if sum([m[j] for m in i]) <= new_form_cap[j]:
                count += 1

        if count == sum(p_int):
            temp = 0
            for n in range(len(i)):
                for h in alpha_index:
                    temp += edge_cost[n+1][h][1]*i[n][alpha_index.index(h)]
            if temp <= total_cost_old:
                total_cost_old = temp
                final_path = i
    return [total_cost_old,final_path]


def summa_cost(plant_com):

    total_demand = sum([i[1] for i in customer_demand ])
    open_capacity = calculate_open_and_cap(plant_com)
    edge_cost = 0
    total_cost = 0
    if open_capacity[1] >= total_demand:
        total_edge_cost = min_edge_cost(customer_demand,plant_com)
        total_cost = open_capacity[0] + total_edge_cost[0]
        print(total_edge_cost[1])
    else:
        total_cost = -1
    return [total_cost,edge_cost]


def run():

    plant_combination_list = enumerate_plant([1,2,3])
    for p in plant_combination_list:

        total_cost = summa_cost(p)
        if total_cost[0] > 0:
            print(p+" : "+str(total_cost[0]))
        else:
            print(p+" : not enough capacity")


run()


