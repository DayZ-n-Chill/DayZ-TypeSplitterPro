# DayZ Type Splitter Pro

I've developed a custom script to manage and format the types.xml data for configuring DayZ's in-game economy. This script was created out of some minor dissatisfaction with existing tools that I felt lacked sufficient organization.

![Instructions](https://cdn.discordapp.com/attachments/1150169601649418250/1304275092544557086/new.png?ex=672ecc56&is=672d7ad6&hm=61f9497271756e0179470c66f4f97f5b6f9f99875bc15ce2d235200d2e2979d9&)

## What makes it pro?

Well, nothing really. It's nothing fancy or special. I just did not like how other splitters out there organized their files.

## What's the difference between yours and others?

Other splitters break down the basic categories but also leave an other.xml file or uncategorized.xml file. Within these files were types that I felt could be manually categorized. My version breaks these down into a few more categories and then also backs up your types.xml and adds the links to your new XML in the cfgeconomycore.xml for you.

### XML Created after the split

- ammo_boxes.xml
- ammo.xml
- animals.xml
- armbands.xml
- clothes.xml
- containers.xml
- contamination.xml
- explosives.xml
- flags.xml
- food.xml
- seasonal.xml
- staticObjs.xml
- tools.xml
- uncategorized.xml
- vehicleParts.xml
- vehicles.xml
- weapons.xml
- wrecks.xml
- zombies.xml

I do still have an uncategorized cause I don't know where to put the watchtower and the fence, but if you have suggestions, leave them in the comments.

Feel free to edit this as you need. It is free to use as you will. The file is in the workshop download.

## Requirements

- Python 3

## Usage

1. Place this in the same folder as your types.xml
2. Double click the typeSplitter.py file
3. Watch the magic and Enjoy!

### Alternate Usage

I use VS Code Python Extensions so I can just push F5 to run Batch and Python code. I recommend it.

## Join the Discord

For support with this or any of my other mods, join the [DayZ n' Chill - Official Discord](https://discord.gg).

## Additional Features and Updates

### Improved File Categorization

We've added more specific categories to reduce the need for a large uncategorized.xml file. This means fewer items left without a proper category, making the in-game economy easier to manage and understand. The tool now categorizes items more thoroughly, minimizing the need for manual adjustments.

### Automatic Backup and Configuration Update

The script now automatically creates a backup of your original types.xml file before making any changes. Additionally, it updates the cfgeconomycore.xml to include links to the newly split XML files, saving you the hassle of manually editing these references.

### Enhanced Logging

We've added enhanced logging to the script, which provides more detailed output during the splitting process. This allows you to see exactly what changes are being made, making troubleshooting easier if anything unexpected occurs.

### Customizable Categories

You can now customize the categories directly within the script. This flexibility allows you to add or modify categories based on your specific server setup, ensuring the tool fits your unique needs.

## Feedback and Suggestions

I'm always looking for ways to improve this tool. If you have ideas for categorizing items like the watchtower or fence, or if there are any new features you'd like to see, leave a comment or join the Discord to discuss!
