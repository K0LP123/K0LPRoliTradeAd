#MADE BY K0LP (or K0LP7 on Roblox :P)
#REMEMBER TO CONFIGURE YOUR CONFIG

import requests
import json
import time
from datetime import datetime, timedelta


#CONFIG
#CONFIG
RolimonsToken = 'Paste your _RoliVerification= cookie here'
Robux = 0
OfferedItems = [1,2,3,4]
RequestedItems = [1,2,3,4] #Remember that tags also use slots in requests in trade ads!
PlayerId = 1067821187
Tags=["upgrade", "downgrade", "demand", "robux"]
   #"adds", "upgrade", "downgrade", "any", "wishlist", "demand", "rares", "rap", "robux", "projecteds"
Time=1470 #1470 seconds is 24 minutes and 30 seconds. Everyday you can post 60 trade ads so if you want it to run 24/7 I wouldnt set it lower than 1440
#CONFIG
#CONFIG

urlTA = 'https://api.rolimons.com/tradeads/v1/createad'
urlIL = 'https://api.rolimons.com/items/v2/itemdetails'

data = {
    "offer_item_ids": OfferedItems,
    "offer_robux": Robux,
    "player_id": PlayerId,
    "request_item_ids": RequestedItems,
    "request_tags": Tags
}

headers = {
    "content-type": "application/json",
    "cookie": "_RoliVerification=" + RolimonsToken
}

while True:
    responseTA = requests.post(urlTA, json=data, headers=headers)
    res_TA = responseTA.json()
    if res_TA.get("success") == True:
        print("✅ Trade ad Posted!✅")
        print("💲 Offered Robux:", Robux)
        responseIL = requests.get(urlIL)
        res_IL = responseIL.json()
        TotalValue = 0
        TotalRap = 0
        item_details = []
        for item_id in OfferedItems:
            item_str = str(item_id)
            item_data = res_IL["items"].get(item_str)
            if item_data:
                TotalValue += item_data[4]
                TotalRap += item_data[2]
                if item_data[1] == "":
                    item_details.append(f"- {item_data[0]} Item Value: {item_data[4]}")
                else:
                    item_details.append(f"- ({item_data[1]}) {item_data[0]}. Item Value: {item_data[4]}")
            else:
                item_details.append(f"- {item_id}: ❌ Item not found in Rolimons database?")

        print("📊 Total Value: ", TotalValue)
        print("📊 Total RAP: ", TotalRap)

        print("🔍 Offered Items:")
        for line in item_details:
            print(line)

        now = datetime.now()
        future_time = now + timedelta(seconds=Time)
        print("🕒 Next Trade Ad will be posted in:", Time / 60, "minutes", "Aka:", future_time.strftime("%H:%M")"\n")
    
    elif res_TA.get("code") == 7105:
        print("⏳ Ad creation cooldown has not elapsed ⏳")

    elif res_TA.get("code") == 2:
        print("❌ Invalid Config! (Probably Tags or Requested Items) ❌")

    elif res_TA.get("code") == 7110:
        TotalRap = 0
        responseIL = requests.get(urlIL)
        res_IL = responseIL.json()
        for item_id in OfferedItems:
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
        
    else:
        print("❌ Something is not working! ❌")
        print("❌ Error message: ", res_TA.get("message"))
        print("❌ Error code: ", res_TA.get("code"))
        print(data)

    time.sleep(Time)
