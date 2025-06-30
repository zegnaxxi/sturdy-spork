import random
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn, MofNCompleteColumn

from bip39 import word_to_bip39_index, bip39_index_to_word, bip39_wordmap, test_inverse as bip39_test_inverse
from bip39_geo import latlon_to_geo_index, geo_index_to_latlon, test_inverse as geo_test_inverse

def obfuscate(corpus: list [str]) -> list[tuple[float, float]]:
    geo_indices = list(map(lambda x: word_to_bip39_index(x), corpus))
    latlons = list(map(lambda x: geo_index_to_latlon(x), geo_indices))
    return latlons


def deobfuscate(latlons: list[tuple[float, float]]) -> list[str]:
    geo_indices = list(map(lambda x: latlon_to_geo_index(x[0], x[1]), latlons))
    words = list(map(lambda x: bip39_index_to_word(x), geo_indices))
    return words

def test_inverse():
    CORPUS_LEN = 12
    TESTS = 1000

    wordmap = bip39_wordmap()

    # Define the columns for your rich progress bar
    with Progress(
        TextColumn("[progress.description]{task.description}"), # Description text (e.g., "Running inversion tests")
        BarColumn(),                                          # The visual progress bar
        MofNCompleteColumn(),                                 # "X/Y complete" (e.g., "500/1000")
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), # Percentage completed
        TimeElapsedColumn(),                                  # Time elapsed since start
        TimeRemainingColumn(),                                # Estimated time remaining
        # You can add more columns if needed, like speed etc.
    ) as progress:
        # Add a task to the progress bar. 'total' is crucial for rich to know
        # the full scope of work.
        task = progress.add_task("[green]Running BIP39 Inversion Tests...", total=TESTS)

        for _ in range(TESTS):
            # Generate a random corpus of BIP39 words
            corpus = random.sample(sorted(wordmap.keys()), CORPUS_LEN)
            latlons = obfuscate(corpus)
            deobfuscated = deobfuscate(latlons)

            if deobfuscated != corpus:
                # Use console.print() to output the error message without disrupting
                # the live progress bar.
                progress.console.print(f"[red]Fail: {deobfuscated} != {corpus}[/red]")
                # Optionally, stop the progress bar immediately on failure
                progress.stop()
                return
            
            # Advance the progress bar for the current task by 1 step
            progress.update(task, advance=1)
            # You can uncomment this line to simulate work and see the bar in action
            # time.sleep(0.001) # Simulate some work


def user_obfuscate():
    corpus = input("Enter a list of words separated by commas: ").split(',')
    corpus = [word.strip() for word in corpus if word.strip() in bip39_wordmap()]
    
    if not corpus:
        print("No valid words provided.")
        return
    
    latlons = obfuscate(corpus)
    print(f"Obfuscated coordinates: {latlons}")
    
    deobfuscated = deobfuscate(latlons)
    print(f"Deobfuscated words: {deobfuscated}")

def user_deobfuscate():
    print("Enter latitude and longitude (or press Enter to finish). Example: 25.3125 -137.8125")

    latlons = []
    for _ in range(12):
        coord = input().strip().split(" ")
        if not len(coord) == 2:
            break
        latlons.append(tuple(map(float, coord)))

    deobfuscated = deobfuscate(latlons)
    print(f"Deobfuscated words: {deobfuscated}")


if __name__ == "__main__":
    if input("If you want to run the inverse test, type 'y': ").strip().lower() == 'y':
        bip39_test_inverse()
        geo_test_inverse()
        test_inverse()

    option = input("If you want to obfuscate your own words, type 'o', otherwise type 'd': ").strip().lower()
    if option == 'o':
        user_obfuscate()
    elif option == 'd':
        user_deobfuscate()