function Init()
    ac = {}
    add_dialouge("Luna", "I cant find my keys..", ac)
    return ac
end

function SpeedometerClicked()
    ac = {}
    add_dialouge("Car", "The car is not moving :(", ac)
    add_dialouge("Car", "Find your keys somewhere.", ac)
    return ac
end

function EpikumeterClicked()
    ac = {}
    add_dialouge("Car", "DIS IS DA MOST EPIKU MOMENT", ac)
    italic(ac)
    add_dialouge("Car", "OF ALL TIME...", ac)
    italic(ac)
    return ac
end

function Stigl_HatClicked()
    ac = {}
    add_dialouge("Luna", "Its so shinyyy!", ac)
    add_dialouge("Luna", "Da keys arent under it though..", ac)
    return ac
end

function StiglClicked()
    ac = {}
    if get_variable("has_keys") == true then
        add_dialouge("Stigl", "Pog u found da keys!", ac)
        return ac
    end
    add_dialouge("Luna", "Stigl?", ac)
    add_dialouge("Stigl", "Ye gwil?", ac)
    add_dialouge("Luna", "Have u seen da keys?", ac)
    add_dialouge("Stigl", "Soowy idk...", ac)
    add_dialouge("Luna", "Its quite ok!", ac)
    return ac
end

function LunaClicked()
    ac = {}
    luna_clicked = get_variable("lunaclicked")
    if luna_clicked == nil then
        add_dialouge("Luna", "ah pls dont click me", ac)
        set_variable("lunaclicked", 1)
    else
        if luna_clicked == 1 then
            add_dialouge("Luna", "pwease stop", ac)
        elseif luna_clicked == 2 then
            add_dialouge("Luna", "PWEEEASE", ac)
        elseif
            luna_clicked == 3 then
            italic(ac)
            add_dialouge("Luna", "cwys", ac)
            italic(ac)
        else
            italic(ac)
            add_dialouge("Luna", "Luna refuses to react.", ac)
            italic(ac)
        end
        set_variable("lunaclicked", luna_clicked + 1)
    end
    return ac
end

function Luna_HairClicked()
    ac = {}
    add_dialouge("Luna", "Pog hair!", ac)
    return ac
end

function Drivers_SeatClicked()
    ac = {}
    if get_variable("has_keys") == true then
        add_dialouge("Luna", "I already have the keys.", ac)
        return ac
    end
    add_dialouge("Luna", "AH i was sitting on them!", ac)
    italic(ac)
    add_dialouge("Luna", "You got keys!", ac)
    italic(ac)
    set_variable("has_keys", true)
    return ac
end

function Passenger_SeatClicked()
    ac = {}
    add_dialouge("Luna", "Thats where stigl is sitting.", ac)
    return ac
end

function KeyholeClicked()
    ac = {}
    if get_variable("has_keys") == true then
        italic(ac)
        add_dialouge("Luna", "I slowly insert the key.", ac)
        add_dialouge("Luna", "I turn it and the engine\nroars to life.", ac)
        play_music("epiku", ac)
        play_animation("car_drive", 4, 3, ac)
        play_animation("spacecar", 4, 3, ac)
        play_animation("reentry", 1, 4, ac)
        italic(ac)
        return ac
    else
        add_dialouge("Luna", "I need to find my keys before\ni use this.", ac)  
    end
    return ac
end