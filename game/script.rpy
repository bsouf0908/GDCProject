##############################################################################
init:
    $ renpy.music.register_channel("blips", mixer=None, loop=True, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)

init python:
    def female(event, **kwargs):
        if event == "show":
            renpy.music.play("audio/female_bleep.ogg", channel="blips")
        elif event == "slow_done" or event == "end":
            renpy.music.stop(channel="blips")

init python:
    def male(event, **kwargs):
        if event == "show":
            renpy.music.play("audio/male_bleep.ogg", channel="blips")
        elif event == "slow_done" or event == "end":
            renpy.music.stop(channel="blips")

init python:
    def narrator(event, **kwargs):
        if event == "show":
            renpy.music.play("audio/narrator_bleep.ogg", channel="blips")
        elif event == "slow_done" or event == "end":
            renpy.music.stop(channel="blips")

define cg = Character('Catgirl', callback=female, ctc="ctc_blink", ctc_position="nestled")
define Protagonist = Character('[povname]', callback=male, ctc="ctc_blink", ctc_position="nestled")
define Narrator = Character('', color="#6699cc", callback=narrator, ctc="ctc_blink", ctc_position="nestled")
define Narrator_NVL = Character('',
    kind = nvl,
    color="#6699cc",
    ctc="ctc_blinkNVL",
    ctc_position="fixed", )
##############################################################################
#Function for when day ends.
define bg_change_days = MultipleTransition([
    False, Fade(1, 0, 1),
    "images/gui/new_day.PNG", Pause(1.0),
    "images/gui/new_day.PNG", Fade(1, 0, 1),
    True])

image word_effect:
    Text("[day]")
    alpha 1.0
    pause .4
    alpha 0.0
    pause .1
    repeat

screen overlay:
    frame:
        yalign 0.0 xalign 0.0
        hbox:
            textbutton " Backpack " action Function(renpy.call, label="inventory")
            textbutton " Buy " action Function(renpy.call, label="market_buy")
            textbutton " Sell " action Function(renpy.call, label="market_sell")
            textbutton " Craft " action Function(renpy.call, label="start_crafting")
            textbutton " Quests " action Function(renpy.call, label="view_quests")
##############################################################################
#Blinking Arrow
image ctc_blink:
       zoom 0.5
       "gui/blinker.png"
       linear 0.75 alpha 1.0
       linear 0.75 alpha 0.0
       repeat

image ctc_anchored:
    xpos 0.93 # Across from right
    ypos 0.87 # Up from bottom
    xanchor 1.0  # On Right
    yanchor 1.0   # On Bottom
    zoom 0.5
    alpha 1.0 # visible
    "images/Arrow.png"
    linear 0.75 alpha 1.0
    linear 0.75 alpha 0.0
    repeat
##############################################################################
image bg shop = Solid("#ffbedb")
image bg lab = Solid("#c3beff")
image splash = "images/menu_and_splash/main_menu.PNG"
image warning = "images/menu_and_splash/splash_1.png"
image title = "images/gui/new_day.png"
image catgirl = im.FactorScale("images/sprites/catgirl_example.png", 0.65, 0.65)

label splashscreen:
    scene black
    $ renpy.pause(1)
    show warning at truecenter with dissolve:
        zoom 0.7
    $ renpy.pause(1)
    hide warning with dissolve
    #$renpy.pause(1)
    show splash at truecenter with dissolve:
        zoom 0.2
    $ renpy.pause(1)
    hide splash with dissolve
    $ renpy.pause(1)
    show title at truecenter:
        zoom 0.5
    $ renpy.pause(2)
    hide text with dissolve
    $ renpy.pause(1)
    return

label start:

    python:
        gold = 20 #starting amount
        inv = []
        seen_items = []

        # crafting
        known_recipes = []
        seen_recipes = []
        made_recipes = []
        newitem = ""

        # shop inventory
        market = []

        # quests
        new_quests = []
        active_quests = []
        completed_quests = []

    ## CRAFT/SHOP SETUP
    $ known_recipes = ["item_sugar", "item_sucker"]
    $ market = [ "item_water", "item_paper", "item_beet" ]

    ## INVENTORY SETUP
    $ InvItem(*item_sugar).pickup(3)
    $ InvItem(*item_water).pickup(2)
    # $ InvItem(*item_sucker).pickup(1)
    # $ InvItem(*item_beet).pickup(200)

label process_quests:
    # add a quest with no unlock conditions
    $ add_new_quest("sucker3")

    # add a quest that only activates if you have money
    if new_quest("sugar1") and gold>0:
        $ new_quests.append("sugar1")

    # activate all new quests
    python:
        if len(new_quests) > 0: #if we have new quests
            for i in new_quests:
                active_quests.insert(0, i) #add to top of the quest list
            new_quests = [] #now reset the new quest list, since they all got added

    Narrator "What is your name?"

    python:
        povname = renpy.input("What is your name?", length=16)
        povname = povname.strip()

        if not povname:
             povname = "Benjamin"

    menu:

        Narrator "What is your gender?"

        "I'm a male.":
            $player_pronoun_His = "His"
            $player_pronoun_his = "his"
            $player_pronoun_He = "He"
            $player_pronoun_he = "he"
            $player_pronoun_guy = "guy"
        "I'm a female.":
            $player_pronoun_His = "Her"
            $player_pronoun_his = "her"
            $player_pronoun_He = "She"
            $player_pronoun_he = "she"
            $player_pronoun_guy = "gal"
        "I'm neither.":
            $player_pronoun_His = "These"
            $player_pronoun_He = "They"

    Protagonist "Hello, I am [povname]. I like catgirls."

    cg "I am a catgirl."

    cg "[povname] is nice. [player_pronoun_He] is a good friend of mine."

    Protagonist "AROOOOOOOOOOGAA."

    jump monday

    label monday:
        scene black
        $ renpy.pause(1)
        $day = "{size=+20}{color=#ffffff}AM 6:00 MONDAY{/color}{/size}"
        show text "{color=#ffffff}{image=word_effect}\nTEMP: 78.4F\n12/25\nNO NEW MESSAGES{/color}" with dissolve

        $ renpy.pause(3)

        hide text with dissolve
        jump monday_morning

label monday_morning:

    #scene ikea with fade

    #show screen overlay with dissolve

    scene bg bedroom with vpunch

    Narrator "As [povname] opens their eyes, the first things that they notice are that it's dark, they're cold, and the autumn leaves are falling with the efficacy of the alarm shocking them to consciousness."

    show screen overlay with dissolve

    Narrator "{cps=*0.2}TIP: CLICK {i}BACKPACK{/i} TO INSPECT STORED ITEMS.{/cps}"

    Narrator "{cps=*0.2}TIP: CLICK {i}BUY{/i} TO SHOP FROM THE LOCAL MARKET.{/cps}"

    Narrator "{cps=*0.2}TIP: CLICK {i}SELL{/i} TO CONTRIBUTE TO THE LOCAL MARKET.{/cps}"

    Narrator "{cps=*0.2}TIP: CLICK {i}CRAFT{/i} TO MAKE ITEMS.{/cps}"

    Narrator "{cps=*0.2}TIP: CLICK {i}QUESTS{/i} FOR AVAILABLE QUESTS.{/cps}"

    Protagonist "Oh, hello! I didn't see you there."

    show catgirl at right with easeinright

    cg "Now that you understand the basics of the game, let me you the battling mechanic."

    cg "You could pull the player into a fight voluntarily (through a menu) or against their will."

    cg "So... do you want to battle?"

    define squares = squares

    label fight:
        menu:
            "Fight":
                call pre_battle
                hide screen overlay
            "Disengage":
                Narrator "You decide to disengage."
                #return
                #return()

    cg "Unfortunately you have to reinitialize labels each time you wish to initiate a battle (for exiting back to dialogue)."

    cg "Check battle-script.rpy and read up on the source code, its really not that hard."

    jump ending

##############################################################################
#implement tools (e.g. phone, inventory, buy, sell, quests, crafting, etc.).


##ITEMS
label inventory:
    hide screen overlay
    #scene bg lab
    call screen inventory(collection=inv) with Dissolve(.2)
    #jump test_menu
    Narrator "You put away your backpack."
    return()
##CRAFTING
label start_crafting:
    #scene bg lab
    hide screen overlay
    call screen recipes() with Dissolve(.2)
    return()

label craft_success:
    show screen reward(newitem.image)
    show screen overlay with dissolve
    Narrator "Made {bt=3}{color=#d48}[newitem.name!t]{/color}{/bt}!"
    #Narrator "Made {color=#d48}[newitem.name!t]{/color}!"
    hide screen reward
    jump start_crafting
    return()

##QUESTS
label view_quests:
    #scene bg lab
    hide screen overlay
    call screen quests(page=0) with Dissolve(.2)
    return()

label activequest:
    call screen quests(page=0)
    return()

label completedquest:
    call screen quests(page=1)
    return()

## SHOP
label market_buy:
    #scene bg shop
    hide screen overlay
    call screen shop(market) with Dissolve(.2)
    Narrator "You stop shopping."
    return()
    #jump test_menu

label market_sell:
    #scene bg shop
    hide screen overlay
    call screen inventory(collection=inv, selling=True) with Dissolve(.2)
    Narrator "You stop selling."
    return()
    #jump test_menu

label ending:
    hide screen overlay
    image creditscroll:
        Text([
        "{b}a game by DARKEUM{/b}\n \n \n"
        "\n{b}Designed and Built By:{/b} \nElon Litman \n"
        "\n{b}Story:{/b} \nBenjamin Souferian \nElon Litman\nTaikary Jiang \n"
        "\n{b}Character Art:{/b} \nTrinity Wu\n"
        "\n{b}Background Art:{/b} \nTrinity Wu \nElon Litman\n"
        "\n{b}Music:{/b} \nElon Litman\n"
        "\n{b}Logo & Icon:{/b} \nBenjamin Souferian \nElon Litman \n"
        "\n{b}Special Thanks:{/b} \nColin Cubinski \nSimon Plotkin \nAriel Baron \nThe Ren'Py Community \n[povname] \n"], outlines=[(3.3, "#ffffff", 0, 0)])
        anchor (0.5, 0.0)
        pos (0.5, 1.0)
        linear 15.0 ypos 0.0 yanchor 1.0

    init:
        $ specialtrans = Dissolve(15)

    $ renpy.transition(specialtrans, layer='master')
    $ quick_menu = False
    scene black with fade

    show creditscroll
    $ renpy.pause(15.0, hard=True)
    hide creditscroll
