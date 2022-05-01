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

def print_bar(bar, lines):
    for str_index, note in bar:
        for i in range(6):
            if (i+1) == str_index:
                lines[i] += f"--{note}"
            else:
                lines[i] += "---"
    for i, line in enumerate(lines):
        lines[i] = f"{lines[i]}|"
    return lines
def print_organized_lines(lines, tab_length = 30):
    lines = lines[::-1]
    for i in range(0, len(lines[0]), tab_length):
        for line in lines:
            print(line[i :i+tab_length])
        print("############################################################")

def shift_bar(bar, shift):
    bar_result = []
    for note_pair in bar:
        bar_result.append(shift_note(note_pair, shift))
    return bar_result
if __name__ == "__main__":
    notes_data_struct = read_notes("music_file.txt")
    shifted_bars = [shift_bar(bar, -4) for bar in notes_data_struct]
    lines = ["" for i in range(6)]
    for bar in shifted_bars:
        lines = print_bar(bar, lines)
    print_organized_lines(lines)