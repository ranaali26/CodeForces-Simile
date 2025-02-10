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
