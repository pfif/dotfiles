local TERMINAL = "XTerm"
local FIREFOX = "Firefox"

-- Standard awesome library
local awful = require("awful")
require("awful.autofocus") --To show the menus bars
awful.rules = require("awful.rules")

local termtag = awful.tag.add("term")
termtag.screen = 1

-- CREATION OF THE TAGS
local firefoxtag = awful.tag.add("firefox")
firefoxtag.screen= 1

local xservertag = awful.tag.add("xserver")
xservertag.screen = 1

--SWITCHING BETWEEN TAGS
function showtag_if(tag_toshow, tag_totoggle)
	local selected = false
	if tag_toshow == tag_totoggle then 
		selected = true 
	end
	tag_totoggle.selected = selected
end

function showtag(tag)
	showtag_if(tag, termtag)
	showtag_if(tag, firefoxtag)
  	showtag_if(tag, xservertag)
end

-- SOME GLOBAL CONFIGURATON
termtag.selected = true --showtag(termtag) -- Terminal is shown by default
awful.layout.set(awful.layout.suit.tile, termtag) --All windows are tiled
awful.layout.set(awful.layout.suit.tile, firefoxtag) --All windows are tiled
awful.layout.set(awful.layout.suit.tile, xservertag) --All windows are tiled

-- KEYBOARD SHORTCUT
modkey = "Mod4"
globalkeys = awful.util.table.join(
	awful.key({ modkey, "Shift"   }, "q", awesome.quit), -- Close awesome
	awful.key({ modkey }, "a", function() showtag(termtag) end), --Switch to terminal
	awful.key({ modkey }, "z", function() showtag(firefoxtag) end), --Switch to firefox
	awful.key({ modkey }, "e", function() showtag(xservertag) end) --Switch to server application
)  
root.keys(globalkeys)

clientkeys = awful.util.table.join(awful.key({ modkey, "Shift"   }, "c",      function (c) c:kill()                         end)) -- Close a window

-- RULES FOR : Keyboard shortcut and tagging spawning clients
awful.rules.rules = {
	{ rule = {}, properties = { keys = clientkeys, tag = xservertag}},
	{ rule = {class = TERMINAL}, properties = { tag = termtag}},
	{ rule = {class = FIREFOX}, properties = { tag = firefoxtag}},
}

-- SPAWNING THE DEFAULT APPLICATIONS
awful.util.spawn("firefox")
awful.util.spawn("xterm +vb -fa monaco  -fs 14 -bg black -fg lightblue -e screen")
