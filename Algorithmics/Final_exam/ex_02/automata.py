def automatata(regex_num, text):
    if len(text) < 2:
        return 0
    current_state = 0
    total_matches = 0
    in_match = False
    actual_index_text = 0
    if regex_num == 1:
        while actual_index_text < len(text):
            char = text[actual_index_text]
            if current_state == 0:
                if char == 'a':
                    current_state = 1
                elif char == 'b':
                    current_state = 2
                else:
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 1:
                if char == 'a':
                    current_state = 3
                elif char == 'b':
                    current_state = 4
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 2:
                if char == 'a':
                    current_state = 5
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 3:
                if char == 'a':
                    current_state = 5
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 4:
                if char == 'a':
                    current_state = 5
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            if current_state == 5:
                if char == 'a' or char == 'b':
                    current_state = 0
                    in_match = True
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            actual_index_text += 1
        return total_matches


    elif regex_num == 2:
        while actual_index_text < len(text):
            char = text[actual_index_text]
            if current_state == 0:
                if char == 'a':
                    current_state = 1
                else:
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 1:
                if char == 'b':
                    current_state = 2
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 2:
                if char == 'a':
                    current_state = 1
                    in_match = True
                elif char == 'c':
                    current_state = 3
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 3:
                if char == 'a':
                    current_state = 1
                    in_match = True
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            actual_index_text += 1
        if in_match:
            total_matches += 1

        return total_matches

    elif regex_num == 3:
        while(actual_index_text < len(text)):
            char = text[actual_index_text]
            if current_state == 0:
                if char == 'b':
                    current_state = 1
                else:
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 1:
                if char == 'a':
                    current_state = 2
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 2:
                if char == 'c':
                    current_state = 3
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 3:
                if char == 'c':
                    current_state = 2
                    in_match = True
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            actual_index_text += 1
        if in_match:
            total_matches += 1
        return total_matches

    if regex_num == 4:
        while(actual_index_text < len(text)):
            char = text[actual_index_text]
            if current_state == 0:
                if char == 'a':
                    current_state = 5
                elif char == 'b':
                    current_state = 2
                elif char == 'c':
                    current_state = 1
                else:
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 1:
                if char == 'b':
                    current_state = 3
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 2:
                if char == 'b':
                    current_state = 4
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 3:
                if char == 'b':
                    current_state = 5
                    in_match = True
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            elif current_state == 4:
                if char == 'a':
                    current_state = 5
                    in_match = True
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False
            if current_state == 5:
                if char == 'a' or char == 'b' or char == 'c':
                    current_state = 0
                    in_match = True
                else:
                    current_state = 0
                    if in_match:
                        total_matches += 1
                        in_match = False

            actual_index_text += 1
        if in_match:
            total_matches += 1
        return total_matches
def read_text_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()


text = read_text_file('injected_output_1.txt')
print(f"Matches found: {automatata(1, text)}")
