from attr import attr
from rest_framework import serializers
from apps.students.models import Assignment
from apps.teachers.models import Teacher

class TeacherAssignmentSerializer(serializers.ModelSerializer):
    """
    Teacher Assignment serializer
    """
    
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):
        """
        validates Whether grade is in data
        whether grade is one of A,B,C or D
        and whether content is in data
        """
        
        state = {
            'DRAFT':'SUBMITTED assignments can only be graded',
            'GRADED':'GRADED assignments cannot be graded again'
        }
        
        
        if 'student' in attrs and attrs['student'] != self.instance.student.id:
            raise serializers.ValidationError('Teacher cannot change the student who submitted the assignment')

        if 'content' in attrs:
            raise serializers.ValidationError('Teacher cannot change the content of the assignment')
        
        
        if 'grade' not in attrs or attrs['grade']=='':
            raise serializers.ValidationError('No Grade has been Provided')

        
        if self.instance.state in state:
            raise serializers.ValidationError(state[self.instance.state])
        
        
        if self.instance.teacher != attrs['teacher']:
            raise serializers.ValidationError('Teacher cannot grade for other teacher''s assignment')

        
        try:
            if 65<ord(attrs['grade']) or ord(attrs['grade'])>68:
                raise serializers.ValidationError('Grade has to be between A and D')
        except TypeError:
            raise serializers.ValidationError('Grade has to be between A and D')
        
        
        if self.partial:
            return attrs

        return super().validate(attrs)


    def update(self,instance,validated_data): 
        
        grade = validated_data.pop('grade')
        
        instance.grade = grade
        instance.state = 'GRADED'
        
        instance.save()
        
        return instance