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
            Please rewrite this text in original words, keeping the overall themes, values, lessons the same. 
            Ensure the rewritten text is clear, accurate, consistent, relevant, up-to-date, well-written, and not repetitive. 
            All names should be replaced with new names.
            Any reference to the author of the book should be replaced with John Smith.
            Examples should be updated as possible in the context of 2023.
            Text:\n{chunk}
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
