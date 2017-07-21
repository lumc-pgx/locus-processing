from typing import List, Dict

from .lookups import fetch_rsid, fetch_sequence


class Chromosome(object):
    def __init__(self, name: str, accession: str):
        self.name = name
        self.accession = accession


class Coordinates(object):
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __len__(self):
        return self.end - self.start


class Snp(object):
    def __init__(self, id: str, g_notation: str, alt_notation: str,
                 c_notation: str, p_notation: str, description: str,
                 tags: List[str]):
        self.id = id
        self.g_notation = g_notation
        self.alt_notation = alt_notation
        self.c_notation = c_notation
        self.p_notation = p_notation
        self.description = description
        self.tags = tags

        self.__rs_id_lookup = None

    @property
    def __get_rs_id_lookup(self) -> dict:
        if self.__rs_id_lookup is None:
            self.__rs_id_lookup = fetch_rsid(self.alt_notation)
        return self.__rs_id_lookup

    @property
    def minor_allele(self) -> str:
        return self.__get_rs_id_lookup.get("minor_allele", "")

    @property
    def major_allele(self) -> str:
        return self.__get_rs_id_lookup.get("ancestral_allele", "")

    @property
    def maf(self) -> float:
        return self.__get_rs_id_lookup.get("MAF", 0.0)

    @property
    def synonyms(self) -> List[str]:
        return self.__get_rs_id_lookup.get("synonyms", [])


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

        self.__sequence = None

    @property
    def sequence(self):
        if self.__sequence is None:
            self.__sequence = fetch_sequence(self.reference,
                                             self.chromosome.name,
                                             self.coordinates.start,
                                             self.coordinates.end)
        return self.__sequence
