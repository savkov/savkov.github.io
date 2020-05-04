import namegenerator
import socket
import sys

import spacy
from planchet import PlanchetClient


def red(s):
    return '\033[91m' + str(s) + '\033[0m'


def pink(s):
    return '\033[95m' + str(s) + '\033[0m'


def green(s):
    return '\033[92m' + str(s) + '\033[0m'


def blue(s):
    return '\033[94m' + str(s) + '\033[0m'


def yellow(s):
    return '\033[93m' + str(s) + '\033[0m'


NAME = str(namegenerator.gen())
NAME_ = pink(NAME)
HOST = str(socket.gethostname())
PLANCHET_HOST = 'localhost'
PLANCHET_PORT = 5005
N_ITEMS = 100
URL = f'http://{PLANCHET_HOST}:{PLANCHET_PORT}'
JOB_INPUT_FILE = './data/news_headlines.jsonl'
JOB_OUTPUT_FILE = './data/news_headlines_output.jsonl'

idx = 1


client = PlanchetClient(URL)
nlp = spacy.load('en')
print(green('✨ Loaded spaCy ✨'))

job_name = 'spacy-ner-job'
metadata = {
    'input_file_path': JOB_INPUT_FILE,
    'output_file_path': JOB_OUTPUT_FILE
}


def parse(text):
    try:
        doc = nlp(text)
        print(green('.'), end='')
    except Exception as e:
        print(red('x'))
        print(f'[{NAME}] ❗ Error: {red(str(e))}')
        return []
    return [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]


# starting up the processing job
response = client.start_job(job_name, metadata, reader_name='JsonlReader',
                            writer_name='JsonlWriter')
if response.status_code == 200:
    print(f'[{NAME_}] ✨Started {blue(job_name)} job on Planchet✨')
else:
    print(f'[{NAME_}] ❗ Job {blue(job_name)} exists on Planchet❗')


# loading an initial batch of sentences
sentences = client.get(job_name, N_ITEMS)
if sentences:
    print(f'[{NAME_}] 🚚 Loaded {N_ITEMS} senstences from Planchet')
else:
    print(f'[{NAME_}] 🛑 {red("No sentences could be loaded")}')
    sys.exit(0)

# processing until exhausted
while sentences:
    records = []
    print(f'[{NAME_}] 🖥 Processing sentences...')
    for id_, record in sentences:
        text = record['text']
        ents = parse(text)
        if not ents:
            continue
        new_record = {
            'text': text,
            'entities': ents
        }
        records.append((id_, new_record))
    print(' 💯')
    print(f'[{NAME_}] ⬆ Sending back sentences...')
    client.send(job_name, records)
    print(f'[{NAME_}] ✔ {green("Completed batch")}', green(f'{idx}'))
    print(f'[{NAME_}] ⬇ Requesting sentences...')
    sentences = client.get(job_name, N_ITEMS)
    if sentences:
        print(f'[{NAME_}] 🚚 Loaded {N_ITEMS} senstences from Planchet')
    else:
        print(f'[{NAME_}] 🏁 No sentences left')
    idx += 1

print(f'[{NAME_}] {green("Done")} 💯')