import tiktoken
import openai
import logging

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def query(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4-0611-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


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
    with open(output_filename, "w", encoding="utf-8") as output_file:
        for chunk in chunks:
            rewritten_chunk = query(
                f"""
                Please rewrite this text in original words, keeping the overall themes, values, lessons the same.
                Examples should be updated.
                Text:\n{chunk}
            """
            )
            output_file.write(rewritten_chunk + "\n\n")


def main():
    book = load_book("htwf.txt")
    chunks = split_into_chunks(book)
    logger.info(f"Number of chunks: {len(chunks)}")
    rewrite_and_save_chunks(chunks, "htwf-new.txt")


if __name__ == "__main__":
    main()
