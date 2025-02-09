import requests
from tqdm import tqdm

def user_status(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            return data["result"]
        else:
            print("Sorry, Data not found!")
    else:
        print(f"Sorry, Handle '{handle}' not found!")
    return []


def accepted_submissions(submissions):
    accepted = set()
    for it in submissions:
        if it.get("verdict") == "OK":
            i = it["problem"]
            problem = f"{i['contestId']}-{i['index']}-{i.get('name', 'Unknown')}-{i.get('rating', 'Unrated')}"
            accepted.add(problem)
    return accepted


def sort_rating(problem):
    parts = problem.split('-')
    if len(parts) == 4 and parts[3].isdigit():
        return int(parts[3])
    return 0

def get_problem_statistics(submissions):
    stats = {
        "total_submissions": len(submissions),
        "accepted_submissions": 0,
        "unique_accepted_problems": 0,
        "average_time_to_solve": 0,
        "problem_ratings": {},
    }

    accepted_times = []
    accepted_problems = set()

    for it in submissions:
        if it.get("verdict") == "OK":
            stats["accepted_submissions"] += 1
            problem = f"{it['problem']['contestId']}-{it['problem']['index']}"
            if problem not in accepted_problems:
                accepted_problems.add(problem)
                stats["unique_accepted_problems"] += 1
                if "creationTimeSeconds" in it:
                    accepted_times.append(it["creationTimeSeconds"])
            rating = it["problem"].get("rating", "Unrated")
            if rating != "Unrated":
                stats["problem_ratings"][rating] = stats["problem_ratings"].get(rating, 0) + 1

    if accepted_times:
        stats["average_time_to_solve"] = (max(accepted_times) - min(accepted_times)) / len(accepted_times) if len(
            accepted_times) > 1 else 0

    return stats

def display_progress_bar(iterable, desc):
    return tqdm(iterable, desc=desc, unit="submission")

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
                for problem in sorted_comparison:
                    print(problem)

        elif choice == "2":
            comparison = user_accepted - compare_to_accepted
            if len(comparison) == 0:
                print("No problems found!")
            else:
                sorted_comparison = sorted(comparison, key=sort_rating, reverse=True)
                print(f"\nProblems solved by {user} but not by {compare_to}:")
                for problem in sorted_comparison:
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