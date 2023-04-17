import WalabotAPI as wb
import sys

def main():
    wb.Init()
    wb.SetSettingsFolder()

    try:
        wb.ConnectAny()
    except wb.WalabotError as err:
        print("Failed to connect to Walabot. Error: {}".format(err))
        sys.exit(1)

    wb.SetProfile(wb.PROF_SENSOR)
    wb.SetThreshold(30) # Set a threshold to detect metal objects only
    wb.SetDynamicImageFilter(wb.FILTER_TYPE_MTI)

    arena_params = {
        'minInCm': 10,
        'maxInCm': 100,
        'resInCm': 2
    }

    wb.SetArenaR(arena_params['minInCm'], arena_params['maxInCm'], arena_params['resInCm'])
    wb.SetArenaTheta(-4, 4, 2)
    wb.SetArenaPhi(-4, 4, 2)

    wb.Start()

    while True:
        try:
            wb.Trigger()
            targets = wb.GetSensorTargets()

            if targets:
                for target in targets:
                    if target.zPosCm > 0:  # Ignore objects behind the sensor
                        print("Metal object detected at (x,y,z): ({:.1f}, {:.1f}, {:.1f}) cm".format(target.xPosCm, target.yPosCm, target.zPosCm))
        except KeyboardInterrupt:
            print("Terminating the Walabot metal detection script.")
            break

    wb.Stop()
    wb.Disconnect()
    print("Disconnected from Walabot.")

if __name__ == "__main__":
    main()
