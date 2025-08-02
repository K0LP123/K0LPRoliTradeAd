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
AutoPick = True #True/False -- Picks top 4 of your items
NotForTrade = [21070012,21070012,21070012] #Items that wont appear in Trade Ads if you use AutoPick

#Manually set your items
OfferedItems = []

#Trade Ad options
Robux = 0
RequestedItems = []
PlayerId = 1067821187
Tags=["upgrade", "downgrade", "demand", "robux"]
   #"adds", "upgrade", "downgrade", "any", "wishlist", "demand", "rares", "rap", "robux", "projecteds"

#Time
Time=1500 #1500 seconds is 25 minutes (57,6 trade ads a day). Everyday you can post 60 trade ads so if you want it to run 24/7 I wouldnt set it lower than 1440

#CONFIG
#CONFIG

urlTA = 'https://api.rolimons.com/tradeads/v1/createad'
urlIL = 'https://api.rolimons.com/items/v2/itemdetails'
urlPI = f'https://inventory.roblox.com/v1/users/{PlayerId}/assets/collectibles?limit=100&sortOrder=Asc'

responsePI = requests.get(urlPI)
res_PI = responsePI.json()


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
    responseIL = requests.get(urlIL)
    res_IL = responseIL.json()
    if AutoPick == True:

        NotOnthold=[]
        ItemValues=[]

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
        AutopickFinalList = [item_id for item_id, _ in sorted(ItemValues, key=lambda x: x[1], reverse=True)[:4]]

        data["offer_item_ids"] = AutopickFinalList

        responseTA = requests.post(urlTA, json=data, headers=headers)            
        print("🤖 Auto Pick! 🤖")

    elif AutoPick == False:
        responseTA = requests.post(urlTA, json=data, headers=headers)

    res_TA = responseTA.json()
    if res_TA.get("success") == True:
        print("✅ Trade ad Posted!✅")
        TotalValue = 0
        TotalRap = 0
        OffItems = []

        if AutoPick == False:
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

        elif AutoPick == True:
            for item_id in AutopickFinalList:
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
        print("💲 Offered Robux:", Robux)
        
        if RequestedItems:
            ReqItems = []
            print("🔍 Requested Items:")
            for line in RequestedItems:
                item_str = str(line)
                item_data = res_IL["items"].get(item_str)
                if item_data[1] == "":
                    ReqItems.append(f"- {item_data[0]} | Item Value: {item_data[4]}")
                else:
                    ReqItems.append(f"- ({item_data[1]}) {item_data[0]} | Item Value: {item_data[4]}")

            for line in ReqItems:
                print(line)

        if Tags:
            print("🔍 Tags:")
            for line in Tags:
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
        if AutoPick == False:
            for item_id in OfferedItems:
                item_str = str(item_id)
                item_data = res_IL["items"].get(item_str)
                if item_data:
                    TotalRap += item_data[2]
        elif AutoPick == True:
            for item_id in AutopickFinalList:
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

    else:
        print("❌ Something is not working! ❌")
        print("❌ Error message: ", res_TA.get("message"))
        print("❌ Error code: ", res_TA.get("code"))

    time.sleep(Time)
