import pandas as pd

data = pd.read_csv('Data\YouTubeComment.csv', encoding='utf-8', on_bad_lines='skip')

with open('Data\YouTubeComment.txt', mode='w', encoding='utf-8') as f:
    f.write(data['comment_text'].str.cat(sep='\n'))
