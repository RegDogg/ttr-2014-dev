# While dev.prc contains settings for both the dev server and client, the
# live server separates these. The client settings go in config/public_client.prc
# and server settings go here. Don't forget to update both if necessary.

# Server settings
want-dev #f
want-cheesy-expirations #t
cogsuit-hack-prevent #t


# Shared secret for CSMUD
# ##### NB! Update config/public_client.prc too! #####
csmud-secret Yv1JrpTUdkX6M86h44Z9q4AUaQYdFnectDgl2I5HOQf8CBh7LUZWpzKB9FBD


# Beta Modifications
# Temporary modifications for unimplemented features go here.
want-bbhq #f
want-pets #f
want-parties #f
want-accessories #f
want-golf #f
want-gardening #f
want-gifting #f
want-keep-alive #f

# Chat Settings
blacklist-sequence-url https://s3.amazonaws.com/cdn.toontownrewritten.com/misc/tsequence.dat
want-whitelist #t
want-blacklist-sequence #t


# Holidays and Events
want-mega-invasions #f
mega-invasion-cog-type tm
