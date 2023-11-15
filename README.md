# Bookalike
_New Words, Same Story_

## Overview

This tool is designed to process text files, breaking them into manageable chunks and rewriting them using OpenAI's
GPT-4 model. It aims to condense the text, anonymize names, alter institutions and locations, modify references to
notable figures, while preserving the core information and maintaining the original tone.

## Features
- Chunking large text files into smaller parts
- Rewriting text to condense and anonymize content
- Preserving the key information and original tone of the text
- Estimating processing time for rewriting tasks

## Usage

To use this tool, you need to have Python installed on your system. You can run the program from the command line with
the following syntax:

```
python main.py <input_file> [options]
```

Where `<input_file>` is the path to the text file you want to process, and `[options]` can include the following flags:

- `-ni`, `--non-interactive`: Run in non-interactive mode (skip any input prompts).
- `--skip-chapters <chapters>`: Comma-separated list of chapter numbers to exclude from processing.
- `--fast`: Run without artificial delay between processing chunks.

For example:

```
python main.py dracula.txt --non-interactive --skip-chapters 1,2,3 --fast
```

The program will generate a new file with the rewritten content, appending `-new` to the original filename.

## Example
Here's an example using the first chapter from Dracula, obtained via Project Gutenberg.

### Original Text
```
CHAPTER I

JONATHAN HARKER’S JOURNAL

(_Kept in shorthand._)


_3 May. Bistritz._--Left Munich at 8:35 P. M., on 1st May, arriving at
Vienna early next morning; should have arrived at 6:46, but train was an
hour late. Buda-Pesth seems a wonderful place, from the glimpse which I
got of it from the train and the little I could walk through the
streets. I feared to go very far from the station, as we had arrived
late and would start as near the correct time as possible. The
impression I had was that we were leaving the West and entering the
East; the most western of splendid bridges over the Danube, which is
here of noble width and depth, took us among the traditions of Turkish
rule.

We left in pretty good time, and came after nightfall to Klausenburgh.
Here I stopped for the night at the Hotel Royale. I had for dinner, or
rather supper, a chicken done up some way with red pepper, which was
very good but thirsty. (_Mem._, get recipe for Mina.) I asked the
waiter, and he said it was called “paprika hendl,” and that, as it was a
national dish, I should be able to get it anywhere along the
Carpathians. I found my smattering of German very useful here; indeed, I
don’t know how I should be able to get on without it.

Having had some time at my disposal when in London, I had visited the
British Museum, and made search among the books and maps in the library
regarding Transylvania; it had struck me that some foreknowledge of the
country could hardly fail to have some importance in dealing with a
nobleman of that country. I find that the district he named is in the
extreme east of the country, just on the borders of three states,
Transylvania, Moldavia and Bukovina, in the midst of the Carpathian
mountains; one of the wildest and least known portions of Europe. I was
not able to light on any map or work giving the exact locality of the
Castle Dracula, as there are no maps of this country as yet to compare
with our own Ordnance Survey maps; but I found that Bistritz, the post
town named by Count Dracula, is a fairly well-known place. I shall enter
here some of my notes, as they may refresh my memory when I talk over my
travels with Mina.
```

### Rewritten Text
```
CHAPTER I

THE TRAVELER'S DIARY

(_Maintained in abbreviated writing._)

_3rd of May, Small Eastern European Town._--Departed from a major German city at
8:35 P.M. on the 1st of May, reaching the Austrian capital early the next
morning. The train should have arrived at 6:46, but was delayed by an hour. The
Hungarian capital appeared magnificent from the brief look I had from the train
and the short walk I managed in the city. I didn't venture far from the station
due to our late arrival and the need to depart on time. It felt as though we
were transitioning from the Western world into the Eastern, marked by a grand
bridge over the wide and deep Danube River, ushering us into a region steeped in
Ottoman history.

We departed on time and arrived at a town called Klausenburgh after dark. I
stayed at the Grand Hotel for the night. For supper, I enjoyed a spicy chicken
dish that left me quite thirsty. (Note to self: obtain the recipe for my
partner.) The waiter informed me it was called "spicy fowl," a local specialty I
could find throughout the Carpathian region. My limited knowledge of German
proved invaluable here; I would have been lost without it.

During a previous stay in the British capital, I visited the Grand Library and
researched Transylvania, thinking some knowledge of the area would be useful
when dealing with a noble from there. I discovered that the noble's domain lies
in the far east of the country, near the borders of three regions: Transylvania,
Moldavia, and Bukovina, surrounded by the Carpathian mountains, one of Europe's
most remote and least known areas. I couldn't find a detailed map of the noble's
castle, as the maps available couldn't compare to our detailed home country
surveys. However, I learned that the postal town mentioned by the noble, now
called by a different name, is relatively well-known. I'm noting down some of my
findings here to refresh my memory when I recount my travels to my partner.
```

## Disclaimer

This tool is intended for legitimate purposes such as creating summaries, anonymizing documents for privacy reasons, or
adapting texts for educational use. It is not to be used for illegal activities, including but not limited to copyright
infringement or any form of plagiarism. Users are responsible for ensuring that their use of the tool complies with all
applicable laws and regulations.

## License
This project is open-source and available under the MIT License.

## Contributions

Contributions to this project are welcome. Please ensure that any contributions adhere to the existing code standards
and include appropriate tests.
