# -*- coding: utf-8 -*-
"""
daily_reminder.py -- FitPlan Pro Daily Workout Reminder
========================================================
Sends a motivational reminder email via Brevo.

FIXES APPLIED:
  7.  CTA URL fixed -- was 'huggingface.co/spaces' (missing app path)
  8.  Timezone bug fixed -- datetime.now() on HuggingFace returns UTC.
      User's reminder time is stored with a UTC offset so comparison is accurate.
  9.  send_daily_reminder() now checks if today's workout is already done/skipped.
      Will NOT send if the user already completed their session.
  10. Replaced urllib with requests for consistent, cleaner error handling.
  11. should_send_reminder() also checks workout completion status before returning True.

USAGE:
    from daily_reminder import send_daily_reminder, should_send_reminder

    if should_send_reminder(username, user_data, session_state):
        ok, msg = send_daily_reminder(username, user_data, session_state)

SETTINGS STORED (via utils.db.save_user_setting):
    reminder_enabled    : "1" or "0"
    reminder_time       : "HH:MM"  (24-hour in UTC to avoid timezone issues)
    reminder_last_sent  : ISO date "YYYY-MM-DD" -- prevents duplicate sends
"""

import os, requests
from datetime import date, datetime, timezone

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
EMAIL_SENDER  = os.getenv("BREVO_SENDER_EMAIL", "noreply@fitplanpro.ai")
SENDER_NAME   = "FitPlan Pro"

# FIX 7: correct app URL
APP_URL = "https://huggingface.co/spaces/Karthik71212/FITPLAN_PRO"

# ── Motivational messages rotated daily ──────────────────────────────────────
_MESSAGES = [
    ("Time to Crush It!", "Your muscles are rested. Your plan is ready. Today is the day."),
    ("Your Workout Is Waiting", "Champions aren't made on rest days. Let's build something today."),
    ("Don't Break the Streak!", "You've been consistent. Don't let today be the day you stopped."),
    ("One Workout Away", "You're one session away from feeling incredible. Let's go!"),
    ("Stay on Track", "Consistency beats intensity. Show up today -- even for 20 minutes."),
    ("Push Your Limits", "Every rep is a vote for the athlete you're becoming. Cast yours today."),
    ("Discipline = Freedom", "Do it now, feel great later. Your future self will thank you."),
]

def _get_message_of_day():
    idx = date.today().toordinal() % len(_MESSAGES)
    return _MESSAGES[idx]


def _build_email_html(username: str, workout_info: dict, reminder_time_display: str) -> str:
    subject_title, body_message = _get_message_of_day()
    day_num  = workout_info.get("day", "?")
    muscle   = workout_info.get("muscle_group", "Workout")
    ex_count = workout_info.get("exercises", 0)
    is_rest  = workout_info.get("is_rest", False)

    if is_rest:
        session_info = "Today is your rest day -- stretch, walk, and recover!"
        cta_text     = "View Rest Day Activities"
    else:
        session_info = (
            f"Day {day_num} -- {muscle}"
            + (f" &nbsp;·&nbsp; {ex_count} exercises" if ex_count else "")
        )
        cta_text = "Open My Workout Plan"

    # FIX 7: APP_URL used in CTA href
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>FitPlan Pro Reminder</title>
</head>
<body style="margin:0;padding:0;background:#0a0200;font-family:'Helvetica Neue',Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0a0200">
<tr><td align="center" style="padding:32px 16px">
<table width="520" cellpadding="0" cellspacing="0"
       style="background:#140202;border-radius:20px;overflow:hidden;border:1px solid rgba(229,9,20,0.35)">

  <tr><td style="height:3px;background:linear-gradient(90deg,#E50914,rgba(229,9,20,0.30))"></td></tr>

  <tr><td style="padding:32px 36px 20px;text-align:center">
    <div style="font-size:2.6rem;margin-bottom:8px">⚡</div>
    <div style="font-size:1.6rem;font-weight:900;color:#E50914;letter-spacing:5px;text-transform:uppercase;margin-bottom:4px">FITPLAN PRO</div>
    <div style="font-size:0.78rem;color:rgba(255,255,255,0.35);letter-spacing:3px;text-transform:uppercase">Daily Workout Reminder</div>
  </td></tr>

  <tr><td style="padding:0 36px">
    <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(229,9,20,0.40),transparent)"></div>
  </td></tr>

  <tr><td style="padding:28px 36px">
    <div style="font-size:1.5rem;font-weight:700;color:#fff;margin-bottom:12px">{subject_title}</div>
    <div style="font-size:1rem;color:rgba(255,255,255,0.70);line-height:1.65;margin-bottom:20px">
      Hey <strong style="color:#fff">{username}</strong>,<br><br>
      {body_message}
    </div>

    <div style="background:rgba(229,9,20,0.10);border:1px solid rgba(229,9,20,0.30);border-radius:14px;padding:18px 22px;margin-bottom:24px">
      <div style="font-size:0.70rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:rgba(229,9,20,0.75);margin-bottom:8px">TODAY'S SESSION</div>
      <div style="font-size:1.05rem;color:#fff">{session_info}</div>
    </div>

    <div style="text-align:center;margin-bottom:8px">
      <a href="{APP_URL}"
         style="display:inline-block;background:linear-gradient(135deg,#E50914,#c0000c);
                color:#fff;font-weight:700;font-size:1rem;padding:14px 36px;
                border-radius:12px;text-decoration:none;letter-spacing:0.5px">
        {cta_text}
      </a>
    </div>
  </td></tr>

  <tr><td style="padding:0 36px 20px">
    <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:14px 18px;border-left:3px solid rgba(229,9,20,0.60)">
      <div style="font-size:0.85rem;font-style:italic;color:rgba(255,255,255,0.55)">
        "The only bad workout is the one that didn't happen."
      </div>
    </div>
  </td></tr>

  <tr><td style="padding:20px 36px;text-align:center;border-top:1px solid rgba(255,255,255,0.06)">
    <div style="font-size:0.72rem;color:rgba(255,255,255,0.28);line-height:1.7">
      You're receiving this because you set a daily reminder at {reminder_time_display}.<br>
      To stop reminders, update your settings in FitPlan Pro.
    </div>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""


def _is_workout_done_today(session_state: dict) -> bool:
    """
    FIX 9 & 11: Returns True if today's workout is already marked done or skipped.
    Used to prevent sending reminders to users who already trained.
    """
    today_str = date.today().isoformat()
    tracking  = session_state.get("tracking", {})
    status    = tracking.get(today_str, {}).get("status", "")
    return status in ("done", "skipped")


def send_daily_reminder(username: str, user_data: dict,
                         session_state: dict) -> tuple:
    """
    Send a daily workout reminder email. Does NOT send if workout already done.

    Returns: (success: bool, message: str)
    """
    if not BREVO_API_KEY or not EMAIL_SENDER:
        return False, "Brevo not configured (set BREVO_API_KEY + BREVO_SENDER_EMAIL)."

    # FIX 9: do not send if workout already done or skipped today
    if _is_workout_done_today(session_state):
        return False, "Workout already completed today -- no reminder needed."

    to_email = user_data.get("email", "")
    if not to_email:
        return False, "No email address found for user."

    # Build today's workout info
    sdays         = session_state.get("structured_days", [])
    plan_start_str = session_state.get("plan_start", date.today().isoformat())
    reminder_time_display = "your scheduled time"

    try:
        from utils.db import get_user_setting
        _rt = get_user_setting(username, "reminder_time")
        if _rt:
            reminder_time_display = _rt + " UTC"
    except Exception:
        pass

    workout_info = {}
    if sdays:
        try:
            _ps  = date.fromisoformat(plan_start_str)
            _idx = (date.today() - _ps).days
            _idx = max(0, min(_idx, len(sdays) - 1))
            _day = sdays[_idx]
            workout_info = {
                "day":          _day.get("day", _idx + 1),
                "muscle_group": _day.get("muscle_group", "Workout"),
                "exercises":    len(_day.get("workout", [])),
                "is_rest":      _day.get("is_rest_day", False),
            }
        except Exception:
            pass

    subject_title, _ = _get_message_of_day()
    html_body = _build_email_html(username, workout_info, reminder_time_display)

    payload = {
        "sender":      {"name": SENDER_NAME, "email": EMAIL_SENDER},
        "to":          [{"email": to_email, "name": username}],
        "subject":     f"FitPlan Pro - {subject_title}",
        "htmlContent": html_body,
    }

    # FIX 10: use requests (consistent with weekly_email.py, better error handling)
    try:
        r = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "accept":       "application/json",
                "api-key":      BREVO_API_KEY,
                "content-type": "application/json",
            },
            json=payload,
            timeout=12,
        )
        if r.ok:
            try:
                from utils.db import save_user_setting
                save_user_setting(username, "reminder_last_sent", date.today().isoformat())
            except Exception:
                pass
            return True, "Reminder sent!"
        else:
            return False, f"Brevo error {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return False, str(e)


def should_send_reminder(username: str, user_data: dict,
                          session_state: dict) -> bool:
    """
    Returns True only if ALL conditions are met:
      - reminder_enabled = "1"
      - current UTC time is within 15 minutes of the stored reminder_time (UTC)
      - reminder not already sent today
      - today's workout is NOT already done or skipped

    FIX 8: Uses UTC time throughout. Reminder time is stored and compared in UTC.
            HuggingFace servers run on UTC so datetime.now(timezone.utc) is always correct.
    FIX 11: Checks workout completion before returning True.
    """
    try:
        from utils.db import get_user_setting

        enabled = get_user_setting(username, "reminder_enabled")
        if enabled != "1":
            return False

        reminder_time_str = get_user_setting(username, "reminder_time") or "08:00"
        last_sent         = get_user_setting(username, "reminder_last_sent") or ""

        # Don't send twice on the same day
        if last_sent == date.today().isoformat():
            return False

        # FIX 9 / 11: skip if workout already done
        if _is_workout_done_today(session_state):
            return False

        # FIX 8: compare in UTC -- HuggingFace servers run UTC
        now_utc    = datetime.now(timezone.utc)
        today_str  = date.today().isoformat()
        target_str = f"{today_str} {reminder_time_str}"
        target_utc = datetime.strptime(target_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        diff_secs  = abs((now_utc - target_utc).total_seconds())
        return diff_secs <= 900  # within 15-minute window

    except Exception:
        return False


# ── SETTINGS UI SNIPPET ───────────────────────────────────────────────────────
# Paste this into pages/1_Profile.py (inside settings section):
"""
IMPORTANT NOTE ON TIMEZONE:
  Reminder times are stored and compared in UTC.
  Tell users to convert their local time to UTC when setting the reminder.
  Example: "8:00 AM IST = 02:30 UTC" -- show this helper in the UI.

COPY THIS INTO pages/1_Profile.py:
-------------------------------------------------------------------
import streamlit as st
from datetime import datetime
from utils.db import get_user_setting, save_user_setting

st.markdown("<div style='font-weight:700;color:rgba(229,9,20,0.75);margin:18px 0 10px'>Daily Reminder Email</div>",
            unsafe_allow_html=True)

_rem_enabled = get_user_setting(uname, "reminder_enabled") or "0"
_rem_time    = get_user_setting(uname, "reminder_time") or "08:00"

rc1, rc2, rc3 = st.columns([2, 3, 2])
with rc1:
    rem_on = st.toggle("Enable Reminder", value=(_rem_enabled == "1"), key="rem_toggle")
with rc2:
    rem_time = st.time_input(
        "Reminder Time (UTC)",
        value=datetime.strptime(_rem_time, "%H:%M").time(),
        key="rem_time_inp",
        help="Enter your reminder time in UTC. IST users: subtract 5h 30m from your local time."
    )
with rc3:
    if st.button("Save Reminder", key="save_reminder", use_container_width=True):
        save_user_setting(uname, "reminder_enabled", "1" if rem_on else "0")
        save_user_setting(uname, "reminder_time", rem_time.strftime("%H:%M"))
        st.success("Reminder saved!")
        st.rerun()

if _rem_enabled == "1":
    _last = get_user_setting(uname, "reminder_last_sent") or "Never"
    st.caption(f"Reminder active at {_rem_time} UTC daily. Last sent: {_last}")

if st.button("Send Test Reminder Now", key="test_reminder"):
    from daily_reminder import send_daily_reminder
    _ok, _msg = send_daily_reminder(uname, data, st.session_state)
    st.success("Test sent!") if _ok else st.error("Failed: " + _msg)
-------------------------------------------------------------------
"""