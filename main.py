import dataclasses
import pandas as pd

from app.utils import generate_paths, read_txt_files
from app.conversation_splitter import texts_to_interaction
from app.kindness import calculate_kindness

def main():
    paths = generate_paths()
    pb_files = read_txt_files(paths)
    interactions = texts_to_interaction(pb_files)
    interactions = calculate_kindness(interactions)
    interactions_dicts = [dataclasses.asdict(interaction) for interaction in interactions]

    df = pd.DataFrame(interactions_dicts)
    df.to_csv("results.csv", sep=";", decimal=",")
    print(interactions_dicts)
    
    print('Done')


if __name__=="__main__":
    main()
