import discord
from discord import ui


# verification modal
class VerificationModal(ui.Modal, title="Enter Access Code"):
    code = ui.TextInput(label="Access Secret")

    @staticmethod
    def retrieve_tokens():
        with open("secrets.txt", "r") as f:
            tokens = f.readlines()
        return tokens

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        waiting_role = discord.utils.get(interaction.guild.roles, name="waiting")
        testorr_role = discord.utils.get(interaction.guild.roles, name="testorrrr🤓")

        tokens = self.retrieve_tokens()
        for secret in tokens:
            if str(self.code.value) in secret.strip():
                tokens.remove(secret)
                await interaction.user.add_roles(testorr_role)
                await interaction.user.remove_roles(waiting_role)
                await interaction.followup.send(
                    f"role {testorr_role.name} granted", ephemeral=True
                )
                break
        else:
            await interaction.followup.send("Invalid Access Code", ephemeral=True)

        with open("secrets.txt", "w") as f:
            f.writelines(tokens)


# verification button
class VerifyButton(ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.green)
        self.vermodal = VerificationModal()

    async def callback(self, interaction):
        await interaction.response.send_modal(self.vermodal)
