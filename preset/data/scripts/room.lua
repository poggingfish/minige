function Init()
    ac = {}
    play_music("song", ac)
    return ac
end
function TVClicked()
    ac = {}
    add_dialouge("Character", "This is my tv.", ac)
    return ac
end
function PlantClicked()
    ac = {}
    add_dialouge("Character", "A beautiful plant.", ac)
    return ac
end
function BooksClicked()
    ac = {}
    add_dialouge("Character", "Books on how to read.", ac)
    add_dialouge("Character", "I still dont understand them.", ac)
    return ac
end
function ShelfClicked()
    ac = {}
    add_dialouge("Character", "Just a shelf.", ac)
    return ac
end
function DoorClicked()
    ac = {}
    italic(ac)
    add_dialouge("Character", "I open the door", ac)
    italic(ac)
    add_goto("room2", ac)
    add_dialouge("Character", "Its the same room but inverted.", ac)
    return ac
end