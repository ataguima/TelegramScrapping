import re
import csv
import traceback
import asyncio
import random
from random import randint
from pathlib import Path
from typing import List, Dict, Union, Tuple

from telethon.client.telegramclient import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.types import InputPeerUser, Channel, UserStatusRecently
from telethon.errors.rpcerrorlist import (PeerFloodError, UserPrivacyRestrictedError,
                                          UserNotMutualContactError, UserChannelsTooMuchError,
                                          ChannelPrivateError, UserIdInvalidError)
from telethon.helpers import TotalList

from myconfig import *

from colorama import init, Fore

init(autoreset=True)
rs = Fore.RESET
lg = Fore.LIGHTGREEN_EX
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [cy, w, r]


def logo() -> None:
    logo_str: List[str] = [
        "`` ``  `` ``  `  `` ``  `` `..-::////::-..` ``  `` ``  `  ``  `  `` ``",
        "  `  `` ``  `` ``  `` ``.:+oosossssssssoooo+:.`` ``  `` ``  `  ``  `",
        "`` ``  `` ``  `  ````./oossssssssssssssssssssoo:.` `   `  ``  `  `  ``",
        "``  `  `   `  `` ``.+osssssssssssssssssssssssssso+.``  `  `   `  `` ` ",
        "  `  ``  `  `` ```/osssssssssssssssssssssssssssssso/``` ``  `  ``  `  ",
        "`` ``  `  ``  ``.+sssssssssssssssssssssssssssssssssso.``  `` ``  `` ``",
        "  `  ``  `  `` .ossssssssssssssssssssssssso++ossssssso. ``  `  ``  `  ",
        "``  `  `  `` ``+ssssssssssssssssssssso+/:-```/sssssssso`  `` ``  `  ``",
        "  `  `   `  ``:ssssssssssssssssoo+/:.````   `osssssssss:``  `  ``  `  ",
        "  `  `   ` ```osssssssssssoo+/-.``  ``.``   :sssssssssso``` `  `  ``  ",
        "`` ``  `` `` `ossssssso+/-.`     ``..`      +sssssssssss` `` ``  `  ``",
        "  `  `` ``  ``ossssssso-.``   ``...`       .ssssssssssso``  `` ``  `  ",
        "``  `  `` `` `osssssssssoo+/:....`         /ssssssssssso` ``  `  `  ``",
        " `  ``  `  ``:ssssssssssssso:.-.`        `ossssssssssss:``  `  ``  `  ",
        "``  `  ``  `  `+sssssssssssss+---:/-`     :ssssssssssso`  `   `  `  ` ",
        " ``    `      `.osssssssssssss/:+osso/.` `osssssssssso.    `        ` ",
        "  `  ``  `  `` `.ossssssssssssoosssssso+/+ssssssssss+.`  `  `  ``  `  ",
        "`` ``  `  ``  ` ``/osssssssssssssssssssssssssssssso/`  `  ``  `  `` ``",
        "  `  ``  `  `` `` `.+osssssssssssssssssssssssssso+.  `` ``  `  ``  `  ",
        "``  `  `  ``  `  `` `./oossssssssssssssssssssoo/.` ``  `  ``  `  `` ``",
        "  `  `` ``  `   `  `` ``.:+oooossssssssooso+:.`` ``  `` ``  `  ``  `  ",
        "```  ``         `  `  `` ````--::////::--```````     ````` `          "
    ]
    total_lines = len(logo_str)
    for idx, line in enumerate(logo_str):
        if idx < total_lines / 3:
            color = colors[0]
        elif idx < (total_lines / 3) * 2:
            color = colors[1]
        else:
            color = colors[2]
        print(f'{color}{line}{rs}')
    print(f'{r}Telegram Scraper{rs}\n')
    print(f'{lg}Version: {rs}1.0 | {lg}Author: {rs}Pierre{rs}\n')


def define_title_file(target_group_title: str, own_group_or_blacklist: bool, username: str) -> str:
    title_file = target_group_title.replace(" ", "_").lower()
    title_file = "".join(re.findall("[a-zA-Z_]", title_file))
    if title_file.endswith("_"):
        title_file = title_file[:-1]
    if not own_group_or_blacklist:
        title_file = f"{title_file}_{username}"
    return f"{title_file}.csv"


async def join_group(client: TelegramClient) -> Tuple[Channel, Channel]:
    try:
        your_group = await client.get_entity(link_channel_to_add_members)
        try:
            await client(JoinChannelRequest(your_group))
            print(f"\n\nGroup {your_group.title} joined")
        except Exception:
            print(f"\n\nGroup {your_group.title} - Already a member or cannot join")
    except ChannelPrivateError:
        print(f"\n\nGroup (bot) can't be joined with this account due to ChannelPrivateError")

    try:
        group_scrape = await client.get_entity(link_channel_you_want_to_scrape)
        try:
            await client(JoinChannelRequest(group_scrape))
            print(f"\n\nGroup {group_scrape.title} joined")
        except Exception:
            print(f"\n\nGroup {group_scrape.title} - Already a member or cannot join")
    except ChannelPrivateError:
        print(f"\n\nGroup {group_scrape.title} can't be joined with this account due to ChannelPrivateError")

    return your_group, group_scrape


async def scrapping_members_of_a_group(own_group: bool, target_group: Channel, client: TelegramClient,
                                        username: str) -> Tuple[List[Dict[str, Union[str, int]]], str]:
    title_file = define_title_file(target_group.title, own_group, username)
    my_file = Path(path_csv) / title_file
    if not my_file.is_file():
        all_participants = await scrap_members_on_a_group(target_group, client)
        title_file = await write_csv_members(all_participants, target_group, own_group, username)
        users_on_group = await read_csv_members(title_file, only_id=own_group)
    else:
        users_on_group = await read_csv_members(title_file, only_id=own_group)
    return users_on_group, title_file


async def scrap_members_on_a_group(target_group: Channel, client: TelegramClient) -> TotalList:
    print('Loading members...')
    all_participants = await client.get_participants(target_group, aggressive=True)
    return all_participants


async def write_csv_members(all_participants: TotalList, target_group: Channel,
                            own_group: bool, username: str) -> str:
    title_file = define_title_file(target_group.title, own_group, username)
    file_path = Path(path_csv) / title_file

    with open(file_path, "w", encoding='UTF-8', newline="") as f:
        writer = csv.writer(f, delimiter=";", lineterminator="\n")
        writer.writerow(list_columns)
        for user in all_participants:
            if not isinstance(user.status, UserStatusRecently):
                continue
            username_val = user.username if user.username else ""
            first_name = user.first_name if user.first_name else ""
            last_name = user.last_name if user.last_name else ""
            name = f"{first_name} {last_name}".strip()
            writer.writerow([username_val, user.id, user.access_hash, name])
    print('Members scraped successfully.')
    return title_file


async def add_member_csv(user: Dict[str, Union[str, int]], title_file: str) -> None:
    file_path = Path(path_csv) / title_file
    with open(file_path, 'a+', encoding='UTF-8', newline="") as f:
        writer = csv.writer(f, delimiter=";", lineterminator="\n")
        username_val = user.get('username', "") or ""
        name = user.get('name', "") or ""
        writer.writerow([username_val, user['id'], user['access_hash'], name])
    print(f"Member {user['id']} added to the CSV")


async def write_csv_blacklist(user: Dict[str, Union[str, int]], reason_blacklist: str,
                              title_file: Union[str, bool] = False) -> None:
    if not title_file:
        title = title_blacklist_csv
        file_path = Path(path_csv) / title
    else:
        title = f"blacklist_{title_file}"
        file_path = Path(path_csv) / title

    file_exist = file_path.is_file()

    with open(file_path, 'a+', encoding='UTF-8', newline="") as f:
        writer = csv.writer(f, delimiter=";", lineterminator="\n")
        if not file_exist:
            writer.writerow(list_columns + ['reason_blacklist'])
        username_val = user.get('username', "") or ""
        name = user.get('name', "") or ""
        writer.writerow([username_val, user['id'], user['access_hash'], name, reason_blacklist])
    print(f"Member {user['id']} added to the blacklist CSV")


async def read_csv_members(input_file: str, only_id: bool) -> List[Union[Dict[str, Union[str, int]], int]]:
    users: List[Union[Dict[str, Union[str, int]], int]] = []
    file_path = Path(path_csv) / input_file
    if file_path.is_file():
        with open(file_path, encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=";", lineterminator="\n")
            next(rows, None)
            if not only_id:
                for row in rows:
                    try:
                        user = {
                            'username': row[0],
                            'id': int(row[1]),
                            'access_hash': int(row[2]),
                            'name': row[3]
                        }
                        users.append(user)
                    except IndexError:
                        print('User data missing id or access_hash')
            else:
                for row in rows:
                    try:
                        users.append(int(row[1]))
                    except IndexError:
                        print('User data missing id')
    return users


def random_choice_username(username: str) -> str:
    """Escolhe aleatoriamente um username da lista, evitando retornar o próprio."""
    available = [api['username'] for api in api_list if api['username'] != username]
    return random.choice(available) if available else username


async def function_send_message(client: TelegramClient, username: str) -> None:
    list_words = ['apple', 'banana', 'cherry', 'dates', 'etc', 'have', 'I', 'You', 'good', 'morning', 'what']
    random_number_message = randint(2, 10)
    sentence = " ".join(random.choice(list_words) for _ in range(random_number_message))
    random_username = random_choice_username(username)
    entity = await client.get_entity(random_username)
    await client.send_message(entity=entity, message=sentence)
    print("Message sent")


async def add_members_to_group(client: TelegramClient, username: str) -> None:
    print(f"\nSESSION: {username}\n")
    your_group, target_group = await join_group(client)
    input_channel = await client.get_input_entity(your_group)

    users_on_your_group, title_file_own = await scrapping_members_of_a_group(True, your_group, client, username)
    users_in_other_group, _ = await scrapping_members_of_a_group(False, target_group, client, username)

    users_blacklist = await read_csv_members(f"blacklist_{define_title_file(target_group.title, True, username)}", True)
    users_blacklist_2 = await read_csv_members(title_blacklist_csv, True)

    blacklist_ids = set(users_on_your_group + users_blacklist + users_blacklist_2)
    users_to_add = [user for user in users_in_other_group if user['id'] not in blacklist_ids]

    random.shuffle(users_to_add)

    for idx, user in enumerate(users_to_add):
        if idx >= (number_of_adds_per_session / split_by):
            break
        try:
            if not user.get('id') or not user.get('access_hash'):
                print(f"Dados inválidos para o usuário, pulando: {user}")
                continue

            user_to_add = InputPeerUser(user['id'], user['access_hash'])
            if idx == 0:
                await client(InviteToChannelRequest(input_channel, [user_to_add]))
                print(f"\nAdd: {user['id']}")
                print(f"{idx + 1}/{len(users_to_add)}")
                await add_member_csv(user, title_file_own)
                print(f"Wait {number_of_seconds_to_wait_between_every_add} sec...")
                await asyncio.sleep(number_of_seconds_to_wait_between_every_add)
            else:
                wait_time = randint(number_of_seconds_min_to_wait_between_every_add,
                                    number_of_seconds_to_wait_between_every_add)
                print(f"\nWait {wait_time} sec...")
                await asyncio.sleep(wait_time)
                await client(InviteToChannelRequest(input_channel, [user_to_add]))
                print(f"Add: {user['id']}")
                print(f"{idx + 1}/{len(users_to_add)}")
                await add_member_csv(user, title_file_own)
                if idx % number_of_adds_between_every_message == 0 and bool_send_message:
                    await function_send_message(client, username)
                else:
                    remaining_wait = number_of_seconds_to_wait_between_every_add - wait_time
                    print(f"Wait {remaining_wait} sec...")
                    await asyncio.sleep(remaining_wait)
        except UserIdInvalidError:
            print(f"Invalid user ID for user {user['id']}. Skipping this user.")
            continue
        except PeerFloodError:
            print("\nFlood Error from Telegram. Switching session...")
            break
        except UserPrivacyRestrictedError:
            print("User privacy settings restrict this action. Skipping.")
            await write_csv_blacklist(user, 'UserPrivacyRestrictedError', title_file=False)
            await asyncio.sleep(number_of_seconds_to_wait_between_every_add)
        except UserNotMutualContactError:
            print("User is not a mutual contact. Skipping.")
            await write_csv_blacklist(user, 'UserNotMutualContactError', title_file=title_file_own)
            await asyncio.sleep(number_of_seconds_to_wait_between_every_add)
        except UserChannelsTooMuchError:
            print("User is in too many channels. Skipping.")
            await write_csv_blacklist(user, 'UserChannelsTooMuchError', title_file=False)
            await asyncio.sleep(number_of_seconds_to_wait_between_every_add)
        except KeyboardInterrupt:
            print(f"{r}---- Adding Terminated ----{rs}")
            break
        except Exception:
            traceback.print_exc()
            print("Unexpected Error")
            await asyncio.sleep(number_of_seconds_to_wait_between_every_add)

    print("\n\nSwitch sessions")
