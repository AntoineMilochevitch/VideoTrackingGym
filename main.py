import videoDetection
import calib
import squatDetection1cam
import curlDetection1cam

def main():
    cam1 = 2
    cam2 = 1
    nbCameras = int(input("Enter the number of cameras (1 or 2): "))
    if nbCameras == 1:
        exoType = int(input("Enter the type of exercise (1 = curl, 2 = squat): "))
        repetitions = int(input("Enter the number of repetitions per set: "))
        sets = int(input("Enter the number of sets: "))
        if exoType == 1:
            curlDetection1cam.main(repetitions,sets)
        elif exoType == 2:
            squatDetection1cam.main(repetitions,sets)
        else:
            print("Invalid exercise type.")
            return
    elif nbCameras == 2:
        calibrate = input("Do you want to calibrate the cameras? (yes/no) ")
        if calibrate.lower() == "yes":
            calib.main()
        exoType = int(input("Enter the type of exercise (1 = curl, 2 = squat): "))
        repetitions = int(input("Enter the number of repetitions per set: "))
        sets = int(input("Enter the number of sets: "))
        videoDetection.main(cam1, cam2, exoType, sets, repetitions)

if __name__ == "__main__":
    main()
