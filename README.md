# Summarcha

> A tool for automatic chat summarization based on [T5](https://arxiv.org/abs/1910.10683) model.

## Table of Contents

- [Summarcha](#summarcha)
  - [Table of Contents](#table-of-contents)
  - [Project topic](#project-topic)
  - [Solution building](#solution-building)
    - [Solution 1 - base Bart model with prefix tuning](#solution-1---base-bart-model-with-prefix-tuning)
    - [Solution 2 - Bart-Summarize model with Telegram Translation API](#solution-2---bart-summarize-model-with-telegram-translation-api)
    - [Solution 3 - ru-T5 model finetuned on the dataset](#solution-3---ru-t5-model-finetuned-on-the-dataset)
  - [Final solution and results](#final-solution-and-results)
  - [Project timeline](#project-timeline)
  - [Developers](#developers)
    - [Team](#team)
    - [Contributions](#contributions)
  - [References](#references)

## Project topic

The project is dedicated to the development of a tool for automatic chat summarization. It is based on the [T5](https://arxiv.org/abs/1910.10683) model which was finetuned on the <!-- TODO -->

## Solution building

### Solution 1 - base Bart model with prefix tuning

<!-- TODO -->

### Solution 2 - Bart-Summarize model with Telegram Translation API

<!-- TODO -->

### Solution 3 - ru-T5 model finetuned on the dataset

<!-- TODO -->

## Final solution and results

## Project timeline

## Developers

### Team

| Full name     | Innopolis Email                 | Github                                                     | Responsibilities                 |
| ------------- | ------------------------------- | ---------------------------------------------------------- | -------------------------------- |
| Andrei Markov | <a.markov@innopolis.university> | [@markovav-official](https://github.com/markovav-official) | Frontend, Dataset creation       |
| Grigorii Fil  | <g.fil@innopolis.university>    | [@Fil-126](https://github.com/Fil-126)                     | Model finetuning, EDA            |
| Timofey Sedov | <t.sedov@innopolis.university>  | [@moflotas](https://github.com/moflotas)                   | Backend, Research, Model testing |

### Contributions

Andrei was mainly responsible for the frontend part of the project. He created modified Telegram web client which allows to send messages to the backend and receive the summary. He also created a dataset for the model finetuning.

Grigorii was responsible for the model finetuning. He performed EDA on the dataset and finetuned the model on the dataset.

Timofey was responsible for the backend part of the project. He created a Telegram bot which receives messages from the frontend and sends them to the model. He also performed research on the model and tested it.

## References

- [T5](https://arxiv.org/abs/1910.10683)
- [Dataset](#TODO)
