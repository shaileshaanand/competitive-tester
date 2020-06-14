#!/usr/bin/python3
def sum_prices(prices, max_limit):
    return sum(prices) - sum([price if price < max_limit else max_limit for price in prices])


if __name__ == "__main__":
    results = []
    for _ in range(int(input())):
        max_limit = int(input().split()[1])
        results.append(
            str(sum_prices(list(map(int, input().split())), max_limit)))
    print("\n".join(results))
