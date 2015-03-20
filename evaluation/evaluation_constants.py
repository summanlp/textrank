
# Datasource filenames.
DATASET_DIRECTORY_FORMAT = "datasets/{dataset}"
TEXT_FILENAME = "text.txt"
SUMMARIES_FILE_PATTERN = "summ[123].txt"

# Used by ROUGE.
MODEL_SUMMARIES_PATTERN = "summ.[A-Z].#ID#.txt"
SYSTEM_SUMMARIES_PATTERN = 'summ.(\d+).txt'

# Used by textrank.
MODEL_SUMMARIES_FORMAT = "summ.{text_id}.{model_id}.txt"
SYSTEM_SUMMARIES_FORMAT = "summ.{text_id}.txt"
