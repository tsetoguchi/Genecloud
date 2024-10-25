import re
import os
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords


def __sanitize_lyrics(lyrics, artist_name):
    # Remove any characters that are invalid in filenames
    lyrics = re.sub(r'[\[\]<>:"/\\|?*,1234567890]', ' ', lyrics)
    # Remove the words "Verse" and "Chorus" (case-insensitive)
    lyrics = re.sub(rf'\b(?:Intro|Verse|Chorus|.txt|{artist_name}|---)\b', '', lyrics, flags=re.IGNORECASE)
    return lyrics


def combine_text_files(input_dir, output_file):
    # Open the output file in write mode
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Iterate through all files in the directory
        for filename in os.listdir(input_dir):
            # Check if the file is a text file
            if filename.endswith('.txt'):
                if filename == "word count.txt":
                    continue
                file_path = os.path.join(input_dir, filename)
                # Open and read the contents of the text file
                with open(file_path, 'r', encoding='utf-8') as infile:
                    # Write the filename as a separator (optional)
                    outfile.write(f'\n--- {filename} ---\n\n')
                    # Write the contents of the file to the output file
                    outfile.write(infile.read())
                    outfile.write('\n')  # Add a newline after each file's content


def create_word_cloud_for_artist(artist_name):
    combine_text_files(f"./{artist_name}", f"./{artist_name}/combined_lyrics.txt")

    with open(f'./{artist_name}/combined_lyrics.txt', 'r', encoding='utf-8') as file:
        text = __sanitize_lyrics(file.read().strip(), artist_name)

    msk = np.array(Image.open('./tweety.png'))

    # Create word cloud with the mask
    wc = WordCloud(background_color='white', mask=msk, contour_width=2,
                   contour_color='white', colormap='copper', width=1000, height=1000).generate(text)


    # Display the word cloud using matplotlib
    plt.imshow(wc, interpolation='bilinear')

    plt.axis("off")
    plt.savefig(f'./{artist_name}/word cloud.png', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    create_word_cloud_for_artist("Sematary")
