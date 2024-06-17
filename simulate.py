import inspect
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
        fig.add_trace(go.Scatter(x=x, y=y))
        fig.show()

    @staticmethod
    def from_gmat_report(path) -> "ScenarioOutput":
        path = Path(path)
        text = path.read_text()
        text = text.splitlines()
        text = [line.strip().split() for line in text[1:]]
        return ScenarioOutput([(float(line[0]), float(line[1])) for line in text])


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

    gmat.UseLogFile("log.txt")
    gmat.LoadScript(str(scenario.script.resolve()))

    gmat.RunScript()

    return ScenarioOutput.from_gmat_report("/workspaces/gmat/R2022a/output/Mass.txt")


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

    # print(Path("/workspaces/gmat/R2022a/output/log.txt").read_text())


if __name__ == "__main__":
    main()
