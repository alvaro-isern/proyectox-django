# from rest_framework import serializers
# from app_engineers.models import (
#     Member, MemberInfo, DocumentType, Country,
#     CollegiateType, DepartmentalCouncil, Chapter, Person
# )
# from django.contrib.auth.models import User
#
#
# class MembersSerializer(serializers.ModelSerializer):
#     """Serializador para el modelo Member."""
#     # person attributes
#     names = serializers.CharField(required=True)
#     paternal_surname = serializers.CharField(required=True)
#     maternal_surname = serializers.CharField(required=True)
#     document_number = serializers.CharField(required=True)
#     email = serializers.EmailField(required=True)
#     cellphone = serializers.CharField(required=True)
#     address = serializers.CharField(required=False)
#     birth_date = serializers.DateField(required=False)
#     photo = serializers.ImageField(required=False)
#     document_type = serializers.IntegerField(required=True)
#     country_code = serializers.IntegerField(required=True)
#
#     # user attributes
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True, write_only=True)
#
#     # member attributes
#     collegiate_code = serializers.CharField(required=True)
#     status = serializers.BooleanField(read_only=True)
#
#     # member info attributes
#     chapter = serializers.IntegerField(required=True)
#     departmental_council = serializers.IntegerField(required=True)
#     collegiate_type = serializers.IntegerField(required=True)
#
#     class Meta:
#         model = Member
#         fields = [
#             'id',
#             'status',
#             'collegiate_code',
#             'paternal_surname',
#             'maternal_surname',
#             'names',
#             'document_type',
#             'document_number',
#             'country_code',
#             'email',
#             'cellphone',
#             'photo',
#             'birth_date',
#             'address',
#             'chapter',
#             'departmental_council',
#             'collegiate_type',
#             'username',
#             'password',
#         ]
#         read_only_fields = ['id']
#
#     def validate_required_field(self, field_name, field_value, model_class, error_message):
#         """Método auxiliar para validar campos requeridos"""
#         if not field_value:
#             raise serializers.ValidationError(
#                 {field_name: "Este campo es obligatorio."})
#         try:
#             return model_class.objects.get(id=field_value)
#         except model_class.DoesNotExist:
#             raise serializers.ValidationError({field_name: error_message})
#
#     def _get_related_objects(self, validated_data):
#         """Obtiene y valida todos los objetos relacionados"""
#         fields_to_validate = {
#             'document_type': (DocumentType, "Tipo de documento no válido."),
#             'country_code': (Country, "País no válido."),
#             'chapter': (Chapter, "Capítulo no válido."),
#             'collegiate_type': (CollegiateType, "Tipo de colegiado no válido."),
#             'departmental_council': (DepartmentalCouncil, "Consejo departamental no válido.")
#         }
#
#         result = {}
#         for field, (model_class, error_message) in fields_to_validate.items():
#             result[field] = self.validate_required_field(
#                 field,
#                 validated_data.pop(field, None),
#                 model_class,
#                 error_message
#             )
#         return result
#
#     def create(self, validated_data):
#         # Obtener y validar objetos relacionados
#         related_objects = self._get_related_objects(validated_data)
#
#         # Crear usuario
#         user = User.objects.create_user(
#             username=validated_data.pop('username'),
#             email=validated_data.pop('email'),
#             password=validated_data.pop('password')
#         )
#
#         # Crear persona
#         person = Person.objects.create(
#             paternal_surname=validated_data.pop('paternal_surname'),
#             maternal_surname=validated_data.pop('maternal_surname'),
#             names=validated_data.pop('names'),
#             document_type=related_objects['document_type'],
#             doc_number=validated_data.pop('document_number'),
#             email=user.email,
#             country=related_objects['country_code'],
#             cellphone=validated_data.pop('cellphone'),
#             address=validated_data.pop('address', None),
#             birth_date=validated_data.pop('birth_date', None),
#             photo=validated_data.pop('photo', None),
#             user=user
#         )
#
#         # Crear miembro
#         member = Member.objects.create(
#             person=person,
#             colligiate_code=validated_data.pop('collegiate_code'),
#             status=True
#         )
#
#         # Crear información del miembro
#         MemberInfo.objects.create(
#             member=member,
#             collegiate_type=related_objects['collegiate_type'],
#             dept_council=related_objects['departmental_council'],
#             chapter=related_objects['chapter']
#         )
#
#         return member
#
#     def to_representation(self, instance):
#         """Representación personalizada del objeto para el formulario"""
#         person = instance.person
#         member_info = instance.member_info.first()
#
#         return {
#             'id': instance.id,
#             'status': instance.status,
#             'collegiate_code': instance.colligiate_code,
#             'paternal_surname': person.paternal_surname,
#             'maternal_surname': person.maternal_surname,
#             'names': person.names,
#             'document_type': getattr(person.document_type, 'id', None),
#             'document_number': person.doc_number,
#             'email': person.email,
#             'country_code': getattr(person.country, 'id', None),
#             'cellphone': person.cellphone,
#             'photo': person.photo.url if person.photo else None,
#             'birth_date': person.birth_date,
#             'address': person.address,
#             'chapter': getattr(member_info.chapter, 'id', None) if member_info else None,
#             'departmental_council': getattr(member_info.dept_council, 'id', None) if member_info else None,
#             'collegiate_type': getattr(member_info.collegiate_type, 'id', None) if member_info else None,
#             'username': person.user.username
#         }
#
#     def update(self, instance, validated_data):
#         # Actualizar datos del usuario
#         if 'username' in validated_data or 'email' in validated_data:
#             user = instance.person.user
#             if 'username' in validated_data:
#                 user.username = validated_data.pop('username')
#             if 'email' in validated_data:
#                 user.email = validated_data.pop('email')
#             if 'password' in validated_data:
#                 user.set_password(validated_data.pop('password'))
#             user.save()
#
#         # Actualizar datos de la persona
#         person = instance.person
#         person_fields = {
#             'paternal_surname': 'paternal_surname',
#             'maternal_surname': 'maternal_surname',
#             'names': 'names',
#             'document_number': 'doc_number',
#             'cellphone': 'cellphone',
#             'address': 'address',
#             'birth_date': 'birth_date',
#             'photo': 'photo'
#         }
#
#         for field, person_field in person_fields.items():
#             if field in validated_data:
#                 setattr(person, person_field, validated_data.pop(field))
#
#         # Actualizar relaciones de la persona
#         if 'document_type' in validated_data:
#             person.document_type = self.validate_required_field(
#                 'document_type',
#                 validated_data.pop('document_type'),
#                 DocumentType,
#                 "Tipo de documento no válido."
#             )
#         if 'country_code' in validated_data:
#             person.country = self.validate_required_field(
#                 'country_code',
#                 validated_data.pop('country_code'),
#                 Country,
#                 "País no válido."
#             )
#
#         person.save()
#
#         # Actualizar datos del miembro
#         if 'collegiate_code' in validated_data:
#             instance.colligiate_code = validated_data.pop('collegiate_code')
#         if 'status' in validated_data:
#             instance.status = validated_data.pop('status')
#         instance.save()
#
#         # Actualizar información del miembro
#         member_info = instance.member_info.first()
#         if member_info:
#             if 'chapter' in validated_data:
#                 member_info.chapter = self.validate_required_field(
#                     'chapter',
#                     validated_data.pop('chapter'),
#                     Chapter,
#                     "Capítulo no válido."
#                 )
#             if 'departmental_council' in validated_data:
#                 member_info.dept_council = self.validate_required_field(
#                     'departmental_council',
#                     validated_data.pop('departmental_council'),
#                     DepartmentalCouncil,
#                     "Consejo departamental no válido."
#                 )
#             if 'collegiate_type' in validated_data:
#                 member_info.collegiate_type = self.validate_required_field(
#                     'collegiate_type',
#                     validated_data.pop('collegiate_type'),
#                     CollegiateType,
#                     "Tipo de colegiado no válido."
#                 )
#             member_info.save()
#
#         return instance
#
#     def destroy(self, instance):
#         """Realiza una eliminación lógica del colegiado."""
#         try:
#             # Asumiendo que el estado inactivo tiene id=1
#             inactive = Status.objects.get(id=1)
#         except Status.DoesNotExist:
#             raise serializers.ValidationError(
#                 {"status": "El estado no existe en la base de datos."}
#             )
#
#         instance.delete_logical()
#         return True
