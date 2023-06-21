from anki.collection import Collection
import csv
import argparse
import logging

# Enable logging
logging.basicConfig(level=logging.ERROR)

# Create the parser
parser = argparse.ArgumentParser(description='Filter a TSV file based on an Anki deck.')

# Add the arguments
parser.add_argument('--anki_path', type=str, required=True, help='Path to your Anki collection')
parser.add_argument('--deck_name', type=str, required=True, help='Name of your Anki deck')
parser.add_argument('--input_tsv', type=str, required=True, help='Path to your input TSV file')
parser.add_argument('--output_tsv', type=str, required=True, help='Path to your output TSV file')

# Parse the arguments
args = parser.parse_args()

# Initialize Anki and select the deck
collection = Collection(args.anki_path)
deck_id = collection.decks.id(args.deck_name)
collection.decks.select(deck_id)

# Get all the notes in the deck
note_ids = collection.decks.cids(deck_id)
notes = []
for id in note_ids:
    try:
        notes.append(collection.get_card(id).note())
    except Exception as e:
        logging.error(f'Failed to get note with id {id}, error: {str(e)}')

# Get the "Kanji" field of all the notes
kanji_field = 'Kanji'
kanjis_in_deck = []
for note in notes:
    kanjis_in_deck.append(note[kanji_field])

# Read the TSV file and filter the lines
with open(args.input_tsv, 'r', newline='', encoding='utf-8') as input_file, open(args.output_tsv, 'w', newline='', encoding='utf-8') as output_file:
    reader = csv.reader(input_file, delimiter='\t')
    writer = csv.writer(output_file, delimiter='\t')

    for row in reader:
        kanji = row[0]
        if kanji in kanjis_in_deck:
            writer.writerow(row)

# Don't forget to close the collection when you're done!
collection.close()
