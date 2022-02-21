from rest_framework import serializers
from .models import Assignment


class StudentAssignmentSerializer(serializers.ModelSerializer):
    """
    Student Assignment serializer
    """
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):
        if 'grade' in attrs and attrs['grade']:
            raise serializers.ValidationError('Student cannot set grade for assignment')

        if 'state' in attrs:
            if attrs['state'] == 'GRADED':
                raise serializers.ValidationError('Student cannot set state to GRADED')
            if attrs['state'] == 'SUBMITTED' and not ('teacher' in attrs and attrs['teacher']):
                raise serializers.ValidationError('Teacher ID has to be sent to set state to SUBMITTED')

        if self.partial:
            return attrs

        return super().validate(attrs)

