import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


# Kick command
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'Kicked {member.mention} for {reason}.')


# Ban command
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'Banned {member.mention} for {reason}.')


# Unban command
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f'Unbanned {user.mention}.')
      return


# Timeout command
@bot.command()
@commands.has_permissions(kick_members=True)
async def timeout(ctx, member: discord.Member, time: int, *, reason=None):
  await member.add_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
  await ctx.send(
    f'{member.mention} has been muted for {time} seconds for {reason}.')
  await asyncio.sleep(time)
  await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
  await ctx.send(f'{member.mention} has been unmuted.')


# Handle errors
@kick.error
async def kick_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please specify the member to kick.')
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send('You do not have permission to kick members.')


@ban.error
async def ban_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please specify the member to ban.')
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send('You do not have permission to ban members.')


@unban.error
async def unban_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please specify the member to unban.')
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send('You do not have permission to unban members.')


@timeout.error
async def timeout_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please specify the member to timeout.')
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send('You do not have permission to timeout members.')


@bot.event
async def on_ready():
  print('Bot is ready.')


@bot.command()
async def addrole(ctx, member: discord.Member, role: discord.Role):
  await member.add_roles(role)
  await ctx.send(f'{member.mention} has been given the {role.name} role.')


@bot.command()
async def removerole(ctx, member: discord.Member, role: discord.Role):
  await member.remove_roles(role)
  await ctx.send(f'{member.mention} has had the {role.name} role removed.')



