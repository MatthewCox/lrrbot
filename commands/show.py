from lrrbot import bot
import storage
import utils

def set_show(lrrbot, show):
	if lrrbot.show != show.lower():
		lrrbot.show = show.lower()
		lrrbot.get_current_game_real.reset_throttle()

def show_name(show):
	return storage.data.get("shows", {}).get(show, {}).get("name", show)

@bot.command("show")
@utils.throttle()
def get_show(lrrbot, conn, event, respond_to):
	"""
	Command: !show

	Post the current show.
	"""
	if lrrbot.show_override:
		conn.privmsg(respond_to, "Currently live: %s (overridden)" % show_name(lrrbot.show_override))
	elif lrrbot.show:
		conn.privmsg(respond_to, "Currently live: %s" % show_name(lrrbot.show))
	else:
		conn.privmsg(respond_to, "Current show not set.")

@bot.command("show override (.*?)")
@utils.mod_only
def show_override(lrrbot, conn, event, respond_to, show):
	"""
	Command: !show override ID

	Override the current show.
	--command
	Command: !show override off

	Disable the override.
	"""
	show = show.lower()
	if show == "off":
		lrrbot.show_override = None
	elif show not in storage.data.get("shows", {}):
		shows = sorted(storage.data.get("shows", {}).keys())
		shows = [s for s in shows if s]
		conn.privmsg(respond_to, "Recognised shows: %s" % ", ".join(shows))
		return
	else:
		lrrbot.show_override = show
	return get_show.__wrapped__(lrrbot, conn, event, respond_to)
