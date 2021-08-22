import re
import pandas as pd
from shutil import copyfile
from chinese_shadowing.config import path_data
from chinese_shadowing.config import path_temporary


if __name__ == '__main__':
    folder_name = 'HSK 1-6 2012'
    media_location = path_temporary / folder_name
    path_notes = path_temporary.joinpath('notes').with_suffix('.txt')

    columns = [
        'simplified', 'traditional', 'pinyin', 'pinyin_with_number',
        'meaning', 'part_of_speech', 'audio', 'homophone', 'homograph',
        'sentence_simplified', 'sentence_traditional',
        'sentence_simplified_cloze', 'sentence_traditional_cloze',
        'sentence_pinyin', 'sentence_traditional_pinyin_with_number',
        'sentence_meaning', 'sentence_audio', 'sentence_image', 'tag'
    ]
    keep = [
        'sentence_simplified', 'sentence_traditional',
        'sentence_pinyin', 'sentence_meaning', 'sentence_audio', 'tag'
    ]

    df = pd.read_csv(path_notes, index_col=0, sep='\t', names=columns)[keep]
    df.dropna(inplace=True)
    df = df.reset_index(drop=True)

    def clean_html(raw_html: str):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', str(raw_html))
        return cleantext
    df = df.applymap(clean_html)


    def extract_hsk_level(raw_string):
        return re.search('([1-6])', raw_string).group(1)
    df['hsk'] = df['tag'].apply(extract_hsk_level)
    df.drop(columns=['tag'], inplace=True)

    def extract_filename(raw_string):
        return re.search('\[sound:(.+?)\]', raw_string).group(1)
    df['sentence_audio'] = df['sentence_audio'].apply(extract_filename)

    df['audio_file'] = df.index
    df['audio_file'] = df['audio_file'].apply(lambda s: str(s) + '.mp3')
    df['old_audio_file'] = df['sentence_audio']
    df['old_audio_file'] = df['old_audio_file'].apply(lambda s: s.replace('_1393816261464', ''))
    df.drop(columns=['sentence_audio'], inplace=True)

    df.columns = [column.replace('sentence_', '') for column in list(df.columns)]

    for index, row in df.iterrows():
        try:
            copyfile(media_location / row['old_audio_file'], path_data / row['audio_file'])
        except FileNotFoundError:
            print(f'FileNotFoundError: {row["old_audio_file"]}')

    df.drop(columns=['old_audio_file'], inplace=True)
    df.to_csv(path_data/'notes.csv', encoding='utf-8')
    print(df)
