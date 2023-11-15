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


def split_into_chunks(text):
    max_tokens = 64000
    chunks = []
    current_chunk = ""
    import re

    chapter_pattern = re.compile(r"^(\d+)$")
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
    return chunks


def rewrite_and_save_chunks(chunks, output_filename):
    total_time = 0
    for i, chunk in enumerate(chunks):
        if i == 0:
            input(f"Chunks created: {len(chunks)}, press any key to continue")
            continue  # first chapter is needless preamble

        original_token_count = len(list(tokenize(chunk)))
        logger.info(f"Token count of the chunk to be sent to LLM: {original_token_count}")
        rewritten_chunk, elapsed_time = query(
            f"""
           Start of Input Text:
           {chunk}
           End of Input Text.
           
           Length Reduction: Condense the text to make it about 25% shorter than the original.
           Anonymize Names: Replace all personal names with generic ones (e.g., "Dale Carnegie" becomes "John Smith").
           Alter Institutions and Locations: Change the names of specific institutions and locations to more generic or fictional ones (e.g., "University of Chicago" to "University of the Midwest").
           Modify References to Notable Figures: Replace names of famous historical or public figures with fictional names (e.g., "Franklin D. Roosevelt" becomes "Jane Doe").
           Preserve Core Information: Ensure that the key information and meaning of the text remain intact.
           Maintain Original Tone: Keep the tone of the original text as close as possible.
           Avoid Repetition: Ensure that the rewritten text does not repeat the same points unnecessarily.
           Check for Clarity: Ensure that the rewritten text is clear and easy to understand.
           Review for Consistency: Make sure that any changes in names or places are consistently applied throughout the text. 
           
           Condensed, updated Text:
        """
        )
        rewritten_token_count = len(list(tokenize(rewritten_chunk)))
        logger.info(
            f"Finished rewriting chapter {i + 1}. Original token count: {original_token_count}, Rewritten token count: {rewritten_token_count}"
        )
        total_time += elapsed_time
        estimated_time = total_time / (i + 1) * len(chunks)
        logger.info(f"Time elapsed so far: {total_time} seconds")
        logger.info(f"Estimated total time: {estimated_time} seconds")
        with open(output_filename, "a+", encoding="utf-8") as output_file:
            output_file.write(rewritten_chunk + "\n\n")
        input("Chunk written, press any key to continue")


def main():
    book = load_book("htwf.txt")
    chunks = split_into_chunks(book)
    logger.info(f"Number of chunks: {len(chunks)}")
    rewrite_and_save_chunks(chunks, "htwf-new.txt")


if __name__ == "__main__":
    main()
