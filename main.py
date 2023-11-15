import tiktoken
import openai
import logging
import time

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def query(prompt: str) -> tuple[str, float]:
    start_time = time.monotonic()
    response = openai.ChatCompletion.create(
        model="gpt-4-0611-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    return response.choices[0].message.content.strip(), elapsed_time


def load_book(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def split_into_chunks(text):
    tokenizer = tiktoken.TikToken()
    max_tokens = 64000
    chunks = []
    current_chunk = ""
    for line in text.split("\n"):
        tokens = tokenizer.tokenize(line)
        if (
            len(tokens) + len(tokenizer.tokenize(current_chunk)) > max_tokens
            or "CHAPTER" in line.upper()
        ):
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
    with open(output_filename, "w", encoding="utf-8") as output_file:
        for i, chunk in enumerate(chunks):
            rewritten_chunk, elapsed_time = query(
                f"""
                Please rewrite this text in original words, keeping the overall themes, values, lessons the same.
                Examples should be updated.
                Text:\n{chunk}
            """
            )
            total_time += elapsed_time
            estimated_time = total_time / (i + 1) * len(chunks)
            logger.info(f"Estimated total time: {estimated_time} seconds")
            output_file.write(rewritten_chunk + "\n\n")


def main():
    book = load_book("htwf.txt")
    chunks = split_into_chunks(book)
    logger.info(f"Number of chunks: {len(chunks)}")
    rewrite_and_save_chunks(chunks, "htwf-new.txt")


if __name__ == "__main__":
    main()
