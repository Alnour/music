c_scale = {
    6:[0, 1, 3, 5, 7], # high e string --> treble
    5:[0, 1, 3],
    4: [0, 2],
    3: [0, 2, 3],
    2: [0, 2, 3],
    1: [0, 1, 3] # low e string --> bass
}

def shift_note(note_pair, shift):
    string_idx, note = note_pair
    c_scale_entry = c_scale[string_idx]
    orig_note_index = c_scale_entry.index(note)
    shifted_index  = orig_note_index + shift
    if shift > 0:
        while shifted_index > len(c_scale_entry) - 1:
            shifted_index = shifted_index - len(c_scale_entry)
            string_idx += 1
            c_scale_entry = c_scale[string_idx]
    else:
        while shifted_index < 0:
            string_idx -= 1
            c_scale_entry = c_scale[string_idx]
            shifted_index = shifted_index + len(c_scale_entry)
    return (string_idx, c_scale_entry[shifted_index])


def process_string_group(string_group):
    strings = string_group.split(":")
    string_idx = int(strings[0])
    notes = strings[1].split(",")
    notes = [int(note) for note in notes]
    note_pairs = [(string_idx, note) for note in notes]
    return note_pairs

def process_bar(bar):
    bar_result = []
    if bar.endswith(";"):
        bar = bar[:-1]
    string_groups = bar.split(";")
    for string_group in string_groups:
        bar_result += process_string_group(string_group)
    return bar_result
def process_line(line):
    bar_result = []
    bars = line.split("|")
    for bar in bars:
        bar_result.append(process_bar(bar))
    return bar_result
def read_notes(file):
    lines_result = []
    with open(file, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.replace(" ", "")
        lines_result += process_line(line)
    return lines_result

def shift_bar(bar, shift):
    bar_result = []
    for note_pair in bar:
        bar_result.append(shift_note(note_pair, shift))
    return bar_result
if __name__ == "__main__":
    notes_data_struct = read_notes("music_file.txt")
    shifted_bars = [shift_bar(bar, -4) for bar in notes_data_struct]
    for i, bar in enumerate(shifted_bars):
        print(f"{bar} | ")
        if i % 4 == 3:
            print("\n")