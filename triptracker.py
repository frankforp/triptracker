from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.settings import SettingsWithNoMenu, SettingsWithTabbedPanel, SettingsWithSidebar
from kivy.logger import Logger
from operations import CurrentDataCollector, Poller, TripDataCollector
from providers import GpsProvider, StubbedProvider
from ui.views import CurrentDataScreen, InactiveTripScreen, TripScreen
from kivy.garden.mapview import MapView


logging_config = '''
[
        {
        "type": "title",
        "title": "These settings will be active when a new trip is started"
    },
    {
        "type": "bool",
        "title": "Enable trip logging",
        "desc": "Enables/disables trip logging.",
        "section": "logging",
        "key": "is_logging_enabled"
    },
    {
        "type": "bool",
        "title": "Enable file logging",
        "desc": "Enables/disables trip logging to file",
        "section": "logging",
        "key": "is_file_logging_enabled"
    },
    {
        "type": "path",
        "title": "Log directory",
        "desc": "Choose the directory where the log files are put",
        "section": "logging",
        "key": "file_log_dir"
    }
]
'''

provider_config = '''
[
    {
        "type": "title",
        "title": "WARNING: Changing any of these settings will restart TripTracker"
    },
    {
        "type": "options",
        "title": "Data provider",
        "desc": "Data source. Real time data through GPSD (GPSD) or data from a GPX file (for demo purposes) (Fake)",
        "section": "providers",
        "key": "provider",
        "options": ["GPSD","Fake"]
    },
    {
        "type": "path",
        "title": "GPX file",
        "desc": "The GPX file that is used for the Fake data provider",
        "section": "providers",
        "key": "fake_file"
    }
]
'''

class TriptrackerApp(App):

    curr_data_collector = CurrentDataCollector()
    trip_collector = TripDataCollector()
    sm = ScreenManager()
    use_kivy_settings = False
    __provider = None
    __should_restart = False

    trip_state = NumericProperty(0)
    is_logging_enabled = BooleanProperty(False)

    def build(self):
        Builder.load_file('ui/triptracker.kv')
        self.settings_cls = SettingsWithSidebar
        # add widgets here
        self.sm.add_widget(CurrentDataScreen(name='current_data'))
        self.sm.add_widget(InactiveTripScreen(name='inactive_trip'))
        self.sm.add_widget(TripScreen(name='trip'))
        return self.sm


    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('logging', {'is_logging_enabled': False, 'is_file_logging_enabled': False, 'file_log_dir': '.'})
        config.setdefaults('providers',
                           {'provider': 'GPSD', 'fake_file': ''})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:

        settings.add_json_panel('Providers', self.config, data=provider_config)
        settings.add_json_panel('Logging', self.config, data=logging_config)

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == 'providers':
            self.__should_restart = True


    def close_settings(self, settings):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        if self.__should_restart:
            self.__stop_app()
            self.__start_app()
            self.__should_restart = False

        super(TriptrackerApp, self).close_settings(settings)



    def on_start(self):
        self.__start_app()

    def on_stop(self):
        self.__stop_app()

    def __start_app(self):
        if self.config.get('providers', 'provider') == 'GPSD':
            self.__provider = GpsProvider()
        else:
           self.__provider = StubbedProvider(self.config.get('providers', 'fake_file'))

        self.__poller = Poller(self.__provider, self.__provider, self.__provider)
        self.__poller.start()

    def __stop_app(self):
        if self.trip_state != 0:
            self.trip_collector.stop()

        self.__poller.stop()



if __name__ == '__main__':
    TriptrackerApp().run()
