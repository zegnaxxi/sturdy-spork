from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn

def bip39_wordmap():
    BIP39_WORDMAP = {}
    with open('bip39_eng.txt', 'r') as f:
        for idx, line in enumerate(f): 
            word = line.strip()
            BIP39_WORDMAP[word] = {
                'index': idx,
                'bin': format(idx, '011b'),
            }
    
    return BIP39_WORDMAP

def word_to_bip39_index(word):
    wordmap = bip39_wordmap()
    if word in wordmap:
        return wordmap[word]['index']
    else:
        print(f"Error: '{word}' is not a valid BIP39 word.")
        return None

def bip39_index_to_word(index):
    wordmap = bip39_wordmap()
    for word, data in wordmap.items():
        if data['index'] == index:
            return word
    return None

def test_inverse():
    wordmap = bip39_wordmap()
    
# Create a Progress instance with custom columns
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        # You can add more columns here, like MofNCompleteColumn, custom status etc.
    ) as progress:
        # Add a task to the progress bar.
        # You get a task_id which you use to update this specific bar.
        task = progress.add_task("[green]Verifying BIP39 Wordmap Inverse...", total=len(wordmap))

        for word, data in wordmap.items():
            index = data['index']
            word_from_index = bip39_index_to_word(index)
            
            if word_from_index != word:
                # Use progress.console.print to avoid messing up the progress bar output
                progress.console.print(f"[red]Fail: word '{word}' with index {index} -> '{word_from_index}'[/red]")
                # If you want to stop the progress bar on failure:
                progress.stop()
                return
            
            progress.update(task, advance=1)