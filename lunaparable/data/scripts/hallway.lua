function StiglClicked()
    ac = {}
    if get_variable("talked_to_stigl_1") == true then
        add_dialouge("Stigl", "Pog!", ac)
        return ac
    end
    add_dialouge("Luna", "Yo whats up Stigl?", ac)
    add_dialouge("Stigl", "Yooo not much hbu?", ac)
    add_dialouge("Luna", "Ahhh same tbh!", ac)
    set_variable("talked_to_stigl_1", true)
    return ac
end
function PaintingClicked()
    ac = {}
    add_dialouge("Luna", "A beautiful painting.\nI made it myself.", ac)
    return ac
end
function Room_DoorClicked()
    ac = {}
    add_dialouge("Luna", "I was just there.\nMaybe I should go outside.", ac)
    return ac
end
function Outside_DoorClicked()
    ac = {}
    if get_variable("talked_to_stigl_1") ~= true then
        add_dialouge("Luna", "I should talk to Stigl first.", ac)
        return ac
    end
    italic(ac)
    add_dialouge("Luna", "I open the door.", ac)
    add_dialouge("Luna", "It is another beautiful day.", ac)
    italic(ac)
    add_goto("outside", ac)
    return ac
end
function Stigl_HatClicked()
    ac = {}
    add_dialouge("Luna", "such a shiny hat\n:pleading:", ac)
    return ac
end