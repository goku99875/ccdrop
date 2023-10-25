import asyncio
import random
import requests
from faker import Faker
from telegram import Bot

def generate_random_address():
    try:
        url = "https://randomuser.me/api/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                user = data["results"][0]
                address = user["location"]
                street = address["street"]
                city = address["city"]
                state = address["state"]
                postcode = address["postcode"]
                country = address["country"]
                return {
                    "Street": f"{street['number']} {street['name']}",
                    "City": city,
                    "State": state,
                    "Postal Code": postcode,
                    "Country": country,
                }
        else:
            return "Unable to fetch data from the API"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def generate_bin():
    bin_number = random.randint(435546, 544544)
    bin_number_str = str(bin_number)
    credit_card_number = f"{bin_number_str}{''.join(random.choice('0123456789') for _ in range(10))}"
    return bin_number_str, credit_card_number

def get_bin_info(bin_number):
    url = f"https://lookup.binlist.net/{bin_number}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bin_info = response.json()
            if bin_info:
                fake = Faker()
                address_info = generate_random_address()
                city = address_info["City"]
                state = address_info["State"]
                message = f"*+++++++++++++++[-] Card Information [-]+++++++++++++++*\n\n"
                message += f"[+] Cardholder Name: {fake.name()}\n"
                message += f"[+] Street: {address_info['Street']}\n"
                message += f"[+] City/Town: {city}\n"
                message += f"[+] State/Province/Region: {state}\n"
                message += f"[+] Zip/Postal Code: {address_info['Postal Code']}\n"
                message += f"[+] Phone Number: {fake.phone_number()}\n"
                message += f"+----------------------------------------+\n"
                message += f"[+] BIN Information [+]\n"
                message += f"[+] BIN: {bin_number}\n"
                message += f"[+] Card Type: {bin_info.get('type', 'N/A')}\n"
                message += f"[+] Brand: {bin_info.get('brand', 'N/A')}\n"
                message += f"[+] Bank Name: {bin_info.get('bank', {}).get('name', 'N/A')}\n"
                message += f"[+] Credit Card Number: {bin_number + ''.join(random.choice('0123456789') for _ in range(10))}\n"
                message += f"[+] Expiration Date: {fake.credit_card_expire()}\n"
                message += f"[+] CVV: {random.randint(100, 999)}\n"
                message += f"+----------------------------------------+\n"
                message += f"[+] Additional Information [+]\n"
                message += f"[+] City/Town: {city}\n"
                message += f"[+] State/Province/Region: {state}\n"
                message += f"[+] Birthdate: {fake.date_of_birth(minimum_age=18, maximum_age=90)}\n"
                message += f"[+] Password: {fake.password(length=10)}\n"
                message += f"[+] Username: {fake.user_name()}\n"
                message += f"[+] IP Address: {fake.ipv4()}\n"
                message += f"[+] MAC Address: {fake.mac_address()}\n"
                message += f"[+] User Agent: {fake.user_agent()}\n"
                message += f"+--Fullz By @Adrain27----+\n"
                return message
            else:
                return "Invalid BIN Input!!"
        else:
            return "Unable to retrieve BIN information"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

async def send_message_to_telegram(message, token, chat_id):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)

async def main():
    bot_token = "6541468487:AAFCJf2YY0sS7htgjo-35dRqw8bGEgrwQ24"
    channel_username = "@opmogod"  # e.g., "@binstesthere"

    # Display custom logo or text when the script is run
    print("*+++++++++++++++ Welcome to the BIN Sender Script! +++++++++++++++*")

    while True:
        bin_number, credit_card_number = generate_bin()
        bin_info = get_bin_info(bin_number)

        # Show that the bin is sent successfully
        print(f"BIN {bin_number} sent successfully!")

        await send_message_to_telegram(bin_info, bot_token, channel_username)
        await asyncio.sleep(10)  # Wait for 60 seconds before sending the next message

if __name__ == "__main__":
    asyncio.run(main())
