import time
import logging
import uiautomator2 as u2
from mobly import test_runner
from mobly import base_test
from mobly.controllers import android_device


class WifiToggleTest(base_test.BaseTestClass):
    def setup_class(self):
        self.ads = self.register_controller(android_device)
        self.dut = self.ads[0]
        device_id = self.dut.serial
        self.device = u2.connect(device_id)
        logging.info("Test setup completed with device ID: %s", device_id)

    def _toggle_switch(self, switch, enable=True):
        if switch.exists:
            current_state = switch.info.get('checked')
            if current_state != enable:
                switch.click()
                time.sleep(2)
                for _ in range(5):
                    new_switch = self.device(className="android.widget.Switch")
                    if new_switch.exists and new_switch.info.get('checked') == enable:
                        logging.info(f"Switch successfully set to {'ON' if enable else 'OFF'}")
                        return
                    time.sleep(1)
                raise AssertionError(f"Failed to set switch to {enable}")
            else:
                logging.info(f"Switch already {'ON' if enable else 'OFF'}")
        else:
            raise Exception("Switch not found")

    def test_01_wifi_toggle_ui_path(self):
        logging.info("Launching Settings app")
        self.dut.adb.shell("am start -n com.android.settings/.Settings")
        time.sleep(3)

        logging.info("Scrolling to 'Network & Internet'")
        self.device(scrollable=True).scroll.to(textContains="Network")
        if not self.device(textContains="Network").click_exists(timeout=5):
            raise Exception("Failed to find 'Network & Internet'")
        time.sleep(2)

        logging.info("Clicking 'Internet'")
        if not self.device(textContains="Internet").click_exists(timeout=5):
            raise Exception("Failed to find 'Internet'")
        time.sleep(2)

        logging.info("Locating Wi-Fi toggle")
        wifi_switch = self.device(className="android.widget.Switch")
        self._toggle_switch(wifi_switch, True)
        self._toggle_switch(wifi_switch, False)

    def test_02_bluetooth_toggle_and_connect(self):
        logging.info("Navigating to Bluetooth settings")
        self.dut.adb.shell("am start -n com.android.settings/.Settings")
        time.sleep(2)

        logging.info("Clicking 'Connected devices'")
        if not self.device(textContains="Connected devices").click_exists(timeout=5):
            raise Exception("Failed to find 'Connected devices'")
        time.sleep(2)

        logging.info("Clicking 'Connection preferences'")
        if not self.device(textContains="Connection preferences").click_exists(timeout=5):
            raise Exception("Failed to find 'Connection preferences'")
        time.sleep(2)

        logging.info("Clicking 'Bluetooth'")
        if not self.device(textContains="Bluetooth").click_exists(timeout=5):
            raise Exception("Failed to find 'Bluetooth'")
        time.sleep(2)

        logging.info("Turning Bluetooth ON")
        bt_switch = self.device(className="android.widget.Switch")
        self._toggle_switch(bt_switch, True)
        time.sleep(3)

        # Start scanning for devices
        logging.info("Clicking 'Pair new device'")
        if self.device(textContains="Pair new device").exists:
            self.device(textContains="Pair new device").click()
        else:
            raise Exception("Could not find 'Pair new device' option")
        time.sleep(5)

        # Replace this with your actual target Bluetooth device name
        target_device_name = "YourDeviceName"
        logging.info(f"Looking for device named: {target_device_name}")
        found = False
        for _ in range(10):
            if self.device(text=target_device_name).exists:
                self.device(text=target_device_name).click()
                found = True
                logging.info("Device found and clicked.")
                break
            time.sleep(2)

        if not found:
            raise Exception(f"Device '{target_device_name}' not found during scan.")

        time.sleep(5)
        if self.device(text='Pair').exists:
            logging.info("Pairing request detected. Clicking 'Pair'")
            self.device(text='Pair').click()
        elif self.device(text='OK').exists:
            self.device(text='OK').click()

        logging.info("Waiting for connection confirmation...")
        time.sleep(8)
        if self.device(text=target_device_name).exists and self.device(text="Connected").exists:
            logging.info(f"Successfully connected to {target_device_name}")
        else:
            raise AssertionError(f"Failed to connect to {target_device_name}")

    def test_03_location_toggle_ui_path(self):
        logging.info("Navigating to Location settings")
        self.dut.adb.shell("am start -n com.android.settings/.Settings")
        time.sleep(3)

        try:
            self.device(scrollable=True).scroll.to(text="Location")
        except Exception as e:
            logging.error(f"Scroll to 'Location' failed: {e}")
            raise Exception("Could not scroll to 'Location'. Adjust text or UI path.")

        if not self.device(text="Location").click_exists(timeout=5):
            raise Exception("Failed to find 'Location'")
        time.sleep(2)

        logging.info("Locating Location toggle")
        loc_switch = self.device(className="android.widget.Switch")
        self._toggle_switch(loc_switch, True)
        self._toggle_switch(loc_switch, False)

    def test_04_mobile_data_toggle_ui_path(self):
        logging.info("Navigating to Mobile Network settings")
        self.dut.adb.shell("am start -n com.android.settings/.Settings")
        time.sleep(3)

        self.device(scrollable=True).scroll.to(textContains="Network")
        if not self.device(textContains="Network").click_exists(timeout=5):
            raise Exception("Failed to find 'Network & Internet'")
        time.sleep(2)

        if not self.device(textContains="Mobile network").click_exists(timeout=5):
            raise Exception("Failed to find 'Mobile network'")
        time.sleep(2)

        data_switch = self.device(className="android.widget.Switch")
        if not data_switch.exists:
            raise Exception("Mobile Data toggle not found")

        self._toggle_switch(data_switch, True)

        logging.info("Toggling Mobile Data OFF")
        data_switch.click()
        for _ in range(5):
            if self.device(text='Turn off').exists or self.device(text='Turn off Jio?').exists:
                if self.device(text='Yes').click_exists(timeout=2):
                    break
            time.sleep(1)

        time.sleep(4)
        data_switch = self.device(className="android.widget.Switch")
        if not data_switch.exists:
            raise Exception("Mobile Data toggle switch disappeared unexpectedly")

        assert not data_switch.info.get('checked'), "Failed to turn Mobile Data OFF"
        self._toggle_switch(data_switch, True)
        logging.info("Mobile Data toggled successfully")


if __name__ == '__main__':
    test_runner.main()



import time
import logging
import uiautomator2 as u2
from mobly import test_runner
from mobly import base_test
from mobly.controllers import android_device


class WifiToggleTest(base_test.BaseTestClass):
    def setup_class(self):
        self.ads = self.register_controller(android_device)
        self.dut = self.ads[0]
        device_id = self.dut.serial
        self.device = u2.connect(device_id)
        logging.info("Test setup completed with device ID: %s", device_id)

    def _toggle_switch(self, switch, enable=True):
        if switch.exists:
            current_state = switch.info.get('checked')
            if current_state != enable:
                switch.click()
                time.sleep(2)
                for _ in range(5):
                    new_switch = self.device(className="android.widget.Switch")
                    if new_switch.exists and new_switch.info.get('checked') == enable:
                        logging.info(f"Switch successfully set to {'ON' if enable else 'OFF'}")
                        return
                    time.sleep(1)
                raise AssertionError(f"Failed to set switch to {enable}")
            else:
                logging.info(f"Switch already {'ON' if enable else 'OFF'}")
        else:
            raise Exception("Switch not found")

    def test_01_wifi_toggle_ui_path(self):
        logging.info("Launching Settings app")
        self.dut.adb.shell("am start -n com.android.settings/.Settings")
        time.sleep(3)

        logging.info("Scrolling to 'Network & Internet'")
        self.device(scrollable=True).scroll.to(textContains="Network")
        if not self.device(textContains="Network").click_exists(timeout=5):
            raise Exception("Failed to find 'Network & Internet'")
        time.sleep(2)

        logging.info("Clicking 'Internet'")
        if not self.device(textContains="Internet").click_exists(timeout=5):
            raise Exception("Failed to find 'Internet'")
        time.sleep(2)

        logging.info("Locating Wi-Fi toggle")
        wifi_switch = self.device(className="android.widget.Switch")
        self._toggle_switch(wifi_switch, True)
        self._toggle_switch(wifi_switch, False)

    def test_02_bluetooth_toggle_and_connect(self):
        logging.info("Navigating to Bluetooth settings")
        self.dut.adb.shell("am start -n com.android.settings/.Settings")
        time.sleep(2)

        logging.info("Clicking 'Connected devices'")
        if not self.device(textContains="Connected devices").click_exists(timeout=3):
            raise Exception("Failed to find 'Connected devices'")
        time.sleep(2)

        logging.info("Clicking 'Connection preferences'")
        if not self.device(textContains="Connection preferences").click_exists(timeout=3):
            raise Exception("Failed to find 'Connection preferences'")
        time.sleep(2)

        logging.info("Clicking 'Bluetooth'")
        if not self.device(textContains="Bluetooth").click_exists(timeout=3):
            raise Exception("Failed to find 'Bluetooth'")
        time.sleep(2)

        logging.info("Turning Bluetooth ON")
        bt_switch = self.device(className="android.widget.Switch")
        self._toggle_switch(bt_switch, True)
        time.sleep(3)

        logging.info("Clicking 'Pair new device'")
        if self.device(textContains="Pair new device").exists:
            self.device(textContains="Pair new device").click()
        else:
            raise Exception("Could not find 'Pair new device' option")
        time.sleep(3)

        target_device_name = "YourDeviceName"
        logging.info(f"Looking for device named: {target_device_name}")
        found = False
        for _ in range(10):
            if self.device(text=target_device_name).exists:
                self.device(text=target_device_name).click()
                found = True
                logging.info("Device found and clicked.")
                break
            time.sleep(2)

        if not found:
            raise Exception(f"Device '{target_device_name}' not found during scan.")

        time.sleep(5)
        if self.device(text='Pair').exists:
            self.device(text='Pair').click()
        elif self.device(text='OK').exists:
            self.device(text='OK').click()

        logging.info("Waiting for connection confirmation...")
        time.sleep(8)
        if self.device(text=target_device_name).exists and self.device(text="Connected").exists:
            logging.info(f"Successfully connected to {target_device_name}")
        else:
            raise AssertionError(f"Failed to connect to {target_device_name}")

    def test_03_location_toggle_ui_path(self):
        logging.info("Navigating to Location settings")
        self.dut.adb.shell("am start -n com.android.settings/.Settings")
        time.sleep(3)

        self.device(scrollable=True).scroll.to(text="Location")
        if not self.device(text="Location").click_exists(timeout=5):
            raise Exception("Failed to find 'Location'")
        time.sleep(2)

        logging.info("Locating Location toggle")
        loc_switch = self.device(className="android.widget.Switch")
        self._toggle_switch(loc_switch, True)
        self._toggle_switch(loc_switch, False)

    def test_04_mobile_data_toggle_ui_path(self):
        logging.info("Navigating to Mobile Network settings")
        self.dut.adb.shell("am start -n com.android.settings/.Settings")
        time.sleep(3)

        self.device(scrollable=True).scroll.to(textContains="Network")
        if not self.device(textContains="Network").click_exists(timeout=5):
            raise Exception("Failed to find 'Network & Internet'")
        time.sleep(2)

        if not self.device(textContains="Mobile network").click_exists(timeout=5):
            raise Exception("Failed to find 'Mobile network'")
        time.sleep(2)

        data_switch = self.device(className="android.widget.Switch")
        if not data_switch.exists:
            raise Exception("Mobile Data toggle not found")

        self._toggle_switch(data_switch, True)

        logging.info("Toggling Mobile Data OFF")
        data_switch.click()
        for _ in range(5):
            if self.device(text='Turn off').exists or self.device(text='Turn off Jio?').exists:
                if self.device(text='Yes').click_exists(timeout=2):
                    break
            time.sleep(1)

        time.sleep(4)
        data_switch = self.device(className="android.widget.Switch")
        if not data_switch.exists:
            raise Exception("Mobile Data toggle switch disappeared unexpectedly")

        assert not data_switch.info.get('checked'), "Failed to turn Mobile Data OFF"
        self._toggle_switch(data_switch, True)
        logging.info("Mobile Data toggled successfully")

    def test_05_battery_saver_toggle_ui_path(self):
        logging.info("Navigating to Battery Saver settings")
        self.dut.adb.shell("am start -a android.settings.BATTERY_SAVER_SETTINGS")
        time.sleep(3)

        logging.info("Looking for Battery Saver toggle switch")
        batt_switch = self.device(className="android.widget.Switch")
        if not batt_switch.exists:
            raise Exception("Battery Saver toggle not found")

        self._toggle_switch(batt_switch, True)
        time.sleep(2)
        self._toggle_switch(batt_switch, False)
        logging.info("Battery Saver toggled ON then OFF successfully")

    def test_06_dark_theme_toggle_ui_path(self):
        logging.info("Navigating to Display settings for Dark Theme")
        self.dut.adb.shell("am start -n com.android.settings/.Settings")
        time.sleep(3)

        logging.info("Scrolling to 'Display'")
        self.device(scrollable=True).scroll.to(text="Display")
        if not self.device(text="Display").click_exists(timeout=5):
            raise Exception("Failed to find 'Display' settings")
        time.sleep(2)

        logging.info("Locating 'Dark theme' toggle")
        self.device(scrollable=True).scroll.to(textContains="Dark theme")
        if not self.device(textContains="Dark theme").click_exists(timeout=5):
            raise Exception("Failed to find 'Dark theme' option")
        time.sleep(2)

        dark_switch = self.device(className="android.widget.Switch")
        if not dark_switch.exists:
            raise Exception("Dark Theme switch not found")

        self._toggle_switch(dark_switch, True)
        time.sleep(2)
        self._toggle_switch(dark_switch, False)
        logging.info("Dark Theme toggled ON then OFF successfully")


if __name__ == '__main__':
    test_runner.main()

