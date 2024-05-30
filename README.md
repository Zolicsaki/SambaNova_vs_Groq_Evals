# SambaNova_vs_Groq_Evals

SambaNova Llama3-8B AlpacaEval: **26.18%**

Groq Llama3-8B AlpacaEval: **19.73%**

Ouch... Groqs int8 quantization degrades the quality of the model a lot. 

To get the generations from SambaNova and Groqs API, please update the API keys with your own and run the scripts 
`python SambaNova_generations.py`
`python Groq_generations.py`

Then use the outputs of the scripts to run [AlpacaEval](https://github.com/tatsu-lab/alpaca_eval)