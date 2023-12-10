# pydantic_marshmallow_tests

## Pydantic benefits

### Nested creation of objects from json

`Settings` can have nested `Comparisons`, which have `ComparisonLevel`s.

These objects will be auto-instantiated with `Settings(settings_dict)`

### Automatic support for instantiating mix of dicts and objects

e.g. `comparisons` can be `[dict, Comparison]` and this will be automatically turned into `[Comparison, Comparison]`

### Automatic dump to dict or json

Once models have been defined, you get json dump and json load for free

### Validation

If a user accidentally puts a `ComparisonLevel` where a comparison should go, an error will be raised
It's possible to add arbitrary validation, such as on enums, or checking 0 < value < 1

### Automatic json schema

A [jsonschema](https://json-schema.org/draft/2020-12/release-notes) compatible json schema can be generated with `settings.model_json_schema()`

## Marshmallow comparison

https://www.augmentedmind.de/2020/10/25/marshmallow-vs-pydantic-python/

Marshmallow has fewer dependencies
https://libraries.io/pypi/pydantic/2.5.2/tree

Marshmallow is more verbose in its vanilla form. there's a lib called marshmallow data classes that possibly helps.

> It was created before there existed Python type hints. So, to define every schema you need to use specific utils and classes provided by Marshmallow. [link](https://fastapi.tiangolo.com/tr/alternatives/#marshmallow)

> [Pydantic] is comparable to Marshmallow. Although it's faster than Marshmallow in benchmarks. And as it is based on the same Python type hints, the editor support is great. [link](https://fastapi.tiangolo.com/tr/alternatives/#pydantic)

> You need to decide early on whether you want to put class definition and schema definition into a single class (using a dataclass - the Pydantic way), or whether to keep them separated (marshmallow). The latter is semantically cleaner, but involves writing more code.[link](https://www.augmentedmind.de/2020/10/25/marshmallow-vs-pydantic-python/)
