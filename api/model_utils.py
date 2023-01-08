from typing import List, Dict, Tuple
from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd


class T5GenerationModel:
    inspiration_prefix = 'Сгенерировать вдохновение: '
    mark_prefix = 'Сгенерировать оценку: '
    punch_prefix = 'Сгенерировать шутку: '

    def __init__(self):
        self.model = None
        self.tokenizer = None

    def load_model_from_file(self, model_dir):
        self.model = T5ForConditionalGeneration.from_pretrained(model_dir)
        self.tokenizer = T5Tokenizer.from_pretrained(model_dir)

    def load_model_from_hub(self,
                            model_name,
                            model_type,
                            force_download=True,
                            use_auth_token=False,
                            revision=None):

        self.tokenizer = T5Tokenizer.from_pretrained(model_name,
                                                     from_flax=model_type == "flax",
                                                     force_download=force_download,
                                                     use_auth_token=use_auth_token,
                                                     revision=revision)

        self.model = T5ForConditionalGeneration.from_pretrained(model_name,
                                                                from_flax=model_type == "flax",
                                                                force_download=force_download,
                                                                use_auth_token=use_auth_token,
                                                                revision=revision)

    def generate_inspirations(self, setup: str,
                              num_return_sequences: int = 5, temperature: float = 1) -> List[str]:
        # Generate inspirations
        setup_ids = self.tokenizer(self.inspiration_prefix + setup, return_tensors="pt").input_ids
        predict_inspiration_ids = self.model.generate(setup_ids,
                                                      top_k=20,
                                                      do_sample=True,
                                                      max_length=50,
                                                      no_repeat_ngram_size=2,
                                                      temperature=temperature,
                                                      num_return_sequences=num_return_sequences).tolist()
        predict_inspirations = [self.tokenizer.decode(p, skip_special_tokens=True) for p in predict_inspiration_ids]
        return predict_inspirations

    def generate_punches(self, setup: str, inspiration: str,
                         num_return_sequences: int = 5, temperature: float = 1) -> List[str]:

        input_ids = self.tokenizer(self.punch_prefix + inspiration + '|' + setup, return_tensors="pt").input_ids
        predict_punches_ids = self.model.generate(input_ids,
                                                  do_sample=True,
                                                  top_k=20,
                                                  max_length=50,
                                                  no_repeat_ngram_size=2,
                                                  temperature=temperature,
                                                  num_return_sequences=num_return_sequences).tolist()
        predict_punches = [self.tokenizer.decode(p, skip_special_tokens=True) for p in predict_punches_ids]
        return predict_punches

    def generate_mark(self, joke: str) -> str:
        input_ids = self.tokenizer(self.mark_prefix + joke, return_tensors="pt").input_ids
        predict_mark_ids = self.model.generate(input_ids).tolist()
        predict_mark = self.tokenizer.decode(predict_mark_ids[0], skip_special_tokens=True)
        return predict_mark

    def inference(self, setup: str, inspirations: List = None,
                  num_return_sequences: int = 5, temperature: float = 1) -> List[Tuple[str, str, str, str]]:
        result_list = list()
        if not inspirations:
            # Generate inspirations
            inspirations = self.generate_inspirations(setup,
                                                      num_return_sequences=num_return_sequences,
                                                      temperature=temperature, )
        for inspiration in inspirations:
            # Generate punches
            punches = self.generate_punches(setup,
                                            inspiration,
                                            num_return_sequences=num_return_sequences,
                                            temperature=temperature)
            for punch in punches:
                joke = setup + punch
                mark = self.generate_mark(joke)
                result_list.append((setup, inspiration, punch, mark))

        sorted_result_list = sorted(result_list, key=lambda tup: tup[3], reverse=True)[:num_return_sequences]
        return sorted_result_list
