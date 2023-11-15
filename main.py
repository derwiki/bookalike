import argparse
import json
import os

import tiktoken
from openai import OpenAI

import logging
import time

client = OpenAI()
logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def query(prompt: str) -> tuple[str, float]:
    start_time = time.monotonic()
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    return response.choices[0].message.content.strip(), elapsed_time


def load_book(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


TOKENIZER = tiktoken.encoding_for_model("gpt-4")


def tokenize(s: str) -> list:
    return TOKENIZER.encode(s)


def split_into_chunks(text, input_file):
    max_tokens = 64000
    chunks = []
    current_chunk = ""
    import re

    chapter_pattern = re.compile(r"^CHAPTER\s+([IVXLCDM]+)$", re.IGNORECASE)
    chapter_count = 0
    for line in text.split("\n"):
        tokens = tokenize(line)
        if len(tokens) + len(
            tokenize(current_chunk)
        ) > max_tokens or chapter_pattern.match(line):
            chapter_count += 1
            logger.info(
                f"Finished chapter {chapter_count - 1}, starting chapter {chapter_count}"
            )
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk += "\n" + line
    if current_chunk:
        chunks.append(current_chunk)
    chunk_file = os.path.splitext(input_file)[0] + "-chunks.json"
    with open(chunk_file, "w") as f:
        json.dump(chunks, f, indent=2)
    return chunks


def rewrite_and_save_chunks(chunks, output_filename, skip_chapters, fast, non_interactive):
    total_time = 0
    for i, chunk in enumerate(chunks):
        logger.info(f"Chunks loaded: {len(chunks)}, ready to begin!")
        if i in skip_chapters:
            logger.info(f"Skipping chapter {i}")
            continue

        original_token_count = len(list(tokenize(chunk)))
        logger.info(
            f"Token count of the chunk to be sent to LLM: {original_token_count}"
        )
        if not non_interactive:
            input("Press any key to continue with the next query")
        rewritten_chunk, elapsed_time = query(
            f"""
           Start of Input Text:
           {chunk}
           End of Input Text.
           
           Anonymize Names: Replace all personal names with generic ones (e.g., "Dale Carnegie" becomes "John Smith").
           Alter Institutions and Locations: Change the names of specific institutions and locations to more generic or fictional ones (e.g., "University of Chicago" to "University of the Midwest").
           Modify References to Notable Figures: Replace names of famous historical or public figures with fictional names (e.g., "Franklin D. Roosevelt" becomes "Jane Doe").
           Preserve Core Information: Ensure that the key information and meaning of the text remain intact.
           Maintain Original Tone: Keep the tone of the original text as close as possible.
           Avoid Repetition: Ensure that the rewritten text does not repeat the same points unnecessarily.
           Check for Clarity: Ensure that the rewritten text is clear and easy to understand.
           Review for Consistency: Make sure that any changes in names or places are consistently applied throughout the text. 
           
           Start of Output Text:
        """
        )
        rewritten_chunk = rewritten_chunk.replace("End of Output Text.", "")
        rewritten_token_count = len(list(tokenize(rewritten_chunk)))
        logger.info(
            f"Finished rewriting chapter {i + 1}. Original token count: {original_token_count}, Rewritten token count: {rewritten_token_count}"
        )
        total_time += elapsed_time
        estimated_time = total_time / (i + 1) * len(chunks)
        logger.info(f"Time elapsed so far: {round(total_time)} seconds")
        logger.info(f"Estimated total time: {round(estimated_time)} seconds")
        with open(output_filename, "a+", encoding="utf-8") as output_file:
            output_file.write(f"Chapter {i}\n\n")
            output_file.write(rewritten_chunk + "\n\n")
        if not fast:
            logger.info("Chunk written, waiting 30s")
            time.sleep(30)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The input text file")
    parser.add_argument("-ni", "--non-interactive", action="store_true", help="Run in non-interactive mode (skip any input prompts)")
    parser.add_argument("--skip-chapters", type=str, help="Comma separated list of chapters to exclude")
    parser.add_argument("--fast", action="store_true", help="Run without artificial delay between chunks")
    args = parser.parse_args()
    skip_chapters = [int(ch) for ch in args.skip_chapters.split(',')] if args.skip_chapters else []

    input_file = args.input_file
    output_file = (
        os.path.splitext(input_file)[0] + "-new" + os.path.splitext(input_file)[1]
    )

    book = load_book(input_file)
    chunk_file = os.path.splitext(input_file)[0] + "-chunks.json"
    if os.path.exists(chunk_file):
        with open(chunk_file, "r") as f:
            chunks = json.load(f)
    else:
        chunks = split_into_chunks(book, input_file)
    logger.info(f"Number of chunks: {len(chunks)}")
    if not args.non_interactive:
        input("Press any key to continue")
    rewrite_and_save_chunks(chunks, output_file, skip_chapters, args.fast, args.non_interactive)


if __name__ == "__main__":
    main()
