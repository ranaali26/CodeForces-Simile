from tqdm import tqdm


def display_progress_bar(iterable, desc="Processing"):
    return tqdm(iterable, desc=desc, unit="item")