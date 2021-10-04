
from rest_framework import serializers

from .models import DataSampleView

class DataSampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataSampleView
        fields = ( 'id','col0', 'col1', 'col2', 'col3', 'col4', 'col5',
                   'col6', 'col7', 'col8', 'col9', 'col10', 'col11',
                   'col12', 'col13', 'col14', 'col15', 'col16', 'col17',
                   'col18', 'col19', 'col20', 'col21', 'col22', 'col23',
                   'col24', 'col25', 'col26', 'col27', 'col28', 'col29',
                   'col30', 'col31', 'col32', 'col33', 'col34', 'col35',
                   'col36', 'col37', 'col38', 'col39', 'col40', 'col41',
                   'col42', 'col43', 'col44', 'col45', 'col46', 'col47',
                   'col48', 'col49', 'col50', 'col51')
