# 👾 Neum AI Chatbot

Example chatbot that connects to a Neum AI data pipeline and allows you to chat with the data available. 

## Overview of the App

Neum AI helps developers automatically connect and synchronize their data into vector databases for retrieval augmented generation. The platform allows you to choose a data source (ex. S3, Blob, Notion and more) and sync the data within that source as vectors into a vector database. Once in the vector database, it allows you to query the data and get the most relevant chunks out. In this example app, we connect those queried chunks into a chatbot interface so you can see the end-to-end experience. The chatbot using a basic system prompt that can be modified.

## Demo App

[Live App](https://neumai-chatbot.streamlit.app/)

To run the app you will need a Neum AI API Key, a live data pipeline on the platform and an OpenAI API Key.

### Get started with Neum AI

Before using this app, you will need to create a [Neum AI account](dashboard.neum.ai) and set up your [first pipeline]([url](https://docs.neum.ai/docs/build-in-the-ui)). 

### Get an OpenAI API key

You can get your own OpenAI API key by following the following instructions:

1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.
