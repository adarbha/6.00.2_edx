###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================


class Cows(object):
    def __init__(self,name,cost):
        self.name = name
        self.cost = cost

    def getName(self):
        return self.name
    
    def getCost(self):
        return self.cost

    def __str__(self):
        return "{} - {}".format(self.name,self.cost)



def bulidCowsFromDict(cow_dict):
    result = []
    for key,val in cow_dict.items():
        result.append(Cows(key,val))
    return result


def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict



# Problem 1


def doGreedy1(cows_list,limit,cows_packed):
    
    if limit <= 0 or len(cows_list) == 0:
        return cows_packed
    else:
        cow_in = cows_list[0]
        if limit >= cow_in.getCost():
            limit = limit - cow_in.getCost()
            cows_packed.append(cow_in)
            doGreedy1(cows_list[1:],limit,cows_packed)
        else:
            doGreedy1(cows_list[1:],limit,cows_packed)
    return cows_packed    
    

def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    
    cows_list = bulidCowsFromDict(cows)
    cows_list_ordered = sorted(cows_list,key = lambda x:x.getCost(),reverse=True)
   
    cows_sent = []
    while len(cows_list_ordered) > 0:
        cows_packed_ordered = doGreedy1(cows_list_ordered,limit,[])
        cows_packed_names = [c.getName() for c in cows_packed_ordered]
        cows_sent.append(cows_packed_names)
        # cows_list_ordered = sorted(cows_list,key = lambda x:x.getCost(),reverse=True)
        cows_list_ordered = [cow for cow in cows_list_ordered if cow not in cows_packed_ordered]


    return cows_sent
    


# Problem 2

class Result2(object):
    def __init__(self,comb,value):
        self.comb = comb
        self.value = value

    def setComb(self,comb):
        self.comb = comb

    def setValue(self,value):
        self.value = value

    def getComb(self):
        return self.comb
    
    def getValue(self):
        return self.value

    def __str__(self):
        return "{} - {}".format(self.comb,self.value)


def get_sum_of_cow_pack(name_list,master_dict):
    result = 0
    for i in name_list:
        result+=master_dict[i]
    return result

def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    result = Result2([],0)
    min_list_size = len(list(cows.keys()))
    for item in get_partitions(list(cows.keys())):
        validity = True
        for pack in item:
            if get_sum_of_cow_pack(pack,cows) > limit:
                validity = False
                break
        if len(item) <= min_list_size and validity:
            min_list_size = len(item)
            result.setComb(item)
            result.setValue(len(item))
            
                        
    return result.getComb()

        
# Problem 3
def compare_cow_transport_algorithms(cows,limit=10):
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    start = time.time()
    greedy_cow_transport(cows)
    end = time.time()

    print("Greedy time - {}".format(end-start))

    start = time.time()
    brute_force_cow_transport(cows)
    end = time.time()

    print("Brute force time - {}".format(end - start))

    
    return


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=10

# print(greedy_cow_transport(cows, limit))
# test = brute_force_cow_transport(cows, limit)
# print(test)
# print(get_sum_of_cow_pack(['Florence', 'Moo Moo', 'Oreo', 'Herman', 'Betsy', 'Millie', 'Maggie', 'Lola', 'Milkshake'],cows))
# print(greedy_cow_transport({'Coco': 59, 'Starlight': 54, 'Rose': 42, 'Luna': 41, 'Buttercup': 11, 'Willow': 59, 'Betsy': 39, 'Abby': 28}, 120))
compare_cow_transport_algorithms(cows)

    


    



    



