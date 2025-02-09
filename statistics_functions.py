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

def sort_rating(problem):
    parts = problem.split('-')
    if len(parts) == 4 and parts[3].isdigit():
        return int(parts[3])
    return 0