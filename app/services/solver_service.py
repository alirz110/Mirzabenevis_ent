import pandas as pd
from collections import Counter
import json
import logging
from pathlib import Path
from functools import lru_cache

logger = logging.getLogger(__name__)

class SolverService:
    def __init__(self, data_file_path: Path):
        self._df: pd.DataFrame = self._load_data(data_file_path)
        self.NORMALIZATION_MAP = {'آ': 'ا', 'ي': 'ی', 'ك': 'ک'}

    def _load_data(self, file_path: Path) -> pd.DataFrame:
        logger.info(f"Attempting to load dictionary from: {file_path}")
        if not file_path.exists():
            logger.critical(f"FATAL: Data file not found at '{file_path}'")
            raise FileNotFoundError(f"Data file not found at {file_path}")
        
        try:
            if file_path.suffix == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported data file format. Use .csv or .xlsx")

            required_cols = {'word', 'word_normalized', 'length', 'char_counts'}
            if not required_cols.issubset(df.columns):
                raise ValueError(f"Data file is missing required columns. Required: {required_cols}")
            
            logger.info(f"🚀 Dictionary loaded successfully with {len(df)} words.")
            return df.reset_index(drop=True)
        except Exception as e:
            logger.critical(f"FATAL: Failed to load or process data file: {e}", exc_info=True)
            raise

    @lru_cache(maxsize=128)
    def normalize_text(self, text: str) -> str:
        processed_text = (text or "").strip()
        for old, new in self.NORMALIZATION_MAP.items():
            processed_text = processed_text.replace(old, new)
        return processed_text

    def find_words(self, input_letters: str) -> dict:
        if self._df is None or self._df.empty:
            return {"error": "Dictionary is not loaded."}
            
        normalized_input = self.normalize_text(input_letters)
        if not normalized_input:
            return {"error": "Input letters are empty."}
        
        input_counter = Counter(normalized_input)
        
        def is_subset(word_char_counts_json: str) -> bool:
            word_counts = json.loads(word_char_counts_json)
            return all(input_counter[char] >= count for char, count in word_counts.items())

        mask = self._df["char_counts"].apply(is_subset)
        results_df = self._df[mask]
        
        if results_df.empty:
            return {"found_words_count": 0, "input_letters": input_letters, "grouped_results": {}}
        
        sorted_df = results_df.sort_values(by=["length", "word_normalized"])
        
        # Fix: Convert integer keys to strings to match the Pydantic model
        grouped = {str(k): v for k, v in sorted_df.groupby("length")["word"].apply(list).to_dict().items()}
        
        return {
            "found_words_count": len(sorted_df),
            "input_letters": input_letters,
            "grouped_results": grouped,
        }

from app.core.config import settings
solver_service = SolverService(data_file_path=settings.DATA_FILE_PATH)