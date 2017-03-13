assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
cols_back = '987654321'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#diag_units describes the two diagonals units
diag_units = [[rows[x]+cols[x] for x in range(len(cols))],[rows[x]+cols_back[x] for x in range(len(cols_back))]]

unitlist = row_units + column_units + square_units + diag_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values
                                      
                    
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    
    # First search for all the potential boxes (all boxes with two possibilities):
    pot_twins = [box for box in values.keys() if len(values[box]) == 2] 

    # Then find boxes with the same two possibiles numbers and that are peers:
    naked_twins = [[aux1,aux2] for aux1 in pot_twins for aux2 in peers[aux1] if values[aux1]==values[aux2]]


    # Eliminate the naked twins as possibilities for their peers

    for x in range(len(naked_twins)):   # for all the pairs found
        
        valor_twin = values[naked_twins[x][0]]   # possible values of the naked twins found
        peers_naked = peers[naked_twins[x][0]] & peers[naked_twins[x][1]]  # peers of the naked twins found
        
        for aux_peer in peers_naked:   # for all boxes that are peers of the pair (naked twins) found
            
            if len(values[aux_peer])>2:  # exclude boxes with 2 or less possible values to exclude the pair (naked twins) found
            
                #Replace with '' the two possible values of the pair (naked twins) in all the peers
                for y in valor_twin:    
                    values = assign_value(values, aux_peer, values[aux_peer].replace(y,''))
                                                                            
    return values                                   

                                      

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    
    valor=[]
    
    
    for x in grid:
        if x == '.':
            valor.append('123456789')
        else:
            valor.append(x)
    
    aux=zip(boxes,valor)
    
    return dict(aux)


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def eliminate(values):

    for x in values.keys():
        if len(values[x]) == 1:
            for y in peers[x]:
                values[y]=values[y].replace(values[x],'')
    
    
    return values

def only_choice(values):
    
    for unidad in unitlist:
        for digitos in '123456789':
            contador=0
            for box in unidad:
                if digitos in values[box]:
                    contador=contador+1
                    aux = box
                    if contador == 1:
                        values[aux] = digitos
                
                return values

def reduce_puzzle(values):
    
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        
        # Your code here: Use the Only Choice Strategy
        
        values = only_choice(values)
                                      
        # Your code here: Use the Naked Twins Strategy
                                      
        values = naked_twins(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    
    if values is False:
        return False # Fallo
    if all(len(values[s]) == 1 for s in boxes):
        return values # Resuelto
    
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
                                                                 
    values = grid_values(grid)
    values = search(values)
                                      
    return values

                                      
                                      
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
