from transformers import AutoModelForSeq2SeqLM
from transformers import AutoTokenizer



model_checkpoint = "ml/models/best"
# model_checkpoint = "d0rj/rut5-base-summ"
prefix = "summarize: "
# prefix = ""
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)
model.eval()


def summarize(text):

    input_ids = tokenizer(prefix + text, return_tensors="pt").input_ids
    max_new_tokens = 60

    outputs = model.generate(input_ids=input_ids, max_new_tokens=max_new_tokens)

    return tokenizer.decode(outputs[0], skip_special_tokens=True, temperature=0)

