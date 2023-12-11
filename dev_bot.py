import discord
from discord import app_commands
from datetime import datetime, timedelta
import pytz
import asyncio
import random
import os
import requests
import dotenv
import json
import time

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

print(f"\033[1m {printer_timestamp()} Token has been loaded ! \033[0m")

TGA25_ID = 845327664143532053


USER2_ID = 8482442444342559029


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False 

client = aclient()

dotenv.load_dotenv(f"{DEFAULT_PATH}/Token/twitch_authorization.env")
twitch_authorization = os.getenv(f"Twitch_Authorization")

print(f"{printer_timestamp()} Twitch authorization token has been loaded !")

dotenv.load_dotenv(f"{DEFAULT_PATH}/Token/twitch_client_id.env")
twitch_client_id = os.getenv(f"Twitch_Client_Id")

print(f"{printer_timestamp()} Twitch client id token has been loaded !")

headers = {
    'Client-Id': f'{twitch_client_id}',
    'Authorization': f'Bearer {twitch_authorization}',
    
}


async def check_shutdown_file():
    if os.path.isfile("shutdown.txt"):
        print(f"{printer_timestamp()} shutdown.txt file exist. \033[91m Bot stopping... \033[0m")
        os.remove("shutdown.txt") 
        await client.close()
        await asyncio.sleep(5)  
        os._exit(0)
    else:
        print(f"{printer_timestamp()} shutdown.txt file doesn't exist. \033[94m Bot starting... \033[0m")



asyncio.run(check_shutdown_file())

is_ready = False

@client.event
async def on_ready():

    try:
     bot_starting_embed = discord.Embed(
        title=":hourglass_flowing_sand: Lancement... :hourglass_flowing_sand: ",
        description="**Le bot est en cours de lancement veuillez patienter....**"

     )

     USER_DM = await client.fetch_user(TGA25_ID)
     message = await USER_DM.send(embed=bot_starting_embed)

     await tree.sync()
     print(f"{printer_timestamp()} Commands Synced !")

     print(f"{printer_timestamp()} Logged in as {client.user.name} !") 

     profile_image_path = f"{IMAGES_PATH}/default_image_{bot_mode_lc}_bot.png"

     profile_image = open(profile_image_path, "rb")
     pfp = profile_image.read()
        
     #await client.user.edit(avatar=pfp)

     print(f"{printer_timestamp()} Profile image sucessfully restablished to default !")

     
     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"/help | {version_number}"))
     print(f"{printer_timestamp()} Bot Status has been corectly set up !")

     # asyncio.create_task(twitch_loop())
     # print(f"{printer_timestamp()} Twitch script has been corectly loaded ! ")

    

     print(f"{printer_timestamp()} Twitch Loop starting in 30 seconds...")

     bot_started_embed = discord.Embed(
        title=":green_circle: Succès ! :green_circle:",
        description="**Le Bot a correctement démarré !** *__(N'oubliez pas de relancer les commandes nécessaires...)__* "

     )

     await asyncio.sleep(3)

     await message.edit(embed=bot_started_embed)

     try:
      with open("JSON Files/starting_time_average.json", 'r') as file:
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
     with open("JSON Files/starting_time_average.json", 'w') as file:
      json.dump(time_data, file)

     time_taken_values = [entry['time_taken'] for entry in time_data]

     average_time_taken = round(sum(time_taken_values) / len(time_taken_values), 1)

     

     print(f"{printer_timestamp()}\033[1;92m All startup operations have been completed in {time_taken}s ! \033[0m\033[1;35m(average is {average_time_taken}s)\033[0m")

     global is_ready
     is_ready = True

    except Exception as e:
       print(f"{printer_timestamp()} \033[1;91m Une erreur s'est produite durant le lancement du bot : \033[0m \033[91m{e} \033[0m")
       bot_start_error = discord.Embed(
          title="**:red_circle: Une erreur est survenue lors du démarage du bot :red_circle: **",
          description=f"**Detail de l'erreur :** `{e}` " 
          
       )
       USER_DM = await client.fetch_user(TGA25_ID)
       await USER_DM.send(embed=bot_start_error)
       pass
       

#VARIABLES   
         
restart_time = datetime.now()
tree = app_commands.CommandTree(client)
france_tz = pytz.timezone("Europe/Paris")
version_note = f"{bot_mode_hc} Arabot v2.0p|Ink Corp|✨TGA25✨"
maintenance_mode = False
default_bot_nick = f"{bot_mode_def} Arabot"
version_number = "v2.0p"
streamer_name = ("Ponce")


explosion_command_avalaible = True
vol_command_avalaible = True

#ID'S VARIABLES

news_channel_id = 1120722998673027082
                 
server_id = 1060183015545913354

bot_channel = 1120723328307581003

autorole_role = 1102260664401150024

#EVENTS






#EMBEDS

 #Help Embed
help_embed = discord.Embed(
        title="Help",
        description="Voici toutes mes commandes :",
        color=discord.Color.from_rgb(252, 165, 119)
)
help_embed.add_field(name="</explosion:1119281805477036194>", value="Fait exploser le serveur. (__Temporairement indisponible)", inline=False)

help_embed.add_field(name="</vol:1119281805477036195>", value="Vole le profil d'un membre du serveur. (__Temporairement indisponible)", inline=False)     

help_embed.add_field(name="</info:1119281805477036197>", value="Affiche les informations du bot.", inline=False)

help_embed.add_field(name="</help:1119281805477036196>", value="Affiche ceci.", inline=False)

help_embed.add_field(name="</admin:1119281805477036192>", value="Affiche le panel d'administration du bot **Commande réservée aux admins du bot**", inline=False)
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
error_embed.add_field(name= "L'erreur a été transmise au développeur :electric_plug:", value="")
error_embed.set_footer(text=version_note)




 #Explosion Force Embed

explosion_force_embed = discord.Embed(
        title="Explosion",
        color=discord.Color.from_rgb(252, 165, 3)
        
)
explosion_force_embed.add_field(name="**Niveau 1 💣**", value="Une explosion de force *1*. Rend inaccessible le serveur pendant 1 minute.", inline=False)
explosion_force_embed.add_field(name="**Niveau 2 🌋**", value="Une explosion de force *2*. Rend inaccessible le serveur pendant 5 minutes.", inline=False)
explosion_force_embed.add_field(name="**Niveau 3 🌪️**", value="Une explosion de force *3*. Rend inaccessible le serveur pendant 10 minutes.", inline=False)
explosion_force_embed.set_footer(text=version_note)

 #Dev Info Embed



dev_info_embed = discord.Embed(


        description="**Informations sur le developpeur du bot**",
        color=discord.Color.from_rgb(134, 27, 242)

        
        
)
dev_info_embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/845327664143532053/65a0b52e2a7b881a64c5769d8f12f359.png?size=512")
dev_info_embed.add_field(name="**Bonjour ! :wave: **", value="Moi c'est <@845327664143532053> <:activedevbadge:1107235074757373963>", inline=False)
dev_info_embed.add_field(name=f"**Développeur**", value="*Code en Python <:logo_python_arabot:1108367929457791116>*", inline=True)
dev_info_embed.add_field(name="**Youtubeur** <:logo_youtube_arabot:1108368195489910836>", value="*Clique* [ici](https://www.youtube.com/channel/UCCxw1YVUMs5czQuhTkJH3eQ)", inline=True)
dev_info_embed.add_field(name="", value=":arrow_right_hook: [Rejoindre le serveur de support](https://discord.gg/uGWkqYazzw) :leftwards_arrow_with_hook:  ", inline=False)
dev_info_embed.set_footer(text=version_note)


 #Give Role Embed

give_role_embed = discord.Embed(
    title="**Auto Rôle**",
    description=f"Cliquez sur le bouton ci dessous pour obtenir le rôle <@&{autorole_role}>",
    color=discord.Color.from_rgb(250, 235, 25)
   
)
give_role_embed.add_field(name="A quoi ça sert ?", value=f"En obtenant le rôle <@&{autorole_role}> vous êtes ainsi __abonnés__ aux *informations* concernant **l'Arabot**.")
give_role_embed.set_footer(text=version_note)


 #Command Unavalaible Embed

unavaileble_command_embed = discord.Embed(
   title="**Oups ! :face_with_monocle: **",
   description="Cette commande revient bientôt...",
   color=discord.Color.from_rgb(66, 135, 245),
   
)
unavaileble_command_embed.set_footer(text=version_note)

#BUTTON VIEWS

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
        

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Réinitialiser le profil", custom_id="button_reset", emoji="🔄")
    async def button1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot_user = interaction.guild.me
        await bot_user.edit(nick=None)


        default_profile_image_path = f"{IMAGES_PATH}/default_image_{bot_mode_lc}_bot.png"

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
        filename = "maintenance_on.txt"
        with open(filename, 'w') as f:
         pass   

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Fin de la maintenance", custom_id="button_end_maintenance", emoji="🛠️")
    async def button4_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
     await interaction.response.send_message("Mode maintenance **désactivé** 👷 !", ephemeral=True)

     await client.change_presence(activity=discord.Activity(status=discord.Status.do_not_disturb ,name="de retour... 🎉", type=discord.ActivityType.watching))  
          
     await asyncio.sleep(10)
     global maintenance_mode
     maintenance_mode=False

     channel = client.get_channel(bot_channel)
     if channel is not None:
        await channel.send("@everyone", embed=end_maintenance_embed)
     else:
        print(f"{printer_timestamp()} Channel not found!")
     await client.change_presence(activity=discord.Activity(status=discord.Status.online))

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Setup Auto_Role", custom_id="button_give_role")
    async def button5_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
       if interaction.user.id == TGA25_ID or USER2_ID:
         try:
          
         
          channel = client.get_channel(bot_channel)  # replace `channel_id` with the actual ID of the channel you want to send the message to
          await channel.send(embed=give_role_embed,view=ButtonView_give_roles())
          
         except Exception as e:
            print(f"{printer_timestamp()} {e}")

       else:
    
         await interaction.response.send_message("Seul @TGA25 est autorisé a utiliser cette commande :no_entry_sign: ", ephemeral=True)     



    @discord.ui.button(style=discord.ButtonStyle.primary, label="Réinitialiser les dm", custom_id="button_reset_private_messages", emoji="🗑️")
    async def button6_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
       for channel in client.private_channels:
            if isinstance(channel, discord.DMChannel):
                async for msg in channel.history(limit=None):
                    if msg.author == client.user:
                        await msg.delete()
                        await interaction.response.send_message("Tout les dm ont été supprimés !", ephemeral=True)



 #Button View Explosion Command
class ButtonView_explosion_command(discord.ui.View):
    def __init__(self):
        super().__init__()


#--------------------------------------------------------
#BUTTON LEVEL 1
#--------------------------------------------------------

    @discord.ui.button(style=discord.ButtonStyle.primary, label="1", custom_id="force1", emoji="💣")
    async def button1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        username_button_pressed = interaction.user.mention
        print(f"{printer_timestamp()} Level 1")

        current_time =  datetime.now(france_tz).strftime("%H:%M")
        current_date = datetime.now().strftime("%d-%m-%Y")  

         # Create and write to the file
        with open("explosion_info.txt", "w") as file:
         file.write(f"Commande utilisée par @{username_button_pressed} le {current_date} à {current_time}.")
    
        view = self
        for child in view.children:
         child.disabled = True

        await interaction.response.edit_message(view=view)

        await asyncio.sleep(1)
        
        await interaction.message.add_reaction("💣")

        

       

        await asyncio.sleep(3)
        guild = interaction.guild
        category = await guild.create_category("🏡Refuge🏡") #Crée la categorie

       
        channel = await guild.create_text_channel("❗venez❗", category=category) #Crée le salon
        await category.edit(position=0) #Met la categorie en haut de la liste


        for role in channel.guild.roles:
         await channel.set_permissions(role, send_messages=False)

        await asyncio.sleep(5)
        await channel.edit(name="🔰Refuge🔰") #Renome le salon

        await asyncio.sleep(3)

        refuge_channel_id = channel.id  #Recupere l'id du salon
        print(f"{printer_timestamp()} <#{refuge_channel_id}>")

        await asyncio.sleep(2)


        with open("user_explosion.txt", "w") as f: #Crée un .txt avec l'id de la personne qui a pressé le bouton
         f.write(f"{username_button_pressed}")

        await interaction.channel.send(f"@here ! Rejoignez le salon <#{refuge_channel_id}> !")

        await asyncio.sleep(2)

        #-------------------------------------------------------------------------------
        #Explosion Command Embed 
        with open("user_explosion.txt", 'r') as file:
         explosion_username = file.read()

        await asyncio.sleep(1)

        explosion_command_embed = discord.Embed( #Crée l'embed
        title="**🟢 Refuge 🟢**",
        description="Ce salon vous permet de patienter jusqu'à la fin des explosions.",
        color=discord.Color.from_rgb(158, 240, 91)        
        )
        explosion_command_embed.set_footer(text=f"{version_note}")
        explosion_command_embed.add_field(name="Le serveur va être inaccessible pendant *1* minute.", value=f"*On peut remercier{explosion_username} 👏👏*", inline=False)
        

        #-------------------------------------------------------------------------------
        channel_id = refuge_channel_id # Replace with the ID of the channel you want to send a message to

        await asyncio.sleep(2)

        refuge_channel = client.get_channel(channel_id)
        embed_message = await channel.send(embed=explosion_command_embed) #Envoi l'embed

        os.remove("user_explosion.txt") #Supprime le fichier .txt

        await asyncio.sleep(2)
   
        refuge_channel = client.get_channel(refuge_channel_id)
      
        await asyncio.sleep(2)

        for role in channel.guild.roles:
         await channel.set_permissions(role, send_messages=False) #Empeche les utilisateurs d'envoyer des messages

         await asyncio.sleep(1)

       #-------------------------------------------------------------------------------

        print(f"{printer_timestamp()} Explosion Started !") 
        async def send_messages_with_delays(guild, message_list, exception_channel_id=refuge_channel_id): #Lance l'explosion
         await asyncio.sleep(1)
         for message in message_list:
          for channel in guild.channels:
            if isinstance(channel, discord.TextChannel) and channel.id != exception_channel_id:
                try:
                    await channel.send(message)
                except:
                    # Handle any exceptions that may occur while sending the message to a channel
                    pass
        delay = random.randint(1, 5)  # Generate a random delay between 1 and 5 seconds
        await asyncio.sleep(delay)
        
        guild = client.get_guild(server_id)
        message = "💥💥💥💥💥"
        await send_messages_with_delays(guild, message)
        print(f"{printer_timestamp()} Explosion Ended !")

        await asyncio.sleep(3)

        print(f"{printer_timestamp()} Starting hidding channels...") 

        #-------------------------------------------------------------------------------

        explosion_command_embed_v2 = discord.Embed( #Crée l'embed v2
        title="**🟢 Refuge 🟢**",
        description="Ce salon vous permet de patienter jusqu'à ce que le serveur soit de nouveau accessible.",
        color=discord.Color.from_rgb(158, 240, 91)        
        )
        explosion_command_embed_v2.set_footer(text=f"{version_note}")
        explosion_command_embed_v2.add_field(name="Le serveur est inaccessible pendant *1* minute.", value=f"*On peut remercier{explosion_username} 👏👏*", inline=False)

        await embed_message.edit(embed=explosion_command_embed_v2)

        #-------------------------------------------------------------------------------

        exception_channel_id = refuge_channel_id  #Cache les salons du serveur
        for channel in guild.channels:
         if channel.id == exception_channel_id:
            await channel.set_permissions(interaction.guild.default_role, send_messages=True, view_channel=True)
         else:
            await channel.set_permissions(interaction.guild.default_role, send_messages=False, view_channel=False)
            print(f"{printer_timestamp()} The channel {channel.name} has been hidden !")

        print(f"{printer_timestamp()} All channels have been correctly hidden !")
        print(f"{printer_timestamp()} Waiting time started !")

        await channel.set_permissions(role, send_messages=False) #Bloque les messages dans le salon

        waitmessage = await channel.send(":lock:")

        await asyncio.sleep(2)

        await waitmessage.edit(content=":clock12: ")
        print(f"{printer_timestamp()} 60s remaining")

        await channel.set_permissions(role, send_messages=False)

        await asyncio.sleep(15)

        await waitmessage.edit(content=":clock3:")  #Actualise le message
        print(f"{printer_timestamp()} 45s remaining")

        await asyncio.sleep(15)

        await waitmessage.edit(content=":clock1230:")
        print(f"{printer_timestamp()} 30s remaining")

        await asyncio.sleep(15)

        await waitmessage.edit(content=":clock9: ")
        print(f"{printer_timestamp()} 15s remaining")

        await asyncio.sleep(15)

        await waitmessage.edit(content=":unlock:")
        print(f"{printer_timestamp()} Waiting time ended !")

        await asyncio.sleep(2)

        #-------------------------------------------------------------------------------

        for channel in guild.channels:
           await channel.set_permissions(interaction.guild.default_role, send_messages=True, view_channel=True)
           print(f"{printer_timestamp()} Server channel {channel.name} with the id {channel_id} has been unhidden !")

        explosion_command_embed_v3 = discord.Embed( #Crée l'embed v3
        title="**🟢 Explosion Terminée 🟢**",
        description="Le serveur est de nouveau accessible !",
        color=discord.Color.from_rgb(158, 240, 91)        
        )
        explosion_command_embed_v3.add_field(name="Ce salon se supprimera dans quelques instants...", value="", inline=False)
        explosion_command_embed_v3.set_footer(text=f"{version_note}")
        

        await embed_message.edit(embed=explosion_command_embed_v3)

        await asyncio.sleep(10)     #Montre les salons a nouveau

        await channel.delete()
        await category.delete()
        print(f"{printer_timestamp()} Refuge channel and refuge category have been deleted !") #Supprime le refuge

#--------------------------------------------------------
#BUTTON LEVEL 2
#--------------------------------------------------------
          
    @discord.ui.button(style=discord.ButtonStyle.primary, label="2", custom_id="force2", emoji="🌋")
    async def button2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
     username_button_pressed = interaction.user.mention
     print(f"{printer_timestamp()} Level 2")

     view = self
     for child in view.children:
      if isinstance(child, discord.ui.Button):
        child.disabled = True

     await interaction.response.edit_message(view=view)


     await asyncio.sleep(1)
        
     await interaction.message.add_reaction("🌋")
       

     await asyncio.sleep(3)
     guild = interaction.guild
     category = await guild.create_category("🏡Refuge🏡") #Crée la categorie

       
     channel = await guild.create_text_channel("❗venez❗", category=category) #Crée le salon
     await category.edit(position=0) #Met la categorie en haut de la liste

     for role in channel.guild.roles:
      await channel.set_permissions(role, send_messages=False)

     await asyncio.sleep(5)
     await channel.edit(name="🔰Refuge🔰") #Renome le salon

     await asyncio.sleep(3)

     refuge_channel_id = channel.id  #Recupere l'id du salon
     print(f"{printer_timestamp()} <#{refuge_channel_id}>")

     await asyncio.sleep(2)


     with open("user_explosion.txt", "w") as f: #Crée un .txt avec l'id de la personne qui a pressé le bouton
      f.write(f"{username_button_pressed}")

     await interaction.channel.send(f"@here! Rejoignez le salon <#{refuge_channel_id}> !")

     await asyncio.sleep(2)

     #-------------------------------------------------------------------------------
     #Explosion Command Embed 
     with open("user_explosion.txt", 'r') as file:
      explosion_username = file.read()

     await asyncio.sleep(1)

     explosion_command_embed = discord.Embed( #Crée l'embed
     title="**🟢 Refuge 🟢**",
     description="Ce salon vous permet de patienter jusqu'à la fin des explosions.",
     color=discord.Color.from_rgb(158, 240, 91)        
     )
     explosion_command_embed.set_footer(text=f"{version_note}")
     explosion_command_embed.add_field(name="Le serveur va être inaccessible pendant *5* minutes.", value=f"*On peut remercier{explosion_username} 👏👏*", inline=False)
        

     #-------------------------------------------------------------------------------
     channel_id = refuge_channel_id # Replace with the ID of the channel you want to send a message to

     await asyncio.sleep(2)

     refuge_channel = client.get_channel(channel_id)
     embed_message = await channel.send(embed=explosion_command_embed) #Envoi l'embed

     os.remove("user_explosion.txt") #Supprime le fichier .txt

     await asyncio.sleep(2)
   
     refuge_channel = client.get_channel(refuge_channel_id)
      
     await asyncio.sleep(2)

     for role in channel.guild.roles:
        await channel.set_permissions(role, send_messages=False) #Empeche les utilisateurs d'envoyer des messages

        await asyncio.sleep(1)

       #-------------------------------------------------------------------------------

        print(f"{printer_timestamp()} Explosion Started !") 
        async def send_messages_with_delays(guild, message_list, exception_channel_id=refuge_channel_id): #Lance l'explosion
         await asyncio.sleep(1)
         for message in message_list:
          for channel in guild.channels:
            if isinstance(channel, discord.TextChannel) and channel.id != exception_channel_id:
                try:
                    await channel.send(message)
                except:
                    # Handle any exceptions that may occur while sending the message to a channel
                    pass
        delay = random.randint(1, 5)  # Generate a random delay between 1 and 5 seconds
        await asyncio.sleep(delay)
        
        guild = client.get_guild(server_id)
        message = "💥💥💥💥💥💥💥💥💥💥"
        await send_messages_with_delays(guild, message)
        print(f"{printer_timestamp()} Explosion Ended !")

        await asyncio.sleep(3)

        print(f"{printer_timestamp()} Starting hidding channels...") 

        #-------------------------------------------------------------------------------

        explosion_command_embed_v2 = discord.Embed( #Crée l'embed v2
        title="**🟢 Refuge 🟢**",
        description="Ce salon vous permet de patienter jusqu'à ce que le serveur soit de nouveau accessible.",
        color=discord.Color.from_rgb(158, 240, 91)        
        )
        explosion_command_embed_v2.set_footer(text=f"{version_note}")
        explosion_command_embed_v2.add_field(name="Le serveur est inaccessible pendant *5* minutes.", value=f"*On peut remercier{explosion_username} 👏👏*", inline=False)

        await embed_message.edit(embed=explosion_command_embed_v2)

        #-------------------------------------------------------------------------------

        exception_channel_id = refuge_channel_id  #Cache les salons du serveur
        for channel in guild.channels:
         if channel.id == exception_channel_id:
            await channel.set_permissions(interaction.guild.default_role, send_messages=True, view_channel=True)
         else:
            await channel.set_permissions(interaction.guild.default_role, send_messages=False, view_channel=False)
            print(f"{printer_timestamp()} The channel {channel.name} has been hidden !")

        print(f"{printer_timestamp()} All channels have been correctly hidden !")
        print(f"{printer_timestamp()} Waiting time started !")

        await channel.set_permissions(role, send_messages=False) #Bloque les messages dans le salon

        waitmessage = await channel.send(":lock:")

        await asyncio.sleep(2)

        await waitmessage.edit(content=":clock12: ")
        print(f"{printer_timestamp()} 5m reamaining")

        await channel.set_permissions(role, send_messages=False)

        await asyncio.sleep(75)

        await waitmessage.edit(content=":clock3:")  #Actualise le message
        print(f"{printer_timestamp()} 3m and 75s reamaining")

        await asyncio.sleep(75)

        await waitmessage.edit(content=":clock1230:")
        print(f"{printer_timestamp()} 2m and 5s reamaining")

        await asyncio.sleep(75)

        await waitmessage.edit(content=":clock9: ")
        print(f"{printer_timestamp()} 1m and 25s reamaining")

        await asyncio.sleep(75)

        await waitmessage.edit(content=":unlock:")
        print(f"{printer_timestamp()} Waiting time ended !")

        await asyncio.sleep(2)

        #-------------------------------------------------------------------------------

        for channel in guild.channels:
           await channel.set_permissions(interaction.guild.default_role, send_messages=True, view_channel=True)
           print(f"{printer_timestamp()} Server channel {channel.name} with the id {channel_id} has been unhidden !")

        explosion_command_embed_v3 = discord.Embed( #Crée l'embed v3
        title="**🟢 Explosion Terminée 🟢**",
        description="Le serveur est de nouveau accessible !",
        color=discord.Color.from_rgb(158, 240, 91)        
        )
        explosion_command_embed_v3.add_field(name="Ce salon se supprimera dans quelques instants...", value="", inline=False)
        explosion_command_embed_v3.set_footer(text=f"{version_note}")
        

        await embed_message.edit(embed=explosion_command_embed_v3)

        await asyncio.sleep(10)   

        await channel.delete()
        await category.delete()
        print(f"{printer_timestamp()} Refuge channel and refuge category have been deleted !") #Supprime le refuge
   
#--------------------------------------------------------
#BUTTON LEVEL 3
#-------------------------------------------------------- 

    @discord.ui.button(style=discord.ButtonStyle.primary, label="3", custom_id="force3", emoji="🌪️")
    async def button3_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        username_button_pressed = interaction.user.mention
        print(f"{printer_timestamp()} Level 3")

        view = self
        for child in view.children:
         if isinstance(child, discord.ui.Button):
          child.disabled = True

        await interaction.response.edit_message(view=view)

        await asyncio.sleep(1)
        
        await interaction.message.add_reaction("🌪️")
       

        await asyncio.sleep(3)
        guild = interaction.guild
        category = await guild.create_category("🏡Refuge🏡") #Crée la categorie

       
        channel = await guild.create_text_channel("❗venez❗", category=category) #Crée le salon
        await category.edit(position=0) #Met la categorie en haut de la liste

        for role in channel.guild.roles:
         await channel.set_permissions(role, send_messages=False)

        await asyncio.sleep(5)
        await channel.edit(name="🔰Refuge🔰") #Renome le salon

        await asyncio.sleep(3)

        refuge_channel_id = channel.id  #Recupere l'id du salon
        print(f"{printer_timestamp()} <#{refuge_channel_id}>")

        await asyncio.sleep(2)


        with open("user_explosion.txt", "w") as f: #Crée un .txt avec l'id de la personne qui a pressé le bouton
         f.write(f"{username_button_pressed}")

        await interaction.channel.send(f"@here ! Rejoignez le salon <#{refuge_channel_id}> !")

        await asyncio.sleep(2)

        #-------------------------------------------------------------------------------
        #Explosion Command Embed 
        with open("user_explosion.txt", 'r') as file:
         explosion_username = file.read()

        await asyncio.sleep(1)

        explosion_command_embed = discord.Embed( #Crée l'embed
        title="**🟢 Refuge 🟢**",
        description="Ce salon vous permet de patienter jusqu'à la fin des explosions.",
        color=discord.Color.from_rgb(158, 240, 91)        
        )
        explosion_command_embed.set_footer(text=f"{version_note}")
        explosion_command_embed.add_field(name="Le serveur va être inaccessible pendant *10* minutes.", value=f"*On peut remercier{explosion_username} 👏👏*", inline=False)
        

        #-------------------------------------------------------------------------------
        channel_id = refuge_channel_id # Replace with the ID of the channel you want to send a message to

        await asyncio.sleep(2)

        refuge_channel = client.get_channel(channel_id)
        embed_message = await channel.send(embed=explosion_command_embed) #Envoi l'embed

        os.remove("user_explosion.txt") #Supprime le fichier .txt

        await asyncio.sleep(2)
   
        refuge_channel = client.get_channel(refuge_channel_id)
      
        await asyncio.sleep(2)

        for role in channel.guild.roles:
         await channel.set_permissions(role, send_messages=False) #Empeche les utilisateurs d'envoyer des messages

         await asyncio.sleep(1)

       #-------------------------------------------------------------------------------

        print(f"{printer_timestamp()} Explosion Started !") 
        async def send_messages_with_delays(guild, message_list, exception_channel_id=refuge_channel_id): #Lance l'explosion
         await asyncio.sleep(1)
         for message in message_list:
          for channel in guild.channels:
            if isinstance(channel, discord.TextChannel) and channel.id != exception_channel_id:
                try:
                    await channel.send(message)
                except:
                    # Handle any exceptions that may occur while sending the message to a channel
                    pass
        delay = random.randint(1, 5)  # Generate a random delay between 1 and 5 seconds
        await asyncio.sleep(delay)
        
        guild = client.get_guild(server_id)
        message = "💥💥💥💥💥💥💥💥💥💥💥💥💥💥💥"
        await send_messages_with_delays(guild, message)
        print(f"{printer_timestamp()} Explosion Ended !")

        await asyncio.sleep(3)

        print(f"{printer_timestamp()} Starting hidding channels...") 

        #-------------------------------------------------------------------------------

        explosion_command_embed_v2 = discord.Embed( #Crée l'embed v2
        title="**🟢 Refuge 🟢**",
        description="Ce salon vous permet de patienter jusqu'à ce que le serveur soit de nouveau accessible.",
        color=discord.Color.from_rgb(158, 240, 91)        
        )
        explosion_command_embed_v2.set_footer(text=f"{version_note}")
        explosion_command_embed_v2.add_field(name="Le serveur est inaccessible pendant *10* minutes.", value=f"*On peut remercier{explosion_username} 👏👏*", inline=False)

        await embed_message.edit(embed=explosion_command_embed_v2)

        #-------------------------------------------------------------------------------

        exception_channel_id = refuge_channel_id  #Cache les salons du serveur
        for channel in guild.channels:
         if channel.id == exception_channel_id:
            await channel.set_permissions(interaction.guild.default_role, send_messages=True, view_channel=True)
         else:
            await channel.set_permissions(interaction.guild.default_role, send_messages=False, view_channel=False)
            print(f"{printer_timestamp()} The channel {channel.name} has been hidden !")

        print(f"{printer_timestamp()} All channels have been correctly hidden !")
        print(f"{printer_timestamp()} Waiting time started !")

        await channel.set_permissions(role, send_messages=False) #Bloque les messages dans le salon

        waitmessage = await channel.send(":lock:")

        await asyncio.sleep(2)

        await waitmessage.edit(content=":clock12: ")
        print(f"{printer_timestamp()} 10m remaining")

        await channel.set_permissions(role, send_messages=False)

        await asyncio.sleep(150)

        await waitmessage.edit(content=":clock3:")  #Actualise le message
        print(f"{printer_timestamp()} 7m and 5s remaining")

        await asyncio.sleep(150)

        await waitmessage.edit(content=":clock1230:")
        print(f"{printer_timestamp()} 5m remaining")

        await asyncio.sleep(150)

        await waitmessage.edit(content=":clock9: ")
        print(f"{printer_timestamp()} 2m and 5s remaining")

        await asyncio.sleep(150)

        await waitmessage.edit(content=":unlock:")
        print(f"{printer_timestamp()} Waiting time ended !")

        await asyncio.sleep(3)

        #-------------------------------------------------------------------------------

        for channel in guild.channels:
           await channel.set_permissions(interaction.guild.default_role, send_messages=True, view_channel=True) #Montre les salons a nouveau
           print(f"{printer_timestamp()} Server channel {channel.name} with the id {channel_id} has been unhidden !") 

        explosion_command_embed_v3 = discord.Embed( #Crée l'embed v3
        title="**🟢 Explosion Terminée 🟢**",
        description="Le serveur est de nouveau accessible !",
        color=discord.Color.from_rgb(158, 240, 91)        
        )
        explosion_command_embed_v3.add_field(name="Ce salon se supprimera dans quelques instants...", value="", inline=False)
        explosion_command_embed_v3.set_footer(text=f"{version_note}")
        

        await embed_message.edit(embed=explosion_command_embed_v3)

        await asyncio.sleep(10)   


        await channel.delete()
        await category.delete()
        print(f"{printer_timestamp()} Refuge channel and refuge category have been deleted !") #Supprime le refuge

 #Button View Roles Give

class ButtonView_give_roles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    custom_plus_emoji = discord.PartialEmoji(name="signe_plus", id=1115292103824658483, animated=False)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Obtenir", custom_id="button_obtain", emoji=custom_plus_emoji)
    async def button1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
     
  

      # ID of the role to add

     role = interaction.guild.get_role(autorole_role) # Get the role

     user = interaction.user # Get the user who clicked the button

     await user.add_roles(role) # Add the role to the user

     given_autorole_embed = discord.Embed( 
        title="",
        description=f"{user.mention} tu as reçu le rôle <@&{autorole_role}> !",
        color=discord.Color.from_rgb(235, 218, 30)        
     )

     await interaction.response.send_message(embed=given_autorole_embed, ephemeral=True)

    custom_minus_emoji = discord.PartialEmoji(name="signe_moins", id=1115292072396726346, animated=False)

    @discord.ui.button(style=discord.ButtonStyle.danger, label="Retirer", custom_id="button_remove", emoji=custom_minus_emoji)
    async def button2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
    # Your callback code here

     
      # ID of the role to remove

     role = interaction.guild.get_role(autorole_role) # Get the role

     user = interaction.user # Get the user who clicked the button

     await user.remove_roles(role) # Remove the role from the user

     removed_autorole_embed = discord.Embed( 
        title="",
        description=f"{user.mention} le rôle <@&{autorole_role}> t'as été retiré !",
        color=discord.Color.from_rgb(235, 218, 30)        
     )

     await interaction.response.send_message(embed=removed_autorole_embed, ephemeral=True)



#SELECT VIEWS  

 #Select Admin Menu

# Create the embed


class AdminSelectMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=10)


        options = [
            discord.SelectOption(label="Statuts", value="status_embed_option", emoji="🟢"),
            discord.SelectOption(label="Paramètres", value="parameters_embed_option", emoji="⚙️"),
            discord.SelectOption(label="Informations", value="information_embed_option", emoji="ℹ️"),
          
        ]
        
        select = discord.ui.Select(options=options, placeholder="Options d'administration", min_values=1, max_values=1)
        select.callback = self.select_callback
        self.add_item(select)

    

    
    async def select_callback(self, interaction):
        
          
        current_time = datetime.now(france_tz).strftime("%H:%M")
        info_embed1 = discord.Embed(
        title="Infos",
        color=discord.Color.from_rgb(60, 240, 132)
        )
        info_embed1.add_field(name="**Ping 🏓**", value=f"*{round(client.latency, 3)}* ms de latence", inline=False)
        info_embed1.add_field(name="**Heure 🕐**", value=f"Il est {current_time}", inline=False)
        info_embed1.add_field(name="**Dernier redémarrage 🔄**", value=f"<t:{int(restart_time.timestamp())}>", inline=False) # Bot restart date and time field
        info_embed1.add_field(name="**Langage de programmation 🌐**", value="__Python__ <:logo_python_arabot:1108367929457791116>", inline=False) # Bot restart date and time field
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



@tree.command(name="admin", description="Affiche le panel d'administration du bot")
async def admin_panel(interaction: discord.Interaction):
    current_time = datetime.now(france_tz).strftime("%H:%M")

    current_date = datetime.now().strftime("%d-%m-%Y")  

    command_name = interaction.data['name']

    user_id = interaction.user.id

    command_id = interaction.data['id']

    guild_name = interaction.guild.name

    TGA25_ID = "845327664143532053"  
    USER_DM = await client.fetch_user(TGA25_ID)

    try:
     if interaction.user.id == TGA25_ID or USER2_ID:
         view = AdminSelectMenu()
         message = await interaction.response.send_message(content="Administration du bot :",view=view)

     else:
      await interaction.response.send_message("Tu n'es pas autorisé a utiliser cette commande :no_entry_sign: ", ephemeral=True)
      
   
    except Exception as e:

        error_dminfo_embed = discord.Embed( 
        title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
        description=f"**Erreur causée par** <@{user_id}>",
        color=discord.Color.from_rgb(245, 170, 66)        
        )
        
        error_dminfo_embed.add_field(name="Details :", value=f"Erreur survenue le `{current_date}` à `{current_time}` à `{current_time}` dans le serveur `{guild_name}`", inline=True)
        error_dminfo_embed.add_field(name="**Commande :**", value=f"`{command_name}`", inline=True)
        error_dminfo_embed.add_field(name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
        error_dminfo_embed.add_field(name="Erreur :", value=f"`{e}`", inline=False)
        error_dminfo_embed.set_footer(text=f"{version_note}")

        
        await USER_DM.send(embed=error_dminfo_embed)
        await interaction.response.send_message(embed=error_embed, ephemeral=True)
      


@tree.command(name="explosion", description="Boum !")
async def explosion_command(interaction: discord.Interaction):

    if explosion_command_avalaible == False :

     await interaction.response.send_message(embed=unavaileble_command_embed, ephemeral=True)

    elif explosion_command_avalaible == True :

     user_id = interaction.user.id
    
     current_date = datetime.now().strftime("%d-%m-%Y") 
    
     current_time = datetime.now(france_tz).strftime("%H:%M")

     command_name = interaction.data['name']

     command_id = interaction.data['id']

     guild_name = interaction.guild.name

     TGA25_ID = "845327664143532053"  
     USER_DM = await client.fetch_user(TGA25_ID)
  


     try:
      if maintenance_mode:
        await interaction.response.send_message(embed=maintenance_embed)
        return
      await interaction.response.send_message(content="Sélectionnez une force d'explosion :",view=ButtonView_explosion_command(), embed=explosion_force_embed)

     except Exception as e:
        error_dminfo_embed = discord.Embed( 
        title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
        description=f"**Erreur causée par** <@{user_id}>",
        color=discord.Color.from_rgb(245, 170, 66)        
        )
        
        error_dminfo_embed.add_field(name="Details :", value=f"Erreur survenue le `{current_date}` à `{current_time}` à `{current_time}` dans le serveur `{guild_name}`", inline=True)
        error_dminfo_embed.add_field(name="**Commande :**", value=f"`{command_name}`", inline=True)
        error_dminfo_embed.add_field(name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
        error_dminfo_embed.add_field(name="Erreur :", value=f"`{e}`", inline=False)
        error_dminfo_embed.set_footer(text=f"{version_note}")

        
        await USER_DM.send(embed=error_dminfo_embed)
        await interaction.response.send_message(embed=error_embed, ephemeral=True)


# ... (imports and constants)

@tree.command(name="vol", description="Vole le nom d'un utilisateur")
async def vol_command(interaction: discord.Interaction, user: discord.Member):
    if vol_command_avalaible == False:
        await interaction.response.send_message(embed=unavaileble_command_embed, ephemeral=True)
    elif vol_command_avalaible == True:
        current_time = datetime.now(france_tz).strftime("%H:%M")
        current_date = datetime.now().strftime("%d-%m-%Y")
        user_id = interaction.user.id
        command_name = interaction.data['name']
        command_id = interaction.data['id']
        guild_name = interaction.guild.name
        TGA25_ID = "845327664143532053"
        USER_DM = await client.fetch_user(TGA25_ID)

        try:
            if maintenance_mode:
                await interaction.response.send_message(embed=maintenance_embed)
            else:
                try:
                    with open("JSON Files/vol_command_cooldown.json", 'r') as f:
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
                        with open(f"Images/{choosen_user}.png", "wb") as f:
                            f.write(response.content)
                            print(f"{printer_timestamp()} Image downloaded successfully!")
                    else:
                        print(f"{printer_timestamp()} Failed to download image.")

                    # Update the bot's username to match the username of the mentioned user
                    profile_image_path = f"Images/{choosen_user}.png"
                    profile_image = open(profile_image_path, 'rb')
                    pfp = profile_image.read()

                    await interaction.response.send_message(f"J'ai volé le profil de <@{user.id}> :tada::tada: ! ", ephemeral=True)

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
                        profile_image_path = f"{IMAGES_PATH}/default_image_{bot_mode_lc}_bot.png"
                        profile_image = open(profile_image_path, "rb")
                        pfp = profile_image.read()

                        await client.user.edit(avatar=pfp)
                        print(f"{printer_timestamp()} Profile image successfully reestablished to default!")
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

                    await interaction.response.send_message(f"Veuillez patienter *{remaining_minutes} minutes* et *{remaining_seconds} secondes* avant de pouvoir réutiliser cette commande.", ephemeral=True)

                # Save the updated server cooldown data to the JSON file
                with open("JSON Files/vol_command_cooldown.json", 'w') as f:
                    json.dump(server_cooldowns, f)

        except Exception as e:
            print(e)
            error_dminfo_embed = discord.Embed(
                title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
                description=f"**Erreur causée par** <@{user.id}>",
                color=discord.Color.from_rgb(245, 170, 66)
            )

            error_dminfo_embed.add_field(name="Details :",
                                         value=f"Erreur survenue le `{current_date}` à `{current_time}` dans le serveur `{guild_name}`",
                                         inline=True)
            error_dminfo_embed.add_field(name="**Commande :**", value=f"`{command_name}`", inline=True)
            error_dminfo_embed.add_field(name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
            error_dminfo_embed.add_field(name="Erreur :", value=f"`{e}`", inline=False)
            error_dminfo_embed.set_footer(text=f"{version_note}")

            await USER_DM.send(embed=error_dminfo_embed)
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

          

        
@tree.command(name="help", description="Affiche les commandes disponibles")
async def embed_command(interaction: discord.Interaction):
    user_id = interaction.user.id

    current_date = datetime.now().strftime("%d-%m-%Y") 

    current_time = datetime.now(france_tz).strftime("%H:%M")

    command_name = interaction.data['name']

    command_id = interaction.data['id']

    guild_name = interaction.guild.name

    TGA25_ID = "845327664143532053"  
    USER_DM = await client.fetch_user(TGA25_ID)





    if maintenance_mode:
        await interaction.response.send_message(embed=maintenance_embed)
        return
    try:
     await interaction.response.send_message(embed=help_embed, ephemeral=False)

    except Exception as e:
        error_dminfo_embed = discord.Embed( 
        title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
        description=f"**Erreur causée par** <@{user_id}>",
        color=discord.Color.from_rgb(245, 170, 66)        
        )
        
        error_dminfo_embed.add_field(name="Details :", value=f"Erreur survenue le `{current_date}` à `{current_time}` dans le serveur `{guild_name}`", inline=True)
        error_dminfo_embed.add_field(name="**Commande :**", value=f"`{command_name}`", inline=True)
        error_dminfo_embed.add_field(name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
        error_dminfo_embed.add_field(name="Erreur :", value=f"`{e}`", inline=False)
        error_dminfo_embed.set_footer(text=f"{version_note}")

        
        await USER_DM.send(embed=error_dminfo_embed)
        await interaction.response.send_message(embed=error_embed, ephemeral=True)
        

    




@tree.command(name="info", description="Affiche des informations à propos du bot")
async def embed_command(interaction: discord.Interaction):
    current_time = datetime.now(france_tz).strftime("%H:%M")

    current_date = datetime.now().strftime("%d-%m-%Y") 

    user_id = interaction.user.id

    command_name = interaction.data['name']

    command_id = interaction.data['id']

    guild_name = interaction.guild.name

    TGA25_ID = "845327664143532053"  
    USER_DM = await client.fetch_user(TGA25_ID)




    if maintenance_mode:
        await interaction.response.send_message(embed=maintenance_embed)
        return
    try:

     current_time = datetime.now(france_tz).strftime("%H:%M")

    # Create the embed
     info_embed2 = discord.Embed(
     title="Infos",
     color=discord.Color.from_rgb(60, 240, 132)
     )
     info_embed2.add_field(name="**Ping 🏓**", value=f"*{round(client.latency, 3)}* ms de latence", inline=False)
     info_embed2.add_field(name="**Heure 🕐**", value=f"Il est *{current_time}* ", inline=False)
     info_embed2.add_field(name="**Dernier redémarrage 🔄**", value=f"<t:{int(restart_time.timestamp())}>" ,inline=False) # Bot restart date and time field
     info_embed2.add_field(name="**Langage de programmation 🌐**", value="*__Python__*" ,inline=False) # Bot restart date and time field
     info_embed2.set_footer(text=version_note)

     await interaction.response.send_message(embed=info_embed2, ephemeral=False)

    except Exception as e:
        error_dminfo_embed = discord.Embed( 
        title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
        description=f"**Erreur causée par** <@{user_id}>",
        color=discord.Color.from_rgb(245, 170, 66)        
        )
        
        error_dminfo_embed.add_field(name="Details :", value=f"Erreur survenue le `{current_date}` à `{current_time}` dans le serveur `{guild_name}`", inline=True)
        error_dminfo_embed.add_field(name="**Commande :**", value=f"`{command_name}`", inline=True)
        error_dminfo_embed.add_field(name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
        error_dminfo_embed.add_field(name="Erreur :", value=f"`{e}`", inline=False)
        error_dminfo_embed.set_footer(text=f"{version_note}")

        
        await USER_DM.send(embed=error_dminfo_embed)
        await interaction.response.send_message(embed=error_embed, ephemeral=True)

@tree.command(name="devinfo", description="Affiche des informations à propos du développeur")
async def dev_info_command(interaction: discord.Interaction):
 current_time = datetime.now(france_tz).strftime("%H:%M")

 current_date = datetime.now().strftime("%d-%m-%Y") 

 command_name = interaction.data['name']

 user_id = interaction.user.id

 command_id = interaction.data['id']

 guild_name = interaction.guild.name

 TGA25_ID = "845327664143532053"  
 USER_DM = await client.fetch_user(TGA25_ID)
   
   

 try:
    emoji_id = 1107235074757373963 # Replace with the ID of your custom emoji
    myemoji = client.get_emoji(emoji_id)
    await interaction.response.send_message(content= myemoji, embed=dev_info_embed)

 except Exception as e:
        error_dminfo_embed = discord.Embed( 
        title="**:red_circle: Une erreur est survenue sur l'un des serveurs :red_circle: **",
        description=f"**Erreur causée par** <@{user_id}>",
        color=discord.Color.from_rgb(245, 170, 66)        
        )
        
        error_dminfo_embed.add_field(name="Details :", value=f"Erreur survenue le `{current_date}` à `{current_time}` dans le serveur `{guild_name}`", inline=True)
        error_dminfo_embed.add_field(name="**Commande :**", value=f"`{command_name}`", inline=True)
        error_dminfo_embed.add_field(name="**ID de la commande :**", value=f"`{command_id}`", inline=True)
        error_dminfo_embed.add_field(name="Erreur :", value=f"`{e}`", inline=False)
        error_dminfo_embed.set_footer(text=f"{version_note}")

        
        await USER_DM.send(embed=error_dminfo_embed)
        await interaction.response.send_message(embed=error_embed, ephemeral=True)

#Twitch Live Alert Loop

async def twitch_loop():
   while not is_ready:
        await asyncio.sleep(30)
        print(f"{printer_timestamp()} Twitch Loop has been started !")

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



            width = 300
            height = 200
            resized_thumbnail_url = thumbnail_url.replace('{width}', str(width)).replace('{height}', str(height))

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
                twitch_message_channel = client.get_channel(news_channel_id)

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

                 await twitch_message_channel.send(content="@everyone",embed=twitch_live_embed)
                 print(f"{printer_timestamp()} Twitch Live Alert has been sent ! (in channel : {twitch_message_channel})")


                

            previous_status = current_status

     else:
        if response.status_code == 429:
            print(f"{printer_timestamp()} ! RATE LIMIT !")
        else:    

         print(f"{printer_timestamp()} Request returned status code {response.status_code}")
         print(response.text)

     await asyncio.sleep(10)
    


# Load cooldowns from the JSON file
try:
    with open('server_cooldowns.json', 'r') as f:
        server_cooldowns = json.load(f)
except FileNotFoundError:
    server_cooldowns = {}

# Command with server-wide cooldown
@tree.command(name='example', description='Example command with server-wide cooldown')
async def example_command(interaction: discord.Interaction):
    # Check if the server is on cooldown
    guild_id = str(interaction.guild_id)
    

    if guild_id not in server_cooldowns:
        server_cooldowns[guild_id] = 0

    current_time = time.time()
    cooldown_time = 60  # Change this to the desired cooldown time in seconds

    if current_time - server_cooldowns[guild_id] > cooldown_time:
        # Server is not on cooldown, proceed with the command
        await interaction.response.send_message("Example command executed!")
        server_cooldowns[guild_id] = current_time  # Update the cooldown time for the server
    else:
        # Server is on cooldown, inform users
        remaining_time = int(cooldown_time - (current_time - server_cooldowns[guild_id]))
        await interaction.response.send_message(f"The server is on cooldown. Please wait {remaining_time} seconds.")
        

    # Save the updated server cooldown data to the JSON file
    with open('server_cooldowns.json', 'w') as f:
        json.dump(server_cooldowns, f)
       
        
#---------------------------------------       
#Commands Cooldowns
#--------------------------------------- 

@vol_command.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        remaining_time = round(error.retry_after, 2)
        message = f"Veuillez patienter {round(error.retry_after/60, 2)} minutes avant de pouvoir réutiliser cette commande.... :hourglass:"
        await interaction.response.send_message(message, ephemeral=True)


@explosion_command.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        remaining_time = timedelta(seconds=round(error.retry_after))
        days, seconds = remaining_time.days, remaining_time.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        message = f"Veuillez patienter {days}j, {hours}h, {minutes}m, {seconds}s avant de pouvoir refaire exploser le serveur.... :hourglass:"
        await interaction.response.send_message(message, ephemeral=True)



client.run(token)