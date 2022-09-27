from telethon import events
from datetime import datetime
from context import db, bot
from decorators import last_handler_decorator
from utils import notify_users


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if not db.is_created(event.sender_id):
        return await event.reply('Ciao! Dimmi il tuo nome con "/nome __Marctiell__" per partecipare al gruppo di calcetto')
    return await event.reply(f'Ciao {db.get_user(event.sender_id)}! Resta in attesa della carica o diffondila con /carichi 😤')


@bot.on(events.NewMessage(pattern='/nome'))
async def name(event):
    chunks = event.raw_text.split(' ')
    if len(chunks) == 1:
        return await event.reply('Devi specificare un nome dopo /nome\nEsempio: /nome __Marctiell__')
    username = " ".join(chunks[1:])
    db.create_user(event.sender_id, username)
    await event.reply(f'Ciao {username}!\nChe la carica sia con te 😤')


@bot.on(events.NewMessage(pattern='/stop'))
async def stop(event):
    if not db.is_created(event.sender_id):
        return await event.reply('Non sei ancora registrato, usa il comando /start per scoprire come fare')
    db.delete_user(event.sender_id)
    await event.reply('Ora non riceverai più le notifiche sulle partite ❌')


@bot.on(events.NewMessage(pattern='/carichi'))
async def carichi(event):
    if not db.is_created(event.sender_id):
        return await event.reply('Non sei ancora registrato, usa il comando /start per scoprire come fare')
    if db.is_player(event.sender_id):
        return await event.reply('Sei già in lista per giocare, tieni a bada la carica 🥵')
    db.set_player(event.sender_id)
    await bot.send_message(event.sender_id, "CARICHI??? 😤😤😤")

    await notify_users(db.get_other_users(event.sender_id), f'La carica pervade il corpo di {db.get_user(event.sender_id)} 🔋🔋🔋')


@bot.on(events.NewMessage(pattern='/scarichi'))
async def scarichi(event):
    if not db.is_created(event.sender_id):
        return await event.reply('Non sei ancora registrato, usa il comando /start per scoprire come fare')

    if not db.is_player(event.sender_id):
        return await event.reply('Non ricordavo che fossi carico 🤔 \nPer baitare i cazzoni usa il comando /carichi e poi il comando /scarichi')
    db.set_player(event.sender_id, wantstoplay=False)
    await bot.send_message(event.sender_id, "Ua squet 😔")
    await notify_users(db.get_other_users(event.sender_id), f'{db.get_user(event.sender_id)} ha foldato 😔')


@bot.on(events.NewMessage(pattern='/iuajuni'))
async def iuajuni(event):
    players = db.get_players()
    if not players:
        return await event.reply('La carica è allo 0% 🪫 Usa il comando /carichi per diffonderla')
    usernames = [repr(user) for user in players]
    list = ",\n".join(usernames)
    await bot.send_message(event.sender_id, f'La carica è con:\n{list}')


@bot.on(events.NewMessage(pattern='/dovequando'))
@last_handler_decorator
async def dovequando(event):
    when = db.when
    where = db.where
    if when == "" and where == "":
        response = 'Non si sa ancora né dove né quando giochiamo 🤔\n'
    elif when == "":
        response = where + '\n'
        response += f'Non si sa ancora quando giochiamo 🤔\n'
    elif where == "":
        response = when + '\n'
        response += f'Non si sa ancora dove giochiamo 🤔\n'
    else:
        response = f'{db.where} - {db.when}'
    await bot.send_message(event.sender_id, response)


@bot.on(events.NewMessage(pattern='/dove'))
async def dove(event):
    where = db.where
    if where == "":
        return await event.reply('Non si sa ancora dove giochiamo 🤔')
    await bot.send_message(event.sender_id, f'{db.where}')


@bot.on(events.NewMessage(pattern='/quando'))
async def quando(event):
    when = db.when
    if when == "":
        return await event.reply('Non si sa ancora quando giochiamo 🤔')
    await bot.send_message(event.sender_id, f'{when}')


@bot.on(events.NewMessage(pattern='/setdove'))
async def setdove(event):
    if not db.is_created(event.sender_id):
        return await event.reply('Non sei ancora registrato, usa il comando /start per scoprire come fare')
    if not db.is_player(event.sender_id):
        return await event.reply('Non sei abbastanza carico 🪫😔, usa il comando /carichi per scoprire un altro lato di te 😤')
    chunks = event.raw_text.split(' ')
    if len(chunks) == 1:
        return await event.reply('Devi specificare un luogo dopo /setdove\n Esempio: /setdove __Locubia fratm__')

    user = db.get_user(event.sender_id)
    old_where = db.where
    new_where = " ".join(chunks[1:])
    db.where = new_where

    if old_where != "":
        await notify_users(db.get_other_users(event.sender_id), f'{user} ha cambiato il luogo della partita da "{old_where}" a "{new_where}"⁉️')
    else:
        await notify_users(db.get_other_users(event.sender_id), f'{user} ha impostato il luogo della partita a "{new_where}"⁉️')
    await bot.send_message(event.sender_id, f'Okke ammo')


@bot.on(events.NewMessage(pattern='/setquando'))
async def setquando(event):
    if not db.is_created(event.sender_id):
        return await event.reply('Non sei ancora registrato, usa il comando /start per scoprire come fare')
    if not db.is_player(event.sender_id):
        return await event.reply('Non sei abbastanza carico 🪫😔, usa il comando /carichi per scoprire un altro lato di te 😤')
    chunks = event.raw_text.split(' ')
    if len(chunks) == 1:
        return await event.reply('Devi specificare la data-ora dopo /setquando\n Esempio: /setquando __Alle 19__')

    user = db.get_user(event.sender_id)
    old_when = db.when
    new_when = " ".join(chunks[1:])
    db.when = f"{new_when} (Impostato alle {datetime.now().strftime('%H:%M')} del {datetime.now().strftime('%d/%m/%Y')})"

    if old_when != "":
        await notify_users(db.get_other_users(event.sender_id), f'{user} ha cambiato il momento della partita da "{old_when}" a "{new_when}"⁉️')
    else:
        await notify_users(db.get_other_users(event.sender_id), f'{user} ha impostato il momento della partita a "{new_when}"⁉️')
    await bot.send_message(event.sender_id, f'Okke ammo')


@bot.on(events.NewMessage(pattern='/reset'))
async def reset(event):
    if not db.is_created(event.sender_id):
        return await event.reply('Non sei ancora registrato, usa il comando /start per scoprire come fare')
    db.reset()
    await notify_users(db.get_other_users(event.sender_id), f'{db.get_user(event.sender_id)} ha resettato luogo, data, ora e carica 🏁')
    await bot.send_message(event.sender_id, f'Luogo, data, ora e carica sono stati resettati')


@bot.on(events.NewMessage(pattern='/backup'))
async def backup(event):
    backup = db.backup
    where = backup["where"]
    when = backup["when"]
    users = backup["users"]
    list_of_users = ",\n".join([repr(player) for player in users])
    await bot.send_message(event.sender_id, f"Prima di resettare c'era: \nposto: {where}\ndata: {when}\n\ngiocatori: \n{list_of_users}")

if __name__ == "__main__":
    with bot:
        print("Bot is running")
        bot.run_until_disconnected()
