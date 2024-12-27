import requests

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


def main():
    user = input("Enter your handle: ")
    compare_to = input("Enter your friend's handle: ")

    user_submissions = user_status(user)
    compare_to_submissions = user_status(compare_to)

    user_accepted = accepted_submissions(user_submissions)
    compare_to_accepted = accepted_submissions(compare_to_submissions)

    comparison = compare_to_accepted - user_accepted

    if len(comparison) == 0:
        print("No problems found!")
    else:
        sorted_comparison = sorted(comparison, key=sort_rating, reverse=True)
        print(f"\nProblems solved by {compare_to} but not by {user}:")
        for it in sorted_comparison:
            print(it)

if __name__ == "__main__":
    main()
