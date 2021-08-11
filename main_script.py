import obspython as obs
import steam_achievements, generate_txt_file

api_key = ""
steam_id = ""
time = 10

# Script
def script():
  global api_key, steam_id

  if (api_key !=  "" and steam_id != ""):
    achievements = steam_achievements.get_steam_achievements(api_key, steam_id)
    generate_txt_file.generate_txt_file(achievements)
  else:
    obs.timer_remove(script)
    obs.remove_current_callback()

def script_load(settings):
  obs.timer_add(script, time*60000)

# Description displayed in the Scripts dialog window
def script_description():
  return """<center><h2>Steam achievements board</h2></center>
            <p>This script allows you to display your steam achievements and some calculated values in your stream.</p>"""



# Called to set default values of data settings
def script_defaults(settings):
  obs.obs_data_set_default_string(settings, "api_key", "")
  obs.obs_data_set_default_string(settings, "steam_id", "")
  obs.obs_data_set_default_int(settings, "time", 10)

# Called to display the properties GUI
def script_properties():
  props = obs.obs_properties_create()
  obs.obs_properties_add_text(props, "api_key", "API Key", obs.OBS_TEXT_DEFAULT)
  obs.obs_properties_add_text(props, "steam_id", "Steam ID", obs.OBS_TEXT_DEFAULT)
  obs.obs_properties_add_int(props, "time", "Time between executes (in minutes)", 1, 60, 1)
  
  return props

# Called after change of settings including once after script load
def script_update(settings):
  global api_key, steam_id, time

  obs.timer_remove(script)

  api_key = obs.obs_data_get_string(settings, "api_key")
  steam_id = obs.obs_data_get_string(settings, "steam_id")
  time = obs.obs_data_get_int(settings, "time")

  script()
  obs.timer_add(script, time*60000)

# Called before data settings are saved
def script_save(settings):
  obs.obs_save_sources()

def script_unload():
    obs.timer_remove(script)