function Action (type, value, value2, value3)
    return {
        type = type, -- Type can be one of these:
                       -- TextBox, Creates a textbox on screen
                       -- Goto, Goes to a new location
                       -- None, Does nothing
                       -- Italic, changes the text to ITALICS.
        value = value, -- For Goto it will go to the location in the value
                   -- For TextBox it will create a textbox with the text in the value
                   -- For None it will do nothing with the value
        
        value2 = value2, -- For TextBox it is the person speaking.
        value3 = value3
    }
end

function add_dialouge(person, text, actions)
    table.insert(actions, Action("TextBox", text, person))
end
function add_goto(room, actions)
    table.insert(actions, Action("Goto", room))
end
function italic(actions)
    table.insert(actions, Action("Italic"))
end
function play_music(name, actions)
    table.insert(actions, Action("Music", name))
end
function play_animation(name, times, speed, actions)
    table.insert(actions, Action("Animation", name, times, speed))
end
function set_variable(name, v)
    _G.globals[name] = v
end
function get_variable(name)
    if pcall( function( attr, key ) return attr[key] end, _G.globals, name) then
        return globals[name]
     else
        return nil
     end
end
