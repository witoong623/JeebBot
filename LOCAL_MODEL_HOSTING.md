# Hosting local LLM model
This is document about hosting LLM server that offer OpenAI compatible API and config the app to use it.

## App configuration
Edit `config.yaml` as follow
- Change `openai_api_key` to `no-key` (actually, it can be any string)
- Change `openai_compatible_base_url` to `http://llama-cpp-server:8000`.

## llama.cpp
### Building llama-server docker image
Normally, you can find server image from [official document on running llama.cpp in docker](https://github.com/ggerganov/llama.cpp/blob/master/docs/docker.md), specifically image with server tag.  
However, if you want to you CUDA, and you have different CUDA version from their pre-built image on your server, you need to build local image yourself.

Clone the repository, checkout the release tag that you want, then run the following command to build the server with, for example with CUDA 12.5.0.
```
docker build -t local/llama.cpp:server-cuda -f .devops/llama-server-cuda.Dockerfile --build-arg CUDA_VERSION=12.5.0 .
```

## Select model and config to use the model
Edit docker/.env to change `GGUF_MODEL_NAME` variable to the name of the model in GGUF format.  
You must download GGUF model, and put it in `local-llm-model` directory.

This project focus on Thai language, so I selected one of the thai language fine-tuned model.

## Running llama-server docker container
To run llama-server container with the app container, run the following command from root directory of the project:
```
docker compose -f docker/docker-compose.yaml -f docker/docker-compose.llama-cpp.yaml up -d
```

You can read about options to control the server in [llama-cli](https://github.com/ggerganov/llama.cpp/tree/master/examples/main) and [llama-server](https://github.com/ggerganov/llama.cpp/tree/master/examples/server) documents.  
Then edit docker compose file at `docker/docker-compose.llama-cpp.yaml`, and change `command` to adjust the options.

## Model Quality Comparison
This is description of the feeling after trying the model in Thai language. It isn't scientifically compare!.
Normally, I use GPT-4o-mini which feel very natural to have conversation and follow instruction correctly.  
Though, it does have ability to answer in very useful manner, which not many people do it in dating conversation.

| Model                                     | Quality                                                                                              |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 1. llama-3-typhoon-v1.5-8b-instruct.Q6_K  | Conversation feel very unnatural. It generate unrelated output when asking to summarize conversation |
| 2. openthaigpt1.5-7b-instruct.Q6_K        | Conversation feel a little bit more natural than 1. But it confuse itself with user                  |
| 3. llama-3-typhoon-v1.5x-8b-instruct-Q6_K | Conversation feel a lot more natural than 1. Doesn't always follow system message                    |
| 4. **openthaigpt1.5-14b-instruct.Q6_K**   | Far better in every aspect than above models for obvious reason!                                     |

Generally speaking, a bigger model with enough bpw quantize should be better.
