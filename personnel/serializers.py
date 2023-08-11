from rest_framework import serializers
from .models import Department, Personnel


class DepartmentSerializer(serializers.ModelSerializer):
    personnel_count = serializers.SerializerMethodField()
    # class Meta:
    #     model = Department
    #     fields = '__all__'
    class Meta:
        model = Department
        fields = (
            'name',
            'personnel_count'
        )
    
    def get_personnel_count(self,obj):
        return Personnel.objects.filter(department_id = obj.id).count()


class PersonnelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Personnel
        fields = ('first_name',
                  'last_name',
                  'title')


class DepartmentPersonnelSerializer(serializers.ModelSerializer):

    personnel = PersonnelSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('id', 'name', 'personnel')