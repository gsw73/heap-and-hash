import sys
import time
import functools
import math

def clock( func ):
    @functools.wraps( func )
    def wrapper( *args, **kwargs ):
        t0 = time.perf_counter()
        result = func( *args, **kwargs )
        t1 = time.perf_counter()

        elapsedTime = t1 - t0
        if elapsedTime < 1e-3:
            units = 'us'
            scale = 1e-6
        elif elapsedTime < 1:
            units = 'ms'
            scale = 1e-3
        else:
            units = 's'
            scale = 1

        print( '[{1:8.2f}{2:s}] {0:s}'.format( func.__name__, (t1 - t0)/scale, units ) ) 
        return result
    return wrapper

class WrongHeapException( Exception ):
    pass

class Heap:

    def __init__( self, name, minHeap = True ):
        self.name = '{}-MIN'.format( name ) if minHeap else '{}-MAX'.format( name )
        self.minHeap = minHeap
        self.compare = self.a_le_b if minHeap else self.a_ge_b
        self.heap = []

    @property
    def MIN( self ):
        if not self.minHeap:
            raise WrongHeapException( minHeap )

        else:
            try:
                my_min = self.heap[ 0 ]

            except IndexError:
                my_min = -1

        return my_min

    @property
    def MAX( self ):
        if self.minHeap:
            raise WrongHeapException( minHeap )

        else:
            try:
                my_max = self.heap[ 0 ]

            except IndexError:
                my_max = -1

        return my_max

    def a_le_b( self, a, b ):
        if a <= b:
            return True
    
        else:
            return False
    
    def a_ge_b( self, a, b ):
        if a >= b:
            return True
    
        else:
            return False

    def parent( self, loc ):
        return math.floor( ( loc - 1 ) / 2 )

    def l_child( self, loc ):
        return 2 * loc + 1

    def r_child( self, loc ):
        return 2 * loc + 2

    def swap( self, loc_a, loc_b ):
        # do the swap
        self.heap[ loc_a ], self.heap[ loc_b ] = self.heap[ loc_b ], self.heap[ loc_a ]

        return

    # when there are two children and you are bubbling down, you choose
    # the child to swap with depending on if you're a MAX tree (max child)
    # or a MIN tree (min child)
    def chosen_child_loc( self, location ):
        left_child_loc = self.l_child( location )
        right_child_loc = self.r_child( location )

        if self.compare( self.heap[ left_child_loc ], self.heap[ right_child_loc ] ):
            return left_child_loc

        else:
            return right_child_loc

    def bubble_up( self, location ):
        if location == 0 or self.compare( self.heap[ self.parent( location ) ], self.heap[ location ] ):
            return

        self.swap( self.parent( location ), location ) 

        self.bubble_up( self.parent( location ) )

        return

    def one_child( self, location ):
        last_index = len( self.heap ) - 1
        if self.l_child( location ) == last_index:
            return True

        else:
            return False

    def no_children( self, location ):
        last_index = len( self.heap ) - 1
        if self.l_child( location ) > last_index:
            return True

        else:
            return False

    def bubble_down( self, location ):
        # no children... done
        if self.no_children( location ):
            return

        # only one child to compare to
        if self.one_child( location ) and self.compare( self.heap[ location ], self.heap[ self.l_child( location ) ] ):
            return

        # two children
        if self.compare( self.heap[ location ], self.heap[ self.l_child( location ) ] ) and self.compare( self.heap[ location ], self.heap[ self.r_child( location ) ] ):
            return

        # otherwise, need to swap
        if self.one_child( location ):
            swap_child_loc = self.l_child( location )

        else:
            swap_child_loc = self.chosen_child_loc( location )

        self.swap( swap_child_loc, location )

        self.bubble_down( swap_child_loc )

        return

    def insert( self, v ):
        # place element at end of list
        self.heap.append( v )
        location = len( self.heap ) - 1

        # always bubble up on insert
        self.bubble_up( location )

        return

    def delete( self, location ):

        removed_loc_is_last_loc = True if location == len( self.heap ) - 1 else False

        # need to return value being deleted
        removed_val = self.heap[ location ]

        # get last value in heap; remove it
        last_val = self.heap.pop()

        # if we remove the last location, no need to do anything else
        # this could also be the last location in the heap
        if removed_loc_is_last_loc:
            return removed_val

        # move last object into deleted spot
        self.heap[ location ] = last_val

        self.bubble_up( location )
        self.bubble_down( location )

        return removed_val

    def __len__( self ):
        return len( self.heap )

    def __str__( self ):
        st = 'Heap:  {} Length = {} Val = {}'.format( self.name, len( self.heap ), self.heap )
        return st

def readFile( inputFile ):
    inAr = []
    
    with open( inputFile, 'rt' ) as fin:
        while True:
            line = fin.readline()
            if not line:
                break

            inAr.append( int( line ) )

        return inAr

def balance( lo, hi ):
    total_length = len( lo ) + len( hi )
    lo_desired_len = math.ceil( total_length / 2 )
    hi_desired_len = math.floor( total_length / 2 )

    while len( lo ) < lo_desired_len:
        mv = hi.delete( 0 )
        lo.insert( mv )

    while len( hi ) < hi_desired_len:
        mv = lo.delete( 0 )
        hi.insert( mv )

    return

def usage():
    print( 'my_prompt>  python3 median_maintenance.py <filename>' )

def main():
    medians = []
    lo_heap = Heap( 'Lo', minHeap = False )
    hi_heap = Heap( 'Hi', minHeap = True  )
    
    if len( sys.argv ) < 2:
        usage()

    inputFile = sys.argv[ 1 ]

    fileAr = readFile( inputFile )

    for v in fileAr:
        # we default to lo tree being a little larger so anything
        # not obviously going into hi tree goes into lo; re-balance later
        if v < hi_heap.MIN or hi_heap.MIN == -1:
            lo_heap.insert( v )

        else:
            hi_heap.insert( v )

        # re-balance
        balance( lo_heap, hi_heap )

        # get median
        medians.append( lo_heap.MAX )

    # print( 'sum = {} of {}'.format( sum( medians ), medians ) )
    print( 'sum of medians is {:,d} and that val mod 10000 is {:,d}'.format( sum( medians ), sum( medians ) % 10000 ) )

    return

if __name__ == '__main__':
    main()
