# Chapter 6: OOP

This chapter provides a comprehensive guide to object-oriented programming in Python, from foundational concepts through advanced topics like descriptors, metaclasses, dataclasses, and design patterns.

## 6.1 OOP Foundations

- [Procedural vs OOP](foundations/procedural_vs_oop.md)
- [Functions to Classes](foundations/functions_to_classes.md)
- [Classes and Instances](foundations/classes_instances.md)
- [Constructor and Destructor](foundations/constructor_destructor.md)

## 6.2 Attributes and Methods

- [Instance Attributes](object_model/instance_attributes.md)
- [Class Attributes](object_model/class_attributes.md)
- [Attribute Lookup](object_model/attribute_lookup.md)
- [Instance Methods](object_model/instance_methods.md)
- [Class Methods](object_model/class_methods.md)
- [Static Methods](object_model/static_methods.md)

## 6.3 Four Pillars of OOP

- [Encapsulation](pillars/encapsulation.md)
- [Abstraction](pillars/abstraction.md)
- [Polymorphism](pillars/polymorphism.md)
- [Inheritance Basics](pillars/inheritance.md)

## 6.4 Advanced Inheritance

- [Initialization Patterns](inheritance/initialization_patterns.md)
- [super() and Cooperation](inheritance/super.md)
- [Method Resolution Order](inheritance/mro.md)
- [C3 Linearization](inheritance/c3_linearization.md)

## 6.5 Composition and Aggregation

- [Is-a vs Has-a](composition/isa_vs_hasa.md)
- [Composition Pattern](composition/composition_pattern.md)
- [Aggregation Pattern](composition/aggregation_pattern.md)
- [Composition vs Inheritance](composition/composition_vs_inheritance.md)
- [Design Guidelines](composition/design_guidelines.md)

## 6.6 Dunder Basics

- [Introduction](dunder/dunder_intro.md)
- [Arithmetic Operators](dunder/dunder_arithmetic.md)
- [Comparison Operators](dunder/dunder_comparison.md)
- [Object Lifecycle](dunder/dunder_lifecycle.md)
- [String Representation](dunder/dunder_string.md)
- [Magic Methods Quick Reference](dunder/magic_methods_quick_reference.md)
- [Magic Methods Exercises](dunder/magic_methods_exercises.md)

## 6.7 Dunder Advanced

- [Container Protocol](dunder_advanced/dunder_containers.md)
- [Iteration Protocol](dunder_advanced/dunder_iterables.md)
- [Callable Objects](dunder_advanced/dunder_callable.md)
- [Context Managers](dunder_advanced/dunder_context.md)

## 6.8 Properties

- [Properties](object_model/properties.md)
- [Cached Properties](object_model/cached_property.md)
- [Properties as Descriptors](object_model/property_descriptor_connection.md)

## 6.9 Descriptor Protocol

- [Descriptor Introduction](descriptors/descriptor_intro.md)
- [\_\_get\_\_ \_\_set\_\_ \_\_delete\_\_](descriptors/descriptor_methods.md)
- [Data vs Non-Data Descriptors](descriptors/descriptor_types.md)
- [Descriptor Use Cases](descriptors/descriptor_applications.md)
- [Attribute Access Lookup](descriptors/attribute_access_lookup.md)

## 6.10 Dunder Attribute Hooks

- [\_\_getattribute\_\_](dunder_attrs/dunder_getattribute.md)
- [\_\_getattr\_\_](dunder_attrs/dunder_getattr.md)
- [\_\_setattr\_\_](dunder_attrs/dunder_setattr.md)
- [\_\_delattr\_\_](dunder_attrs/dunder_delattr.md)

## 6.11 Dynamic Attribute Access

- [getattr setattr delattr](dynamic/builtin_attr_functions.md)
- [Dynamic vs Static Access](dynamic/dynamic_vs_static.md)

## 6.12 dataclasses

- [dataclasses Module](dataclasses/dataclasses.md)
- [field() Function](dataclasses/field.md)
- [\_\_post\_init\_\_ Method](dataclasses/post_init.md)
- [Frozen Dataclasses](dataclasses/frozen.md)
- [Dataclass Inheritance](dataclasses/inheritance.md)
- [slots and kw_only](dataclasses/slots_kw_only.md)
- [Dataclass vs NamedTuple vs attrs](dataclasses/comparison.md)
- [Practical Patterns](dataclasses/practical_patterns.md)

## 6.13 Enumerations

- [Enum Basics](enum/enum_basics.md)
- [Enum Members and Values](enum/members_values.md)
- [IntEnum and StrEnum](enum/int_str_enum.md)
- [Flag and IntFlag](enum/flag.md)
- [auto() Function](enum/auto.md)
- [Enum Methods and Customization](enum/methods_customization.md)
- [Enum Practical Patterns](enum/practical_patterns.md)

## 6.14 Abstract Base Classes

- [ABC and abstractmethod](abc/abstract_base_classes.md)
- [typing.Protocol](abc/typing_protocol.md)
- [collections.abc](abc/collections_abc.md)
- [Virtual Subclasses (register)](abc/virtual_subclasses.md)

## 6.15 Metaclasses

- [Metaclasses Introduction](metaclasses/metaclasses_intro.md)
- [\_\_init\_subclass\_\_](metaclasses/init_subclass.md)

## 6.16 OOP Projects

- [Task Management System](projects/task_management_project.md)
- [User Authentication System](projects/user_auth_project.md)
- [RPG Character System](projects/rpg_character_project.md)
- [Banking System](projects/banking_system_project.md)
- [Notification System](projects/notification_system_project.md)
