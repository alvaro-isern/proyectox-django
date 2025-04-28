from django.db import models
from app_engineers.models import Person, Engineer, DepartmentalCouncil

# Create your models here.
class Event(models.Model):
    event_type = models.ForeignKey('EventType', on_delete=models.CASCADE, related_name='events', verbose_name="Event Type")
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, related_name='events', verbose_name="Entity")
    title = models.CharField(max_length=100, verbose_name="Event Title")
    description = models.TextField(verbose_name="Event Description", null=True, blank=True)
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    modality = models.CharField(max_length=50, verbose_name="Modality", null=True, blank=True, choices=[
        (1, 'PRESENCIAL'),
        (2, 'VIRTUAL'),
        (3, 'HÍBRIDO'),
    ])
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='events', verbose_name="Room")
    fee = models.ForeignKey('Fee', on_delete=models.CASCADE, related_name='events', verbose_name="Fee")

    class Meta:
        db_table = 'events'
        ordering = ['start_date']
        verbose_name = "Event"
        verbose_name_plural = "Events"

class EventType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Event Type Name")
    description = models.TextField(verbose_name="Description", null=True, blank=True)

    class Meta:
        db_table = 'event_types'
        ordering = ['name']
        verbose_name = "Event Type"
        verbose_name_plural = "Event Types"

class Entity(models.Model):
    name = models.CharField(max_length=100, verbose_name="Entity Name")
    entity_type = models.CharField(max_length=50, verbose_name="Entity Type", choices=[
        (1, 'PÚBLICA'),
        (2, 'PRIVADA'),
    ])
    ruc = models.CharField(max_length=20, verbose_name="RUC", null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name="Address", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Phone", null=True, blank=True)
    email = models.EmailField(verbose_name="Email", null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', verbose_name="Logo", null=True, blank=True)

    class Meta:
        db_table = 'entities'
        ordering = ['name']
        verbose_name = "Entity"
        verbose_name_plural = "Entities"

class Room(models.Model):
    departament_council = models.ForeignKey(DepartmentalCouncil, on_delete=models.CASCADE, related_name='rooms', verbose_name="Departmental Council")
    name = models.CharField(max_length=50, verbose_name="Room Name")
    type = models.CharField(max_length=50, verbose_name="Room Type", choices=[
        (1, 'AUDITORIO'),
        (2, 'SALÓN DE CLASES'),
        (3, 'OFICINA'),
        (4, 'OTRO'),
    ])
    capacity = models.IntegerField(verbose_name="Capacity")
    location = models.CharField(max_length=100, verbose_name="Location", null=True, blank=True)
    equipment = models.TextField(verbose_name="Equipment", null=True, blank=True)
    hour_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Hour Fee")
    rental_available = models.BooleanField(default=True, verbose_name="Rental Available")
    status = models.CharField(max_length=20, verbose_name="Status", choices=[
        (1, 'DISPONIBLE'),
        (2, 'OCUPADO'),
        (3, 'EN MANTENIMIENTO'),
    ])

    class Meta:
        db_table = 'rooms'
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

class Fee(models.Model):
    participant_type = models.CharField(max_length=50, verbose_name="Participant Type", choices=[
        (1, 'EXTERNO'),
        (2, 'INTERNO'),
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date", null=True, blank=True)
    group_discount = models.BooleanField(default=False, verbose_name="Group Discount")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Discount Percentage", null=True, blank=True)
    group_min = models.IntegerField(verbose_name="Group Minimum", null=True, blank=True)
    desciption = models.TextField(verbose_name="Description", null=True, blank=True)


    class Meta:
        db_table = 'fees'
        verbose_name = "Fee"
        verbose_name_plural = "Fees"

class EventInscription(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='inscriptions', verbose_name="Event")
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name='inscriptions', verbose_name="Participant")
    inscription_date = models.DateField(verbose_name="Inscription Date")
    payment_required = models.BooleanField(default=True, verbose_name="Payment Required")
    inscription_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Inscription Cost", null=True, blank=True)

    class Meta:
        db_table = 'event_inscriptions'
        ordering = ['inscription_date']
        verbose_name = "Event Inscription"
        verbose_name_plural = "Event Inscriptions"

class Participant(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='participants', verbose_name="Person")
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name='participants', verbose_name="Engineer", null=True, blank=True)
    partipant_type = models.CharField(max_length=50, verbose_name="Participant Type", choices=[
        (1, 'EXTERNO'),
        (2, 'INTERNO'),
    ])
    study_center_type = models.CharField(max_length=50, verbose_name="Study Center Type", choices=[
        (1, 'UNIVERSIDAD'),
        (2, 'INSTITUTO'),
        (3, 'OTRO'),
    ])
    institution_name = models.CharField(max_length=50, null=True, blank=True)
    carreer = models.CharField(max_length=50, null=True, blank=True)
    register_date = models.DateField(verbose_name="Register Date")

    class Meta:
        db_table = 'participants'
        ordering = ['register_date']
        verbose_name = "Participant"
        verbose_name_plural = "Participants"

class CertificateSignature(models.Model):
    executive = models.ForeignKey('Executive', on_delete=models.CASCADE, related_name='signatures', verbose_name="Executive")
    position = models.CharField(max_length=50, verbose_name="Position", null=True, blank=True)
    full_name = models.CharField(max_length=100, verbose_name="Full Name", null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name="Title", null=True, blank=True)
    signature_image = models.ImageField(upload_to='signatures/', verbose_name="Signature Image", null=True, blank=True)
    active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        db_table = 'certificate_signatures'
        verbose_name = "Certificate Signature"
        verbose_name_plural = "Certificate Signatures"

class ConfigSignature(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='config_signatures', verbose_name="Event")
    main_signature = models.ForeignKey('CertificateSignature', on_delete=models.CASCADE, related_name='main_signatures', verbose_name="Main Signature")
    secondary_signature = models.ForeignKey('CertificateSignature', on_delete=models.CASCADE, related_name='secondary_signatures', verbose_name="Secondary Signature")
    additional_signature = models.ForeignKey('CertificateSignature', on_delete=models.CASCADE, related_name='third_signatures', verbose_name="Third Signature", null=True, blank=True)

    class Meta:
        db_table = 'config_signatures'
        verbose_name = "Config Signature"
        verbose_name_plural = "Config Signatures"

class EventCertificate(models.Model):
    event_asistent = models.ForeignKey('EventAsistent', on_delete=models.CASCADE, related_name='certificates', verbose_name="Event Assistant", null=True, blank=True)
    event_speaker = models.ForeignKey('EventSpeaker', on_delete=models.CASCADE, related_name='certificates', verbose_name="Event Speaker", null=True, blank=True)
    code = models.CharField(max_length=50, verbose_name="Certificate Code")
    issue_date = models.DateField(verbose_name="Issue Date")
    certificate_type = models.CharField(max_length=50, verbose_name="Certificate Type", choices=[
        (1, 'ASISTENCIA'),
        (2, 'PARTICIPACIÓN'),
        (3, 'EXPOSICIÓN'),
        (4, 'OTROS'),
    ])
    certificate_url = models.URLField(verbose_name="Certificate URL", null=True, blank=True)
    configuration_signature = models.ForeignKey('ConfigSignature', on_delete=models.CASCADE, related_name='certificates', verbose_name="Configuration Signature")
    certificate_text = models.TextField(verbose_name="Certificate Text", null=True, blank=True)
    certificate_template = models.CharField(max_length=50, verbose_name="Certificate Template", null=True, blank=True)

    class Meta:
        db_table = 'event_certificates'
        ordering = ['issue_date']
        verbose_name = "Event Certificate"
        verbose_name_plural = "Event Certificates"

class EventAsistent(models.Model):
    inscription = models.ForeignKey(EventInscription, on_delete=models.CASCADE, related_name='assistants', verbose_name="Event Inscription")
    date = models.DateField(verbose_name="Date")
    entry_time = models.TimeField(verbose_name="Entry Time", null=True, blank=True)
    exit_time = models.TimeField(verbose_name="Exit Time", null=True, blank=True)
    observations = models.TextField(verbose_name="Observations", null=True, blank=True)

    class Meta:
        db_table = 'event_assistants'
        ordering = ['date']
        verbose_name = "Event Assistant"
        verbose_name_plural = "Event Assistants"

class Speaker(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='speakers', verbose_name="Person")
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name='speakers', verbose_name="Engineer", null=True, blank=True)
    institution_origin = models.CharField(max_length=50, verbose_name="Institution Origin", null=True, blank=True)
    position = models.CharField(max_length=50, verbose_name="Position", null=True, blank=True)
    bio = models.TextField(verbose_name="Biography", null=True, blank=True)
    academic_level = models.CharField(max_length=50, verbose_name="Academic Level", choices=[
        (1, 'BACHILLER'),
        (2, 'TITULADO'),
        (3, 'MAESTRÍA'),
        (4, 'DOCTORADO'),
        (5, 'POSTDOCTORADO'),
        (6, 'OTRO'),
    ])
    professional_profile = models.TextField(verbose_name="Professional Profile", null=True, blank=True)

    class Meta:
        db_table = 'speakers'
        verbose_name = "Speaker"
        verbose_name_plural = "Speakers"

class EventSpeaker(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='speakers', verbose_name="Event")
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, related_name='event_speakers', verbose_name="Speaker")
    topic = models.CharField(max_length=100, verbose_name="Topic", null=True, blank=True)
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    date = models.DateField(verbose_name="Date")
    start_time = models.TimeField(verbose_name="Start Time", null=True, blank=True)
    end_time = models.TimeField(verbose_name="End Time", null=True, blank=True)
    orden = models.IntegerField(verbose_name="Order", null=True, blank=True)
    material = models.FileField(upload_to='materials/', verbose_name="Material", null=True, blank=True)

    class Meta:
        db_table = 'event_speakers'
        ordering = ['start_time']
        verbose_name = "Event Speaker"
        verbose_name_plural = "Event Speakers"

class Executive(models.Model):
    enfineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name='executives', verbose_name="Engineer")
    position = models.ForeignKey('Position', on_delete=models.CASCADE, related_name='executives', verbose_name="Position")
    period = models.ForeignKey('Period', on_delete=models.CASCADE, related_name='executives', verbose_name="Period")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date", null=True, blank=True)
    type_entity = models.CharField(max_length=50, verbose_name="Entity Type", choices=[
        (1, 'PÚBLICA'),
        (2, 'PRIVADA'),
    ])
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, related_name='executives', verbose_name="Entity")
    status = models.CharField(max_length=20, verbose_name="Status", choices=[
        (1, 'ACTIVO'),
        (2, 'INACTIVO'),
    ])

    class Meta:
        db_table = 'executives'
        verbose_name = "Executive"
        verbose_name_plural = "Executives"

class Position(models.Model):
    name = models.CharField(max_length=50, verbose_name="Position Name")
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    level = models.CharField(max_length=50, verbose_name="Level", choices=[
        (1, 'NACIONAL'),
        (2, 'DEPARTAMENTAL'),
        (3, 'LOCAL'),
    ])
    type_organ = models.CharField(max_length=50, verbose_name="Organ Type", choices=[
        (1, 'PÚBLICA'),
        (2, 'PRIVADA'),
    ])

    class Meta:
        db_table = 'positions'
        verbose_name = "Position"
        verbose_name_plural = "Positions"

class Period(models.Model):
    name = models.CharField(max_length=50, verbose_name="Period Name")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    status = models.CharField(max_length=20, verbose_name="Status", choices=[
        (1, 'ACTIVO'),
        (2, 'INACTIVO'),
    ])

    class Meta:
        db_table = 'periods'
        verbose_name = "Period"
        verbose_name_plural = "Periods"
