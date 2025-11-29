from typing import Dict

def looks_like_device(text: str) -> bool:
    t = text.lower()
    keywords = ["android","iphone","ios","ipad","windows","mac","macos",
        "pixel","samsung","oneplus","tablet","phone","pc","laptop"]
    return any(k in t for k in keywords)

def decide_reply(message: str,state: Dict) -> str:
    text = message.lower().strip()
    t = text

    if text in {"quit","exit","bye","ok","thanks","ok thanks"}:
        return ("Thanks for reaching out to Spotify Support. "
            "If you still need help later, just come back and message me again.")

    if state.get("flow") == "app_crash" and state.get("step") == "ask_device":
        if looks_like_device(text):
            state["device_info"] = text
            state["step"] = "done"
            state.pop("flow",None)
            return ("Thanks. First,update Spotify and your operating system to the latest version, "
                "then clear the app cache and restart your device. "
                "If the app still crashes,reinstall Spotify and sign in again.")
        else:
            return ("To help you better,please tell me your device and operating system, "
                "for example: 'Android 14 phone','iPhone iOS 17',or 'Windows 11 laptop'")

    if state.get("flow") == "login_issue" and state.get("step") == "ask_email":
        state["email_hint"] = text
        state["step"] = "done"
        state.pop("flow",None)
        return ("Got it. Make sure you are using the correct email address on the login screen, "
            "then tap Forgot password? and follow the reset link sent to your inbox or spam folder. "
            "If you still cannot log in,contact Spotify Support with that email so they can verify your account.")

    if state.get("flow") == "billing_issue" and state.get("step") == "ask_region":
        state["region"] = text
        state["step"] = "done"
        state.pop("flow",None)
        return ("Thanks. Check your subscription status on the account page and your bank statement. "
            "If you see unexpected charges,contact your bank first,then reach out to Spotify with a screenshot "
            "of the charge so they can review it.")

    if any(w in t for w in ["crash","crashes","crashing","keeps crashing","freezes",
            "not working","won't open","cant open","can't open",
            "stops playing","stops working"]):
        state["flow"] = "app_crash"
        state["step"] = "ask_device"
        state["unclear_count"] = 0
        return ("Sorry the Spotify app is not working properly. "
            "Which device and operating system are you using "
            "(for example,Android 14 phone,iPhone iOS 17,Windows 11 PC)?")

    if any(w in t for w in ["login","log in","sign in","password","cant sign in","cannot sign in"]):
        state["flow"] = "login_issue"
        state["step"] = "ask_email"
        state["unclear_count"] = 0
        return ("Let’s fix your login. Are you trying to sign in with email,phone number,Facebook,Google or Apple?")

    if any(w in t for w in ["payment","billing","charged","charge","receipt"]):
        state["flow"] = "billing_issue"
        state["step"] = "ask_region"
        state["unclear_count"] = 0
        return ("I can help with billing. Which country are you in and what payment method are you using "
            "(card,PayPal,mobile carrier,or something else)?")

    if any(w in t for w in ["download","downloads","offline","can’t save","cant save","downloaded songs","downloaded music"]):
        state["unclear_count"] = 0
        return ("If downloads or offline mode are not working,please check that:"
            "1) You have enough free storage on your device,"
            "2) You are on Wi‑Fi or a stable connection while downloading,"
            "3) Your Premium subscription is active and you are logged into the correct account.")

    if (("background" in t)
        or ("other app" in t)
        or ("another app" in t)
        or ("when i open whatsapp" in t)
        or ("music stops" in t and any(w in t for w in ["when i open","when i use","switch apps","multitask"]))):
        state["unclear_count"] = 0
        return ("It sounds like music stops when you use other apps. Please check that:"
            "1) Battery saver or power optimization is disabled for Spotify,"
            "2) Spotify is allowed to run in the background in your device settings,"
            "3) On Android,disable any 'sleeping apps' or 'background app limits' for Spotify."
            "After changing these settings,restart your device and try again.")

    if any(w in t for w in ["hi","hello","hey","good morning","good evening"]):
        state["unclear_count"] = 0
        return ("Hi,this is Spotify Support. I can help with login issues,subscription & billing, "
            "the app crashing or not playing,downloads & offline mode,background playback, "
            "and basic account questions. Tell me in one sentence what you need help with.")

    if ("cancel" in t and "subscription" in t) or "cancel premium" in t or "cancel my premium" in t or "cancel my subscription" in t or "cancel my premium subscription" in t or "want to cancel premium" in t or "want to cancel subscription" in t:
        state["unclear_count"] = 0
        return ("To cancel Spotify Premium,go to your account page in a browser,open the Plans or Manage plan section, "
            "and choose Cancel Premium. You will keep Premium until the end of the current billing period.")

    if "change plan" in t or "switch plan" in t or "family plan" in t or "change my plan" in t or "switch my plan" in t or ("change" in t and "plan" in t) or ("switch" in t and "plan" in t):
        state["unclear_count"] = 0
        return ("To change your plan,open your account page,go to Plans and pick the plan you want "
            "(Individual,Duo,Family,or Student). The change usually takes effect on your next billing date.")

    if "playlist" in t and any(w in t for w in ["gone","missing","deleted","lost"]):
        state["unclear_count"] = 0
        return ("If a playlist is missing,first check that you are logged into the same Spotify account you used before. "
            "If a playlist was deleted,you can restore it from the Recover playlists section on the account page.")

    if any(w in t for w in ["song not available","track not available","greyed out","grayed out","can't find a song"]):
        state["unclear_count"] = 0
        return ("Greyed‑out songs are usually unavailable due to licensing changes in your region, "
            "or they were removed by the artist or label. In that case,they unfortunately cannot be played.")

    if "change email" in t or "update email" in t or ("change" in t and "email" in t) or ("update" in t and "email" in t):
        state["unclear_count"] = 0
        return ("You can change the email on your Spotify account from your account page under Edit profile. "
            "Update the email,save the changes,and confirm it from the new email inbox.")

    if ("username" in t or " user name" in t) and any(w in t for w in ["change","edit","update"]):
        state["unclear_count"] = 0
        return ("Spotify usernames cannot usually be changed,but you can change your display name in the app "
            "under Settings → View profile → Edit profile. Your display name is what other people see.")

    unclear_count = state.get("unclear_count",0)
    state["unclear_count"] = unclear_count + 1

    if unclear_count == 0:
        return ("I’m not completely sure what you need. Are you having trouble with login,payments, "
            "the app crashing,music stopping in the background,downloads/offline,or something else?")
    elif unclear_count == 1:
        return ("I still can’t match that to a specific help topic. Please write one short sentence like "
            "can't log in, music stops when I open other apps, or problem with Premium payment")
    else:
        return ("This looks like something a human agent should review. Please contact Spotify Support through the "
            "Help section in the app or on the website,and share a brief description and screenshots if possible.")

def bot_reply(user_text:str,session_state:dict)->str:
    return decide_reply(user_text,session_state.setdefault("bot_state",{}))