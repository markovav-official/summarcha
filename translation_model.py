from typing import List

from transformers import MBart50TokenizerFast, MBartForConditionalGeneration

model = MBartForConditionalGeneration.from_pretrained(
    "facebook/mbart-large-50-many-to-many-mmt")


def query(text: str, src_lang: str, target_lang: str):
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    tokenizer.src_lang = src_lang
    encoded = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=1024
    )
    generated_tokens = model.generate(
        **encoded,
        forced_bos_token_id=tokenizer.lang_code_to_id[target_lang],
        use_cache=True
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]


if __name__ == "__main__":
    print(query("Hello world", "en_XX", "ru_RU"))
    print(query("Привет, мир", "ru_RU", "en_XX"))
