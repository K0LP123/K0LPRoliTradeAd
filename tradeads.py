#Hello someone /e wave
#Started working on this discord bot on 17/09/2025 :P - k0lp
import discord
from discord.ext import commands
import json
import requests
from datetime import datetime, timedelta
import random
import asyncio

CONFIG_FILE = "config.json"

def load_config_file():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config_file(config_file):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_file, f, indent=4)

config_file = load_config_file()

urlTA = 'https://api.rolimons.com/tradeads/v1/createad'
urlIL = 'https://api.rolimons.com/items/v2/itemdetails'
urlPI = f'https://inventory.roblox.com/v1/users/{config_file["PlayerID"]}/assets/collectibles?limit=100&sortOrder=Asc'

responseIL = requests.get(urlIL)
resIL = responseIL.json()

Tag_Icons = {
    "upgrade": "📈 Upgrade",
    "downgrade": "📉 Downgrade",
    "adds": "➕ Adds",
    "any": "📊 Any",
    "wishlist": "🗄️ Wishlist",
    "demand": "📊 Demand",
    "rares": "💎 Rares",
    "rap": "📊 Rap",
    "robux": "💲 Robux",
    "projecteds": "⚠️ Projecteds"
}

#Bot settings 
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)


#NFT command
@bot.group(name="nft", invoke_without_command=True)
async def nft(ctx):
    await ctx.send("❌ Use `add`, `remove`, `list` or `clear`! Use `!help nft` for more details!")

@nft.command(name="list") #NFT Embed List
async def nft_list(ctx):

    config_file = load_config_file()
    NFT_Items=[]
    NonRolimonsApiItems=0

    for NFT_List in config_file["NotForTrade"]:
        item_data = resIL["items"].get(str(NFT_List))
        if item_data:
            if item_data[1] != "": #Checks if theres an acronym and if there is it picks it
                Item_Name = item_data[1]
            else:
                Item_Name=item_data[0]# If there isnt sets item name
            Item_Value=item_data[4]
            NFT_Items.append((Item_Name, NFT_List, Item_Value))
        else:
            NonRolimonsApiItems = NonRolimonsApiItems +1
            await ctx.send(f"❌ Rolimons API doesnt recognize {NonRolimonsApiItems} IDs in the config!")
    NFT_Items = sorted(NFT_Items, key=lambda x: x[2], reverse=True) #Sorts Items by value 
    
    NFT_Item_List = ""
    for Item_Name, NFT_List, _ in NFT_Items:
        NFT_Item_List += f"● {Item_Name} ({NFT_List})\n"
            
    nftembed = discord.Embed(
        title="🚫 Not For Trade List",
        color=0x33cc66
    )

    nftembed.add_field(name="", value=NFT_Item_List, inline=False)

    await ctx.send(embed=nftembed) #Sends embed

@nft.command(name="add") #NFT add
async def NFTAdd(ctx, *, arg: str = None):
    arg_id = int(arg)

    if arg is None:
        await ctx.send("❌ Forgot the parameter!")
        return
    
    config_file = load_config_file()

    if arg_id in config_file["NotForTrade"]:
        await ctx.send(f"❌ Item is already in NFT List.")
        return
    
    #Adds ID to the config
    item_data = resIL["items"].get(str(arg))
    if item_data:
        config_file["NotForTrade"].append(arg_id)
        save_config_file(config_file)
        await ctx.send(f"✅ ID: {arg} has been added to NFT List!")
    else:
        await ctx.send(f"❌ Item not recognized by Rolimons API!")       

@nft.command(name="remove") #NFT remove
async def NFTRemove(ctx, *, arg: str = None):
    arg_id = int(arg)

    if arg is None:
        await ctx.send("❌ Forgot the parameter! ")
        return
    
    config_file = load_config_file()

    if arg_id not in config_file["NotForTrade"]:
        await ctx.send(f"⚠️ ID isnt in the NFT List.")
        return
    
    config_file["NotForTrade"].remove(arg_id)
    save_config_file(config_file)
    await ctx.send(f"✅ ID: {arg_id} has been removed from NFT List!")

@nft.command(name="clear") #NFT clear
async def NFTClear(ctx, *, arg: str = None):
    config_file = load_config_file()
    
    config_file["NotForTrade"].clear()
    save_config_file(config_file)
    await ctx.send("✅ Nft list has been cleared!")


#Tags command
@bot.group(name="tags", invoke_without_command=True)
async def tags(ctx):
    await ctx.send('❌ Use `add`, `remove`, `list`, `clear` or `set`! Use `!help tags` for more details!')

@tags.command(name="list") #Tags Embed List
async def TagsList(ctx):

    tagsembed = discord.Embed(
        title="🏷️ Tags ",
        color=0x33cc66,
        description="📈 Upgrade\n📉 Downgrade\n📊 Demand\n💎 Rares\n📊 Rap\n💲 Robux\n➕ Adds\n⚠️ Projecteds\n📊 Any\n🗄️ Wishlist\n",
    )

    await ctx.send(embed=tagsembed) #Sends embed

@tags.command(name="add") #Tags add
async def TagsAdd(ctx, *, arg: str = None):

    if arg is None:
        await ctx.send("❌ Forgot the tag! List of tags: `upgrade`, `downgrade`, `adds`, `demand`, `rap`, `rares`, `robux`, `projecteds`, `any` and `wishlist`.")
        return
    
    config_file = load_config_file()

    if arg in config_file["Tags"]:
        await ctx.send(f"⚠️ Tag already in Tags.")
        return
    
    All_Of_Tags =["add", "upgrade", "downgrade", "any", "wishlist", "demand", "rares", "rap", "robux", "projecteds"]
    if arg not in All_Of_Tags:
        await ctx.send(f"❌ Tag doesnt exist! List of tags: `upgrade`, `downgrade`, `adds`, `demand`, `rap`, `rares`, `robux`, `projecteds`, `any` and `wishlist`.")
        return
    #Adds ID to the config
    if len(config_file["Tags"]) < 4:
        config_file["Tags"].append(arg)
        save_config_file(config_file)
        await ctx.send(f"✅ {arg} has been added to Tags")
    else:
        await ctx.send("❌ Theres 4 tags already!")

@tags.command(name="remove") #Tags remove
async def Tags_Remove(ctx, *, arg: str = None):
    if arg is None:
        await ctx.send("❌ Forgot the parameter! List of tags: `upgrade`, `downgrade`, `adds`, `demand`, `rap`, `rares`, `robux`, `projecteds`, `any` and `wishlist`.")
        return
    
    config_file = load_config_file()
    
    if arg not in config_file["Tags"]:
        await ctx.send(f"⚠️ Tag not found in Tags.")
        return
    
    config_file["Tags"].remove(arg)
    save_config_file(config_file)
    await ctx.send(f"✅ {arg} has been removed from Tags!")

@tags.command(name="set") #Tags Sets presets
async def TagsList(ctx, *, arg: str = None):
    if arg == "list":
        await ctx.send("```You can make your presets by editing config.json file!\n\n  default\n- 📈 Upgrade\n- 📉 Downgrade\n- 📊 Demand\n- 📊 Rap\n\n  adds1\n- 📈 Upgrade\n- 📉 Downgrade\n- ➕ Adds\n\n  adds2\n- 📊 Any\n- ➕ Adds\n\n  adds3\n- ➕ Adds\n\n```")
        return
    config_file=load_config_file()
    if arg in config_file:
        larg = arg.lower()
        config_file["Tags"] = config_file[f"{larg}"]
        save_config_file(config_file)
        await ctx.send(f"✅ Tags set to {larg} preset!")
        return
    
    if arg not in config_file:
        await ctx.send(f"❌ Preset doesnt exist!")
        return
    
    await ctx.send("❌ Check `!tags set list` for list of presets!")

@tags.command(name="clear") #Tags clear
async def TagsClear(ctx, *, arg: str = None):
    config_file = load_config_file()
    
    config_file["Tags"].clear()
    save_config_file(config_file)
    await ctx.send("✅ Tags have been cleared!")


#Config command        
@bot.command(name="config") 
async def config_command(ctx):
    config_file = load_config_file()

    configembed = discord.Embed(
        title="📋 Your Config",
        color=0x33cc66
    )

    if config_file["AutoPick"] == "false" and config_file["Top4"] == "false":
        Manual_Pick = "true"
    else:
        Manual_Pick = "false"

    #Fields  
    configembed.add_field(name="Auto Pick", value=f"`{config_file['AutoPick'] }`", inline=True)
    configembed.add_field(name="Minimum Value", value=f"`{config_file['MinValue'] }`", inline=True)
    configembed.add_field(name="Top 4", value=f"`{config_file['Top4'] }`", inline=False)
    configembed.add_field(name="Manual Pick", value=f"`{Manual_Pick}`", inline=False)
    configembed.add_field(name="Demand Only", value=f"`{config_file['DemandOnly'] }`", inline=True)
    configembed.add_field(name="Time", value=f"`{int(config_file['Time']/60)} minutes`", inline=False)
    configembed.add_field(name="Robux", value=f"`{config_file['Robux'] }`", inline=True) #In life we have robux

    if config_file["AutoPick"] == "true": #Items offered Autopick
        configembed.add_field(name="✉️ Offered Items:", value="AutoPick chosen! Bot will randomly pick items", inline=False)

    NotOnthold=[]
    Top4Items=[]
    #Items offered Top4
    if config_file["Top4"] == "true":
        responsePI = requests.get(urlPI)
        res_PI = responsePI.json()
        dataIH = res_PI.get("data")
        
        for ItemsHold in dataIH:
            ItemID = ItemsHold.get("assetId")
            if ItemsHold.get("isOnHold") is False:
                NotOnthold.append(ItemID)

        for item in NotOnthold:
            if item in config_file["NotForTrade"]: #removes nft items
                continue
            item_data = resIL["items"].get(str(item))
            if item_data:
                if item_data[1] != "": #Checks if theres an acronym and if there is it picks it
                    Item_Name = item_data[1]
                else:
                    Item_Name=item_data[0]# If there isnt sets item name
                value=item_data[4]
                Top4Items.append((item, value, Item_Name))
             
        Top4List = [(Item_Name, value) for _, value, Item_Name in sorted(Top4Items, key=lambda x: x[1], reverse=True)[:4]]
        Top4FinalList = ""
        for name, value in Top4List: #Makes fancy numbers
            ItemValue = value
            if value >= 1000:
                value = value / 1000
                if value.is_integer():
                    ItemValue = f"{int(value)}K"
                else:
                    ItemValue = f"{value:.1f}K"   
            elif value >= 1000000:
                value = value / 1000000
                if value.is_integer():
                    ItemValue = f"{int(value)}M"
                else:
                    ItemValue = f"{value:.1f}M"
            elif value <= 1000:
                ItemValue = int(value)
            Top4FinalList += f"● {name} {ItemValue}\n"
        configembed.add_field(name="✉️ Offered Items", value=Top4FinalList, inline=False)

    if Manual_Pick == "true": #Manual pick
        Manual_Offered =[]
        if config_file["OfferedItems"]:
            for item in config_file["OfferedItems"]:
                item_data = resIL["items"].get(str(item))
                if item_data:
                    if item_data[1] != "": #Checks if theres an acronym and if there is it picks it
                        Item_Name = item_data[1]
                    else:
                        Item_Name=item_data[0]# If there isnt sets item name
                    value=item_data[4]
                    Manual_Offered.append((item, value, Item_Name))

                ManualList = [(Item_Name, value) for _, value, Item_Name in sorted(Manual_Offered, key=lambda x: x[1], reverse=True)[:4]]
                ManualListFinal = ""
                for name, value in ManualList:
                    if value >= 1000000:
                        value = value / 1000000
                        if value.is_integer():
                            ItemValue = f"{int(value)}M"
                        else:
                            ItemValue = f"{value:.1f}M"
                    elif value >= 1000:
                        value = value / 1000
                        if value.is_integer():
                            ItemValue = f"{int(value)}K"
                        else:
                            ItemValue = f"{value:.1f}K"   
                    elif value <= 1000:
                        ItemValue = int(value)
                    ManualListFinal += f"● {name} {ItemValue}\n"
        else:
            ManualListFinal="`None`"

        configembed.add_field(name="✉️ Offered Items:", value=ManualListFinal, inline=False)

    #Tags
    Tags = ""
    for item_str in config_file["Tags"]:
        if item_str in Tag_Icons:
            Tags += f"- {Tag_Icons[item_str]}\n"
        else:
            Tags += f"- {item_str}\n"

    configembed.add_field(name="🏷️ Tags", value=Tags, inline=False) #Tags
    
    #Requested Items
    Fancy_Requested = ""  
    if config_file["RequestedItems"]:
        for item_id in config_file["RequestedItems"]:
            item_data = resIL["items"].get(str(item_id))
            if item_data:
                if item_data[1] != "": #Checks if theres an acronym and if there is it picks it
                    Item_Name = item_data[1]
                else:
                    Item_Name=item_data[0]# If there isnt sets item name
                value=item_data[4]
                Fancy_Requested += f"● {Item_Name} {value}\n"
    else:
        Fancy_Requested = "`None`"

    configembed.add_field(name="🔍 Requested Items", value=Fancy_Requested, inline=False)

    await ctx.send(embed=configembed) #sends embed



#Set command
@bot.group(name="set", invoke_without_command=True)
async def set(ctx):
    await ctx.send('❌ Wrong option! Use `!help set` for more details!')


@set.command(name="autopick") #Set Autopick
async def SetAutopick(ctx):
    config_file = load_config_file()
    config_file["AutoPick"] = "true"
    config_file["Top4"] = "false"
    save_config_file(config_file)
    await ctx.send('✅ AutoPick has been picked!')

@set.command(name="demandonly") #Set DemandOnly
async def SetDemandOnly(ctx, *, arg: str = None):
    if arg == "true":
        config_file = load_config_file()
        config_file["DemandOnly"] = "true"
        await ctx.send('✅ DemandOnly has been set to: True')

        save_config_file(config_file)
        return

    if arg == "false":
        config_file = load_config_file()
        config_file["DemandOnly"] = "false"
        save_config_file(config_file)
        await ctx.send('❌ DemandOnly has been set to: False')
        return

    await ctx.send('❌ DemandOnly can be only set as: `false/true`')

@set.command(name="manualpick") #Set Manualpick
async def SetManualPick(ctx):
    config_file = load_config_file()
    config_file["AutoPick"] = "false"
    config_file["Top4"] = "false"
    save_config_file(config_file)
    await ctx.send('✅ ManualPick has been picked!')

@set.command(name="minvalue") #Set MinValue
async def SetMinValue(ctx, *, arg: str = None):
    config_file = load_config_file()
    if arg.isnumeric():
        config_file["MinValue"] = int(arg)
        save_config_file(config_file)
        await ctx.send(f'✅ Minvalue has been set to: `{arg}`')
    else:
        await ctx.send('❌ This isnt a number')

@set.command(name="playerid") #Set PlayerID
async def SetPlayerID(ctx, *, arg: str = None):
    config_file = load_config_file()
    if arg.isnumeric():
        config_file["PlayerID"] = int(arg)
        save_config_file(config_file)
        await ctx.send(f'✅ PlayerID has been set to: `{arg}`')
    else:
        await ctx.send('❌ This isnt a number')

@set.command(name="robux") #Set Robux
async def SetRobux(ctx, *, arg: str = None):
    config_file = load_config_file()
    if arg.isnumeric():
        config_file["Robux"] = int(arg)
        save_config_file(config_file)
        await ctx.send(f'✅ Robux has been set to: `{arg}`')
    else:
        await ctx.send('❌ This isnt a number')

@set.command(name="time") #Set Time
async def SetTime(ctx, *, arg: str = None):
    config_file = load_config_file()
    if arg.isnumeric():
        config_file["Time"] = int(arg)
        save_config_file(config_file)
        await ctx.send(f'✅ Time has been set to: `{arg}` seconds')
    else:
        await ctx.send('❌ This isnt a number')

@set.command(name="top4") #Set Top4
async def SetAutopick(ctx):
    config_file = load_config_file()
    config_file["Top4"] = "true"
    config_file["AutoPick"] = "false"
    save_config_file(config_file)
    await ctx.send('✅ Top4 has been picked!')

@set.command(name="rolitoken") #Set Rolimons Token
async def SetRoliToken(ctx, *, arg: str = None):

    config_file = load_config_file()
    config_file["RolimonsToken"] = arg
    save_config_file(config_file)
    await ctx.send('✅ Rolimons Token has been set')

@set.command(name="channel") #Set Discord Channel
async def SetChannel(ctx, *, arg: str = None):
        config_file = load_config_file()
        config_file["DiscordChannel"] = int(arg)
        save_config_file(config_file)
        await ctx.send('✅ Discord Channel has been set')



#Items Command
@bot.group(name="items", invoke_without_command=True)
async def items(ctx):
    await ctx.send('❌ Use `offered <option>` or `requested <option>`. Check `!help items` for more!')


#Items Offered
@items.group(name="offered", invoke_without_command=True) #Items offered
async def itemsoffered(ctx):
    await ctx.send('❌ Use `add`, `clear` or `remove`. Check `!help items` for more!')

@itemsoffered.command(name="add") #Items offered add
async def itemsofferedadd(ctx, *, arg: str = None):
    if arg is None:
        await ctx.send('❌ Please provide an item ID to remove')
        return
    
    config_file = load_config_file()
    if arg.isnumeric():
        if len(config_file["OfferedItems"]) < 4:
            item_data = resIL["items"].get(str(int(arg)))
            if item_data:
                config_file["OfferedItems"].append(int(arg))
                save_config_file(config_file)  
                await ctx.send(f'✅ {arg} has been added to Offered Items!')
            else:
                await ctx.send('❌ Couldnt find this item in Rolimons API')
        else:
            await ctx.send('❌ Theres 4 IDs in Offered Items!')            

    else:
        await ctx.send('❌ Thats not a number :C')

@itemsoffered.command(name="remove") #Items offered remove
async def itemsofferedremove(ctx, *, arg: str = None):
    if arg is None:
        await ctx.send('❌ Please provide an item ID to remove')
        return

    if arg.isnumeric():
        config_file = load_config_file()
        if int(arg) in config_file["OfferedItems"]:
            config_file["OfferedItems"].remove(int(arg))
            save_config_file(config_file)  
            await ctx.send(f'✅ {arg} has been removed from Offered Items!')
        else:
            await ctx.send('❌ Couldnt find this item in your config')
    else:
        await ctx.send('❌ Thats not a number :C')

@itemsoffered.command(name="clear") #NFT clear
async def itemsofferedclear(ctx, *, arg: str = None):
    config_file = load_config_file()
    
    config_file["OfferedItems"].clear()
    save_config_file(config_file)
    await ctx.send("✅ OfferedItems items have been cleared!")

#Items Requested
@items.group(name="requested", invoke_without_command=True) #Items offered
async def itemsrequested(ctx):
    await ctx.send('❌ Use `add`, `clear` or `remove`. Check `!help items` for more!')

@itemsrequested.command(name="add") #Items offered add
async def itemsrequestedadd(ctx, *, arg: str = None):
    if arg is None:
        await ctx.send('❌ Please provide an item ID to remove')
        return
    
    config_file = load_config_file()
    if arg.isnumeric():
        item_data = resIL["items"].get(str(int(arg)))
        if len(config_file["RequestedItems"]) < 4:
            if item_data:
                config_file["RequestedItems"].append(int(arg))
                save_config_file(config_file)  
                await ctx.send(f'✅ {arg} has been added to Requested Items!')
            else:
                await ctx.send('❌ Couldnt find this item in Rolimons API')
        else:
            await ctx.send('❌ Theres already 4 IDs in Requested Items!')            
    else:
        await ctx.send('❌ Thats not a number :C')

@itemsrequested.command(name="remove") #Items offered remove
async def itemsrequestedremove(ctx, *, arg: str = None):
    if arg is None:
        await ctx.send('❌ Please provide an item ID to remove')
        return
    
    if arg.isnumeric():
        config_file = load_config_file()
        if int(arg) in config_file["RequestedItems"]:
            config_file["RequestedItems"].remove(int(arg))
            save_config_file(config_file)  
            await ctx.send(f'✅ {arg} has been removed from Requested Items!')
        else:
            await ctx.send('❌ Couldnt find this item in your config')
    else:
        await ctx.send('❌ Thats not a number :C')

@itemsrequested.command(name="clear") #NFT clear
async def itemsrequestedclear(ctx, *, arg: str = None):
    config_file = load_config_file()
    
    config_file["RequestedItems"].clear()
    save_config_file(config_file)
    await ctx.send("✅ Requested Items have been cleared!")

#Help command
bot.remove_command('help')
@bot.group(name="help", invoke_without_command=True)
async def help(ctx, *, arg: str = None):
    if arg != "help":
        nftembed = discord.Embed(
            title="📝 Help",
            description='List of all commands with options avaible in this discord bot.\nUse `!help <command>` for more details and examples.',
            color=0x33cc66
        )

        nftembed.add_field(name="items:", value="offered / requested \n`add <id>`\n`remove <id>`\n`clear`\n", inline=False)
        nftembed.add_field(name="set", value="`autopick`\n`channel`\n`demandonly <true/false>`\n`manualpick`\n`minvalue <number>`\n`playerid <id>`\n`robux <number>`\n`time <number> (in seconds)`\n`rolitoken <token>`\n`top4`", inline=False)
        nftembed.add_field(name="nft", value='`add <id>`\n`remove <id>`\n`clear`', inline=False)
        nftembed.add_field(name="tags", value="`add <tag>`\n`remove <tag>`\n`set <preset>`\n`clear`\n`list`\n", inline=False)
        nftembed.add_field(name="config", value="`None`", inline=False)
        nftembed.add_field(name="help", value="`None`\n`items`\n`set`\n`nft`\n`tags`\n`config`", inline=False)

        await ctx.send(embed=nftembed) #Sends embed

    if arg =="help":
        await ctx.send('Uhhhhhhh what? Why would I know what help does? You might need to google that twin.')

@help.command(name="config") #Config Help 
async def helpconfig(ctx, *, arg: str = None):
    await ctx.send('```Shows your current config.```')

@help.command(name="nft") #NFT Help FIX IT 
async def helpnft(ctx, *, arg: str = None):
    await ctx.send('```Lets you edit your "Not For Trade" list.\nCommands:\n\nnft add <id>\n- Adds ID to NFT list.\n\nnft remove <id>\n- Removes ID from NFT list.\n\nnft clear\n- Clears your NFT list.```')

@help.command(name="set") #Set Help FIT IT
async def helpset(ctx, *, arg: str = None):
    await ctx.send('```Lets you edit your config file.\nCommands:\n\nset autopick\n- Changes Autopick to true and Top4 to false.\n\nset demandonly <true/false>\n- When set to true, top4/autopick will only pick items that have at least terrible demand on rolimons website.\n\nset manualpick\n- Sets Top4 and Autopick to False.\n\nset minvalue <number>\n- Autopick wont pick items with value under this number.\n\nset playerid <id>\n- Sets PlayerID in config to typed ID.\n\nset robux <number>\n- Sets Robux number.\n\nset time <number> (in seconds)\n- Sets time between trade ads in seconds.\n\nset rolitoken <token>\n- Sets your Rolimons Token.\n\nset top4\n- Changes Autopick to False and Top4 to True\n\n```')

@help.command(name="tags") #Tags Help FIT IT
async def helptags(ctx, *, arg: str = None):
    await ctx.send('W.I.P.')

@help.command(name="items") #Items Help FIT IT
async def helpitems(ctx, *, arg: str = None):
    await ctx.send('W.I.P.')

#Hello again someone
#Last change of this discord bot was on 01/10/2025 :P

#Start of Trade Ad maker
#Started working on this on 21/09/2025 :D
async def trade_ad_loop():
    while True:
        config_file = load_config_file()
        Logs =""

        #Bot sending Errors/Trade ads to discord channel
        channel_id = config_file.get("DiscordChannel")
        channel = None
        if channel_id is not None:
            channel = bot.get_channel(channel_id)
        else:
            print("⚠️ Discord Channel not found! Check if you typed correct id or use !set channel <id> to set it!")

        RolimonsToken = config_file["RolimonsToken"]
        Top4 = config_file["Top4"]
        AutoPick = config_file["AutoPick"]
        Minvalue = config_file["MinValue"]
        NotForTrade = config_file["NotForTrade"]
        OfferedItems = config_file["OfferedItems"]
        Robux = config_file["Robux"]
        RequestedItems = config_file["RequestedItems"]
        PlayerId = config_file["PlayerID"]
        Tags=config_file["Tags"]
        Time=config_file["Time"]
        DemandOnly=config_file["DemandOnly"]

        data = {
            "offer_item_ids": OfferedItems,
            "offer_robux": Robux,
            "player_id": PlayerId,
            "request_item_ids": RequestedItems,
            "request_tags": Tags
        }

        if Robux <= 0: #u cant make a trade ad when robux are 0 or less than a 0
            del data["offer_robux"]

        headers = {
            "content-type": "application/json",
            "cookie": "_RoliVerification=" + RolimonsToken
        }

        responsePI = requests.get(urlPI)
        res_PI = responsePI.json()
        responseIL = requests.get(urlIL)
        res_IL = responseIL.json()

        NotOnthold=[]
        ItemValues=[]
        NotOntholdForTrade =[]
        TradeMode =""

        if Top4 == "true" or AutoPick == "true":
            dataIH = res_PI.get("data")
            for ItemsHold in dataIH:
                ItemID = ItemsHold.get("assetId")
                if ItemsHold.get("isOnHold") is False:
                    NotOnthold.append(ItemID)

            for item in NotOnthold:
                if item in NotForTrade:
                    continue
                else:
                    NotOntholdForTrade.append(item)

            if Top4 == "true":#Make top4 and autopick to be 1
                for item in NotOntholdForTrade:
                    item_data = res_IL["items"].get(str(item))
                    if item_data:
                        value=item_data[4]
                        if DemandOnly == "true":
                            if item_data[5] >= 0:
                                ItemValues.append((item, value))
                            else:
                                continue
                        if DemandOnly == "false":
                            ItemValues.append((item, value))

                Top4List = [item_id for item_id, _ in sorted(ItemValues, key=lambda x: x[1], reverse=True)[:4]]

                data["offer_item_ids"] = Top4List

            elif AutoPick == "true":
                for item in NotOntholdForTrade:
                    item_data = res_IL["items"].get(str(item))
                    if item_data:
                        value=item_data[4]
                        if value >= Minvalue:
                            if DemandOnly == "true":
                                if item_data[5] >= 0:
                                    ItemValues.append((item, value))
                                else:
                                    continue
                            if DemandOnly == "false":
                                ItemValues.append((item, value))
                                
                if len(ItemValues) >= 4:
                    AutoPickList = [item_id for item_id, _ in sorted(random.sample(ItemValues, 4), key=lambda x: x[1], reverse=True)]
                else:
                    AutoPickList = [item_id for item_id, _ in sorted(ItemValues, key=lambda x: x[1], reverse=True)]

                data["offer_item_ids"] = AutoPickList

        responseTA = requests.post(urlTA, json=data, headers=headers)

        if Top4 == "true":#Very pro code ignore plz
            if DemandOnly =="false":
                TradeMode = "Top4"
            elif DemandOnly =="true":
                TradeMode = "Top4 with DemandOnly"
        elif AutoPick == "true":
            if DemandOnly =="false":
                TradeMode = "Autopick"
            elif DemandOnly =="true":
                TradeMode = "Autopick with DemandOnly"
        else:
            TradeMode = "Manualpick"
            

        res_TA = responseTA.json()
        if res_TA.get("success") == True:

            Logs += (f"✅ Trade ad Posted! ({TradeMode})\n\n")
            TotalValue = 0
            TotalRap = 0
            OffItems = []

            if Top4 == "false" and AutoPick == "false":
                for item_id in OfferedItems:
                    item_data = res_IL["items"].get(str(item_id))
                    if item_data:
                        TotalValue += item_data[4]
                        TotalRap += item_data[2]
                        if item_data[1] == "":
                            OffItems.append(f"- {item_data[0]} Item Value: {item_data[4]}")
                        else:
                            OffItems.append(f"- ({item_data[1]}) {item_data[0]}. Item Value: {item_data[4]}")

            elif Top4 == "true":
                for item in Top4List:
                    item_data = res_IL["items"].get(str(item))
                    if item_data:
                        TotalValue += item_data[4]
                        TotalRap += item_data[2]
                        if item_data[1] == "":
                            OffItems.append(f"- {item_data[0]} | Item Value: {item_data[4]}")
                        else:
                            OffItems.append(f"- {item_data[1]} | Item Value: {item_data[4]}")

            elif AutoPick == "true":
                for item in AutoPickList:
                    item_data = res_IL["items"].get(str(item))
                    if item_data:
                        TotalValue += item_data[4]
                        TotalRap += item_data[2]
                        if item_data[1] == "":
                            OffItems.append(f"- {item_data[0]} | Item Value: {item_data[4]}")
                        else:
                            OffItems.append(f"- {item_data[1]} | Item Value: {item_data[4]}")

            Logs += (f"📊 Total Value: {TotalValue}\n")
            Logs += (f"📊 Total RAP: {TotalRap}\n\n")

            if RequestedItems:
                ReqItems = []
                for line in RequestedItems:
                    item_data = res_IL["items"].get(str(line))
                    if item_data[1] == "":
                        ReqItems.append(f"- {item_data[0]} | Item Value: {item_data[4]}")
                    else:
                        ReqItems.append(f"- {item_data[1]} | Item Value: {item_data[4]}")

                ReqItemslist =""
                for line in ReqItems:
                    ReqItemslist += f"{line}\n"
                
                Logs += (f"🔍 Requested Items:\n{ReqItemslist}\n\n")

            #Tags
            TagsText = ""
            for item_str in config_file["Tags"]:
                TagsText += f"- {Tag_Icons.get(item_str)}\n"

            if TagsText:
                Logs += (f"🔍 Tags:\n{TagsText}\n")

            if Robux > 0:
                Logs += (f"💲 Robux: {Robux}\n\n")

            Logs += ("📜 Offered Items:\n")
            OffItemslist=""
            for line in OffItems:
                OffItemslist += f"{line}\n"
            
            future_time = datetime.now() + timedelta(seconds=Time)   
            Logs += (f"{OffItemslist}\n")
            Logs +=(f"🕒 Next Trade Ad will be posted in: {Time / 60} minutes, Aka: {future_time.strftime('%H:%M')}\n")

            #Sends Trade ad into discord channel and terminal
            print(Logs)
            if channel:
                await channel.send(Logs)

        ErrorLogs =""     
        if res_TA.get("success") == False:
            future_time = datetime.now() + timedelta(seconds=Time)
            if res_TA.get("code") == 7105:
                ErrorLogs +=(f"⏳ Ad creation cooldown has not elapsed ⏳\n🕒 Next try will be at: {future_time.strftime('%H:%M')} 🕒")
    
            elif res_TA.get("code") == 7110:
                ErrorLogs+=(f"❌ Change your Robux! Robux number can't exceed 50% RAP. ❌\n🕒 Next try will be at: {future_time.strftime('%H:%M')} @everyone 🕒")            
            
            elif res_TA.get("code") == 5:
                ErrorLogs +=(f"❌ Invalid Rolimons Token! ❌\n🕒 Next try will be at: {future_time.strftime('%H:%M')} @everyone 🕒")
    
            elif res_TA.get("code") == 14:
                ErrorLogs +=(f"❌ 24-hour ad creation limit has been hit! ❌\n🕒 Next try will be at: {future_time.strftime('%H:%M')} @everyone 🕒")
    
            elif res_TA.get("code") == 7104:
                ErrorLogs+=(f"❌ Player does not own all offered items! ❌\n🕒 Next try will be at: {future_time.strftime('%H:%M')} @everyone 🕒")
    
            elif res_TA.get("code") == 7111:
                ErrorLogs+=(f"❌ Requested value exceeds limit based on offered value (More than 5x) ❌\n🕒 Next try will be at: {future_time.strftime('%H:%M')} @everyone 🕒")
                        
            elif res_TA.get("code") == 2:
                if res_TA.get('message') =="Invalid offered item count":
                    ErrorLogs += (f"❌ There are no items offered or theres too much! ❌\n🕒 Next try will be at: {future_time.strftime('%H:%M')} @everyone 🕒")
                
                if res_TA.get('message') =="Invalid requested slot count":
                    config_file = load_config_file()
                    config_file["TagsReset"] +=1
                    save_config_file(config_file)
                    if config_file["TagsReset"]==1:
                        ErrorLogs += (f"❌ Theres more than 4 Total Tags and Requested items OR there arent any!\n⚠️ Next try will set tags to default and clear Requested Items.\n🕒 Next try will be at: {future_time.strftime('%H:%M')} @everyone 🕒")                    
                    elif config_file["TagsReset"]==2:
                        ErrorLogs += (f"⚠️ Tags and Requested Items have been reseted!\n🕒 Next try will be at: {future_time.strftime('%H:%M')} @everyone 🕒")
                        config_file["Tags"]=config_file["default"]
                        config_file["RequestedItems"] =[]
                        config_file["TagsReset"] =0
                        save_config_file(config_file)

                else:
                    ErrorLogs += (f"❌ Something is not working!\n❌ Error message: {res_TA.get('message')}\n❌ Error code: {res_TA.get('code')}\n🕒 Next try will be at: {future_time.strftime('%H:%M')} @everyone 🕒")

            elif res_TA.get("code") != None:
                ErrorLogs += (f"❌ Something is not working!\n❌ Error message: {res_TA.get('message')}\n❌ Error code: {res_TA.get('code')}\n🕒 Next try will be at: {future_time.strftime('%H:%M')} @everyone 🕒")
            
            print(ErrorLogs)
            if channel:
                await channel.send(ErrorLogs)

        await asyncio.sleep(int(Time))

#Hello hello again
#Last change of Trade Ad Thingy was on 27/09/2025 :P

#Errors
@bot.event
async def on_command_error(ctx, error):
    print("Command error:", error)

#Starts Trade Ad Thingy when discord bot loads
@bot.event
async def on_ready():
    bot.loop.create_task(trade_ad_loop()) 
    if config_file["TagsReset"] > 0:
        config_file["TagsReset"] =0
        save_config_file(config_file)


#Token
config_file = load_config_file()

TOKEN = config_file["TOKEN"]

if __name__ == "__main__":
    if not TOKEN:
        print("No discord token plz fix")
    else:
        bot.run(TOKEN)