# Editors

## `nano`

- ++ctrl+o++: Save file
- ++ctrl+x++: Exit editor
- ++ctrl+w++: Search for text
- ++ctrl+u++: Undo last action
- ++ctrl+k++: Cut current line
- ++ctrl+u++: Paste cut line above the current line

## `micro`

- ++ctrl+s++: Save file
- ++ctrl+q++: Quit editor
- ++ctrl+f++: Find text
- ++ctrl+z++: Undo last action
- ++ctrl+e++: Open command prompt
    - `save`: Save file
    - `quit`: Quit editor
    - `find`: Find text
    - `set filetype <filetype>`: Set syntax highlighting based on file type
    - `set tabsize <number>`: Set the number of spaces for a tab


## `vim`

- ++d++ ++d++: Delete current line
- ++p++: Paste the deleted line above the current line
- ++i++: Enter insert mode to edit text
- ++colon++ ++w++: Save file
- ++colon++ ++q++: Quit editor

## `helix`

[Keymap](https://docs.helix-editor.com/keymap.html)

<iframe width="560" height="315" src="https://www.youtube.com/embed/HcuDmSb-JBU?si=AAfRl1fhq7Cb8DgW" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
/// caption
The Most Underrated IDE
///

### Normal mode

- Undo: `u
- Redo: `U
- Move cursor forward: `w`
- Move cursor backward: `b`
- Delete highlighted text: `d`
- Find next char: `f`
- Find previous char: ``F``
- Go to end of line: `g` `l`
- Go to beginning of line: `g` `h`
- Show all keybindings: ++space++ ++?++
    - Search for a specific keybinding: type `%bindings <binding>`
- File picker: ++space++ `f`
    - Open file in vertical split: ++ctrl+v++
    - Open file in horizontal split: ++ctrl+h++
    - Move to left split: ++ctrl+w++ ++left++
    - Close current split: ++ctrl+w++ ++q++
- Symbol picker: ++space++ `s`
- Project-wide symbol picker: ++space++ `S`
- Diagnostic picker: ++space++ `d`
- Comment line: ++ctrl+c++
- Highlight current line and move to next line: `x`
- Replace highlighted text (LSP rename): ++space++ `r`
- Go to definition: `g` d`
    - Go out of definition: ++ctrl+o++
    - Go into definition: ++ctrl+i++
- Go to references: `g` `r`
- Jump to a two-character label: `g` `w`
- Expand selection to the next node in the syntax tree: ++option+up++
- Shrink selection to the previous node in the syntax tree: ++option+down++

### Select mode

- Enter select mode: `v`
- Move cursor forward with appended selection: `w`
- Move cursor backward with appended selection: `b`
