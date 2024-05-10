from pathlib import Path
import sys

gmat_install = Path("/workspaces/gmat/R2022a")

api_startup_file_name = "api_startup_file.txt"
gmat_bin = gmat_install / "bin"
startup_file = gmat_bin / api_startup_file_name

if startup_file.exists():
    sys.path.insert(1, str(gmat_bin.resolve()))

    import gmatpy as gmat

    gmat.Setup(str(startup_file))

else:
    print("Cannot find GMAT api_startup_file.txt")
    exit(1)

# Use a core script file to drive the analysis
script = gmat_install / "api" / "Ex_R2020a_ToLuna.script"
gmat.LoadScript(str(script.resolve()))

# Set up the objects used to scan for a solution
burn = gmat.GetObject("TOI")
time = gmat.GetObject("LeoTime")
start = gmat.GetObject("StartEpoch")
tank = gmat.GetObject("FuelTank1")

print()

closest = 1000000000.0
dt = 4000
dv = 2.9
start_time = 0.0

# Scan through the delta-V using the burn object
for i in range(10):
    # Scan through the cost time in low Earth orbit
    for j in range(20):
        # Scan through the epoch of the insertion state into orbit
        for k in range(25):
            start_epoch = k / 2.0
            start.SetField("Value", start_epoch / 24)
            time.SetField("Value", 1500.0 + i * 100)
            burn.SetField("Element1", 3.0 + j * 0.01)
            gmat.RunScript()
            moon_dist = gmat.GetRuntimeObject("MoonDistance")
            r = moon_dist.GetNumber("Value")
            if closest > r or True:
                closest = r
                dt = time.GetNumber("Value")
                dv = burn.GetNumber("Element1")
                start_time = start.GetNumber("Value")
                fuel = tank.GetNumber("FuelMass")

                # Report intermediate results if they are better than previous values
                print(
                    closest,
                    "Launch ",
                    start_time,
                    " Coast time: ",
                    dt,
                    "   Delta-V: ",
                    dv,
                    "   Moon Distance: ",
                    r,
                    " Fuel Mass: ",
                    fuel
                )

# Build the name for the solution script
soln = script.with_stem(script.stem + "_soln")
print("\nSaving solution to ", soln, "\n")

# Set the values for the best solution found
start.SetField("Value", start_time)
time.SetField("Value", dt)
burn.SetField("Element1", dv)

# Write out a script with the best values found
gmat.SaveScript(str(soln.resolve()))
