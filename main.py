from api_functions import user_status, accepted_submissions
from statistics_functions import get_problem_statistics, sort_rating
from utils import display_progress_bar

def main():
    user = input("Enter your handle: ")
    compare_to = input("Enter your friend's handle: ")

    print(f"\nFetching submissions for {user}...")
    user_submissions = user_status(user)
    print(f"Fetching submissions for {compare_to}...")
    compare_to_submissions = user_status(compare_to)

    user_accepted = accepted_submissions(user_submissions)
    compare_to_accepted = accepted_submissions(compare_to_submissions)
    user_stats = get_problem_statistics(user_submissions)
    compare_to_stats = get_problem_statistics(compare_to_submissions)

    while True:
        print("\nChoose an option to display:")
        print("1. Problems solved by your friend but not by you")
        print("2. Problems solved by you but not by your friend")
        print("3. Your statistics")
        print("4. Your friend's statistics")
        print("5. Compare statistics")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            comparison = compare_to_accepted - user_accepted
            if len(comparison) == 0:
                print("No problems found!")
            else:
                sorted_comparison = sorted(comparison, key=sort_rating, reverse=True)
                print(f"\nProblems solved by {compare_to} but not by {user}:")
                for problem in display_progress_bar(sorted_comparison, desc="Displaying problems"):
                    print(problem)

        elif choice == "2":
            comparison = user_accepted - compare_to_accepted
            if len(comparison) == 0:
                print("No problems found!")
            else:
                sorted_comparison = sorted(comparison, key=sort_rating, reverse=True)
                print(f"\nProblems solved by {user} but not by {compare_to}:")
                for problem in display_progress_bar(sorted_comparison, desc="Displaying problems"):
                    print(problem)

        elif choice == "3":
            print(f"\nStatistics for {user}:")
            print(f"Total Submissions: {user_stats['total_submissions']}")
            print(f"Accepted Submissions: {user_stats['accepted_submissions']}")
            print(f"Unique Accepted Problems: {user_stats['unique_accepted_problems']}")
            print(f"Average Time to Solve (seconds): {user_stats['average_time_to_solve']:.2f}")
            print("Problem Ratings Distribution:")
            for rating, count in sorted(user_stats['problem_ratings'].items()):
                print(f"  Rating {rating}: {count} problems")

        elif choice == "4":
            print(f"\nStatistics for {compare_to}:")
            print(f"Total Submissions: {compare_to_stats['total_submissions']}")
            print(f"Accepted Submissions: {compare_to_stats['accepted_submissions']}")
            print(f"Unique Accepted Problems: {compare_to_stats['unique_accepted_problems']}")
            print(f"Average Time to Solve (seconds): {compare_to_stats['average_time_to_solve']:.2f}")
            print("Problem Ratings Distribution:")
            for rating, count in sorted(compare_to_stats['problem_ratings'].items()):
                print(f"  Rating {rating}: {count} problems")

        elif choice == "5":
            print("\nComparison of Statistics:")
            print(f"{'Metric':<25} {user:<15} {compare_to:<15}")
            print(
                f"{'Total Submissions':<25} {user_stats['total_submissions']:<15} {compare_to_stats['total_submissions']:<15}")
            print(
                f"{'Accepted Submissions':<25} {user_stats['accepted_submissions']:<15} {compare_to_stats['accepted_submissions']:<15}")
            print(
                f"{'Unique Accepted Problems':<25} {user_stats['unique_accepted_problems']:<15} {compare_to_stats['unique_accepted_problems']:<15}")
            print(
                f"{'Average Time to Solve':<25} {user_stats['average_time_to_solve']:<15.2f} {compare_to_stats['average_time_to_solve']:<15.2f}")

        elif choice == "6":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice! Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()