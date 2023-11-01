import os
import pandas as pd
import json
import re
from config import PARQUET_FILEPATH, OUTPUT_FILEPATH, DATASET_SIZE, MIN_CHARS, MAX_CHARS, INSTRUCTIONS, SAMPLE_TRANSCRIPT, SAMPLE_SUMMARY, SAMPLE_TRANSCRIPT_2, SAMPLE_SUMMARY_2

def get_df_from_parquet(parquet_file):
    assert(os.path.exists(parquet_file))
    """Read a parquet file into a pandas DataFrame"""
    try:
        return pd.read_parquet(parquet_file)
    except:
        print("Error reading parquet file")
        return None

def get_texts_and_summaries(df):
    """Get the texts and summaries from the DataFrame"""
    assert(df is not None)
    texts = df['text'].tolist()
    summaries = df['summary'].tolist()
    return texts, summaries

def replace_space_before_punctuation(text):
    # Replace instances of " ," with ","
    text = re.sub(r'\s+,', ',', text)
    return text.strip()
def is_valid_entry(text, summary):
    if not text or not summary:
        return None
    if len(text) < MIN_CHARS or len(text) > MAX_CHARS:
        return None
    if len(summary) < MIN_CHARS or len(summary) > MAX_CHARS:
        return None
    # clean summaries
    if summary.startswith('\u2013'):
        summary = summary[1:]
    # remove leading and trailing whitespace
    text = replace_space_before_punctuation(text)
    summary = replace_space_before_punctuation(summary)
    if summary[0].islower():
        # Make the first letter of the summary uppercase
        summary = summary[0].upper() + summary[1:]
    return text, summary

def write_to_file(texts: list[str], summaries: list[str], output_file):
    """Write the texts and summaries to a file"""
    assert(len(texts) >= DATASET_SIZE)
    with open(output_file, 'w', encoding='utf-8') as f:
        count = 0
        alternate_sample = True
        for text, summary in zip(texts, summaries):
            result = is_valid_entry(text, summary)
            if result is None:
                continue
            text, summary = result
            if alternate_sample:
                few_shot = INSTRUCTIONS + "Sample Transcript:\n" + SAMPLE_TRANSCRIPT + "\n#END TRANSCRIPT\nSample Summary:\n" + SAMPLE_SUMMARY + "\n#END SUMMARY"
            else:
                few_shot = INSTRUCTIONS + "Sample Transcript:\n" + SAMPLE_TRANSCRIPT_2 + "\n#END TRANSCRIPT\nSample Summary:\n" + SAMPLE_SUMMARY_2 + "\n#END SUMMARY"
            
            entry = f"{few_shot}\nTranscript:\n{text}\n#END TRANSCRIPT\nSummary:\n{summary}\n#END SUMMARY"
            data = {"text" : entry}
            json.dump(data, f, ensure_ascii=False)
            f.write('\n')

            alternate_sample = not alternate_sample
            count += 1
            if count >= DATASET_SIZE:
                break

def main():
    parquet_file = PARQUET_FILEPATH
    df = get_df_from_parquet(parquet_file)
    if df is None:
        print("Fix parquet file!")
        return
    texts, summaries = get_texts_and_summaries(df)
    output_file = OUTPUT_FILEPATH
    write_to_file(texts, summaries, output_file)

if __name__ == '__main__':
    main()