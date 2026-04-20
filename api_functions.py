import requests


class CodeforcesAPIError(Exception):
    pass


class HandleNotFoundError(CodeforcesAPIError):
    pass


class APIConnectionError(CodeforcesAPIError):
    pass


def validate_handle(handle):
    if not handle or not handle.strip():
        raise ValueError("Handle cannot be empty!")

    handle = handle.strip()

    if len(handle) < 3 or len(handle) > 24:
        raise ValueError("Handle must be between 3 and 24 characters!")

    if not all(c.isalnum() or c in '-_.' for c in handle):
        raise ValueError("Handle can only contain letters, numbers, hyphens, underscores, and dots!")

    return handle


def user_status(handle):
    handle = validate_handle(handle)
    url = f"https://codeforces.com/api/user.status?handle={handle}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data["status"] == "OK":
            return data["result"]
        else:
            raise CodeforcesAPIError(f"API returned error: {data.get('comment', 'Unknown error')}")

    except requests.exceptions.Timeout:
        raise APIConnectionError("Request timed out. Please check your internet connection.")
    except requests.exceptions.ConnectionError:
        raise APIConnectionError("Could not connect to Codeforces. Please check your internet.")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            raise HandleNotFoundError(f"Handle '{handle}' not found on Codeforces!")
        raise APIConnectionError(f"HTTP Error: {e}")
    except ValueError:
        raise CodeforcesAPIError("Invalid response from Codeforces API.")


def user_info(handle):
    handle = validate_handle(handle)
    url = f"https://codeforces.com/api/user.info?handles={handle}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data["status"] == "OK":
            return data["result"][0]
        else:
            raise CodeforcesAPIError(f"API returned error: {data.get('comment', 'Unknown error')}")

    except requests.exceptions.Timeout:
        raise APIConnectionError("Request timed out.")
    except requests.exceptions.ConnectionError:
        raise APIConnectionError("Could not connect to Codeforces.")
    except requests.exceptions.HTTPError:
        if response.status_code == 400:
            raise HandleNotFoundError(f"Handle '{handle}' not found!")
        raise


def accepted_submissions(submissions):
    if not submissions:
        return set()

    accepted = set()
    for sub in submissions:
        if not isinstance(sub, dict):
            continue
        if sub.get("verdict") == "OK":
            problem = sub.get("problem", {})
            contest_id = problem.get("contestId", "Unknown")
            index = problem.get("index", "Unknown")
            name = problem.get("name", "Unknown")
            rating = problem.get("rating", "Unrated")
            accepted.add(f"{contest_id}-{index}-{name}-{rating}")
    return accepted