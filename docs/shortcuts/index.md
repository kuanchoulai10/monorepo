# Shortcuts

Keys and shortcuts for various tools.

For how to edit this document, see [Keys | PyMarkdown Extension](https://facelessuser.github.io/pymdown-extensions/extensions/keys/). 

## Helix

Vim-like modal editor with multiple selection support and built-in language server integration.

### How Helix Works

Helix operates through different **modes** that change how your keyboard input is interpreted:

- **Normal Mode** (default): Your keyboard becomes a command interface. Letters like `w`, `b`, `d` are commands for navigation and text manipulation, not typing
- **Insert Mode**: Standard typing mode where letters appear as text on screen
- **Select Mode**: Extends text selections as you move the cursor, similar to holding Shift in other editors
- **Command Mode**: Execute ex-style commands (like `:quit`, `:save`) by typing them out

The key insight: you spend most time in **Normal Mode** navigating and commanding, briefly entering **Insert Mode** to type, then immediately returning to **Normal Mode**. This feels awkward initially but becomes incredibly efficient.

### Scenario 1: Opening and Exploring a Project *(Normal Mode)*

Imagine you're starting work on a new codebase. Launch Helix and you'll be in **Normal mode** - think of this as your command dashboard. Your first task is finding the main file. Press ++space++, then ++f++ - this opens the file picker. You'll see a fuzzy finder where you can type part of a filename. Use ++j++/++k++ to navigate the list, then ++enter++ to open your selection.

Let's say you're now looking at `main.py` but need to check `config.py` too. Instead of opening another file picker, press ++space++, then ++b++ to see your buffer list - files you already have open. This becomes invaluable when juggling multiple files.

The file is 500 lines long - intimidating! But navigation is easy: ++g++, ++g++ jumps to line 1 instantly. ++shift+g++ takes you to the very end. For quick scrolling, ++ctrl+u++ jumps up half a screen, ++ctrl+d++ jumps down.

**Essential shortcuts:**

- ++space++, ++f++: Open file picker
- ++space++, ++b++: Switch between open buffers  
- ++g++, ++g++: Jump to start of file
- ++shift+g++: Jump to end of file
- ++ctrl+u++ / ++ctrl+d++: Page up/down

### Scenario 2: Making Your First Code Change *(Normal --> Insert --> Normal)*

You found a function that needs a new parameter. Place your cursor at the end of the parameter list using arrow keys or ++h++/++j++/++k++/++l++. Now you need to start typing - but you're in **Normal mode** where letters are commands, not text!

To enter **Insert mode**, press ++a++ (append after cursor). Notice your status bar shows "INSERT" - now you can type like any regular editor. Add `, debug=False` to the parameter list.

When done typing, press ++esc++ to return to **Normal mode**. This two-mode dance becomes second nature: Normal for navigation/commands, Insert for actual typing.

**Essential shortcuts:**

- ++i++: Insert before cursor
- ++a++: Insert after cursor
- ++o++: New line below and insert
- ++shift+o++: New line above and insert
- ++esc++: Return to Normal mode

### Scenario 3: Refactoring Code *(Normal Mode)*

You spot a poorly named variable `x` that should be `user_count`. Place your cursor on any instance of `x`. In **Normal mode**, press ++space++, then ++r++. Helix analyzes your code and highlights ALL occurrences of this variable across your entire project! Type the new name `user_count` and hit ++enter++ - every instance updates automatically. This is language-server powered renaming.

But what if you want to see what this variable does? Place your cursor on `user_count` and press ++g++, then ++r++. A picker shows every place this variable is referenced. Select one with ++j++/++k++ and ++enter++ to jump there.

**Essential shortcuts:**

- ++space++, ++r++: Rename symbol everywhere
- ++g++, ++d++: Go to definition
- ++g++, ++r++: Go to references
- ++space++, ++a++: Apply code action

### Scenario 4: Debugging with Diagnostics *(Normal Mode)*

Your code has syntax errors - the status bar shows "2 errors, 1 warning". Press ++bracket-right++, then ++d++ to jump to the first diagnostic. Helix positions your cursor exactly on the problematic code and shows the error message.

Want to auto-fix it? Press ++space++, then ++a++ for code actions. Helix might offer "Add missing import" or "Fix syntax error". Select the fix with ++j++/++k++ and ++enter++.

**Essential shortcuts:**

- ++bracket-right++, ++d++: Next diagnostic
- ++bracket-left++, ++d++: Previous diagnostic
- ++space++, ++a++: Show code actions

### Scenario 5: Finding Code Across the Project *(Normal Mode)*

You remember seeing a function called `calculate_tax` somewhere but can't find it. Press ++space++, then ++s++ - this opens the symbol picker showing all functions/classes in the current file. Not there? Try ++space++, then ++slash++ for global search across your entire project. Type "calculate_tax" and Helix searches every file, showing matches with context.

If your cursor is already on a word you want to search for, ++space++, then ++question++ searches for that word everywhere instantly.

**Essential shortcuts:**

- ++space++, ++s++: Symbol picker (current file)
- ++space++, ++slash++: Global search in project
- ++space++, ++question++: Search word under cursor
- ++slash++: Search in current file
- ++n++ / ++shift+n++: Next/previous match

### Scenario 6: Working with Multiple Selections *(Normal/Select Mode)*

You have a list of email addresses that all need ".com" appended. Select one email by pressing ++w++ to select the word. Now press ++v++ to enter **Select mode** - this extends your selection as you move with ++j++/++k++/++l++.

Here's the magic: with text selected, press ++alt+c++. Helix finds ALL identical selections in your file and gives you multiple cursors! Now type ".com" and it appears after every email simultaneously. Press ++semicolon++ to collapse back to one cursor.

**Essential shortcuts:**

- ++x++: Select current line
- ++w++: Select word forward
- ++v++: Enter Select mode (extend selection)
- ++alt+c++: Select all matching text
- ++semicolon++: Collapse to single cursor

### Scenario 7: Side-by-Side Editing *(Normal --> Window Mode)*

You're comparing two config files. Press ++ctrl+w++ - you're now in **Window mode** (notice the status change). Press ++v++ for vertical split. Now you have two panes! Press ++ctrl+w++, then ++h++/++l++ to move between them.

Open different files in each pane using ++space++, ++f++ as usual. When done with splits, press ++ctrl+w++, then ++q++ to close the current pane.

**Essential shortcuts:**

- ++ctrl+w++: Enter Window mode
- ++v++: Vertical split (in Window mode)
- ++s++: Horizontal split (in Window mode)
- ++h++/++j++/++k++/++l++: Navigate between panes (in Window mode)
- ++q++: Close current pane (in Window mode)

## Micro

A terminal-based text editor that aims to be easy to use and intuitive.

- ++ctrl+++