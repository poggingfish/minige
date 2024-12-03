function TVClicked()
    ac = {}
    add_dialouge("Character", "This is not my tv.", ac)
    return ac
end
function PlantClicked()
    ac = {}
    add_dialouge("Character", "A ugly plant.", ac)
    return ac
end
function BooksClicked()
    ac = {}
    add_dialouge("Character", "Books on how not to read.", ac)
    add_dialouge("Character", "I understand them.", ac)
    return ac
end
function ShelfClicked()
    ac = {}
    add_dialouge("Character", "Not just a shelf.", ac)
    return ac
end
function DoorClicked()
    ac = {}
    italic(ac)
    add_dialouge("Character", "I open the door", ac)
    italic(ac)
    add_goto("room", ac)
    add_dialouge("Character", "Its the same room but inverted.", ac)
    return ac
end