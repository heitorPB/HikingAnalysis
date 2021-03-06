import os
import click
from hikingAnalysis.HikingAnalysis import HikingAnalysis


@click.command()
@click.option('--plot-3D/--no-plot-3D', default=True, show_default=True,
              help="Make a 3D visualisation of the hike")
@click.option('--plot-2D/--no-plot-2D', default=True, show_default=True,
              help="Make a 2D map the hike")
@click.option('--statistics/--no-statistics', default=True, show_default=True,
              help="Print statistics of the hike")
@click.argument('input', type=click.Path(exists=True))
@click.argument('output-dir', default=".", type=click.Path(exists=True))
def cli(input, output_dir, statistics, plot_2d, plot_3d):
    hike = HikingAnalysis(input, output_dir, statistics, plot_2d, plot_3d)
    hike.go()


if __name__ == "__main__":
    cli()
