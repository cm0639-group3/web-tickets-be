from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

class CaseInsensitiveSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        # Case-insensitive lookup for the related field
        case_insensitive_lookup = {f'{self.slug_field}__iexact': data}
        try:
            return self.queryset.get(**case_insensitive_lookup)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=data)
        except (TypeError, ValueError):
            self.fail('invalid')
