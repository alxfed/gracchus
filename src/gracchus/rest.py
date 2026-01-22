# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import List, Dict
from os import environ
import requests
# from .adapters import prepared_grch_messages, format_grch_output


api_key             = environ.get("XAI_API_KEY")
api_base            = environ.get("XAI_API_BASE", "https://api.x.ai/v1")
default_model       = environ.get("XAI_DEFAULT_MODEL", "grok-3-mini")
response_model      = environ.get("XAI_RESPONSE_MODEL",'grok-3-mini')

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key,
    # "Organization": organization
}


def response(input, **kwargs) -> List:
    """A completions endpoint call through requests.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            n               = 1 to ...
            best_of         = 4
            frequency_penalty = -2.0 to 2.0
            presence_penalty = -2.0 to 2.0
            max_tokens      = number of tokens
            logprobs        = number up to 5
            stop            = ["stop"]  array of up to 4 sequences
            logit_bias      = map token: bias -1.0 to 1.0 (restrictive -100 to 100)
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
        "input":                kwargs.get("input", input),
        "instructions":         kwargs.get("instructions", None),
        "max_output_tokens":    kwargs.get("max_tokens", 5),
        "previous_response_id": kwargs.get("previous_response_id", None),
        "reasoning":            kwargs.get("reasoning", reasoning),
        "temperature":      kwargs.get("temperature", 1.0),
        "top_p":            kwargs.get("top_p", None),
        "text":             kwargs.get("text", text)
    }
    responses = []
    try:
        response = requests.post(
            f"{api_base}/completions",
            headers=headers,
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            for choice in response.json()['choices']:
                responses.append(choice)
        else:
            print(f"Request status code: {response.status_code}")
        return responses
    except Exception as e:
        print("Unable to generate Completions response")
        print(f"Exception: {e}")
        return responses


def models() -> List:
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
    mod = models()

    print('ok')