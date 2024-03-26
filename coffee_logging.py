from discord_webhook import DiscordWebhook, DiscordEmbed
import requests

class Notifications():
    def __init__(self, url:str, allowedNotifications:dict) -> None:
        '''
        Parameters:
            url - the discord webhook url, https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
            allowedNotifications - A dictionary containing what notifications to send
                Keys:
                    initialization
                    product_creation
                    price_creation
                    out_of_stock
                    purchase_successful
        '''
        self.notifications = allowedNotifications
        self.url = url

    def initialized(self) -> None:
        '''
        Sends a message notifying the user that the machine has been initialized
        '''

        if self.notifications["initialization"]:
            embed = DiscordEmbed(title="✅  Initialization Completed")

            DiscordWebhook(url=self.url, embeds=[embed]).execute()

    
    def priceCreated(self, product:str, slot: int, price:float) -> None:
        '''
        Sends a message notifying the user that a default price has been created for the specified product

        Parameters:
            product - The name of the product
            slot - The vending slot id of the product
            price - The default price that has been created
        '''

        if self.notifications["price_creation"]:
            embed = DiscordEmbed(title="🪙  Default Price Created",
                                description=f"A default price was not found for `{product}` in `vending slot {slot}`. A new price of `${price:.{2}f}` has been set.")

            DiscordWebhook(url=self.url, embeds=[embed]).execute()
    
    def productCreated(self, slot: int) -> None:
        '''
        Sends a message notifying the user that a placeholder product has been created

        Parameters:
            slot - The vending slot id of the product
        '''

        if self.notifications["product_creation"]:
            embed = DiscordEmbed(title="🔨  Placeholder Product Created",
                                description=f"A product was not found for `vending slot {slot}`. A placeholder product has been created to populate the slot. If this is a mistake add the `vending_slot` key to your products metadata.")

            DiscordWebhook(url=self.url, embeds=[embed]).execute()

    def unexpectedError(self, error:str) -> None:
        '''
        Send an error message in discord

        Parameters:
            error - the exception that was thrown
        '''
        embed = DiscordEmbed(title="💀  An Unkown Error Has Occoured",
                            description=f"Please investigate this issue, the program will now restart automatically.\n```python\n{error}```")
        
        DiscordWebhook(url=self.url, embeds=[embed]).execute()
