from marshmallow import Schema, fields


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


class CoordinatesSchema(Schema):
    start = fields.Int()
    end = fields.Int()


class SnpSchema(Schema):
    g_notation = fields.Str()
    alt_notation = fields.Str()
    c_notation = fields.Str(allow_none=True)
    p_notation = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)


class HaplotypeSchema(Schema):
    name = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True)
    snsps = fields.List(fields.Str(), allow_none=True)
    activity = fields.Str(allow_none=True)


class LocusSchema(Schema):
    version = fields.Str()
    name = fields.Str()
    reference = fields.Str()
    chromosome = fields.Nested(ChromosomeSchema)
    coordinates = fields.Nested(CoordinatesSchema)
    transcript = fields.Str()
    snps = DictField(fields.Str(), fields.Nested(SnpSchema))
    haplotypes = fields.Nested(HaplotypeSchema, many=True)
