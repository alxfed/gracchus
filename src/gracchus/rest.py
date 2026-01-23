# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
import requests
# from .adapters import prepared_grch_messages, format_grch_output

# load_env()

api_key             = environ.get("XAI_API_KEY")
api_base            = environ.get("XAI_API_BASE", "https://api.x.ai/v1")
default_model       = environ.get("XAI_DEFAULT_MODEL", "grok-3-mini")
response_model      = environ.get("XAI_RESPONSE_MODEL",'grok-3-mini')

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key,
    # "Organization": organization
}


def response(incoming, **kwargs):
    """A completions endpoint call through requests.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            frequency_penalty = -2.0 to 2.0
            presence_penalty = -2.0 to 2.0
            max_tokens      = number of tokens
    """
    reasoning = {
        "effort": "high",
        "summary": "detailed"
    }
    text = {
        "format": {
            "type": "text"
        }
    }
    json_data = {
        "model":                kwargs.get("model", response_model),
        "input":                kwargs.get("input", incoming),
        "instructions":         kwargs.get("instructions", None),
        "max_output_tokens":    kwargs.get("max_tokens", 10000),
        "previous_response_id": kwargs.get("previous_response_id", None),
        "reasoning":            kwargs.get("reasoning", reasoning),
        "temperature":          kwargs.get("temperature", 1.0),
        "top_p":                kwargs.get("top_p", None),
        "text":                 kwargs.get("text", text)
    }
    try:
        content = ''
        reasoning_content = ''
        id = ''
        answer = requests.post(
            f"{api_base}/responses",
            headers=headers,
            json=json_data,
        )
        if answer.status_code == requests.codes.ok:
            the = answer.json()
            id = the["id"]
            output = the["output"]
            summary = output[0]['summary']
            for piece in summary:
                reasoning_content += piece['text']
            reply = output[1]['content']
            for chunk in reply:
                content += chunk['text']
        else:
            print(f"Request status code: {answer.status_code}")

        return content, reasoning_content, id

    except Exception as e:
        print("Unable to generate Completions response")
        print(f"Exception: {e}")
        return '', '', ''


def models():
    """Returns a list of available models."""
    models_list = []
    try:
        response = requests.get(f"{api_base}/models",
                                headers=headers)
        if response.status_code == requests.codes.ok:
            for model in response.json()['data']:
                models_list.append(model['id'])
            return models_list
        else:
            print(f"Request status code: {response.status_code}")
            return []
    except Exception as e:
        print("Unable to generate Models response")
        print(f"Exception: {e}")
        return models_list


if __name__ == '__main__':
    # mod = models()
    respa = response("What model are you?")
    print('ok')