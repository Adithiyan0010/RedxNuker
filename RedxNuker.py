import requests
import json
import os
from colorama import Fore, Style

def print_banner():
    banner = """

 ██████╗ ███████╗██████╗ ██╗  ██╗██╗    ██╗ █████╗ ██████╗ ███████╗
██╔══██╗██╔════╝██╔══██╗╚██╗██╔╝██║    ██║██╔══██╗██╔══██╗██╔════╝
██████╔╝█████╗  ██║  ██║ ╚███╔╝ ██║ █╗ ██║███████║██████╔╝█████╗  
██╔══██╗██╔══╝  ██║  ██║ ██╔██╗ ██║███╗██║██╔══██║██╔══██╗██╔══╝  
██║  ██║███████╗██████╔╝██╔╝ ██╗╚███╔███╔╝██║  ██║██║  ██║███████╗
╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
                                                                                
    """
    print(Fore.RED + banner + Style.RESET_ALL)

def print_menu():
    menu = """
    ╔══════════════════════════════════════════════════════════════╗
    ║ 1. Webhook Sender          | Send messages via webhook       ║
    ║ 2. Multi Webhook Spammer   | Spam multiple webhooks          ║
    ║ 3. Webhook Deleter         | Delete a single webhook         ║
    ║ 4. Multi Webhook Deleter   | Delete multiple webhooks        ║
    ║ 5. Webhook Info            | Get webhook details             ║
    ║ 6. God Mode                | Advanced server control         ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(Fore.CYAN + menu + Style.RESET_ALL)

async def send_webhook_async(session, url, data, headers):
    try:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 429:  # Rate limit hit
                retry_after = float((await response.json()).get('retry_after', 1))
                await asyncio.sleep(retry_after)
                return False
            await response.read()
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def send_webhook():
    import asyncio
    import aiohttp
    
    url = input("Enter webhook URL: ")
    count = int(input("How many times to send: "))
    message = input("Message to send: ")
    name = input("Webhook name: ")
    
    headers = {'Content-Type': 'application/json'}
    data = {"username": name, "content": message}
    
    async def main():
        sent_count = 0
        async with aiohttp.ClientSession() as session:
            while sent_count < count:
                success = await send_webhook_async(session, url, data, headers)
                if success:
                    sent_count += 1
                    print(f"Progress: {sent_count}/{count}", end="\r")
                await asyncio.sleep(0.5)  # Add delay between requests
        print(f"\nSent {sent_count} messages successfully!")
    
    asyncio.run(main())

def multi_webhook_spammer():
    import asyncio
    import aiohttp
    
    path = input("Enter path to txt file: ")
    count = int(input("How many times to send: "))
    message = input("Message to send: ")
    name = input("Webhook name: ")
    
    headers = {'Content-Type': 'application/json'}
    data = {"username": name, "content": message}
    
    async def main():
        async with aiohttp.ClientSession() as session:
            with open(path, 'r') as file:
                webhooks = [webhook.strip() for webhook in file.readlines()]
                tasks = []
                for webhook in webhooks:
                    tasks.extend([send_webhook_async(session, webhook, data, headers) for _ in range(count)])
                await asyncio.gather(*tasks)
                print(f"Sent {count} messages to {len(webhooks)} webhooks successfully!")
    
    asyncio.run(main())

def delete_webhook():
    url = input("Enter webhook URL to delete: ")
    requests.delete(url)

def multi_webhook_deleter():
    path = input("Enter path to txt file: ")
    with open(path, 'r') as file:
        webhooks = file.readlines()
        for webhook in webhooks:
            webhook = webhook.strip()
            requests.delete(webhook)

def webhook_info():
    url = input("Enter webhook URL: ")
    response = requests.get(url)
    print(response.json())

def god_mode():
    import discord
    from discord.ext import commands

    token = input("Enter bot token: ")
    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print("\nBot is ready!")
        print("\nAvailable servers:")
        for i, guild in enumerate(bot.guilds, 1):
            print(f"{i}. {guild.name}")
        
        server_num = int(input("\nSelect server number: ")) - 1
        guild = bot.guilds[server_num]
        
        channel_name = input("Enter channel name to create: ")
        num_channels = int(input("Enter number of channels to create: "))
        message = input("Enter message to send: ")
        msg_count = int(input("Enter number of messages to send: "))
        
        print("\nCreating channels and webhooks...")
        webhooks = []
        
        for i in range(num_channels):
            channel = await guild.create_text_channel(f"{channel_name}-{i+1}")
            webhook = await channel.create_webhook(name="SnowWare")
            webhooks.append(webhook)
            print(f"Created channel and webhook: {channel.name}")
        
        print("\nSending messages...")
        for webhook in webhooks:
            for _ in range(msg_count):
                await webhook.send(content=message)
        
        print("Operation completed!")
        await bot.close()

    bot.run(token)

def main():
    print_banner()
    print_menu()
    choice = input("Select an option: ")
    
    if choice == "1":
        send_webhook()
    elif choice == "2":
        multi_webhook_spammer()
    elif choice == "3":
        delete_webhook()
    elif choice == "4":
        multi_webhook_deleter()
    elif choice == "5":
        webhook_info()
    elif choice == "6":
        god_mode()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
