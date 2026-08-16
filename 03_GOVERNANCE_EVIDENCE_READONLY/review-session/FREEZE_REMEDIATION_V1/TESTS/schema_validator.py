import re, json, os

class ValidationError(Exception):
    pass

class SchemaValidator:
    def __init__(self, root_schema):
        self.root_schema = root_schema
        self.defs = root_schema.get('$defs', {})

    def resolve_ref(self, ref):
        if ref.startswith('#/$defs/'):
            def_name = ref.replace('#/$defs/', '')
            if def_name in self.defs:
                return self.defs[def_name]
            raise ValidationError(f'Definition {def_name} not found in $defs')
        raise ValidationError(f'External ref {ref} not supported')

    def validate(self, instance, schema=None):
        if schema is None:
            schema = self.root_schema

        if '$ref' in schema:
            schema = self.resolve_ref(schema['$ref'])

        # Type validation
        expected_type = schema.get('type')
        if expected_type:
            if expected_type == 'object' and not isinstance(instance, dict):
                raise ValidationError(f'Expected object, got {type(instance).__name__}')
            elif expected_type == 'array' and not isinstance(instance, list):
                raise ValidationError(f'Expected array, got {type(instance).__name__}')
            elif expected_type == 'string' and not isinstance(instance, str):
                raise ValidationError(f'Expected string, got {type(instance).__name__}')
            elif expected_type == 'integer' and (not isinstance(instance, int) or isinstance(instance, bool)):
                raise ValidationError(f'Expected integer, got {type(instance).__name__}')
            elif expected_type == 'number' and not (isinstance(instance, (int, float)) and not isinstance(instance, bool)):
                raise ValidationError(f'Expected number, got {type(instance).__name__}')
            elif expected_type == 'boolean' and not isinstance(instance, bool):
                raise ValidationError(f'Expected boolean, got {type(instance).__name__}')

        # Enum validation
        if 'enum' in schema:
            if instance not in schema['enum']:
                raise ValidationError(f'Value {instance} not in enum {schema["enum"]}')

        # Const validation
        if 'const' in schema:
            if instance != schema['const']:
                raise ValidationError(f'Value {instance} does not match const {schema["const"]}')

        # String constraints
        if isinstance(instance, str):
            if 'minLength' in schema and len(instance) < schema['minLength']:
                raise ValidationError(f'String length {len(instance)} < minLength {schema["minLength"]}')
            if 'pattern' in schema:
                if not re.search(schema['pattern'], instance):
                    raise ValidationError(f'String "{instance}" does not match pattern "{schema["pattern"]}"')
            if 'format' in schema:
                fmt = schema['format']
                if fmt == 'uuid':
                    uuid_regex = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
                    if not re.match(uuid_regex, instance):
                        raise ValidationError(f'String "{instance}" is not a valid UUID format')

        # Number constraints
        if isinstance(instance, (int, float)) and not isinstance(instance, bool):
            if 'minimum' in schema and instance < schema['minimum']:
                raise ValidationError(f'Value {instance} < minimum {schema["minimum"]}')
            if 'maximum' in schema and instance > schema['maximum']:
                raise ValidationError(f'Value {instance} > maximum {schema["maximum"]}')

        # Object constraints
        if isinstance(instance, dict):
            required = schema.get('required', [])
            for req in required:
                if req not in instance:
                    raise ValidationError(f'Missing required property: "{req}"')

            props = schema.get('properties', {})
            additional_props = schema.get('additionalProperties', True)

            for k, v in instance.items():
                if k in props:
                    self.validate(v, props[k])
                elif not additional_props:
                    raise ValidationError(f'Additional property "{k}" not allowed')

        # Array constraints
        if isinstance(instance, list):
            if 'minItems' in schema and len(instance) < schema['minItems']:
                raise ValidationError(f'Array items count {len(instance)} < minItems {schema["minItems"]}')
            items_schema = schema.get('items')
            if items_schema:
                for item in instance:
                    self.validate(item, items_schema)

        # oneOf validation
        if 'oneOf' in schema:
            matches = 0
            last_err = None
            for sub_schema in schema['oneOf']:
                try:
                    combined = dict(schema)
                    del combined['oneOf']
                    # merge properties and required
                    if 'properties' in sub_schema:
                        combined_props = dict(combined.get('properties', {}))
                        combined_props.update(sub_schema['properties'])
                        combined['properties'] = combined_props
                    if 'required' in sub_schema:
                        combined_req = list(combined.get('required', []))
                        combined_req.extend(sub_schema['required'])
                        combined['required'] = list(set(combined_req))
                    self.validate(instance, combined)
                    matches += 1
                except ValidationError as e:
                    last_err = e
            if matches != 1:
                raise ValidationError(f'Expected exactly oneOf match, got {matches}. Last error: {last_err}')

        return True
