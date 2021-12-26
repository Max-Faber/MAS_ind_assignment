from random import random
import statistics, math

def generate_scores_x(n: int) -> list[float]:
    """Generates a list (size n) of random house scores (x)"""
    return [random() for _ in range(n)]

def visit_houses(n: int) -> bool:
    house_scores_x: list[float] = generate_scores_x(n=n)
    n_reject_houses: int = round(n / math.e)
    max_score_e_sample: float = float('-inf')

    for i, house_score_x in enumerate(house_scores_x):
        if i < n_reject_houses:
            max_score_e_sample = max(max_score_e_sample, house_score_x) # We store the highest house score from the samples
            continue # Reject
        if house_score_x > max_score_e_sample:
            is_best_house = house_score_x == max(house_scores_x)
            # print(f'Renting house, current offer: {house_score_x}, max sample offer: {max_score_e_sample}, this is {"NOT" if not is_best_house else ""} the highest offer!')
            return is_best_house
    # mc_estimate = sum(house_scores_x) / len(house_scores_x)
    # mc_population_std = statistics.stdev(house_scores_x)
    return False # We didn't rent any house

def MC_sampling(n_samples: int, n_houses: int) -> None:
    n_rented_best_house = 0

    for i, _ in enumerate(range(n_samples)):
        print(f'{i + 1}/{n_samples}')
        n_rented_best_house += 1 if visit_houses(n=n_houses) else 0
    print(f'Best house is rented {round((n_rented_best_house / n_houses) * 100, 2)}% of the time!')

if __name__ == '__main__':
    n_samples = 10000
    n_houses = 1000000 # One million seems to be sufficiently large

    MC_sampling(n_samples=n_samples, n_houses=n_houses)
