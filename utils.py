from tqdm import tqdm


def display_progress_bar(iterable, desc="Processing"):
    return tqdm(iterable, desc=desc, unit="item")


def format_table(headers, rows, col_width=20):
    header_line = "".join(h.ljust(col_width) for h in headers)
    separator = "-" * (col_width * len(headers))

    lines = [header_line, separator]
    for row in rows:
        lines.append("".join(str(val).ljust(col_width) for val in row))

    return "\n".join(lines)


def safe_input(prompt, validator=None, error_msg="Invalid input!"):
    while True:
        value = input(prompt).strip()
        if validator is None:
            return value
        try:
            return validator(value)
        except (ValueError, Exception) as e:
            print(f"{error_msg}: {e}")