"""
5022CMD Advanced Algorithms - Question 3 (UPGRADED)
Fibonacci: Big-O derivation, Multithreading vs Single-threaded
"""

import threading
import time
import sys

# Increase recursion limit to handle Fibonacci(40) safely
sys.setrecursionlimit(10000)


# ============================================================
# FIBONACCI FUNCTION (recursive)
# ============================================================
def fibonacci(n):
    """
    Recursive Fibonacci.
    Time complexity: O(2^n) (precisely O(phi^n), phi ~ 1.618)
    Space complexity: O(n) due to recursion stack.
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ============================================================
# MULTITHREADED VERSION
# ============================================================
def run_multithreaded(nums=(35, 38, 40)):
    """
    Run Fibonacci for each n in a separate thread.
    Measures T = end_time_of_last_finished_thread - start_time_of_first_started_thread.
    """
    results = [0] * len(nums)
    start_times = [0] * len(nums)
    end_times = [0] * len(nums)

    def worker(index, n):
        start_times[index] = time.perf_counter_ns()
        results[index] = fibonacci(n)
        end_times[index] = time.perf_counter_ns()

    threads = []
    for i, n in enumerate(nums):
        t = threading.Thread(target=worker, args=(i, n))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    t_start = min(start_times)   # Start time of the first thread to start
    t_end = max(end_times)       # End time of the last thread to finish
    elapsed = t_end - t_start
    return results, elapsed


# ============================================================
# SINGLE-THREADED VERSION
# ============================================================
def run_singlethreaded(nums=(35, 38, 40)):
    """Run Fibonacci sequentially for all n."""
    start = time.perf_counter_ns()
    results = [fibonacci(n) for n in nums]
    end = time.perf_counter_ns()
    return results, end - start


# ============================================================
# EXPERIMENT RUNNER (10 ROUNDS)
# ============================================================
def run_experiment(rounds=10):
    nums = (35, 38, 40)

    # --- MULTITHREADED ---
    print("\n" + "=" * 70)
    print(" EXPERIMENT 1: Fibonacci Computation (WITH Multithreading)")
    print("=" * 70)
    print(f"{'Round':<8} | {'Fib(35)':<10} | {'Fib(38)':<10} | {'Fib(40)':<10} | {'Time (ns)':<15}")
    print("-" * 70)

    mt_times = []
    for r in range(1, rounds + 1):
        results, elapsed = run_multithreaded(nums)
        mt_times.append(elapsed)
        print(f"Round {r:<2} | {results[0]:<10} | {results[1]:<10} | {results[2]:<10} | {elapsed:>15,} ns")

    avg_mt = sum(mt_times) / len(mt_times)
    print("-" * 70)
    print(f"Average T (With Multithreading):    {avg_mt:>15,.0f} ns\n")

    # --- SINGLE-THREADED ---
    print("=" * 70)
    print(" EXPERIMENT 2: Fibonacci Computation (WITHOUT Multithreading)")
    print("=" * 70)
    print(f"{'Round':<8} | {'Fib(35)':<10} | {'Fib(38)':<10} | {'Fib(40)':<10} | {'Time (ns)':<15}")
    print("-" * 70)

    st_times = []
    for r in range(1, rounds + 1):
        results, elapsed = run_singlethreaded(nums)
        st_times.append(elapsed)
        print(f"Round {r:<2} | {results[0]:<10} | {results[1]:<10} | {results[2]:<10} | {elapsed:>15,} ns")

    avg_st = sum(st_times) / len(st_times)
    print("-" * 70)
    print(f"Average T (Without Multithreading): {avg_st:>15,.0f} ns\n")

    # --- COMPARISON ---
    print("=" * 70)
    print(" FINAL ANALYSIS")
    print("=" * 70)
    if avg_mt < avg_st:
        reduction = (1 - avg_mt / avg_st) * 100
        print(f"Observation: Multithreading reduced the average completion time")
        print(f"by approximately {reduction:.1f}%.")
    else:
        print("Observation: Multithreading did NOT reduce the average completion time.")
    print("=" * 70 + "\n")


# ============================================================
# MENU
# ============================================================
def main():
    print("=" * 60)
    print("  WELCOME TO FIBONACCI MULTITHREADING DEMO")
    print("=" * 60)

    while True:
        print("\n┌──────────────────────────────────────────┐")
        print("│                MAIN MENU                 │")
        print("├──────────────────────────────────────────┤")
        print("│  1. Run Full Experiment (10 Rounds)      │")
        print("│  2. Compute a Single Fibonacci Number    │")
        print("│  3. Run 1 Round of Comparison Only       │")
        print("│  4. Exit                                 │")
        print("└──────────────────────────────────────────┘")

        choice = input("Enter choice (1-4): ").strip()

        if choice == '1':
            print("\nRunning experiment... (This will take about 45-60 seconds)")
            print("Please wait while the 10 rounds are computed...")
            run_experiment(rounds=10)

        elif choice == '2':
            try:
                n = int(input("Enter a number (n) to compute Fibonacci: "))
                if n < 0:
                    print("  ⚠ Please enter a positive number.")
                    continue

                print(f"\nComputing Fib({n})...")
                start = time.perf_counter_ns()
                result = fibonacci(n)
                end = time.perf_counter_ns()

                print(f"  ✓ Fib({n}) = {result:,}")
                print(f"  Time taken: {end - start:,} ns")
            except ValueError:
                print("  ⚠ Invalid input. Please enter a whole number.")

        elif choice == '3':
            nums = (35, 38, 40)
            print("\n--- 1 Round Comparison ---")

            print("Running WITH Multithreading...")
            results_mt, mt_time = run_multithreaded(nums)
            print(f"  Fib(35)={results_mt[0]:,}, Fib(38)={results_mt[1]:,}, Fib(40)={results_mt[2]:,}")
            print(f"  Time T (MT): {mt_time:,} ns")

            print("\nRunning WITHOUT Multithreading...")
            results_st, st_time = run_singlethreaded(nums)
            print(f"  Fib(35)={results_st[0]:,}, Fib(38)={results_st[1]:,}, Fib(40)={results_st[2]:,}")
            print(f"  Time T (ST): {st_time:,} ns")

        elif choice == '4':
            print("\nThank you for using the Fibonacci Demo. Goodbye!")
            break
        else:
            print("  ⚠ Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()