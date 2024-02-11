import discord
from discord import app_commands
from datetime import datetime
from datetime import timedelta
import pytz
import asyncio
import random
import os
import requests
import dotenv
import json
import time
import re
from blagues_api import BlaguesAPI
from blagues_api import BlagueType


#PATH

DEFAULT_PATH = os.getcwd() 

IMAGES_PATH = f"Images"

TEXT_PATH = f"Text_Files"

bot_mode_lc ="dev"
bot_mode_hc = "DEV"
bot_mode_def = "Dev"




def printer_timestamp():
   return datetime.now().strftime("\033[1;90m %Y-%m-%d %H:%M:%S \033[0m")

dotenv.load_dotenv(f"{DEFAULT_PATH}/Token/{bot_mode_lc}_bot.env")
token = os.getenv(f"{bot_mode_hc}_BOT_TOKEN")

global start_time
start_time = datetime.now()

print(f"\033[1m{printer_timestamp()} Token has been loaded ! \033[0m")

TGA25_ID = 845327664143532053


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all()) 
        self.synced = False 

client = aclient()

dotenv.load_dotenv(f"{DEFAULT_PATH}/Token/blagues_api.env")
blagues_token = os.getenv(f"Blagues_Token")

print(f"{printer_timestamp()} Blagues API token has been loaded !")

dotenv.load_dotenv(f"{DEFAULT_PATH}/Token/twitch_client_secret.env")
twitch_client_secret = os.getenv(f"Twitch_Secret")

print(f"{printer_timestamp()} Twitch secret token has been loaded !")

dotenv.load_dotenv(f"{DEFAULT_PATH}/Token/twitch_client_id.env")
twitch_client_id = os.getenv(f"Twitch_Client_Id")

print(f"{printer_timestamp()} Twitch client id token has been loaded !")


dotenv.load_dotenv(f"{DEFAULT_PATH}/Token/twitch_access_token.env")
twitch_access_token = os.getenv(f"Twitch_Access_Token")

print(f"{printer_timestamp()} Twitch access token has been loaded !")

url = 'https://id.twitch.tv/oauth2/token'
payload = {
    'client_id': twitch_client_id,
    'client_secret': twitch_client_secret,
    'grant_type': 'client_credentials'
}

async def check_shutdown_file():
    if os.path.isfile("shutdown.txt"):
        print(f"{printer_timestamp()} shutdown.txt file exist. \033[91m Bot is stopping... \033[0m")
        os.remove("shutdown.txt") 
        await client.close()
        await asyncio.sleep(5)  
        os._exit(0)
    else:
        print(f"{printer_timestamp()} shutdown.txt file doesn't exist. \033[94m Bot is starting... \033[0m")

asyncio.run(check_shutdown_file())

is_ready = False

@client.event
async def on_ready():
    await client.wait_until_ready()
    print(f"{printer_timestamp()} Bot ready !")

    try:
     bot_starting_embed = discord.Embed(
        title="**Lancement en cours... ⏳**",
        description="**Le bot est en train de démarrer. Veuillez patienter...**"

     )

     USER_DM = await client.fetch_user(TGA25_ID)
     message = await USER_DM.send(embed=bot_starting_embed)

     await tree.sync()
     print(f"{printer_timestamp()} Commands Synced !")

     print(f"{printer_timestamp()} Logged in as {client.user.name} !") 

     profile_image_path = f"{IMAGES_PATH}/Bot Logo/default_image_{bot_mode_lc}_bot.png"

     profile_image = open(profile_image_path, "rb")
     pfp = profile_image.read()
        
     await client.user.edit(avatar=pfp)

     print(f"{printer_timestamp()} Profile image sucessfully restablished to default !")

     
     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"/help | {version_number}"))
     print(f"{printer_timestamp()} Bot Status has been corectly set up !")

     asyncio.create_task(twitch_loop())
     print(f"{printer_timestamp()} Twitch loop has been corectly created ! ")

     # Open the JSON file and read its contents
     with open("JSON Files/Global Data/setup_data.json", 'r') as file:
      data = json.load(file)

     # Iterate over each entry in the setup data
     for entry in data:
      guild_id = entry["Guild Id"]
      guild_name = entry["Guild Name"]
      news_role_id = entry["Created Role Id"]
      channel_id = entry["Choosen Channel Id"]
      autorole_mesage_id = entry["Autorole Mesage Id"]

      if autorole_mesage_id == "":
        continue

      # Find the guild object
      guild = client.get_guild(guild_id)
      if guild is None:
        print(f"Guild with ID {guild_id} not found.")
        continue

      # Find the channel object
      channel = guild.get_channel(channel_id)
      if channel is None:
        print(f"Channel with ID {channel_id} not found in guild {guild.name}.")
        continue
      
      # Find the role object
      arabot_notif_role = guild.get_role(news_role_id)
      if arabot_notif_role is None:

        continue  

      # Find the mesage object
      old_mesage = await channel.fetch_message(autorole_mesage_id)
      await old_mesage.delete()

      # Give Role Embed
      give_role_embed = discord.Embed(
      title="**Auto Rôle**",
      description=f"Cliquez sur le bouton ci-dessous pour obtenir le rôle <@&{arabot_notif_role.id}>",
      color=discord.Color.from_rgb(3, 144, 252)
      )
      give_role_embed.add_field(name="A quoi ça sert ?", value=f"En obtenant le rôle <@&{arabot_notif_role.id}> vous êtes ainsi __abonnés__ aux *informations* concernant **l'Arabot**.")
      give_role_embed.set_footer(text=version_note)

      class ButtonView_give_roles(discord.ui.View):
       def __init__(self):
        super().__init__(timeout=None)

       @discord.ui.button(style=discord.ButtonStyle.green, label="Obtenir", custom_id="button_obtain", emoji="➕")
       async def button1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(arabot_notif_role.id)  # Get the role
        await interaction.user.add_roles(role)  # Add the role to the user

        given_autorole_embed = discord.Embed( 
        title="",
        description=f"{interaction.user.mention} tu as reçu le rôle <@&{arabot_notif_role.id}> !",
        color=discord.Color.from_rgb(3, 144, 252)        
        )

        await interaction.response.send_message(embed=given_autorole_embed, ephemeral=True)

       @discord.ui.button(style=discord.ButtonStyle.danger, label="Retirer", custom_id="button_remove", emoji="➖")
       async def button2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
         role = interaction.guild.get_role(arabot_notif_role.id)  # Get the role
         user = interaction.user  # Get the user who clicked the button

         await user.remove_roles(role)  # Remove the role from the user

         removed_autorole_embed = discord.Embed( 
         title="",
         description=f"{user.mention} le rôle <@&{arabot_notif_role.id}> t'as été retiré !",
         color=discord.Color.from_rgb(3, 144, 252)        
         )
         await interaction.response.send_message(embed=removed_autorole_embed, ephemeral=True)

      # Find the channel object
      channel = guild.get_channel(channel_id)

      new_mesage = await channel.send(embed=give_role_embed, view=ButtonView_give_roles())

      for entry in data:
       if entry.get("Guild Name") == guild_name:
        entry["Autorole Mesage Id"] = new_mesage.id
        break

      # Write the updated bot_setup_data to the JSON file
      with open("JSON Files/Global Data/setup_data.json", 'w') as file:
       json.dump(data, file)


      



    

     print(f"{printer_timestamp()} Twitch Loop starting in 30 seconds...")

     bot_started_embed = discord.Embed(
        title=":green_circle: Succès ! :green_circle:",
        description="**Le bot a correctement démarré !**\n*__(N'oubliez pas de relancer les commandes nécessaires...)__* "

     )

     await asyncio.sleep(3)

     await message.edit(embed=bot_started_embed)

     try:
      with open("JSON Files/Global Data/starting_time_average.json", 'r') as file:
        time_data = json.load(file)
     except FileNotFoundError:
      time_data = []

     end_time = datetime.now()
     time_taken = round((end_time - start_time).total_seconds(), 1)


     time_data.append({
     "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
     "time_taken": time_taken
     })

# Save the updated data back to the file
     with open("JSON Files/Global Data/starting_time_average.json", 'w') as file:
      json.dump(time_data, file)

     time_taken_values = [entry['time_taken'] for entry in time_data]

     average_time_taken = round(sum(time_taken_values) / len(time_taken_values), 1)

     

     print(f"{printer_timestamp()}\033[1;92m All startup operations have been completed in {time_taken}s ! \033[0m\033[1;35m(average is {average_time_taken}s)\033[0m")

     global is_ready
     is_ready = True

    except Exception as e:
       print(f"{printer_timestamp()} \033[1;91mAn error has occured during bot starting : \033[0m \033[91m{e} \033[0m")
       bot_start_error = discord.Embed(
          title="**:red_circle: Une erreur est survenue lors du démarage du bot :red_circle: **",
          description=f"**Detail de l'erreur :** `{e}` "
          
       )
       USER_DM = await client.fetch_user(TGA25_ID)
       await USER_DM.send(embed=bot_start_error)
       print(f"{printer_timestamp()} \033[1;34mWaiting....\033[0m")

       await asyncio.sleep(10)
       print(f"{printer_timestamp()} \033[1;33mBot stoping....\033[0m")

       await client.close()
       os._exit(0)
       

#BOT DISCONECT EVENT HANDLING

@client.event
async def on_disconnect():
    print(f"{printer_timestamp()} Bot disconnected. Reconnecting...")

    while not client.is_closed():
        try:
            await client.login(token)
            print(f"{printer_timestamp()} Reconnected successfully.")
            break
        except Exception as e:
            print(f"{printer_timestamp()} Reconnect failed. Retrying in 5 seconds... Error: {e}")
            await asyncio.sleep(30)


#VARIABLES   
         
restart_time = datetime.now()
tree = app_commands.CommandTree(client)
france_tz = pytz.timezone("Europe/Paris")
version_note = f"{bot_mode_def} Arabot v2.0 | Ink Corp |✨TGA25✨"
maintenance_mode = False
default_bot_nick = f"{bot_mode_def} Arabot"
version_number = "v2.0"

streamer_name = ("Locklear")

lock_icon_url = "https://i.postimg.cc/MTG44vm8/lock-icon.png"
clock12_icon_url = "https://i.postimg.cc/nrCysCX1/clock12-icon.png"
clock3_icon_url = "https://i.postimg.cc/SRFPKDpm/clock3-icon.png"
clock1230_icon_url = "https://i.postimg.cc/2yQKLhzh/clock1230-icon.png"
clock9_icon_url = "https://i.postimg.cc/7ZYWb5jJ/clock9-icon.png"
unlock_icon_url = "https://i.postimg.cc/X7gPVf10/unlock-icon.png"
trash_icon_url = "https://i.postimg.cc/1z6SZ7Fm/trash-icon.png"
tada_icon_url = "https://i.postimg.cc/zvrbZPGK/tada-icon.png"

def generate_current_time_timestamp():
   discord_current_time = datetime.now(france_tz)
   current_time_timestamp = int(discord_current_time.timestamp())
   return current_time_timestamp














explosion_command_avalaible = True
vol_command_avalaible = True

#ID'S VARIABLES

#TO MODIFY !!!!

goomink_news_channel_id = 1193954102670020648

            
bot_channel = 1120723328307581003



setup_command_id = 1184232293691293726

help_command_id = 1098204837612617731

explosion_command_id = 1119281805477036194

vol_command_id = 1119281805477036195

effacer_dm_command_id = 1184924715480006707

info_command_id = 1119281805477036197

dev_info_command_id = 1108432433830965340

admin_command_id = 1098204837612617733

conditions_command_id = 1190253770379120722

joke_command_id = 1201271328745992252

share_couscous_command_id = 1191482935258398774

server_info_command_id = 1190775361009635428

support_command_id = 1205262201229942795


#EVENTS

@client.event
async def on_message(message):
    couscous_trigger_pattern = re.compile(r"\b(?:tajine|couscous)\b", re.IGNORECASE)
    greeting_trigger_pattern = re.compile(r"\b(?:hi|hello|salut|bonjour|hey|helo|salu|salutation|salutations)\b", re.IGNORECASE)

    # Make sure the bot doesn't respond to its own messages
    if message.author == client.user:
        return

    # Check if any trigger word is present in the message content
    if couscous_trigger_pattern.search(message.content):
        # Add a reaction for couscous trigger
        await message.add_reaction("<:logo_python_arabot:1108367929457791116>")

    elif greeting_trigger_pattern.search(message.content):
        # Add a reaction for greeting trigger
        await message.add_reaction("👋")


try:
    with open("JSON Files/Global Data/welcome_data_file.json", 'r') as f:
        welcome_data = json.load(f)
except FileNotFoundError:
    welcome_data = {} 

def get_fallback_channel(guild):
    return discord.utils.get(guild.text_channels)

@client.event
async def on_guild_join(guild):
    guild_id = str(guild.id)

    welcome_embed = discord.Embed(
        title="Bonjour ! :wave:",
        description="",
        color=discord.Color.from_rgb(176, 68, 52)
    )
    welcome_embed.add_field(name="",value="Merci de m'avoir ajouté !", inline=False)

    welcome_embed.add_field(name="", value="", inline=False)

    welcome_embed.add_field(name="", value=f"Je suis un bot français mais avec quelques origines...\nJe possède plusieurs commandes, toutes visibles avec la commande </help:{help_command_id}>.", inline=False)

    welcome_embed.add_field(name="", value="", inline=False)

    welcome_embed.add_field(name="", value=f"**Avant de pouvoir m'utiliser merci de faire </setup:{setup_command_id}> pour lire les conditions d'utilisations et me configurer :smile:**", inline=False)
    welcome_embed.set_footer(text=version_note)

    # Check if the guild has already received the welcome message
    if guild_id not in welcome_data or not welcome_data[guild_id]:
        default_channel = guild.system_channel
        fallback_channel = get_fallback_channel(guild)  # Replace this with your logic to get a fallback channel
        
        # Define the welcome message variable outside of the if statement
        

        if default_channel:
            print(f"{printer_timestamp()} The bot has been added to the server {guild.name}. Welcome message sending to :{default_channel.name} ({default_channel.id})")

            await default_channel.send(embed=welcome_embed)

        elif fallback_channel:
            print(f"{printer_timestamp()} The bot has been added to the server {guild.name}. Welcome message sending to fallback channel: {fallback_channel.name} ({fallback_channel.id})")
            await fallback_channel.send(embed=welcome_embed)
        else:
            print(f"{printer_timestamp()} The bot has been added to the server {guild.name}: No default channel or fallback channel has been set. Unable to send welcome message...")

        # Mark the guild as having received the welcome message
        welcome_data[guild_id] = True

        # Save the updated data to the JSON file
        with open("JSON Files/welcome_data_file.json", "w") as f:
            json.dump(welcome_data, f, indent=2)
    


#EMBEDS

 #Help Embed
help_embed = discord.Embed(
        title="Help",
        description="Voici toutes mes commandes :",
        color=discord.Color.from_rgb(252, 165, 119)
)
help_embed.add_field(name=f"</explosion:{explosion_command_id}>", value="Fait exploser le serveur", inline=False)

help_embed.add_field(name=f"</vol:{vol_command_id}>", value="Vole le profil d'un membre du serveur", inline=False)

help_embed.add_field(name=f"</blague:{joke_command_id}>", value="Raconte une blague", inline=False) 

help_embed.add_field(name=f"</effacer-dm:{effacer_dm_command_id}>", value="Supprime tout les messages privés avec le bot", inline=False)

help_embed.add_field(name=f"</info:{info_command_id}>", value="Affiche les informations du bot", inline=False)

help_embed.add_field(name=f"</devinfo:{dev_info_command_id}>", value="Affiche des informations sur le développeur du bot", inline=False)

help_embed.add_field(name=f"</info-serveur:{server_info_command_id}>", value="Affiche des informations sur ce serveur", inline=False)

help_embed.add_field(name=f"</support:{support_command_id}>", value="Besoin d'aide ? Rejoignez le serveur support !", inline=False)

help_embed.add_field(name=f"</help:{help_command_id}>", value="Affiche ceci", inline=False)

help_embed.add_field(name=f"</conditions:{conditions_command_id}>", value="Affiche les conditions d'utilisation du bot", inline=False)

help_embed.add_field(name=f"</setup:{setup_command_id}>", value="Affiche l'interface de configuration du bot", inline=False)

help_embed.add_field(name=f"</admin:{admin_command_id}>", value="Affiche le panel d'administration du bot ***Commande réservée aux admins du bot***", inline=False)

help_embed.set_footer(text=version_note)

 #Warning Timeout Embed

warning_timeout_embed = discord.Embed(
    color=discord.Color.from_rgb(245, 129, 66)
        
)
warning_timeout_embed.add_field(name="Attention ! 🚨", value="Vous n'avez qu'**1 minute** pour utiliser les modules.")

 #Maintenance Embed

maintenance_embed = discord.Embed(
    title="**Maintenance 🚧**",
    description="Une maintenance est en cours...👷",
    color=discord.Color.from_rgb(240, 206, 17)
        
)
maintenance_embed.set_footer(text=version_note)

 #End Maintenance Embed

end_maintenance_embed = discord.Embed(
    title="**Fini ! :green_circle:**",
    description="La maintenance est maintenant terminée... :white_check_mark:",
    color=discord.Color.from_rgb(68, 242, 129)
        
)
end_maintenance_embed.set_footer(text=version_note)


 #Error Embed 

error_embed = discord.Embed(
    title="**Oups ! :face_with_monocle:**",
    description="Une erreur est survenue...",
    
    color=discord.Color.from_rgb(235, 64, 52)
        
)
error_embed.add_field(name= "L'erreur a été transmise au développeur :electric_plug:", value="*Ceci ne devrait pas arriver...*\nVous pouvez rejoindre le serveur support avec la commande `/support` !")
error_embed.set_footer(text=version_note)




 #Explosion Force Embed

explosion_force_embed = discord.Embed(
        title="Explosion",
        color=discord.Color.from_rgb(252, 165, 3)
        
)
explosion_force_embed.add_field(name="**Niveau 1 💣**", value="Rend inaccessible le serveur pendant 1 minute.", inline=False)
explosion_force_embed.add_field(name="**Niveau 2 🌋**", value="Rend inaccessible le serveur pendant 5 minutes.", inline=False)
explosion_force_embed.add_field(name="**Niveau 3 🌪️**", value="Rend inaccessible le serveur pendant 10 minutes.", inline=False)
explosion_force_embed.set_footer(text=version_note)

 #Dev Info Embed



dev_info_embed = discord.Embed(


        description="**Informations sur le developpeur du bot**",
        color=discord.Color.from_rgb(134, 27, 242)

        
        
)
dev_info_embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/845327664143532053/65a0b52e2a7b881a64c5769d8f12f359.png?size=512")
dev_info_embed.add_field(name="**Bonjour ! :wave: **", value="Moi c'est <@845327664143532053> <:activedevbadge:1107235074757373963>", inline=False)
dev_info_embed.add_field(name=f"**Développeur**", value="*Développeur Python <:logo_python_arabot:1108367929457791116>*", inline=True)
dev_info_embed.add_field(name="**Youtubeur** <:logo_youtube_arabot:1108368195489910836>", value="*Clique* [ici](https://www.youtube.com/channel/UCCxw1YVUMs5czQuhTkJH3eQ)", inline=True)
dev_info_embed.add_field(name="", value=":arrow_right_hook: [Rejoindre le serveur support](https://discord.gg/uGWkqYazzw) :leftwards_arrow_with_hook:  ", inline=False)
dev_info_embed.set_footer(text=version_note)

 #Command Unavalaible Embed

unavaileble_command_embed = discord.Embed(
   title="**Oups ! :face_with_monocle: **",
   description="Cette commande revient bientôt...",
   color=discord.Color.from_rgb(66, 135, 245),
   
)
unavaileble_command_embed.set_footer(text=version_note)


tos_not_accepted_embed = discord.Embed(
   title="Vous n'avez pas accepté les conditions d'utilisation !",
   description="*Pour utiliser le bot, veuillez les accepter en exécutant la commande* `/conditions`\n\n**Si vous préférez ne pas les accepter, vous ne pourrez pas utiliser les commandes** :x:",
   color=discord.Color.from_rgb(66, 135, 245),
   
)
tos_not_accepted_embed.add_field(name="", value="*Dura lex sed lex (La loi est dure, mais c'est la loi)*")
tos_not_accepted_embed.set_footer(text=version_note)


tos_embed = discord.Embed(
   title="🤖 Conditions d'utilisation 🤖",
   description="*Veuillez lire attentivement ce qui suit :*",
   color=discord.Color.from_rgb(66, 135, 245),
   
)
tos_embed.add_field
tos_embed.add_field(name="__1-Utilisation conforme__", value="*Vous êtes responsable de l'utilisation de l'Arabot de manière conforme aux règlements en vigueur. Nous déclinons toute responsabilité en cas d'utilisation inappropriée du bot.* 🤖❌", inline=True)
tos_embed.add_field(name="__2-Respect d'autrui__", value="*Utilisez les commandes de manière respectueuse et évitez tout contenu offensant. Gardez à l'esprit que l'humour au second degré ne doit pas franchir les limites du respect.* 🤝", inline=True)
tos_embed.add_field(name="__3-Bot humoristique__", value="*Le bot a été créé dans une optique satirique visant à ridiculiser les stéréotypes absurdes. L'utilisation de l'Arabot dans ce contexte satirique implique une compréhension du second degré et de l'objectif de dénonciation des stéréotypes stupides.* 🤔", inline=True)
tos_embed.add_field(name="__4-Changements possibles__", value="*Parfois, quelques ajustements sont nécessaires. Restez informé en consultant nos annonces sur le [serveur support.](https://discord.gg/uGWkqYazzw)* 🛠️📢", inline=True)
tos_embed.add_field(name="__5-Utilisation de l'Arabot__", value="**En acceptant ces termes, vous adhérez aux règles.**\n*Si celles-ci ne correspondent pas à vos attentes, aucun problème. Cependant, vous ne devriez pas utiliser l'Arabot. *⚠️", inline=False)

tos_embed.set_footer(text=version_note)


#BUTTON VIEWS

 #Button View Delete Bot
        

 #Button View Status

class ButtonView_status(discord.ui.View):
    def __init__(self, message):
        super().__init__(timeout=None)
        self.message = message
        

#En ligne

    @discord.ui.button(style=discord.ButtonStyle.primary, label="En ligne", custom_id="button1", emoji="🟢")
    async def button1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(content="Statut du bot : **En ligne**", ephemeral=True)
        await client.change_presence(status=discord.Status.online)
#Inactif

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Inactif", custom_id="button2", emoji="🌙")
    async def button2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(content="Statut du bot : **Inactif**", ephemeral=True)
        await client.change_presence(status=discord.Status.idle)
#Ne pas deranger

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Ne pas déranger", custom_id="button3", emoji="🔕")
    async def button3_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(content="Statut du bot : **Ne pas déranger**", ephemeral=True)
        await client.change_presence(status=discord.Status.dnd) 

#Hors ligne

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Hors ligne", custom_id="button4", emoji="❌")
    async def button4_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(content="Statut du bot : **Hors ligne**", ephemeral=True)
        await client.change_presence(status=discord.Status.offline)                 

#Invisible

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Invisible", custom_id="button5", emoji="👻")
    async def button5_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(content="Statut du bot : **Invisible**", ephemeral=True)
        await client.change_presence(status=discord.Status.invisible)  

 
   
             
 #Button View Parameters

class ButtonView_settings(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)
        self.bot = client

    @discord.ui.button(style=discord.ButtonStyle.danger, label="Supprimer le bot", custom_id="delete_bot_button")
    async def button_delete_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content="**Êtes-vous sûr ?** (Le bot pourra être ajouté à nouveau avec un lien d'invitation)\nRépondez `oui` pour supprimer le bot de ce serveur. :grey_question:", ephemeral=True, delete_after=35)

        try:
            confirm_response = await self.bot.wait_for(
                "message",
                check=lambda m: m.author == interaction.user and m.channel == interaction.channel,
                timeout=30  # You can adjust the timeout duration
            )

            if confirm_response.content.lower() == "oui":
                # Delete the bot from the server
               await confirm_response.delete()
               print(f"{printer_timestamp()} Bot deleted from server: {interaction.guild.name} ({interaction.guild.id})")
               await interaction.edit_original_response(content="**Le bot a bien été supprimé... **:cry:")

               await interaction.guild.leave()
                
            else:
                await interaction.edit_original_response(content="**Opération annulée...** :x:")
                await confirm_response.delete()
        
        except asyncio.TimeoutError:
            await interaction.edit_original_response(content="***Temps écoulé.*** Veuillez réessayer. :alarm_clock:")    
        

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Réinitialiser le profil", custom_id="button_reset", emoji="🔄")
    async def button1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot_user = interaction.guild.me
        await bot_user.edit(nick=None)


        default_profile_image_path = f"{IMAGES_PATH}/Bot Logo/default_image_{bot_mode_lc}_bot.png"

        default_profile_image = open(default_profile_image_path, "rb")
        pfp = default_profile_image.read()
        
        await client.user.edit(avatar=pfp)
        await interaction.response.send_message("Le profil du bot a été réinitialisé. ✅", ephemeral=False)

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Arrêt", custom_id="button_shutdown", emoji="🔴")
    async def button2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
     user = interaction.user
     await interaction.response.defer()
     filename = "shutdown.txt"
     with open(filename, 'w') as f:
        pass   
     await asyncio.sleep(1)
     await interaction.message.edit(content="⬜⬜⬜⬜", view=self)
     await asyncio.sleep(1)
     await interaction.message.edit(content="🟩⬜⬜⬜", view=self)
     await asyncio.sleep(1)
     await interaction.message.edit(content="🟩🟩⬜⬜", view=self)
     await asyncio.sleep(1)
     await interaction.message.edit(content="🟩🟩🟩⬜", view=self)
     await asyncio.sleep(1)
     await interaction.message.edit(content="🟩🟩🟩🟩", view=self)
  
     await asyncio.sleep(5)
     await interaction.message.edit(content="☠️", view=self)
     await asyncio.sleep(2)

     print(f"The bot has been stopped by {user.name} !")

     await client.close()
     os._exit(0) 

     

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Maintenance", custom_id="button_maintenance", emoji="🚧")
    async def button3_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        global maintenance_mode
        maintenance_mode=True
        await interaction.response.send_message("Mode maintenance **activé** 👷 !", ephemeral=True)
        await client.change_presence(activity=discord.Activity(status=discord.Status.do_not_disturb ,name="la maintenance 👷", type=discord.ActivityType.watching))

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Fin de la maintenance", custom_id="button_end_maintenance", emoji="🛠️")
    async def button4_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
     await interaction.response.send_message("Mode maintenance **désactivé** 👷 !", ephemeral=True)

     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="de retour...🎉"))  
          
     await asyncio.sleep(10)
     global maintenance_mode
     maintenance_mode=False

     # Open the JSON file and read its contents
     with open("JSON Files/Global Data/setup_data.json", 'r') as file:
      data = json.load(file)

     # Iterate over each entry in the setup data
     for entry in data:
      guild_id = entry["Guild Id"]
      channel_id = entry["Choosen Channel Id"]
      news_role_id = entry["Created Role Id"]

      # Find the guild object
      guild = client.get_guild(guild_id)
      if guild is None:
        print(f"Guild with ID {guild_id} not found.")
        continue

      # Find the channel object
      channel = guild.get_channel(channel_id)
      if channel is None:
        print(f"Channel with ID {channel_id} not found in guild {guild.name}.")
        continue

      # Find the role object
      role = guild.get_role(news_role_id)
      if role is None:
        print(f"The news role was not found in guild {guild.name}.")
        continue    

      # Sending message to the channel
      await channel.send(f"{role.mention}", embed=end_maintenance_embed)
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"/help | {version_number}"))

     # Update presence outside the loop
     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"/help | {version_number}"))




 #Button View Explosion Command
class ButtonView_explosion_command(discord.ui.View):
    def __init__(self):
        super().__init__()


#--------------------------------------------------------
#BUTTON LEVEL 1
#--------------------------------------------------------

    @discord.ui.button(style=discord.ButtonStyle.primary, label="1", custom_id="force1", emoji="💣")
    async def button1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        choosen_level = 1

        view = self
        for child in view.children:
         child.disabled = True

        await interaction.response.edit_message(view=view)

        await asyncio.sleep(1)
        
        await interaction.message.add_reaction("💣")

        data = {
        "guild_id": guild.id,
        "guild_name": guild.name,
        "choosen_level": choosen_level ,
        "username_button_pressed": interaction.user.mention
        }

# Specify the file name
        file_name = "JSON Files/Explosion_Command_Data/level_info_explosion_command.json"

# Write data to the JSON file
        with open(file_name, 'w') as json_file:
         json.dump(data, json_file)

        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Explosion system launching...")
        await explosion_command_system(interaction)

#--------------------------------------------------------
#BUTTON LEVEL 2
#--------------------------------------------------------
          
    @discord.ui.button(style=discord.ButtonStyle.primary, label="2", custom_id="force2", emoji="🌋")
    async def button2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
     guild = interaction.guild
      
     choosen_level = 2

     view = self
     for child in view.children:
        child.disabled = True

     await interaction.response.edit_message(view=view)

     await asyncio.sleep(1)
        
     await interaction.message.add_reaction("🌋")

     data = {
     "guild_id": guild.id,
     "guild_name": guild.name,
     "choosen_level": choosen_level ,
     "username_button_pressed": interaction.user.mention
     }

# Write data to the JSON file
     file_name = "JSON Files/Explosion_Command_Data/level_info_explosion_command.json"
     with open(file_name, 'w') as json_file:
        json.dump(data, json_file)
     print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Explosion system launching...")
     await explosion_command_system(interaction)

   
#--------------------------------------------------------
#BUTTON LEVEL 3
#-------------------------------------------------------- 

    @discord.ui.button(style=discord.ButtonStyle.primary, label="3", custom_id="force3", emoji="🌪️")
    async def button3_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
             guild = interaction.guild
             choosen_level = 3

             view = self
             for child in view.children:
               child.disabled = True

             await interaction.response.edit_message(view=view)

             await asyncio.sleep(1)
        
             await interaction.message.add_reaction("🌪️")

             data = {
             "guild_id": guild.id,
             "guild_name": guild.name,
             "choosen_level": choosen_level ,
             "username_button_pressed": interaction.user.mention
             }

             file_name = "JSON Files/Explosion_Command_Data/level_info_explosion_command.json"


             with open(file_name, 'w') as json_file:
              json.dump(data, json_file)
             print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Explosion system launching...")
             await explosion_command_system(interaction)

 #Button View Roles Give




class ButtonView_setup_tos(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    custom_accept_emoji = discord.PartialEmoji(name="rules_logo", id=1190051921365573803, animated=False)
    custom_refuse_emoji = discord.PartialEmoji(name="refuse_logo", id=1189625708838916207, animated=False)

    @discord.ui.button(style=discord.ButtonStyle.green, label="J'ai lu et j'accepte", custom_id="button_accept_tos", emoji=custom_accept_emoji)
    async def button_accept_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"{printer_timestamp()} {interaction.user.global_name} {interaction.user.id} TOS have been accepted !")
        await interaction.response.send_message(content="Vous avez accepté les conditions d'utilisation...\nMerci ! :grin:", ephemeral=True)

        tos_data = {interaction.user.id: {"accepted_tos": True}}

        with open("JSON Files/Global Data/TOS_info_data.json", 'w') as f:
            json.dump(tos_data, f)

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Je refuse", custom_id="button_deny_tos", emoji=custom_refuse_emoji)
    async def button_refuse_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(f"{printer_timestamp()} {interaction.user.global_name} {interaction.user.id} TOS have been denied...")
        await interaction.response.send_message(content="Vous avez refusé les conditions d'utilisation... :x:", ephemeral=True)

        tos_data = {interaction.user.id: {"accepted_tos": False}}

        with open("JSON Files/Global Data/TOS_info_data.json", 'w') as f:
            json.dump(tos_data, f)


   



#SELECT VIEWS  

class TESTSelectMenu(discord.ui.View):
    def __init__(self, roles):
        super().__init__(timeout=None)

        
       
        self.roles = roles

        # Create a select dropdown with role options
        self.select = discord.ui.Select(placeholder="Select a role", options=[
                discord.SelectOption(label=role.name, value=str(role.id)) for role in roles
        ])
            
        # Add the select dropdown to the view
        self.add_item(self.select)

       

    async def select_callback(self, component: discord.ui.Select):
        selected_role_id = int(component.values[0])
        selected_role = discord.utils.get(self.roles, id=selected_role_id)

        if selected_role:
            # Perform actions with the selected role
            print(f"You have selected role {selected_role}.")
        else:
            print("Error")



 #Select Admin Menu

# Create the embed


class AdminSelectMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)



 
        options = [
            discord.SelectOption(label="Statuts", value="status_embed_option", emoji="🟢"),
            discord.SelectOption(label="Paramètres", value="parameters_embed_option", emoji="⚙️"),
            discord.SelectOption(label="Informations", value="information_embed_option", emoji="ℹ️"),
          
        ]
        
        select = discord.ui.Select(options=options, placeholder="Options d'administration", min_values=1, max_values=1)
        select.callback = self.select_callback
        self.add_item(select)

    

    
    async def select_callback(self, interaction):
        
          
        
        info_embed1 = discord.Embed(
        title="Infos",
        color=discord.Color.from_rgb(60, 240, 132)
        )
        info_embed1.add_field(name="**Ping 🏓**", value=f"*{round(client.latency, 2)}* ms de latence", inline=False)
        info_embed1.add_field(name="**Date & Heure 🕐**", value=f"Nous sommes le <t:{generate_current_time_timestamp()}:D> et il est <t:{generate_current_time_timestamp()}:t>", inline=False)
        info_embed1.add_field(name="**Dernier redémarrage 🔄**", value=f"<t:{int(restart_time.timestamp())}>", inline=False) # Bot restart date and time field
        info_embed1.add_field(name="**Langage de programmation 🌐**", value="*Python* <:logo_python_arabot:1108367929457791116>", inline=False) # Bot restart date and time field
        info_embed1.set_footer(text=version_note)

        selected_option = interaction.data['values'][0]

        if selected_option == "status_embed_option":
            await interaction.response.edit_message(content="Modifiez le **statut** du bot :")
            await interaction.channel.send(view=ButtonView_status(interaction))
            
            

        elif selected_option == "parameters_embed_option":
            await interaction.response.edit_message(content="Modifiez les **parametres** du bot :")
            await interaction.channel.send(view=ButtonView_settings(interaction))

        else:

         await interaction.response.send_message(embed=info_embed1, ephemeral=True)

                


#COMMANDS

@tree.command(name="blague", description="Raconte une blague")
async def test_command(interaction: discord.Interaction):
            with open("JSON Files/Global Data/TOS_info_data.json", 'r') as json_file:
              loaded_data = json.load(json_file)

            # Extract relevant data from loaded JSON using the specific guild ID
            user_id = str(interaction.user.id)
            user_data = loaded_data.get(user_id, {})
            is_tos_accepted = loaded_data.get(user_id, {}).get("accepted_tos", False)

            if not user_data:
              await interaction.response.send_message(content="Faites `/conditions` et réessayez !",ephemeral=True)
            else:
              if not is_tos_accepted:    
               await interaction.response.send_message(embed=tos_not_accepted_embed, ephemeral=True)
              else:  
                blagues = BlaguesAPI(blagues_token)

                blague = await blagues.random(disallow=[BlagueType.GLOBAL, BlagueType.DEV])

                joke = blague.joke
                answer = blague.answer
                type_blague = blague.type

                hc_type_blague = type_blague[0].upper() + type_blague[1:]

                joke_embed = discord.Embed(
                 title="",
                 description="",
                 color=discord.Color.from_rgb(60, 240, 132)
                )
                joke_embed.add_field(name=f"{joke}", value=f"||{answer}||")
                joke_embed.set_footer(text=f"{hc_type_blague} • Demandé à {datetime.now(france_tz).strftime('%H:%M')} par {interaction.user.global_name} | BlaguesAPI")

                await interaction.response.send_message(embed=joke_embed)

@tree.command(name="couscous", description="Partage un couscous avec quelqu'un")
async def share_couscous_command(interaction: discord.Interaction, utilisateur: discord.User):
            if isinstance(interaction.channel, discord.DMChannel):
             await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les dm ! :no_entry_sign:", ephemeral=True)
            else:

             with open("JSON Files/Global Data/TOS_info_data.json", 'r') as json_file:
              loaded_data = json.load(json_file)

             # Extract relevant data from loaded JSON using the specific guild ID
             user_id = str(interaction.user.id)
             user_data = loaded_data.get(user_id, {})
             is_tos_accepted = loaded_data.get(user_id, {}).get("accepted_tos", False)

             if not user_data:
              await interaction.response.send_message(content="Faites `/conditions` et réessayez !",ephemeral=True)
             else:
              if not is_tos_accepted:    
               await interaction.response.send_message(embed=tos_not_accepted_embed, ephemeral=True)
              else:
                 #
                 couscous_gifs = [
                 "https://i.postimg.cc/0NzhwZ0T/couscous-gif-01.gif",
                 "https://i.postimg.cc/wM4GMmsq/couscous-gif-02.gif",
                 "https://i.postimg.cc/bv8cK1xW/couscous-gif-03.gif",
                 "https://i.postimg.cc/rs9QRt00/couscous-gif-04.gif"
                 ]

                 random_couscous_gif = random.choice(couscous_gifs)
                 # Create random messages
                 random_messages = [
                 f"**{interaction.user.global_name}** partage un succulent couscous avec toi !\nBon appétit ! 🍲",
                 f"**{interaction.user.global_name}** t'offre un délicieux couscous.\nProfitez-en ! 🌟",
                 f"**{interaction.user.global_name}** a préparé un couscous spécial pour toi.\nC'est l'heure du festin ! 🎉",
                 f"**{interaction.user.global_name}** et **{utilisateur.global_name}** savourent un couscous ensemble.\nQuelqu'un veut la recette ! 📖",
                 ]

                 random_message = random.choice(random_messages)

                 # Create an embed for the couscous
                 couscous_embed = discord.Embed(
                    title="",
                    color=discord.Color.green()
                 )
                 couscous_embed.add_field(name="", value=random_message)
                 couscous_embed.set_image(url=random_couscous_gif)
                 couscous_embed.set_footer(text=version_note)

                 if utilisateur.bot:
                    no_couscous_bot_embed = discord.Embed(
                    title="",
                    description="**Pas sûr que les robots aiment le couscous...** 🤖🍲",
                    color=discord.Color.orange()
                    )
                    await interaction.response.send_message(embed=no_couscous_bot_embed, ephemeral=True)
                 else:
                    # Send the couscous embed with the random message
                    await interaction.response.send_message(content=utilisateur.mention,embed=couscous_embed)
   
          

@tree.command(name="info-serveur", description="Affiche les informations du serveur")
async def server_info(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les dm ! :no_entry_sign:", ephemeral=True)
    else:
        with open("JSON Files/Global Data/TOS_info_data.json", 'r') as json_file:
            loaded_data = json.load(json_file)

        # Extract relevant data from loaded JSON using the specific guild ID
        user_id = str(interaction.user.id)
        user_data = loaded_data.get(user_id, {})
        is_tos_accepted = loaded_data.get(user_id, {}).get("accepted_tos", False)

        if not user_data:
            await interaction.response.send_message(content="Faites `/conditions` et réessayez !",ephemeral=True)
        else:

         if not is_tos_accepted:
            await interaction.response.send_message(embed=tos_not_accepted_embed, ephemeral=True)
         else:
             #
            if interaction.guild.premium_tier == 0:
             guild_boost_level = f"Aucun boost"

            elif interaction.guild.premium_tier == 1:
             guild_boost_level = f"Niveau 1 {interaction.guild.premium_subscription_count} boost(s)"

            elif interaction.guild.premium_tier == 2:
             guild_boost_level = f"Niveau 2 {interaction.guild.premium_subscription_count} boost(s)"

            elif interaction.guild.premium_tier == 3:
             guild_boost_level = f"Niveau 3 {interaction.guild.premium_subscription_count} boost(s)"             

            bot_members = [member for member in interaction.guild.members if member.bot]
            server_stat_embed = discord.Embed(
            title="Quelques infos sur ce serveur :information_source:",
        
            description=f"*__{interaction.guild.name} ({interaction.guild.id})__*\n**{len(interaction.guild.channels)} salons • {len(interaction.guild.threads)} fils • {len(interaction.guild.roles)} roles • {len(bot_members)} bots**",
            color=discord.Color.from_rgb(3, 165, 252)
            )
            server_stat_embed.set_thumbnail(url=interaction.guild.icon)

            server_stat_embed.add_field(name="Membres :", value=interaction.guild.member_count, inline=True)

            server_stat_embed.add_field(name="Propriétaire :", value=f"<@{interaction.guild.owner.id}>", inline=True)

            server_stat_embed.add_field(name="Boost :", value=guild_boost_level)

            server_stat_embed.add_field(name="Création du serveur", value=f"<t:{int(interaction.guild.created_at.timestamp())}:F>")

            bot_member = interaction.guild.get_member(client.user.id)

            server_stat_embed.add_field(name="Date d'ajout de l'Arabot :", value=f"<t:{(int(bot_member.joined_at.timestamp()))}:F>")
                      
            server_stat_embed.set_footer(text=version_note)

            await interaction.response.send_message(embed=server_stat_embed)


@tree.command(name="support", description="Besoin d'aide ? Rejoignez le serveur support !")
async def support_command(interaction: discord.Interaction):

    class ButtonView_support(discord.ui.View):                
        def __init__(self):
            super().__init__(timeout=None)

            super().add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="Serveur Support", url="https://discord.com/invite/uGWkqYazzw"))

    await interaction.response.send_message("Cliquez [ici](https://discord.com/invite/uGWkqYazzw) pour rejoindre le serveur support.", view=ButtonView_support(), ephemeral=True)



@tree.command(name="setup", description="Configuration du bot")
async def setup(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les dm ! :no_entry_sign:", ephemeral=True)
    else:
        with open("JSON Files/Global Data/TOS_info_data.json", 'r') as json_file:
            loaded_data = json.load(json_file)

        # Extract relevant data from loaded JSON using the specific guild ID
        user_id = str(interaction.user.id)
        user_data = loaded_data.get(user_id, {})
        is_tos_accepted = loaded_data.get(user_id, {}).get("accepted_tos", False)

        if not user_data:
            await interaction.response.send_message(content="Faites `/conditions` et réessayez !", ephemeral=True)
        else:
            if not is_tos_accepted:
                await interaction.response.send_message(embed=tos_not_accepted_embed, ephemeral=True)
            else:
                test_embed = discord.Embed(
                    title="Configuration du bot",
                    description= f"**Seules les personnes avec la permission** `Administrateur` **sont autorisées à configurer le bot.**\n\n*Vérifiez que vous possédez cette permission et appuyez sur* **Commencer**",
                    color=discord.Color.from_rgb(252, 165, 119)
                )

                class ButtonView_test(discord.ui.View):
                    def __init__(self, interaction: discord.Interaction):
                        super().__init__(timeout=None)
                        self.bot = interaction.client

                    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Commencer", custom_id="start", disabled=False)
                    async def button_start_callback(self, interaction: discord.Interaction, button):
                        try:
                            with open("JSON Files/Global Data/setup_data.json", 'r') as file:
                                global bot_setup_data
                                bot_setup_data = json.load(file)
                        except FileNotFoundError:
                            bot_setup_data = []  

                        print("Start")

                        guild = interaction.guild
                        admin_role_ids = [role.id for role in guild.roles if role.permissions.administrator and not role.managed]

                        if admin_role_ids:
                            role_mentions = [f"<@&{role_id}>" for role_id in admin_role_ids]
                            roles = ', '.join(role_mentions)
                        else:
                            print("No non-bot roles found with 'Admin' permission.")

                        # Update embed title and description
                        test_embed.title = "1/4 Configuration du bot"

                        user = interaction.user

                        admin_role_ids = [role.id for role in guild.roles if role.permissions.administrator and not role.managed]

                        has_admin_role = any(role.id in admin_role_ids for role in user.roles)

                        global guild_name
                        global guild_id
                        global setup_user_name
                        global setup_user_id

                        guild_name = interaction.guild.name
                        guild_id = interaction.guild.id
                        setup_user_name = interaction.user.global_name
                        setup_user_id = interaction.user.id

                        if guild_name not in [entry.get("Guild Name") for entry in bot_setup_data]:
                            bot_setup_data.append({
                                "Guild Name": guild_name,
                                "Guild Id": guild_id,
                                "Setup User Info": f"{setup_user_name} {setup_user_id}",
                                "Timestamp": datetime.now(france_tz).strftime("%Y-%m-%d %H:%M:%S"),
                                "Status": "Started",
                                "Choosen Channel Name": "",
                                "Choosen Channel Id": "",
                                "Created Role Id": "",
                                "Autorole Mesage Id": "",
                            })

                        with open("JSON Files/Global Data/setup_data.json", 'w') as file:
                            json.dump(bot_setup_data, file)

                        if not has_admin_role:
                            test_embed.description  =f"**Vous n'avez pas les permissions nécessaires !**\n\n*Veuillez demander à un utilisateur avec le(s) role(s) :*\n{roles}"
                            for entry in bot_setup_data:
                                if entry.get("Guild Name") == guild_name:
                                    entry["Status"] = "Admin Error"
                                    entry["Timestamp"] = datetime.now(france_tz).strftime("%Y-%m-%d %H:%M:%S")
                                    break  # Exit loop once the entry is found and updated  
                        else:
                            print("roles ok")
                            for entry in bot_setup_data:
                                if entry.get("Guild Name") == guild_name:
                                    entry["Status"] = "Admin Role Finished"
                                    entry["Timestamp"] = datetime.now(france_tz).strftime("%Y-%m-%d %H:%M:%S")
                                    break  # Exit loop once the entry is found and updated

                            # Hide the "Commencer" button
                            start_button = self.children[0]
                            start_button.disabled = True
                            start_button.style = discord.ButtonStyle.green

                            # Show the "Etape 1" button
                            step_1_button = self.children[1]
                            step_1_button.disabled = False
                            step_1_button.style = discord.ButtonStyle.blurple

                            test_embed.title = "1/4 Configuration du bot"
                            test_embed.description = "Pour que le bot fonctionne correctement, il a besoin d'être en haut de la liste des rôles.\n\nPlacez-le en haut puis cliquez sur **Vérifier**"

                        # Write the updated bot_setup_data to the JSON file
                        with open("JSON Files/Global Data/setup_data.json", 'w') as file:
                            json.dump(bot_setup_data, file)

                        await interaction.response.edit_message(view=self, embed=test_embed)

                    @discord.ui.button(style=discord.ButtonStyle.grey, label="Vérifier", custom_id="step_1", disabled=True)
                    async def button_step_1_callback(self, interaction: discord.Interaction, button):

                        bot_member = client.user.name

                        highest_role = interaction.guild.roles[-1].name

                        if highest_role != bot_member:
                            print(highest_role)
                            print(bot_member)
                            print("Bot's role is not on top of the role list.")
                            test_embed.description = f"Le bot n'est pas en haut de la liste !\n\nVeuillez réessayer..."

                            for entry in bot_setup_data:
                                if entry.get("Guild Name") == guild_name:
                                    entry["Status"] = "Top Role List Error"
                                    entry["Timestamp"] = datetime.now(france_tz).strftime("%Y-%m-%d %H:%M")
                                    break  # Exit loop once the entry is found and updated
                        elif highest_role == bot_member:
                            test_embed.title = "2/4 Configuration du bot"
                            test_embed.description = "Veuillez cliquer sur le bouton ci-dessous puis envoyer un salon."

                            step_1_button = self.children[1]
                            step_1_button.disabled = True
                            step_1_button.style = discord.ButtonStyle.green

                            step_2_button = self.children[2]
                            step_2_button.disabled = False
                            step_2_button.style = discord.ButtonStyle.blurple

                            for entry in bot_setup_data:
                                if entry.get("Guild Name") == guild_name:
                                    entry["Status"] = "Top Role List Finished"
                                    entry["Timestamp"] = datetime.now(france_tz).strftime("%Y-%m-%d %H:%M:%S")
                                    break  # Exit loop once the entry is found and updated  

                        # Write the updated bot_setup_data to the JSON file
                        with open("JSON Files/Global Data/setup_data.json", 'w') as file:
                            json.dump(bot_setup_data, file)
                        await interaction.response.edit_message(view=self, embed=test_embed)

                    @discord.ui.button(style=discord.ButtonStyle.grey, label="Choisir un salon", custom_id="step_2", disabled=True)
                    async def button_step_2_callback(self, interaction: discord.Interaction, button):
                        print("Step 2")
                        class Feedback(discord.ui.Modal, title="Choix du salon"):
                            channel_get_name = discord.ui.TextInput(
                                label="Salon",
                                placeholder="nom du salon",
                                required=False,
                            )

                            async def on_submit(self2, interaction: discord.Interaction):
                                guild = interaction.guild
                                choosen_channel = self2.channel_get_name.value

                                global choosen_channel_global_info
                                choosen_channel_global_info = discord.utils.get(guild.channels, name=choosen_channel)

                                if choosen_channel_global_info is None or not isinstance(choosen_channel_global_info, discord.TextChannel):
                                    print(f"**Opération annulée. Le salon spécifié est invalide.** :x:")
                                    test_embed.description = f"**Veuillez réessayer.\nLe salon spécifié est invalide.** :x:"
                                else:
                                    choosen_channel_id = int(choosen_channel_global_info.id)
                                    print(choosen_channel_id)

                                if choosen_channel_global_info and isinstance(choosen_channel_global_info, discord.TextChannel):
                                    print(f"User provided a valid channel: {choosen_channel_global_info.mention}")
                                    # Iterate over each entry in the setup data
                                    for entry in bot_setup_data:
                                     guild_id = entry["Guild Id"]
                                     guild_name = entry["Guild Name"]
                                     news_role_id = entry["Created Role Id"]
                                     channel_id = entry["Choosen Channel Id"]
                                     autorole_mesage_id = entry["Autorole Mesage Id"]

                                     if autorole_mesage_id == "":
                                      continue

                                     # Find the guild object
                                     guild = client.get_guild(guild_id) #Probleme , salon choisi est different , bot trouve pas message, mauvais salon , meme problleme on_startup
                                     if guild is None:
                                      print(f"Guild with ID {guild_id} not found.")
                                      continue

                                     # Find the channel object
                                     channel = guild.get_channel(channel_id)
                                     if channel is None:
                                      print(f"Channel with ID {channel_id} not found in guild {guild.name}.")
                                      continue
      
                                     # Find the mesage object
                                     old_mesage = await channel.fetch_message(autorole_mesage_id)
                                     if old_mesage is None:
                                        print(f"Message with ID {autorole_mesage_id} not found in guild {guild.name}.")
                                     else:    
                                      await old_mesage.delete()


                                    for entry in bot_setup_data:
                                        if entry.get("Guild Name") == guild_name:
                                            entry["Status"] = "Choosen channel Finished"
                                            entry["Timestamp"] = datetime.now(france_tz).strftime("%Y-%m-%d %H:%M:%S")
                                            entry["Choosen Channel Name"] = choosen_channel_global_info.name
                                            entry["Choosen Channel Id"] = choosen_channel_global_info.id

                                            break  # Exit loop once the entry is found and updated

                                    # Hide the "Etape 2" button
                                    step_2_button = self.children[2]
                                    step_2_button.disabled = True
                                    step_2_button.style = discord.ButtonStyle.green

                                    step_3_button = self.children[3]
                                    step_3_button.disabled = False
                                    step_3_button.style = discord.ButtonStyle.blurple

                                    test_embed.title = f"3/4 Configuration du bot"
                                    test_embed.description = f"Cliquez sur le bouton ci-dessous pour créer un rôle pour être informé des modifications du bot."

                                else:
                                    print(f"**Veuillez réessayer. Le canal spécifié est invalide.** :x:")

                                    test_embed.description = f"**Veuillez réessayer\nLe salon spécifié est invalide.** :x:"

                                    for entry in bot_setup_data:
                                        if entry.get("Guild Name") == guild_name:
                                            entry["Status"] = f"Choosen channel Error"
                                            entry["Timestamp"] = datetime.now(france_tz).strftime("%Y-%m-%d %H:%M:%S")
                                            break  # Exit loop once the entry is found and updated

                                await interaction.response.edit_message(view=self, embed=test_embed)
                                # Write the updated bot_setup_data to the JSON file
                                with open("JSON Files/Global Data/setup_data.json", 'w') as file:
                                    json.dump(bot_setup_data, file)

                        await interaction.response.send_modal(Feedback())

                    @discord.ui.button(style=discord.ButtonStyle.grey, label="Créer", custom_id="step_3", disabled=True)
                    async def button_step_3_callback(self, interaction: discord.Interaction, button):
                        print("Step 3")
                        
                        role_name = "Arabot News"

                        global existing_role
                        existing_role = discord.utils.get(interaction.guild.roles, name=role_name)

                        if not existing_role:

                            global arabot_notif_role

                            arabot_notif_role = await interaction.guild.create_role(name="Arabot News", hoist=False, mentionable=True, color=discord.Color.from_rgb(245, 138, 66))
                            print("arabot notif role has been created!")

                            global arabot_notif_role_id
                            arabot_notif_role_id = arabot_notif_role.id

                            for entry in bot_setup_data:
                                if entry.get("Guild Name") == guild_name:
                                    entry["Status"] = "News Role Creation Finished"
                                    entry["Timestamp"] = datetime.now(france_tz).strftime("%Y-%m-%d %H:%M:%S")
                                    entry["Created Role Id"] = arabot_notif_role.id
                                    break  # Exit loop once the entry is found and updated
                        else:
                            print(f"Role '{role_name}' already exists!")

                            for entry in bot_setup_data:
                                if entry.get("Guild Name") == guild_name:
                                    entry["Status"] = "Existing News Role Finished"
                                    entry["Timestamp"] = datetime.now(france_tz).strftime("%Y-%m-%d %H:%M:%S")
                                    break  # Exit loop once the entry is found and updated

                            arabot_notif_role = existing_role

                        step_3_button = self.children[3]
                        step_3_button.disabled = True
                        step_3_button.style = discord.ButtonStyle.green

                        step_4_button = self.children[4]
                        step_4_button.disabled = False
                        step_4_button.style = discord.ButtonStyle.blurple

                        test_embed.title = f"4/4 Configuration du bot"
                        test_embed.description = f"Vous y êtes presque !\n\nSi vous avez des questions ou simplement besoin d'aide, n'hésitez pas à rejoindre le [serveur support](https://discord.com/invite/uGWkqYazzw)."

                        await interaction.response.edit_message(view=self, embed=test_embed)

                        # Write the updated bot_setup_data to the JSON file
                        with open("JSON Files/Global Data/setup_data.json", 'w') as file:
                            json.dump(bot_setup_data, file)

                    @discord.ui.button(style=discord.ButtonStyle.grey, label="Ok", custom_id="step_4", disabled=True)
                    async def button_step_4_callback(self, interaction: discord.Interaction, button):
                        print("Step 4")

                        # Give Role Embed
                        give_role_embed = discord.Embed(
                            title="**Auto Rôle**",
                            description=f"Cliquez sur le bouton ci-dessous pour obtenir le rôle <@&{arabot_notif_role.id}>",
                            color=discord.Color.from_rgb(3, 144, 252)
                        )
                        give_role_embed.add_field(name="A quoi ça sert ?", value=f"En obtenant le rôle <@&{arabot_notif_role.id}> vous êtes ainsi __abonnés__ aux *informations* concernant **l'Arabot**.")
                        give_role_embed.set_footer(text=version_note)

                        class ButtonView_give_roles(discord.ui.View):
                            def __init__(self):
                                super().__init__(timeout=None)

                            @discord.ui.button(style=discord.ButtonStyle.green, label="Obtenir", custom_id="button_obtain", emoji="➕")
                            async def button1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
                                role = interaction.guild.get_role(arabot_notif_role.id)  # Get the role
                                await interaction.user.add_roles(role)  # Add the role to the user

                                given_autorole_embed = discord.Embed( 
                                    title="",
                                    description=f"{interaction.user.mention} tu as reçu le rôle <@&{arabot_notif_role.id}> !",
                                    color=discord.Color.from_rgb(3, 144, 252)        
                                )

                                await interaction.response.send_message(embed=given_autorole_embed, ephemeral=True)

                            @discord.ui.button(style=discord.ButtonStyle.danger, label="Retirer", custom_id="button_remove", emoji="➖")
                            async def button2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
                                role = interaction.guild.get_role(arabot_notif_role.id)  # Get the role
                                user = interaction.user  # Get the user who clicked the button

                                await user.remove_roles(role)  # Remove the role from the user

                                removed_autorole_embed = discord.Embed( 
                                    title="",
                                    description=f"{user.mention} le rôle <@&{arabot_notif_role.id}> t'as été retiré !",
                                    color=discord.Color.from_rgb(3, 144, 252)        
                                )
                                await interaction.response.send_message(embed=removed_autorole_embed, ephemeral=True)

                        setup_modification_recap = discord.Embed(
                            title="Récapitulatif des modifications :",
                            description= "",
                            color=discord.Color.from_rgb(252, 165, 119),
                        )
                        setup_modification_recap.add_field(name="", value=f"Le salon par défaut du bot est désormais le salon {choosen_channel_global_info.mention}.", inline=True)

                        if not existing_role:
                            setup_modification_recap.add_field(name="", value=f"Le rôle ***{arabot_notif_role.name}*** a été créé.", inline=False)
                        else:
                            setup_modification_recap.add_field(name="", value=f"Le rôle ***{arabot_notif_role.name}*** existait déjà sur le serveur, il n'a donc pas été créé à nouveau.", inline=False)

                        setup_modification_recap.set_author(name= interaction.user.global_name, icon_url= interaction.user.avatar.url)

                        setup_modification_recap.set_footer(text=f"{version_note}")

                        user_id = await client.fetch_user(interaction.user.id)

                        setup_modification_recap_message = await user_id.send(embed=setup_modification_recap)

                        
                        test_embed.title = ""
                        test_embed.description = f"**Configuration Terminée !**\n*Cliquez [ici]({setup_modification_recap_message.jump_url}) pour accéder au récapitulatif des modifications.*"

                        autorole_message = await choosen_channel_global_info.send(embed=give_role_embed, view=ButtonView_give_roles())

                        for entry in bot_setup_data:
                            if entry.get("Guild Name") == guild_name:
                                entry["Status"] = "Finished"
                                entry["Timestamp"] = datetime.now(france_tz).strftime("%Y-%m-%d %H:%M:%S")
                                entry["Autorole Mesage Id"] = autorole_message.id

                                break  # Exit loop once the entry is found and updated
                        step_4_button = self.children[4]
                        step_4_button.disabled = True
                        step_4_button.style = discord.ButtonStyle.grey

                        await interaction.response.edit_message(view=None, embed=test_embed)
                        # Write the updated bot_setup_data to the JSON file
                        with open("JSON Files/Global Data/setup_data.json", 'w') as file:
                            json.dump(bot_setup_data, file)

                    @discord.ui.button(style=discord.ButtonStyle.red, label="Annuler", custom_id="cancel", disabled=False)
                    async def button_right_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
                        print("cancel")

                        test_embed.title = ""
                        test_embed.description = "**Configuration Annulée !**"

                        for entry in bot_setup_data:
                         if entry.get("Guild Name") == guild_name:
                          entry["Status"] = "Canceled"
                          entry["Timestamp"] = datetime.now(france_tz).strftime("%Y-%m-%d %H:%M:%S")
                          break  # Exit loop once the entry is found and updated

                                                # Write the updated bot_setup_data to the JSON file
                        with open("JSON Files/Global Data/setup_data.json", 'w') as file:
                            json.dump(bot_setup_data, file)

                        await interaction.response.edit_message(view=None, embed=test_embed)


                await interaction.response.send_message(embed=test_embed, view=ButtonView_test(interaction), ephemeral=True)



@tree.command(name="conditions", description="Affiche les conditions d'utilisation du bot")
async def conditions_command(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les dm ! :no_entry_sign:", ephemeral=True)
    else:
     await interaction.response.send_message(embed=tos_embed, view=ButtonView_setup_tos(), ephemeral=True)

@tree.command(name="effacer-dm", description="Supprime tout DM du bot")
async def delete_dm(interaction: discord.Interaction):
    # Check if the command is sent in a DM
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content=":hourglass_flowing_sand: Tous les messages du bot sont en cours de suppression.....\n\n(Vous serez notifié quand ce sera fini. :information_source:)", ephemeral=True)

        # Fetch the bot's sent messages in the DM
        bot_messages = []
        async for message in interaction.channel.history(limit=None):
            if message.author == interaction.client.user:
                bot_messages.append(message)

        # Delete each bot message
        for message in bot_messages:
            await message.delete()
            await asyncio.sleep(1)

        await interaction.edit_original_response(content="Tous les messages du bot ont étés supprimés :white_check_mark: !")
        user_to_dm = await client.fetch_user(interaction.user.id)
        notification_message = await user_to_dm.send(content="🔔")
        await notification_message.delete()


    else:
        with open("JSON Files/Global Data/TOS_info_data.json", 'r') as json_file:
            loaded_data = json.load(json_file)

        # Extract relevant data from loaded JSON using the specific guild ID
        user_id = str(interaction.user.id)
        user_data = loaded_data.get(user_id, {})
        is_tos_accepted = loaded_data.get(user_id, {}).get("accepted_tos", False)

        if not user_data:
            await interaction.response.send_message(content="Faites `/conditions` et réessayez !",ephemeral=True)
        else:
        
         if not is_tos_accepted:
            await interaction.response.send_message(embed=tos_not_accepted_embed, ephemeral=True)
         else:
            await interaction.response.send_message("Cette commande n'est utilisable que dans les DM !", ephemeral=True)


@tree.command(name="admin", description="Affiche le panel d'administration du bot")
async def admin_panel(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les dm ! :no_entry_sign:", ephemeral=True)
    else:
        command_name = interaction.data['name']
        user_id = interaction.user.id
        command_id = interaction.data['id']
        guild_name = interaction.guild.name
        
        USER_DM = await client.fetch_user(TGA25_ID)

        try:
            if interaction.user.id == TGA25_ID:
                view = AdminSelectMenu()
                await interaction.response.send_message(content="Administration du bot :", view=view, ephemeral=True)
            else:
                await interaction.response.send_message("Tu n'es pas autorisé a utiliser cette commande ! :no_entry_sign: ", ephemeral=True)

        except Exception as e:
            error_dminfo_embed = discord.Embed(
                title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
                description=f"**Erreur causée par** <@{user_id}>",
                color=discord.Color.from_rgb(245, 170, 66)
            )

            error_dminfo_embed.add_field(name="Details :",
                                         value=f"Erreur survenue il y à <t:{generate_current_time_timestamp()}:R> dans le serveur `{guild_name}`",
                                         inline=True)
            error_dminfo_embed.add_field(name="**Commande :**", value=f"`{command_name}`", inline=True)
            error_dminfo_embed.add_field(name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
            error_dminfo_embed.add_field(name="Erreur :", value=f"`{e}`", inline=False)
            error_dminfo_embed.set_footer(text=f"{version_note}")

            await USER_DM.send(embed=error_dminfo_embed)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)


@tree.command(name="explosion", description="Boum !")
async def explosion_command(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les DM ! :no_entry_sign:", ephemeral=True)
    else:
        with open("JSON Files/Global Data/TOS_info_data.json", 'r') as json_file:
            loaded_data = json.load(json_file)

        # Extract relevant data from loaded JSON using the specific guild ID
        user_id = str(interaction.user.id)
        user_data = loaded_data.get(user_id, {})
        is_tos_accepted = loaded_data.get(user_id, {}).get("accepted_tos", False)

        if not user_data:
            await interaction.response.send_message(content="Faites `/conditions` et réessayez !", ephemeral=True)
        else:
            if not is_tos_accepted:
                await interaction.response.send_message(embed=tos_not_accepted_embed, ephemeral=True)
            else:
                if explosion_command_avalaible == False:
                    await interaction.response.send_message(embed=unavaileble_command_embed, ephemeral=True)
                else:
                    try:
                        with open("JSON Files/Explosion_Command_Data/explosion_command_cooldown.json", 'r') as f:
                            explosion_command_cooldown = json.load(f)
                    except FileNotFoundError:
                        explosion_command_cooldown = {}

                    # Check for cooldown
                    guild_id = str(interaction.guild_id)

                    if guild_id not in explosion_command_cooldown:
                        explosion_command_cooldown[guild_id] = 0

                    current_time = time.time()
                    cooldown_time = 5 * 24 * 60 * 60  # Cooldown time set to 5 days in seconds

                    if current_time - explosion_command_cooldown[guild_id] <= cooldown_time:
                        # Server is on cooldown, inform users
                        remaining_time_seconds = int(cooldown_time - (current_time - explosion_command_cooldown[guild_id]))

                        remaining_days, remaining_seconds = divmod(remaining_time_seconds, 24 * 60 * 60)
                        remaining_hours, remaining_seconds = divmod(remaining_seconds, 60 * 60)
                        remaining_minutes, remaining_seconds = divmod(remaining_seconds, 60)

                        remaining_time_formatted = (
                            f"{remaining_days} jours, {remaining_hours} heures, {remaining_minutes} minutes et {remaining_seconds} secondes"
                        )

                        await interaction.response.send_message(f"Veuillez attendre {remaining_time_formatted} avant de refaire exploser ce serveur... :hourglass_flowing_sand:", ephemeral=True)
                        return

                    explosion_command_cooldown[guild_id] = current_time  # Update the cooldown time for the server

                    user_id = interaction.user.id
                    command_name = interaction.data['name']
                    command_id = interaction.data['id']
                    guild_name = interaction.guild.name
                    TGA25_ID = "845327664143532053"
                    USER_DM = await client.fetch_user(TGA25_ID)

                    try:
                        if maintenance_mode:
                            await interaction.response.send_message(embed=maintenance_embed, ephemeral=True)
                            return
                        await interaction.response.send_message(content="Sélectionnez une force d'explosion :",
                                                                 view=ButtonView_explosion_command(), embed=explosion_force_embed)

                    except Exception as e:
                        error_dminfo_embed = discord.Embed(
                            title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
                            description=f"**Erreur causée par** <@{user_id}>",
                            color=discord.Color.from_rgb(245, 170, 66)
                        )

                        error_dminfo_embed.add_field(name="Details :",
                                                     value=f"Erreur survenue il y a <t:{generate_current_time_timestamp()}:R> dans le serveur `{guild_name}`",
                                                     inline=True)
                        error_dminfo_embed.add_field(name="**Commande :**", value=f"`{command_name}`", inline=True)
                        error_dminfo_embed.add_field(name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
                        error_dminfo_embed.add_field(name="Erreur :", value=f"`{e}`", inline=False)
                        error_dminfo_embed.set_footer(text=f"{version_note}")

                        await USER_DM.send(embed=error_dminfo_embed)
                        await interaction.response.send_message(embed=error_embed, ephemeral=True)

                    # Save the updated server cooldown data to the JSON file
                    with open("JSON Files/Explosion_Command_Data/explosion_command_cooldown.json", 'w') as f:
                        json.dump(explosion_command_cooldown, f)








@tree.command(name="vol", description="Vole le nom d'un utilisateur")
async def vol_command(interaction: discord.Interaction, user: discord.Member):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les dm ! :no_entry_sign:", ephemeral=True)
    else:
        with open("JSON Files/Global Data/TOS_info_data.json", 'r') as json_file:
            loaded_data = json.load(json_file)

        # Extract relevant data from loaded JSON using the specific guild ID
        user_id = str(interaction.user.id)
        user_data = loaded_data.get(user_id, {})
        is_tos_accepted = loaded_data.get(user_id, {}).get("accepted_tos", False)

        if not user_data:
            await interaction.response.send_message(content="Faites `/conditions` et réessayez !",ephemeral=True)
        else:

         if not is_tos_accepted:
            await interaction.response.send_message(embed=tos_not_accepted_embed, ephemeral=True)
         else:
            if vol_command_avalaible == False:
                await interaction.response.send_message(embed=unavaileble_command_embed, ephemeral=True)
            elif vol_command_avalaible == True:
                user_id = interaction.user.id
                command_name = interaction.data['name']
                command_id = interaction.data['id']
                guild_name = interaction.guild.name
                TGA25_ID = "845327664143532053"
                USER_DM = await client.fetch_user(TGA25_ID)

                try:
                    if maintenance_mode:
                        await interaction.response.send_message(embed=maintenance_embed, ephemeral=True)
                    else:
                        try:
                            with open("JSON Files/Vol_Command_Data/vol_command_cooldown.json", 'r') as f:
                                server_cooldowns = json.load(f)
                        except FileNotFoundError:
                            server_cooldowns = {}

                        guild_id = str(interaction.guild_id)

                        if guild_id not in server_cooldowns:
                            server_cooldowns[guild_id] = 0

                        current_time = time.time()
                        cooldown_time = 300  # Change this to the desired cooldown time in seconds

                        if current_time - server_cooldowns[guild_id] > cooldown_time:
                            bot_user = interaction.guild.me
                            choosen_user_id = user.id
                            choosen_user = await client.fetch_user(choosen_user_id)
                            choosen_user_avatar_url = choosen_user.avatar.url
                            response = requests.get(choosen_user_avatar_url)

                            if response.status_code == 200:
                                # Save the image to disk
                                with open(f"Images/Downloaded Images/{choosen_user}.png", "wb") as f:
                                    f.write(response.content)
                                    print(f"{printer_timestamp()} Image downloaded successfully!")
                            else:
                                print(f"{printer_timestamp()} Failed to download image.")

                            # Update the bot's username to match the username of the mentioned user
                            profile_image_path = f"Images/Downloaded Images/{choosen_user}.png"
                            profile_image = open(profile_image_path, 'rb')
                            pfp = profile_image.read()

                            await interaction.response.send_message(f"J'ai temporairement 'volé' le profil de <@{user.id}> :tada: ! ", ephemeral=True)

                            try:
                                await client.user.edit(avatar=pfp)
                                print(f"{printer_timestamp()} The avatar has been successfully changed to: {user.avatar}")
                            except Exception as rate_limit_error:
                                if "You are changing your avatar too fast" in str(rate_limit_error):
                                    print(f"{printer_timestamp()} ! Rate limit avatar !")
                                    await interaction.edit_original_response(
                                        content=":red_circle: Une erreur est survenue durant la modification de la photo de profil... :red_circle: ")
                                    pass

                            if user.bot:
                                await bot_user.edit(nick=user.name)
                                print(f"{printer_timestamp()} The nickname has been successfully changed to {user.name} #{user.id} (Bot)")
                            else:
                                await bot_user.edit(nick=user.global_name)
                                print(f"{printer_timestamp()} The nickname has been successfully changed to {user.name} #{user.id} (Normal User)")

                            print(f"{printer_timestamp()} The profile of {user.name} #{user.id} has been stolen! (profile resetting in 30s)")
                            await asyncio.sleep(30)

                            # Reset the profile after 30s
                            try:
                                profile_image_path = f"{IMAGES_PATH}/Bot Logo/default_image_{bot_mode_lc}_bot.png"
                                profile_image = open(profile_image_path, "rb")
                                pfp = profile_image.read()

                                await client.user.edit(avatar=pfp)
                                print(f"{printer_timestamp()} Profile image successfully reestablished to default!")

                                await bot_user.edit(nick=default_bot_nick)
                                print(f"{printer_timestamp()} Nickname successfully reestablished to default!")

                                await interaction.edit_original_response(
                                    content="Mon profil a correctement été réinitialisé :white_check_mark: !")
                                server_cooldowns[guild_id] = current_time

                            except Exception as rate_limit_error:
                                if "You are changing your avatar too fast" in str(rate_limit_error):
                                    print(f"{printer_timestamp()} ! Rate limit avatar !")
                                    pass

                                    await bot_user.edit(nick=default_bot_nick)
                                    print(f"{printer_timestamp()} Nickname successfully reestablished to default!")

                                    await interaction.edit_original_response(
                                        content="Mon profil a partiellement été réinitialisé :ballot_box_with_check: !")
                                    server_cooldowns[guild_id] = current_time
                                else:
                                    await bot_user.edit(nick=default_bot_nick)
                                    print(f"{printer_timestamp()} Nickname successfully reestablished to default!")

                                    await interaction.edit_original_response(
                                        content="Mon profil a correctement été réinitialisé :white_check_mark: !")
                                    server_cooldowns[guild_id] = current_time
                        else:
                            remaining_time = int(cooldown_time - (current_time - server_cooldowns[guild_id]))

                            remaining_minutes = remaining_time // 60
                            remaining_seconds = remaining_time % 60

                            await interaction.response.send_message(
                                f"Veuillez patienter ***{remaining_minutes} minutes*** et ***{remaining_seconds} secondes*** avant de pouvoir réutiliser cette commande.", ephemeral=True)

                        # Save the updated server cooldown data to the JSON file
                        with open("JSON Files/Vol_Command_Data/vol_command_cooldown.json", 'w') as f:
                            json.dump(server_cooldowns, f)

                except Exception as e:
                    print(e)
                    error_dminfo_embed = discord.Embed(
                        title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
                        description=f"**Erreur causée par** <@{user.id}>",
                        color=discord.Color.from_rgb(245, 170, 66)
                    )

                    error_dminfo_embed.add_field(
                        name="Details :", value=f"Erreur survenue il y à <t:{generate_current_time_timestamp()}:R> dans le serveur `{guild_name}`",
                        inline=True)
                    error_dminfo_embed.add_field(
                        name="**Commande :**", value=f"`{command_name}`", inline=True)
                    error_dminfo_embed.add_field(
                        name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
                    error_dminfo_embed.add_field(
                        name="Erreur :", value=f"`{e}`", inline=False)
                    error_dminfo_embed.set_footer(text=f"{version_note}")

                    await USER_DM.send(embed=error_dminfo_embed)
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)


          

        
@tree.command(name="help", description="Affiche les commandes disponibles")
async def embed_command(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les DM ! :no_entry_sign:", ephemeral=True)
    else:
        # Define loaded_data outside the else block
        loaded_data = {}
        with open("JSON Files/Global Data/TOS_info_data.json", 'r') as json_file:
            loaded_data = json.load(json_file)

        # Extract relevant data from loaded JSON using the specific guild ID
        user_id = str(interaction.user.id)
        user_data = loaded_data.get(user_id, {})
        is_tos_accepted = loaded_data.get(user_id, {}).get("accepted_tos", False)

        if not user_data:
            await interaction.response.send_message(content="Faites `/conditions` et réessayez !",ephemeral=True)
        else:

         if not is_tos_accepted:
            await interaction.response.send_message(embed=tos_not_accepted_embed, ephemeral=True)
         else:
            # Rest of the code for when TOS is accepted
            # ...

            user_id = interaction.user.id
            command_name = interaction.data['name']
            command_id = interaction.data['id']
            guild_name = interaction.guild.name
            TGA25_ID = "845327664143532053"
            USER_DM = await client.fetch_user(TGA25_ID)

            if maintenance_mode:
                await interaction.response.send_message(embed=maintenance_embed, ephemeral=True)
                return

            try:
                await interaction.response.send_message(embed=help_embed, ephemeral=False)
            except Exception as e:
                error_dminfo_embed = discord.Embed(
                    title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
                    description=f"**Erreur causée par** <@{user_id}>",
                    color=discord.Color.from_rgb(245, 170, 66)
                )

                error_dminfo_embed.add_field(
                    name="Details :", value=f"Erreur survenue il y a <t:{generate_current_time_timestamp()}:R> dans le serveur `{guild_name}`", inline=True)
                error_dminfo_embed.add_field(
                    name="**Commande :**", value=f"`{command_name}`", inline=True)
                error_dminfo_embed.add_field(
                    name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
                error_dminfo_embed.add_field(
                    name="Erreur :", value=f"`{e}`", inline=False)
                error_dminfo_embed.set_footer(text=f"{version_note}")

                await USER_DM.send(embed=error_dminfo_embed)
                await interaction.response.send_message(
                    embed=error_embed, ephemeral=True)

        

    




@tree.command(name="info", description="Affiche des informations à propos du bot")
async def embed_command(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les dm ! :no_entry_sign:", ephemeral=True)
    else:
        with open("JSON Files/Global Data/TOS_info_data.json", 'r') as json_file:
            loaded_data = json.load(json_file)

        # Extract relevant data from loaded JSON using the specific guild ID
        user_id = str(interaction.user.id)
        user_data = loaded_data.get(user_id, {})
        is_tos_accepted = loaded_data.get(user_id, {}).get("accepted_tos", False)

        if not user_data:
            await interaction.response.send_message(content="Faites `/conditions` et réessayez !",ephemeral=True)
        else:

         if not is_tos_accepted:
            await interaction.response.send_message(embed=tos_not_accepted_embed, ephemeral=True)
         else:
            # The code that should execute when terms of service are accepted
            user_id = interaction.user.id
            command_name = interaction.data['name']
            command_id = interaction.data['id']
            guild_name = interaction.guild.name
            TGA25_ID = "845327664143532053"
            USER_DM = await client.fetch_user(TGA25_ID)

            if maintenance_mode:
                await interaction.response.send_message(embed=maintenance_embed, ephemeral=True)
                return

            try:
                # Create the embed
                info_embed2 = discord.Embed(
                    title="Infos",
                    color=discord.Color.from_rgb(60, 240, 132)
                )
                info_embed2.add_field(name="**Ping 🏓**", value=f"*{round(client.latency, 2)}* ms de latence", inline=False)
                info_embed2.add_field(name="**Date & Heure 🕐**", value=f"Nous sommes le <t:{generate_current_time_timestamp()}:D> et il est <t:{generate_current_time_timestamp()}:t>", inline=False)
                info_embed2.add_field(name="**Dernier redémarrage 🔄**", value=f"<t:{int(restart_time.timestamp())}>", inline=False)
                info_embed2.add_field(name="**Langage de programmation 🌐**", value="*Python* <:logo_python_arabot:1108367929457791116>", inline=False)
                info_embed2.set_footer(text=version_note)

                await interaction.response.send_message(embed=info_embed2, ephemeral=False)

            except Exception as e:
                error_dminfo_embed = discord.Embed(
                    title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
                    description=f"**Erreur causée par** <@{user_id}>",
                    color=discord.Color.from_rgb(245, 170, 66)
                )

                error_dminfo_embed.add_field(
                    name="Details :", value=f"Erreur survenue il y a à <t:{generate_current_time_timestamp()}:R> dans le serveur `{guild_name}`", inline=True)
                error_dminfo_embed.add_field(
                    name="**Commande :**", value=f"`{command_name}`", inline=True)
                error_dminfo_embed.add_field(
                    name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
                error_dminfo_embed.add_field(
                    name="Erreur :", value=f"`{e}`", inline=False)
                error_dminfo_embed.set_footer(text=f"{version_note}")

                await USER_DM.send(embed=error_dminfo_embed)
                await interaction.response.send_message(embed=error_embed, ephemeral=True)


@tree.command(name="devinfo", description="Affiche des informations à propos du développeur")
async def dev_info_command(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message(content="Vous ne pouvez pas utiliser cette commande dans les dm ! :no_entry_sign:", ephemeral=True)
    else:
        with open("JSON Files/Global Data/TOS_info_data.json", 'r') as json_file:
            loaded_data = json.load(json_file)

        # Extract relevant data from loaded JSON using the specific guild ID
        user_id = str(interaction.user.id)
        user_data = loaded_data.get(user_id, {})
        is_tos_accepted = loaded_data.get(user_id, {}).get("accepted_tos", False)

        if not user_data:
            await interaction.response.send_message(content="Faites `/conditions` et réessayez !",ephemeral=True)
        else:

         if not is_tos_accepted:
            await interaction.response.send_message(embed=tos_not_accepted_embed, ephemeral=True)
         else:
            command_name = interaction.data['name']
            user_id = interaction.user.id
            command_id = interaction.data['id']
            guild_name = interaction.guild.name
            TGA25_ID = "845327664143532053"
            USER_DM = await client.fetch_user(TGA25_ID)

            try:
                emoji_id = 1107235074757373963  # Replace with the ID of your custom emoji
                myemoji = client.get_emoji(emoji_id)
                await interaction.response.send_message(content=myemoji, embed=dev_info_embed)

            except Exception as e:
                error_dminfo_embed = discord.Embed(
                    title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
                    description=f"**Erreur causée par** <@{user_id}>",
                    color=discord.Color.from_rgb(245, 170, 66)
                )

                error_dminfo_embed.add_field(
                    name="Details :", value=f"Erreur survenue il y a à <t:{generate_current_time_timestamp()}:R> dans le serveur `{guild_name}`", inline=True)
                error_dminfo_embed.add_field(
                    name="**Commande :**", value=f"`{command_name}`", inline=True)
                error_dminfo_embed.add_field(
                    name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
                error_dminfo_embed.add_field(
                    name="Erreur :", value=f"`{e}`", inline=False)
                error_dminfo_embed.set_footer(text=f"{version_note}")

                await USER_DM.send(embed=error_dminfo_embed)
                await interaction.response.send_message(embed=error_embed, ephemeral=True)



#Twitch Live Alert Loop

async def twitch_loop():
   while not is_ready:
        await asyncio.sleep(30)
        print(f"{printer_timestamp()} Twitch Loop has been started !")

        headers = {
        'Client-Id': f'{twitch_client_id}',
        'Authorization': f'Bearer {twitch_access_token}',
        }

   previous_status = None

   

   while True:
     response = requests.get(f"https://api.twitch.tv/helix/streams?user_login={streamer_name}", headers=headers)

    # Ensure the request was successful
     if response.status_code == 200:
        user_info = json.loads(response.text)   

        if not user_info['data']:
            current_status = f"{streamer_name} is offline..."
        else:
            current_status = f"{streamer_name} is online !"
            # Additional information if online
            user_name = user_info["data"][0]["user_name"]
            user_id = user_info["data"][0]["user_id"]
            user_login = user_info["data"][0]["user_login"]
            game_name = user_info["data"][0]["game_name"]
            title = user_info["data"][0]["title"]
            thumbnail_url = user_info["data"][0]["thumbnail_url"]

            timestamp = int(time.time())  # Get current Unix timestamp
            thumbnail_url_with_timestamp = f"{thumbnail_url}.{timestamp}"

            width = 300
            height = 200
            resized_thumbnail_url = thumbnail_url_with_timestamp.replace('{width}', str(width)).replace('{height}', str(height))

        if current_status != previous_status:
            print(f"{printer_timestamp()} {current_status}")
            if current_status == f"{streamer_name} is online !":
                print(f"{printer_timestamp()} -----------------------")
                print(f"{printer_timestamp()} User Name: {user_name}")
                print(f"{printer_timestamp()} User Id = {user_id}")
                print(f"{printer_timestamp()} Game Name: {game_name}")
                print(f"{printer_timestamp()} Title: {title}")
                print(f"{printer_timestamp()} Thumbnail URL: {resized_thumbnail_url}")
                print(f"{printer_timestamp()} Live URL : https://twitch.tv/{user_login}")
                print(f"{printer_timestamp()} -----------------------")
                

                live_url = f"https://twitch.tv/{user_login}"

                 # Replace with your channel ID
                twitch_message_channel = client.get_channel(goomink_news_channel_id)


                if twitch_message_channel:
                 
                 twitch_live_embed = discord.Embed( 
                 title=f"🔴 LIVE 🔴",
                 description="",
                 color=discord.Color.from_rgb(136, 3, 252)        
                 )
                 twitch_live_embed.add_field(name="", value=f"***{user_name}*** est en live sur *__{game_name}__* <:logo_twitch_arabot:1151919627983659148>", inline=False)
                 twitch_live_embed.add_field(name=f"", value=f"{title}", inline=True)
                 
                 twitch_live_embed.add_field(name="", value= f":rocket: **Venez voir en cliquant** [ici]({live_url}) :rocket:", inline=False)

                 twitch_live_embed.set_image(url=resized_thumbnail_url)

                 twitch_live_embed.set_footer(text=f"{version_note}")

                 await twitch_message_channel.send(content="@everyon e",embed=twitch_live_embed)
                 print(f"{printer_timestamp()} Twitch Live Alert has been sent ! (in channel : {twitch_message_channel})")

            previous_status = current_status

     else:
        if response.status_code == 429:
            print(f"{printer_timestamp()} Twitch API system is being  rate limited !!")
            USER_DM = await client.fetch_user(TGA25_ID)
            await USER_DM.send(content="***__Twitch API system is being  rate limited !!__**\n*Please check the [console](https://portal.daki.cc/)*")
        else:    

         print(f"{printer_timestamp()} Request returned status code {response.status_code}")
         
         USER_DM = await client.fetch_user(TGA25_ID)

         error_data = response.json()
         error_message = error_data.get("message", "No error message provided")
         error_status = error_data.get("status", "No status provided")

         await USER_DM.send(content=f"Twitch API system returned status code **{error_status}** : `{error_message}`\nThe bot has been stopped\nPlease check the [console](https://portal.daki.cc/)")
         await client.close()


     await asyncio.sleep(15)


@tree.command(name="test", description="test_command")
async def test_command(interaction: discord.Interaction):
    print("test")





         











    


async def explosion_command_system(interaction: discord.Interaction):

    # Load data from JSON file
    with open("JSON Files/Explosion_Command_Data/level_info_explosion_command.json", 'r') as json_file:
        loaded_data = json.load(json_file)

    # Extract relevant data from loaded JSON
    explosion_command_system_choosen_level = loaded_data.get("choosen_level")
    username_button_pressed = loaded_data.get("username_button_pressed")

    # Display information about the loaded data
    print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Explosion level is level {explosion_command_system_choosen_level} !")

    try:
        guild_id = interaction.guild_id
        guild = client.get_guild(guild_id)

        # Create the 'Explosion' role
        explosion_role = await interaction.guild.create_role(name="Explosion", hoist=True, mentionable=False, color=discord.Color.from_rgb(242, 153, 51))
        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} The explosion role has been created !")

        try:
            # Set the position of the 'Explosion' role
            bot_highest_role = interaction.guild.me.top_role
            desired_position = bot_highest_role.position - 1

            test_positions = {
                explosion_role: desired_position,
            }

            await interaction.guild.edit_role_positions(positions=test_positions)

        except Exception as position_role_error:
            print(f"{printer_timestamp()} An error has occurred while trying to change role position: {position_role_error}")

        # Get non-bot members in the guild and assign the 'Explosion' role
        members = [member for member in interaction.guild.members if not member.bot]
        for member in members:
            if member != guild.owner:
                await member.add_roles(explosion_role)

        # Store roles of all members before removing certain roles
        stored_roles = {member.id: [role.id for role in member.roles] for member in members}

        # Identify roles to be removed
        removed_roles = []
        for role_ids in stored_roles.values():
            for role_id in role_ids:
                role = discord.utils.get(interaction.guild.roles, id=role_id)
                if role is not None and role.name not in ["@everyone", explosion_role.name]:
                    if member != guild.owner:
                     removed_roles.append(role)

        # Remove identified roles from all members
        if removed_roles:
             for member_id, roles in stored_roles.items():
                member = interaction.guild.get_member(member_id)
                if member:
                    try:
                        if member != guild.owner:
                         await member.remove_roles(*removed_roles)
                    except Exception as e:
                        print(f"{printer_timestamp()} Error removing roles for {member.display_name}: {e}")

        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Roles removal process completed for all guild members !")

        # Create 'Refuge' category and channel
        refuge_category = await guild.create_category("🏡Refuge🏡")
        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Refuge category has been created !")

        refuge_channel = await guild.create_text_channel("❗venez❗", category=refuge_category)
        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Refuge channel has been created !")
        await refuge_category.edit(position=0)

        # Set permissions for 'Explosion' role in the 'Refuge' channel
        await refuge_channel.set_permissions(explosion_role, send_messages=False)

        # Pause for a moment
        await asyncio.sleep(10)

        # Update the name of the 'Refuge' channel
        await refuge_channel.edit(name="🔰Refuge🔰")
        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Refuge category name has been updated !")

        # Pause for a moment
        await asyncio.sleep(0.5)

        refuge_channel_id = refuge_channel.id

        # Pause for a moment
        await asyncio.sleep(0.5)

        # Check if guild_id is present in welcome_data
        if guild_id not in welcome_data or not welcome_data[guild_id]:
            default_channel = guild.system_channel
            fallback_channel = get_fallback_channel(guild)

            # Send a message to the default or fallback channel
            if default_channel:
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Message sending to :{default_channel.name} ({default_channel.id})")
                await default_channel.send(content=f"@hee ! Rejoignez le salon <#{refuge_channel_id}> !")
            elif fallback_channel:
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Message sending to fallback channel: {fallback_channel.name} ({fallback_channel.id})")
                await fallback_channel.send(content=f"@her ! Rejoignez le salon <#{refuge_channel_id}> !")

            # Create an Embed for the 'Refuge' channel
            explosion_refuge_embed = discord.Embed(
                title="**🟢 Refuge 🟢**",
                description="Ce salon vous permet de patienter jusqu'à la fin des explosions.",
                color=discord.Color.from_rgb(158, 240, 91)
            )

            # Add fields based on the explosion level
            if explosion_command_system_choosen_level == 1:
                explosion_refuge_embed.add_field(name="Le serveur va être inaccessible pendant *1* minute.",
                                                value=f"*On peut remercier {username_button_pressed} ... 👏👏*",
                                                inline=False)
            elif explosion_command_system_choosen_level == 2:
                explosion_refuge_embed.add_field(name="Le serveur va être inaccessible pendant *5* minutes.",
                                                value=f"*On peut remercier {username_button_pressed} ... 👏👏*",
                                                inline=False)
            else:
                explosion_refuge_embed.add_field(name="Le serveur va être inaccessible pendant *10* minutes.",
                                                value=f"*On peut remercier {username_button_pressed} ... 👏👏*",
                                                inline=False)

            # Set footer text
            explosion_refuge_embed.set_footer(text=f"{version_note}")

            # Send the Embed to the 'Refuge' channel
            refuge_embed_message = await refuge_channel.send(embed=explosion_refuge_embed)

            # Pause for a moment
            await asyncio.sleep(5)

            print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Explosion Started !")

            if explosion_command_system_choosen_level == 1:
                explosion_message_content = "💥💥"

            elif explosion_command_system_choosen_level == 2:
                explosion_message_content = "💥💥💥💥"

            else: 
                explosion_message_content = "💥💥💥💥💥💥"  

            for channel in guild.text_channels:
             if channel.id == refuge_channel.id:
                continue
             try:
                # Send "aaa" in separate messages to the text channel
                delay = random.uniform(0.3, 1.3)
                await channel.send(explosion_message_content)
                await asyncio.sleep(delay)

             except Exception as e:
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Failed to send message to {channel.name} : {e}")

            print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Explosion Ended !")


            await asyncio.sleep(15)            

            # Update the 'Refuge' Embed after sending messages to channels
            if explosion_command_system_choosen_level == 1:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est inaccessible pendant *1* minute.",
                                                    value=f"*Vous pouvez désormais envoyer des messages dans ce salon :pen_ballpoint:*",
                                                    inline=False)
            elif explosion_command_system_choosen_level == 2:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est inaccessible pendant *5* minutes.",
                                                    value=f"*Vous pouvez désormais envoyer des messages dans ce salon :pen_ballpoint:*",
                                                    inline=False)
            else:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est inaccessible pendant *10* minutes.",
                                                    value=f"*Vous pouvez désormais envoyer des messages dans ce salon :pen_ballpoint:*",
                                                    inline=False)

            # Edit the 'Refuge' Embed message with the updated information
            await refuge_embed_message.edit(embed=explosion_refuge_embed)

             # Allow people to send messages in the 'Refuge' channel
            await refuge_channel.set_permissions(explosion_role, send_messages=True)

            print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Channel hiding started...")

            # Hide all channels (except 'Refuge') for the 'Explosion' role
            for channel in guild.text_channels:
                if channel.id != refuge_channel_id:
                    try:
                        await channel.set_permissions(explosion_role, view_channel=False)
                    except Exception as e:
                        print(f"{printer_timestamp()} Error hiding channel {channel}: {e}")

            print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} All channels have been successfully hidden !")

            await asyncio.sleep(20)

            print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Waiting time starting...")


            if explosion_command_system_choosen_level == 1:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction. :construction_site:",
                                                    value=f"",
                                                    inline=False)
                explosion_refuge_embed.set_thumbnail(url=lock_icon_url)

            elif explosion_command_system_choosen_level == 2:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction. :construction_site:",
                                                    value=f"",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=lock_icon_url)
                

            else:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction. :construction_site:",
                                                    value=f"",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=lock_icon_url)

            # Edit the 'Refuge' Embed message with the updated information
            await refuge_embed_message.edit(embed=explosion_refuge_embed)

            await asyncio.sleep(10)

            if explosion_command_system_choosen_level == 1:
               sleep_time = 15

            elif explosion_command_system_choosen_level == 2:
                sleep_time = 75

            else:
                sleep_time = 150      

            if explosion_command_system_choosen_level == 1:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction.. :construction_site:",
                                                    value=f"*Temps d'attente restant: environ 1 minute* ",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=clock12_icon_url)
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Remaining time : 60s")

            elif explosion_command_system_choosen_level == 2:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction.. :construction_site:",
                                                    value=f"*Temps d'attente restant: environ 5 minutes*",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=clock12_icon_url)
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Remaining time : 5min")
            else:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction.. :construction_site:",
                                                    value=f"*Temps d'attente restant: environ 10 minutes*",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=clock12_icon_url)
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Remaining time : 10min")

            # Edit the 'Refuge' Embed message with the updated information
            await refuge_embed_message.edit(embed=explosion_refuge_embed)

            

            # Pause for a specified duration
            await asyncio.sleep(sleep_time)


            if explosion_command_system_choosen_level == 1:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction... :construction_site:",
                                                    value=f"*Temps d'attente restant: environ 45 secondes* ",
                                                    inline=False)
                

                explosion_refuge_embed.set_thumbnail(url=clock3_icon_url)
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Remaining time : 45s")


            elif explosion_command_system_choosen_level == 2:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction... :construction_site:",
                                                    value=f"*Temps d'attente restant: environ 3 minutes*",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=clock3_icon_url)
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Remaining time : 3min")
            else:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction... :construction_site:",
                                                    value=f"*Temps d'attente restant: 7 minutes*",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=clock3_icon_url)
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Remaining time : 7min")

            # Edit the 'Refuge' Embed message with the updated information
            await refuge_embed_message.edit(embed=explosion_refuge_embed)

            await asyncio.sleep(sleep_time)

            if explosion_command_system_choosen_level == 1:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction.. :construction_site:",
                                                    value=f"*Temps d'attente restant: environ 30 secondes* ",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=clock1230_icon_url)
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Remaining time : 30s")

            elif explosion_command_system_choosen_level == 2:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction.. :construction_site:",
                                                    value=f"*Temps d'attente restant: environ 2 minutes*",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=clock1230_icon_url)
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Remaining time : 2min")

            else:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction.. :construction_site:",
                                                    value=f"*Temps d'attente restant: environ 5 minutes*",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=clock1230_icon_url)
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Remaining time : 5min")

            # Edit the 'Refuge' Embed message with the updated information
            await refuge_embed_message.edit(embed=explosion_refuge_embed)

            await asyncio.sleep(sleep_time)

            if explosion_command_system_choosen_level == 1:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction. :construction_site:",
                                                    value=f"*Temps d'attente restant: environ 15 secondes* ",
                                                    inline=False)

                explosion_refuge_embed.set_thumbnail(url=clock9_icon_url)
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Remaining time : 15s")
            
            elif explosion_command_system_choosen_level == 2:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction. :construction_site:",
                                                    value=f"*Temps d'attente restant: environ 75 secondes*",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=clock9_icon_url)
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Remaining time : 75s")
                                                    
            else:
                explosion_refuge_embed.set_field_at(0, name="Le serveur est en cours de reconstruction. :construction_site:",
                                                    value=f"*Temps d'attente restant: environ 2 minutes*",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=clock9_icon_url)
                print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Remaining time : 2min")

            # Edit the 'Refuge' Embed message with the updated information
            await refuge_embed_message.edit(embed=explosion_refuge_embed)

            await asyncio.sleep(sleep_time)

            if explosion_command_system_choosen_level == 1:
                explosion_refuge_embed.set_field_at(0, name="Le serveur va progressivement redevenir accessible... :hourglass_flowing_sand:",
                                                    value=f"",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=unlock_icon_url)

            elif explosion_command_system_choosen_level == 2:
                explosion_refuge_embed.set_field_at(0, name="Le serveur va progressivement redevenir accessible... :hourglass_flowing_sand:",
                                                    value=f"",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=unlock_icon_url)
            else:
                explosion_refuge_embed.set_field_at(0, name="Le serveur va progressivement redevenir accessible... :hourglass_flowing_sand:",
                                                    value=f"",
                                                    inline=False)
                
                explosion_refuge_embed.set_thumbnail(url=unlock_icon_url)

            await refuge_embed_message.edit(embed=explosion_refuge_embed)

            print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Waiting time ended !")
            await asyncio.sleep(5)

   
            if explosion_command_system_choosen_level == 1:
               explosion_message_delete_limit = 2
                    

            elif explosion_command_system_choosen_level == 2:
                explosion_message_delete_limit = 4
                  
                
            else:
               explosion_message_delete_limit = 6

           
            # Delete bot messages from all channels
            for channel in guild.text_channels:
             if channel.id != refuge_channel_id:
              try:
               messages_to_delete = []
               async for message in channel.history(limit=explosion_message_delete_limit):
                if message.author == client.user:
                    messages_to_delete.append(message)
                else:
                    # If you want to stop when you encounter a user message, break the loop here
                    pass

            # Bulk delete the bot messages
               if messages_to_delete:
                await channel.delete_messages(messages_to_delete)
                await asyncio.sleep(1.5 * len(messages_to_delete))
              except discord.Forbidden:
               print(f"Missing permissions to delete messages in #{channel.name} of {guild.name}")

            print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} All explosion messages have been erased !")            

            # Pause for a specified duration
            await asyncio.sleep(10)

        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Channel unhiding started...")



        # Unhide all channels for the 'Explosion' role
        for channel in guild.text_channels:
            if channel.id != refuge_channel_id:
                try:
                    await channel.set_permissions(explosion_role, view_channel=True)
                except Exception as e:
                    print(f"{printer_timestamp()} Error unhiding channel {channel}: {e}")

        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} All channels have been successfully unhidden !")

        

        explosion_refuge_embed.title = "**🟢 Explosion Terminée 🟢**"
        explosion_refuge_embed.description = "Le serveur est de nouveau accessible !"

        explosion_refuge_embed.set_field_at(0, name=f"Merci à tous d'avoir participé ! :grin:",
                                                    value=f"Ce salon ainsi que le role <@&{explosion_role.id}> se supprimeront dans quelques instants...",
                                                    inline=False)
                
        explosion_refuge_embed.set_thumbnail(url=tada_icon_url)
        await refuge_embed_message.edit(embed=explosion_refuge_embed)


        # Set permissions for 'Explosion' role in the 'Refuge' channel
        await refuge_channel.set_permissions(explosion_role, send_messages=False)

        # Restore original roles for all members
        for member_id, roles in stored_roles.items():
            member = interaction.guild.get_member(member_id)
            if member:
                try:
                    await member.add_roles(*[interaction.guild.get_role(role_id) for role_id in roles if role_id != interaction.guild.default_role.id])
                except Exception as e:
                    print(f"{printer_timestamp()} Error while restoring roles for {member}: {e}")

        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} All members' roles have been restored !")

        # Pause for a specified duration
        await asyncio.sleep(30)

        # Delete the 'Refuge' channel
        await refuge_channel.delete()
        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Refuge channel deleted !")

        # Delete the 'Refuge' category
        await refuge_category.delete()
        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Refuge category deleted !")

        # Remove the 'Explosion' role from all members
        for member in members:
            if member != guild.owner:
                try:
                    await member.remove_roles(explosion_role)
                except Exception as e:
                    print(f"{printer_timestamp()} Error while removing the explosion role from {member}: {e}")

        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} The explosion role has been removed from all members !")

        # Delete the 'Explosion' role
        await explosion_role.delete()
        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} Explosion role deleted !")
        print(f"{printer_timestamp()} {interaction.guild.name} {interaction.guild.id} \033[92mThe explosion command system has been succesfully finished !\033[92m")


    except Exception as global_explosion_system_error:
        print(global_explosion_system_error)
        pass


client.run(token)