start_text = ("Hello, @{username}, I will help you with your medications.\n"
              "You can control me by sending these commands:\n\n"
              "/newmedication - create a new medication\n"
              "/mymedication - get a list of your medications and edit them\n"
              "/cancel - cancel the operation\n\n"
              "/help - a list of available commands")

cancel_text = ("The command has been cancelled. "
               "Anything else I can do for you?\n\n"
               "Send /help for a list of commands.")
cancel_empty_text = "No active command to cancel. I wasn't doing anything anyway. Zzzzz..."

newmedication_choose_name_text = ("Alright, a new medication. "
                                  "How are we going to call it? "
                                  "Please choose a name for your medication.")
newmedication_choose_time_text = ("Good. Now let's choose time for reminder.It must be in `HH:MM` format. "
                                  "Like this, for example: `09:00` or `13:30`")
newmedication_wrong_time_text = "Sorry, time must be in `HH:MM` format, e.g., `09:00` or `13:30`."

newmedication_finish = ("That's it. You've added `{name}` medication. "
                        "Each day at `{time}` you will receive a notification.")

mymedication_text = "Choose a medication from the list below:"
mymedication_empty_text = ("You currently have no medications. "
                           "Use /newmedication command to create a first medication.")

medication_info_text = ("Here it is: `{name}` (`{time}`).\n"
                        "What do you want to do with the medication?")

medication_delete_confirm_text = "You are about to delete your bot `{name}` (`{time}`). Is that correct?"
medication_delete_finish_text = "You have deleted `{name}` (`{time}`)."
