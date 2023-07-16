import hashlib
import time
from functools import wraps
from typing import Union

from fastapi import status
from fastapi.responses import JSONResponse

from exceptions import BannedPromptError
from lib.prompt import BANNED_PROMPT
import random

PROMPT_PREFIX = "<#"
PROMPT_SUFFIX = "#>"


def check_banned(prompt: str):
    words = set(w.lower() for w in prompt.split())
    if len(words & BANNED_PROMPT) != 0:
        raise BannedPromptError(f"banned prompt: {prompt}")


def unique_id():
    """生成唯一的 10 位数字，作为任务 ID"""
    return int(hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest(), 16) % 10**10


def prompt_handler(uid: str, gender: str, age: float, picurl: Union[str, None] = None):
    """
    拼接 Prompt 形如: <#1234567890#>a cute cat
    """
    gender = "boy" if gender == "male" else "girl"
    age = "newborn" if age < 1 else str(age)+" year old"
    tmp1 = f"a {age} chinese baby {gender} sitting on grass with cute shoes and cute clothes, with sweet smile, precise and sharp, natural surroundings, elegant and simple style --q 1 --s 100 --v 5.2 --style raw --no dark  background"
    tmp2 = f"a {age} chinese baby {gender} sitting on beach with lovely clothes, with sweet smile, precise and sharp, sunny day and blue sky, elegant and simple style --q 1 --s 100 --v 5.2 --style raw --no dark  background"
    tmp3 = f"a {age} chinese baby {gender} dressed in white wearing a knit hat, in the style of 32k uhd, russell dongjun lu, light beige and light amber, soft femininity, dark blue and light beige, shiny eyes, beige --q 1 --s 100 --v 5.2 --style raw --no black"
    tmp4 = f"a {age} chinese baby {gender} wearing a hat wearing a sweater, in the style of 32k uhd, hallyu, soft and dreamy atmosphere, matte photo, uhd image  --q 1 --s 100 --v 5.2 --style raw --no dark background"
    prompt = random.sample([tmp1, tmp2, tmp3, tmp4], 1)[0]
    if age == "newborn":
        prompt = f"a {age} chinese baby {gender} sleep in the white soft bed, covered by the blanket, laughing with the very sweet smile, studio protrait shots, in the style of 32k uhd, hallyu, soft and dreamy atmosphere, matte photo, uhd image  --q 1 --s 100 --v 5.2 --style raw --no dark background"
    #prompt = tmp4
    check_banned(prompt)

    trigger_id = uid+"_"+str(unique_id())

    if not picurl and prompt.startswith(("http://", "https://")):
        picurl, _, prompt = prompt.partition(" ")

    return trigger_id, f"{picurl+' ' if picurl else ''}{PROMPT_PREFIX}{trigger_id}{PROMPT_SUFFIX}{prompt}"


def http_response(func):
    @wraps(func)
    async def router(*args, **kwargs):
        trigger_id, resp = await func(*args, **kwargs)
        if resp is not None:
            code, trigger_result = status.HTTP_200_OK, "success"
        else:
            code, trigger_result = status.HTTP_400_BAD_REQUEST, "fail"

        return JSONResponse(
            status_code=code,
            content={"trigger_id": trigger_id, "trigger_result": trigger_result}
        )

    return router
