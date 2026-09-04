from collections import defaultdict


def get_problem_statistics(submissions):
    if not submissions:
        return {
            "total_submissions": 0,
            "accepted_submissions": 0,
            "unique_accepted_problems": 0,
            "acceptance_rate": 0,
            "average_attempts_before_ac": 0,
            "problem_ratings": {},
            "languages_used": {},
            "verdicts_distribution": {},
        }

    stats = {
        "total_submissions": len(submissions),
        "accepted_submissions": 0,
        "unique_accepted_problems": 0,
        "acceptance_rate": 0,
        "average_attempts_before_ac": 0,
        "problem_ratings": {},
        "languages_used": {},
        "verdicts_distribution": {},
    }

    accepted_problems = set()
    problem_attempts = defaultdict(int)
    languages = defaultdict(int)
    verdicts = defaultdict(int)

    for sub in submissions:
        if not isinstance(sub, dict):
            continue

        verdict = sub.get("verdict", "Unknown")
        verdicts[verdict] += 1

        lang = sub.get("programmingLanguage", "Unknown")
        languages[lang] += 1

        problem = sub.get("problem", {})
        problem_id = f"{problem.get('contestId', '?')}-{problem.get('index', '?')}"
        problem_attempts[problem_id] += 1

        if verdict == "OK":
            stats["accepted_submissions"] += 1
            if problem_id not in accepted_problems:
                accepted_problems.add(problem_id)
                stats["unique_accepted_problems"] += 1

                rating = problem.get("rating", "Unrated")
                if rating != "Unrated":
                    stats["problem_ratings"][rating] = stats["problem_ratings"].get(rating, 0) + 1

    if stats["total_submissions"] > 0:
        stats["acceptance_rate"] = round(
            (stats["accepted_submissions"] / stats["total_submissions"]) * 100, 2
        )

    if accepted_problems:
        total_attempts = sum(problem_attempts[p] for p in accepted_problems)
        stats["average_attempts_before_ac"] = round(total_attempts / len(accepted_problems), 2)

    stats["languages_used"] = dict(languages)
    stats["verdicts_distribution"] = dict(verdicts)

    return stats


def sort_rating(problem):
    parts = problem.split('-')
    if len(parts) >= 4:
        try:
            return int(parts[3])
        except ValueError:
            return 0
    return 0