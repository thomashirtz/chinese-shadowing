import json
import os
from chinese_shadowing.config import path_temporary

# Unzip to 'HSK 1-6 2012'
# Export Notes in Anki => Put notes.txt in the temporary folder

if __name__ == '__main__':
    folder_name = 'HSK 1-6 2012'
    media_location = path_temporary / folder_name
    media_file = media_location.joinpath('media')

    with open(media_file) as f:
        data = json.load(f)

    for old_name, new_name in data.items():
        if os.path.exists(media_location/old_name) and not os.path.exists(media_location/new_name):
            os.rename(media_location/old_name, media_location/new_name)

