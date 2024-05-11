import plotly
import plotly.graph_objects as go
from types import ModuleType
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass
class Scenario:
    script: Path
    crew_count: int
    crew_average_mass: float  # kg
    spacecraft_dry_mass: int  # kg


@dataclass
class ScenarioOutput:
    mass_timeseries: list[tuple[float, float]]

    def plot(self):
        x = [t[0] for t in self.mass_timeseries]
        y = [t[1] for t in self.mass_timeseries]
        fig = go.Figure()
        fig.update_layout(title_text="Mass over time of crewed spacecraft to Luna")
        fig.update_xaxes(title_text="Time (s)")
        fig.update_yaxes(title_text="Mass (kg)")
        fig.add_trace(go.Line(x=x, y=y))
        fig.show()


def load_gmat() -> ModuleType:
    gmat_install = Path("/workspaces/gmat/R2022a")

    api_startup_file_name = "api_startup_file.txt"
    gmat_bin = gmat_install / "bin"
    startup_file = gmat_bin / api_startup_file_name

    if startup_file.exists():
        sys.path.insert(1, str(gmat_bin.resolve()))

        import gmatpy as gmat

        gmat.Setup(str(startup_file))

        return gmat

    else:
        print("Cannot find GMAT api_startup_file.txt")
        exit(1)


def run_scenario(scenario: Scenario) -> ScenarioOutput:

    gmat = load_gmat()

    # Use a core script file to drive the analysis
    gmat.LoadScript(str(scenario.script.resolve()))

    # Set up the objects used to scan for a solution
    sat = gmat.GetObject("Sat")
    dry_mass = float(sat.GetField("DryMass"))
    dry_mass += scenario.crew_average_mass * scenario.crew_count

    sat.SetField("DryMass", dry_mass)

    mass_timeseries = [(0, dry_mass)]

    gmat.RunScript()

    tank = gmat.GetObject("FuelTank1")
    fuel_mass = tank.GetField("FuelMass")

    # TODO... figure out how to advance the simulation in steps and get fuel mass

    final_time = sat.GetField("ElapsedSecs")

    mass_timeseries.append([(final_time, fuel_mass)])

    return ScenarioOutput(mass_timeseries)


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--crew_count",
        "-c",
        type=int,
        default=2,
        help="The number of crew on the spacecraft",
    )
    arg_parser.add_argument(
        "--script",
        "-s",
        type=Path,
        default="lunar_transfer.script",
        help="The path to the GMAT script",
    )
    arg_parser.add_argument("--crew_avg_mass", type=float, default=62, help="units: kg")
    arg_parser.add_argument(
        "--spacecraft_dry_mass", type=float, default=62, help="units: kg"
    )

    args = arg_parser.parse_args()

    scenario = Scenario(
        args.script, args.crew_count, args.crew_avg_mass, args.spacecraft_dry_mass
    )

    output = run_scenario(scenario)

    output.plot()


if __name__ == "__main__":
    main()
