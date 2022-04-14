def partition(array, start, end, compare):
    #pivot is designated as first element in array if start = 0 
    pivot = array[start]

    # initialized as 2nd index in array
    low = start + 1

    # last index in array
    high = end

    while True:
        # keep updating high and move it to the left side if high is > pivot
        while low <= high and compare(array[high], pivot):
            high = high - 1

        # keep updating low and move it to the right side if low is < pivot
        while low <= high and not compare(array[low], pivot):
            low = low + 1

        #ensure that high and low pointer has not crossed each other
        #if so, means all is moved to correct position
        if low <= high:
            #swap low and high index values
            array[low], array[high] = array[high], array[low]
        else:
            break

    #move pivot into place
    array[start], array[high] = array[high], array[start]

    return high

def quickSort(array, start, end, compare):
    if start >= end:
        return

    p = partition(array, start, end, compare)

    #recursively sort left half
    quickSort(array, start, p-1, compare)

    #recursively sort right half
    quickSort(array, p+1, end, compare)
