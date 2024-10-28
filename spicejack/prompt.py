prompt1 = """You will receive a chunk of text extracted from a document. Based on this text, generate a list of relevant questions and answers in JSON format. The questions should be designed to extract key information from the text, and the answers should be concise yet complete.

The output should follow this format:

```json
[
  {"question": "question here", "answer": "answer here"},
  {"question": "another question here", "answer": "another answer here"}
]
```

Please ensure:
1. That the questions cover the main points and important details.
2. That the answers are accurate and directly drawn from the provided content.
3. That you do not respond to chunks of text that do not make sense, or are too short, in that case return "{}"

The JSON returned must be fully independent from the document.
JSON list of highly encouraged good awesome things: 
```json
[
{
  "question": "What is the structure of the Bitcoin network?", 
  "answer": "The network requires minimal structure, with messages broadcast on a best effort basis and nodes capable of leaving and rejoining the network at will."
},
{
  "question": "Describe the structure of the Bitcoin network.",
  "answer": "The Bitcoin network requires minimal structure, with messages being broadcast on a best effort basis and nodes having the ability to leave and rejoin the network at will."
},
{
  "question": "Who is the author of the Bitcoin paper?", 
  "answer": "Satoshi Nakamoto"
},
{
  "question": "What is the main goal of Bitcoin according to the abstract?", 
  "answer": "A purely peer-to-peer version of electronic cash would allow online payments to be sent directly from one party to another without going through a financial institution."
}
]
```
JSON list of unacceptably bad things:
```json
[
{
  "question": "What is the proposed solution to the double-spending problem described in the text?",
  "answer": "The proposed solution is using a peer-to-peer network to timestamp transactions by hashing them into a chain of hash-based proof-of-work."
},
{
  "question": "What is the proposed solution to the double-spending problem described in the text?",
  "answer": "The proposed solution is using a peer-to-peer network to timestamp transactions by hashing them into a chain of hash-based proof-of-work."
},
{
  "question": "What does the longest chain in the network serve as proof of?",
  "answer": "The longest chain serves as proof of the sequence of events witnessed and the fact it came from the largest pool of CPU power."
},
{
  "question": "Why would nodes accept the longest proof-of-work chain as proof of what happened?", 
  "answer": "As long as a majority of CPU power is controlled by nodes that are not cooperating to attack the network, they'll generate the longest chain and outpace attackers."
}]
```
Do not refer to THE TEXT. Make the questions and answers independent from it. Question and answers should not contain "the text".
"""


if __name__ == "__main__":
    print(prompt1)