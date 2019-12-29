from django import forms

##CSV Download Form##
# SR_ColumnVariables = ['Remoteness Index', "Total Number of Learners Receiving CCT's", "Percentage of Students Recieving CCT's",
# 'Water Access', 'Internet Access', 'Electricty Access', 'Total Number of Learners with Gender Distribution', "Total Number of Learners With Disability"]
# FAVORITE_COLORS_CHOICES = [
#     ('blue', 'Blue'),
#     ('green', 'Green'),
#     ('black', 'Black'),
# ]

SR_ColumnVariables = [
        ('remoteness', 'Remoteness Index'),
        ('total_reci', "Total Number of Learners Receiving CCT's"),
        ('cct_percen', "Percentage of Students Recieving CCT's"),
        ('original_w', "Water Access"),
        ('original_i', "Internet Access"),
        ('original_e', "Electricty Access"),
        ('total_enro', "Total Number of Learners with Gender Distribution"),
        ('pwd_total', "Total Number of Learners With Disability"),
    ]

class SimpleForm(forms.Form):
    # school_year = forms.DateField(widget=forms.SelectDateWidget(years=[2015, 2016, 2017]))
    columns = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=SR_ColumnVariables,
    )


REGION_CHOICES = [
    ('ARMM', 'ARMM'),
    ('CAR', 'CAR'),
    ('NCR', 'NCR'),
    ('Region I', 'Region I'),
    ('Region II', 'Region II'),
    ('Region III', 'Region III'),
    ('Region IV-A', 'Region IV-A'),
    ('Region IV-B', 'Region IV-B'),
    ('Region IVA', 'Region IVA'),
    ('Region IVB', 'Region IVB'),
    ('Region IX', 'Region IX'),
    ('Region V', 'Region V'),
    ('Region VI', 'Region VI'),
    ('Region VII', 'Region VII'),
    ('Region VIII', 'Region VIII'),
    ('Region X', 'Region X'),
    ('Region XI', 'Region XI'),
    ('Region XII', 'Region XII'),
    ('Region XIII', 'Region XIII'),
    ]

class RegionForm(forms.Form):
    region_choice = forms.CharField(label='Select a Region', widget=forms.Select(choices=REGION_CHOICES))
