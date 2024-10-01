"""
File: term_project.py
Description:
Student Names: Amanda Roberts and Jana Kassem
Studnet UT EIDs: acr4437 and jmk4958
Course Name: CS 313E
"""

import numpy

class MaxHeap:
    def __init__(self):
        self.heap = []

    def size(self):
        '''Returns the size of this heap'''
        return len(self.heap) - 1

    def parent(self, i):
        '''Returns the parent of node at index i'''
        return (i - 1) // 2

    def left_child(self, i):
        '''Returns the left child of node at index i'''
        return 2 * i + 1

    def right_child(self, i):
        '''Returns the right child of node at index i'''
        return 2 * i + 2
    
    def swap(self, from_pos, to_pos):
        '''A helper function to swap two nodes of the heap'''
        self.heap[from_pos], self.heap[to_pos] = self.heap[to_pos], self.heap[from_pos]

    def insert(self, element):
        '''Inserts an element to the heap structure and maintain the heap property'''
        self.heap.append(element)
        current = self.size()

        while (self.heap[current] > self.heap[self.parent(current)]):
            self.swap(current, self.parent(current))
            current = self.parent(current)

    def max_heapify(self, i):
        '''Function to heapify the node at index'''
        l = self.left_child(i)
        r = self.right_child(i)
        if l <= self.size() and self.heap[l] > self.heap[i]:
            largest = l
        else:
            largest = i
        if r <= self.size() and self.heap[r] > self.heap[largest]:
            largest = r
        if largest != i :
            self.swap(i, largest)
            self.max_heapify(largest)
        
    def heapsort(self):
        n = len(self.heap)
        #Build a max heap
        for i in range(n // 2 - 1, -1, -1):
            self.max_heapify(i)

        #Extract elements one by one from the heap
        sorted_heap = []
        for i in range(n - 1, 0, -1):
            self.heap[0], self.heap[i] = self.heap[i], self.heap[0]  # Swap
            sorted_heap.append(self.heap.pop())
            self.max_heapify(0)
        
        #Append the last remaining element (the root) to the sorted heap
        sorted_heap.append(self.heap.pop())

        return sorted_heap[::-1]

def binary_search(data, value):
    left = 0
    right = len(data) - 1

    while left <= right:
        mid = left + ((right - left) // 2)

        if data[mid] == value:
            return mid
        elif value < data[mid]:
            right = mid - 1
        elif value > data[mid]:
            left = mid + 1
    #return all greater than
    return left


def find_p_value(chisq_dist, test_stat):
    '''Calculate p-value using sorted chi-squared values'''
    #find where test_stat falls in distribution
    num_above = len(chisq_dist) - binary_search(chisq_dist, test_stat)
    
    p_value = num_above / len(chisq_dist)
    return p_value


def create_sim(user_total, expected_props):
    '''Generate simulation based on user input'''
    sim_data = []
    for _ in range(10000):
        sim_data.append(numpy.random.multinomial(user_total, expected_props))
    return sim_data


def get_user_counts():
    '''Get user counts for candy combinations'''
    user_blue = input("How many Blue M&Ms: ")
    while not user_blue.isnumeric():
        print("Please enter an integer.")
        user_blue = input("How many Blue M&Ms: ")

    user_orange = input("How many Orange M&Ms: ")
    while not user_orange.isnumeric():
        print("Please enter an integer.")
        user_orange = input("How many Orange M&Ms: ")

    user_green = input("How many Green M&Ms: ")
    while not user_green.isnumeric():
        print("Please enter an integer.")
        user_green = input("How many Green M&Ms: ")

    user_yellow = input("How many Yellow M&Ms: ")
    while not user_yellow.isnumeric():
        print("Please enter an integer.")
        user_yellow = input("How many Yellow M&Ms: ")

    user_red = input("How many Red M&Ms: ")
    while not user_red.isnumeric():
        print("Please enter an integer.")
        user_red = input("How many Red M&Ms: ")

    user_brown = input("How many Brown M&Ms: ")
    while not user_brown.isnumeric():
        print("Please enter an integer.")
        user_brown = input("How many Brown M&Ms: ")

    user_observed = [int(user_blue), int(user_orange), int(user_green), int(user_yellow), int(user_red), int(user_brown)]
    user_total = sum(user_observed)

    return user_observed, user_total


def calc_chisq_single(observed, expected):
    return numpy.sum(((observed - expected) ** 2) / expected)


def calc_chisq_data(observed_data, expected_counts):
    chisq_dist_list = MaxHeap()
    for current_ob in observed_data:
        chisq = calc_chisq_single(current_ob, expected_counts)
        chisq_dist_list.insert(chisq)

    sorted_chisq_values = chisq_dist_list.heapsort()
    return sorted_chisq_values

def main():
    #company and user expected values
    expected_props = [0.24, 0.20, 0.16, 0.14, 0.13, 0.13]
    user_observed, user_total = get_user_counts()
    expected_counts = []
    for i in range(6):
        expected_counts.append(expected_props[i] * user_total)

    #simulation of M&M bags
    sim_data = create_sim(user_total, expected_props)

    #sorted list using heap
    chisq_dist = calc_chisq_data(sim_data,expected_counts)

    test_stat = calc_chisq_single(numpy.array(user_observed), numpy.array(expected_counts))
    p_value = find_p_value(chisq_dist, test_stat)

    print()
    print("P-value:", p_value)
    if p_value >= .05:
        print("Since the p-value is greater than .05, it is likely that your observed color frequencies follow the frequencies given by the company.")
    else:
        print("Since the p-value is less than .05, it is unlikely that your observed color frequencies follow the frequencies given by the company.")
    


if __name__ == "__main__":
    main()
