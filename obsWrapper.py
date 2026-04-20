import obspython as obs
import subprocess
import os
import threading

bot_process = None
current_settings = None

def script_description():
    return "Start Twitch bot when OBS loads"

def log_reader(pipe, name):
    for line in iter(pipe.readline, ''):
        print(f"[{name}] {line}", end='')

def restart_bot(props, prop):
    script_unload()
    script_load(current_settings)
    return True

def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(props, "bot_path", "Bot Path", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "target_channel", "Target Channel Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "client_id", "Client ID", obs.OBS_TEXT_PASSWORD)
    obs.obs_properties_add_text(props, "client_secret", "Client Secret", obs.OBS_TEXT_PASSWORD)
    
    obs.obs_properties_add_button(props, "restart", "Restart Bot", restart_bot)

    return props

def script_load(settings):
    global bot_process, current_settings
    current_settings = settings

    bot_path = obs.obs_data_get_string(settings, "bot_path")
    client_id = obs.obs_data_get_string(settings, "client_id")
    client_secret = obs.obs_data_get_string(settings, "client_secret")
    target_channel = obs.obs_data_get_string(settings, "target_channel")

    env = os.environ.copy()
    env["CLIENT_ID"] = client_id
    env["CLIENT_SECRET"] = client_secret
    env["TARGET_CHANNEL"] = target_channel

    if bot_path:
        bot_process = subprocess.Popen(
            ["python", bot_path],
            env=env,
            cwd=os.path.dirname(bot_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        threading.Thread(target=log_reader, args=(bot_process.stdout, "BOT"), daemon=True).start()
        threading.Thread(target=log_reader, args=(bot_process.stderr, "ERR"), daemon=True).start()

def script_unload():
    global bot_process
    if bot_process:
        bot_process.terminate()
        bot_process.wait()
        bot_process = None