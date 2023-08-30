start_text = ("Hello, @{username}, I will help you with your medications.\n"
              "You can control me by sending these commands:\n\n"
              "/newmedication - create a new medication\n"
              "/mymedication - get a list of your medications and edit them\n"
              "/history - get info on whether you took your medications for the last {days_amount} days\n"
              "/cancel - cancel the operation\n\n"
              "/help - a list of available commands")
start_empty_username_text = "You do not have username 🙈"

cancel_text = ("The command has been cancelled. "
               "Anything else I can do for you?\n\n"
               "Send /help for a list of commands.")
cancel_empty_text = "No active command to cancel. I wasn't doing anything anyway. Zzzzz..."

history_header_text = ("Here is your history for the last {days_amount} days "
                       "between <code>{start_date}</code> and <code>{end_date}</code> dates:\n--------------------\n\n")
history_empty_text = ("No medications were taken during last {days_amount} days "
                      "between <code>{start_date}</code> and <code>{end_date}</code> dates.")
history_whole_day_text = "<code>{date}</code>:\n{content}\n"
history_whole_day_empty_text = "No medications were taken on this date :(\n"
history_one_notification_text = "- {name}\n"

newmedication_choose_name_text = ("Alright, a new medication. "
                                  "How are we going to call it? "
                                  "Please choose a name for your medication.")
newmedication_choose_time_text = ("Good. Now let's choose time for reminder.It must be in <code>HH:MM</code> format. "
                                  "Like this, for example: <code>09:00</code> or <code>13:30</code>. "
                                  "Time has to be between <code>05:00</code> and <code>19:55</code>. "
                                  "Also minutes must be divisible by 5, e.g., "
                                  "<code>16:25</code> and not <code>16:24</code>.")
newmedication_wrong_time_text = ("Sorry, time must be in <code>HH:MM</code> format, e.g., "
                                 "<code>09:00</code> or <code>13:30</code>. "
                                 "Time has to be between <code>05:00</code> and <code>19:55</code>. "
                                 "Also minutes must be divisible by 5, e.g., "
                                 "<code>16:25</code> and not <code>16:24</code>.")

newmedication_finish = ("That's it. You've added <code>{name}</code> medication. "
                        "Each day at <code>{time}</code> you will receive a notification.")

mymedication_text = "Choose a medication from the list below:"
mymedication_empty_text = ("You currently have no medications. "
                           "Use /newmedication command to create a first medication.")

medication_info_text = ("Here it is: <code>{name}</code> (<code>{time}</code>).\n"
                        "What do you want to do with the medication?")

medication_delete_confirm_text = ("You are about to delete your bot <code>{name}</code> (<code>{time}</code>). "
                                  "Is that correct?")
medication_delete_finish_text = "You have deleted <code>{name}</code> (<code>{time}</code>)."

medication_take_confirm_text = "It's time 💊. Please, take <code>{name}</code> medication on <code>{date}</code>."
medication_take_followup_text = ("Hey, it's me again 💊. Seems like you forgot to take "
                                 "<code>{name}</code> on <code>{date}</code> 🤧. "
                                 "Please, take it and press below button.")
medication_take_finish_text = "Good job. You took <code>{name}</code> medication on <code>{date}</code> 💪"

n_new_user_text = "@{username} just started using bot 🥳"
n_medication_taken_text = "@{username} just took <code>{name}</code> medication on <code>{date}</code> date."
