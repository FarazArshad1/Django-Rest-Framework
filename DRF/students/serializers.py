from rest_framework import serializers
from .models import Students
from datetime import datetime
import re

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = "__all__"

    def validate_batch(self, value):
        current_year = datetime.now().year
        if value < 2000 or value > current_year:
            raise serializers.ValidationError(
                f"Batch year must be between 2000 and {current_year}."
            )

    def validate_roll_number(self, value):
        # Enforce format like F25AB001
        pattern = r"^F\d{2}(AB|BB)\d{3}$"
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Roll number must follow format F{last two digits of batch}{AB or BB}{three digits}, e.g., F25AB123"
            )
        return value

    def validate(self, attrs):
        batch = attrs.get("batch")
        roll_number = attrs.get("roll_number")

        # Optional cross-field check:
        if batch and roll_number:
            year_digits = str(batch)[-2:]
            if not roll_number.startswith(f"F{year_digits}"):
                raise serializers.ValidationError(
                    {"roll_number": "Roll number must match the batch year prefix."}
                )
        return attrs
