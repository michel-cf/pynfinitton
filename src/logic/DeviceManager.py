import libinfinitton


class DeviceManager:

    def __init__(self):
        self.device = libinfinitton.Infinitton()

    @staticmethod
    def is_connected():
        return libinfinitton.Infinitton.is_present()
