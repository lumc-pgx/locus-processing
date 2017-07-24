from os import listdir
from os.path import join, isfile

import click

from . import load_locus_yaml


def _validate_inputs(ctx, param, value):
    """Mutually exclusive group for -I and -D"""
    if param.name == "input_directory":
        idir = value
        ifile = ctx.params.get("input")
    elif param.name == "input":
        ifile = value
        idir = ctx.params.get("input_directory")
    else:
        ifile = None
        idir = None

    if (ifile is None and idir is None) or (ifile is not None and idir is not None):
        raise click.BadArgumentUsage("Either --input OR --input-directory must be set")

    return value


def _single_locus_to_bed(path, prefix):
    bed_fmt = "{chrom}\t{start}\t{end}\t{name}"
    loc = load_locus_yaml(path)
    if prefix is not None:
        name = "{0}_{1}".format(prefix, loc.name)
    else:
        name = loc.name
    bed = bed_fmt.format(
        chrom=loc.chromosome.name,
        start=loc.coordinates.start,
        end=loc.coordinates.end,
        name=name
    )
    return bed


@click.command(short_help="Write regions in locus files to bed")
@click.option("--input", "-I", type=click.Path(exists=True),
              help="Path to input locus file")
@click.option("--input-directory", "-D",
              type=click.Path(exists=True, file_okay=False, dir_okay=True),
              help="Path to directory containing locus files", callback=_validate_inputs)
@click.option("--prefix", "-p",
              type=click.STRING, help="Prefix to region names")
def locus_to_bed(input=None, input_directory=None, prefix=None):
    if input:
        print(_single_locus_to_bed(input, prefix))
    else:
        candidates = [join(input_directory, x) for x in listdir(input_directory)]
        yamls = filter(lambda x: isfile(x) and (x.endswith(".yaml") or x.endswith(".yml")), candidates)
        for y in yamls:
            print(_single_locus_to_bed(y, prefix))


def _validate_single_locus(path):
    click.echo("{0}: ".format(path), nl=False)
    try:
        _ = load_locus_yaml(path)
    except ValueError as error:
        return_str = "ERROR, {r}".format(r=str(error))
        click.secho(return_str, fg="red")
    else:
        return_str = "PASS"
        click.secho(return_str, fg="green")


@click.command(short_help="Validate locus definiton files")
@click.option("--input", "-I", type=click.Path(exists=True),
              help="Path to input locus file")
@click.option("--input-directory", "-D",
              type=click.Path(exists=True, file_okay=False, dir_okay=True),
              help="Path to directory containing locus files",
              callback=_validate_inputs)
def validate_locus(input=None, input_directory=None):
    if input is not None:
        _validate_single_locus(input)
    else:
        candidates = [join(input_directory, x) for x in listdir(input_directory)]
        yamls = filter(lambda x: isfile(x) and (x.endswith(".yaml") or x.endswith(".yml")), candidates)
        for y in yamls:
            _validate_single_locus(y)
