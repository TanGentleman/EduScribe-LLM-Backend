# EduScribe-LLM-Backend
 Pythonic dataset processing for fine-tuning LLMs. Used for a CalHacks 2023 award winning project.

EduScribe Devpost: https://devpost.com/software/eduscribe
Repository: https://github.com/VinnyXP/EduScribe

## Procedure
1. Download a dataset from huggingface. For this project, I chose https://huggingface.co/datasets/vgoldberg/longform_article_summarization
2. Set filepaths and configuration constants in `config.py`
3. Run `python parse_parquet.py`

## Features
1. Various functions to parse parquet files into a usable format for our use case, fine-tuning LLMs using the Together.ai API.
