# anycubic-kobra-go-pi-cam
OpenSCAD project for a cam and Raspberry Pi Mount to the top bar of the Anycubic Kobra Go Filament 3D Printer

[This project is on Thingiverse](https://www.thingiverse.com/thing:5815529).

## general information

This small project is meant to mount a `Raspberry Pi 4B` to the top of the `Anycubic Kobra Go` printer between the top bar and the filament holder.  
You'll need to replace the two `M4×6` fabric holding screws of the filament holder by `M4×12` ones, if you want to keep the default filament holder in place.

Additionally, you'll need 4 M3×16 (for the fan ... you may need to adjust the size of those screws to your needs!) as well as 4 M3×20 for the housing. For those 8 screws, you also need some female screws (“Muttern” in German).

The project also has space for a small stripboard (2×7 dots) – which is used for fan control ... the additional information about that piece of hardware as well as the corresponding software / code will also be posted here – soon.

*Holding the stripboard in place isn't designed that well in the current version – that will probably be improved in the future ...*

## the fan

I used an `4.7kΩ` resistor and a NPN transistor of the `BC547` type to make the following work.

![](https://cdn.thingiverse.com/assets/04/60/63/2c/19/f27e3070-734f-469d-aec3-fbca4a250fcf.svg)

### `pip` requirements

As user `root` run `pip install RPi.GPIO gpiozero loguru` or simply run `python -m pip install -r requirements.txt` (as well as `root` user).

### the script

As user `root` place the code of the file `fan-control.py` at `/usr/local/bin/fan-control` and make it executable by `chmod o+x /usr/local/bin/fan-control`.

### the `systemd` service

To run the service on every boot of the Pi, create the file `/etc/systemd/system/fancontrol.service` with the content of the file `fancontrol.service` out of this repository.

Don't forget to enable (`systemctl enable test.service`) and start (`systemctl start test.service` or simply reboot your Pi) your service!

You also can check the (current) logs by running `systemctl status fancontrol.service`.
