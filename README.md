# convo-mock
A proof-of-concept for one of August's interrogation segments in Python. Specifically, this uses the OpenAI API to support a dialogue tree by A) detecting questions with prewritten answers and B) answering questions that don't have prewritten answers based on a given character profile for the murder victim's brother.

You will need to create a `.env` file with your OpenAI API key to run the application. Add the following line to your `.env` file: `OPENAI_API_KEY=<your-key-here>`. Depending on your API subscription tier, you might run into rate limiting issues if you converse too quickly...

**TODO:** add support for conversation topic hints
