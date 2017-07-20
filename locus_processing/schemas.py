from marshmallow import Schema, fields, post_load, validates_schema
from marshmallow.exceptions import ValidationError

from .models import Chromosome, Coordinates, Snp, Haplotype, Locus


class DictField(fields.Field):
    # adapted from https://github.com/marshmallow-code/marshmallow/issues/120#issuecomment-81382070

    def __init__(self, key_field, nested_field, *args, **kwargs):
        fields.Field.__init__(self, *args, **kwargs)
        self.key_field = key_field
        self.nested_field = nested_field

    def _deserialize(self, value, attr, obj):
        ret = {}
        for key, val in value.items():
            k = self.key_field.deserialize(key)
            v = self.nested_field.deserialize(val)
            ret[k] = v
        return ret

    def _serialize(self, value, attr, obj):
        ret = {}
        for key, val in value.items():
            k = self.key_field._serialize(key, attr, obj)
            v = self.nested_field.serialize(key, self.get_value(attr, obj))
            ret[k] = v
        return ret


class ChromosomeSchema(Schema):
    name = fields.Str()
    accession = fields.Str()

    @post_load
    def make_chromosome(self, data):
        return Chromosome(**data)


class CoordinatesSchema(Schema):
    start = fields.Int()
    end = fields.Int()

    @post_load
    def make_coordinate(self, data):
        return Coordinates(**data)

    @validates_schema
    def validate_location(self, data):
        if data['end'] < data['start']:
            raise ValidationError("End cannot be before start")


class SnpSchema(Schema):
    g_notation = fields.Str()
    alt_notation = fields.Str()
    c_notation = fields.Str(allow_none=True)
    p_notation = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)

    @post_load
    def make_snp(self, data):
        return Snp(**data)


class HaplotypeSchema(Schema):
    name = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True)
    snps = fields.List(fields.Str(), allow_none=True)
    activity = fields.Str(allow_none=True)

    @post_load
    def make_haplotype(self, data):
        return Haplotype(**data)


class LocusSchema(Schema):
    version = fields.Str()
    name = fields.Str()
    reference = fields.Str()
    chromosome = fields.Nested(ChromosomeSchema)
    coordinates = fields.Nested(CoordinatesSchema)
    transcript = fields.Str()
    snps = DictField(fields.Str(), fields.Nested(SnpSchema))
    haplotypes = fields.Nested(HaplotypeSchema, many=True)

    @post_load
    def make_locus(self, data):
        return Locus(**data)
