import sys

def loadFile( fileName ):
    s = set()

    with open( fileName, 'rt' ) as fin:
        while True:
            line = fin.readline()
            if not line:
                break

            s.add( int( line ) )

    return s

def usage():
    print( 'my_prompt>  python3 two_sum.py <min> <max> <filename>' )

def main():
    if len( sys.argv ) != 4:
        usage()
        return

    inputFileName = sys.argv[ 3 ]
    interval_min = int( sys.argv[ 1 ] )
    interval_max = int( sys.argv[ 2 ] )

    main_t_set = set()
    main_set = loadFile( inputFileName )

    # val + y = t, t in range( MIN, MAX+1 )
    while True:
        try:
            val = main_set.pop()

        except KeyError:
            break

        else:
            # create set of all y values needed to sum to t
            y_set = { t - val for t in range( interval_min, interval_max + 1 ) }

            # see which y values exist in main set
            y_intersect_main = y_set & main_set

            # put t values in t_set - recalc'd from y
            t_set = { y + val for y in y_intersect_main }

            # add to main t set with union
            main_t_set = main_t_set | t_set
            # print( 'main_t_set = {}'.format( main_t_set ) )

    print( 'size of t_set: {}'.format( len( main_t_set ) ) )

if __name__ == '__main__':
    main()
