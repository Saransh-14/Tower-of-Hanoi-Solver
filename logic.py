# logic.py

# In-memory representations of the pegs
pegs_data = {
    0: [], # Peg A
    1: [], # Peg B
    2: []  # Peg C
}

moves_queue = []
is_animating = False

def init_pegs_data(num_disks):
   
    global pegs_data
    pegs_data[0] = list(range(num_disks, 0, -1))
    pegs_data[1] = []
    pegs_data[2] = []

def hanoi_algo(n, from_peg, to_peg, helper_peg):
    
    global moves_queue
    if n == 1:
        moves_queue.append((from_peg, to_peg))
        return
    
    hanoi_algo(n - 1, from_peg, helper_peg, to_peg)
    moves_queue.append((from_peg, to_peg))
    hanoi_algo(n - 1, helper_peg, to_peg, from_peg)