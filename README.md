# OpenAI API Quickstart - Python example app

This is a project for the cloudbeds prompt engineering job application. It was based on the OpenAI quickstart guide for python, and expanded upon by myself.

## Description

There are a few examples:

1. A DALL-E 2 prompt generator, using a prompting method created for Midjourney by Alberto Romero via his Substack newsletter [The Algorithmic Bridge](https://thealgorithmicbridge.substack.com/)
2. A prompt generator that takes a certain past (or present) civilization and asks GPT 3 to generate a text in its characteristic style. This functionality has two steps:
   1. Retrieve the type of media that the civilization was known for
   2. Retrieve the characteristics of that civilization to refine the prompt (warmongering, erudite, religious, etc...)
3. A scientific article idea generator. Give it a subject and a field of expertise and it will generate a list of ideas (3) for scientific articles

---

This structure could be used to generate whatever our minds can wish for. Note that this specific model can be expanded as much as requeired, using a dropdown list and further specifications (formal vs. casual, different languages, etc...) that were not contemplated in this demonstration.
