from src.config.config import ConfigGPT, RetrievalConfig
from src.config.prompts import (
    ConversationPrompts,
    RetrievalPrompts,
    GenerativePrompts,
)
from openai import OpenAI, AsyncOpenAI
from src.database.user_data import UserData
import json


class GPT:
    """
    ## GPT
    GPT es usado para realizar servicios a la api de gpt openAI.
    #### inputs:
    - `model`: modelo de gpt que se utilizara
    """

    def __init__(
        self,
        user,
        model=ConfigGPT.DEFAULT_MODEL_NAME,
    ):
        self.client = OpenAI(api_key=ConfigGPT.OPENAI_API_KEY)
        self.asyncclient = AsyncOpenAI(api_key=ConfigGPT.OPENAI_API_KEY)
        if user is not None:
            self.user_data = UserData(user)
        self.model = model
        self.current_price = 0

    def completion(self, history, system_message, json_format=False, temperature=0.4):
        messages = [item for item in history]
        messages.insert(0, {"role": "system", "content": system_message})

        completion = (
            self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=temperature
            )
            if not json_format
            else self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"},
            )
        )

        self.get_price(completion.usage)
        message = completion.choices[0].message.content

        return json.loads(message) if json_format else message

    async def async_completion(
        self, history, system_message, json_format=False, temperature=0.4
    ):
        messages = [item for item in history]
        messages.insert(0, {"role": "system", "content": system_message})

        completion = (
            await self.asyncclient.chat.completions.create(
                model=self.model, messages=messages, temperature=temperature
            )
            if not json_format
            else await self.asyncclient.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"},
            )
        )

        self.get_price(completion.usage)
        message = completion.choices[0].message.content

        # return message
        return json.loads(message) if json_format else message

    def reload_price(self):
        self.current_price = 0

    def get_price(self, usage):
        """
        ## `def` get_price
        recibe el uso de la api y calcula el precio del uso del llamado actua a la api, usando los valores de precio dado por la documentacion oficial de openAI. Ademas aumenta el precio actual usado por la instacia de `class GPT`

        ### inputs:
            - `usage`: uso de la api retornado en el completion respuesta del llamado a la api de gpt
        ### outputs:
            - `price`: precio final del llamado a la api.
        """

        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens

        input_price = ConfigGPT.MODEL_PRICE[self.model]["input"]
        output_price = ConfigGPT.MODEL_PRICE[self.model]["output"]
        price = input_tokens * input_price + output_tokens * output_price

        self.current_price += price
        return price


class GPTChat(GPT):
    def __init__(self, user, model=ConfigGPT.DEFAULT_MODEL_NAME):
        super().__init__(user, model)

    def select_fields_from_query(self, history):
        system_message = ConversationPrompts.select_fields_from_query(
            self.user_data.get_fields()
        )
        return self.completion(history, system_message, True)["fields"]

    def identifique_query(self, history):
        system_message = ConversationPrompts.identifique_query()
        return self.completion(history, system_message, True)

    def conversation(self, history, fields, projects=False, temperature=0.2):
        info = self.user_data.get_info_from_fields(fields)
        if projects:
            info["projects"] = projects
        else:
            info.pop("projects", None)

        system_message = ConversationPrompts.basic_info(info, projects)
        return self.completion(
            history, system_message, json_format=projects, temperature=temperature
        )


class GPTRetrieval(GPT):
    def __init__(self, model=ConfigGPT.DEFAULT_MODEL_NAME):
        super().__init__(user=None, model=model)

    def end_irs(self, projects, history):
        if not len(projects):
            return []
        project_keys = list(projects[0].keys())
        keys = self.get_keys_from_projetckeys(project_keys)["keys"]

        system_message = RetrievalPrompts.irs_prompt(projects, keys)
        return self.completion(history, system_message, True)

    def get_keys_from_projetckeys(self, project_keys):
        system_message = RetrievalPrompts.get_keys()
        history = [{"role": "user", "content": str(project_keys)}]
        return self.completion(history, system_message, True)


class GPTGeneration(GPT):
    def __init__(self, model=ConfigGPT.DEFAULT_MODEL_NAME):
        super().__init__(info="", model=model)

    async def decode_work(self, work, base_fields):
        system_message = GenerativePrompts.work_info(base_fields)
        history = [{"role": "user", "content": work}]
        return await self.async_completion(
            history=history, system_message=system_message, json_format=True
        )

    async def decode_md(self, md):
        system_message = GenerativePrompts.md_info()
        history = [{"role": "user", "content": md}]
        return await self.async_completion(
            history=history, system_message=system_message, json_format=True
        )
