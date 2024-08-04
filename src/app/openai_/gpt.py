from src.config.config import ConfigGPT
from src.config.prompts import basic_info
from openai import OpenAI, AsyncOpenAI
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
        info,
        model=ConfigGPT.DEFAULT_MODEL_NAME,
    ):
        self.client = OpenAI(api_key=ConfigGPT.OPENAI_API_KEY)
        self.asyncclient = AsyncOpenAI(api_key=ConfigGPT.OPENAI_API_KEY)
        self.info = info
        self.model = model
        self.current_price = 0

    def identifique_query(self, history):
        pass

    def conversation(self, history):
        system_message = basic_info(self.info)
        messages = [item for item in history]
        messages.insert(0, {"role": "system", "content": system_message})

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=0.4,
            messages=messages,
        )
        self.get_price(completion.usage)
        message = completion.choices[0].message.content
        return message

    def reload_price(self):
        """
        ## `def` reload_price
        Resetea el valor de precio usado por el servicio, este es el precio total que se ha usado en una consulta dada
        """
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
