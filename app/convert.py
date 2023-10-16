import aiohttp
import asyncio


async def convert_currency_async(amount, Cur_Name):
    url = f"https://api.nbrb.by/exrates/rates/{Cur_Name}?parammode=2"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            rate = data["Cur_OfficialRate"]
            converted_amount = rate * amount
            return converted_amount


async def get_float_input_async(prompt):
    while True:
        try:
            value = float(await asyncio.get_event_loop().run_in_executor(None, input, prompt))
            return value
        except ValueError:
            return '-1'
