import logging


def generate_paths():
    paths = []
    for i in range(1,31):
        path = f'./data/in_process/p{i}.txt'
        paths.append(path)
    logging.debug("Number of paths %s", len(paths))
    return paths

class Probanden_file:
    def __init__(self, proband: str, text: str):
        self.proband = proband
        self.text = text

def read_txt_files(paths):
    probanden_files = []
    for path in paths:
        
        with open(path, 'r') as f:
            text= f.read()
            pb = Probanden_file(proband=path[-7:-4], text=text)
            probanden_files.append(pb)
    logging.debug("Number of probanden files %s", len(probanden_files)) 
    return probanden_files