from ids_peak import ids_peak
from ids_peak_ipl import ids_peak_ipl
from ids_peak import ids_peak_ipl_extension


class IDSCamera(object):
    """IDS Camera interface, keeping all memory and low level bus management opaque
    to the user, for ease of use."""

    def __init__(self):
        ids_peak.Library.Initialize()

        self.__acquisition_ready = False
        self.__pixel_format = ids_peak_ipl.PixelFormatName_BGRa8
        self.__resolution = None
        self.__device = None
        self.__datastream = None

        self.__create_device_manager()

    def __create_device_manager(self):

        self.__device_manager = ids_peak.DeviceManager.Instance()

        self.__device_manager.Update()

        # Si no hem trobat cap càmera, tallem pel dret!
        if self.__device_manager.Devices().empty():
            self.__destroy()
            raise ids_peak.NotFoundException("No devices found!")

    def __setup_data_stream(self):
        datastreams = self.__device.DataStreams()

        if datastreams.empty():
            self.__destroy()
            raise ids_peak.NotAvailableException("Devie has no DataStream!")

        self.__datastream = datastreams[0].OpenDataStream()
        self.__nodemap_remote_device = self.__device.RemoteDevice().NodeMaps()[0]
        # Preparem captures d'imatge contínues
        try:
            self.__nodemap_remote_device.FindNode("UserSetSelector").SetCurrentEntry("Default")
            self.__nodemap_remote_device.FindNode("UserSetLoad").Execute()
            self.__nodemap_remote_device.FindNode("UserSetLoad").WaitUntilDone()
        except ids_peak.Exception:
            # Userset is not available
            pass
        payload_size = self.__nodemap_remote_device.FindNode("PayloadSize").Value()

        buffer_count_max = self.__datastream.NumBuffersAnnouncedMinRequired()
        # Allocate and announce image buffers and queue them
        for i in range(buffer_count_max):
            buffer = self.__datastream.AllocAndAnnounceBuffer(payload_size)
            self.__datastream.QueueBuffer(buffer)

    def __setup_nodemap(self):
        self.__nodemap_remote_device = self.__device.RemoteDevice().NodeMaps()[0]

    def __stop_acquisition(self):
        if not self.__device:
            return
        # Otherwise try to stop acquisition
        try:
            remote_nodemap = self.__device.RemoteDevice().NodeMaps()[0]
            remote_nodemap.FindNode("AcquisitionStop").Execute()

            # Stop and flush datastream
            self.__datastream.KillWait()
            self.__datastream.StopAcquisition(ids_peak.AcquisitionStopMode_Default)
            self.__datastream.Flush(ids_peak.DataStreamFlushMode_DiscardAll)

            self.__acquisition_running = False

            # Unlock parameters after acquisition stop
            if self.__nodemap_remote_device is not None:
                try:
                    self.__nodemap_remote_device.FindNode("TLParamsLocked").SetValue(0)
                except Exception as e:
                    raise e

        except Exception as e:
            raise e

    def get_devices(self):
        return self.__device_manager.Devices()

    def select_device(self, device_idx):
        self.__device = None
        try:
            device = self.__device_manager.Devices()[device_idx]
        except:
            self.__destroy()
            raise KeyError(f"Device {device_idx} not found")

        # Intenta obrir la càmera
        if not device.IsOpenable():
            self.__destroy()
            raise ids_peak.NotAvailableException(f"Device {device_idx} could not be opened")

        self.__device = device.OpenDevice(ids_peak.DeviceAccessType_Control)

        # Con
        self.__setup_data_stream()

    def set_fps(self, fps: float):
        """Intenta configurar les imatges per segon que la càmera capturarà, fins el màxim establert
        per la pròpia càmera."""
        try:
            max_fps = self.__nodemap_remote_device.FindNode("AcquisitionFrameRate").Maximum()
            target_fps = min(max_fps, fps)
            self.__nodemap_remote_device.FindNode("AcquisitionFrameRate").SetValue(target_fps)
        except ids_peak.Exception as e:
            raise e

    def get_fps(self):
        """Retorna els fps actuals amb els què treballa la càmera."""
        try:
            current_fps = self.__nodemap_remote_device.FindNode("AcquisitionFrameRate").Value()
        except ids_peak.Exception as e:
            raise e
        return current_fps

    def set_exposure_time(self, etime: float):
        try:
            # Hem d'assegurar que el temps es trobi entre el mínim i màxim d'exposició actuals de la càmera
            minexp = self.__nodemap_remote_device.FindNode("ExposureTime").Minimum()
            maxexp = self.__nodemap_remote_device.FindNode("ExposureTime").Maximum()
            target_exposure = max(minexp, min(maxexp, etime))
            self.__nodemap_remote_device.FindNode("ExposureTime").SetValue(target_exposure)
        except ids_peak.Exception as e:
            raise e

    def get_exposure_time(self):
        """Retorna el temps d'exposició actual de la càmera, en microsegons."""
        try:
            current_etime = self.__nodemap_remote_device.FindNode("ExposureTime").Value()
        except ids_peak.Exception as e:
            raise e
        return current_etime

    def get_resolution(self):
        if not self.__device:
            raise NameError("Device not selected")
        try:
            width = self.__nodemap_remote_device.FindNode("Width").Value()
            height = self.__nodemap_remote_device.FindNode("Height").Value()
        except ids_peak.Exception as e:
            raise e
        return width, height

    def start_acquisition(self):
        """Comença la captura contínua d'imatges amb els paràmetres seleccionats."""
        try:
            self.__nodemap_remote_device.FindNode("TLParamsLocked").SetValue(1)

            self.__datastream.StartAcquisition()
            self.__nodemap_remote_device.FindNode("AcquisitionStart").Execute()
            self.__nodemap_remote_device.FindNode("AcquisitionStart").WaitUntilDone()
        except Exception as e:
            raise e

        self.__acquisition_ready = True

    def set_pixel_format(self, kind):
        """Selecciona el format en què es guardaran les imatges."""
        if kind == "BGRa8":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BGRa8
        elif kind == "BGRa10":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BGRa10
        elif kind == "BGRa12":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BGRa12
        elif kind == "Mono8":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_Mono8
        elif kind == "Mono10":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_Mono10
        elif kind == "Mono12":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_Mono12
        elif kind == "BayerRG8":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BayerRG8
        elif kind == "BayerRG10":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BayerRG10
        elif kind == "BayerRG12":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BayerRG12
        elif kind == "BayerGR8":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BayerGR8
        elif kind == "BayerGR10":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BayerGR10
        elif kind == "BayerGR12":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BayerGR12
        elif kind == "BayerBG8":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BayerBG8
        elif kind == "BayerBG10":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BayerBG10
        elif kind == "BayerBG12":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BayerBG12
        elif kind == "BayerGB8":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BayerGB8
        elif kind == "BayerGB10":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BayerGB10
        elif kind == "BayerGB12":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BayerGB12
        elif kind == "BGR8":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BGR8
        elif kind == "BGR10":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BGR10
        elif kind == "BGR12":
            self.__pixel_format = ids_peak_ipl.PixelFormatName_BGR12

    def capture(self):
        if not self.__acquisition_ready:
            raise RuntimeError("Acquisition not ready")
        
        # Recuperem el buffer directament de la càmera
        buff = self.__datastream.WaitForFinishedBuffer(5000)
        # Recuperem la imatge i fem debayering si cal
        ipl_image = ids_peak_ipl_extension.BufferToImage(buff)
        converted_image = ipl_image.ConvertTo(self.__pixel_format)
        # Indiquem que el búffer es pot tornar a utilitzar
        self.__datastream.QueueBuffer(buff)
        # Retornem la imatge en format numpy
        image_array = converted_image.get_numpy_1D().copy()
        return image_array

    def __destroy(self):
        try:
            self.__stop_acquisition()
        except Exception as e:
            pass
        
        ids_peak.Library.Close()

    def __del__(self):
        self.__destroy()

