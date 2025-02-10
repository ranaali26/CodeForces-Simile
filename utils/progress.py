from tqdm import tqdm

def display_progress_bar(iterable, desc):
    return tqdm(iterable, desc=desc, unit="submission")