class Split_Text_File:
    def __init__(self, file):
        self.file_to_split = file

    def create_files(self):
        lines = 10000
        small_file = None

        with open(self.file_to_split, mode='r', encoding='utf-8') as big_file:
            for line_num, line in enumerate(big_file):
                if line_num % lines == 0:
                    if small_file:
                        small_file.close()
                    small_filename = f'Smaller Files\end_line_{line_num + lines}.txt'
                    small_file = open(small_filename, "w", encoding='utf-8')
                small_file.write(line)
            if small_file:
                small_file.close()

if __name__ =="__main__":
    test = Split_Text_File('Data\YoutubeComment.txt')
    test.create_files()
