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

    print(f"Creating word cloud for {artist_name}...")

    combine_text_files(f"./{artist_name}", f"./{artist_name}/combined_lyrics.txt")

    with open(f'./{artist_name}/combined_lyrics.txt', 'r', encoding='utf-8') as file:
        text = __sanitize_lyrics(file.read().strip(), artist_name)

    msk = np.array(Image.open('./tweety.png'))

    # Create word cloud with the mask
    wc = WordCloud(background_color='white', mask=msk, contour_width=2,
                   contour_color='white', colormap='bone', width=1920, height=1080).generate(text)

    # 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap',
    # 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd',
    # 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2',
    # 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r',
    # 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn',
    # 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r',
    # 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r',
    # 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr',
    # 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix',
    # 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_grey',
    # 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern',
    # 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r',
    # 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma',
    # 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r',
    # 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r',
    # 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r',
    # 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r',
    # 'winter', 'winter_r'

    # Display the word cloud using matplotlib
    plt.imshow(wc, interpolation='bilinear')

    plt.axis("off")
    plt.savefig(f'./{artist_name}/word cloud.png', bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":

    # artists = ["Sabrina Carpenter"]

    artists = ["Sabrina Carpenter", "Justin Bieber", "Future", "Gucci Mane", "Jay-Z",
               "Ariana Grande", "Bladee", "Chief Keef", "6ix9ine", "Cocteau Twins",
               "Drake", "Dua Lipa", "Eminem", "Kanye West", "Kendrick Lamar", "Lauv",
               "Lil Yachty", "Mos Def", "Nas", "Sematary", "Skrillex", "Taylor Swift",
               "The Cool Kids", "The Notorious B.I.G.", "The Weeknd", "Tupac", "Wu-Tang Clan"]

    for artist in artists:
        create_word_cloud_for_artist(artist)
