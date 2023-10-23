# Fediverse JSON Schemas

This is a repository for experiments with defining JSON Schema for Fediverse protocols.

Schemas have currently been created for :

* Activity Streams 2.0
* ActivityPub
* Mastodon ActivityPub
* JSON Resource Description (JRD, Webfinger, NodeInfo)

## Installation

This git repository contains several submodules so you need to clone it using the `--recurse-submodules` option.

`git clone --recurse-submodules <repo-url>`

If you forget to use the extra option, you can initialize the modules with:

`git submodule update --init --recursive`

## Running Tests


To run the tests, you'll need to use poetry to install the package.

```
poetry install
```

and then run the pytest tests:

```bash
poetry run pytest
```

or

```bash
poetry shell
pytest
```

## Schemas

### General Information

The schemas are stored in the `schemas` directory. I use subdirectories to manage the complex schemas.

Rather than one large file, the schemas are currently separated into files that generally correspond to a "type" in the related protocol. In the future, I may consider writing a script to combine the files into one schema file.

The schema ids are in the form `schema:<path>` and, in Python, I use a resolver to map the schema id to the directory and file containing the schema.


### Activity Streams 2.0 (AS2) Schema

Experimental JSON Schema for defining AS2 message constraints and metadata.

The top-level schema is in `as2/activitystreams2-schema.json`. This references type-specific schemas. There are also two special schemas for untyped messages and messages with only extension properties.

Note that *all* properties are optional in AS2. The `{}` document is valid. Specifically, this leads to a somewhat surprising fact that `type` is optional so untyped documents are also valid. The JSON-LD `@context` is optional but a consumer must assume the standard AS2 context (i.e., inject it if it's missing) when using JSON-LD expansion.

Properties can be inherited from a parent type like `Object`, `Links` or `Activity` (and others). To support this inheritance and still validate type-specific properties, any type that has subtypes has their schema split into a `<type>-schema.json` file and a `<type>-base-schema.json` file. Subtypes will then reference the `<type>-base-schema.json` to *inherit* that base type's constraints. This can happen recursively if there are multiple levels of inheritance.

### ActivityPub (AP) Schema

This is a specialization of AS2 that adds new, required and optional properties to the actors (e.g., `inbox`, `endpoints`, ...).

### Mastodon ActivityPub Schema

(This is a WIP.) The Mastodon schema significantly constraints the AP schema. Mastodon supports only a small subset of the AP/AS2 data model.

I'm starting to investigate how many of the Mastodon-specific constrains can be represented in JSON Schema. For example, Mastodon allows a list of types to be specified for an AP Object, but not for an AP Activity.

### JSON Resource Descriptor (JRD) Schema

These schema describe the JRD format used by Webfinger and the top-level link list for the nodeinfo protocol.

## Related

* [Activity Streams 2.0](https://www.w3.org/TR/activitystreams-core/)
* [Activity Streams 2.0 Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/)
* [Activity Streams 2.0 JSON-LD Context](https://www.w3.org/ns/activitystreams.jsonld)
* [ActivityPub](https://www.w3.org/TR/activitypub/)
* [Mastodon ActivityPub](https://docs.joinmastodon.org/spec/activitypub/)
* [Webfinger/JRD](https://www.rfc-editor.org/rfc/rfc7033)
* [Nodeinfo](https://github.com/jhass/nodeinfo/blob/main/PROTOCOL.md)
* [JSON Schema](https://json-schema.org/)
