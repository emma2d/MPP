def bubble_sort ( list1 ) :

    # Given a list of numbers as input this function will return the list sorted from smallest to largest
    # : param list : list of numbers
    # : return : sorted list of numbers from smallest to largest


    for i in range (0 , len ( list1 ) -1) :
        for j in range ( len ( list1 ) -1) :
            if ( list1 [ j ] > list1 [ j +1]) :
                temp = list1 [ j ]
                list1 [ j ] = list1 [ j +1]
                list1 [ j +1] = temp