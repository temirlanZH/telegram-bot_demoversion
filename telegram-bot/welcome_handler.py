
# Standard Modules
from datetime import datetime as dt

from telebot.types import Message

      
def prep_cmd_msg(message: Message) -> str:
        msg_text = " {0.first_name} ".format(message.from_user)

        with open("static/bot.txt", "r") as welcome_text:
            lines = welcome_text.readlines()


            start = f"[{message.text[1:]}]\n"
            stop = f"[{message.text}]\n"

            start_index = lines.index(start)
            stop_index = lines.index(stop)

            for index in range(start_index, stop_index):
                if start in lines[index]:
                    continue
                elif stop in lines[index]:
                    break
                if "Good" in lines[index]:
                    time_index = _check_time()
                    greatings = [greating for greating in lines[index].split("!")]
                    lines[index] = greatings[time_index] + "!/n"
                msg_text += lines[index]

        return msg_text



def  _check_time() -> int:

    curr_time = dt.now()
    curr_hour = curr_time.hour

    if 4 <= curr_hour < 12:
         return 0
    elif 12 <= curr_hour < 18:
        return 1
    elif 18 <= curr_hour < 22:
         return 2
    elif 22 <= curr_hour < 0 or 0 <= curr_hour < 4: 
        return 3