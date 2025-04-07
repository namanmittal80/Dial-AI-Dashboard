# Prompts for conversation analysis

SENTIMENT_PROMPT = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a conversation analyzer and you follow rules. You are analyzing conversations that represent
a call between a representative of an NGO and a beneficiary. The call is surveying the beneficiary.
Analyze the following conversation and answer these specific questions:
1. Is the overall sentiment positive or negative? Answer with only one word: 'positive' or 'negative'
2. Pick max one quote of maximum 15 words that demonstrates this sentiment. Make sure this is a direct quote, do not change the words.

Respond only with the one word, and on the next line the quote. 
Do not include any other text or comments.

Here is the conversation:
{conversation_text}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

FLAGS_PROMPT = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a conversation analyzer and you follow rules. You are analyzing conversations that represent
a call between a representative of an NGO and a beneficiary. The call is surveying the beneficiary.
Analyze this conversation and answer these questions in order:
1. Should this conversation be flagged for attention? Answer only 'yes' or 'no'
2. If yes, what is the main reason for flagging? One brief sentence.
3. If yes, what is the severity? Answer with only: 'high', 'medium', or 'low'
4. If yes, what type of issue is it? Answer with only: 'technical', 'fraud', or 'urgent'
5. If yes, pick max one quote of maximum 15 words that demonstrates this sentiment. Make sure this is a direct quote, do not change the words.

Respond only with the answers in order, one per line.
Do not include any other text or comments.

Here is the conversation:
{conversation_text}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

FEEDBACK_PROMPT = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a conversation analyzer and you follow rules. You are analyzing conversations that represent
a call between a representative of an NGO and a beneficiary. The call is surveying the beneficiary.
Analyze this conversation and answer these questions in order:
1. Does this conversation contain any feedback or suggestions? Answer only 'yes' or 'no'
2. If yes, what type of feedback is it? Answer with only: 'suggestion' or 'pain_point'
3. If yes, rate the impact as: 'high', 'medium', or 'low'
4. If yes, pick max one quote of maximum 15 words that demonstrates this sentiment. Make sure this is a direct quote, do not change the words.

Respond only with the answers in order, one per line.
Do not include any other text or comments.

Here is the conversation:
{conversation_text}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>""" 