# SpiceJack

SpiceJack is a tool for generating json questions and answers from documents in python.

## Usage

```python
from spicejack.pdf import PDFprocessor

def filter1(list):
    """
    Example filter
    """
    return [i.replace("badword","b*dword") for i in list]


processor = PDFprocessor(
    "/path/to/Tax_Evasion_Tutorial.pdf",
    use_legitimate = True, # Runs the processor with the openai api (See "legitimate use")
    filters = (filter1,) # Extra custom filters
)

processor.run(
    thread = True # Runs the processor in a child thread. (threading.Thread)
    process = True # Runs the processor in a child thread. (multiprocessing.Process)
    logging = True # Prints the responses from the LLM
)

```

## Legitimate use

Create a file named .env and put this:

```dotenv
OPENAI_API_KEY = "<YOUR-OPENAI-API-KEY>"
```

## Installation

```bash
pip install spicejack
```

## Support me

You can use SpiceJack for completely free, but donations are very appreciated as I am making this on an 10+ year old laptop.

### Bitcoin

bc1q7xaxer2xpxttm3vpzc8s9dutvck8u9ercxxc95

### Ethereum

0xB7351e098c80E2dCDE48BB769ac14c599E32c47E

### Monero

44Y47Sf2huJV4hx7K1JrTeKbgkPsWdRWSbEiAHRWKroaGYAnxkPjdxhUsDeiFeQ3wc6Tw8v3uYTZMbBUfcdUUgqt5HCqbtY

### Litecoin

LQzd9phuN7iPRn8p5rT1zyVssJ8nY5WjM5

## Roadmap

- [x] Python library

- [ ] Mass generation

- [ ] GUI
