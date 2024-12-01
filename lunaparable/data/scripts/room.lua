function Init()
    ac = {}
    play_music("home", ac)
    return ac
end
function BooksClicked()
    ac = {}
    add_dialouge("Luna", "These are my pog books.", ac)
    return ac
end
function PlushieClicked()
    ac = {}
    add_dialouge("Luna", "DIS PLUSHIE IS EPIC", ac)
    return ac
end
function DoorClicked()
    ac = {}
    add_dialouge("Luna", "Lemme go through this door!", ac)
    italic(ac)
    add_dialouge("Luna", "The door squeaks open.", ac)
    italic(ac)
    add_goto("hallway", ac)
    return ac
end