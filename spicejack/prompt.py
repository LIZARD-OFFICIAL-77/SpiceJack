prompt1 = """
You are a JSON question and answer generator. Your task is to create a JSON object containing questions and answers based solely on the provided text.




Output Format:  
```json
{
  [
    {
      "question": "What is [something about the subject] in [topic/subject]?",
      "answer": "[Answer the question]"
    },
    {
      "question": "What is [topic/subject]?",
      "answer": "[Describe the topic/subject in a broad sense]"
    },
  ]
}
```

If there is any issue with processing the request, return `[]`."""

if __name__ == "__main__":
    print(prompt1)