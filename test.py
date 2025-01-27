import itertools
import torch

# Parameters for Mega Millions
n = 70  # Total white balls
k = 5   # Ticket size
t = 2   # Minimum matching condition

def generate_combinations(n, k):
    # Generate all possible combinations of k numbers from 1 to n
    return list(itertools.combinations(range(1, n + 1), k))

def has_at_least_t_matches(set1, set2, t):
    # Check if two sets have at least 't' common numbers
    return len(set(set1).intersection(set2)) >= t

def find_minimal_tickets(n, k, t):
    all_combinations = generate_combinations(n, k)
    all_draws = generate_combinations(n, k)

    # Convert draws and combinations to torch tensors for GPU processing
    all_combinations_tensor = torch.tensor(all_combinations, device='cuda')
    all_draws_tensor = torch.tensor(all_draws, device='cuda')
    
    covered_draws = set()
    selected_tickets = []

    while len(covered_draws) < len(all_draws):
        best_ticket = None
        max_cover = 0
        uncovered_draws = set(all_draws) - covered_draws

        for ticket in all_combinations:
            # Count how many uncovered draws this ticket can cover
            cover_count = sum(1 for draw in uncovered_draws if has_at_least_t_matches(ticket, draw, t))
            if cover_count > max_cover:
                max_cover = cover_count
                best_ticket = ticket

        if best_ticket:
            selected_tickets.append(best_ticket)
            # Mark all draws covered by this ticket
            covered_draws.update(draw for draw in all_draws if has_at_least_t_matches(best_ticket, draw, t))
        else:
            break  # No more improvements possible

    return selected_tickets

# Run the optimization
selected_tickets = find_minimal_tickets(n, k, t)

# Display results
print(f"Minimal number of tickets needed: {len(selected_tickets)}")
print("Selected tickets:")
for ticket in selected_tickets:
    print(ticket)
