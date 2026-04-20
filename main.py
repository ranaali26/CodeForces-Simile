from api_functions import (
    user_status, accepted_submissions, user_info,
    CodeforcesAPIError, HandleNotFoundError, APIConnectionError,
    validate_handle
)
from statistics_functions import get_problem_statistics, sort_rating
from utils import display_progress_bar, format_table, safe_input


def display_user_stats(stats, handle):
    print(f"\n{'='*50}")
    print(f"  Statistics for {handle}")
    print(f"{'='*50}")
    print(f"  Total Submissions:       {stats['total_submissions']}")
    print(f"  Accepted Submissions:    {stats['accepted_submissions']}")
    print(f"  Unique Accepted Problems:{stats['unique_accepted_problems']}")
    print(f"  Acceptance Rate:         {stats['acceptance_rate']}%")
    print(f"  Avg Attempts Before AC:  {stats['average_attempts_before_ac']}")

    print(f"\n  Problem Ratings Distribution:")
    for rating, count in sorted(stats['problem_ratings'].items()):
        bar = "█" * min(count, 30)
        print(f"    Rating {rating:>6}: {count:>3} {bar}")

    print(f"\n  Languages Used:")
    for lang, count in sorted(stats['languages_used'].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    {lang:<25}: {count}")

    print(f"\n  Verdicts Distribution:")
    for verdict, count in sorted(stats['verdicts_distribution'].items(), key=lambda x: x[1], reverse=True):
        print(f"    {verdict:<25}: {count}")


def display_comparison_table(user, friend, user_stats, friend_stats):
    print(f"\n{'='*60}")
    print(f"  Comparison: {user} vs {friend}")
    print(f"{'='*60}")

    metrics = [
        ("Total Submissions", "total_submissions"),
        ("Accepted Submissions", "accepted_submissions"),
        ("Unique Accepted", "unique_accepted_problems"),
        ("Acceptance Rate (%)", "acceptance_rate"),
        ("Avg Attempts Before AC", "average_attempts_before_ac"),
    ]

    print(f"  {'Metric':<25} {user:<15} {friend:<15}")
    print(f"  {'-'*55}")
    for name, key in metrics:
        u_val = user_stats[key]
        f_val = friend_stats[key]
        indicator = ""
        if isinstance(u_val, (int, float)) and isinstance(f_val, (int, float)):
            if u_val > f_val:
                indicator = " ✅"
            elif u_val < f_val:
                indicator = " ❌"
        print(f"  {name:<25} {str(u_val):<15} {str(f_val):<15}{indicator}")


def display_problems(problems, title):
    if not problems:
        print("No problems found!")
        return

    sorted_problems = sorted(problems, key=sort_rating, reverse=True)
    print(f"\n{title}:")
    print(f"{'='*60}")
    print(f"  {'Contest':<10} {'Index':<8} {'Name':<30} {'Rating':<8}")
    print(f"  {'-'*56}")

    for problem in display_progress_bar(sorted_problems, desc="Loading"):
        parts = problem.split('-')
        if len(parts) >= 4:
            print(f"  {parts[0]:<10} {parts[1]:<8} {parts[2]:<30} {parts[3]:<8}")
        else:
            print(f"  {problem}")


def main():
    print("╔══════════════════════════════════════╗")
    print("║       CodeForces Simile v2.0         ║")
    print("╠══════════════════════════════════════╣")
    print("║  Compare your progress with friends  ║")
    print("╚══════════════════════════════════════╝")

    try:
        user = safe_input("\nEnter your handle: ", validate_handle, "Invalid handle")
        compare_to = safe_input("Enter your friend's handle: ", validate_handle, "Invalid handle")

        print(f"\nFetching submissions for {user}...")
        user_submissions = user_status(user)
        print(f"Fetching submissions for {compare_to}...")
        compare_to_submissions = user_status(compare_to)

        print("Data fetched successfully!\n")

    except HandleNotFoundError as e:
        print(f"\n{e}")
        return
    except APIConnectionError as e:
        print(f"\nConnection Error: {e}")
        return
    except CodeforcesAPIError as e:
        print(f"\nAPI Error: {e}")
        return

    user_accepted = accepted_submissions(user_submissions)
    compare_to_accepted = accepted_submissions(compare_to_submissions)
    user_stats = get_problem_statistics(user_submissions)
    compare_to_stats = get_problem_statistics(compare_to_submissions)

    while True:
        print("\n┌─────────────────────────────────────┐")
        print("│            MENU OPTIONS              │")
        print("├─────────────────────────────────────┤")
        print("│  1. Problems solved by friend only   │")
        print("│  2. Problems solved by you only      │")
        print("│  3. Your statistics                  │")
        print("│  4. Friend's statistics              │")
        print("│  5. Compare statistics               │")
        print("│  6. Exit                             │")
        print("└─────────────────────────────────────┘")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            comparison = compare_to_accepted - user_accepted
            display_problems(comparison, f"Problems solved by {compare_to} but not by {user}")

        elif choice == "2":
            comparison = user_accepted - compare_to_accepted
            display_problems(comparison, f"Problems solved by {user} but not by {compare_to}")

        elif choice == "3":
            display_user_stats(user_stats, user)

        elif choice == "4":
            display_user_stats(compare_to_stats, compare_to)

        elif choice == "5":
            display_comparison_table(user, compare_to, user_stats, compare_to_stats)

        elif choice == "6":
            print("\nGoodbye! Keep coding!")
            break

        else:
            print("Invalid choice! Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
