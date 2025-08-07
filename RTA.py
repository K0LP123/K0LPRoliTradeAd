#MADE BY K0LP (or K0LP7 on Roblox :P)
#REMEMBER TO CONFIGURE YOUR CONFIG!!!!

import requests
import json
import time
from datetime import datetime, timedelta


#CONFIG
#CONFIG
RolimonsToken = 'Paste your _RoliVerification= here'

#AutoPick
Top4 = True #True/False -- Picks top 4 of your items that arent in NotForTrade
AutoPick = False #True/False -- Picks random 4 items from your inventory that are over Minvalue and arent in NotForTrade
Minvalue = 10000 #Minimum value of items in Autopick
NotForTrade = [] #Items that wont appear in Trade Ads if you use AutoPick

#Manually set your items
OfferedItems = [] 

#Trade Ad options
Robux = 0
RequestedItems = []
PlayerId = 1067821187
Tags=["upgrade", "downgrade", "demand", "robux"] #"adds", "upgrade", "downgrade", "any", "wishlist", "demand", "rares", "rap", "robux", "projecteds"

#Time
Time=1500 #1500 seconds is 25 minutes (57,6 trade ads a day). Everyday you can post 60 trade ads so if you want it to run 24/7 I wouldnt set it lower than 1440

#CONFIG
#CONFIG

urlTA = 'https://api.rolimons.com/tradeads/v1/createad'
urlIL = 'https://api.rolimons.com/items/v2/itemdetails'
urlPI = f'https://inventory.roblox.com/v1/users/{PlayerId}/assets/collectibles?limit=100&sortOrder=Asc'

data = {
    "offer_item_ids": OfferedItems,
    "offer_robux": Robux,
    "player_id": PlayerId,
    "request_item_ids": RequestedItems,
    "request_tags": Tags
}

if Robux == 0:
    del data["offer_robux"]

headers = {
    "content-type": "application/json",
    "cookie": "_RoliVerification=" + RolimonsToken
}

while True:
    responsePI = requests.get(urlPI)
    res_PI = responsePI.json()
    responseIL = requests.get(urlIL)
    res_IL = responseIL.json()
    NotOnthold=[]
    ItemValues=[]
    if Top4:
        dataIH = res_PI.get("data", [])
        for ItemsHold in dataIH:
            ItemID = ItemsHold.get("assetId")
            if ItemsHold.get("isOnHold") is False:
                NotOnthold.append(ItemID)

        for item in NotOnthold:
            if item in NotForTrade:
                continue
            item_str = str(item)
            item_data = res_IL["items"].get(item_str)
            if item_data:
                value=item_data[4]
                ItemValues.append((item, value))
        Top4List = [item_id for item_id, _ in sorted(ItemValues, key=lambda x: x[1], reverse=True)[:4]]

        data["offer_item_ids"] = Top4List
        responseTA = requests.post(urlTA, json=data, headers=headers)

        print("🤖 Top4 Pick! 🤖")

    if AutoPick:
        dataIH = res_PI.get("data", [])
        for ItemsHold in dataIH:
            ItemID = ItemsHold.get("assetId")
            if ItemsHold.get("isOnHold") is False:
                NotOnthold.append(ItemID)

        for item in NotOnthold:
            if item in NotForTrade:
                continue
            item_str = str(item)
            item_data = res_IL["items"].get(item_str)
            if item_data:
                value=item_data[4]
                if value >= Minvalue:
                    ItemValues.append((item, value))
        AutoPickList = [item_id for item_id, _ in sorted(random.sample(ItemValues, 4), key=lambda x: x[1], reverse=True)]

        data["offer_item_ids"] = AutoPickList
        print("🤖 Auto Pick! 🤖")
        responseTA = requests.post(urlTA, json=data, headers=headers)

    elif Top4 == False and AutoPick == False:
        print("🧑 Manual Pick 🧑")
        responseTA = requests.post(urlTA, json=data, headers=headers)

    res_TA = responseTA.json()
    if res_TA.get("success") == True:
        print("✅ Trade ad Posted!✅")
        TotalValue = 0
        TotalRap = 0
        OffItems = []

        if Top4 == False and AutoPick == False:
            for item_id in OfferedItems:
                item_str = str(item_id)
                item_data = res_IL["items"].get(item_str)
                if item_data:
                    TotalValue += item_data[4]
                    TotalRap += item_data[2]
                    if item_data[1] == "":
                        OffItems.append(f"- {item_data[0]} Item Value: {item_data[4]}")
                    else:
                        OffItems.append(f"- ({item_data[1]}) {item_data[0]}. Item Value: {item_data[4]}")

        elif Top4:
            for item_id in Top4List:
                item_str = str(item_id)
                item_data = res_IL["items"].get(item_str)
                if item_data:
                    TotalValue += item_data[4]
                    TotalRap += item_data[2]
                    if item_data[1] == "":
                        OffItems.append(f"- {item_data[0]} | Item Value: {item_data[4]}")
                    else:
                        OffItems.append(f"- ({item_data[1]}) {item_data[0]} | Item Value: {item_data[4]}")

        elif AutoPick:
            for item_id in AutoPickList:
                item_str = str(item_id)
                item_data = res_IL["items"].get(item_str)
                if item_data:
                    TotalValue += item_data[4]
                    TotalRap += item_data[2]
                    if item_data[1] == "":
                        OffItems.append(f"- {item_data[0]} | Item Value: {item_data[4]}")
                    else:
                        OffItems.append(f"- ({item_data[1]}) {item_data[0]} | Item Value: {item_data[4]}")

        print("📊 Total Value: ", TotalValue)
        print("📊 Total RAP: ", TotalRap)
        
        if RequestedItems:
            ReqItems = []
            for line in RequestedItems:
                item_str = str(line)
                item_data = res_IL["items"].get(item_str)
                if item_data[1] == "":
                    ReqItems.append(f"- {item_data[0]} | Item Value: {item_data[4]}")
                else:
                    ReqItems.append(f"- ({item_data[1]}) {item_data[0]} | Item Value: {item_data[4]}")

            print("🔍 Requested Items:")
            for line in ReqItems:
                print(line)

        if Tags:
            print("🔍 Tags:")
            for line in Tags:   #"adds", "upgrade", "downgrade", "any", "wishlist", "demand", "rares", "rap", "robux", "projecteds"
                if line == "adds":
                    print("- ➕ Adds")
                if line == "upgrade":
                    print("- 📈 Upgrade")
                if line == "downgrade":
                    print("- 📉 Downgrade")
                if line == "any":
                    print("- 📊 any")
                if line == "wishlist":
                    print("- 🗄️ wishlist")
                if line == "demand":
                    print("- 📊 demand")
                if line == "rares":
                    print("- 💎 rares")
                if line == "rap":
                    print("- 📊 rap")
                if line == "robux":
                    print("- 💲 robux")
                if line == "projecteds":
                    print("- ⚠️ projecteds")
                   
        if Robux > 0:
            print("💲 Offered Robux:", Robux)

        print("📜 Offered Items:")
        for line in OffItems:
            print(line)
            
        now = datetime.now()
        future_time = now + timedelta(seconds=Time)
        print("🕒 Next Trade Ad will be posted in:", Time / 60, "minutes", "Aka:", future_time.strftime("%H:%M"),"\n")
    
    elif res_TA.get("code") == 7105:
        print("⏳ Ad creation cooldown has not elapsed ⏳")

    elif res_TA.get("code") == 2:
        print("❌ Invalid Config! (Probably Tags or Requested Items) ❌")

    elif res_TA.get("code") == 7110:
        TotalRap = 0
        res_IL = requests.get(urlIL).json()
        if Top4 == False:
            for item_id in OfferedItems:
                item_str = str(item_id)
                item_data = res_IL["items"].get(item_str)
                if item_data:
                    TotalRap += item_data[2]
        elif Top4 == True:
            for item_id in Top4List:
                item_str = str(item_id)
                item_data = res_IL["items"].get(item_str)
                if item_data:
                    TotalRap += item_data[2]

        print("❌ Change your Robux! Robux number can't exceed 50% RAP ❌")
        print(f"📊 50% of Total RAP: {round(TotalRap/2)}")

    elif res_TA.get("code") == 5:
        print("❌ Invalid Rolimons Token! ❌")

    elif res_TA.get("code") == 7112:
        print("❌ Invalid Roblox User ID! ❌")

    elif res_TA.get("code") == 14:
        print("❌ 24-hour ad creation limit has been hit! ❌")
        
    elif res_TA.get("code") == 7104:
        print("❌ Player does not own all offered items! ❌")

    elif res_TA.get("code") == 7111:
        print("❌ Value of items on Requested side exceed value of items on Offered side! (Change requested items) ❌")

    else:
        print("❌ Something is not working! ❌")
        print("❌ Error message: ", res_TA.get("message"))
        print("❌ Error code: ", res_TA.get("code"))

    time.sleep(Time)
