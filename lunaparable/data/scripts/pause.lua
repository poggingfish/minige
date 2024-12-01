function SaveClicked()
    ac = {}
    table.insert(ac, Action("Save"))
    add_dialouge("System", "Saved!", ac)
    return ac
end
function ReturnClicked()
    ac = {}
    table.insert(ac, Action("Back"))
    return ac
end
function QuitClicked()
    ac = {}
    table.insert(ac, Action("Quit"))
    return ac
end