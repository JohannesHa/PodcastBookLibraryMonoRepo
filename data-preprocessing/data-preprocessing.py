import os
from pathlib import Path

def preprocess_podcast_transcripts():
    """
    Preprocess files from `raw-transcript-data` into `preprocessed-transcript-data` by removing all non text parts.
    """
    # Open every file in a folder
    RAW_TRANSCRIPT_DATA_PATH = Path("./data-preprocessing/raw-transcript-data")
    PREPROCESSED_TRANSCRIPT_DATA_PATH = Path("./data-preprocessing/preprocessed-transcript-data")
    for filename in os.listdir(RAW_TRANSCRIPT_DATA_PATH):
        if filename.endswith(".vtt"):
            with open(f"{RAW_TRANSCRIPT_DATA_PATH}/{filename}", "r") as f:
                # Read the file
                file_contents = f.read()
                # Only store every third line
                transcript_text = "".join(file_contents.splitlines()[3:][::3])
                # Store transcript text in preprocessed folder
                with open(f"{PREPROCESSED_TRANSCRIPT_DATA_PATH}/{filename}", "w") as f:
                    f.write(transcript_text)

if __name__ == "__main__":
    preprocess_podcast_transcripts()