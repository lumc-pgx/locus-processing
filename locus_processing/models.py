from typing import List, Dict


class Chromosome(object):
    def __init__(self, name: str, accession: str):
        self.name = name
        self.accession = accession


class Coordinates(object):
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end


class Snp(object):
    def __init__(self, g_notation: str, alt_notation: str,
                 c_notation: str, p_notation: str, description: str,
                 tags: List[str]):
        self.g_notation = g_notation
        self.alt_notation = alt_notation
        self.c_notation = c_notation
        self.p_notation = p_notation
        self.description = description
        self.tags = tags


class Haplotype(object):
    def __init__(self, name: str, type: str, snps: List[str], activity: str):
        self.name = name
        self.type = type
        self.snps = snps
        self.activity = activity


class Locus(object):
    def __init__(self, version: str, name: str, reference: str,
                 chromosome: Chromosome, coordinates: Coordinates,
                 transcript: str, snps: Dict[str, Snp],
                 haplotypes: List[Haplotype]):
        self.version = version
        self.name = name
        self.reference = reference
        self.chromosome = chromosome
        self.coordinates = coordinates
        self.transcript = transcript
        self.snps = snps
        self.haplotypes = haplotypes
